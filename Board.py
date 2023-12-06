from Soldier import Soldier
from King import King
from victory_GUI import Victory

class Board:

    def __init__(self, window):
        self.window = window
        self.buttons_list = []
        self.num_of_dead_black_soldiers = 0
        self.num_of_dead_white_soldiers = 0
        self.first_button_pressed = None
        self.second_button_pressed = None
        self.additional_capture_square = None
        self.the_turn_of = "white"
        self.setup_board()

    def setup_board(self):
        """ Initialize the 'buttons_list' where all the calculations will be. """
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
        """ This function is handle in the user's move, and return orders to the Board GUI."""
        # Cancels all the moves the user doing if it's not his turn.
        # or in case the user have more to eat. and he is not doing the right move.
        if (self.buttons_list[row][column] is not None and self.the_turn_of not in self.buttons_list[row][column].color) or (
                self.additional_capture_square is not None and self.first_button_pressed is None and (
                row != self.additional_capture_square[0] or column != self.additional_capture_square[1])):
            self.first_button_pressed = self.second_button_pressed = None
            return self.first_button_pressed, self.second_button_pressed, False, False, "", None, None
        # Handles the case that the user doing a valid move with the first button.
        elif self.first_button_pressed is None and self.buttons_list[row][column] is not None:
            self.first_button_pressed = (row, column)
            return self.first_button_pressed, self.second_button_pressed, False, False, "", None, None
        # Changes the second click to be the first, when he clicked another soldier on the second click.
        elif self.second_button_pressed is None and self.first_button_pressed is not None and \
                self.buttons_list[row][column] is not None:
            self.first_button_pressed = (row, column)
            return self.first_button_pressed, self.second_button_pressed, False, False, "", None, None
        # Manage the soldier movement.
        elif self.second_button_pressed is None and self.first_button_pressed is not None and \
                self.buttons_list[row][column] is None and (
                "king" not in self.buttons_list[self.first_button_pressed[0]][self.first_button_pressed[1]].color):
            (first_button, second_button, move, crown, color, eaten_row,
             eaten_column) = self.manage_soldier_movement(row, column)
            return first_button, second_button, move, crown, color, eaten_row, eaten_column
        # Manage the king movement.
        elif self.second_button_pressed is None and self.first_button_pressed is not None and \
                self.buttons_list[row][column] is None and (
                self.buttons_list[self.first_button_pressed[0]][self.first_button_pressed[1]].color == "white_king" or
                self.buttons_list[self.first_button_pressed[0]][self.first_button_pressed[1]].color == "black_king"):
            (first_button, second_button, move, crown, color, eaten_row, eaten_column) = self.manage_king_movement(
                row, column)
            return first_button, second_button, move, crown, color, eaten_row, eaten_column
        else:
            # This is needed in case the user pressed 2 buttons with soldiers on them, which is not legal.
            return self.first_button_pressed, self.second_button_pressed, False, False, "", None, None

    def manage_soldier_movement(self, row, column):
        """ In case the user wants to move a soldier, this function checks if the move is legal and does it if it is. """
        self.second_button_pressed = (row, column)
        # Checking if this move is legal.
        soldier_to_move = self.first_button_pressed
        (valid, num_of_steps) = self.buttons_list[soldier_to_move[0]][soldier_to_move[1]].check_move(
            source=soldier_to_move, dest=self.second_button_pressed)
        if valid:
            eaten_row = eaten_column = None
            if num_of_steps == 2 or num_of_steps == -2:
                can_eat, eaten_row, eaten_column = self.check_if_2_steps_legal()
                if not can_eat or (num_of_steps == -2 and self.additional_capture_square is None):
                    self.first_button_pressed = self.second_button_pressed = None
                    return self.first_button_pressed, self.second_button_pressed, False, False, "", None, None
                else:
                    self.delete_death_soldiers(self.buttons_list[eaten_row][eaten_column].color, eaten_row, eaten_column)
                    # Checking if there is more to eat.
                    more_to_eat = self.got_more_to_eat()
                    if more_to_eat:
                        self.additional_capture_square = self.second_button_pressed
                    else:
                        self.additional_capture_square = None
                        self.the_turn_of = "black" if self.the_turn_of == "white" else "white"
            # Handle the case where the user got more to eat in one turn, but he tries to do illegal move.
            elif num_of_steps == 1 and self.additional_capture_square is not None:
                self.first_button_pressed = self.second_button_pressed = None
                return self.first_button_pressed, self.second_button_pressed, False, False, "", None, None
            else:
                self.the_turn_of = "black" if self.the_turn_of == "white" else "white"

            # Checking if a soldier becoming a king.
            crown, color = self.crown_checker()
            if crown:
                self.make_soldier_a_king(color)
            self.move_soldier()

            first_button_to_return = self.first_button_pressed
            second_button_to_return = self.second_button_pressed
            self.first_button_pressed = self.second_button_pressed = None
            return first_button_to_return, second_button_to_return, True, crown, color, eaten_row, eaten_column
        else:
            self.first_button_pressed = self.second_button_pressed = None
            return None, None, False, False, "", None, None

    def manage_king_movement(self, row, column):
        """ In case the user wants to move a king, this function checks if the move is legal and does it if it is. """
        self.second_button_pressed = (row, column)
        valid = self.buttons_list[self.first_button_pressed[0]][self.first_button_pressed[1]].check_move(
            source=self.first_button_pressed, dest=self.second_button_pressed)
        if valid:
            valid2, opponent_row_to_eat, opponent_column_to_eat = self.check_king_move()
            if not valid2:
                self.first_button_pressed = None
                self.second_button_pressed = None
                return None, None, False, False, "", None, None
            if opponent_row_to_eat is not None:
                death_color = "white" if "white" in self.buttons_list[opponent_row_to_eat][
                    opponent_column_to_eat].color else "black"
                self.delete_death_soldiers(death_color, opponent_row_to_eat, opponent_column_to_eat)

                # Checking if there is more to eat.
                more_to_eat = self.got_more_to_eat()
                if more_to_eat:
                    self.additional_capture_square = self.second_button_pressed
                else:
                    self.additional_capture_square = None
                    self.the_turn_of = "black" if self.the_turn_of == "white" else "white"
            else:
                self.the_turn_of = "black" if self.the_turn_of == "white" else "white"

            self.move_king()
            first_button_to_return = self.first_button_pressed
            second_button_to_return = self.second_button_pressed
            self.first_button_pressed = None
            self.second_button_pressed = None

            return first_button_to_return, second_button_to_return, True, False, "", opponent_row_to_eat, opponent_column_to_eat

    def check_if_2_steps_legal(self) -> (bool, int, int):
        """ This function checks if a soldier's move of 'eating' is legal. """
        middle_square_row = int((self.first_button_pressed[0] + self.second_button_pressed[0]) / 2)
        middle_square_column = int((self.first_button_pressed[1] + self.second_button_pressed[1]) / 2)

        eat_button_color = self.buttons_list[self.first_button_pressed[0]][self.first_button_pressed[1]].color
        eaten_button = self.buttons_list[middle_square_row][middle_square_column]

        if eaten_button is not None and eaten_button.color != eat_button_color:
            return True, middle_square_row, middle_square_column
        return False, None, None

    def delete_death_soldiers(self, dead_color, row_to_delete, column_to_delete):
        """ This function gets a (row, column) of an eaten soldier and his color, and deletes it from the list. """
        if dead_color == "white":
            self.num_of_dead_white_soldiers += 1
        else:
            self.num_of_dead_black_soldiers += 1
        self.buttons_list[row_to_delete][column_to_delete] = None
        self.check_victory()

    def move_soldier(self):
        """ This function replaces the move buttons. """
        source_row = self.first_button_pressed[0]
        source_column = self.first_button_pressed[1]
        dest_row = self.second_button_pressed[0]
        dest_column = self.second_button_pressed[1]

        self.buttons_list[dest_row][dest_column] = self.buttons_list[source_row][source_column]
        self.buttons_list[source_row][source_column] = None

    def make_soldier_a_king(self, color):
        """ This function turns a soldier into a king. """
        source_row, source_column = self.first_button_pressed
        # for a white soldier.
        if color == "white":
            self.buttons_list[source_row][source_column] = King("white_king")
        # for a black soldier.
        elif color == "black":
            self.buttons_list[source_row][source_column] = King("black_king")

    def check_king_move(self) -> (bool, int, int):
        """ Checks that there is only 1 (or zero) of the opposing soldiers on the track.
            and returns a boolean + (row, column) in case there is one of the enemy soldiers in the track. """
        source_row, source_column = self.first_button_pressed
        dest_row, dest_column = self.second_button_pressed

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
        eaten_row = eaten_column = None
        while num_of_loops > 0:
            num_of_loops -= 1
            temp_row = start_checking_position[0] + row_helper
            row_helper += 1
            temp_column = start_checking_position[1] + column_helper
            column_helper = column_helper + 1 if left_side else column_helper - 1

            if self.buttons_list[temp_row][temp_column] is None:
                continue
            elif self.the_turn_of in self.buttons_list[temp_row][temp_column].color:
                return False, None, None
            elif self.buttons_list[temp_row][temp_column] is not None:
                num_of_opponent_soldiers += 1
                eaten_row = temp_row
                eaten_column = temp_column
                if num_of_opponent_soldiers >= 2:
                    return False, None, None

        return True, eaten_row, eaten_column

    def move_king(self):
        """ This function switches the buttons when a king moves. """
        source_row, source_column = self.first_button_pressed
        dest_row, dest_column = self.second_button_pressed

        self.buttons_list[dest_row][dest_column] = self.buttons_list[source_row][source_column]
        self.buttons_list[source_row][source_column] = None

    def got_more_to_eat(self) -> bool:
        """ This function checks if there are more of the opponent's soldiers to eat in the same turn legally. """
        eat_row, eat_column = self.second_button_pressed
        top_right = (eat_row - 1, eat_column + 1)
        top_left = (eat_row - 1, eat_column - 1)
        bottom_right = (eat_row + 1, eat_column + 1)
        bottom_left = (eat_row + 1, eat_column - 1)

        # I added 1, so I won't need to check separately for 'index out of range' in two squares.
        if (top_right[0] - 1 >= 0 and top_right[1] + 1 <= 7) and (
                self.buttons_list[top_right[0]][top_right[1]] is not None) \
                and (self.the_turn_of not in self.buttons_list[top_right[0]][top_right[1]].color) \
                and (self.buttons_list[top_right[0] - 1][top_right[1] + 1] is None):
            return True
        elif (top_left[0] - 1 >= 0 and top_left[1] - 1 >= 0) and (
                self.buttons_list[top_left[0]][top_left[1]] is not None) \
                and (self.the_turn_of not in self.buttons_list[top_left[0]][top_left[1]].color) \
                and (self.buttons_list[top_left[0] - 1][top_left[1] - 1] is None):
            return True
        elif (bottom_right[0] + 1 <= 7 and bottom_right[1] + 1 <= 7) and (
                self.buttons_list[bottom_right[0]][bottom_right[1]] is not None) \
                and (self.the_turn_of not in self.buttons_list[bottom_right[0]][bottom_right[1]].color) \
                and (self.buttons_list[bottom_right[0] + 1][bottom_right[1] + 1] is None):
            return True
        elif (bottom_left[0] + 1 <= 7 and bottom_left[1] - 1 >= 0) and (
                self.buttons_list[bottom_left[0]][bottom_left[1]] is not None) \
                and (self.the_turn_of not in self.buttons_list[bottom_left[0]][bottom_left[1]].color) \
                and (self.buttons_list[bottom_left[0] + 1][bottom_left[1] - 1] is None):
            return True
        else:
            return False

    def crown_checker(self) -> (bool, str):
        """ This function checks if a pawn has reached the edge of the board and become a king. """
        source_row, source_column = self.first_button_pressed
        dest_row = self.second_button_pressed[0]

        # for a white soldier.
        if self.buttons_list[source_row][source_column].color == "white" and dest_row == 0:
            return True, "white"
        # for a black soldier.
        elif self.buttons_list[source_row][source_column].color == "black" and dest_row == 7:
            return True, "black"
        return False, ""

    def check_victory(self):
        """ This function checks the amount of dead soldiers from each group, and declares on a winner, if there is one. """
        if self.num_of_dead_white_soldiers >= 12:
            self.window.destroy()
            Victory("Black")
        elif self.num_of_dead_black_soldiers >= 12:
            self.window.destroy()
            Victory("White")
            
