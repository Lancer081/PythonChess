import chess
import chess.svg
from chessboard import display

# Simple evaluation function (material count)
def evaluate_board(board):
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
    }

    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            if piece.color == chess.WHITE:
                score += piece_values.get(piece.piece_type, 0)
            else:
                score -= piece_values.get(piece.piece_type, 0)
    return score

# Minimax search with simple evaluation and fixed depth
def minimax(board, depth, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    legal_moves = list(board.legal_moves)
    if maximizing_player:
        best_value = -float('inf')
        for move in legal_moves:
            board.push(move)
            value = minimax(board, depth - 1, False)
            best_value = max(best_value, value)
            board.pop()
        return best_value
    else:
        best_value = float('inf')
        for move in legal_moves:
            board.push(move)
            value = minimax(board, depth - 1, True)
            best_value = min(best_value, value)
            board.pop()
        return best_value

# Find the best move using minimax with fixed depth
def find_best_move(board, depth):
    legal_moves = list(board.legal_moves)
    best_move = None
    best_value = -float('inf')

    for move in legal_moves:
        board.push(move)
        value = minimax(board, depth - 1, False)
        if value > best_value:
            best_value = value
            best_move = move
        board.pop()

    return best_move

# Main function
def main():
    board = chess.Board()
    depth = 3  # Set the search depth

    while not board.is_game_over():
        display.display(board)
        if board.turn == chess.WHITE:
            # White's turn - find and make the best move
            best_move = find_best_move(board, depth)
            board.push(best_move)
        else:
            # Black's turn - also find and make the best move
            best_move = find_best_move(board, depth)
            board.push(best_move)

if __name__ == "__main__":
    main()
