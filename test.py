import matplotlib.pyplot as plt
from tkinter import *
import networkx as nx
from Fourmi import *
import math
from Civilisation import *
from Fourmi import *
import csv
from tqdm import tqdm
import pandas as pd

# Création d'un graphe complet
graphe = nx.complete_graph(30)

# Fixer une graine pour assurer la reproductibilité
np.random.seed(22)

# Génération des positions des nœuds aléatoirement dans un carré [-1, 1] x [-1, 1]
positions = {node: (np.random.uniform(-1, 1), np.random.uniform(-1, 1)) for node in graphe.nodes()}

    
# Set node positions as graph attributes
nx.set_node_attributes(graphe, positions, 'pos')
    
# Initialize distances between nodes
distances = {(i, j): math.sqrt(
    (positions[i][0] - positions[j][0])**2 + 
    (positions[i][1] - positions[j][1])**2
) * 100  # Scale up for more interesting distances
for i in graphe.nodes for j in graphe.nodes if i != j}
    
# Add distances and initial pheromone to edges
pheromone_initial = 1.0
for (i, j), distance in distances.items():
    graphe[i][j]["distance"] = round(distance, 2)
    graphe[i][j]["pheromone"] = pheromone_initial
    
# Affichage du graphe
def affiche_graphe() :
    plt.figure(figsize=(10, 10))
    nx.draw(graphe, pos=positions, with_labels=True, node_size=300, node_color="skyblue", edge_color="gray")
    plt.title("Graphe Complet à 30 Nœuds")
    plt.show()

# Le nombre de fourmis est égal au nombre de villes 
nb_fourmis = 30

# Listes des hyperparamètres à tester
l_alpha = [0, 0.5, 1, 2, 5]
l_beta = [0,1,2,5]
l_rho = [0.3,0.5,0.7,0.9,0.999]
l_Q = [1, 100, 10000]

# Nombre maximum d'itérations
nb_iter_max = 60

# Nombre de fois que l'on répète la même expérience
n = 10 #On fait une moyenne sur 10 essais


def simulation(filename):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["alpha", "beta", "rho", "q", "mean"])  # En-tête du CSV

        total_iterations = len(l_alpha) * len(l_beta) * len(l_rho) * len(l_Q) * n
        progress_bar = tqdm(total=total_iterations, desc="Simulation en cours", unit="itérations")

        for alpha in l_alpha:
            for beta in l_beta:
                for rho in l_rho:
                    for q in l_Q:
                        mean = 0
                        for i in range(n):
                            taux_evaporation = 1 - rho
                            mean += essai(taux_evaporation, alpha, beta, q)
                            progress_bar.update(1)  # Mise à jour de la barre de progression
                        mean /= n
                        print([alpha, beta, rho, q, mean])
                        writer.writerow([alpha, beta, rho, q, mean])  # Écriture immédiate dans le CSV
                        file.flush() 

        progress_bar.close()

def essai(taux_evaporation,alpha,beta,Q) :
    civilisation = Civilisation(graphe, nb_fourmis, taux_evaporation,alpha,beta,Q)
    N_iter = 0 # Compteur de cycles
    stagnation = False

    while N_iter <= nb_iter_max and not stagnation : 
            civilisation.tour()
            civilisation.maj_pheromone()
            plus_court_trajet = civilisation.maj_plus_court_trajet()
            stagnation = civilisation.stagnation()
            if stagnation: print("Stagnation")
            civilisation.vide_tabou()
            N_iter +=1
    return(civilisation.longueur_plus_court_trajet)

def visualiser_resultats() :
    # Charger les données depuis le fichier CSV
    df = pd.read_csv("resultats_simulation.csv")

    # Valeurs de référence
    alpha_ref = 1
    beta_ref = 5
    rho_ref = 0.5
    Q_ref = 100

    # Taille des polices
    font_size_title = 22
    font_size_labels = 18
    font_size_ticks = 16

    # Création de la figure avec 4 sous-graphiques
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    # Tracer la moyenne en fonction de chaque paramètre en gardant les autres fixes

    # 1. Moyenne en fonction de alpha
    df_alpha = df[(df["beta"] == beta_ref) & (df["rho"] == rho_ref) & (df["q"] == Q_ref)]
    axes[0, 0].plot(df_alpha["alpha"], df_alpha["mean"], marker="o", linestyle="-")
    axes[0, 0].set_xlabel("Alpha", fontsize=font_size_labels)
    axes[0, 0].set_ylabel("Mean", fontsize=font_size_labels)
    axes[0, 0].set_title("Moyenne en fonction de Alpha", fontsize=font_size_title)
    axes[0, 0].tick_params(axis="both", labelsize=font_size_ticks)

    # 2. Moyenne en fonction de beta
    df_beta = df[(df["alpha"] == alpha_ref) & (df["rho"] == rho_ref) & (df["q"] == Q_ref)]
    axes[0, 1].plot(df_beta["beta"], df_beta["mean"], marker="s", linestyle="-")
    axes[0, 1].set_xlabel("Beta", fontsize=font_size_labels)
    axes[0, 1].set_ylabel("Mean", fontsize=font_size_labels)
    axes[0, 1].set_title("Moyenne en fonction de Beta", fontsize=font_size_title)
    axes[0, 1].tick_params(axis="both", labelsize=font_size_ticks)

    # 3. Moyenne en fonction de rho
    df_rho = df[(df["alpha"] == alpha_ref) & (df["beta"] == beta_ref) & (df["q"] == Q_ref)]
    axes[1, 0].plot(df_rho["rho"], df_rho["mean"], marker="^", linestyle="-")
    axes[1, 0].set_xlabel("Rho", fontsize=font_size_labels)
    axes[1, 0].set_ylabel("Mean", fontsize=font_size_labels)
    axes[1, 0].set_title("Moyenne en fonction de Rho", fontsize=font_size_title)
    axes[1, 0].tick_params(axis="both", labelsize=font_size_ticks)

    # 4. Moyenne en fonction de Q
    df_Q = df[(df["alpha"] == alpha_ref) & (df["beta"] == beta_ref) & (df["rho"] == rho_ref)]
    axes[1, 1].plot(df_Q["q"], df_Q["mean"], marker="d", linestyle="-")
    axes[1, 1].set_xlabel("Q", fontsize=font_size_labels)
    axes[1, 1].set_ylabel("Mean", fontsize=font_size_labels)
    axes[1, 1].set_title("Moyenne en fonction de Q", fontsize=font_size_title)
    axes[1, 1].tick_params(axis="both", labelsize=font_size_ticks)

    # Ajustement des espacements
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Affichage
    plt.show()