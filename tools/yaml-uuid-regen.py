#!/usr/bin/env python3
"""
Zabbix template UUID rewriter.

This small utility walks a YAML file recursively and replaces every key named
"uuid" with a fresh UUID value. It is intended for Zabbix templates, where
items and triggers often need unique UUIDs inside a template.

Usage:
    ./rewrite_uuid.py template.yml
"""

import argparse
import sys
import uuid
from pathlib import Path

import yaml


def rewrite_uuids(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "uuid" and isinstance(value, str):
                obj[key] = uuid.uuid4().hex
            else:
                rewrite_uuids(value)
    elif isinstance(obj, list):
        for item in obj:
            rewrite_uuids(item)


def main():
    parser = argparse.ArgumentParser(
        description="Replace all 'uuid' fields recursively in a Zabbix template YAML file."
    )
    parser.add_argument(
        "path",
        help="YAML file to process.",
    )
    args = parser.parse_args()

    path = Path(args.path)

    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 1

    if not path.is_file():
        print(f"ERROR: not a regular file: {path}", file=sys.stderr)
        return 1

    try:
        text = path.read_text(encoding="utf-8")
        data = yaml.safe_load(text)
    except Exception as e:
        print(f"ERROR: cannot read/parse YAML in {path}: {e}", file=sys.stderr)
        return 1

    if data is None:
        print(f"ERROR: YAML file is empty: {path}", file=sys.stderr)
        return 1

    rewrite_uuids(data)

    try:
        output = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
        path.write_text(output, encoding="utf-8")
        print(f"updated: {path}")
    except Exception as e:
        print(f"ERROR: cannot write {path}: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
