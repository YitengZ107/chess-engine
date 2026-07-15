import chess
from search import choose_best_move

def print_board(board):
    print()
    print(board)
    print()

def main():
    board = chess.Board()
    engine_depth = 3

    while not board.is_game_over(claim_draw=True):
        print_board(board)

        if board.turn == chess.WHITE:
            move_text = input("Enter your move: ").strip()

            try:
                move = chess.Move.from_uci(move_text)
            except ValueError:
                print("Invalid format. Use a move such as e2e4.")
                continue

            if move not in board.legal_moves:
                print("That move is not legal.")
                continue

            board.push(move)

        else:
            print("Engine is choosing a move...")
            move = choose_best_move(board, engine_depth)

            if move is None:
                break

            print(f"Engine plays: {move}")
            board.push(move)

    print_board(board)

    outcome = board.outcome(claim_draw=True)

    if outcome is not None:
        print(f"Game over: {outcome.result()}")
        print(f"Reason: {outcome.termination.name}")


if __name__ == "__main__":
    main()