import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE, CREAM
from .piece import Piece


def draw_squares(screen):
    """
    draws the board squares
    :param screen: the screen
    :return: void
    """
    screen.fill(BLACK)
    for row in range(ROWS):
        for col in range(row % 2, COLS, 2):
            pygame.draw.rect(screen, CREAM, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


class Board:
    def __init__(self):
        """
        creates a board
        features:
        red_pieces_left, white_pieces_left - how many pieces of each color are on the board
        red_queens, white_queens - how many queens of each color are on the board
        """
        self.board = []
        self.red_pieces_left = self.white_pieces_left = 12
        self.red_queens = self.white_queens = 0
        self.create_board()

    def move(self, piece, row, col):
        """
        moves a piece
        :param piece: the piece that you're moving
        :param row: the row you want to move it to
        :param col: the column you want to move it to
        :return: void
        """
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_queen()
            if piece.color == WHITE:
                self.white_queens += 1
            else:
                self.red_queens += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        """
        creates a 2d table that represents how the board will look like.
        0 - no piece there
        :return: void
        """
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, screen):
        """
        draws the board according to the 2d table
        :param screen: the screen
        :return: void
        """
        draw_squares(screen)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(screen)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_pieces_left -= 1
                else:
                    self.white_pieces_left -= 1
    
    def winner(self):
        """
        return who wins
        :return: the color that won
        """
        if self.white_queens == 1:
            return WHITE
        elif self.red_queens == 1:
            return RED
        
        return None 
    
    def moves_options(self, piece):
        """
        prints what moves the player can do onto the screen
        :param piece: the piece you want to move
        :return: table with the valid moves
        """
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.queen:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.queen:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        """
        returns what move you can do on the left side of the piece
        :param start: the farthest row from where your piece is on the left (till the end of the screen)
        :param stop: the closest row from where your piece is on the left
        :param step: how many steps you can take
        :param color: the piece color
        :param left: the column right next to you on your left
        :param skipped: array of the last squares you've checked and skipped
        :return: the moves you can do
        """
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        """
         returns what move you can do on the right side of the piece
         :param start: the farthest row from where your piece is on the right (till the end of the screen)
         :param stop: the closest row from where your piece is on the right
         :param step: how many steps you can take
         :param color: the piece color
         :param right: the column right next to you on your right
        :param skipped: array of the last squares you've checked and skipped
         :return: the moves you can do
         """
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves