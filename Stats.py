import os
import pandas as pd
import numpy as np

class Puissance4CSV:
    # Initialisation des variables de classe
    arrayTurn = None  # Tableau pour stocker les coups joués
    _scoreGame = None  # Tableau pour stocker les scores des parties
    _dfCSV = None  # DataFrame pour stocker les données des parties
    _fileDF = "Data/data.csv"  # Chemin du fichier CSV

    def __init__(self):
        # Initialisation des données
        # #TEST IF FILE EXIST
        
        try:
            # Lecture du fichier CSV s'il existe
           if os.path.getsize(self._fileDF) > 0:
            self._dfCSV = pd.read_csv(self._fileDF, low_memory=False, sep=';')
        except FileNotFoundError:
            # Création du répertoire et du fichier CSV s'ils n'existent pas
            os.makedirs("./Data/")
            open(self._fileDF, 'w').close()
            

    def AjouterLigne(self, coord):
        # Ajouter une nouvelle paire de coordonnées au tableau des coups joués
        nouvelle_paire = np.array([[coord[0], coord[1]]])
        if self.arrayTurn is None:
            self.arrayTurn = nouvelle_paire
        else:
            self.arrayTurn = np.vstack([self.arrayTurn, nouvelle_paire])

    def _CreateGameDF(self, newNumberOfThisGame=0, winner=1):
        # Créer un nouveau DataFrame pour une nouvelle partie
        data = {
            (f'Partie{newNumberOfThisGame}', 'Coordonnee'): [],
            (f'Partie{newNumberOfThisGame}.1', 'Score'): [],
        }
        self._dfCSV = pd.DataFrame(data)

        # Ajouter le gagnant au DataFrame
        new_row = pd.DataFrame([['Winner', str(winner)]], columns=self._dfCSV.columns)
        self._dfCSV = pd.concat([new_row, self._dfCSV], ignore_index=True)

        # Ajouter les coups joués et les scores au DataFrame
        new_row = {
            (f'Partie{newNumberOfThisGame}', 'Coordonnee'): self.arrayTurn.tolist(),
            (f'Partie{newNumberOfThisGame}.1', 'Score'): self._scoreGame.tolist()
        }
        new_row_df = pd.DataFrame(new_row)
        self._dfCSV = pd.concat([self._dfCSV, new_row_df], ignore_index=True)

    def Sauvegarder(self, winner):
        # Sauvegarder les données de la partie actuelle dans le fichier CSV
        df = pd.DataFrame()
        try:
            # Lire le fichier CSV existant
            df = pd.read_csv(self._fileDF, low_memory=False, sep=';')
            # Extraire le numéro de la dernière partie enregistrée
            numberOfLastGame = int(df.columns[-2][6:])
        except pd.errors.EmptyDataError:
            numberOfLastGame = 0

        # Initialiser les tableaux des coups pour chaque joueur
        p1Turn = np.array([self.arrayTurn[0]])
        p2Turn = np.array([self.arrayTurn[1]]) if len(self.arrayTurn) > 1 else np.array([])

        # Répartir les coups joués entre les deux joueurs
        for i in range(len(self.arrayTurn) - 2):
            row = self.arrayTurn[i + 2]
            if (i + 2) % 2 == 0:
                p1Turn = np.vstack([p1Turn, row])
            else:
                if p2Turn.size == 0:
                    p2Turn = np.array([row])
                else:
                    p2Turn = np.vstack([p2Turn, row])

        # Générer les scores pour chaque joueur en fonction du gagnant
        if winner == 1:
            scoreP1 = np.array(self.generate_geometric_parts(p1Turn.shape[0], 1))
            scoreP2 = np.array(self.generate_geometric_parts(p2Turn.shape[0], -1))
        else:
            scoreP1 = np.array(self.generate_geometric_parts(p1Turn.shape[0], -1))
            scoreP2 = np.array(self.generate_geometric_parts(p2Turn.shape[0], 1))

        # Fusionner les scores des deux joueurs
        self._scoreGame = np.empty(scoreP1.size + scoreP2.size, dtype=scoreP1.dtype)
        self._scoreGame[0::2] = scoreP1
        self._scoreGame[1::2] = scoreP2

        # Créer un nouveau DataFrame pour la nouvelle partie et l'ajouter au DataFrame existant
        self._CreateGameDF(numberOfLastGame + 1, winner)

        dfOldGame = pd.DataFrame()
        try:
            # Lire le fichier CSV existant
            dfOldGame = pd.read_csv(self._fileDF, low_memory=False, sep=';', index_col=0, header=[0, 1])
        except pd.errors.EmptyDataError:
            print("Pas de data dans csv dfOldGame!")

        # Combiner les DataFrames et les enregistrer dans le fichier CSV
        df_combined = pd.concat([dfOldGame, self._dfCSV], axis=1)
        df_combined.to_csv(self._fileDF, sep=';')

        # Réinitialiser le tableau des coups joués
        self.arrayTurn = None

    def AfficherDF(self):
        # Afficher le DataFrame actuel
        print(self._dfCSV)

    def charger(self):
        # Charger les données depuis le fichier CSV
        try:
            self._dfCSV = pd.read_csv(self._fileDF, low_memory=False, sep=';')
            return self._dfCSV
        except FileNotFoundError:
            print("Fichier non trouvé. Un nouveau fichier sera créé.")
        except pd.errors.EmptyDataError:
            print("Pas de data !")

    def generate_geometric_parts(self, num_parts, pointOfGame):  # pointOfGame est 1 si victoire, -1 si défaite
        # Générer une séquence géométrique pour les scores
        total_percentage = 100
        ratio = 1.2

        # Calculer le premier terme a
        a = (total_percentage * (ratio - 1)) / (ratio ** num_parts - 1) * pointOfGame

        # Générer les parts
        parts = [(a * (ratio ** i)) for i in range(num_parts)]

        return parts
