from movement import Movement

class Human(Movement):
    def make_move() -> tuple:
        x = int(input())
        y = int(input())
        return tuple(x,y)
        