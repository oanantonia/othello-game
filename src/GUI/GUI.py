import pygame
import sys

from src.Board.Board import Board
from src.Service.Computer import Computer

class GUI:
    def __init__(self, board: Board, computer: Computer):
        self.board = board
        self.computer = computer

        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((800, 730))
        pygame.display.set_caption('Reversi/Othello')

    def menu(self):
        self.screen.fill((161, 212, 131))
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, 800, 730), 7, 15)
        title_font = pygame.font.SysFont('ComicSans', 70, True)
        title = title_font.render("Welcome to Othello!", True, (130, 112, 78))
        self.screen.blit(title, (65, 250))
        choice_font = pygame.font.SysFont('Calibri', 40, True)
        choice = choice_font.render("Choose a color! (black is first :))", True, (255, 255, 255))
        self.screen.blit(choice, (140, 350))

        pygame.draw.rect(self.screen, (255, 255, 255), (220, 420, 150, 75), 7, 15)
        pygame.draw.rect(self.screen, (255, 255, 255), (420, 420, 150, 75), 7, 15)

        self.screen.fill((255, 255, 255), (225, 425, 140, 65))
        self.screen.fill((255, 255, 255), (425, 425, 140, 65))

        black = choice_font.render("Black", True, (0, 0, 0))
        white = choice_font.render("White", True, (0, 0, 0))

        self.screen.blit(black, (250, 440))
        self.screen.blit(white, (445, 440))

    def choose_difficulty(self):
        self.screen.fill((161, 212, 131))
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, 800, 730), 7, 15)

        title_font = pygame.font.SysFont('ComicSans', 60, True)
        choice_font = pygame.font.SysFont('Calibri', 40, True)
        title = title_font.render("Choose a difficulty!", True, (255, 255, 255))
        self.screen.blit(title, (120, 250))

        pygame.draw.rect(self.screen, (255, 255, 255), (220, 420, 150, 75), 7, 15)
        pygame.draw.rect(self.screen, (255, 255, 255), (420, 420, 150, 75), 7, 15)

        self.screen.fill((255, 255, 255), (225, 425, 140, 65))
        self.screen.fill((255, 255, 255), (425, 425, 140, 65))

        easy = choice_font.render("Easy", True, (0, 0, 0))
        hard = choice_font.render("Hard", True, (0, 0, 0))

        self.screen.blit(easy, (255, 440))
        self.screen.blit(hard, (450, 440))

    def draw_board(self):
        self.screen.fill((130, 112, 78))
        self.screen.fill((161, 212, 131), (100, 100, 600, 600))

        title_font = pygame.font.SysFont('Calibri', 60, True)
        title = title_font.render("OTHELLO", True, (255, 255, 255))
        self.screen.blit(title, (285, 30))

        pygame.draw.rect(self.screen, (0, 0, 0), (97, 97, 607, 607), 7, 15)
        for row in range(8):
            for column in range(8):
                pygame.draw.rect(self.screen, (0, 0, 0), (column*75+100, row*75+100, 75, 75), 1)

    def draw_pieces(self, board: list):
        for row in range(8):
            for column in range(8):
                if board[row][column] != 0:
                    x = column * 75 + 37.5 + 100
                    y = row * 75 + 37.5 + 100
                    r = 31
                    if board[row][column] == 1:
                        pygame.draw.circle(self.screen, (0, 0, 0), (x, y), r)
                    elif board[row][column] == 2:
                        pygame.draw.circle(self.screen, (255, 255, 255), (x, y), r)

    def draw_moves(self, board: Board, color: int):
        moves = board.get_valid_moves(color)
        for move in moves:
            x = move[1] * 75 + 37.5 + 100
            y = move[0] * 75 + 37.5 + 100
            r = 5
            if color == 1:
                pygame.draw.circle(self.screen, (0, 0, 0), (x, y), r)
            elif color == 2:
                pygame.draw.circle(self.screen, (255, 255, 255), (x, y), r)

    def draw_score(self, board: Board):
        b, w = board.get_score()
        score_font = pygame.font.SysFont('Calibri', 30, True)
        score1 = score_font.render("●" + str(b), True, (0, 0, 0))
        score2 = score_font.render("●" + str(w), True, (255, 255, 255))
        score = score_font.render("Score:", True, (255, 255, 255))
        self.screen.blit(score, (15, 25))
        self.screen.blit(score1, (100, 25))
        self.screen.blit(score2, (100, 55))

    def finish(self, player_color: int):
        self.screen.fill((161, 212, 131))
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, 800, 730), 7, 15)

        score = self.board.get_score()
        font = pygame.font.SysFont('Calibri', 60, True)

        if (score[0] > score[1] and player_color == 1) or (score[0] < score[1] and player_color == 2):
            title = font.render("YOU WON! :)", True, (0, 0, 0))
        elif (score[0] < score[1] and player_color == 1) or (score[0] > score[1] and player_color == 2):
            title = font.render("YOU LOST! :(", True, (0, 0, 0))
        else:
            title = font.render("DRAW! :[", True, (0, 0, 0))

        self.screen.fill((255, 255, 255), (200, 200, 400, 75))
        self.screen.blit(title, (250, 210))

        choice_font = pygame.font.SysFont('Calibri', 40, True)

        pygame.draw.rect(self.screen, (255, 255, 255), (220, 420, 150, 75), 7, 15)
        pygame.draw.rect(self.screen, (255, 255, 255), (420, 420, 150, 75), 7, 15)

        self.screen.fill((255, 255, 255), (225, 425, 140, 65))
        self.screen.fill((255, 255, 255), (425, 425, 140, 65))

        replay = choice_font.render("Replay", True, (0, 0, 0))
        exit_game = choice_font.render("Exit", True, (0, 0, 0))

        self.screen.blit(replay, (240, 440))
        self.screen.blit(exit_game, (460, 440))


    def run(self):
        clock = pygame.time.Clock()
        current_state = "menu1"

        color = 1
        player_color = 1

        game_difficulty = 0

        while True:
            clock.tick(60)

            if current_state == "menu1":
                self.menu()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if 225 <= x <= 365 and 420 <= y <= 490:
                            player_color = 1
                            self.computer.color = 2
                            current_state = "menu2"

                        elif 425 <= x <= 565 and 420 <= y <= 490:
                            player_color = 2
                            self.computer.color = 1
                            current_state = "menu2"

                        pygame.time.wait(300)

            if current_state == "menu2":
                self.choose_difficulty()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if 225 <= x <= 365 and 420 <= y <= 490:
                            game_difficulty = 0
                            current_state = "game"

                        elif 425 <= x <= 565 and 420 <= y <= 490:
                            game_difficulty = 1
                            current_state = "game"

                        pygame.time.wait(300)


            if current_state == "game":
                self.draw_board()
                self.draw_pieces(self.board.get_board())
                self.draw_moves(self.board, color)
                self.draw_score(self.board)

                try:
                    if self.board.get_finish():
                        current_state = "finish"
                        continue

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        if not self.board.get_valid_moves(color):
                            print("You have no moves!")
                            color = self.computer.color

                        if color == player_color and self.board.get_valid_moves(color):
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                x, y = pygame.mouse.get_pos()
                                col = (x - 100) // 75
                                row = (y - 100) // 75

                                self.board.click(row, col, color)

                                color = self.computer.color

                    if color == self.computer.color:
                        self.draw_board()
                        self.draw_pieces(self.board.get_board())
                        self.draw_score(self.board)
                        pygame.display.update()

                        pygame.time.wait(400)

                        if self.board.get_valid_moves(self.computer.color):
                            if game_difficulty == 0:
                                self.computer.easy(self.board)
                            if game_difficulty == 1:
                                self.computer.hard(self.board)
                        else:
                            print("Computer has no moves!")

                        color = player_color

                except Exception as e:
                    continue

            if current_state == "finish":
                pygame.time.wait(400)
                self.finish(player_color)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        if 225 <= x <= 365 and 420 <= y <= 490:
                            self.board = Board()
                            self.computer = Computer(2)
                            self.run()

                        elif 425 <= x <= 565 and 420 <= y <= 490:
                            pygame.quit()
                            sys.exit()

            pygame.display.update()
