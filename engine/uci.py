import sys
import chess

from engine.search import choose_best_move

ENGINE_NAME = "YitengChessEngine"
ENGINE_AUTHOR = "Yiteng Zhang"
DEFAULT_DEPTH = 4


def send(message: str) -> None:
    print(message, flush=True)


def set_position(board: chess.Board, command: str) -> None:
    tokens = command.strip().split()

    if len(tokens) < 2:
        return

    # position startpos moves e2e4 e7e5
    if tokens[1] == "startpos":
        board.set_fen(chess.STARTING_FEN)

        if "moves" in tokens:
            move_index = tokens.index("moves")
            move_list = tokens[move_index + 1:]

            for move_text in move_list:
                board.push_uci(move_text)

    # position fen <fen> moves ...
    elif tokens[1] == "fen":
        if "moves" in tokens:
            move_index = tokens.index("moves")
            fen = " ".join(tokens[2:move_index])
            move_list = tokens[move_index + 1:]
        else:
            fen = " ".join(tokens[2:])
            move_list = []

        board.set_fen(fen)

        for move_text in move_list:
            board.push_uci(move_text)


def handle_go(board: chess.Board, command: str) -> None:
    tokens = command.strip().split()
    depth = DEFAULT_DEPTH

    if "depth" in tokens:
        try:
            depth_index = tokens.index("depth")
            depth = int(tokens[depth_index + 1])
        except (ValueError, IndexError):
            depth = DEFAULT_DEPTH

    best_move = choose_best_move(board, depth)

    if best_move is None:
        send("bestmove 0000")
    else:
        send(f"bestmove {best_move.uci()}")


def main() -> None:
    board = chess.Board()

    while True:
        try:
            command = input().strip()
        except EOFError:
            break

        if not command:
            continue

        if command == "uci":
            send(f"id name {ENGINE_NAME}")
            send(f"id author {ENGINE_AUTHOR}")
            send("uciok")

        elif command == "isready":
            send("readyok")

        elif command == "ucinewgame":
            board.reset()

        elif command.startswith("position"):
            set_position(board, command)

        elif command.startswith("go"):
            handle_go(board, command)

        elif command == "stop":
            # For this simple engine, searches are synchronous,
            # so there is nothing special to stop here.
            pass

        elif command == "quit":
            break

        # Optional commands that many GUIs may send.
        elif command.startswith("setoption"):
            pass

        elif command == "d":
            # helpful for manual testing
            send(str(board))

        else:
            # Ignore unsupported commands for now.
            pass


if __name__ == "__main__":
    main()