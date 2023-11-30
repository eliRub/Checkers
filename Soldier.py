
class Soldier:

    def __init__(self, color: str):
        self.color = color


    def check_move(self, source: tuple, dest: tuple):
        first_row = source[0]
        first_column = source[1]
        second_row = dest[0]
        second_column = dest[1]

        if self.color == "white":
            # I made sure that the soldier can only do one step at the time.
            if (first_row - second_row) == 1 and abs(first_column - second_column) == 1:
                return True, 1
            elif (first_row - second_row) == 2 and abs(first_column - second_column) == 2:
                return True, 2
            else:
                return False, 0
        else:
            # I made sure that the soldier can only do one step at the time.
            if (second_row - first_row) == 1 and abs(first_column - second_column) == 1:
                return True, 1
            elif (second_row - first_row) == 2 and abs(first_column - second_column) == 2:
                return True, 2
            else:
                return False, 0
