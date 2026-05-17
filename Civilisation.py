import networkx as nx
import numpy as np
from Fourmi import *
import random


class Civilisation:
    def __init__(self, graphe,nb_Fourmis, taux_evaporation = 0.5, alpha = 1, beta =2, Q =1):
        self.graphe = graphe
        self.fourmis = []
        self.taux_evaporation = taux_evaporation
        self.plus_court_trajet = []
        self.longueur_plus_court_trajet = np.inf
        self.plus_court_trajet_toute_iter = []

        self.nb_Fourmis = nb_Fourmis
        fourmis = []

        # Ville de départ aléatoire pour chaque fourmi
        for i in range(nb_Fourmis) :
            start_node = np.random.choice(self.graphe.nodes)
            fourmis.append(Fourmi(self, alpha, beta, start_node, Q))
        
        # Ajout des fourmis dans la civilisation
        for fourmi in fourmis :
            self.ajoute_fourmi(fourmi)
        
    def ajoute_fourmi(self,fourmi) :
        self.fourmis.append(fourmi)   

    def voisins(self, ville):
        return [n for n in self.graphe.neighbors(ville)]

    def evaporation_pheromone(self) :
        for (i,j) in self.graphe.edges :
            self.graphe[i][j]["pheromone"] *= (1-self.taux_evaporation)

    def tour(self) :
        n = len(self.graphe.nodes)
        for fourmi in self.fourmis :
            while len(fourmi.tabou) < n :
                fourmi.choisir_prochaine_ville()

    def rotation_equivalente(self, liste1, liste2):
        """
        Vérifie si liste2 est une rotation circulaire de liste1.
        Ex: [A, B, C, D] et [C, D, A, B] sont équivalentes.
        Vérifie également si liste2 est une rotation équivalante de liste1[::-1]
        Ex: [A, B, C, D] et [C, B, A, D] sont équivalentes.
        """
        if len(liste1) != len(liste2):
            return False
        double_liste1 = liste1 * 2  # Permet de détecter une rotation
        return any((liste2 == double_liste1[i:i+len(liste2)] or liste2[::-1] == double_liste1[i:i+len(liste2)]) for i in range(len(liste1)))

    def stagnation(self):
        """
        Vérifie si toutes les fourmis suivent la même boucle, indépendamment du point de départ.
        """
        if len(self.fourmis) == 0:
            return False  # Pas de fourmis -> pas de stagnation

        chemins = [fourmi.tabou for fourmi in self.fourmis] 
        premier_chemin = chemins[0]  # Base de comparaison

        return all(self.rotation_equivalente(premier_chemin, chemin) for chemin in chemins)
                
    
    def maj_pheromone(self) :
        self.evaporation_pheromone()
        for fourmi in self.fourmis : 
            fourmi.deposer_pheromone()
    
    def vide_tabou(self) :
        for fourmi in self.fourmis :
            fourmi.vider_tabou()

    def maj_plus_court_trajet(self) :
        pct = []
        l_min = np.inf 
        for fourmi in self.fourmis :
            if fourmi.longueur_tour < l_min :
                l_min = fourmi.longueur_tour
                pct = fourmi.tabou
        self.plus_court_trajet = pct
        if l_min < self.longueur_plus_court_trajet:
            self.plus_court_trajet_toute_iter = pct
        self.longueur_plus_court_trajet = l_min
        return(pct)
    


