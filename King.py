
class King:

    def __init__(self, color):
        self.color = color


    def check_move(self, source: tuple, dest: tuple):
        first_row = source[0]
        first_column = source[1]
        second_row = dest[0]
        second_column = dest[1]

        if abs(first_row - second_row) == abs(first_column - second_column):
            return True

        return False
