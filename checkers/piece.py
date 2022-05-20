from .constants import RED, WHITE, SQUARE_SIZE, GREY, CROWN
import pygame


class Piece:
    """

    """
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        """
        creates a piece
        :param row: the row in which the piece is in
        :param col: the column in which the piece is in
        :param color: the piece's color
        """
        self.row = row
        self.col = col
        self.color = color
        self.queen = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        """
        calc piece position (the center of the square its in by pixles)
        :return: void
        """
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_queen(self):
        """
        sets if the piece is a queen
        :return: void
        """
        self.queen = True
    
    def draw(self, screen):
        """
        draws the piece (two circles on top of each other, one functions as an outline
        :param screen: the screen
        :return: void
        """
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(screen, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(screen, self.color, (self.x, self.y), radius)
        if self.queen:
            screen.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    def move(self, row, col):
        """
        sets new position params
        :param row: the row to which the piece was moved to
        :param col: the column to which the piece was moved to
        :return: void
        """
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        """
        return the piece color (rgb)
        :return: the piece rgb values as a string
        """
        return str(self.color)
