#!/usr/bin/env python3
"""Light validation for generated config.service.ts files."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, Set

REQUIRED_MARKERS = ["TITLE_API", "COLUMNS_API", "ACTIONS_API", "class ConfigService", "getDataApi"]


def fields_from_columns(text: str) -> Set[str]:
    patterns = [
        r'field\s*:\s*["\']([^"\']+)["\']',
        r'["\']field["\']\s*:\s*["\']([^"\']+)["\']',
    ]
    found: Set[str] = set()
    for pattern in patterns:
        found.update(re.findall(pattern, text))
    return found


def params_from_actions(text: str) -> List[str]:
    params: List[str] = []
    for block in re.findall(r'params\s*:\s*\[([^\]]*)\]', text, flags=re.S):
        params.extend(re.findall(r'["\']([^"\']+)["\']', block))
    return params


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_config_service.py <config.service.ts>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    errors: List[str] = []
    warnings: List[str] = []

    for marker in REQUIRED_MARKERS:
        if marker not in text:
            errors.append(f"Missing required marker: {marker}")

    fields = fields_from_columns(text)
    params = params_from_actions(text)
    allowed_context = {
        "id", "uuid", "context_user_id", "id_context_user", "id_user",
        "id_groupe", "token", "authorization"
    }
    missing = sorted({p for p in params if p not in fields and p not in allowed_context})
    if missing:
        warnings.append("Action params not found in COLUMNS_API: " + ", ".join(missing))

    select_count = len(re.findall(r'type\s*:\s*["\']select["\']|["\']type["\']\s*:\s*["\']select["\']', text))
    dropdown_sources = len(re.findall(r'dropdown\s*:', text)) + len(re.findall(r'localOptions\s*:', text)) + len(re.findall(r'options\s*:', text))
    if select_count and dropdown_sources == 0:
        warnings.append("Select columns detected but no dropdown/localOptions/options source found.")

    print(f"Validation report for {path}")
    print(f"Columns detected: {len(fields)}")
    print(f"Action params detected: {len(params)}")

    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"- {error}")
    else:
        print("\nErrors: none")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("Warnings: none")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
