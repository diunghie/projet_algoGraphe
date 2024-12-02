import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import networkx as nx

class DynamicGraph: # une classe DynamicGraph est définie pour représenter un graphe dynamique
    def __init__(self): # Ce graphe a des attributs suivants pour stocker les informations sur le graphe:  
        self.vertices = {} # vertices (un dictionnaire)
        self.edges = set() # edges (un ensemble)
        self.colors = {} # et colors (un dictionnaire)
        self.edges_added = set()  # Ajouter cette ligne pour initialiser l'attribut edges_added
        
    def add_vertex(self, vertex): # Cette méthode ajoute un sommet 'vertex' au graphe
        if vertex not in self.vertices: # vérifie si le sommet 'vertex' n'est pas déjà dans le graphe
            self.vertices[vertex] = set() # ajoute le sommet 'vertex' au dictionnaire 'vertices'
            self.colors[vertex] = None # initialise la couleur du sommet 'vertex' à None
            
    def add_edge(self, edge): # Cette méthode ajoute une arête au graphe        
        self.edges.add(frozenset(edge)) # ajoute une arête au graphe sous forme d'un frozenset pour garantir l'immutabilité et l'unicité des arêtes
        for vertex in edge: # parcourt chaque sommet dans l'arête ce qui est représentée par une paire non ordonnée de sommets
            self.vertices[vertex].add(frozenset(edge)) # ajoute 'edge' à 'vertices'. Pour ∀ sommet de 'edge', ajoute l'arête auquel ce sommet appartient

    def edge_exists(self, edge):
        edge = frozenset(edge)
        return edge in self.edges


    def color_graph(self): # Cette méthode colorie l'ensemble du graphe de manière cohérente
        m = len(self.vertices) # calcule le nombre total de sommets dans le graphe
        for vertex in self.vertices: # parcourt tous les sommets du graph
            if self.colors[vertex] is None: # vérifie si le sommet actuel (vertex) n'a pas encore de couleur attribuée
                self.color_connected_component(vertex) # colore la CC contenant 'vertex' et met à jour les couleurs des sommets dans cette CC

    """
    Cette méthode 'color_connected_component' explore la composante connectée (CC) du sommet initial, attribuant des couleurs cohérentes aux sommets 
    en évitant les couleurs déjà utilisées par les voisins
    """
    def color_connected_component(self, start_vertex):
        queue = deque([start_vertex]) # Crée une deque 'queue' avec le sommet initial comme élément unique pour parcourir les sommets de la CC
        used_colors = set() # Initialise un ensemble vide 'used_colors' pour suivre les couleurs déjà utilisées dans la CC

        while queue: # boucle qui continue tant que la file d'attente n'est pas vide (càd qu'il reste des sommets à explorer dans la CC)
            current_vertex = queue.popleft() # Retire et récupère 1e sommet de 'queue'. Il est actuellement examiné dans le processus de coloration
            available_colors = set(range(1, len(self.vertices) + 1)) # Initialise un ensemble de couleurs disponibles (de 1 au nombre total de sommets)

            for edge in self.vertices[current_vertex]: # Parcourt toutes les arêtes (edges) associées au sommet actuel dans le dictionnaire vertices
                adjacent_vertex = next(iter(set(edge) - {current_vertex})) # Détermine le sommet adjacent au sommet actuel via l'arête en cours d'examen

                if adjacent_vertex in self.colors and self.colors[adjacent_vertex] is not None: # Vérifie si le sommet adj a déjà 1 couleur attribuée
                    available_colors.discard(self.colors[adjacent_vertex]) # cette couleur est retirée de l'ensemble des couleurs disponibles

            if available_colors: # Vérifie si des couleurs sont disponibles après avoir examiné les voisins
                # Modification pour s'assurer que la couleur du sommet associée à la nouvelle arête est différente
                if current_vertex in self.edges_added: # Vérifie si le sommet actuel est associé à une nouvelle arête ajoutée
                    available_colors.discard(self.colors[current_vertex]) # Supprime la couleur du sommet actuel de l'ensemble des couleurs disponibles

                color = min(available_colors) # choisit la plus petite couleur disponible
                self.colors[current_vertex] = color # Attribue cette couleur au sommet actuel dans le dictionnaire 'colors'
                used_colors.add(color) # Ajoute la couleur utilisée à l'ensemble des couleurs déjà utilisées 'used_colors'

                for edge in self.vertices[current_vertex]: # Parcourt à nouveau les arêtes associées au sommet actuel
                    adjacent_vertex = next(iter(set(edge) - {current_vertex})) # Détermine à nouveau le sommet adjacent à partir de l'arête

                    # Vérifie si le sommet adj n'a pas encore de couleur attribuée
                    if adjacent_vertex in self.colors and self.colors[adjacent_vertex] is None: 
                        queue.append(adjacent_vertex) # Ajoute le sommet adjacent à la file d'attente pour le traiter ultérieurement

                if self.edges_added: # Vérifie si de nouvelles arêtes ont été ajoutées au graphe
                    for vertex in self.edges_added: # Itère sur les sommets associés aux arêtes nouvellement ajoutées
                        # Vérifie si le sommet n'est pas le sommet actuel et n'a pas encore été ajouté à 'deque'
                        if vertex != current_vertex and vertex not in queue: 
                            queue.append(vertex) # ajoute le sommet à la file pour un traitement ultérieur

            else: # Si aucune couleur n'est disponible pour le sommet actuel
                new_color = max(used_colors) + 1 # Trouve la couleur maximale utilisée et l'incrémente pour obtenir une nouvelle couleur
                self.colors[current_vertex] = new_color # Attribue la nouvelle couleur au sommet actuel
                used_colors.add(new_color) # Ajoute la nouvelle couleur à l'ensemble des couleurs utilisées

                for edge in self.vertices[current_vertex]: #  Itère sur les arêtes du sommet actuel
                    adjacent_vertex = next(iter(set(edge) - {current_vertex})) # Détermine le sommet adjacent au sommet actuel dans l'arête actuelle

                    # Vérifie si le sommet adjacent n'a pas encore été attribué une couleur
                    if adjacent_vertex in self.colors and self.colors[adjacent_vertex] is None:
                        queue.append(adjacent_vertex) # ajoute le sommet adjacent à la file pour un traitement ultérieur

        self.edges_added = set()  # Réinitialise l'ensemble des arêtes ajoutées après le traitement de la composante connectée
        self.chromatic_number() # Met à jour le nombre chromatique après que la composante connectée a été colorée

    """ 
    Cette méthode met à jour les couleurs du graphe après une modification. Elle prend en charge deux paramètres optionnels : modified_vertex 
    et modified_edge. Ces paramètres indiquent quel sommet ou quelle arête a été modifié. 
    """
    def update_graph_after_modification(self, modified_vertex=None, modified_edge=None): 
        if modified_vertex: # Vérifie si un sommet a été modifié
            self.color_connected_component(modified_vertex) # met à jour des couleurs de la composante connectée du sommet modifié

        if modified_edge: # Vérifie si une arête a été modifiée
            for vertex in modified_edge: # Parcourt chaque sommet dans la liste modified_edge pour traiter chaque sommet de l'arête modifiée
                self.color_connected_component(vertex) # la composante connectée de chaque sommet de l'arête modifiée est mise à jour
    
    def plotGraph(self):
        # Extrait les informations pertinentes du graphe dynamique, notamment les sommets, les arêtes et les couleurs associées
        vertices = self.vertices
        edges = self.edges
        colors = self.colors
    
        # Calcule le nombre de sommets dans le graphe pour déterminer la taille de la matrice
        V = len(vertices)
    
        # Calcule les positions des sommets dans le plan en utilisant circular_layout
        pos = nx.circular_layout(nx.Graph(edges))
    
        plt.figure(figsize=(8, 8))
        plt.axis('equal')
    
        # Trace les arêtes du graphe en utilisant networkx.draw
        nx.draw(nx.Graph(edges), pos, with_labels=False, font_weight='bold', node_color='blue', font_color='black',
                font_size=10, node_size=100, edge_color='blue', linewidths=0.8, edgecolors='black')
    
        # Sélectionner uniquement les sommets qui ont des positions calculées (pos). 
        # Certains sommets peuvent ne pas être présents dans pos s'ils n'ont pas d'arêtes.
        valid_nodes = [v for v in vertices.keys() if v in pos]
        nx.draw_networkx_nodes(nx.Graph(edges), pos, nodelist=valid_nodes, node_color='red',
                               node_size=100, edgecolors='black', linewidths=1.5)
    
        # Ajoute du texte à la position du sommet pour afficher le numéro du sommet et la couleur attribuée
        for i in range(1, V + 1):
            if i in pos:  # Vérifie si le sommet a une position calculée (pos)
                plt.text(pos[i][0] + 0.02, pos[i][1] + 0.02, f"Sommet {i}\nCouleur: {colors.get(i, 'N/A')}", fontsize=10,
                         color=f'C{colors.get(i, "N/A")}')
    
        plt.show()

    def display_colored_graph(self): # Cette méthode est responsable de l'affichage des informations relatives au graphe colorié
        print("\nColored Dynamic Graph:") 
        print("Vertices:", self.vertices) # Affiche les sommets du graphe et leurs ensembles d'arêtes associés
        print("Edges:", self.edges) # Affiche l'ensemble des arêtes du graphe
        print("Colors:", self.colors) # Affiche les couleurs attribuées à chaque sommet du graphe
        
    def chromatic_number(self): # Cette méthode calcule le nombre chromatique du graphe
        self.color_graph() # attribuer des couleurs aux sommets du graphe si ce n'est pas déjà fait
        return len(set(self.colors.values())) # Retourne le nombre chromatique du graphe

    def reset_graph(self):
        self.vertices = {} # vertices (un dictionnaire)
        self.edges = set() # edges (un ensemble)
        self.colors = {} # et colors (un dictionnaire)
        self.edges_added = set()  # Ajouter cette ligne pour initialiser l'attribut edges_added
        



if __name__ == '__main__':
    g = DynamicGraph()
    g.add_vertex(1)
    g.add_vertex(2)

    g.add_edge((1, 2))
    g.color_graph()

    print(g.colors)