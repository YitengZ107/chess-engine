import chess
from board_eval import PIECE_VALUES, evaluate_board

INFINITY = 1000000

TRANSPOSITION_TABLE = {}

def move_order_score(
    board: chess.Board,
    move: chess.Move,
) -> int:
    """
    Gives promising moves a higher score so they are searched first.

    This score is only used to order moves.
    It is not the board evaluation.
    """
    score = 0

    # Search promotions early.
    if move.promotion is not None:
        score += 10_000
        score += PIECE_VALUES[move.promotion]

    # Search captures early.
    if board.is_capture(move):
        attacking_piece = board.piece_at(move.from_square)

        # En passant captures a pawn even though the destination
        # square is empty before the move.
        if board.is_en_passant(move):
            captured_value = PIECE_VALUES[chess.PAWN]
        else:
            captured_piece = board.piece_at(move.to_square)

            if captured_piece is not None:
                captured_value = PIECE_VALUES[captured_piece.piece_type]
            else:
                captured_value = 0

        if attacking_piece is not None:
            attacker_value = PIECE_VALUES[attacking_piece.piece_type]
        else:
            attacker_value = 0

        # Prefer capturing valuable pieces with less valuable pieces.
        score += 5_000
        score += captured_value * 10
        score -= attacker_value

    # Search checking moves before normal quiet moves.
    if board.gives_check(move):
        score += 1_000

    # Give castling a small ordering bonus.
    if board.is_castling(move):
        score += 100

    return score


def order_moves(board: chess.Board) -> list[chess.Move]:
    moves = list(board.legal_moves)

    moves.sort(
        key=lambda move: move_order_score(board, move),
        reverse=True,
    )

    return moves


def tactical_moves(board: chess.Board) -> list[chess.Move]:
    moves = [
        move
        for move in board.legal_moves
        if board.is_capture(move) or move.promotion is not None
    ]

    moves.sort(
        key=lambda move: move_order_score(board, move),
        reverse=True,
    )

    return moves


def quiescence(
    board: chess.Board,
    alpha: int,
    beta: int,
    depth_left: int = 4,
) -> int:
    if depth_left == 0 or board.is_game_over():
        return evaluate_board(board)

    stand_pat = evaluate_board(board)

    # When the king is in check, the engine must examine
    # all legal responses rather than only captures.
    if board.is_check():
        moves = order_moves(board)
    else:
        moves = tactical_moves(board)

    if board.turn == chess.WHITE:
        if stand_pat >= beta:
            return stand_pat

        alpha = max(alpha, stand_pat)

        for move in moves:
            board.push(move)
            score = quiescence(
                board,
                alpha,
                beta,
                depth_left - 1,
            )
            board.pop()

            if score >= beta:
                return score

            alpha = max(alpha, score)

        return alpha

    if stand_pat <= alpha:
        return stand_pat

    beta = min(beta, stand_pat)

    for move in moves:
        board.push(move)
        score = quiescence(
            board,
            alpha,
            beta,
            depth_left - 1,
        )
        board.pop()

        if score <= alpha:
            return score

        beta = min(beta, score)

    return beta


def alpha_beta(
    board: chess.Board,
    depth: int,
    alpha: int,
    beta: int,
) -> int:
    if board.is_game_over():
        return evaluate_board(board)

    if depth == 0:
        return quiescence(board, alpha, beta)

    # Store the board position and remaining search depth.
    table_key = (board.fen(), depth)

    if table_key in TRANSPOSITION_TABLE:
        return TRANSPOSITION_TABLE[table_key]

    cutoff_occurred = False

    # White maximizes the evaluation.
    if board.turn == chess.WHITE:
        best_score = -INFINITY

        for move in order_moves(board):
            board.push(move)

            score = alpha_beta(
                board,
                depth - 1,
                alpha,
                beta,
            )

            board.pop()

            best_score = max(best_score, score)
            alpha = max(alpha, best_score)

            if alpha >= beta:
                cutoff_occurred = True
                break

    # Black minimizes the evaluation.
    else:
        best_score = INFINITY

        for move in order_moves(board):
            board.push(move)

            score = alpha_beta(
                board,
                depth - 1,
                alpha,
                beta,
            )

            board.pop()

            best_score = min(best_score, score)
            beta = min(beta, best_score)

            if alpha >= beta:
                cutoff_occurred = True
                break

    # Only save complete searches.
    if not cutoff_occurred:
        TRANSPOSITION_TABLE[table_key] = best_score

    return best_score


def choose_best_move(
    board: chess.Board,
    depth: int,
) -> chess.Move | None:
    
    TRANSPOSITION_TABLE.clear()
    
    best_move = None
    white_to_move = board.turn == chess.WHITE

    alpha = -INFINITY
    beta = INFINITY

    best_score = -INFINITY if white_to_move else INFINITY

    for move in order_moves(board):
        board.push(move)
        score = alpha_beta(
            board,
            depth - 1,
            alpha,
            beta,
        )
        board.pop()

        if white_to_move:
            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, best_score)

        else:
            if score < best_score:
                best_score = score
                best_move = move

            beta = min(beta, best_score)

    return best_move