import pandas as pd # type: ignore

class Puissance4CSV:
    def __init__(self, fichier='./Data/puissance4_parties.csv'):
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



    def generate_geometric_parts(total_percentage, num_parts, ratio):
        # Calculer le premier terme a
        a = (total_percentage * (ratio - 1)) / (ratio ** num_parts - 1)
        
        # Générer les parts
        parts = [a * (ratio ** i) for i in range(num_parts)]
        
        return parts

    # Exemple d'utilisation
    total_percentage = 100
    num_parts = 5
    ratio = 1.5

    parts = generate_geometric_parts(total_percentage, num_parts, ratio)
    print("Les parts sont :", parts)
    print("La somme des parts est :", sum(parts))
