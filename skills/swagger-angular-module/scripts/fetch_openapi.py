#!/usr/bin/env python3
"""Fetch a protected OpenAPI/Swagger JSON/YAML document without writing secrets to disk.

Examples:
  export API_SWAGGER_TOKEN="eyJ..."
  python fetch_openapi.py https://your-api-server.com/api/swagger/resource-api \
    --output /tmp/resource-api.openapi.json \
    --token-env API_SWAGGER_TOKEN \
    --scheme Bearer

  python fetch_openapi.py https://example.com/openapi.json \
    --output /tmp/openapi.json \
    --header-env X-API-Key=MY_API_KEY
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


def build_headers(args: argparse.Namespace) -> dict[str, str]:
    headers: dict[str, str] = {
        "Accept": "application/json, application/yaml, text/yaml, */*",
        "User-Agent": "swagger-angular-module/1.0",
    }

    for raw in args.header or []:
        if ":" not in raw:
            raise SystemExit(f"Invalid --header value. Expected 'Name: value', got: {raw!r}")
        name, value = raw.split(":", 1)
        headers[name.strip()] = value.strip()

    for raw in args.header_env or []:
        if "=" not in raw:
            raise SystemExit(f"Invalid --header-env value. Expected 'Header-Name=ENV_NAME', got: {raw!r}")
        name, env_name = raw.split("=", 1)
        value = os.environ.get(env_name.strip())
        if not value:
            raise SystemExit(f"Environment variable {env_name.strip()} is empty or missing")
        headers[name.strip()] = value

    token = None
    if args.token:
        token = args.token
    if args.token_env:
        token = os.environ.get(args.token_env)
        if not token:
            raise SystemExit(f"Environment variable {args.token_env} is empty or missing")
    if token:
        scheme = args.scheme.strip()
        headers["Authorization"] = f"{scheme} {token}" if scheme else token

    return headers


def fetch(url: str, headers: dict[str, str]) -> bytes:
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            status = getattr(resp, "status", 200)
            data = resp.read()
            content_type = resp.headers.get("content-type", "")
    except urllib.error.HTTPError as exc:
        body = exc.read(400).decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {exc.code} while fetching Swagger. Response preview: {body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Network error while fetching Swagger: {exc}") from exc

    if status >= 400:
        raise SystemExit(f"HTTP {status} while fetching Swagger")

    preview = data[:200].decode("utf-8", errors="replace").lstrip().lower()
    if preview.startswith("<!doctype html") or preview.startswith("<html"):
        raise SystemExit(
            "The URL returned HTML, not OpenAPI. Use the direct JSON/YAML spec URL, not the Swagger UI page."
        )

    if "text/html" in content_type.lower():
        raise SystemExit(
            "The URL returned text/html, not OpenAPI. Use the direct JSON/YAML spec URL or check authorization."
        )

    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch a protected Swagger/OpenAPI document")
    parser.add_argument("url", help="Direct OpenAPI/Swagger JSON/YAML URL")
    parser.add_argument("--output", "-o", required=True, help="Output path for downloaded spec")
    parser.add_argument("--token", help="Access token. Prefer --token-env to avoid shell history leaks.")
    parser.add_argument("--token-env", help="Environment variable containing the access token")
    parser.add_argument("--scheme", default="Bearer", help="Authorization scheme, default: Bearer. Use empty string for raw token header.")
    parser.add_argument("--header", action="append", help="Extra header, format 'Name: value'. Can be repeated.")
    parser.add_argument("--header-env", action="append", help="Header from env, format 'Header-Name=ENV_NAME'. Can be repeated.")
    args = parser.parse_args()

    headers = build_headers(args)
    safe_headers = {k: ("***" if k.lower() in {"authorization", "cookie", "x-api-key"} else v) for k, v in headers.items()}
    print(f"Fetching OpenAPI from {args.url}")
    print(f"Headers: {json.dumps(safe_headers, ensure_ascii=False)}")
    data = fetch(args.url, headers)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    print(f"Saved Swagger/OpenAPI to {out}")
    print(f"Bytes: {len(data)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
