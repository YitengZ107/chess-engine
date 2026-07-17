import chess

from search import choose_best_move

ENGINE_DEPTH = 4
HUMAN_COLOR = chess.WHITE


def print_board(board: chess.Board) -> None:
    print()
    print(board)
    print()

    if board.is_check():
        print("Check!\n")


def parse_human_move(
    board: chess.Board,
    move_text: str,
) -> chess.Move | None:
    """
    Accepts either standard chess notation:
        e4, Nf3, Bxc6, O-O

    Or UCI coordinate notation:
        e2e4, g1f3, f1c4
    """

    # Try standard algebraic notation first.
    try:
        return board.parse_san(move_text)
    except ValueError:
        pass

    # Try UCI notation second.
    try:
        return board.parse_uci(move_text.lower())
    except ValueError:
        return None


def human_turn(board: chess.Board) -> bool:
    while True:
        move_text = input(
            "Your move (or type 'quit'): "
        ).strip()

        if move_text.lower() == "quit":
            return False

        move = parse_human_move(board, move_text)

        if move is None:
            print(
                "Invalid or illegal move. "
                "Examples: e4, Nf3, e2e4, g1f3\n"
            )
            continue

        board.push(move)
        return True


def engine_turn(board: chess.Board) -> None:
    print(f"Engine is searching at depth {ENGINE_DEPTH}...")

    move = choose_best_move(board, ENGINE_DEPTH)

    if move is None:
        return

    # Generate SAN before pushing because SAN depends
    # on the current board position.
    move_san = board.san(move)

    print(f"Engine plays: {move_san} ({move.uci()})")

    board.push(move)


def print_result(board: chess.Board) -> None:
    outcome = board.outcome(claim_draw=True)

    print("\nFinal position:")
    print_board(board)

    if outcome is None:
        print("Game ended before a result was reached.")
        return

    reason = outcome.termination.name.replace("_", " ").title()

    print(f"Result: {outcome.result()}")
    print(f"Reason: {reason}")

    if outcome.winner == chess.WHITE:
        print("White wins!")
    elif outcome.winner == chess.BLACK:
        print("Black wins!")
    else:
        print("The game is a draw.")


def main() -> None:
    board = chess.Board()

    print("Chess Engine")
    print("You are playing as White.")
    print("Enter moves such as e4, Nf3, e2e4, or g1f3.")
    print("Type 'quit' to stop playing.")

    while not board.is_game_over(claim_draw=True):
        print_board(board)

        if board.turn == HUMAN_COLOR:
            continue_game = human_turn(board)

            if not continue_game:
                print("\nYou ended the game.")
                return
        else:
            engine_turn(board)

    print_result(board)


if __name__ == "__main__":
    main()