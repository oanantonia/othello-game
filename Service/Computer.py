import copy
import math

from src.Board.Board import Board


class Computer:
    def __init__(self, color: int):
        self.color = color
        if self.color == 1:
            self.opponent_color = 2
        elif self.color == 2:
            self.opponent_color = 1

    def easy(self, board: Board) -> None:
        """
        Computer plays in "easy" mode. It picks the winning move if that is possible, avoids making moves that determine the
        player to win next and picks moves that maximize the number of pieces that is has.
        :param board: the board that contains the information of the current game
        :return: None
        """
        #get the possible moves of the computer
        moves = board.get_valid_moves(self.color)

        if not moves:
            return

        move_score = []  #store a "score" for each possible move, determined by how good that move is
        #the higher the score, the better the move is
        for move in moves:
            r, c = move

            #evaluate the outcome of making this move on the current board
            board_copy = copy.deepcopy(board)
            board_copy.click(r, c, self.color)

            #check if the computer can win in one move
            if board_copy.get_finish():
                b, w = board_copy.get_score()
                if (b > w and self.color == 1) or (w > b and self.color == 2):
                    move_score.append((r, c, 100))
                    continue

            opponent_moves = board_copy.get_valid_moves(self.opponent_color)

            #check if the player can win in one move
            lose = False
            for opponent_move in opponent_moves:
                ro, co = opponent_move

                board_copy_2 = copy.deepcopy(board_copy)
                board_copy_2.click(ro, co, self.opponent_color)

                if board_copy_2.get_finish():
                    b, w = board_copy_2.get_score()
                    if (b > w and self.opponent_color == 1) or (w > b and self.opponent_color == 2):
                        lose = True
                        break

            #determine the score of the move
            if lose:
                score = -1  #worst outcome
            else:
                current_b, current_w = board.get_score()
                possible_b, possible_w = board_copy.get_score()
                if self.color == 1:
                    score = possible_b - current_b
                elif self.color == 2:
                    score = possible_w - current_w

            move_score.append((r, c, score))

        mx = -2
        for i in move_score:
            if i[2] > mx:
                mx = i[2]
                chosen_move = (i[0], i[1])

        board.click(chosen_move[0], chosen_move[1], self.color)

    def evaluate(self, board: list, color: int) -> int:
        """
        Evaluates the "score" of one player's positions on the current board.
        This is not the usual score, it is one given by the square_weights matrix, which evaluates the position of a
        players pieces.
            - Corners: These are the most valuable squares since they cannot be reversed by the opponent.
            - Buffers: These are the least valuable squares since they open the corner for the opponent.
            - Borders: These are quite valuable squares. They can still be reverse by the opponent, but it is less likely.
            - Inner Borders: Not the best, but not the worst squares. They open the border for the opponent.
            - Middle: These squares have the same weight since they don't provide any valuable information about weather
            they will or will not remain to one player.
        In order to compute the score, the opponent's piece's position's weight is subtracted.
        :param board: the board that contains the information of the current game
        :param color: the color of the player we want to evaluate
        :return: the score of the player's positions
        """
        square_weights = [
            [500,  -100, 10, 10, 10, 10, -100,  500],
            [-100, -250, -1, -1, -1, -1, -250, -100],
            [10,     -1,  1,  1,  1,  1,   -1,   10],
            [10,     -1,  1,  1,  1,  1,   -1,   10],
            [10,     -1,  1,  1,  1,  1,   -1,   10],
            [10,     -1,  1,  1,  1,  1,   -1,   10],
            [-100, -250, -1, -1, -1, -1, -250, -100],
            [500,  -100, 10, 10, 10, 10, -100,  500]
        ]

        if color == 1:
            opponent_color = 2
        elif color == 2:
            opponent_color = 1

        score = 0

        for row in range(8):
            for column in range(8):
                if board[row][column] == color:
                    score += square_weights[row][column]
                elif board[row][column] == opponent_color:
                    score -= square_weights[row][column]

        return score

    def minimax(self, board: Board, depth: int, computer: bool) -> int:
        """
        The MiniMax algorithm, adapted to this implementation of the Othello game.
        Recursively simulates moves in order to provide the best outcome.
        The computer is the maximizing player and the user is the minimizing player.
        :param board: the board that contains the information of the current game
        :param depth: the number of moves that the computer looks ahead at
        :param computer: whether the computer player or not
        :return: the best score found
        """
        if depth == 0 or board.get_finish():
            return self.evaluate(board.get_board(), self.color)
        if computer:
            score = -math.inf
            moves = board.get_valid_moves(self.color)
            if not moves:
                return self.minimax(board, depth - 1, False)
            for move in moves:
                new_board = copy.deepcopy(board)
                new_board.click(move[0], move[1], self.color)
                score = max(score, self.minimax(new_board, depth - 1, False))
            return score
        else:
            score = math.inf
            moves = board.get_valid_moves(self.opponent_color)
            if not moves:
                return self.minimax(board, depth - 1, True)
            for move in moves:
                new_board = copy.deepcopy(board)
                new_board.click(move[0], move[1], self.opponent_color)
                score = min(score, self.minimax(new_board, depth - 1, True))
            return score

    def hard(self, board: Board) -> None:
        """
        Computer plays in "hard" mode. It simulates 3 moves in advance and chooses the path witch would provide the highest score.
        :param board: the board that contains the information of the current game
        :return: None
        """
        best_score = -math.inf
        best_move = None

        moves = board.get_valid_moves(self.color)

        if not moves:
            return

        for move in moves:
            board_copy = copy.deepcopy(board)
            board_copy.click(move[0], move[1], self.color)

            score = self.minimax(board_copy, 3, False)

            if score > best_score:
                best_score = score
                best_move = move

        if best_move:
            board.click(best_move[0], best_move[1], self.color)
