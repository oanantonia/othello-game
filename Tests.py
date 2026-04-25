import copy
import math
from unittest import TestCase

from src.Board.Board import Board, InvalidMoveException, ColorDoesNotExistException
from src.Service.Computer import Computer


class BoardTests(TestCase):
    def setUp(self):
        self.board = Board()

    def test_initialization(self):
        board_state = self.board.get_board()
        self.assertEqual(board_state[3][3], self.board.white)
        self.assertEqual(board_state[4][4], self.board.white)
        self.assertEqual(board_state[3][4], self.board.black)
        self.assertEqual(board_state[4][3], self.board.black)

        self.assertEqual(self.board.get_score()[0], 2)
        self.assertEqual(self.board.get_score()[1], 2)

    def test_valid_move(self):
        self.assertTrue(self.board.check_move(2, 3, self.board.black))
        self.assertTrue(self.board.check_move(3, 2, self.board.black))
        self.assertTrue(self.board.check_move(4, 5, self.board.black))
        self.assertTrue(self.board.check_move(5, 4, self.board.black))

    def test_invalid_move_bounds(self):
        self.assertFalse(self.board.check_move(-1, 0, self.board.black))
        self.assertFalse(self.board.check_move(0, 8, self.board.black))
        self.assertFalse(self.board.check_move(8, 8, self.board.black))

    def test_invalid_move(self):
        self.assertFalse(self.board.check_move(3, 3, self.board.black))

    def test_flips(self):
        self.board.click(2, 3, self.board.black)

        board_state = self.board.get_board()

        self.assertEqual(board_state[2][3], self.board.black)
        self.assertEqual(board_state[3][3], self.board.black)
        self.assertEqual(board_state[4][3], self.board.black)

    def test_invalid_move_raise_exception(self):
        with self.assertRaises(InvalidMoveException):
            self.board.click(0, 0, self.board.black)

    def test_invalid_color_raises_exception(self):
        with self.assertRaises(ColorDoesNotExistException):
            self.board.click(2, 3, 7)

    def test_get_score(self):
        self.board.click(2, 3, self.board.black)

        b_score, w_score = self.board.get_score()
        self.assertEqual(b_score, 4)
        self.assertEqual(w_score, 1)

class ComputerTests(TestCase):
    def setUp(self):
        self.board = Board()
        self.computer_black = Computer(1)
        self.computer_white = Computer(2)

    def test_easy_valid_move(self):
        initial_board = copy.deepcopy(self.board.get_board())

        self.computer_black.easy(self.board)

        self.assertNotEqual(self.board.get_board(), initial_board)

        b_score, w_score = self.board.get_score()
        self.assertEqual(b_score, 4)
        self.assertEqual(w_score, 1)

        initial_board = copy.deepcopy(self.board.get_board())

        self.computer_white.easy(self.board)

        self.assertNotEqual(self.board.get_board(), initial_board)

    def test_hard_valid_move(self):
        initial_board = copy.deepcopy(self.board.get_board())

        self.computer_black.hard(self.board)

        self.assertNotEqual(self.board.get_board(), initial_board)

        b_score, w_score = self.board.get_score()
        self.assertEqual(b_score, 4)
        self.assertEqual(w_score, 1)

        initial_board = copy.deepcopy(self.board.get_board())

        self.computer_white.hard(self.board)

        self.assertNotEqual(self.board.get_board(), initial_board)

    def test_minimax_depth_zero(self):
        score = self.computer_black.minimax(self.board, 0, True)
        self.assertEqual(score, 0)

    def test_minimax_score(self):
        score = self.computer_black.minimax(self.board, 2, True)

        self.assertIsInstance(score, int)
        self.assertNotEqual(score, math.inf)
        self.assertNotEqual(score, -math.inf)

    def test_computers_play_game(self):
        for i in range(2):
            self.computer_black.hard(self.board)
            if self.board.get_finish():
                break

            self.computer_white.easy(self.board)
            if self.board.get_finish():
                break

        b, w = self.board.get_score()
        self.assertEqual(b + w, 8)


