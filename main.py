import chess
from search import choose_minimax_move

board = chess.Board()

print("Starting board:")
print(board)

move = choose_minimax_move(board, depth=2)

print("\nBot chooses:")
print(move)

if move is not None:
    board.push(move)

print("\nBoard after bot move:")
print(board)