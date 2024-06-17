import tkinter as tk

class Puissance4:
    _instance = None  # Variable de classe pour stocker l'unique instance

    @classmethod
    def get_instance(cls, root):
        if cls._instance is None:
            cls._instance = cls(root)
        return cls._instance

    def __init__(self, root):
        if Puissance4._instance is not None:
            raise Exception("Cette classe est un singleton !")
        else:
            self.root = root
            self.root.title("Connect Four")
            self.rows, self.cols = 6, 7
            self.cell_size = 100
            self.width = self.cols * self.cell_size
            self.height = self.rows * self.cell_size
            self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

            self.player = 1  # Start with the Red player (1)

            self.current_player_label = tk.Label(self.root, text="Player's turn: Red", font=('Helvetica', 14))
            self.current_player_label.pack(side="top", fill="x")

            self.frame = tk.Frame(self.root)
            self.frame.pack(expand=True)

            self.canvas = tk.Canvas(self.frame, width=self.width, height=self.height)
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
                    self.canvas.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10, fill="red")
                elif self.board[i][j] == 2:
                    self.canvas.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10, fill="yellow")

    def display_current_player(self):
        player_color = "Red" if self.player == 1 else "Yellow"
        self.current_player_label.config(text=f"Player's turn: {player_color}")

    def place_token(self, row, col, player):
        self.board[row][col] = player
        self.draw_board()
        self.change_player()

    def change_player(self):
        self.player = 2 if self.player == 1 else 1
        self.display_current_player()

    def handle_click(self, event):
        col = event.x // self.cell_size
        for row in range(self.rows-1, -1, -1):
            if self.board[row][col] == 0:
                self.place_token(row, col, self.player)
                display_row = self.rows - 1 - row  # Reverse the row for display
                move = f"{self.player_color(self.player)} : {col},{display_row}"
                self.moves_list.insert(tk.END, move)
                break

    def player_color(self, player):
        return "Red" if player == 1 else "Yellow"

    def on_resize(self, event):
        width = self.root.winfo_width()
        if width < self.width + self.moves_list.winfo_reqwidth():
            self.moves_list.pack_forget()
            self.canvas.pack(side="left", fill="both", expand=True)
        else:
            self.moves_list.pack(side="left", fill="y", expand=False)
            self.canvas.pack(side="left", fill="both", expand=True)

    def play(self, color, column):
        """ Jouer un coup dans le jeu. """
        # Logique pour jouer un coup
        # Par exemple, supposons que 'color' est 'red' ou 'yellow' et 'column' est un indice de colonne
        if color.lower() == 'red':
            player = 1
        elif color.lower() == 'yellow':
            player = 2
        else:
            raise ValueError("Invalid color. Choose 'red' or 'yellow'.")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x700")  # Set an initial size for the window
    game = Puissance4(root)
    root.mainloop()
