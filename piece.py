from abc import ABC, abstractmethod 

ROWS = 8

class Piece(ABC):

    def __init__(self, color) -> None:
        self.color = color
        # self.position = position
        self.num_moves = 0

    def get_color(self) -> str: 
        return self.color
    
    # def get_position(self) -> list:
    #     return self.position
    
    # def set_position(self, new_position):
    #     self.position = new_position

    @abstractmethod
    def get_legal_moves(self):
        raise NotImplementedError()

    # def move(self, new_position):
    #     if new_position in self.get_legal_moves():
    #         self.position = new_position

class Pawn(Piece):

    def __init__(self, color, position) -> None:
        super().__init__(color, position)
    
    def get_legal_moves(self, current_position, board_status):
        if self.num_moves == 0:
            return []



