from __future__ import annotations

from typing import Tuple

from .tictactoe import GameState, legal_moves, next_state, is_terminal, utility


def minimax(state: GameState, max_player: str = "X") -> Tuple[int | None, int]:
    if is_terminal(state):
        return None, utility(state, max_player)

    if state.player == max_player:
        best_val = -10
        best_move = None
        for move in legal_moves(state):
            _, val = minimax(next_state(state, move), max_player)
            if val > best_val:
                best_val = val
                best_move = move
        return best_move, best_val

    best_val = 10
    best_move = None
    for move in legal_moves(state):
        _, val = minimax(next_state(state, move), max_player)
        if val < best_val:
            best_val = val
            best_move = move
    return best_move, best_val
