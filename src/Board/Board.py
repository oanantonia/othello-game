import string

from texttable import Texttable

class InvalidMoveException(Exception):
    pass

class ColorDoesNotExistException(Exception):
    pass

class Board:
    def __init__(self):
        self.empty = 0
        self.black = 1
        self.white = 2
        self.__board = [[self.empty for _ in range (8)] for _ in range (8)]

        #Setting the first 4 pieces that are in the middle of the board at the start of the game
        self.__board[3][3] = self.white
        self.__board[4][3] = self.black
        self.__board[3][4] = self.black
        self.__board[4][4] = self.white

    def check_move(self, row: int, column: int, color: int) -> bool:
        """
        Checks the validity of the move by making sure that the new piece is placed inside the board bounds, on an empty cell
        and sandwiches opposite colored pieces and no empty spaces, together with an already placed piece of the same color.
        :param row: the row coordinate
        :param column: the column coordinate
        :param color: the color code (1/2)
        :return: bool
        """
        #check bounds
        if not (0 <= row < 8 and 0 <= column < 8):
            return False

        #check if the cell is empty
        if self.__board[row][column] != self.empty:
            return False

        #check if we can find a piece of the same colour, which sandwiches opposite-colour pieces in between with no empty spaces

        #determine opponent color
        if color == self.black:
            other_color = self.white
        elif color == self.white:
            other_color = self.black
        else:
            raise ColorDoesNotExistException("This color does not exist!")

        for d1 in [-1, 1, 0]:
            for d2 in [-1, 1, 0]:
                if d1 == 0 and d2 == 0:
                    continue

                r, c = row + d1, column + d2
                found_opposite = False

                while 0 <= r < 8 and 0 <= c < 8:
                    if self.__board[r][c] == other_color:
                        found_opposite = True
                    elif self.__board[r][c] == color:
                        if found_opposite:
                            return True
                        else:
                            break #own color is found
                    else:
                        break #empy space is found

                    r += d1
                    c += d2

        return False

    def click(self, row: int, column: int, color: int) -> None:
        """
        Makes a move if it is valid, flipping the opposite colored pieces that get sandwiched
        :param row: the row coordinate
        :param column: the column coordinate
        :param color: the color code (1/2)
        :return: None
        """
        if not self.check_move(row, column, color):
            raise InvalidMoveException("This move is not permitted!")

        #place new piece
        self.__board[row][column] = color

        if color == self.black:
            other_color = self.white
        elif color == self.white:
            other_color = self.black
        else:
            raise ColorDoesNotExistException("This color does not exist!")

        #flip pieces
        for d1 in [-1, 1, 0]:
            for d2 in [-1, 1, 0]:
                if d1 == 0 and d2 == 0:
                    continue

                r, c = row + d1, column + d2
                flip = []

                while 0 <= r < 8 and 0 <= c < 8:
                    if self.__board[r][c] == other_color:
                        flip.append((r, c))
                    elif self.__board[r][c] == color:
                        for fr, fc in flip:
                            self.__board[fr][fc] = color
                        break
                    else:
                        break

                    r += d1
                    c += d2

    def get_score(self) -> tuple[int, int]:
        #The score is determined by the number of pieces of the same color
        black_score = 0
        white_score = 0

        for row in self.__board:
            for cell in row:
                if cell == self.black:
                    black_score += 1
                elif cell == self.white:
                    white_score += 1

        return black_score, white_score

    def get_valid_moves(self, color: int) -> list[tuple[int, int]]:
        """
        Returns a list of all valid moves for the given color.
        :param color: the color code (1/2)
        :return: list[tuple[int, int]]
        """
        valid_moves =[]

        for row in range(8):
            for column in range(8):
                if self.check_move(row, column, color):
                    valid_moves.append((row, column))

        return valid_moves

    def get_finish(self) -> bool:
        """
        Determine whether the game is finished or not.
        :return: bool
        """
        if self.get_valid_moves(self.black) == [] and self.get_valid_moves(self.white) == []:
            return True
        return False

    def get_board(self):
        return self.__board

    def __str__(self):
        board = Texttable()
        board.header([" "] + list(string.ascii_uppercase[0:8]))
        i = 1
        for row in self.__board:
            new_row = [i]
            for cell in row:
                if cell == 1:
                    new_row.append("●")
                elif cell == 2:
                    new_row.append("○")
                else:
                    new_row.append(" ")

            board.add_row(new_row)
            i += 1
        return board.draw()


