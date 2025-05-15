from strategies.movement import Movement
from threading import Event

class Human(Movement):
    def __init__(self, M, N, click):
        self.M = M
        self.N = N
        self.click = click
        self.click_event = Event()
        self.clicked_pos = None

    def set_click_pos(self, row, col):
        self.clicked_pos = (row, col)

    def make_move(self, board) -> tuple:
        self.click_event.clear()    # reset the flag
        self.click_event.wait()  # block until click event flag is true (waits for a click)
        row, col = self.clicked_pos
        if 0 <= row < self.M and 0 <= col < self.N and board[row][col] == 0:
            return self.clicked_pos
        return None
    
    def __str__(self):
        return "Human"