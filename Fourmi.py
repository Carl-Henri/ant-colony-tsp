import random
import numpy as np

class Fourmi:
    def __init__(self,civilisation, alpha, beta, start_node, Q):
        # Poids des phéromones dans le calcul des probabilités
        self.alpha = alpha
        # Poids des distances dans le calcul des probabilités
        self.beta = beta
        self.civilisation = civilisation
        self.tabou = [start_node]  # Liste taboue (villes visitées)
        self.distance_parcourue = 0
        self.ville = start_node
        self.longueur_tour = 0
        # Module la quantité de phéromones déposée par la fourmi
        self.Q = Q
    
    def choisir_prochaine_ville(self):
        """ Choisir la prochaine ville selon la probabilité P_ij """
        voisins = self.civilisation.voisins(self.ville) 
        voisins_accessibles = [value for value in voisins if value not in self.tabou]

        if not voisins_accessibles:
            return None  # Plus de villes accessibles
    
        probabilites = []
        denominateur = 0
        
        # Calcul de la probabilité pour chaque ville qu'elle soit choisie
        for j in voisins_accessibles :
            pheromone = self.civilisation.graphe[self.ville][j]["pheromone"]
            distance = self.civilisation.graphe[self.ville][j]["distance"]
            proba = (pheromone ** self.alpha) * ((1 / distance) ** self.beta) 
            denominateur += proba
            probabilites.append(proba)
        
        try:
            probabilites = [proba/denominateur for proba in probabilites]
        except: # Choix uniforme si pas de phéromones
            probabilites = [1/len(probabilites) for i in range(len(probabilites))]
        # Choix de la ville selon la distribution calculée
        prochaine_ville = random.choices(voisins_accessibles, weights=probabilites)[0]
        
        # Mise à jour de la trajectoire de la fourmi
        self.longueur_tour += self.civilisation.graphe[self.tabou[-1]][prochaine_ville]["distance"]
        self.tabou.append(prochaine_ville)
        self.ville = self.tabou[-1]
        
        return prochaine_ville

    def deposer_pheromone(self):
        for i in range(len(self.tabou)-1) :
            self.civilisation.graphe[self.tabou[i]][self.tabou[i+1]]["pheromone"] += self.Q/self.longueur_tour
        # Il faut aussi mettre à jour l'arête allant de la dernière ville visitée à la ville de départ
        # puisque la fourmi revient à la ville de départ
        self.civilisation.graphe[self.tabou[-1]][self.tabou[0]]["pheromone"] += self.Q/self.longueur_tour
    
    def vider_tabou(self) :
        start_node = np.random.choice(self.civilisation.graphe.nodes)
        self.tabou = [start_node]
        self.longueur_tour = 0