import tkinter as tk
from PIL import Image, ImageTk
from colorama import Fore
from Board import Board


class BoardGUI:

    def __init__(self):
        self.window = tk.Tk()
        self.board = Board(window=self.window)
        self.buttons = []
        self.setup_board()


    def setup_board(self):
        """ This function initializing the GUI of the board. """
        # Window
        self.window.title("Checkers!")
        self.window.geometry("650x640")

        # Title Frame
        title_frame = tk.Frame(master=self.window, width=650, height=70)
        title_frame.pack()
        title_label = tk.Label(master=title_frame, text="Hi there, have fun!", font='Courier 25 underline')
        title_label.place(relx=0.2, rely=0.2)

        # Board Frame
        board_frame = tk.Frame(master=self.window, width=650, height=570)
        board_frame.pack()

        # Load and resize images
        black_soldier = Image.open("./images/black_soldier.png")
        white_soldier = Image.open("./images/white_soldier.png")

        square_size = 60
        black_soldier = black_soldier.resize((square_size+7, square_size))
        white_soldier = white_soldier.resize((square_size+7, square_size))

        black_soldier = ImageTk.PhotoImage(black_soldier)
        white_soldier = ImageTk.PhotoImage(white_soldier)

        # Buttons
        for i in range(8):
            row = []
            for j in range(8):
                # Creating a square with the right color.
                square_color = "#8B5A2B" if (j + i) % 2 == 0 else "#CDAA7D"
                # The (width, height) in this button means 74 and 65 pixels, because I added an image to it.
                # This is for the white soldiers.
                if (j + i) % 2 == 0 and i <= 2:
                    button = tk.Button(master=board_frame,
                                       image=black_soldier,
                                       activebackground="YELLOW",
                                       width=74,
                                       height=65,
                                       bg=square_color,
                                       command=lambda b_row=i, b_column=j: self.handle_square_press(b_row, b_column))
                # This is for the black soldiers.
                elif (j + i) % 2 == 0 and i >= 5:
                    button = tk.Button(master=board_frame,
                                       image=white_soldier,
                                       activebackground="YELLOW",
                                       width=74,
                                       height=65,
                                       bg=square_color,
                                       command=lambda b_row=i, b_column=j: self.handle_square_press(b_row, b_column))
                # This is for the squares between the white and black soldiers.
                elif (i + j) % 2 == 0:
                    button = tk.Button(master=board_frame,
                                       activebackground="YELLOW",
                                       width=10,
                                       height=4,
                                       bg=square_color,
                                       command=lambda b_row=i, b_column=j: self.handle_square_press(b_row, b_column))
                # This is for squares that are not played on.
                else:
                    # The (width, height) in this button means width of 10 average characters. and height of 4 lines.
                    button = tk.Button(master=board_frame, width=10, height=4, bg=square_color)
                    # Disables all the un-plays squares.
                    button["state"] = "disable"

                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)
        
        # Testing
        # for i in range(8):
        #     for j in range(8):
        #         if self.board.buttons_list[i][j] is not None and self.board.buttons_list[i][j].color == "white":
        #             print(Fore.LIGHTWHITE_EX + self.board.buttons_list[i][j].color, end="||" + Fore.RESET)
        #         elif self.board.buttons_list[i][j] is not None:
        #             print(Fore.LIGHTBLACK_EX + self.board.buttons_list[i][j].color, end="||" + Fore.RESET)
        #         else:
        #             print(self.board.buttons_list[i][j], end="||")  # == None
        #     print()
        self.window.mainloop()
        print("\n----------------------------------------------------\n")
        for i in range(8):
            for j in range(8):
                if self.board.buttons_list[i][j] is not None and (self.board.buttons_list[i][j].color == "white" or self.board.buttons_list[i][j].color == "white_king"):
                    print(Fore.LIGHTWHITE_EX + self.board.buttons_list[i][j].color, end="||" + Fore.RESET)
                elif self.board.buttons_list[i][j] is not None:
                    print(Fore.LIGHTBLACK_EX + self.board.buttons_list[i][j].color, end="||" + Fore.RESET)
                else:
                    print(self.board.buttons_list[i][j], end="||")  # == None
            print()

    def handle_square_press(self, row, column):
        """ This function sends the row and column of the pressed button to the backend, and if the backend returns True,
            then a move will be made in the GUI. """
        (first, second, move, crown, color, eaten_row, eaten_column) = self.board.handle_square_press(row, column)
        if move:
            self.move(source_button=first, dest_button=second, crown=crown, king_color=color,
                      eaten_row=eaten_row, eaten_column=eaten_column)


    def move(self, source_button, dest_button, crown, king_color, eaten_row, eaten_column):
        """ This function gets a source and destination buttons, and replace between them. """

        source_row, source_column = source_button
        dest_row, dest_column = dest_button

        if eaten_row is not None and eaten_column is not None:
            self.buttons[eaten_row][eaten_column].config(image="", width=10, height=4)

        source_button_widget = self.buttons[source_row][source_column]
        source_button_command = source_button_widget.cget("command")
        dest_button_widget = self.buttons[dest_row][dest_column]
        dest_button_command = dest_button_widget.cget("command")

        source_button_widget.grid(row=dest_row, column=dest_column)
        dest_button_widget.grid(row=source_row, column=source_column)

        self.buttons[dest_row][dest_column] = source_button_widget
        self.buttons[source_row][source_column] = dest_button_widget
            
        dest_button_widget.config(command=source_button_command)
        source_button_widget.config(command=dest_button_command)

        if crown:
            self.make_soldier_king(king_color, dest_row, dest_column)


    def make_soldier_king(self, king_color, dest_row, dest_column):

        if king_color == "white":
            king_image = Image.open("./images/white_king.png")
        else:
            king_image = Image.open("./images/black_king.png")

        square_size = 60
        image_resize = king_image.resize((square_size + 7, square_size))
        king_image = ImageTk.PhotoImage(image_resize)

        button_widget = self.buttons[dest_row][dest_column]
        button_widget.image = king_image

        button_widget.config(image="", width=10, height=4)
        button_widget.config(image=king_image, width=74, height=65)
