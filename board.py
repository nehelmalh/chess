import copy
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional, Tuple

from piece import Bishop, King, Knight, Pawn, Queen, Rook


class Players(Enum):
    WHITE = 0
    BLACK = 1


BOARD = 8
BOARD_ROWS = ["a", "b", "c", "d", "e", "f", "g", "h"]
KING_SIDE_CASTLE = "O-O"
QUEEN_SIDE_CASTLE = "O-O-O"


PIECE_MAPPING = {1: Pawn, 2: Knight, 3: Bishop, 4: Rook, 5: Queen, 6: King}
CHESS_NOTATION_MAPPING = {"N": Knight, "B": Bishop, "R": Rook, "Q": Queen, "K": King}


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
        self.board = self._initialize_board()
        # better to keep track of the moves themselves vs the num of moves
        self.moves = []
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_rook_kingside_moved = False
        self.white_rook_queenside_moved = False
        self.black_rook_kingside_moved = False
        self.black_rook_queenside_moved = False

    def status(self):
        print("\033[H\033[J", end="")
        if len(self.moves) % 2 == 0:
            print("White to move")
        else:
            print("Black to move")
        self._print_board()

    def _initialize_board(self):
        chess_board = [[None for _ in range(BOARD)] for _ in range(BOARD)]
        for i in range(BOARD):
            chess_board[1][i] = 1
            chess_board[6][i] = -1
        chess_board[0][0] = 4
        chess_board[0][1] = 2
        chess_board[0][2] = 3
        chess_board[0][3] = 5
        chess_board[0][4] = 6
        chess_board[0][5] = 3
        chess_board[0][6] = 2
        chess_board[0][7] = 4

        chess_board[7][0] = -4
        chess_board[7][1] = -2
        chess_board[7][2] = -3
        chess_board[7][3] = -5
        chess_board[7][4] = -6
        chess_board[7][5] = -3
        chess_board[7][6] = -2
        chess_board[7][7] = -4
        return chess_board

    def _convert_position_to_array(self, piece_position: str) -> Tuple[int]:
        assert len(piece_position) == 2, "please enter move position like A3,B4,etc"
        column, row = piece_position[0].lower(), int(piece_position[1])
        assert column in BOARD_ROWS, f"row must be in {BOARD_ROWS}"
        assert int(row) in list(range(1, 9)), f"row {row} must be in {range(1,9)}"
        array_col = ord(column) - 97
        array_row = row - 1
        return (array_row, array_col)

    def castle(self, move, color):
        if self.is_check(color):
            print("Cannot castle while under check")
            return

        if self._check_castle_eligible(color, move):
            if not color:
                if move == KING_SIDE_CASTLE:
                    if self.is_check(color, (0, 4), (0, 6)):
                        print("Cannot castle as king will be under check")
                        return
                    self.board[0][4] = None
                    self.board[0][7] = None
                    self.board[0][6] = 6
                    self.board[0][5] = 4
                elif move == QUEEN_SIDE_CASTLE:
                    if self.is_check(color, (0, 4), (0, 2)):
                        print("Cannot castle as king will be under check")
                        return
                    self.board[0][4] = None
                    self.board[0][0] = None
                    self.board[0][2] = 6
                    self.board[0][3] = 4
            else:
                if move == KING_SIDE_CASTLE:
                    if self.is_check(color, (7, 4), (7, 6)):
                        print("Cannot castle as king will be under check")
                        return
                    self.board[7][4] = None
                    self.board[7][7] = None
                    self.board[7][6] = 6
                    self.board[7][5] = 4
                elif move == QUEEN_SIDE_CASTLE:
                    if self.is_check(color, (7, 4), (7, 2)):
                        print("Cannot castle as king will be under check")
                        return
                    self.board[7][4] = None
                    self.board[7][0] = None
                    self.board[7][2] = 6
                    self.board[7][3] = 4
        else:
            print("Cannot castle.")

    def change_pieced_moved(self, move: tuple[int]):
        if move == (0, 0):
            self.white_rook_queenside_moved = True
        elif move == (0, 4):
            self.white_king_moved = True
        elif move == (0, 7):
            self.white_rook_kingside_moved = True
        elif move == (7, 0):
            self.black_rook_queenside_moved = True
        elif move == (7, 4):
            self.black_king_moved = True
        elif move == (7, 7):
            self.black_rook_kingside_moved = True

    def _check_castle_eligible(self, color, move):
        pieces_eligible = True
        start = 4
        if not color:
            row = 0
            if move == KING_SIDE_CASTLE:
                end = 7
                pieces_eligible = not (
                    self.white_king_moved or self.white_rook_kingside_moved
                )

            elif move == QUEEN_SIDE_CASTLE:
                end = 0
                pieces_eligible = not (
                    self.white_king_moved or self.white_rook_queenside_moved
                )
        else:
            row = 7
            if move == KING_SIDE_CASTLE:
                end = 7
                pieces_eligible = not (
                    self.black_king_moved or self.black_rook_kingside_moved
                )

            elif move == QUEEN_SIDE_CASTLE:
                end = 7
                pieces_eligible = not (
                    self.black_king_moved or self.black_rook_queenside_moved
                )
        return pieces_eligible and self._is_path_clear(start, end, row)

    def _is_path_clear(self, start, end, row) -> bool:
        if start > end:
            start, end = end, start
        for col in range(start + 1, end):
            if self.board[row][col]:
                return False
        return True

    def _print_board(self):
        for n, row in enumerate(reversed(self.board)):
            print(BOARD - n, end=" ")
            for piece_rep in row:
                if piece_rep is None:
                    print("[ ]", end=" ")
                    continue
                elif piece_rep > 0:
                    color = 0
                else:
                    color = 1
                piece = PIECE_MAPPING[abs(piece_rep)](color)
                print(f"[{piece.print_friendly()}]", end=" ")
            print()
        for n in range(BOARD + 1):
            if n == 0:
                print("  ", end=" ")
            else:
                print(chr(ord("`") + n), end="   ")
        print("\n")

    def get_board(self) -> List[List]:
        return self.board

    def king_position(self, color, opposition=False) -> tuple:
        # Black is 1 white is 0
        if color:
            king = -6
        else:
            king = 6
        for row in range(BOARD):
            for column in range(BOARD):
                loc = self.board[row][column]
                if loc and loc == king:
                    return (row, column)

    def find_opponent_pieces(self, color) -> tuple:
        piece_locations = []
        for row in range(BOARD):
            for column in range(BOARD):
                loc = self.board[row][column]
                if loc:
                    # black is 1
                    if not color and loc < 0:
                        piece_locations.append((row, column))
                    elif color and loc > 0:
                        piece_locations.append((row, column))
        return piece_locations

    def move(
        self,
        current_position: Optional[str] = None,
        new_position: Optional[str] = None,
    ):
        color_to_move = len(self.moves) % 2
        print("Color to move: ", color_to_move)
        if self.is_check(color_to_move):
            print("Your king is under check.")
        if not current_position:
            current_position = input(
                "Enter position of piece you want to move as string: "
            )
        current_position = self._convert_position_to_array(current_position)
        row, column = current_position[0], current_position[1]
        piece_rep = self.board[row][column]
        if not piece_rep:
            print("No piece at current position", current_position)
            return
        if piece_rep > 0:
            color = 0
        else:
            color = 1
        piece = PIECE_MAPPING[abs(piece_rep)](color)
        if (color % 2) != color_to_move:
            print("Can only move your own piece")
            return
        if not new_position:
            new_position = input(
                "Enter position of where you want to move piece as string: "
            )
        new_position = self._convert_position_to_array(new_position)
        if self.is_check(color_to_move, current_position, new_position):
            print("Can't make this move as your king will be under check.")
            return
        legal_moves = piece.get_legal_moves(current_position, self.board)
        if new_position not in legal_moves:
            print(f"New position {new_position} not in legal moves {legal_moves}")
            return
        else:
            self.board[row][column] = None
            self.board[new_position[0]][new_position[1]] = piece_rep
            self.moves.append((current_position, new_position))
            self.change_pieced_moved(current_position)
        self.status()
        print("CONVERTED POSITION IS: ", new_position)

    def is_check(self, color: int, current_position=None, new_position=None):
        temp_board = copy.deepcopy(self.board)
        if current_position and new_position:
            piece_rep = temp_board[current_position[0]][current_position[1]]
            temp_board[current_position[0]][current_position[1]] = None
            temp_board[new_position[0]][new_position[1]] = piece_rep

        my_king_location = self.king_position(color)
        opponent_pieces = self.find_opponent_pieces(color)
        for opponent_piece_loc in opponent_pieces:
            opponent_piece = temp_board[opponent_piece_loc[0]][opponent_piece_loc[1]]
            if opponent_piece > 0:
                color = 0
            else:
                color = 1
            piece = PIECE_MAPPING[abs(opponent_piece)](color)
            legal_moves = piece.get_legal_moves(opponent_piece_loc, temp_board)
            if my_king_location in legal_moves:
                print("King is under check")
                return True

    def chess_notation(self, move: str):
        color_to_move = len(self.moves) % 2

        # if move[0].islower():
        #     piece = Pawn(color_to_move)
        #     return

        move = move.upper()

        if move in [KING_SIDE_CASTLE, QUEEN_SIDE_CASTLE]:
            self.castle(move, color_to_move)

    def pawn_star(self, new_position):
        pass


if __name__ == "__main__":
    board = ChessBoardArray()
    print("Welcome and good luck!")
    board.status()
    while True:
        user_input = input("Enter your next move: ")
        if user_input.lower() == "quit":
            break
        method = getattr(board, user_input, None)
        if method and callable(method):
            method()
