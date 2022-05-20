import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from .board import Board


class Game:
    def __init__(self, screen):
        """
        initiates game
        :param screen: the screen
        """
        self._init()
        self.screen = screen

    def update(self):
        """
        update the game according to recnt actions
        :return: void
        """
        self.board.draw(self.screen)
        row, col = self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
        return row, col

    def _init(self):
        """
        initiates the game params
        :return: void
        """
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self):
        """
        return who won
        :return: the winner's color
        """
        return self.board.winner()

    def reset(self):
        """
        resets game
        :return: void
        """
        self._init()

    def select(self, row, col):
        """
        checks if the piece selected can be moved
        :param row: the row the piece is in
        :param col: the column the piece is in
        :return:
        """
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.moves_options(piece)
            return col, row

        return False, False

    def _move(self, row, col):
        """
        moves a piece
        :param row: the row you want to move the piece to
        :param col: the column you want to move the piece to
        :return: true if can be moved, false if not
        """
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        """
        draws the moves a player can do with the piece its on
        :param moves: the table that says where player can move
        :return: void
        """
        row, col = 0, 0
        for move in moves:
            row, col = move
            pygame.draw.circle(self.screen, BLUE,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)
        return row, col

    def change_turn(self):
        """
        switches turns
        :return:
        """
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED