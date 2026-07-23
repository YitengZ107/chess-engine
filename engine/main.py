import random

import chess

from engine.search import choose_best_move

ENGINE_DEPTH = 5

def choose_human_color() -> chess.Color:
    while True:
        print("\nChoose your color:")
        print("1. White")
        print("2. Black")
        print("3. Random")

        choice = input("Enter 1, 2, or 3: ").strip().lower()

        if choice in ("1", "white", "w"):
            return chess.WHITE

        if choice in ("2", "black", "b"):
            return chess.BLACK

        if choice in ("3", "random", "r"):
            chosen_color = random.choice(
                [chess.WHITE, chess.BLACK]
            )

            color_name = (
                "White"
                if chosen_color == chess.WHITE
                else "Black"
            )

            print(f"You were randomly assigned {color_name}.")
            return chosen_color

        print("Invalid choice. Please enter 1, 2, or 3.")


def print_board(
    board: chess.Board,
    human_color: chess.Color,
) -> None:
    print()

    # Flip the board when the human plays Black.
    print(
        board
        if human_color == chess.WHITE
        else board.transform(chess.flip_vertical)
    )

    print()

    if board.is_check():
        print("Check!\n")


def parse_human_move(
    board: chess.Board,
    move_text: str,
) -> chess.Move | None:
    """
    Accepts standard algebraic notation:
        e4, Nf3, Bxc6, O-O

    Or UCI coordinate notation:
        e2e4, g1f3, f1c4
    """

    try:
        return board.parse_san(move_text)
    except ValueError:
        pass

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

    # SAN must be generated before the move is pushed.
    move_san = board.san(move)

    print(f"Engine plays: {move_san} ({move.uci()})")

    board.push(move)


def print_result(
    board: chess.Board,
    human_color: chess.Color,
) -> None:
    outcome = board.outcome(claim_draw=True)

    print("\nFinal position:")
    print_board(board, human_color)

    if outcome is None:
        print("Game ended before a result was reached.")
        return

    reason = outcome.termination.name.replace(
        "_",
        " ",
    ).title()

    print(f"Result: {outcome.result()}")
    print(f"Reason: {reason}")

    if outcome.winner is None:
        print("The game is a draw.")
    elif outcome.winner == human_color:
        print("You win!")
    else:
        print("The engine wins!")


def main() -> None:
    board = chess.Board()
    human_color = choose_human_color()

    human_color_name = (
        "White"
        if human_color == chess.WHITE
        else "Black"
    )

    print("\nChess Engine")
    print(f"You are playing as {human_color_name}.")
    print("Enter moves such as e4, Nf3, e2e4, or g1f3.")
    print("Type 'quit' to stop playing.")

    while not board.is_game_over(claim_draw=True):
        print_board(board, human_color)

        if board.turn == human_color:
            continue_game = human_turn(board)

            if not continue_game:
                print("\nYou ended the game.")
                return
        else:
            engine_turn(board)

    print_result(board, human_color)


if __name__ == "__main__":
    main()
