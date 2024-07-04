import os

import pandas as pd
import numpy as np


class Puissance4CSV:
    # create a list numpy array
    arrayTurn = None
    _scoreGame = None
    _dfCSV = None
    _fileDF = "Data/data.csv"

    def __init__(self):
        # Initialisation des données
        print("Initialisation des données")
        # #TEST IF FILE EXIST
        try:
            self._dfCSV = pd.read_csv(self._fileDF, low_memory=False ,sep=';')
        except FileNotFoundError:
            os.makedirs("./Data/")
            open(self._fileDF, 'w').close()
            print("Fichier non trouvé. Un nouveau fichier sera créé.")
            
            print("Pas de data dans csv dfOldGame!")

    def AjouterLigne(self, coord):
        nouvelle_paire = np.array([[coord[0], coord[1]]])
        print("Nouvelle paire : ", nouvelle_paire)
        if self.arrayTurn is None:
            self.arrayTurn = nouvelle_paire
        else:
            self.arrayTurn = np.vstack([self.arrayTurn, nouvelle_paire])

    def _CreateGameDF(self, newNumberOfThisGame=0,winner=1):
        data = {
            (f'Partie{newNumberOfThisGame}', 'Coordonnee'): [],
            (f'Partie{newNumberOfThisGame}.1', 'Score'): [],
        }
        self._dfCSV = pd.DataFrame(data)

        new_row = pd.DataFrame([['Winner', str(winner)]], columns=self._dfCSV.columns)

        self._dfCSV = pd.concat([new_row, self._dfCSV], ignore_index=True)

        new_row = {
            (f'Partie{newNumberOfThisGame}', 'Coordonnee'): self.arrayTurn.tolist(),
            (f'Partie{newNumberOfThisGame}.1', 'Score'): self._scoreGame.tolist()
        }
        new_row_df = pd.DataFrame(new_row)
        self._dfCSV = pd.concat([self._dfCSV, new_row_df], ignore_index=True)

    def Sauvegarder(self, winner):
        df = pd.DataFrame()
        try:
            df = pd.read_csv(self._fileDF, low_memory=False ,sep=';')
            numberOfLastGame = int(df.columns[-2][6:]) # get penultimate column name and extract the number
        except pd.errors.EmptyDataError:
            numberOfLastGame = 0

        print("self arrayTurn : ", self.arrayTurn)

        p1Turn = np.array([self.arrayTurn[0]])
        p2Turn = np.array([self.arrayTurn[1]]) if len(self.arrayTurn) > 1 else np.array([])

        for i in range(len(self.arrayTurn) - 2):
            row = self.arrayTurn[i + 2]
            if (i + 2) % 2 == 0:
                p1Turn = np.vstack([p1Turn, row])
            else:
                if p2Turn.size == 0:
                    p2Turn = np.array([row])
                else:
                    p2Turn = np.vstack([p2Turn, row])

        if winner == 1:
            scoreP1 = np.array(self.generate_geometric_parts(p1Turn.shape[0], 1))
            scoreP2 = np.array(self.generate_geometric_parts(p2Turn.shape[0], -1))
        else:
            scoreP1 = np.array(self.generate_geometric_parts(p1Turn.shape[0], -1))
            scoreP2 = np.array(self.generate_geometric_parts(p2Turn.shape[0], 1))

        self._scoreGame = np.empty(scoreP1.size + scoreP2.size, dtype=scoreP1.dtype)
        self._scoreGame[0::2] = scoreP1
        self._scoreGame[1::2] = scoreP2

        self._CreateGameDF(numberOfLastGame + 1, winner)

        dfOldGame = pd.DataFrame()

        try:
            dfOldGame = pd.read_csv(self._fileDF, low_memory=False, sep=';', index_col=0, header=[0, 1])
        except pd.errors.EmptyDataError:
            print("Pas de data dans csv dfOldGame!")

        print(self._dfCSV)
        print("========")
        print(dfOldGame)
        df_combined = pd.concat([dfOldGame, self._dfCSV], axis=1)
        print(df_combined)
        df_combined.to_csv(self._fileDF, sep=';')
        self.arrayTurn = None

    def AfficherDF(self):
        print(self._dfCSV)

    def charger(self):
        try:
            self._dfCSV = pd.read_csv(self._fileDF,low_memory=False , sep=';')
            return self._dfCSV
        except FileNotFoundError:
            print("Fichier non trouvé. Un nouveau fichier sera créé.")
        except pd.errors.EmptyDataError:
            print("Pas de data !")


    def generate_geometric_parts(self,num_parts, pointOfGame): # pointOfGame is 1 if win -1 if lose
        total_percentage = 100
        # num_parts = 5
        ratio = 1.2

        # Calculer le premier terme a
        a = (total_percentage * (ratio - 1)) / (ratio ** num_parts - 1) * pointOfGame

        # Générer les parts
        parts = [(a * (ratio ** i)) for i in range(num_parts)]

        return parts

# player_data.AjouterLigne([1, 4])
# player_data.AjouterLigne([2, 4])
# player_data.AjouterLigne([3, 5])
# player_data.AjouterLigne([3, 4])
# player_data.AjouterLigne([3, 2])
# player_data.AjouterLigne([1, 2])
# player_data.AjouterLigne([0, 2])

# player_data.Sauvegarder(1)