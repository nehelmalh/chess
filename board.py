from abc import ABC, abstractmethod
from enum import Enum
from typing import List

from piece import Pawn


class Players(Enum):
    WHITE = "W"
    BLACK = "B"


BOARD = 8


class ChessBoard(ABC):
    def __init__(self) -> None:
        self.board = None

    @abstractmethod
    def _initialize_board(self):
        raise NotImplementedError()

    @abstractmethod
    def get_board(self):
        raise NotImplementedError()


class ChessBoardArray(ChessBoard):
    def __init__(self) -> None:
        super().__init__()
        self._initialize_board()
        self.num_moves = 0

    def game_status(self):
        print("\033[H\033[J", end="")
        if self.num_moves % 2 == 0:
            print("White to move")
        else:
            print("Black to move")
        self._print_board()

    def _initialize_board(self):
        chess_board = [[None for _ in range(BOARD)] for _ in range(BOARD)]
        for i in range(BOARD):
            chess_board[1][i] = Pawn(Players.WHITE.value)
            chess_board[6][i] = Pawn(Players.BLACK.value)
        self.board = chess_board

    def _print_board(self):
        if self.num_moves % 2 == 0:
            print_board = reversed(self.board)
        else:
            print_board = self.board
        for row in print_board:
            for piece in row:
                if piece is None:
                    print("[ ]", end=" ")
                else:
                    print(f"[{piece.print_friendly()}]", end=" ")
            print()

    def get_board(self) -> List[List]:
        return self.board

    def move(self):
        current_position_input = input(
            "Enter position of piece you want to move as tuple: "
        )
        current_position = tuple(int(x) for x in current_position_input.split(","))
        row = current_position[0]
        column = current_position[1]
        piece = self.board[row][column]
        if not piece:
            print("No piece at current position", current_position)
            return None
        new_position_input = input(
            "Enter position of where you want to move this piece as tuple: "
        )
        new_position = tuple(int(x) for x in new_position_input.split(","))
        legal_moves = piece.get_legal_moves(current_position, self.board)
        if new_position not in legal_moves:
            print(f"New position {new_position} not in legal moves {legal_moves}")
        else:
            piece.increase_moves()
            self.num_moves = self.num_moves + 1
            self.board[row][column] = None
            self.board[new_position[0]][new_position[1]] = piece
        self.game_status()


if __name__ == "__main__":
    board = ChessBoardArray()
    print("Welcome and good luck!")
    board.game_status()
    while True:
        user_input = input("Enter your next move: ")
        if user_input.lower() == "quit":
            break
        method = getattr(board, user_input, None)
        if method and callable(method):
            method()
