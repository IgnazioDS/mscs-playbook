#!/usr/bin/env python3
"""Mirrors MinIO raw objects to a local directory for recovery."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from minio import Minio


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--access-key", required=True)
    parser.add_argument("--secret-key", required=True)
    parser.add_argument("--bucket", default="events")
    parser.add_argument("--secure", action="store_true")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    client = Minio(
        args.endpoint,
        access_key=args.access_key,
        secret_key=args.secret_key,
        secure=args.secure,
    )
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    mirrored = 0
    for item in client.list_objects(args.bucket, recursive=True):
        target = output_dir / item.object_name
        target.parent.mkdir(parents=True, exist_ok=True)
        client.fget_object(args.bucket, item.object_name, str(target))
        mirrored += 1

    print(json.dumps({"bucket": args.bucket, "mirrored_objects": mirrored}, sort_keys=True))


if __name__ == "__main__":
    main()
