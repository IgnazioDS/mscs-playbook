from __future__ import annotations

from typing import Tuple

from .tictactoe import GameState, legal_moves, next_state, is_terminal, utility


def alphabeta(state: GameState, max_player: str = "X") -> Tuple[int | None, int]:
    def max_value(node: GameState, alpha: int, beta: int) -> tuple[int | None, int]:
        if is_terminal(node):
            return None, utility(node, max_player)
        best_val = -10
        best_move = None
        for move in legal_moves(node):
            _, val = min_value(next_state(node, move), alpha, beta)
            if val > best_val:
                best_val = val
                best_move = move
            alpha = max(alpha, best_val)
            if alpha >= beta:
                break
        return best_move, best_val

    def min_value(node: GameState, alpha: int, beta: int) -> tuple[int | None, int]:
        if is_terminal(node):
            return None, utility(node, max_player)
        best_val = 10
        best_move = None
        for move in legal_moves(node):
            _, val = max_value(next_state(node, move), alpha, beta)
            if val < best_val:
                best_val = val
                best_move = move
            beta = min(beta, best_val)
            if beta <= alpha:
                break
        return best_move, best_val

    if state.player == max_player:
        return max_value(state, -10, 10)
    return min_value(state, -10, 10)
