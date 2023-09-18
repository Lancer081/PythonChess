import chess
import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set the window dimensions
window_width = 400
window_height = 400

# Set the square size and colors
square_size = window_width // 8
light_color = (255, 206, 158)
dark_color = (209, 139, 71)

# Initialize the chessboard
board = chess.Board()
depth = 3  # Set the search depth

# Create the Pygame window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Chess Engine")

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

# Negamax search with simple evaluation and fixed depth
def negamax(board, depth, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    legal_moves = list(board.legal_moves)
    best_value = -float('inf')

    for move in legal_moves:
        board.push(move)
        value = -negamax(board, depth - 1, not maximizing_player)
        board.pop()
        best_value = max(best_value, value)

    return best_value

# Find the best move using negamax with fixed depth
def find_best_move(board, depth):
    legal_moves = list(board.legal_moves)
    best_move = None
    best_value = -float('inf')

    for move in legal_moves:
        board.push(move)
        value = -negamax(board, depth - 1, False)
        board.pop()
        if value > best_value:
            best_value = value
            best_move = move

    return best_move

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Draw the chessboard
    for y in range(8):
        for x in range(8):
            rect = pygame.Rect(x * square_size, y * square_size, square_size, square_size)
            color = light_color if (x + y) % 2 == 0 else dark_color
            pygame.draw.rect(window, color, rect)

    # Draw the pieces on the chessboard
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            piece_image = pygame.image.load(f"images/{piece.symbol()}.png")  # Replace with your piece images
            piece_image = pygame.transform.scale(piece_image, (square_size, square_size))
            piece_rect = piece_image.get_rect()
            piece_rect.topleft = (chess.square_file(square) * square_size, chess.square_rank(square) * square_size)
            window.blit(piece_image, piece_rect)

    # Check for user input and make moves for the engine
    if not board.is_game_over() and board.turn == chess.WHITE:
        # White's turn - find and make the best move
        best_move = find_best_move(board, depth)
        board.push(best_move)

    pygame.display.update()

# Quit Pygame
pygame.quit()
