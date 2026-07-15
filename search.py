import chess
from board_eval import evaluate_board

INFINITY = 1_000_000


def alpha_beta(board, depth, alpha, beta):
    if depth == 0 or board.is_game_over(claim_draw=True):
        return evaluate_board(board)

    if board.turn == chess.WHITE:
        best_score = -INFINITY

        for move in board.legal_moves:
            board.push(move)
            score = alpha_beta(board, depth - 1, alpha, beta)
            board.pop()

            best_score = max(best_score, score)
            alpha = max(alpha, best_score)

            if beta <= alpha:
                break

        return best_score

    best_score = INFINITY

    for move in board.legal_moves:
        board.push(move)
        score = alpha_beta(board, depth - 1, alpha, beta)
        board.pop()

        best_score = min(best_score, score)
        beta = min(beta, best_score)

        if beta <= alpha:
            break

    return best_score


def choose_best_move(board, depth):
    best_move = None
    white_to_move = board.turn == chess.WHITE

    if white_to_move:
        best_score = -INFINITY
    else:
        best_score = INFINITY

    for move in board.legal_moves:
        board.push(move)
        score = alpha_beta(
            board,
            depth - 1,
            -INFINITY,
            INFINITY
        )
        board.pop()

        if white_to_move and score > best_score:
            best_score = score
            best_move = move

        elif not white_to_move and score < best_score:
            best_score = score
            best_move = move

    return best_move