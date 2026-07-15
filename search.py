import random
import chess
from board_eval import evaluate_board

def choose_random_move(board):
    legal_moves = list(board.legal_moves)

    if len(legal_moves) == 0:
        return None

    return random.choice(legal_moves)

def choose_material_move(board):
    best_move = None
    white_to_move = board.turn == chess.WHITE

    if white_to_move:
        best_score = -999999
    else:
        best_score = 999999

    for move in board.legal_moves:
        board.push(move)
        score = evaluate_board(board)
        board.pop()

        if white_to_move:
            if score > best_score:
                best_score = score
                best_move = move
        else:
            if score < best_score:
                best_score = score
                best_move = move

    return best_move

def minimax(board, depth):
    # Stop searching when the depth reaches zero
    # or when the game has ended.
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if board.turn == chess.WHITE:
        best_score = -999999

        for move in board.legal_moves:
            board.push(move)
            score = minimax(board, depth - 1)
            board.pop()

            best_score = max(best_score, score)

        return best_score

    else:
        best_score = 999999

        for move in board.legal_moves:
            board.push(move)
            score = minimax(board, depth - 1)
            board.pop()

            best_score = min(best_score, score)

        return best_score
    
def choose_minimax_move(board, depth):
    best_move = None
    white_to_move = board.turn == chess.WHITE

    if white_to_move:
        best_score = -999999
    else:
        best_score = 999999

    for move in board.legal_moves:
        board.push(move)
        score = minimax(board, depth - 1)
        board.pop()

        if white_to_move:
            if score > best_score:
                best_score = score
                best_move = move
        else:
            if score < best_score:
                best_score = score
                best_move = move

    return best_move