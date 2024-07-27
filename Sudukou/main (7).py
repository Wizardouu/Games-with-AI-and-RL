import tkinter as tk
from gui import *
from helpers import *


class MainGUI:

    def __init__(self, master):
        self.master = master
        self.master.title("Main GUI")

        # Define button style
        button_style = {"width": 80, "height": 7, "background": "orange", "foreground": "white"}

        self.button1 = tk.Button(self.master, text="Random Solver", font=40, command=self.random_solver, **button_style)
        self.button1.pack(padx=20)  # Add  margin between buttons

        self.button2 = tk.Button(self.master, text="Input Solver", font=40, command=self.input_solver, **button_style)
        self.button2.pack(padx=20)  # Add  margin between buttons

        self.button3 = tk.Button(self.master, text="Interactive", font=40, command=self.interactive_solver,
                                 **button_style)
        self.button3.pack(padx=20)  # Add  margin between buttons

    def random_solver(self):
        self.master.withdraw()  # Hide the main GUI
        gui = tk.Toplevel(self.master)  # Create a new top-level window
        # Add your GUI 1 widgets here
        gui.protocol("WM_DELETE_WINDOW", lambda: self.on_close(gui))
        # TODO RANDOM BOARD GENERATOR
        board_2d = generate_random_board()
        # board_2d = [[int(char) for char in row] for row in board]

        game = SudokuGameSteps(board_2d, "arc_consistency_log.txt")
        game.start()

        root = gui
        app = SudokuUI_Mode_Solver(root, game)
        root.mainloop()

    def input_solver(self):
        self.master.withdraw()  # Hide the main GUI
        gui = tk.Toplevel(self.master)  # Create a new top-level window
        # Add your GUI 1 widgets here
        gui.protocol("WM_DELETE_WINDOW", lambda: self.on_close(gui))

        board = ZERO_BOARD
        board_2d = [[int(char) for char in row] for row in board]

        game = SudokuGame(board_2d, "arc_consistency_log.txt")
        game.start()
        root = gui
        app = SudokuUI_Mode_Input(root, game)
        root.mainloop()

    def interactive_solver(self):
        self.master.withdraw()  # Hide the main GUI
        gui = tk.Toplevel(self.master)  # Create a new top-level window
        # Add your GUI 1 widgets here
        gui.protocol("WM_DELETE_WINDOW", lambda: self.on_close(gui))
        
        board_2d = generate_random_board()
        # board_2d = [[int(char) for char in row] for row in board]

        game = SudokuGameSteps(board_2d, "arc_consistency_log.txt")
        game.start()
        root = gui
        app = SudokuUI_Interactive(root, game)
        root.mainloop()

    def on_close(self, window):
        window.destroy()  # Close the window
        self.master.deiconify()  # Show the main GUI again


def main():
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
