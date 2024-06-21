import tkinter as tk

from Game import Game


class Connect4GUI:
    _instance = None

    def __new__(cls, arg):
        if cls._instance is None:
            cls._instance = super(Connect4GUI, cls).__new__(cls)
        return cls._instance

    def __init__(self, root):
        self.root = root
        self.root.title("Connect Four")
        self.rows, self.cols = 6, 7
        self.cell_size = 100
        self.width = self.cols * self.cell_size
        self.height = self.rows * self.cell_size
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        self.player = 2  # Start with the Yellow player 1

        self.current_player_label = tk.Label(self.root,
                                             text="Player's turn: Red",
                                             font=('Helvetica', 14))
        self.current_player_label.pack(side="top", fill="x")

        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True)

        self.canvas = tk.Canvas(self.frame, width=self.width,
                                height=self.height)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.draw_board()

        self.moves_list = tk.Listbox(self.frame, width=20)

        self.display_current_player()
        self.canvas.bind("<Button-1>", self.handle_click)
        self.root.bind("<Configure>", self.on_resize)

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(self.rows):  # Ensure to draw the bottom row
            for j in range(self.cols):
                x0 = j * self.cell_size
                y0 = i * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black")
                if self.board[i][j] == 1:
                    self.canvas.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10,
                                            fill="red")
                elif self.board[i][j] == 2:
                    self.canvas.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10,
                                            fill="yellow")

    def display_current_player(self):
        player_color = "rouge" if self.player == 2 else "jaune"
        self.current_player_label.config(text=f"Au tour de : {player_color}")

    def place_token(self, row, col, player):
        self.board[row][col] = player
        self.draw_board()
        self.change_player()

    def change_player(self):
        self.player = 2 if self.player == 1 else 1
        self.display_current_player()

    def handle_click(self, event):
        print("Click : ", event.x // self.cell_size)
        game_instance = Game()
        
        game_instance.playTurn(event.x // self.cell_size)
        # playTurn(event.x // self.cell_size)
        return event.x // self.cell_size


    def on_resize(self, event):
        width = self.root.winfo_width()
        if width < self.width + self.moves_list.winfo_reqwidth():
            self.moves_list.pack_forget()
            self.canvas.pack(side="left", fill="both", expand=True)
        else:
            self.moves_list.pack(side="left", fill="y", expand=False)
            self.canvas.pack(side="left", fill="both", expand=True)

    def displaywinner(self, event):
        width = self.root.winfo_width()
        if width < self.width + self.moves_list.winfo_reqwidth():
            self.moves_list.pack_forget()
            self.canvas.pack(side="left", fill="both", expand=True)
        else:
            self.moves_list.pack(side="left", fill="y", expand=False)
            self.canvas.pack(side="left", fill="both", expand=True)