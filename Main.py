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
        move = chess.Move.null()  # Initialize move as a null move
        if depth > 0:
            # Perform minimax search with depth
            legal_moves = list(board.legal_moves)
            best_value = -float('inf')
            for legal_move in legal_moves:
                board.push(legal_move)
                value = minimax(board, depth - 1, -float('inf'), float('inf'), False)
                board.pop()
                if value > best_value:
                    best_value = value
                    move = legal_move
        if move != chess.Move.null():
            board.push(move)

    pygame.display.update()

# Quit Pygame
pygame.quit()
