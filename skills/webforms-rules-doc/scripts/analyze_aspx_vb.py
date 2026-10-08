#!/usr/bin/env python3
"""
Static analyzer for ASP.NET WebForms / VB.NET business-rule documentation.

It reads source text files only. It does not run the application and does not
modify the analyzed source files.

Usage:
  python analyze_aspx_vb.py <folder-or-files> --out-dir outputs/webforms-rules-doc --redact
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import os
import re
import sys
import zipfile
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

SUPPORTED_EXTENSIONS = {
    ".aspx", ".ascx", ".master", ".vb", ".config", ".sql", ".resx",
    ".asmx", ".ashx", ".svc", ".xml", ".js", ".css", ".vbproj", ".sln"
}
SKIP_DIRS = {"bin", "obj", ".git", ".svn", ".vs", "packages", "node_modules", "temp", "tmp", "logs", "log"}
MAX_FILE_SIZE_BYTES = 3_000_000
MAX_EVIDENCE_PER_CATEGORY = 300

SECRET_PATTERNS = [
    (re.compile(r"(?i)(password\s*=\s*)[^;\s\"']+"), r"\1[SECRET_MASKED]"),
    (re.compile(r"(?i)(pwd\s*=\s*)[^;\s\"']+"), r"\1[SECRET_MASKED]"),
    (re.compile(r"(?i)(api[_-]?key\s*[=:]\s*)[^;\s\"']+"), r"\1[SECRET_MASKED]"),
    (re.compile(r"(?i)(token\s*[=:]\s*)[^;\s\"']+"), r"\1[SECRET_MASKED]"),
    (re.compile(r"(?i)(secret\s*[=:]\s*)[^;\s\"']+"), r"\1[SECRET_MASKED]"),
    (re.compile(r"(?i)(connectionString\s*=\s*\")[^\"]+(\")"), r"\1[CONNECTION_STRING_MASKED]\2"),
    (re.compile(r"(?i)(Data Source\s*=\s*)[^;\s\"']+"), r"\1[SERVER_MASKED]"),
    (re.compile(r"(?i)(Server\s*=\s*)[^;\s\"']+"), r"\1[SERVER_MASKED]"),
    (re.compile(r"(?i)(Initial Catalog\s*=\s*)[^;\s\"']+"), r"\1[DB_MASKED]"),
    (re.compile(r"(?i)(User ID\s*=\s*)[^;\s\"']+"), r"\1[USER_MASKED]"),
    (re.compile(r"(?i)(uid\s*=\s*)[^;\s\"']+"), r"\1[USER_MASKED]"),
    (re.compile(r"\\\\[A-Za-z0-9_.-]+\\[A-Za-z0-9_.$ -]+"), r"\\[UNC_PATH_MASKED]"),
    (re.compile(r"(?i)https?://[A-Za-z0-9_.:/?&=%#\-]+"), r"[URL_MASKED]"),
]

PATTERNS: Dict[str, List[re.Pattern[str]]] = {
    "validation": [
        re.compile(r"\bRequiredFieldValidator\b", re.I),
        re.compile(r"\bRegularExpressionValidator\b", re.I),
        re.compile(r"\bRangeValidator\b", re.I),
        re.compile(r"\bCompareValidator\b", re.I),
        re.compile(r"\bCustomValidator\b", re.I),
        re.compile(r"\bValidationGroup\b", re.I),
        re.compile(r"\bPage\.IsValid\b", re.I),
        re.compile(r"\bString\.IsNullOrEmpty\b|\bIsNothing\b|\bIs Nothing\b", re.I),
    ],
    "workflow_condition": [
        re.compile(r"^\s*If\b", re.I),
        re.compile(r"^\s*ElseIf\b", re.I),
        re.compile(r"^\s*Select\s+Case\b", re.I),
        re.compile(r"\bCase\s+", re.I),
        re.compile(r"\b(statut|status|etat|state|workflow|valider|annuler|rejeter|cloturer|clôturer|approuver)\b", re.I),
    ],
    "calculation": [
        re.compile(r"\b(Dim|Set)?\s*\w*(montant|total|somme|prix|taux|taxe|tva|remise|quantite|quantité|solde|budget|plafond)\w*\s*(=|\+=|-=)", re.I),
        re.compile(r"=\s*[^\n]*(\+|-|\*|/)[^\n]*(montant|total|prix|taux|taxe|tva|remise|quantite|solde|budget|plafond)", re.I),
        re.compile(r"\b(Math\.Round|Round|Ceiling|Floor|DateAdd|DateDiff|CDec|CDbl|CInt)\b", re.I),
    ],
    "roles_access": [
        re.compile(r"\b(User\.IsInRole|Roles\.|Thread\.CurrentPrincipal)\b", re.I),
        re.compile(r"\b(role|profil|profile|droit|autorisation|permission|habilitation|groupe)\b", re.I),
        re.compile(r"\bSession\s*\(\s*\"?(role|profil|droit|user|utilisateur|service)", re.I),
    ],
    "ui_behavior": [
        re.compile(r"\.(Visible|Enabled|ReadOnly)\s*=", re.I),
        re.compile(r"\b(Visible|Enabled|ReadOnly)\s*=\s*\"?(true|false)\"?", re.I),
    ],
    "data_access": [
        re.compile(r"\b(SqlConnection|SqlCommand|SqlDataAdapter|DataSet|DataTable|ExecuteNonQuery|ExecuteReader|ExecuteScalar)\b", re.I),
        re.compile(r"\b(SELECT|INSERT|UPDATE|DELETE|EXEC|EXECUTE)\b", re.I),
        re.compile(r"\b(CommandType\.StoredProcedure|StoredProcedure)\b", re.I),
    ],
    "message_error": [
        re.compile(r"\b(MsgBox|alert\(|ValidationSummary|ShowMessage|MessageBox|Throw New|Err\.Raise)\b", re.I),
        re.compile(r"\.(Text|ErrorMessage)\s*=\s*\"", re.I),
        re.compile(r"\bTry\b|\bCatch\b|\bFinally\b", re.I),
    ],
    "configuration": [
        re.compile(r"\bappSettings\b|\bconnectionStrings\b|\bConfigurationManager\b", re.I),
        re.compile(r"\b(AppSettings|ConnectionStrings)\b", re.I),
        re.compile(r"\b(smtp|endpoint|url|path|chemin|report|crystal|rdlc|mail)\b", re.I),
    ],
}

CONTROL_TAG_RE = re.compile(r"<\s*asp:(\w+)[^>]*", re.I)
ID_RE = re.compile(r"\bID\s*=\s*\"([^\"]+)\"", re.I)
CONTROL_TO_VALIDATE_RE = re.compile(r"\bControlToValidate\s*=\s*\"([^\"]+)\"", re.I)
ERROR_MESSAGE_RE = re.compile(r"\bErrorMessage\s*=\s*\"([^\"]+)\"", re.I)
EVENT_RE = re.compile(r"\b(Sub|Function)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", re.I)
HANDLES_RE = re.compile(r"\bHandles\s+(.+)$", re.I)
PROC_RE = re.compile(r"(?i)(?:CommandText\s*=\s*\"|SqlCommand\s*\(\s*\"|EXEC(?:UTE)?\s+)([A-Za-z0-9_\.\[\]]+)")
SQL_TABLE_RE = re.compile(r"(?i)\b(?:FROM|JOIN|UPDATE|INTO)\s+([A-Za-z0-9_\.\[\]]+)")
APPSETTING_RE = re.compile(r"(?i)(?:<add\s+key=\"([^\"]+)\"|AppSettings\s*\(\s*\"([^\"]+)\")")
SESSION_RE = re.compile(r"(?i)Session\s*\(\s*\"([^\"]+)\"\s*\)")


def redact_text(text: str) -> str:
    for pattern, repl in SECRET_PATTERNS:
        text = pattern.sub(repl, text)
    return text


def md(text: Any) -> str:
    return html.escape(str(text), quote=False).replace("|", "\\|")


def safe_read(path: Path) -> str:
    data = path.read_bytes()
    if len(data) > MAX_FILE_SIZE_BYTES:
        data = data[:MAX_FILE_SIZE_BYTES]
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            pass
    return data.decode("latin-1", errors="replace")


def collect_files(inputs: Sequence[Path]) -> Tuple[List[Path], List[str]]:
    files: List[Path] = []
    warnings: List[str] = []
    for source in inputs:
        if not source.exists():
            warnings.append(f"Path not found: {source}")
            continue
        if source.is_file() and source.suffix.lower() == ".zip":
            # Zip support is intentionally shallow and safe.
            tmp_dir = Path(tempfile.mkdtemp(prefix="webforms_rules_zip_"))
            with zipfile.ZipFile(source) as zf:
                for info in zf.infolist():
                    parts = Path(info.filename).parts
                    if info.filename.startswith("/") or ".." in parts:
                        continue
                    zf.extract(info, tmp_dir)
            files.extend(list(iter_source_files(tmp_dir)))
        elif source.is_file():
            if source.suffix.lower() in SUPPORTED_EXTENSIONS:
                files.append(source)
        elif source.is_dir():
            files.extend(list(iter_source_files(source)))
    unique = []
    seen = set()
    for f in files:
        key = str(f.resolve())
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return unique, warnings


def iter_source_files(root: Path) -> Iterable[Path]:
    for current, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d.lower() not in SKIP_DIRS]
        for name in names:
            p = Path(current) / name
            if p.suffix.lower() in SUPPORTED_EXTENSIONS:
                yield p


def common_root(paths: Sequence[Path]) -> Path:
    if not paths:
        return Path.cwd()
    try:
        return Path(os.path.commonpath([str(p.resolve()) for p in paths]))
    except ValueError:
        return Path.cwd()


def rel(p: Path, root: Path) -> str:
    try:
        return str(p.resolve().relative_to(root.resolve())).replace(os.sep, "/")
    except Exception:
        return str(p)


def add_evidence(evidence: Dict[str, List[Dict[str, Any]]], category: str, file_ref: str, line_no: int, line: str) -> None:
    if len(evidence[category]) >= MAX_EVIDENCE_PER_CATEGORY:
        return
    clean = redact_text(line.strip())
    if len(clean) > 260:
        clean = clean[:257] + "..."
    evidence[category].append({"file": file_ref, "line": line_no, "text": clean})


def analyze(inputs: Sequence[Path], redact: bool = True) -> Dict[str, Any]:
    files, warnings = collect_files(inputs)
    root = common_root(files)
    evidence: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    controls: List[Dict[str, Any]] = []
    validators: List[Dict[str, Any]] = []
    events: List[Dict[str, Any]] = []
    procedures: Counter[str] = Counter()
    tables: Counter[str] = Counter()
    sessions: Counter[str] = Counter()
    config_keys: Counter[str] = Counter()
    file_rows: List[Dict[str, Any]] = []

    for path in files:
        file_ref = rel(path, root)
        try:
            text = safe_read(path)
            raw_hash = hashlib.sha1(text.encode("utf-8", errors="ignore")).hexdigest()[:12]
        except Exception as exc:
            warnings.append(f"Read error {file_ref}: {exc}")
            continue
        lines = text.splitlines()
        file_rows.append({"file": file_ref, "extension": path.suffix.lower(), "lines": len(lines), "sha1_12": raw_hash})

        for line_no, line in enumerate(lines, 1):
            scan = line[:2500]
            for category, patterns in PATTERNS.items():
                if any(p.search(scan) for p in patterns):
                    add_evidence(evidence, category, file_ref, line_no, scan)

            if path.suffix.lower() in {".aspx", ".ascx", ".master"}:
                for m in CONTROL_TAG_RE.finditer(scan):
                    tag = m.group(0)
                    cid = ID_RE.search(tag)
                    ctv = CONTROL_TO_VALIDATE_RE.search(tag)
                    emsg = ERROR_MESSAGE_RE.search(tag)
                    item = {
                        "file": file_ref,
                        "line": line_no,
                        "type": m.group(1),
                        "id": cid.group(1) if cid else "",
                        "control_to_validate": ctv.group(1) if ctv else "",
                        "error_message": redact_text(emsg.group(1)) if emsg else "",
                    }
                    controls.append(item)
                    if "Validator" in item["type"]:
                        validators.append(item)

            if path.suffix.lower() == ".vb":
                ev = EVENT_RE.search(scan)
                if ev:
                    handles = HANDLES_RE.search(scan)
                    events.append({
                        "file": file_ref,
                        "line": line_no,
                        "kind": ev.group(1),
                        "name": ev.group(2),
                        "handles": handles.group(1).strip() if handles else "",
                    })

            for m in PROC_RE.finditer(scan):
                procedures[redact_text(m.group(1))] += 1
            for m in SQL_TABLE_RE.finditer(scan):
                tables[redact_text(m.group(1))] += 1
            for m in SESSION_RE.finditer(scan):
                sessions[redact_text(m.group(1))] += 1
            for m in APPSETTING_RE.finditer(scan):
                key = m.group(1) or m.group(2)
                if key:
                    config_keys[redact_text(key)] += 1

    summary = {
        "analyzed_at": dt.datetime.now().isoformat(timespec="seconds"),
        "root": str(root),
        "file_count": len(files),
        "extensions": dict(Counter(row["extension"] for row in file_rows)),
        "warnings": warnings,
    }
    return {
        "summary": summary,
        "files": file_rows,
        "controls": controls[:1000],
        "validators": validators[:1000],
        "events": events[:1000],
        "dependencies": {
            "stored_procedures": procedures.most_common(100),
            "tables": tables.most_common(100),
            "sessions": sessions.most_common(100),
            "config_keys": config_keys.most_common(100),
        },
        "evidence": dict(evidence),
    }


def render_inventory(data: Dict[str, Any]) -> str:
    out = ["# Inventory - WebForms/VB.NET static analysis", ""]
    s = data["summary"]
    out += [
        "## Summary", "",
        f"- Analyzed at: `{md(s['analyzed_at'])}`",
        f"- Root: `{md(s['root'])}`",
        f"- Files analyzed: {s['file_count']}",
        "- Analysis mode: static text analysis only; application code was not executed.",
        "",
        "## Extensions", "",
    ]
    for ext, count in sorted(s["extensions"].items()):
        out.append(f"- `{md(ext)}`: {count}")
    if s.get("warnings"):
        out += ["", "## Warnings", ""]
        out.extend([f"- {md(w)}" for w in s["warnings"]])
    out += ["", "## Files", "", "| File | Extension | Lines | Hash |", "|---|---:|---:|---|"]
    for row in data["files"]:
        out.append(f"| `{md(row['file'])}` | `{md(row['extension'])}` | {row['lines']} | `{row['sha1_12']}` |")
    out += ["", "## WebForms controls", "", "| File | Line | Type | ID | ControlToValidate | ErrorMessage |", "|---|---:|---|---|---|---|"]
    for c in data["controls"][:300]:
        out.append(f"| `{md(c['file'])}` | {c['line']} | {md(c['type'])} | `{md(c['id'])}` | `{md(c['control_to_validate'])}` | {md(c['error_message'])} |")
    out += ["", "## VB.NET events and methods", "", "| File | Line | Kind | Name | Handles |", "|---|---:|---|---|---|"]
    for e in data["events"][:300]:
        out.append(f"| `{md(e['file'])}` | {e['line']} | {md(e['kind'])} | `{md(e['name'])}` | `{md(e['handles'])}` |")
    out += ["", "## Dependencies", ""]
    deps = data["dependencies"]
    for title, key in [("Stored procedures", "stored_procedures"), ("SQL tables/views", "tables"), ("Session keys", "sessions"), ("Config keys", "config_keys")]:
        out += [f"### {title}", ""]
        if deps[key]:
            for name, count in deps[key]:
                out.append(f"- `{md(name)}` ({count})")
        else:
            out.append("- None detected.")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def render_evidence(data: Dict[str, Any]) -> str:
    labels = {
        "validation": "Validation",
        "workflow_condition": "Workflow / Condition",
        "calculation": "Calcul",
        "roles_access": "Rôle / Accès",
        "ui_behavior": "Comportement UI",
        "data_access": "Dépendance SQL / données",
        "message_error": "Message / Erreur",
        "configuration": "Configuration",
    }
    out = ["# Evidence Map - WebForms/VB.NET", "", "| ID | Catégorie | Fichier | Ligne | Extrait masqué | Statut initial |", "|---|---|---|---:|---|---|"]
    idx = 1
    for cat, items in data["evidence"].items():
        for item in items:
            status = "A confirmer" if cat in {"workflow_condition", "calculation", "data_access", "configuration"} else "Candidat"
            out.append(f"| EV-{idx:04d} | {md(labels.get(cat, cat))} | `{md(item['file'])}` | {item['line']} | `{md(item['text'])}` | {status} |")
            idx += 1
    if idx == 1:
        out.append("| - | - | - | - | Aucun élément détecté | - |")
    return "\n".join(out).rstrip() + "\n"


def write_outputs(data: Dict[str, Any], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "analysis.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "inventory.md").write_text(render_inventory(data), encoding="utf-8")
    (out_dir / "evidence-map.md").write_text(render_evidence(data), encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Static WebForms/VB.NET rule evidence analyzer")
    parser.add_argument("paths", nargs="+", help="Folders, files, or zip archives to analyze")
    parser.add_argument("--out-dir", default="outputs/webforms-rules-doc", help="Output directory")
    parser.add_argument("--redact", action="store_true", help="Redact secrets in evidence output")
    args = parser.parse_args(argv)

    input_paths = [Path(p) for p in args.paths]
    data = analyze(input_paths, redact=args.redact)
    # Derive module output folder from first input path.
    first = input_paths[0]
    module = first.stem if first.is_file() else first.name
    module = re.sub(r"[^A-Za-z0-9_.-]+", "_", module or "module")
    out_dir = Path(args.out_dir) / module
    write_outputs(data, out_dir)
    print(f"Analysis written to: {out_dir}")
    print(f"Files analyzed: {data['summary']['file_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
