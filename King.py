
class King:

    def __init__(self, color):
        self.color = color

    @staticmethod
    def check_move(source: tuple, dest: tuple):
        """ Checks that the move the user made is legal in terms of the direction of the move.
            That is, checking that he does not jump straight....
        """

        first_row = source[0]
        first_column = source[1]
        second_row = dest[0]
        second_column = dest[1]

        if abs(first_row - second_row) == abs(first_column - second_column):
            return True

        return False
