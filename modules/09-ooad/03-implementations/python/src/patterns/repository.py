"""Intent: mediate between domain and data mapping using a repository.
When to use: hide persistence details behind a collection-like interface.
Pitfalls: leaking storage details or mixing query logic into domain.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class User:
    user_id: str
    name: str
    tier: str


class InMemoryUserRepository:
    def __init__(self) -> None:
        self._store: Dict[str, User] = {}

    def save(self, user: User) -> None:
        self._store[user.user_id] = user

    def get(self, user_id: str) -> Optional[User]:
        return self._store.get(user_id)

    def list_all(self) -> List[User]:
        return list(self._store.values())

    def find_by_tier(self, tier: str) -> List[User]:
        return [u for u in self._store.values() if u.tier == tier]
