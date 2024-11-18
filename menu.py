import tkinter as tk
from tkinter import ttk
from fanorona_telo import Game3x3

class FanoronaGameMenu:
    def __init__(self, root):
        self.root = root
        self.current_frame = None
        self.selected_game = None
        self.setup_main_menu()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def setup_main_menu(self):
        self.clear_frame()
        self.main_menu_frame = tk.Frame(self.root)
        self.main_menu_frame.pack(expand=True, fill=tk.BOTH)

        title_label = tk.Label(self.main_menu_frame, text="Fanorona Game", font=("Helvetica", 24))
        title_label.pack(pady=20)

        tk.Button(self.main_menu_frame, text="Jouer", command=lambda: self.setup_configuration("Fanorona 3x3")).pack(pady=10)

        self.current_frame = self.main_menu_frame

    def setup_configuration(self, game_name):
        self.selected_game = game_name
        self.clear_frame()
        
        self.configuration_frame = tk.Frame(self.root)
        self.configuration_frame.pack(expand=True, fill=tk.BOTH)

        self.button_frame = tk.Frame(self.configuration_frame)
        self.button_frame.pack(side="top", fill="x", pady=10)

        self.back_button = tk.Button(self.button_frame, text="Retour", command=self.setup_main_menu)
        self.back_button.pack(side="left", padx=10)
        
        title_label = tk.Label(self.configuration_frame, text="Configuration", font=("Helvetica", 24))
        title_label.pack(pady=20)

        # Configuration joueur 1
        player1_frame = tk.Frame(self.configuration_frame)
        player1_frame.pack(pady=10)
        tk.Label(player1_frame, text="Player 1:").pack(side=tk.LEFT)
        self.player1_name_entry = tk.Entry(player1_frame)
        self.player1_name_entry.insert(0, "joueur_1")
        self.player1_name_entry.pack(side=tk.LEFT, padx=10)
        self.player1_color_combobox = ttk.Combobox(player1_frame, values=["Red", "Blue", "Green", "Yellow"])
        self.player1_color_combobox.current(0)
        self.player1_color_combobox.pack(side=tk.LEFT)

        # Configuration joueur 2
        player2_frame = tk.Frame(self.configuration_frame)
        player2_frame.pack(pady=10)
        tk.Label(player2_frame, text="Player 2:").pack(side=tk.LEFT)
        self.player2_name_entry = tk.Entry(player2_frame)
        self.player2_name_entry.insert(0, "joueur_2")
        self.player2_name_entry.pack(side=tk.LEFT, padx=10)
        self.player2_color_combobox = ttk.Combobox(player2_frame, values=["Red", "Blue", "Green", "Yellow"])
        self.player2_color_combobox.current(1)
        self.player2_color_combobox.pack(side=tk.LEFT)

        # Configuration rounds
        rounds_frame = tk.Frame(self.configuration_frame)
        rounds_frame.pack(pady=10)
        tk.Label(rounds_frame, text="Rounds:").pack(side=tk.LEFT)
        self.rounds_var = tk.IntVar(value=1)
        tk.Button(rounds_frame, text="-", command=self.decrease_rounds).pack(side=tk.LEFT, padx=5)
        tk.Label(rounds_frame, textvariable=self.rounds_var).pack(side=tk.LEFT)
        tk.Button(rounds_frame, text="+", command=self.increase_rounds).pack(side=tk.LEFT, padx=5)

        tk.Button(self.configuration_frame, text="Start Game", command=self.start_game).pack(pady=20)

        self.current_frame = self.configuration_frame

    def decrease_rounds(self):
        if self.rounds_var.get() > 1:
            self.rounds_var.set(self.rounds_var.get() - 1)

    def increase_rounds(self):
        self.rounds_var.set(self.rounds_var.get() + 1)

    def start_game(self):
        # Extraction valeur de configuration
        player1_name = self.player1_name_entry.get()
        player1_color = self.player1_color_combobox.get()
        player2_name = self.player2_name_entry.get()
        player2_color = self.player2_color_combobox.get()
        num_rounds = self.rounds_var.get()
        
        self.clear_frame()
        
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(expand=True, fill=tk.BOTH)


        # Initialisation jeux
        Game3x3(self.root, player1_name, player2_name, player1_color, player2_color, num_rounds, self.setup_main_menu, self.game_frame)

