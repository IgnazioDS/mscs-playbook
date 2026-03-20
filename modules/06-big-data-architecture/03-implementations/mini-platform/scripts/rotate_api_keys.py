#!/usr/bin/env python3
"""Builds scoped API key env values for overlap and retirement windows."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

MINI_PLATFORM_ROOT = Path(__file__).resolve().parents[1]
SHARED_ROOT = MINI_PLATFORM_ROOT / "shared"
if str(SHARED_ROOT) not in sys.path:
    sys.path.insert(0, str(SHARED_ROOT))

from mini_platform.auth import parse_api_keys
from mini_platform.ops import render_scoped_key_env, rotate_keys


def _parse_retire_ids(raw: str) -> set[str]:
    return {item.strip() for item in raw.split(",") if item.strip()}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", choices=["ingest", "operator"], required=True)
    parser.add_argument("--current", required=True)
    parser.add_argument("--add", action="append", default=[])
    parser.add_argument("--retire", default="")
    args = parser.parse_args()

    current = [(record.key_id, record.secret) for record in parse_api_keys(args.current, scope=args.scope).values()]
    additions = []
    for entry in args.add:
        parsed = parse_api_keys(entry, scope=args.scope)
        additions.extend((record.key_id, record.secret) for record in parsed.values())

    rotated = rotate_keys(current, add_entries=additions, retire_key_ids=_parse_retire_ids(args.retire))
    print(json.dumps({"scope": args.scope, "env_value": render_scoped_key_env(rotated)}, sort_keys=True))


if __name__ == "__main__":
    main()
