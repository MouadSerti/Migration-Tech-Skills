#!/usr/bin/env python3
"""Summarize Swagger/OpenAPI endpoints for Angular module generation."""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, List

HTTP_METHODS = {"get", "post", "put", "patch", "delete"}


def load_spec(source: str) -> Dict[str, Any]:
    if source.startswith(("http://", "https://")):
        with urllib.request.urlopen(source, timeout=30) as response:  # nosec - developer tool
            text = response.read().decode("utf-8")
    else:
        text = Path(source).read_text(encoding="utf-8")

    if source.endswith((".yaml", ".yml")):
        try:
            import yaml  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise SystemExit("YAML file detected. Install PyYAML or export Swagger as JSON.") from exc
        return yaml.safe_load(text)

    return json.loads(text)


def resolve_ref(spec: Dict[str, Any], ref: str) -> Dict[str, Any]:
    if not ref.startswith("#/"):
        return {"$ref": ref}
    node: Any = spec
    for part in ref[2:].split("/"):
        node = node.get(part, {}) if isinstance(node, dict) else {}
    return node if isinstance(node, dict) else {}


def schema_name(schema: Dict[str, Any]) -> str:
    if "$ref" in schema:
        return str(schema["$ref"]).split("/")[-1]
    if "type" in schema:
        return str(schema["type"])
    return "unknown"


def extract_schema(schema: Dict[str, Any], spec: Dict[str, Any], depth: int = 0) -> Dict[str, Any]:
    if depth > 4 or not isinstance(schema, dict):
        return {}
    if "$ref" in schema:
        schema = resolve_ref(spec, schema["$ref"])
    if "items" in schema and isinstance(schema["items"], dict):
        return extract_schema(schema["items"], spec, depth + 1)
    if "properties" in schema:
        return schema
    for key in ("schema", "content"):
        if key in schema and isinstance(schema[key], dict):
            return extract_schema(schema[key], spec, depth + 1)
    return schema


def request_body_fields(operation: Dict[str, Any], spec: Dict[str, Any]) -> List[str]:
    body = operation.get("requestBody", {})
    content = body.get("content", {}) if isinstance(body, dict) else {}
    schema: Dict[str, Any] = {}
    for media in ("application/json", "application/*+json", "*/*"):
        if media in content:
            schema = content[media].get("schema", {})
            break
    if not schema and content:
        first = next(iter(content.values()))
        schema = first.get("schema", {}) if isinstance(first, dict) else {}
    schema = extract_schema(schema, spec)
    props = schema.get("properties", {}) if isinstance(schema, dict) else {}
    return list(props.keys())


def response_fields(operation: Dict[str, Any], spec: Dict[str, Any]) -> List[str]:
    responses = operation.get("responses", {})
    for status in ("200", "201", "default"):
        response = responses.get(status, {})
        content = response.get("content", {}) if isinstance(response, dict) else {}
        for media_data in content.values():
            if isinstance(media_data, dict):
                schema = extract_schema(media_data.get("schema", {}), spec)
                props = schema.get("properties", {}) if isinstance(schema, dict) else {}
                return list(props.keys())
    return []


def swagger2_body_fields(parameters: Iterable[Dict[str, Any]], spec: Dict[str, Any]) -> List[str]:
    for param in parameters:
        if param.get("in") == "body":
            schema = extract_schema(param.get("schema", {}), spec)
            props = schema.get("properties", {}) if isinstance(schema, dict) else {}
            return list(props.keys())
    return []


def summarize(spec: Dict[str, Any]) -> List[Dict[str, Any]]:
    paths = spec.get("paths", {})
    result: List[Dict[str, Any]] = []
    for path, path_item in sorted(paths.items()):
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            if method.lower() not in HTTP_METHODS or not isinstance(operation, dict):
                continue
            params = operation.get("parameters", [])
            param_names = [p.get("name") for p in params if isinstance(p, dict) and p.get("name")]
            body_fields = request_body_fields(operation, spec) or swagger2_body_fields(params, spec)
            result.append({
                "method": method.upper(),
                "path": path,
                "tags": operation.get("tags", []),
                "operationId": operation.get("operationId", ""),
                "summary": operation.get("summary", ""),
                "params": param_names,
                "bodyFields": body_fields,
                "responseFields": response_fields(operation, spec),
            })
    return result


def print_markdown(rows: List[Dict[str, Any]]) -> None:
    print("# OpenAPI summary\n")
    for row in rows:
        print(f"## {row['method']} {row['path']}")
        if row["tags"]:
            print(f"- Tags: {', '.join(map(str, row['tags']))}")
        if row["operationId"]:
            print(f"- operationId: {row['operationId']}")
        if row["summary"]:
            print(f"- Summary: {row['summary']}")
        print(f"- Params: {', '.join(row['params']) if row['params'] else '-'}")
        print(f"- Body fields: {', '.join(row['bodyFields']) if row['bodyFields'] else '-'}")
        print(f"- Response fields: {', '.join(row['responseFields']) if row['responseFields'] else '-'}")
        print()


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: openapi_summary.py <swagger-or-openapi-json-yaml-or-url>", file=sys.stderr)
        return 2
    spec = load_spec(sys.argv[1])
    rows = summarize(spec)
    print_markdown(rows)
    print(f"Total endpoints: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
