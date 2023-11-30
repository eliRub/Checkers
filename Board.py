from Soldier import Soldier
from King import King
from victory_GUI import Victory

class Board:

    def __init__(self, window):
        self.window = window
        self.buttons_list = []
        self.black_soldiers_death = 0
        self.white_soldiers_death = 0
        self.first_button_pressed = None
        self.second_button_pressed = None
        self.the_turn_of = "white"
        self.setup_board()

    def setup_board(self):
        """ Initialize the 'buttons_list' that all the calculations will be in. """
        for i in range(8):
            temp_row_arr: list[Soldier | None] = []
            for j in range(8):
                if (i + j) % 2 == 0 and i <= 2:
                    soldier = Soldier("black")
                elif (i + j) % 2 == 0 and i >= 5:
                    soldier = Soldier("white")
                else:
                    soldier = None
                temp_row_arr.append(soldier)
            self.buttons_list.append(temp_row_arr)

    def handle_square_press(self, row, column):
        """ This function is checking if the move is legal, and returns True to the BoardGUI if a move should be made."""
        while True:
            # Canceled all the moves the user doing if it's not his turn.
            if self.buttons_list[row][column] is not None and self.the_turn_of not in self.buttons_list[row][column].color:
                self.first_button_pressed = None
                self.second_button_pressed = None
                break
            if self.first_button_pressed is None and self.buttons_list[row][column] is not None:
                self.first_button_pressed = (row, column)
                break
            elif self.second_button_pressed is None and self.first_button_pressed is not None and \
                self.buttons_list[row][column] is None and (
                self.buttons_list[self.first_button_pressed[0]][self.first_button_pressed[1]].color == "white_king" or
                self.buttons_list[self.first_button_pressed[0]][self.first_button_pressed[1]].color == "black_king"):

                self.second_button_pressed = (row, column)
                valid = self.buttons_list[self.first_button_pressed[0]][self.first_button_pressed[1]].check_move(
                        source=self.first_button_pressed, dest=self.second_button_pressed)
                if valid:
                    valid2, opponent_row, opponent_column = self.check_king_move()
                    if not valid2:
                        self.first_button_pressed = None
                        self.second_button_pressed = None
                        break
                    self.move_king(opponent_row, opponent_column)
                    first_button_to_return = self.first_button_pressed
                    second_button_to_return = self.second_button_pressed
                    self.first_button_pressed = None
                    self.second_button_pressed = None
                    self.the_turn_of = "black" if self.the_turn_of == "white" else "white"
                    return first_button_to_return, second_button_to_return, True, False, "", opponent_row, opponent_column

            elif self.second_button_pressed is None and self.first_button_pressed is not None and \
                    self.buttons_list[row][column] is None and "king" not in \
                    self.buttons_list[self.first_button_pressed[0]][self.first_button_pressed[1]].color:
                self.second_button_pressed = (row, column)
                # Checking if this move is legal.
                soldier_to_move = self.first_button_pressed
                (valid, num_of_steps) = self.buttons_list[soldier_to_move[0]][soldier_to_move[1]].check_move(
                                        source=soldier_to_move, dest=self.second_button_pressed)
                if valid:
                    eaten_row = eaten_column = None
                    if num_of_steps == 2:
                        can_eat, eaten_row, eaten_column = self.check_if_2_steps_legal()
                        if not can_eat:
                            self.first_button_pressed = None
                            self.second_button_pressed = None
                            break
                    # Checking if a soldier becoming a king.
                    crown, color = self.crown_checker()
                    self.move_soldier(crown, color)

                    first_button_to_return = self.first_button_pressed
                    second_button_to_return = self.second_button_pressed
                    self.first_button_pressed = None
                    self.second_button_pressed = None
                    self.the_turn_of = "black" if self.the_turn_of == "white" else "white"
                    # check_if_there_more_to_eat()
                    return first_button_to_return, second_button_to_return, True, crown, color, eaten_row, eaten_column
                else:
                    self.first_button_pressed = None
                    self.second_button_pressed = None
                    break
            elif self.second_button_pressed is None and self.first_button_pressed is not None and \
                    self.buttons_list[row][column] is not None:
                self.first_button_pressed = (row, column)
                break
            else:
                # This is needed in case the user pressed 2 buttons with soldiers on them, which is not legal.
                break
        return self.first_button_pressed, self.second_button_pressed, False, False, "", None, None

    def check_if_2_steps_legal(self):
        """ This function checks if a move of 'eating' is legal."""
        middle_square_row = int((self.first_button_pressed[0] + self.second_button_pressed[0]) / 2)
        middle_square_column = int((self.first_button_pressed[1] + self.second_button_pressed[1]) / 2)

        eat_button_color = self.buttons_list[self.first_button_pressed[0]][self.first_button_pressed[1]].color
        eaten_button = self.buttons_list[middle_square_row][middle_square_column]

        if eaten_button is not None and eaten_button.color != eat_button_color:
            self.delete_death_soldiers(eaten_button.color, middle_square_row, middle_square_column)
            return True, middle_square_row, middle_square_column
        return False, None, None

    def delete_death_soldiers(self, dead_color, row_to_delete, column_to_delete):
        """ """
        if dead_color == "white":
            self.white_soldiers_death += 1
        else:
            self.black_soldiers_death += 1
        self.buttons_list[row_to_delete][column_to_delete] = None
        self.check_victory()

    def move_soldier(self, crown, color):
        """ This function replaces the buttons, and also makes the soldier to a king if needed. """
        source_row = self.first_button_pressed[0]
        source_column = self.first_button_pressed[1]
        dest_row = self.second_button_pressed[0]
        dest_column = self.second_button_pressed[1]

        # for a white soldier.
        if crown and color == "white":
            self.buttons_list[source_row][source_column] = King("white_king")
        # for a black soldier.
        elif crown and color == "black":
            self.buttons_list[source_row][source_column] = King("black_king")

        self.buttons_list[dest_row][dest_column] = self.buttons_list[source_row][source_column]
        self.buttons_list[source_row][source_column] = None

    def check_king_move(self):
        eaten_row = eaten_column = None
        source_row = self.first_button_pressed[0]
        source_column = self.first_button_pressed[1]
        dest_row = self.second_button_pressed[0]
        dest_column = self.second_button_pressed[1]

        # Checking which side it's going.
        sorted_positions = sorted([(source_row, source_column), (dest_row, dest_column)])
        start_checking_position = sorted_positions[0]
        row_helper = column_helper = 1
        left_side = True
        if sorted_positions[0][0] < sorted_positions[1][0] and sorted_positions[0][1] > sorted_positions[1][1]:
            column_helper = -1
            left_side = False

        num_of_loops = abs(source_row - dest_row) - 1
        num_of_opponent_soldiers = temp_row = temp_column = 0
        while num_of_loops > 0:
            num_of_loops -= 1
            temp_row = start_checking_position[0] + row_helper
            row_helper += 1
            if left_side:
                temp_column = start_checking_position[1] + column_helper
                column_helper += 1
            else:
                temp_column = start_checking_position[1] + column_helper
                column_helper -= 1

            if self.buttons_list[temp_row][temp_column] is None:
                continue
            elif self.the_turn_of in self.buttons_list[temp_row][temp_column].color:
                return False, None, None
            else:
                num_of_opponent_soldiers += 1
                eaten_row = temp_row
                eaten_column = temp_column
                if num_of_opponent_soldiers >= 2:
                    return False, None, None

        return True, eaten_row, eaten_column

    def move_king(self, opponent_row_to_delete, opponent_column_to_delete):
        source_row = self.first_button_pressed[0]
        source_column = self.first_button_pressed[1]
        dest_row = self.second_button_pressed[0]
        dest_column = self.second_button_pressed[1]

        if opponent_column_to_delete is None:
            self.buttons_list[dest_row][dest_column] = self.buttons_list[source_row][source_column]
            self.buttons_list[source_row][source_column] = None
        else:
            death_color = "white" if "white" in self.buttons_list[opponent_row_to_delete][opponent_column_to_delete].color else "black"
            self.delete_death_soldiers(death_color, opponent_row_to_delete, opponent_column_to_delete)

            self.buttons_list[dest_row][dest_column] = self.buttons_list[source_row][source_column]
            self.buttons_list[source_row][source_column] = None
            self.check_victory()

    def check_if_there_more_to_eat(self):
        eat_row = self.second_button_pressed[0]
        eat_column = self.second_button_pressed[1]
        top_right = ()
        top_left = ()
        bottom_right = ()
        bottom_left = ()

    def crown_checker(self):
        source_row = self.first_button_pressed[0]
        source_column = self.first_button_pressed[1]
        dest_row = self.second_button_pressed[0]
        dest_column = self.second_button_pressed[1]

        # for a white soldier.
        if self.buttons_list[source_row][source_column].color == "white" and dest_row == 0:
            return True, "white"
        # for a black soldier.
        elif self.buttons_list[source_row][source_column].color == "black" and dest_row == 7:
            return True, "black"
        return False, ""

    def check_victory(self):
        """ This function checks the amount of dead soldiers from each group, and declares on a winner,if there is one. """
        if self.white_soldiers_death >= 12:
            self.window.destroy()
            Victory("Black")
        elif self.black_soldiers_death >= 12:
            self.window.destroy()
            Victory("White")
