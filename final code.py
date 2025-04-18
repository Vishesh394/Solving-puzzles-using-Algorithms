import tkinter as tk
from tkinter import messagebox
import numpy as np
import random


def show_main_menu(): 
    root.deiconify()

def hide_main_menu():
    root.withdraw()

# Tic Tac Toe Game with Minimax AI
def start_tic_tac_toe():
    hide_main_menu()
    tic_tac_toe_window = tk.Toplevel(root)
    tic_tac_toe_window.title("Tic Tac Toe")
    tic_tac_toe_window.geometry("300x400")
    tic_tac_toe_window.configure(bg="#FCE38A")

    playerX, playerO = "X", "O"
    user_player = playerX
    ai_player = playerO
    curr_player = playerX
    board = [[None for _ in range(3)] for _ in range(3)]
    turns, game_over = 0, False

    def set_tile(row, column):
        nonlocal curr_player, turns, game_over
        if game_over or board[row][column]["text"]:
            return
        board[row][column]["text"] = curr_player
        curr_player = ai_player if curr_player == user_player else user_player
        label["text"] = curr_player + "'s turn"
        check_winner()
        if not game_over and curr_player == ai_player:
            tic_tac_toe_window.after(500, ai_move)

    def ai_move():
        nonlocal curr_player
        best_score = float('-inf')
        best_move = None
        for r in range(3):
            for c in range(3):
                if board[r][c]["text"] == "":
                    board[r][c]["text"] = ai_player
                    score = minimax(board, 0, False)
                    board[r][c]["text"] = ""
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
        if best_move:
            r, c = best_move
            board[r][c]["text"] = ai_player
            curr_player = user_player
            label["text"] = curr_player + "'s turn"
            check_winner()

    def minimax(board_state, depth, is_maximizing):
        result = evaluate(board_state)
        if result is not None:
            return result

        if is_maximizing:
            best = float('-inf')
            for r in range(3):
                for c in range(3):
                    if board_state[r][c]["text"] == "":
                        board_state[r][c]["text"] = ai_player
                        best = max(best, minimax(board_state, depth + 1, False))
                        board_state[r][c]["text"] = ""
            return best
        else:
            best = float('inf')
            for r in range(3):
                for c in range(3):
                    if board_state[r][c]["text"] == "":
                        board_state[r][c]["text"] = user_player
                        best = min(best, minimax(board_state, depth + 1, True))
                        board_state[r][c]["text"] = ""
            return best

    def evaluate(board_state):
        for row in range(3):
            if board_state[row][0]["text"] == board_state[row][1]["text"] == board_state[row][2]["text"] and board_state[row][0]["text"]:
                return 1 if board_state[row][0]["text"] == ai_player else -1
        for col in range(3):
            if board_state[0][col]["text"] == board_state[1][col]["text"] == board_state[2][col]["text"] and board_state[0][col]["text"]:
                return 1 if board_state[0][col]["text"] == ai_player else -1
        if board_state[0][0]["text"] == board_state[1][1]["text"] == board_state[2][2]["text"] and board_state[0][0]["text"]:
            return 1 if board_state[0][0]["text"] == ai_player else -1
        if board_state[0][2]["text"] == board_state[1][1]["text"] == board_state[2][0]["text"] and board_state[0][2]["text"]:
            return 1 if board_state[0][2]["text"] == ai_player else -1
        for r in range(3):
            for c in range(3):
                if board_state[r][c]["text"] == "":
                    return None
        return 0

    def check_winner():
        nonlocal turns, game_over
        turns += 1
        result = evaluate(board)
        if result == 1:
            label.config(text=ai_player + " wins!", fg="red")
            game_over = True
        elif result == -1:
            label.config(text=user_player + " wins!", fg="red")
            game_over = True
        elif turns == 9:
            label.config(text="It's a tie!", fg="blue")
            game_over = True

    def new_game():
        nonlocal turns, game_over, curr_player
        turns, game_over, curr_player = 0, False, user_player
        label.config(text=curr_player + "'s turn", fg="black")
        for r in range(3):
            for c in range(3):
                board[r][c].config(text="")
        if curr_player == ai_player:
            tic_tac_toe_window.after(500, ai_move)

    def return_to_main():
        tic_tac_toe_window.destroy()
        show_main_menu()

    frame = tk.Frame(tic_tac_toe_window, bg="#FCE38A")
    label = tk.Label(frame, text=curr_player + "'s turn", font=("Arial", 16, "bold"), bg="#FCE38A")
    label.grid(row=0, column=0, columnspan=3, pady=10)

    for r in range(3):
        for c in range(3):
            board[r][c] = tk.Button(frame, text="", font=("Arial", 20), width=5, height=2, bg="white",
                                    command=lambda row=r, col=c: set_tile(row, col))
            board[r][c].grid(row=r+1, column=c, padx=5, pady=5)

    tk.Button(frame, text="Restart", font=("Arial", 14), bg="#FF6363", fg="white", command=new_game).grid(row=4, column=0, columnspan=3, pady=10)
    tk.Button(frame, text="Return to Main Menu", font=("Arial", 14), bg="gray", fg="white", command=return_to_main).grid(row=5, column=0, columnspan=3, pady=10)
    frame.pack(pady=10)

    if curr_player == ai_player:
        tic_tac_toe_window.after(500, ai_move)

# Sudoku Functions
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def start_sudoku(predefined=None):
    hide_main_menu()
    sudoku_window = tk.Toplevel(root)
    sudoku_window.title("Sudoku Solver")
    sudoku_window.configure(bg="#A8E6CF")

    entries = []

    def solve():
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                val = entries[i][j].get()
                row.append(int(val) if val.isdigit() else 0)
            board.append(row)

        if solve_sudoku(board):
            for i in range(9):
                for j in range(9):
                    entries[i][j].delete(0, tk.END)
                    entries[i][j].insert(0, str(board[i][j]))
        else:
            messagebox.showerror("Sudoku", "No solution exists!")

    def return_to_main():
        sudoku_window.destroy()
        show_main_menu()

    for i in range(9):
        row_entries = []
        for j in range(9):
            entry = tk.Entry(sudoku_window, width=3, font=('Arial', 16, 'bold'), justify='center', bg="#FFFFFF", relief="solid", bd=1)
            entry.grid(row=i, column=j, padx=(1 if j % 3 else 3), pady=(1 if i % 3 else 3))
            row_entries.append(entry)
        entries.append(row_entries)

    if predefined:
        for i in range(9):
            for j in range(9):
                if predefined[i][j] != 0:
                    entries[i][j].insert(0, str(predefined[i][j]))

    tk.Button(sudoku_window, text="Solve", command=solve, font=('Arial', 14), bg="#FF6363", fg="white").grid(row=9, column=0, columnspan=9, pady=10)
    tk.Button(sudoku_window, text="Return to Main Menu", font=('Arial', 14), bg="gray", fg="white", command=return_to_main).grid(row=10, column=0, columnspan=9, pady=10)

def choose_sudoku_problem():
    hide_main_menu()
    problem_window = tk.Toplevel(root)
    problem_window.title("Choose Sudoku Problem")
    problem_window.configure(bg="#D0E6A5")

    problems = [
        [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ],
        [
            [0, 0, 0, 2, 6, 0, 7, 0, 1],
            [6, 8, 0, 0, 7, 0, 0, 9, 0],
            [1, 9, 0, 0, 0, 4, 5, 0, 0],
            [8, 2, 0, 1, 0, 0, 0, 4, 0],
            [0, 0, 4, 6, 0, 2, 9, 0, 0],
            [0, 5, 0, 0, 0, 3, 0, 2, 8],
            [0, 0, 9, 3, 0, 0, 0, 7, 4],
            [0, 4, 0, 0, 5, 0, 0, 3, 6],
            [7, 0, 3, 0, 1, 8, 0, 0, 0]
        ]
    ]

    def select_problem(index):
        problem_window.destroy()
        start_sudoku(predefined=problems[index])

    tk.Label(problem_window, text="Select a predefined Sudoku puzzle", font=("Arial", 16, "bold"), bg="#D0E6A5").pack(pady=10)
    for idx, _ in enumerate(problems):
        tk.Button(problem_window, text=f"Problem {idx+1}", font=("Arial", 14), bg="#3D348B", fg="white",
                  command=lambda i=idx: select_problem(i)).pack(pady=5)

# Main Menu
root = tk.Tk()
root.title("Puzzle Hub")
root.geometry("400x350")
root.configure(bg="#FFD3B6")

frame = tk.Frame(root, bg="#FFD3B6")
frame.pack(pady=20)

tk.Label(frame, text="🧩Choose a Puzzle 🎮🧩", font=("Arial", 18, "bold"), bg="#FFD3B6", fg="#3D348B").pack(pady=10)

tk.Button(frame, text="Solve Tic-Tac-Toe", font=("Arial", 14), bg="#3D348B", fg="white", width=25, command=start_tic_tac_toe).pack(pady=5)

tk.Button(frame, text="Sudoku - Blank Grid", font=("Arial", 14), bg="#3D348B", fg="white", width=25, command=start_sudoku).pack(pady=5)

tk.Button(frame, text="Sudoku - Choose Problem", font=("Arial", 14), bg="#3D348B", fg="white", width=25, command=choose_sudoku_problem).pack(pady=5)

tk.Button(frame, text="Exit", font=("Arial", 14), bg="#FF6363", fg="white", width=25, command=root.quit).pack(pady=10)

root.mainloop()
