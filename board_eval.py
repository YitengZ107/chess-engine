import chess


piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0
}

CHECKMATE_SCORE = 100000


def evaluate_board(board):
    # If the current player is checkmated, the other player won.
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -CHECKMATE_SCORE
        else:
            return CHECKMATE_SCORE

    # Drawn positions are neutral.
    if board.is_stalemate():
        return 0

    if board.is_insufficient_material():
        return 0

    score = 0

    for piece_type, value in piece_values.items():
        white_pieces = len(board.pieces(piece_type, chess.WHITE))
        black_pieces = len(board.pieces(piece_type, chess.BLACK))

        score += white_pieces * value
        score -= black_pieces * value

    return score

# def position_score(board):
