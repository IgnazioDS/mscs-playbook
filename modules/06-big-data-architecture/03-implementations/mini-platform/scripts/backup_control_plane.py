#!/usr/bin/env python3
"""Exports Postgres control-plane state to a JSON snapshot."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor

MINI_PLATFORM_ROOT = Path(__file__).resolve().parents[1]
SHARED_ROOT = MINI_PLATFORM_ROOT / "shared"
if str(SHARED_ROOT) not in sys.path:
    sys.path.insert(0, str(SHARED_ROOT))

from mini_platform.ops import CONTROL_PLANE_TABLES, snapshot_manifest


def dump_tables(pg_conn) -> dict[str, list[dict]]:
    snapshot: dict[str, list[dict]] = {}
    with pg_conn.cursor(cursor_factory=RealDictCursor) as cur:
        for table in CONTROL_PLANE_TABLES:
            cur.execute(f"SELECT * FROM {table}")
            snapshot[table] = [dict(row) for row in cur.fetchall()]
    return snapshot


def build_snapshot(pg_conn) -> dict[str, object]:
    created_at = datetime.now(timezone.utc).isoformat()
    return {
        "manifest": snapshot_manifest(
            version=os.getenv("APP_VERSION", "dev"),
            build_sha=os.getenv("APP_BUILD_SHA", "local"),
            created_at=created_at,
        ),
        "data": dump_tables(pg_conn),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default=f"artifacts/control-plane-backup-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json",
    )
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pg_conn = psycopg2.connect(os.environ["POSTGRES_DSN"])
    try:
        snapshot = build_snapshot(pg_conn)
    finally:
        pg_conn.close()

    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(snapshot, handle, default=str, indent=2, sort_keys=True)

    print(json.dumps({"snapshot_path": str(output_path), "tables": CONTROL_PLANE_TABLES}))


if __name__ == "__main__":
    main()
