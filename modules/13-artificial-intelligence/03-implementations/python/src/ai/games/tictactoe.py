from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class GameState:
    board: tuple[str, ...]
    player: str


def initial_state() -> GameState:
    return GameState(board=(" ",) * 9, player="X")


def legal_moves(state: GameState) -> list[int]:
    return [idx for idx, value in enumerate(state.board) if value == " "]


def next_state(state: GameState, move: int) -> GameState:
    board = list(state.board)
    board[move] = state.player
    next_player = "O" if state.player == "X" else "X"
    return GameState(board=tuple(board), player=next_player)


def winner(state: GameState) -> str | None:
    lines = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]
    for a, b, c in lines:
        if state.board[a] != " " and state.board[a] == state.board[b] == state.board[c]:
            return state.board[a]
    return None


def is_terminal(state: GameState) -> bool:
    return winner(state) is not None or " " not in state.board


def utility(state: GameState, max_player: str = "X") -> int:
    win = winner(state)
    if win is None:
        return 0
    return 1 if win == max_player else -1


def pretty(state: GameState) -> str:
    rows = [state.board[i : i + 3] for i in range(0, 9, 3)]
    return "\n".join("|".join(row) for row in rows)
