# MyCanva.py
import tkinter as tk

import GameType
from MyButton import MyButton


class MyCanvas(tk.Canvas):
    board = None

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='white')
        self.current_screen = None
        self.rows = 6
        self.cols = 7
        self.cell_size = 100
        self.width = self.cols * self.cell_size
        self.height = (self.rows + 1) * self.cell_size
        self.canvas = self
        self.board = [[0] * self.cols for _ in range(self.rows)]
        self.player = 1
        self.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 1, 2]
        ]  # REALLY BOARD HERE
        self.show_menu()
        print("MyCanvas init : ", self.master.game)

    def draw_board(self):
        self.delete("all")
        for i in range(self.rows):
            for j in range(self.cols):
                x0 = j * self.cell_size
                y0 = i * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                self.create_rectangle(x0, y0, x1, y1, outline="black")
                if self.board[i][j] == 1:
                    self.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10,
                                     fill="red")
                elif self.board[i][j] == 2:
                    self.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10,
                                     fill="yellow")

        self.canvas.bind("<Button-1>", self.handle_click)

    def update_draw_board(self):
        self.draw_board()
        self.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 2, 1, 2]
        ] # REALLY NEW BOARD HERE
        self.after(500, self.update_draw_board)

    #======================= GAME =============================

    def setup_game(self):
        self.root = self.master
        self.root.title("Connect Four")
        self.restart_button = None
        self.rows, self.cols = 6, 7
        self.cell_size = 100
        self.width = self.cols * self.cell_size
        self.height = (self.rows + 1) * self.cell_size
        self.config(width=self.width, height=self.height)
        self.create_rectangle(0, 0, self.width, self.cell_size, fill="blue",
                              outline="blue")
        self.create_text(self.width / 2, self.cell_size / 2,
                         text="Current Player: Red", font=("Arial", 24),
                         fill="white")
        self.draw_board()

        self.update_draw_board()

    def handle_click(self, event):
        print("Column : ", event.x // self.cell_size)
        # NATHAN UPDATE REALLY BOARD

    # ========================== MENU ==========================

    def show_menu(self):
        self.clear()
        self.current_screen = "menu"
        self.create_text(200, 40, text="Menu Screen", font=("Arial", 24),
                         fill='black')
        MyButton(self, 200, 150, "Joueur contre Joueur", self.start_game_pvp)
        MyButton(self, 200, 190, "Joueur contre Ordinateur",
                 self.start_game_pve)
        MyButton(self, 200, 230, "Ordinateur contre Ordinateur",
                 self.start_game_ia)

    def start_game_pvp(self, event=None):
        self.clear()
        self.master.game.gameType = GameType.GameType.PVP
        print("Game Type : ", self.master.game.gameType)
        self.setup_game()
        self.master.bind('m', self.back_to_menu)

    def start_game_pve(self, event=None):
        self.clear()
        self.current_screen = "game"
        self.create_text(200, 40, text="Game Screen PVE", font=("Arial", 24))
        self.create_text(200, 200, text="Press 'm' for Menu",
                         font=("Arial", 16))
        self.master.bind('m', self.back_to_menu)

    def start_game_ia(self, event=None):
        self.clear()
        self.current_screen = "game"
        self.create_text(200, 40, text="Game Screen IA", font=("Arial", 24))
        self.create_text(200, 200, text="Press 'm' for Menu",
                         font=("Arial", 16))
        self.master.bind('m', self.back_to_menu)

    def back_to_menu(self, event=None):
        if self.current_screen == "game":
            self.show_menu()
            self.master.unbind('m')

    def place_token(self, row, col, player):
        self.board[row][col] = player
        self.draw_board()
        self.change_player()

    def change_player(self):
        self.player = 2 if self.player == 1 else 1
        self.display_current_player()

    def clear(self):
        self.delete("all")
