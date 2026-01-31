from src.ai.games.tictactoe import GameState
from src.ai.games.minimax import minimax
from src.ai.games.alphabeta import alphabeta


def test_minimax_finds_winning_move():
    # X to move, can win at position 2
    board = (
        "X", "X", " ",
        "O", "O", " ",
        " ", " ", " ",
    )
    state = GameState(board=board, player="X")
    move, value = minimax(state, max_player="X")
    assert move == 2
    assert value == 1


def test_alphabeta_matches_minimax():
    board = (
        "X", "O", "X",
        "O", "X", " ",
        " ", " ", "O",
    )
    state = GameState(board=board, player="X")
    move_min, value_min = minimax(state, max_player="X")
    move_ab, value_ab = alphabeta(state, max_player="X")
    assert value_ab == value_min
    assert move_ab == move_min
