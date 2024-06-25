# MyCanva.py
import tkinter as tk
from MyButton import MyButton

class MyCanvas(tk.Canvas):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='white')
        self.current_screen = None

        # Afficher le menu principal au démarrage
        self.show_menu()

    #======================= GAME =============================

    def setup_game(self):
        self.root = self.master
        self.root.title("Connect Four")
        self.rows, self.cols = 6, 7
        self.cell_size = 100
        self.width = self.cols * self.cell_size
        self.height = self.rows * self.cell_size
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        self.player = 2  # Start with the Yellow player

        self.current_player_label = tk.Label(self.root, text="Player's turn: Red", font=('Helvetica', 14))
        self.current_player_label.pack(side="top", fill="x")

        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True)

        self.canvas = tk.Canvas(self.frame, width=self.width, height=self.height)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.draw_board()

        self.moves_list = tk.Listbox(self.frame, width=20)
        self.moves_list.pack(side="right", fill="y")

        self.display_current_player()
        self.canvas.bind("<Button-1>", self.handle_click)
        self.root.bind("<Configure>", self.on_resize)

    def draw_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.create_rectangle(x1, y1, x2, y2, outline="black", fill="blue")
                self.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline="black", fill="white")














    # =========================== BUTTON ===========================

    def clear(self):
        self.delete("all")

    def show_menu(self):
        self.clear()
        self.current_screen = "menu"
        self.create_text(200, 100, text="Menu", font=("Arial", 24))

        MyButton(self, 200, 150, "Joueur contre Joueur", self.start_game_pvp)
        MyButton(self, 200, 190, "Joueur contre Ordinateur", self.start_game_pve)
        MyButton(self, 200, 230, "Ordinateur contre Ordinateur", self.start_game_ia)

    def start_game_pvp(self, event=None):
        self.clear()
        self.setup_game()
        # self.current_screen = "game"
        # self.create_text(200, 40, text="Game Screen PVP", font=("Arial", 24))
        # self.create_text(200, 200, text="Press 'm' for Menu", font=("Arial", 16))



        self.master.bind('m', self.back_to_menu)

    def start_game_pve(self, event=None):
        self.clear()
        self.current_screen = "game"
        self.create_text(200, 40, text="Game Screen PVE", font=("Arial", 24))
        self.create_text(200, 200, text="Press 'm' for Menu", font=("Arial", 16))

        self.master.bind('m', self.back_to_menu)

    def start_game_ia(self, event=None):
        self.clear()
        self.current_screen = "game"
        self.create_text(200, 40, text="Game Screen IA", font=("Arial", 24))
        self.create_text(200, 200, text="Press 'm' for Menu", font=("Arial", 16))

        self.master.bind('m', self.back_to_menu)

    def back_to_menu(self, event=None):
        if self.current_screen == "game":
            self.show_menu()
            self.master.unbind('m')


