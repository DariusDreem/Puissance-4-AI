import pandas as pd

class Puissance4CSV:
    def __init__(self, fichier='puissance4_parties.csv'):
        self.fichier = fichier
        self.df = pd.DataFrame()
    
    def ajouter_coup(self, partie, joueur, tour, coordonnees):
        index = f"Joueur{joueur} ({tour})"
        self.df.loc[index, partie] = coordonnees
    
    def sauvegarder(self):
        self.df.to_csv(self.fichier)
    
    def charger(self):
        try:
            self.df = pd.read_csv(self.fichier, index_col=0)
        except FileNotFoundError:
            print("Fichier non trouvé. Un nouveau fichier sera créé.")

# Exemple d'utilisation
jeu = Puissance4CSV()
jeu.charger()  # Charge les données existantes si le fichier existe

jeu.ajouter_coup('Partie1', 1, 1, '(0,0)')
jeu.ajouter_coup('Partie1', 2, 1, '(0,1)')
jeu.ajouter_coup('Partie2', 1, 1, '(1,0)')

jeu.sauvegarder()