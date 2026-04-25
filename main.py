from src.Board.Board import Board
from src.Service.Computer import Computer
from src.GUI.GUI import GUI
from src.UI.UI import UI

if __name__ == "__main__":
    board = Board()
    computer = Computer(2)
    gui = GUI(board, computer)

    gui.run()
