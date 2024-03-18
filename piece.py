from abc import ABC, abstractmethod


class Piece(ABC):
    def __init__(self, color: str) -> None:
        self.color = color
        self.num_moves = 0

    def increase_moves(self) -> int:
        self.num_moves = self.num_moves + 1

    def get_color(self) -> str:
        return self.color

    def get_position(self) -> list:
        return self.position

    def set_position(self, new_position):
        self.position = new_position

    @abstractmethod
    def get_legal_moves(self):
        raise NotImplementedError()

    @abstractmethod
    def print_friendly(self):
        raise NotImplementedError()

        # Dummy representation for testing

    # def move(self, new_position):
    #     if new_position in self.get_legal_moves():
    #         self.position = new_position


class Pawn(Piece):
    def __init__(self, color) -> None:
        super().__init__(color)

    def print_friendly(self):
        return "BPwn" if self.color == "B" else "WPwn"

    # Moves would be of type (0,1)/(1,1) and for black (0,-1)/(1,-1)
    # Split based on kill moves and move moves, kill moves only available when occupied
    # For some pieces these will be the same
    # For king we would need additional checks
    # Does the piece figure out its legal moves from the board its give
    # OR the board Engine asks for the pawns possible moves and decides which is legal
    # Figure out a way
    def get_legal_moves(self, current_position: tuple, board_status: list[list]):
        row = current_position[0]
        column = current_position[1]
        if self.num_moves == 0:
            if self.color == "W":
                return [(row + 1, column), (row + 2, column)]
            else:
                return [(row + 1, column), (row + 2, column)]
        else:
            if self.color == "W":
                if not board_status[row + 1][column]:
                    return [(row + 1, column)]
                else:
                    print("No moves available for current position", current_position)
                    return None
            else:
                if not board_status[row - 1][column]:
                    return [(row - 1, column)]
                else:
                    print("No moves available for current position", current_position)
                    return None
