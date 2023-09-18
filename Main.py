import chess
import chess.svg
import chess.engine

# Simple evaluation function (material count)
def evaluate(board):
    piece_values = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9}
    score = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            if piece.color == chess.WHITE:
                score += piece_values.get(piece.piece_type, 0)
            else:
                score -= piece_values.get(piece.piece_type, 0)

    return score

# Alpha-Beta pruning with iterative deepening
def alpha_beta(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate(board)

    legal_moves = list(board.legal_moves)
    if maximizing_player:
        best_value = -float('inf')
        for move in legal_moves:
            board.push(move)
            value = alpha_beta(board, depth - 1, alpha, beta, False)
            board.pop()
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_value
    else:
        best_value = float('inf')
        for move in legal_moves:
            board.push(move)
            value = alpha_beta(board, depth - 1, alpha, beta, True)
            board.pop()
            best_value = min(best_value, value)
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value

# Iterative deepening search with Alpha-Beta pruning
def find_best_move(board, depth):
    best_move = None
    best_value = -float('inf')
    alpha = -float('inf')
    beta = float('inf')

    for d in range(1, depth + 1):
        legal_moves = list(board.legal_moves)
        for move in legal_moves:
            board.push(move)
            value = alpha_beta(board, d, alpha, beta, False)
            board.pop()
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
        print(f"Depth {d}: Best Move = {best_move}, Value = {best_value}")

    return best_move

# Main function
def main():
    board = chess.Board()
    depth = 4  # Set the search depth

    while not board.is_game_over():
        print(board)
        if board.turn == chess.WHITE:
            # White's turn - find and make the best move
            best_move = find_best_move(board, depth)
            board.push(best_move)
        else:
            # Black's turn - simple random move for demonstration
            move = chess.Move.from_uci("e7e5")
            board.push(move)

if __name__ == "__main__":
    main()
