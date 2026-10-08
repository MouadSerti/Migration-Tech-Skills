#!/usr/bin/env python3
"""Create a new Angular business module by cloning an existing module folder.

The script copies the module structure (ts/html/css/scss/json by default) from a
reference module into a new module folder whose name can be
provided directly or derived from an API title.
"""
import argparse
import re
import shutil
import sys
import unicodedata
from pathlib import Path

DEFAULT_EXTENSIONS = {".ts", ".html", ".scss", ".css", ".json"}


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = value.replace("&", " et ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "nouveau-module"


def copy_module(template_dir: Path, target_dir: Path, extensions: set[str], force: bool, dry_run: bool) -> list[Path]:
    if not template_dir.exists() or not template_dir.is_dir():
        raise SystemExit(f"Template module not found: {template_dir}")
    if target_dir.exists() and any(target_dir.iterdir()) and not force:
        raise SystemExit(f"Target module already exists and is not empty: {target_dir}. Use --force to overwrite.")

    copied: list[Path] = []
    for src in sorted(template_dir.rglob("*")):
        rel = src.relative_to(template_dir)
        dst = target_dir / rel
        if src.is_dir():
            if not dry_run:
                dst.mkdir(parents=True, exist_ok=True)
            continue
        if extensions and src.suffix not in extensions:
            continue
        copied.append(dst)
        if dry_run:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    return copied


def main() -> int:
    parser = argparse.ArgumentParser(description="Clone an Angular module folder from a template module.")
    parser.add_argument("--modules-root", default="src/app/main/modules", help="Angular modules root directory")
    parser.add_argument("--template", required=True, help="Reference module folder name")
    parser.add_argument("--module", help="Target module folder name. If omitted, derived from --title")
    parser.add_argument("--title", help="API title used to derive the target folder name")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files in the target module")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be copied without writing files")
    parser.add_argument("--extensions", default=".ts,.html,.scss,.css,.json", help="Comma-separated extensions to copy")
    args = parser.parse_args()

    module_name = slugify(args.module or args.title or "")
    modules_root = Path(args.modules_root)
    template_dir = modules_root / args.template
    target_dir = modules_root / module_name
    extensions = {e.strip() if e.strip().startswith('.') else f".{e.strip()}" for e in args.extensions.split(',') if e.strip()}

    copied = copy_module(template_dir, target_dir, extensions, args.force, args.dry_run)
    print(f"module_name={module_name}")
    print(f"template_dir={template_dir}")
    print(f"target_dir={target_dir}")
    print(f"files_copied={len(copied)}")
    for p in copied:
        print(p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
