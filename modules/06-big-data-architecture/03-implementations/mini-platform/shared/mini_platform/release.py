"""Release metadata helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReleaseMetadata:
    version: str
    build_sha: str
    build_time: str

    def as_dict(self) -> dict[str, str]:
        return {
            "version": self.version,
            "build_sha": self.build_sha,
            "build_time": self.build_time,
        }
