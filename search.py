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
    
    if board.turn == chess.WHITE:
        best_score = -999999
    else:
        best_score = 999999
    
    for move in board.legal_moves:
        board.push(move)
        score = evaluate_board(board)
        board.pop()
        if board.turn == chess.WHITE:
            if score > best_score:
                best_score = score
                best_move = move
        else:
            if score < best_score:
                best_score = score
                best_move = move
        
    return best_move