import chess

CHECKMATE_SCORE = 100000

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0,
}

MOBILITY_WEIGHTS = {
    chess.KNIGHT: 4,
    chess.BISHOP: 3,
    chess.ROOK: 2,
    chess.QUEEN: 1,
}


def evaluate_board(board: chess.Board) -> int:
    """
    Returns a positive score when White is better
    and a negative score when Black is better.
    """

    outcome = board.outcome()

    if outcome is not None:
        if outcome.winner == chess.WHITE:
            return CHECKMATE_SCORE

        if outcome.winner == chess.BLACK:
            return -CHECKMATE_SCORE

        return 0

    score = 0

    score += evaluate_material(board)
    score += evaluate_piece_positions(board)
    score += evaluate_pawn_structure(board)
    score += evaluate_bishop_pair(board)
    score += evaluate_mobility(board)
    score += evaluate_king_safety(board)

    return score


def evaluate_material(board: chess.Board) -> int:
    score = 0

    for piece_type, value in PIECE_VALUES.items():
        white_count = len(board.pieces(piece_type, chess.WHITE))
        black_count = len(board.pieces(piece_type, chess.BLACK))

        score += white_count * value
        score -= black_count * value

    return score


def evaluate_piece_positions(board: chess.Board) -> int:

    score = 0

    for color in (chess.WHITE, chess.BLACK):
        sign = 1 if color == chess.WHITE else -1

        # Small bonus for pawns on the central d- and e-files.
        for square in board.pieces(chess.PAWN, color):
            file_index = chess.square_file(square)

            if file_index in (3, 4):
                score += sign * 8

        # Knights strongly prefer central squares.
        for square in board.pieces(chess.KNIGHT, color):
            score += sign * centralization_bonus(square, weight=5)

        # Bishops receive a smaller centralization bonus.
        for square in board.pieces(chess.BISHOP, color):
            score += sign * centralization_bonus(square, weight=2)

        # Queens receive only a small centralization bonus.
        for square in board.pieces(chess.QUEEN, color):
            score += sign * centralization_bonus(square, weight=1)

        for square in board.pieces(chess.ROOK, color):
            rank = chess.square_rank(square)

            if color == chess.WHITE:
                relative_rank = rank
            else:
                relative_rank = 7 - rank

            # Rooks are powerful on the seventh rank.
            if relative_rank == 6:
                score += sign * 25

            score += sign * rook_file_bonus(board, square, color)

    return score


def centralization_bonus(square: chess.Square, weight: int) -> int:

    file = chess.square_file(square)
    rank = chess.square_rank(square)

    file_distance = abs(file - 3.5)
    rank_distance = abs(rank - 3.5)

    distance_from_center = file_distance + rank_distance

    return int((7 - distance_from_center) * weight)


def rook_file_bonus(
    board: chess.Board,
    rook_square: chess.Square,
    color: chess.Color,
) -> int:
    
    rook_file = chess.square_file(rook_square)

    friendly_pawns = [
        square
        for square in board.pieces(chess.PAWN, color)
        if chess.square_file(square) == rook_file
    ]

    enemy_pawns = [
        square
        for square in board.pieces(chess.PAWN, not color)
        if chess.square_file(square) == rook_file
    ]

    # Open file: no pawns from either player.
    if not friendly_pawns and not enemy_pawns:
        return 20

    # Semi-open file: no friendly pawns.
    if not friendly_pawns:
        return 10

    return 0


def evaluate_pawn_structure(board: chess.Board) -> int:\

    score = 0

    for color in (chess.WHITE, chess.BLACK):
        sign = 1 if color == chess.WHITE else -1
        pawns = list(board.pieces(chess.PAWN, color))

        pawn_counts_by_file = {
            file_index: 0
            for file_index in range(8)
        }

        for square in pawns:
            file_index = chess.square_file(square)
            pawn_counts_by_file[file_index] += 1

        color_score = 0

        # Penalize doubled pawns.
        for count in pawn_counts_by_file.values():
            if count > 1:
                color_score -= (count - 1) * 15

        for square in pawns:
            file_index = chess.square_file(square)

            adjacent_files = []

            if file_index > 0:
                adjacent_files.append(file_index - 1)
            if file_index < 7:
                adjacent_files.append(file_index + 1)
            has_adjacent_pawn = any(
                pawn_counts_by_file[adjacent_file] > 0
                for adjacent_file in adjacent_files
            )

            # Penalize isolated pawns.
            if not has_adjacent_pawn:
                color_score -= 10
            # Reward passed pawns based on advancement.
            if is_passed_pawn(board, square, color):
                advancement = pawn_advancement(square, color)
                color_score += 20 + advancement * 10

        score += sign * color_score

    return score


def is_passed_pawn(
    board: chess.Board,
    pawn_square: chess.Square,
    color: chess.Color,
) -> bool:
    
    pawn_file = chess.square_file(pawn_square)
    pawn_rank = chess.square_rank(pawn_square)

    enemy_pawns = board.pieces(chess.PAWN, not color)

    for enemy_square in enemy_pawns:
        enemy_file = chess.square_file(enemy_square)
        enemy_rank = chess.square_rank(enemy_square)

        # Only pawns on the same or neighboring files matter.
        if abs(enemy_file - pawn_file) > 1:
            continue
        if color == chess.WHITE and enemy_rank > pawn_rank:
            return False
        if color == chess.BLACK and enemy_rank < pawn_rank:
            return False

    return True


def pawn_advancement(
    square: chess.Square,
    color: chess.Color,
) -> int:
    
    rank = chess.square_rank(square)

    if color == chess.WHITE:
        return max(0, rank - 1)

    return max(0, 6 - rank)


def evaluate_bishop_pair(board: chess.Board) -> int:
    
    score = 0

    if len(board.pieces(chess.BISHOP, chess.WHITE)) >= 2:
        score += 30
    if len(board.pieces(chess.BISHOP, chess.BLACK)) >= 2:
        score -= 30

    return score


def evaluate_mobility(board: chess.Board) -> int:
    
    score = 0

    for color in (chess.WHITE, chess.BLACK):
        sign = 1 if color == chess.WHITE else -1

        for piece_type, weight in MOBILITY_WEIGHTS.items():
            for square in board.pieces(piece_type, color):
                usable_attacks = 0

                for target_square in board.attacks(square):
                    target_piece = board.piece_at(target_square)

                    if target_piece is None or target_piece.color != color:
                        usable_attacks += 1

                score += sign * usable_attacks * weight

    return score


def evaluate_king_safety(board: chess.Board) -> int:
    # King safety matters less after both queens are gone.
    queens_remaining = (
        len(board.pieces(chess.QUEEN, chess.WHITE))
        + len(board.pieces(chess.QUEEN, chess.BLACK))
    )

    if queens_remaining == 0:
        return 0

    white_safety = king_safety_for_color(board, chess.WHITE)
    black_safety = king_safety_for_color(board, chess.BLACK)

    return white_safety - black_safety


def king_safety_for_color(
    board: chess.Board,
    color: chess.Color,
) -> int:
    
    king_square = board.king(color)

    if king_square is None:
        return 0

    score = 0

    castled_squares = (
        {chess.C1, chess.G1}
        if color == chess.WHITE
        else {chess.C8, chess.G8}
    )

    if king_square in castled_squares:
        score += 30

    king_file = chess.square_file(king_square)
    king_rank = chess.square_rank(king_square)

    shield_direction = 1 if color == chess.WHITE else -1
    shield_rank = king_rank + shield_direction

    if 0 <= shield_rank <= 7:
        for file in range(
            max(0, king_file - 1),
            min(7, king_file + 1) + 1,
        ):
            shield_square = chess.square(file, shield_rank)
            piece = board.piece_at(shield_square)

            if (
                piece is not None
                and piece.color == color
                and piece.piece_type == chess.PAWN
            ):
                score += 8

    return score