# MyCanva.py
import tkinter as tk

import GameType
from MyButton import MyButton

class MyCanvas(tk.Canvas):
    board = None
    fontSize = 16
    textTopBoard = None
    buttonRestart = None
    clickDeosntWork = False
    trainningIA = None

    # ========================== MENU ==========================

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='white')
        self.current_screen = None
        self.rows = 6
        self.cols = 7
        self.cell_size = 100
        self.board = self.master.game.board
        self.width = 380
        self.height = 350
        self.config(width=self.width, height=self.height)

        self.canvas = self
        self.board = [[0] * self.cols for _ in range(self.rows)]
        self.player = 1
        self.show_menu()
        print("MyCanvas init : ", self.master.game)

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
        MyButton(self, 200, 270, "Entraînement  IA",
                 self.Start_training_ia)
        MyButton(self, 200, 310, "Statistiques",
                 self.Show_Stats)

    def start_game_pvp(self):
        self.clear()
        self.master.game.gameType = GameType.GameType.PVP
        print("Game Type : ", self.master.game.gameType)
        self.setup_game()

    def start_game_pve(self):
        self.clear()
        self.master.game.gameType = GameType.GameType.PVC
        print("Game Type : ", self.master.game.gameType)
        self.setup_game()
        self.master.game.SetPlayerPVC()

    def start_game_ia(self):
        self.clear()
        self.master.game.gameType = GameType.GameType.CVC
        print("Game Type : ", self.master.game.gameType)
        self.setup_game()
        self.master.game.SetPlayerCVC()

    def Start_training_ia(self):
        self.clear()
        self.trainningIA = True
        self.master.game.gameType = GameType.GameType.CVC
        print("Game Type : ", self.master.game.gameType)
        self.setup_game()
        self.master.game.SetPlayerCVC()
        self.master.game.playTurn(-1)

    def Show_Stats(self):
        # self.clear()
        self.master.game.analyze_first_moves()
        print("Show Stats Here ^^")


    def back_to_menu(self):
        if self.current_screen == "game":
            self.show_menu()
            self.master.unbind('m')

    def clear(self):
        self.delete("all")

    #======================= GAME =============================

    def setup_game(self):
        self.root = self.master
        self.root.title("Connect Four")
        self.rows, self.cols = 6, 7
        self.cell_size = 100
        self.width = (self.cols * self.cell_size) + 10
        self.height = (self.rows + 1) * self.cell_size
        self.config(width=self.width, height=self.height)
        self.draw_board()
        self.update_draw_board()

    def handle_click(self, event):
        if self.clickDeosntWork or self.master.game.gameType is GameType.GameType.CVC:
            self.master.game.playTurn(event.x // self.cell_size)
        else :
            print("Click doesn't work")
            self.clickDeosntWork = True


    def draw_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                x0 = j * self.cell_size + 5
                y0 = i * self.cell_size + 50
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
        self.delete("all")
        if not self.master.game.IsFinished:
            text = f"Joueur actuelle {self.master.game.player_turn}"
        else :
            text = f"Joueur gagnant {self.master.game.player_turn}"

        self.create_text(self.winfo_reqwidth() // 2, self.fontSize, text=text,
                         font=("Helvetica", self.fontSize), fill="black")
        self.board = self.master.game.board
        self.draw_board()
        if not self.master.game.IsFinished:
            self.after(100, self.update_draw_board)
        else:
            self.buttonRestart = tk.Button(self.root, text="Restart Game", command=self.restart_game)
            self.buttonRestart.pack()

            print("self.trainningIA : ", self.trainningIA)
            if self.trainningIA:
                print("Training IA : New game")
                self.buttonRestart.pack_forget()
                self.master.game.ResetBoardGame()
                self.Start_training_ia()
                

    def restart_game(self):
        self.buttonRestart.pack_forget()
        self.master.game.ResetBoardGame()
        self.show_menu()
        self.width = 230
        self.height = 500
        self.clickDeosntWork = False

