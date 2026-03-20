#!/usr/bin/env python3
"""Restores a Postgres control-plane snapshot from JSON."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import psycopg2
from psycopg2 import sql

MINI_PLATFORM_ROOT = Path(__file__).resolve().parents[1]
SHARED_ROOT = MINI_PLATFORM_ROOT / "shared"
if str(SHARED_ROOT) not in sys.path:
    sys.path.insert(0, str(SHARED_ROOT))

from mini_platform.ops import restore_insert_order, restore_truncate_order


def _restore_rows(pg_conn, snapshot: dict[str, object]) -> dict[str, int]:
    restored_counts: dict[str, int] = {}
    with pg_conn.cursor() as cur:
        for table in restore_truncate_order():
            cur.execute(sql.SQL("TRUNCATE TABLE {} CASCADE").format(sql.Identifier(table)))

        for table in restore_insert_order():
            rows = snapshot["data"].get(table, [])
            restored_counts[table] = len(rows)
            if not rows:
                continue
            columns = list(rows[0].keys())
            query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table),
                sql.SQL(", ").join(sql.Identifier(column) for column in columns),
                sql.SQL(", ").join(sql.Placeholder() for _ in columns),
            )
            for row in rows:
                cur.execute(query, [row[column] for column in columns])
    return restored_counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_path")
    args = parser.parse_args()

    with Path(args.snapshot_path).open("r", encoding="utf-8") as handle:
        snapshot = json.load(handle)

    pg_conn = psycopg2.connect(os.environ["POSTGRES_DSN"])
    pg_conn.autocommit = True
    try:
        restored_counts = _restore_rows(pg_conn, snapshot)
    finally:
        pg_conn.close()

    print(json.dumps({"restored_tables": restored_counts}, sort_keys=True))


if __name__ == "__main__":
    main()
