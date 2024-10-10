import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.current_player = 'X'
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()
        self.window.mainloop()

    def create_board(self):
        # Create a 3x3 grid of buttons for the Tic Tac Toe board
        for row in range(3):
            for col in range(3):
                # Create a button with specified dimensions and assign the on_click function
                button = tk.Button(self.window, text='', width=10, height=3,
                                  command=lambda r=row, c=col: self.on_click(r, c))
                # Place the button in the correct position on the grid
                button.grid(row=row, column=col)
                # Store the button in the buttons list
                self.buttons[row][col] = button

    def on_click(self, row, col):
        if self.buttons[row][col]['text'] == '':
            self.buttons[row][col]['text'] = self.current_player
            if self.check_winner(row, col):
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_board()
            elif self.check_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self, row, col):
        # Check row
        if all(self.buttons[row][i]['text'] == self.current_player for i in range(3)):
            return True
        # Check column
        if all(self.buttons[i][col]['text'] == self.current_player for i in range(3)):
            return True
        # Check diagonals
        if row == col and all(self.buttons[i][i]['text'] == self.current_player for i in range(3)):
            return True
        if row + col == 2 and all(self.buttons[i][2-i]['text'] == self.current_player for i in range(3)):
            return True
        return False

    def check_draw(self):
        return all(self.buttons[row][col]['text'] != '' for row in range(3) for col in range(3))

    def reset_board(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col]['text'] = ''
        self.current_player = 'X'

if __name__ == "__main__":
    TicTacToe()