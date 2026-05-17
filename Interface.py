import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import networkx as nx
import random
from Fourmi import *
import math
from Civilisation import *
from Fourmi import *
import matplotlib.patches as mpatches
import tkinter.messagebox as msgbox

class ZoneAffichage(Canvas):
    def __init__(self, parent, w=500, h=400, _bg='white'):  # 500x400 : dessin final !
        self.__w = w
        self.__h = h

        # Pour avoir un contour pour le Canevas
        self.__fen_parent=parent
        Canvas.__init__(self, parent, width=w, height=h, bg=_bg, relief=RAISED, bd=5)

    def get_dims(self):
        return (self.__w, self.__h)

    def creer_noeud(self, x_centre, y_centre, rayon , col, fill_color="white"):
        noeud=Balle(self, x_centre, y_centre, rayon , col)
        return noeud

    def action_pour_un_clique(self, event):
        # Placer un noeud à l'endroit cliqué
        self.__fen_parent.placer_un_noeud(event.x, event.y)


    def placer_un_noeud_sur_canevas(self, x_centre, y_centre, col=None, fill_color="white"):
        w,h = self.get_dims()
        rayon=5
        if col == None :
            col= random.choice(['green', 'blue', 'red', 'magenta', 'black', 'maroon', 'purple', 'navy', 'dark cyan'])

        node=self.creer_noeud(x_centre, y_centre, rayon , col, fill_color)
        self.update()

        self.__fen_parent.set_coordonnes_du_last_node(x_centre, y_centre)
        return node.get_node_ident()

class FenPrincipale(Tk):
    def __init__(self):
        self.civilisation = None
        self.beta = 2       
        self.alpha = 1
        self.nb_fourmis = 50
        self.nb_iter_max = 50
        self.taux_evaporation = 0.5

        # Create the main window
        Tk.__init__(self)
        self.geometry("1000x800")
        self.title("Voyageur de commerce")

        # Set up window close event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Construction de la grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Definition de la zone de placement des noeuds
        self.__zoneAffichage = ZoneAffichage(self)
        self.__zoneAffichage.grid(column=0, row=1,padx=10, pady=10)

        # -- Création d'une barre d'outil avec divers boutons --
        BarreOutil = Frame(self, borderwidth=2, relief=GROOVE)
        BarreOutil.grid(column=0, row=0,columnspan=3)

        # Création des boutons 
        self.__boutonPlacerPoints = Button(BarreOutil, text='Positionnement', command=self.positionnement).grid(column=0, row=1, padx=10, pady=10) 
        self.__boutonQuitter = Button(BarreOutil, text='Quitter', command=self.on_closing).grid(column=0, row=2, padx=50, pady=5)
        self.__boutonBegin = Button(BarreOutil, text='Simulation', command=self.begin).grid(column=2, row=1, padx=10, pady=10)
        self.__boutonUndo = Button(BarreOutil, text='Effacer le dernier noeud', command=self.undo_last_noeud).grid(column=1, row=2, padx=5, pady=5)
        self.__boutonEffacer = Button(BarreOutil, text='Effacer', command=self.effacer).grid(column=1, row=1, padx=5, pady=5)
        self.__bouton_enregistrer = Button(BarreOutil, text="Enregistrer les paramètres", command=self.enregistrer).grid(column=2, row=2,padx=10, pady=10)         # Bouton pour enregistrer les paramètres

        # Création du champ permettant de rentrer le nombre d'itération
        self.text_nb_iter_max =Label(BarreOutil, text="Nombre max d'itération")
        self.text_nb_iter_max.grid(column=3, row=0,padx=10, pady=10)
        self.entry_nb_iter_max = Entry(BarreOutil)
        self.entry_nb_iter_max.insert(0, str(self.nb_iter_max))
        self.entry_nb_iter_max.grid(column=4, row=0,padx=10, pady=10)

        # Création du champ permettant de rentrer alpha
        self.text_alpha = Label(BarreOutil, text="alpha").grid(column=3, row=1,padx=10, pady=10)
        self.entry_alpha = Entry(BarreOutil)
        self.entry_alpha.insert(0, str(self.alpha))
        self.entry_alpha.grid(column=4, row=1,padx=10, pady=10)

        # Création du champ permettant de rentrer beta
        self.text_beta = Label(BarreOutil, text="beta").grid(column=3, row=2,padx=10, pady=10)
        self.entry_beta = Entry(BarreOutil)
        self.entry_beta.insert(0, str(self.beta))
        self.entry_beta.grid(column=4, row=2,padx=10, pady=10)

        # Création du champ permettant de rentrer le nombre de fourmis
        self.text_nb_fourmis = Label(BarreOutil, text="nombre de fourmis").grid(column=3, row=3,padx=10, pady=10)
        self.entry_nb_fourmis = Entry(BarreOutil)
        self.entry_nb_fourmis.insert(0, str(self.nb_fourmis))
        self.entry_nb_fourmis.grid(column=4, row=3,padx=10, pady=10)

        # Création du champ permettant de rentrer le taux d'évaporation
        self.text_taux_evaporation = Label(BarreOutil, text="taux d'évaporation").grid(column=3, row=4,padx=10, pady=10)
        self.entry_taux_evaporation = Entry(BarreOutil)
        self.entry_taux_evaporation.insert(0, str(self.taux_evaporation))
        self.entry_taux_evaporation.grid(column=4, row=4,padx=10, pady=10)

        self.__zoneAffichage.bind('<Button-1>', self.__zoneAffichage.action_pour_un_clique)

        self.__liste_d_ident_d_objets_crees=[]
        self.__liste_coordonnes_centre_des_nodes=[]
        
        # Create matplotlib figure and embed in Tkinter
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        # The figure isn't shown in the positionnement mode

        # Create matplotlib figure and embed in Tkinter
        self.fig1, self.ax1 = plt.subplots(figsize=(8, 6))
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self)
        self.canvas_widget1 = self.canvas1.get_tk_widget()
        self.canvas_widget1.grid(column=1, row=1,padx=10, pady=10)

    def on_closing(self):
        """Handle window close event properly"""
        # Clean up any resources
        plt.close('all')  # Close all matplotlib figures
        self.destroy()    # Destroy the Tkinter window
        import sys
        sys.exit(0)       # Exit the Python program completely

    def enregistrer(self):
        try: 
            self.nb_iter_max = float(self.entry_nb_iter_max.get())
        except:
            msgbox.showinfo("Erreur", "Valeur nb_iter_max est incorrecte\nLa valeur précédente est conservée") # Si l'utilisateur fait n'importe quoi, on ignore
        try: 
            self.alpha = float(self.entry_alpha.get())
        except:
            msgbox.showinfo("Erreur", "Valeur alpha est incorrecte\nLa valeur précédente est conservée") # Si l'utilisateur fait n'importe quoi, on ignore
        try: 
            self.beta = float(self.entry_beta.get())
        except:
            msgbox.showinfo("Erreur", "Valeur beta est incorrecte\nLa valeur précédente est conservée") # Si l'utilisateur fait n'importe quoi, on ignore
        try:
            self.nb_fourmis = int(self.entry_nb_fourmis.get())
        except:
            msgbox.showinfo("Erreur", "Valeur nombre de fourmis est incorrecte\nLa valeur précédente est conservée") # Si l'utilisateur fait n'importe quoi, on ignore
        try:
            self.taux_evaporation = float(self.entry_taux_evaporation.get())
        except:
            msgbox.showinfo("Erreur", "Valeur taux evaporation est incorrecte\nLa valeur précédente est conservée") # Si l'utilisateur fait n'importe quoi, on ignore

    def positionnement(self):
        self.canvas_widget.grid_remove()
        self.__zoneAffichage.bind('<Button-1>', self.__zoneAffichage.action_pour_un_clique)
        self.__zoneAffichage.grid(column=0, row=1,padx=10, pady=10)

    def affiche(self):
        """Cette méthode gère l'affichage du graphe"""
        # Clear previous plot
        self.ax.clear()
        
        # Get node positions
        pos = nx.get_node_attributes(self.civilisation.graphe, 'pos')

        # Draw nodes
        nx.draw_networkx_nodes(self.civilisation.graphe, pos, ax=self.ax)

        # Draw edges with distance labels
        for (u, v, data) in self.civilisation.graphe.edges(data=True):
            # Draw the edge
            self.ax.plot([pos[u][0], pos[v][0]], 
                         [pos[u][1], pos[v][1]], 
                         'gray', alpha=0.5)
            
        # Draw node labels
        nx.draw_networkx_labels(self.civilisation.graphe, pos, ax=self.ax)

        # Draw path (this iteration)     
        path_edges = list(zip(self.civilisation.plus_court_trajet, self.civilisation.plus_court_trajet[1:]))
        nx.draw_networkx_edges(self.civilisation.graphe, pos, 
                                   edgelist=path_edges, 
                                   edge_color='r', 
                                   width=2, 
                                   arrows=True,
                                   ax=self.ax)
        
        # Draw optimal path (any iteration)  
        path_edges = list(zip(self.civilisation.plus_court_trajet_toute_iter, self.civilisation.plus_court_trajet_toute_iter[1:]))
        nx.draw_networkx_edges(self.civilisation.graphe, pos, 
                                   edgelist=path_edges, 
                                   edge_color='green', 
                                   width=2, 
                                   arrows=True,
                                   ax=self.ax)

        # Set title and adjust plot
        self.ax.set_title("Graph with Real Distances")
        self.ax.set_xlabel("X coordinate")
        self.ax.set_ylabel("Y coordinate")

        # Create legend elements
        green_patch = mpatches.Patch(color='green', label='Shortest path (all iterations)')
        red_patch = mpatches.Patch(color='red', label='Shortest path (this iteration)')

        # Add legend to the plot
        self.ax.legend(handles=[green_patch, red_patch])

        # Remove axis ticks
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        # Update the canvas
        self.canvas.draw()

        # Update Tkinter window without blocking
        self.update()

    def begin(self):    
        num_nodes = len(self.__liste_coordonnes_centre_des_nodes)
        if num_nodes == 0:
            return False # Si il n'y a pas de noeuds on ne lance pas la simulation
        
        # Create a complete graph
        graphe = nx.complete_graph(num_nodes)
            
        # Generate node positions 
        positions = {}
        for (i,node) in enumerate(graphe.nodes()):
            positions[node] = self.__liste_coordonnes_centre_des_nodes[i]
            
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

        self.civilisation = Civilisation(graphe, self.nb_fourmis, self.taux_evaporation,self.alpha,self.beta)
        self.__zoneAffichage.grid_remove()
        self.__zoneAffichage.unbind('<Button-1>')
        self.canvas_widget.grid(column=0, row=1,padx=10, pady=10)

        N_iter = 0 # Compteur de cycles
        stagnation = False
        Longueur_trajet = []
        
        while N_iter <= self.nb_iter_max and not stagnation : 
                self.civilisation.tour()
                self.civilisation.maj_pheromone()
                plus_court_trajet = self.civilisation.maj_plus_court_trajet()
                stagnation = self.civilisation.stagnation()
                if stagnation: msgbox.showinfo("Stagnation", "L'algorithme stagne, il n'y pas de changement d'une itération à l'autre.\nArrêt de l'algorithme")
                self.civilisation.vide_tabou()
                Longueur_trajet.append(self.civilisation.longueur_plus_court_trajet)
                self.affiche()
                self.affiche_plus_court_trajet(N_iter, Longueur_trajet)
                N_iter +=1

    def affiche_plus_court_trajet(self, N_iter,Longueur_trajet):
        """ Cette méthode affiche la longeur du plus court trajet en fonction de l'itération"""
        # Clear previous plot
        self.ax1.clear()

        self.ax1.plot([k for k in range(N_iter+1)], Longueur_trajet)

        # Set title and adjust plot
        self.ax1.set_ylabel("Longueur du plus court chemin")
        self.ax1.set_xlabel("Itération")
        self.ax1.grid()
        
        # Update the canvas
        self.canvas1.draw()

        # Update Tkinter window without blocking
        self.update()


    def add_a_node_to_your_list(self, noeud) :
        self.__liste_d_ident_d_objets_crees.append(noeud)
        #print(self.__liste_d_ident_d_objets_crees)
        
    def placer_un_noeud(self, x, y):
        node=self.__zoneAffichage.placer_un_noeud_sur_canevas(x,y)
        self.add_a_node_to_your_list(node)
        self.set_coordonnes_du_last_node(x,y)
        self.__liste_coordonnes_centre_des_nodes.append((x,y))


    def set_coordonnes_du_last_node(self, x_centre, y_centre):
        self.__last_node=(x_centre, y_centre)

    def get_last_node(self):
        return self.__last_node


    def undo_last_noeud(self):
        print("Avant undo, liste contient {} elements".format(len(self.__liste_d_ident_d_objets_crees)))
        if len(self.__liste_d_ident_d_objets_crees)==0 :
            return # pas de noeud à enlever

        x_centre,  y_centre=self.get_last_node()

        last_node=self.__liste_d_ident_d_objets_crees.pop()

        # Pour supprimer, il faut can_id du noeud, pas le noeud lui mm !!
        self.__zoneAffichage.delete(last_node)
        self.__zoneAffichage.update()

        x_last_node,y_last_node=self.__liste_coordonnes_centre_des_nodes.pop()
        self.set_coordonnes_du_last_node(x_last_node,y_last_node)
        print("Après undo, liste contient {} elements".format(len(self.__liste_d_ident_d_objets_crees)))

        

    def ajout_noeud(self):
        # Dessin d'un petit cercle
        x_centre,  y_centre = self.not_used_generer_un_point_XY_dans_une_bande()
        print("(x,y) =", x_centre, ' , ', y_centre)

        rayon=5
        col= random.choice(['green', 'blue', 'red', 'magenta', 'black', 'maroon', 'purple', 'navy', 'dark cyan'])
        self.__zoneAffichage.creer_noeud(x_centre, y_centre, rayon , col)
        self.__zoneAffichage.update()
        self.__last_node=(x_centre, y_centre)


    def effacer(self):
        """ Efface la zone graphique """
        self.__zoneAffichage.delete(ALL)
        self.__liste_d_ident_d_objets_crees.clear()
        self.__liste_coordonnes_centre_des_nodes.clear()

#--------------------------
class Balle:
    def __init__(self, canvas, cx, cy, rayon, couleur, fill_color="white"):
        self.__cx, self.__cy = cx, cy
        self.__rayon = rayon
        self.__color = couleur
        self.__can = canvas  # Il le faut pour les déplacements

        self.__canid = self.__can.create_oval(cx - rayon, cy - rayon, cx + rayon, cy + rayon, outline=couleur, fill=fill_color)
        # Pour 3.6 : col: object  # essaie typage !

    def get_node_ident(self):
        return self.__canid
    

if __name__ == "__main__":
    fen = FenPrincipale()
    fen.mainloop()
