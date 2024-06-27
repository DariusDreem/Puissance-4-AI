import MyTk

class Connect4GUI(MyTk):
    def __init__(self):
        super().__init__()
        self.quit_button = None
        self.label = None
        print("Menu")
        self.printMenu()



    _instance = None
    menu = None

    def __init__(self):
        self.quit_button = None
        self.label = None
        print("Menu")
        self.printMenu()

    def createGameGUI(self, root):
        self.restart_button = None
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

        game_instance = Game(self)
        game_instance.finishLoadGui()
        return game_instance

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

    def show_restart_button(self):
        self.restart_button = tk.Button(self.root, text="Recommencer",
                                        command=self.restart_game)
        self.restart_button.pack(side="bottom")

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

    def display_winner(self, player):
        player_color = "rouge" if self.player == 1 else "jaune"
        self.current_player_label.config(text=f"Le gagant est {player_color}")
        if not self.restart_button:
            self.show_restart_button()

    def restart_game(self):
        print("Restarting game")

        if self.menu is None:
            print("Merde !")
            return

        self.menu.openFrame()

    # ----------------------------

    def initWindowGame(self, root):
        gui = self.createGameGUI(root)
        game = Game()
        game.setGUI(gui)
        return game

    def playpvp(self):
        print("Play PVP")

        self.hiddenFrame()



        root = tk.Tk()
        game = self.initWindowGame(root)
        game.setGameType(GameType.PVP)

        game.play(root)

    def playpve(self):
        print("Play PVE")

        root = tk.Tk()
        game = self.initWindowGame(root)
        game.setGameType(GameType.PVC)

        game.play(root)
        self.window.quit()

    def playeve(self):
        print("Play EVE")
        root = tk.Tk()
        gui = self.createGameGUI(root)
        game = Game(gui, GameType.PVC, self)
        game.setGUI(gui)
        game.play(root)

    def printMenu(self):
        self.window = tk.Tk()
        self.window.title("Menu")
        self.window.geometry("400x400")
        self.window.resizable(False, False)

        self.label = tk.Label(self.window, text="Bienvenue dans Puissance-4!",
                              font=("Helvetica", 20))
        self.label.pack(pady=20)

        self.play_button = tk.Button(self.window, text="Joueur vs Joueur",
                                     font=("arial", 15), command=self.playpvp)
        self.play_button.pack(pady=20)

        self.play_button = tk.Button(self.window, text="Joueur vs Ordinateur",
                                     font=("arial", 15), command=self.playpve)
        self.play_button.pack(pady=20)

        self.play_button = tk.Button(self.window,
                                     text="Ordinateur vs Ordinateur",
                                     font=("arial", 15), command=self.playeve)
        self.play_button.pack(pady=20)

        self.quit_button = tk.Button(self.window, text="Quitter",
                                     font=("arial", 15),
                                     command=self.window.quit)
        self.quit_button.pack(pady=20)

        self.window.mainloop()

    def hiddenFrame(self):
        self.window.withdraw()

    def openFrame(self):
        self.window.deiconify()
        self.window.mainloop()

    # Et d'autres étapes de réinitialisation si nécessaire
