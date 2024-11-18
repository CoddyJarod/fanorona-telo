import tkinter as tk
from tkinter import messagebox

class Game3x3:
    def __init__(self, master, player1_name, player2_name, player1_color, player2_color, num_rounds, menu_frame, game_frame):
        # Initialisation des paramètres du jeu
        self.master = master  # La fenêtre principale de l'application
        self.player1_name = player1_name  # Nom du joueur 1
        self.player2_name = player2_name  # Nom du joueur 2
        self.player1_color = player1_color  # Couleur du joueur 1
        self.player2_color = player2_color  # Couleur du joueur 2
        self.num_rounds = num_rounds  # Nombre de manches à jouer
        self.current_round = 1  # Manche actuelle
        self.scores = {player1_name: 0, player2_name: 0}  # Scores des joueurs

        self.menu_frame = menu_frame  # Cadre pour le menu principal
        self.game_frame = game_frame  # Cadre pour le jeu

        self.master.title("Fanorona 3x3")  # Titre de la fenêtre

        # Frame pour les boutons
        self.button_frame = tk.Frame(self.game_frame)
        self.button_frame.pack(side="top", fill="x", pady=10)

        # Bouton pour quitter le jeu
        self.back_button = tk.Button(self.button_frame, text="Quitter", command=self.confirm_exit)
        self.back_button.pack(side="left", padx=10)

        # Bouton pour redémarrer le jeu
        self.restart_button = tk.Button(self.button_frame, text="Restart Game", command=self.reset_game)
        self.restart_button.pack(side="right", padx=10)

        # Canvas pour dessiner le plateau de jeu
        self.canvas = tk.Canvas(self.game_frame, width=300, height=300)
        self.canvas.pack(pady=20)

        # Frame pour afficher les scores
        self.score_frame = tk.Frame(self.game_frame)
        self.score_frame.pack(pady=20)

        self.setup_scoreboard()  # Configuration du tableau de scores
        self.setup_board()  # Configuration du plateau de jeu

        # Positions initiales des boules pour chaque joueur
        self.positions = {
            player1_name: [(2, 0), (2, 1), (2, 2)],
            player2_name: [(0, 0), (0, 1), (0, 2)]
        }

        # Sauvegarde des positions originales pour réinitialiser le jeu
        self.original_positions = {k: list(v) for k, v in self.positions.items()}

        # Compte des mouvements pour chaque boule
        self.moves_count = {player1_name: {pos: 0 for pos in self.positions[player1_name]},
                            player2_name: {pos: 0 for pos in self.positions[player2_name]}}

        self.turn = player1_name  # Tour du joueur actuel
        self.selected_boule = None  # Boule sélectionnée par le joueur
        self.draw_boules()  # Dessine les boules sur le plateau
        self.draw_highlight()  # Dessine le surlignement sur la boule sélectionnée

        # Liaison de l'événement de clic sur le canevas
        self.canvas.bind("<Button-1>", self.click_handler)

    def setup_scoreboard(self):
        # Configuration du tableau des scores
        self.score_label = tk.Label(self.score_frame, text=f"Round {self.current_round} of {self.num_rounds}", font=("Arial", 16))
        self.score_label.pack()

        # Affichage du score du joueur 1
        self.player1_label = tk.Label(self.score_frame, text=f"{self.player1_name}: {self.scores[self.player1_name]} points", fg=self.player1_color, font=("Arial", 14))
        self.player1_label.pack(side="left", padx=20)

        # Affichage du score du joueur 2
        self.player2_label = tk.Label(self.score_frame, text=f"{self.player2_name}: {self.scores[self.player2_name]} points", fg=self.player2_color, font=("Arial", 14))
        self.player2_label.pack(side="right", padx=20)

    def update_scoreboard(self):
        # Mise à jour du tableau des scores
        self.score_label.config(text=f"Round {self.current_round} of {self.num_rounds}")
        self.player1_label.config(text=f"{self.player1_name}: {self.scores[self.player1_name]} points")
        self.player2_label.config(text=f"{self.player2_name}: {self.scores[self.player2_name]} points")

    def setup_board(self):
        # Configuration du plateau de jeu
        self.draw_movement_lines()  # Dessine les lignes de mouvement sur le plateau

    def draw_movement_lines(self):
        # Dessine les lignes de mouvement sur le canevas
        self.canvas.create_line(50, 50, 50, 250, fill="green", dash=(4, 2))
        self.canvas.create_line(150, 50, 150, 250, fill="green", dash=(4, 2))
        self.canvas.create_line(250, 50, 250, 250, fill="green", dash=(4, 2))
        self.canvas.create_line(50, 50, 250, 50, fill="green", dash=(4, 2))
        self.canvas.create_line(50, 150, 250, 150, fill="green", dash=(4, 2))
        self.canvas.create_line(50, 250, 250, 250, fill="green", dash=(4, 2))
        self.canvas.create_line(50, 50, 250, 250, fill="green", dash=(4, 2))
        self.canvas.create_line(50, 250, 250, 50, fill="green", dash=(4, 2))

    def draw_boules(self):
        # Dessine les boules sur le plateau pour chaque joueur
        self.canvas.delete("boule")  # Supprime les anciennes boules
        for player in self.positions:
            color = self.player1_color if player == self.player1_name else self.player2_color
            for pos in self.positions[player]:
                x, y = pos[1] * 100 + 50, pos[0] * 100 + 50 # Calcul des coordonnées pour le dessin
                self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color, outline="black", tags="boule")
    
    def draw_highlight(self):
        # Dessine un surlignement autour des boules du joueur dont c'est le tour
        self.canvas.delete("highlight")  # Supprime les anciens surlignements
        for pos in self.positions[self.turn]:
            x, y = pos[1] * 100 + 50, pos[0] * 100 + 50
            self.canvas.create_oval(x-25, y-25, x+25, y+25, outline="white", width=2, tags="highlight")
        if self.selected_boule:
            x, y = self.selected_boule[1] * 100 + 50, self.selected_boule[0] * 100 + 50
            self.canvas.create_oval(x-25, y-25, x+25, y+25, outline="green", width=2, tags="highlight")

    def click_handler(self, event):
        # Gestion du clic sur le plateau de jeu
        row, col = event.y // 100, event.x // 100  # Convertit les coordonnées du clic en indices de ligne et de colonne
        clicked_pos = (row, col)  # Position cliquée

        if self.selected_boule is None:
            # Si aucune boule n'est sélectionnée, sélectionner la boule cliquée
            if clicked_pos in self.positions[self.turn]:
                self.selected_boule = clicked_pos
                self.draw_highlight() # Mettre à jour l'affichage du surlignement
            else:
                messagebox.showerror("Erreur", "Veuillez cliquer sur une boule de votre propre joueur.")
        else:
            # Si une boule est déjà sélectionnée, gérer le mouvement
            if self.is_valid_move(self.selected_boule, clicked_pos) or clicked_pos in self.positions[self.turn]:
                # Si le joueur clique sur sa propre boule
                if clicked_pos in self.positions[self.turn]:
                    self.selected_boule = clicked_pos
                    self.draw_highlight()
                else:
                    # Effectuer le mouvement
                    self.move_boule(self.selected_boule, clicked_pos)
                    # Vérifier si le joueur a gagné
                    if self.check_winner(self.turn):
                        self.scores[self.turn] += 1 # Augmenter le score du joueur
                        messagebox.showinfo("Victoire", f"{self.turn} a gagné cette manche!")
                        if self.current_round < self.num_rounds:
                            self.current_round += 1 # Passer à la manche suivante
                            self.reset_board() # Réinitialiser le plateau
                        else:
                            self.end_game() # Terminer le jeu si toutes les manches sont jouées
                    else:
                        # Passer le tour au joueur suivant
                        self.turn = self.player1_name if self.turn == self.player2_name else self.player2_name
                    self.selected_boule = None # Réinitialiser la boule sélectionnée
                    self.draw_highlight() # Mettre à jour l'affichage du surlignement
            else:
                messagebox.showerror("Erreur", "Déplacement non valide.")
                self.selected_boule = None
                self.draw_highlight()

    def move_boule(self, from_pos, to_pos):
        player = self.turn
        self.positions[player].remove(from_pos)
        self.positions[player].append(to_pos)
        self.moves_count[player][from_pos] += 1
        self.moves_count[player][to_pos] = self.moves_count[player].pop(from_pos)
        self.draw_boules()

    def is_valid_move(self, from_pos, to_pos):
        # Vérifie si un mouvement est valide
        return to_pos in self.get_valid_moves_from(from_pos)

    def get_valid_moves_from(self, pos):
        valid_moves = set()
        row, col = pos

        # Mouvement vertical
        if col == 0 and (row, col + 1) not in self.positions[self.player1_name] and (row, col + 1) not in self.positions[self.player2_name]:
            valid_moves.add((row, col + 1))
        elif col == 1:
            if (row, col - 1) not in self.positions[self.player1_name] and (row, col - 1) not in self.positions[self.player2_name]:
                valid_moves.add((row, col - 1))
            if (row, col + 1) not in self.positions[self.player1_name] and (row, col + 1) not in self.positions[self.player2_name]:
                valid_moves.add((row, col + 1))
        elif col == 2 and (row, col - 1) not in self.positions[self.player1_name] and (row, col - 1) not in self.positions[self.player2_name]:
            valid_moves.add((row, col - 1))

        # Mouvement horizontal
        if row == 0 and (row + 1, col) not in self.positions[self.player1_name] and (row + 1, col) not in self.positions[self.player2_name]:
            valid_moves.add((row + 1, col))
        elif row == 1:
            if (row - 1, col) not in self.positions[self.player1_name] and (row - 1, col) not in self.positions[self.player2_name]:
                valid_moves.add((row - 1, col))
            if (row + 1, col) not in self.positions[self.player1_name] and (row + 1, col) not in self.positions[self.player2_name]:
                valid_moves.add((row + 1, col))
        elif row == 2 and (row - 1, col) not in self.positions[self.player1_name] and (row - 1, col) not in self.positions[self.player2_name]:
            valid_moves.add((row - 1, col))

        if row == col:  # Haut-gauche diagonale
            if row > 0 and (row - 1, col - 1) not in self.positions[self.player1_name] and (row - 1, col - 1) not in self.positions[self.player2_name]:
                valid_moves.add((row - 1, col - 1))
            if row < 2 and (row + 1, col + 1) not in self.positions[self.player1_name] and (row + 1, col + 1) not in self.positions[self.player2_name]:
                valid_moves.add((row + 1, col + 1))
                
        if row + col == 2:  # Bas-gauche diagonale
            if row > 0 and (row - 1, col + 1) not in self.positions[self.player1_name] and (row - 1, col + 1) not in self.positions[self.player2_name]:
                valid_moves.add((row - 1, col + 1))
            if row < 2 and (row + 1, col - 1) not in self.positions[self.player1_name] and (row + 1, col - 1) not in self.positions[self.player2_name]:
                valid_moves.add((row + 1, col - 1))

        return valid_moves

    def check_winner(self, player):
        # Vérifie si le joueur a gagné
        for line in self.get_lines():  # Obtenir les lignes de vérification
            if all(pos in self.positions[player] for pos in line) and \
                    all(self.moves_count[player][pos] > 0 for pos in line):  # Vérifier si toutes les boules ont été déplacées
                return True
        return False
    
    def get_lines(self):
        # Retourne les lignes de vérification pour les conditions de victoire
        return [
            [(0, 0), (0, 1), (0, 2)],  # Ligne 1
            [(1, 0), (1, 1), (1, 2)],  # Ligne 2
            [(2, 0), (2, 1), (2, 2)],  # Ligne 3
            [(0, 0), (1, 0), (2, 0)],  # Colonne 1
            [(0, 1), (1, 1), (2, 1)],  # Colonne 2
            [(0, 2), (1, 2), (2, 2)],  # Colonne 3
            [(0, 0), (1, 1), (2, 2)],  # Diagonale \
            [(0, 2), (1, 1), (2, 0)],  # Diagonale /
        ]

    def reset_game(self):
        # Réinitialise le jeu pour une nouvelle partie
        self.current_round = 1 # Réinitialiser la manche actuelle
        self.scores = {self.player1_name: 0, self.player2_name: 0} # Réinitialiser les scores
        self.reset_board() # Réinitialiser le plateau de jeu

    def reset_board(self):
        # Réinitialise le plateau de jeu
        self.positions = {k: list(v) for k, v in self.original_positions.items()} # Restaurer les positions originales
        self.moves_count = {player: {pos: 0 for pos in positions} for player, positions in self.positions.items()} # Réinitialiser les compteurs de mouvement
        self.turn = self.player1_name # Redémarrer avec le joueur 1
        self.selected_boule = None  # Réinitialiser la sélection
        self.draw_boules()  # Redessiner les boules
        self.update_scoreboard()  # Réinitialiser score
        self.draw_highlight()  # Réafficher le surlignement

        
    def end_game(self):
        # Terminer le jeu et afficher le score final
        winner = max(self.scores, key=self.scores.get)
        messagebox.showinfo("Fin de jeu", f"{winner} a gagné la partie avec {self.scores[winner]} points!")
        self.reset_game()

    def confirm_exit(self):
        # Confirmation avant de quitter le jeu
        if messagebox.askyesno("Confirmation de quitter", "Etes-vous sûre de retourner au menu?"):
            self.show_menu()

    def show_menu(self):
        self.game_frame.destroy()
        self.menu_frame()
