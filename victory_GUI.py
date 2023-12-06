import tkinter as tk
import subprocess
import os

class Victory:

    def __init__(self, wining_color: str):
        self.wining_color = wining_color
        self.window_setup()

    def window_setup(self):
        """ Sets up the GUI of the 'Victory' window."""
        window = tk.Tk()
        window.geometry("600x400")
        window.title("VICTORY!")

        title_frame = tk.Frame(master=window, width=600, height=200)
        title_frame.pack()

        victory_label = tk.Label(master=title_frame, text=f"{self.wining_color} WON!", font='Courier 25 underline')
        victory_label.pack()

        buttons_frame = tk.Frame(master=window, width=600, height=400)
        buttons_frame.pack()
        quit_button = tk.Button(master=buttons_frame,
                                activebackground="GREEN",
                                width=30,
                                height=6,
                                text="Quit",
                                bg="lightgreen",
                                command=window.destroy)
        quit_button.place(relx=0.3, rely=0.1)
        play_again_button = tk.Button(master=buttons_frame,
                                      activebackground="GREEN",
                                      width=30,
                                      height=6,
                                      text="Play Again",
                                      bg="lightgreen",
                                      command=lambda w=window: self.new_game(w))
        play_again_button.place(relx=0.3, rely=0.5)

        window.mainloop()

    def new_game(self, this_window):
        """ In case the user press the 'play again' button, this function will be executed."""
        this_window.destroy()

        current_directory = os.path.dirname(os.path.abspath(__file__))
        main_script_path = os.path.join(current_directory, 'main.py')
        subprocess.call(['python', main_script_path])
