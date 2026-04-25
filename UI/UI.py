from src.Board.Board import Board
from src.Service.Computer import Computer


class InvalidColorException(Exception):
    pass


class InvalidInputException(Exception):
    pass


class UI:
    def __init__(self, board: Board, computer: Computer):
        self.board = board
        self.computer = computer

    def choose_color(self) -> int:
        """
        Lets the user choose the color of the pieces they want to play with.
        :return: the code of the chosen color (1/2)
        """
        choice = input("Choose color(black/white):").strip().lower()

        if choice == 'black':
            color = 1
            self.computer.color = 2
        elif choice == 'white':
            color = 2
            self.computer.color = 1
        else:
            raise InvalidColorException("This color doesn't exist!")

        return color

    def choose_difficulty(self) -> int:
        """
        Lets the user choose the difficulty of the game.
        :return: the code of the chosen color (1/2)
        """
        choice = input("Choose difficulty(easy/hard):").strip().lower()

        if choice == 'easy':
            difficulty = 1
        elif choice == 'hard':
            difficulty = 2
        else:
            raise InvalidInputException("This difficulty doesn't exist!")

        return difficulty

    def finish(self, color: int) -> None:
        """
        Prints the suitable message when the game is finished.
        :param color: the color of the player
        :return: None
        """
        score = self.board.get_score()
        if (score[0] > score[1] and color == 1) or (score[0] < score[1] and color == 2):
            print("You Won! :D")
        elif (score[0] < score[1] and color == 1) or (score[0] > score[1] and color == 2):
            print("You Lost! :(")
        else:
            print("Draw! :]")

    def run_computer(self, difficulty: int) -> None:
        if difficulty == 1:
            self.computer.easy(self.board)
        elif difficulty == 2:
            self.computer.hard(self.board)

    def choose_move(self) -> tuple[int, int]:
        print("Choose your move!")
        r = int(input("Enter row number:")) - 1

        if r < 0 or r > 7:
            raise InvalidInputException("Invalid row number!")

        c = input("Enter column letter:").strip().upper()
        c = ord(c) - 65

        if c < 0 or c > 7:
            raise InvalidInputException("Invalid column letter!")

        return r, c

    def run(self):
        first_run = True
        color = 1
        difficulty = 1

        while True:
            try:
                if first_run:
                    color = self.choose_color()
                    difficulty = self.choose_difficulty()
                    first_run = False
                    if color == 2:
                        print(self.board)
                        self.run_computer(difficulty)

                if self.board.get_finish():
                    print(self.board)
                    self.finish(color)
                    break

                print(self.board)

                if not self.board.get_valid_moves(color):
                    print("You have no moves!")

                else:
                    r, c = self.choose_move()

                    self.board.click(r, c, color)

                    print(self.board)

                if self.board.get_valid_moves(self.computer.color):
                    self.run_computer(difficulty)
                else:
                    print("Opponent has no moves!")

            except Exception as e:
                print(e)


