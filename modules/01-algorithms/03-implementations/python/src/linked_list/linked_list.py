"""Minimal singly linked list implementation for educational use.

Problem:
    Store elements in nodes linked by pointers to the next node.

Inputs/Outputs:
    Node(data, next) and LinkedList with prepend + iteration.

Complexity:
    prepend: O(1), iteration: O(n).

Typical use cases:
    Teaching pointer-based structures and sequence traversal.
"""

from __future__ import annotations

from typing import Any, Iterator, Optional


class Node:
    """A single linked list node holding data and a next pointer."""

    def __init__(self, data: Any, nxt: Optional["Node"] = None) -> None:
        self.data = data
        self.next = nxt


class LinkedList:
    """Singly linked list supporting prepend and iteration."""

    def __init__(self) -> None:
        self.head: Optional[Node] = None

    def prepend(self, data: Any) -> None:
        """Insert data at the head of the list in O(1)."""
        self.head = Node(data, self.head)

    def __iter__(self) -> Iterator[Any]:
        """Yield elements from head to tail."""
        cur = self.head
        while cur:
            yield cur.data
            cur = cur.next
