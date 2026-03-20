#!/usr/bin/env python3
"""Exports ClickHouse schema and migration state."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from clickhouse_driver import Client as ClickHouseClient


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=9000)
    parser.add_argument("--database", default="analytics")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    client = ClickHouseClient(host=args.host, port=args.port)
    create_table = client.execute(f"SHOW CREATE TABLE {args.database}.events")[0][0]
    migrations = client.execute(
        f"SELECT version, applied_at FROM {args.database}.schema_migrations ORDER BY version"
    )

    output = {
        "database": args.database,
        "events_table_ddl": create_table,
        "schema_migrations": migrations,
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"snapshot_path": str(output_path)}, sort_keys=True))


if __name__ == "__main__":
    main()
