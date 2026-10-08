#!/usr/bin/env python3
"""Generate a documentation-oriented inventory of project changes.

This script is intentionally conservative: it does not edit files. It helps the
skill decide which code and documentation files must be read before updating the
project documentation.
"""

from __future__ import annotations

import argparse
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DOC_PATH = "src/app/main/pages/code-documentation"


@dataclass(frozen=True)
class ChangedFile:
    status: str
    path: str
    category: str
    documentation_targets: tuple[str, ...]


def run_git(root: Path, args: list[str]) -> tuple[int, str]:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        return completed.returncode, completed.stdout.strip()
    except FileNotFoundError:
        return 127, "git command not found"


def is_git_repo(root: Path) -> bool:
    code, output = run_git(root, ["rev-parse", "--is-inside-work-tree"])
    return code == 0 and output.splitlines()[-1:] == ["true"]


def classify(path: str) -> tuple[str, tuple[str, ...]]:
    normalized = path.replace("\\", "/")
    targets: list[str] = []

    if normalized.startswith(".claude/skills/"):
        return "skill", ("code-documentation.component.ts/html", "docs/10-best-practices.md")

    if normalized.startswith(DOC_PATH):
        if "/docs/" in normalized:
            return "documentation-markdown", ("docs/*.md", "README.md")
        if "/examples/" in normalized:
            return "documentation-example", ("examples/*", "docs/*.md")
        if "/schemas/" in normalized:
            return "documentation-schema", ("schemas/*.json", "docs/02-module-configuration.md")
        if normalized.endswith(".component.ts"):
            return "documentation-angular-ts", ("navSections", "snippets", "HTML anchors")
        if normalized.endswith(".component.html"):
            return "documentation-angular-html", ("HTML sections", "navSections")
        if normalized.endswith(".component.scss"):
            return "documentation-angular-style", ("SCSS classes",)
        return "documentation", (DOC_PATH,)

    if "/routes" in normalized or normalized.endswith("routing.module.ts") or "app-routing" in normalized:
        return "structure-routing", ("architecture", "README.md", "docs/01-getting-started.md")

    if "/components/" in normalized or normalized.endswith(".component.ts"):
        targets.extend(["component section", "Inputs/Outputs", "examples"])
        return "code-component", tuple(targets)

    if "/services/" in normalized or normalized.endswith(".service.ts"):
        return "code-service", ("services/API docs", "docs/07-services-api.md", "examples")

    if normalized.endswith("types.ts") or "/types/" in normalized or normalized.endswith(".interface.ts"):
        return "code-types", ("types section", "schemas/*.json", "docs/02-module-configuration.md")

    if "/modules/" in normalized:
        return "structure-module", ("modules-list", "architecture", "docs/01-getting-started.md")

    if normalized.endswith((".html", ".scss")):
        return "ui-template-style", ("component docs", "examples")

    if normalized.endswith(".json"):
        return "configuration", ("documentation.angular-style.json", "schemas/*.json", "README.md")

    if normalized.endswith(".md"):
        return "markdown", ("README/docs consistency",)

    return "other", ("manual review",)


def parse_name_status(output: str) -> list[ChangedFile]:
    changes: list[ChangedFile] = []
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = line.split("\t")
        status = parts[0]
        path = parts[-1]
        category, targets = classify(path)
        changes.append(ChangedFile(status=status, path=path, category=category, documentation_targets=targets))
    return changes


def parse_status_short(output: str) -> list[ChangedFile]:
    changes: list[ChangedFile] = []
    for raw_line in output.splitlines():
        if not raw_line.strip():
            continue
        status = raw_line[:2].strip() or "?"
        path = raw_line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        category, targets = classify(path)
        changes.append(ChangedFile(status=status, path=path, category=category, documentation_targets=targets))
    return changes


def unique_changes(*groups: Iterable[ChangedFile]) -> list[ChangedFile]:
    seen: set[str] = set()
    result: list[ChangedFile] = []
    for group in groups:
        for item in group:
            key = item.path
            if key not in seen:
                seen.add(key)
                result.append(item)
    return result


def fallback_tree(root: Path, scope: str) -> list[str]:
    base = root if scope == "all" else root / scope
    if not base.exists():
        return [f"scope not found: {scope}"]

    ignored = {"node_modules", ".git", "dist", "build", ".angular", "coverage"}
    useful_suffixes = {".ts", ".html", ".scss", ".json", ".md", ".py"}
    files: list[str] = []

    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in ignored]
        for filename in filenames:
            path = Path(dirpath) / filename
            if path.suffix in useful_suffixes or filename in {"SKILL.md", "README.md"}:
                try:
                    files.append(str(path.relative_to(root)).replace("\\", "/"))
                except ValueError:
                    files.append(str(path))
        if len(files) >= 300:
            files.append("... tree truncated after 300 files")
            break
    return files


def render_markdown(root: Path, since: str | None, scope: str, changes: list[ChangedFile], git_available: bool, diff_stat: str, tree: list[str]) -> str:
    lines: list[str] = []
    lines.append("# Documentation change inventory")
    lines.append("")
    lines.append(f"- Root: `{root}`")
    lines.append(f"- Scope: `{scope}`")
    lines.append(f"- Git available: `{git_available}`")
    lines.append(f"- Since: `{since or 'not provided'}`")
    lines.append("")

    if changes:
        lines.append("## Changed files by documentation category")
        lines.append("")
        grouped: dict[str, list[ChangedFile]] = {}
        for change in changes:
            grouped.setdefault(change.category, []).append(change)
        for category in sorted(grouped):
            lines.append(f"### {category}")
            lines.append("")
            for change in grouped[category]:
                targets = ", ".join(f"`{target}`" for target in change.documentation_targets)
                lines.append(f"- `{change.status}` `{change.path}` -> {targets}")
            lines.append("")
    else:
        lines.append("## Changed files")
        lines.append("")
        lines.append("No Git changes detected. Use the structure snapshot below for a full documentation review.")
        lines.append("")

    if diff_stat:
        lines.append("## Git diff stat")
        lines.append("")
        lines.append("```text")
        lines.append(diff_stat)
        lines.append("```")
        lines.append("")

    if tree:
        lines.append("## Structure snapshot")
        lines.append("")
        lines.append("```text")
        lines.extend(tree)
        lines.append("```")
        lines.append("")

    lines.append("## Recommended next reads")
    lines.append("")
    if changes:
        for change in changes[:50]:
            lines.append(f"- Read `{change.path}` and update targets: {', '.join(change.documentation_targets)}")
    else:
        lines.append(f"- Read `{DOC_PATH}/README.md`")
        lines.append(f"- Read `{DOC_PATH}/code-documentation.component.ts`")
        lines.append(f"- Read `{DOC_PATH}/code-documentation.component.html`")
        lines.append("- Read the main module/component files under the requested scope")

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a documentation-oriented project change inventory.")
    parser.add_argument("--root", default=".", help="Project root directory.")
    parser.add_argument("--since", default=None, help="Optional Git ref to compare against.")
    parser.add_argument("--scope", default="all", help="Scope path to include in the structure snapshot.")
    parser.add_argument("--out", default=None, help="Optional markdown output path.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    git_available = is_git_repo(root)
    changes: list[ChangedFile] = []
    diff_stat = ""

    if git_available:
        if args.since:
            _, name_status = run_git(root, ["diff", "--name-status", args.since, "--"])
            _, diff_stat = run_git(root, ["diff", "--stat", args.since, "--"])
            changes = parse_name_status(name_status)
        else:
            _, status_short = run_git(root, ["status", "--short"])
            _, diff_names = run_git(root, ["diff", "--name-status", "--"])
            _, diff_stat = run_git(root, ["diff", "--stat", "--"])
            changes = unique_changes(parse_status_short(status_short), parse_name_status(diff_names))

    tree = fallback_tree(root, args.scope)
    markdown = render_markdown(root, args.since, args.scope, changes, git_available, diff_stat, tree)

    if args.out:
        out_path = Path(args.out)
        if not out_path.is_absolute():
            out_path = root / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(markdown, encoding="utf-8")
        print(str(out_path))
    else:
        print(markdown)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
