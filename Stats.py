import pandas as pd


class Puissance4CSV:
    def __init__(self):
        # Initialisation des données
        data = {
            ('Partie1','Coordonnee'): [[1,4], [1,5], [2,5]],
            ('Partie1', 'Score'): [0.001, 0.002, 0.003],
            # ('Partie1','P2', 'Coordonnée'): [[1, 5], [2, 5], [3, 5]],
            # ('Partie1','P2', 'Score'): [0.015, 0.026, 0.039]
        }
        self.df = pd.DataFrame(data)

        X = 1
        new_row = pd.DataFrame([['Winner ' + str(X), '']], columns=self.df.columns)

        self.df = pd.concat([new_row, self.df], ignore_index=True)
        # print(self.df)

        self.df.to_csv('test.csv', sep = ';')






    def ajouter_ligne(self, coord):
        # Création d'une nouvelle ligne pour les colonnes 'P1' et 'P2'
        new_row = {
            ('Partie1', 'Coordonnée'): [coord],
            # ('Partie1','Score'): [score]
        }

        # Convertir new_row en DataFrame avec les mêmes colonnes que self.df
        new_row_df = pd.DataFrame(new_row)

        # Concaténer la nouvelle ligne au DataFrame existant
        self.df = pd.concat([self.df, new_row_df], ignore_index=True)

    def afficher_dataframe(self):
        print(self.df)


# Utilisation de la classe
player_data = Puissance4CSV()
player_data.afficher_dataframe()  # Afficher le DataFrame initial

# Ajout d'une nouvelle ligne pour 'P1' et 'P2'
# player_data.ajouter_ligne([3,6])
# player_data.ajouter_ligne([3,6])
# player_data.afficher_dataframe()  # Afficher le DataFrame mis à jour
