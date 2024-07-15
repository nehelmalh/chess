from abc import ABC, abstractmethod


class Piece(ABC):
    def __init__(self, color: str) -> None:
        self.color = color
        self.type = None

    def is_white(self) -> bool:
        return self.color == 0

    def get_position(self) -> list:
        return self.position

    def set_position(self, new_position):
        self.position = new_position

    def _is_same_color(self, board_status, new_row, new_col, color) -> bool:
        piece_rep = board_status[new_row][new_col]
        if piece_rep > 0:
            color_piece = 0
        else:
            color_piece = 1
        return color == color_piece

    def unrestricted_legal_moves(self, range_of_moves, current_position, board_status):
        legal_moves = []
        row, col = current_position

        for move in range_of_moves:
            new_row = row
            new_col = col

            while True:
                row_move, col_move = move
                new_row += row_move
                new_col += col_move
                if new_row < 0 or new_row >= 8 or new_col < 0 or new_col >= 8:
                    break
                if not board_status[new_row][new_col]:
                    legal_moves.append((new_row, new_col))
                else:
                    piece_rep = board_status[new_row][new_col]
                    if piece_rep > 0:
                        color_piece = 0
                    else:
                        color_piece = 1
                    if self.color != color_piece:
                        legal_moves.append((new_row, new_col))
                        break
                    else:
                        break
        return legal_moves

    def restricted_legal_moves(self, range_of_moves, current_position, board_status):
        legal_moves = []
        row, col = current_position
        for move in range_of_moves:
            new_row = row
            new_col = col

            row_move, col_move = move
            new_row += row_move
            new_col += col_move
            if new_row < 0 or new_row >= 8 or new_col < 0 or new_col >= 8:
                continue
            if not board_status[new_row][new_col]:
                legal_moves.append((new_row, new_col))
            else:
                if self._is_same_color(board_status, new_row, new_col, self.color):
                    legal_moves.append((new_row, new_col))
                    continue
                else:
                    continue
        return legal_moves

    @abstractmethod
    def get_legal_moves(self):
        raise NotImplementedError()

    @abstractmethod
    def print_friendly(self):
        raise NotImplementedError()


class Pawn(Piece):
    def __init__(self, color) -> None:
        super().__init__(color)
        self.points = 1
        # Range of moves can be based on color
        # We can init

    def print_friendly(self):
        return "p" if self.color else "P"

    # For some pieces these will be the same
    # For king we would need additional checks
    # Make a end state
    # Make the queen
    def get_legal_moves(
        self, current_position: tuple, board_status: list[list]
    ) -> list[tuple]:
        range_of_moves = [(1, 0), (1, 1), (1, -1)]
        take_moves = [(1, 1), (1, -1)]
        # Make a more generic set of moves and pop/update based on num moves
        row, column = current_position
        legal_moves = []
        if self.is_white() and row == 1:
            return [(row + 1, column), (row + 2, column)]
        elif not self.is_white() and row == 6:
            return [(row - 1, column), (row - 2, column)]

        for move in range_of_moves:
            if self.is_white():
                row_move, column_move = move
            else:
                row_move, column_move = move
                row_move = -1 * row_move
            new_row = row + row_move
            new_col = column + column_move
            if not board_status[new_row][new_col] and move not in take_moves:
                legal_moves.append((new_row, new_col))
            elif board_status[new_row][new_col]:
                if not self._is_same_color(board_status, new_row, new_col, self.color):
                    legal_moves.append((new_row, new_col))
        return legal_moves


class Queen(Piece):
    def __init__(self, color) -> None:
        super().__init__(color)
        self.points = 9

    def print_friendly(self):
        return "q" if self.color else "Q"

    def get_legal_moves(
        self, current_position: tuple, board_status: list[list]
    ) -> list[tuple]:
        range_of_moves = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]
        return self.unrestricted_legal_moves(
            range_of_moves, current_position, board_status
        )


class Rook(Piece):
    def __init__(self, color) -> None:
        super().__init__(color)
        self.points = 5

    def print_friendly(self):
        return "r" if self.color else "R"

    def get_legal_moves(
        self, current_position: tuple, board_status: list[list]
    ) -> list[tuple]:
        range_of_moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        return self.unrestricted_legal_moves(
            range_of_moves, current_position, board_status
        )


class Bishop(Piece):
    def __init__(self, color) -> None:
        super().__init__(color)
        self.points = 3

    def print_friendly(self):
        return "b" if self.color else "B"

    def get_legal_moves(
        self, current_position: tuple, board_status: list[list]
    ) -> list[tuple]:
        range_of_moves = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self.unrestricted_legal_moves(
            range_of_moves, current_position, board_status
        )


class Knight(Piece):
    def __init__(self, color) -> None:
        super().__init__(color)
        self.points = 3

    def print_friendly(self):
        return "k" if self.color else "K"

    def get_legal_moves(
        self, current_position: tuple, board_status: list[list]
    ) -> list[tuple]:
        range_of_moves = [
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1),
            (1, 2),
            (-1, 2),
            (1, -2),
            (-1, -2),
        ]
        return self.restricted_legal_moves(
            range_of_moves, current_position, board_status
        )


class King(Piece):
    def __init__(self, color) -> None:
        super().__init__(color)
        self.type = "king"

    def print_friendly(self):
        return "♔" if self.color else "♚"

    def get_legal_moves(
        self, current_position: tuple, board_status: list[list]
    ) -> list[tuple]:
        range_of_moves = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]
        return self.restricted_legal_moves(
            range_of_moves, current_position, board_status
        )
