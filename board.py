from abc import ABC, abstractmethod
from typing import List

from piece import Pawn 

BOARD = 8

class ChessBoard(ABC):

    def __init__(self) -> None:
        self.board = None

    @abstractmethod
    def initialize_board(self):
        raise NotImplementedError()

    @abstractmethod
    def get_board(self):
        raise NotImplementedError()


class ChessBoardArray(ChessBoard):
    def __init__(self) -> None:
        super().__init__()
        self.initialize_board()
    
    def _initialize_board(self):
        chess_board = [[None for _ in range(BOARD)] for _ in range(BOARD)]
        for i in range(BOARD):
            chess_board[1][i] = Pawn("W")
            chess_board[6][i] = Pawn("B")
        self.board = chess_board

    def get_board(self) -> List[List]:
        return self.board




