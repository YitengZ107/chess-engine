import chess
from search import choose_material_move

board = chess.Board()

print("Starting board:")
print(board)

move = choose_material_move(board)

print("\nBot chooses:")
print(move)

board.push(move)

print("\nBoard after bot move:")
print(board)