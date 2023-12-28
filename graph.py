import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from collections import deque

@dataclass
class Vertex():
    """
    La classe Vertex classe decrit à la fois un sommet d'un graphe et un case
    de la grille du Sudoku.

    """

    cx : int  # abscisse de la case 
    cy : int # ordonnée de la case
    value : int = 0 # la valeur de la classe qui pourait correspondre a la couleur
    color : int = 0 # 

    nbInstance : int = 0
    id : int = 0

    def __init__(self, cx, cy, value=None):
        Vertex.nbInstance += 1
        self.id = Vertex.nbInstance
        self.cx = cx
        self.cy = cy
        self.value = value

    def __eq__(self, __value: object) -> bool:
        print(type(__value))
        assert isinstance(__value, Vertex)
        return __value.cx == self.cx and __value.cy == self.cy
    
    def __del__(self):
        pass

    def __hash__(self) -> int:
        return self.cx*1000 + self.cx**2 + self.cy**2 + self.cy
    
    def __str__(self) -> str:
        return f"({self.cx}, {self.cy})"
    
    def __repr__(self) -> str:
        return self.__str__()


@dataclass
class Edge():
    """
    La classe Edge represente un arrete du graphe 
    """
    vertices : frozenset

    def __init__(self, v1 : Vertex, v2 : Vertex):
        self.vertices = frozenset((v1, v2))

    def __iter__(self):
        return self.vertices.__iter__()

    def __eq__(self, __value: object) -> bool:
        assert isinstance(__value, Edge)
        return __value.vertices == self.vertices
    
    def __del__(self):
        pass

    def __hash__(self) -> int:
        return self.vertices.__hash__()




class DynamicSudokuGraph:
    """
    La classe DynamicSudokuGraph modelise le jeu de Sudoku grace a un graphe.
    Chaque sommet du graphe est une case de la grille de Sudoku et l'attribut *value*
    du sommet represente la couleur du sommet.
    La resolution par coloriage se fait en generant la matrice d'adjacence associé,
    de colorier la matrice puis de mettre a jour le graphe a partir
    """
    def __init__(self):
        self.vertices = {}
        self.edges = set()


    def add_vertex(self, vertex : Vertex):
        if vertex not in self.vertices:
            self.vertices[vertex] = set()

    def remove_vertex(self, vertex):
        if vertex in self.vertices:
            self.colors[vertex.color] = None
            self.edges = {edge for edge in self.edges if vertex not in edge.vertices}
            del self.vertices[vertex]

        pass

    def add_edge(self, edge : Edge):
        self.edges.add(edge)
        for vertex in edge:
            self.vertices[vertex].add(edge)

    def remove_edge(self, edge : Edge):
        if edge in self.edges:

            self.edges.remove(edge)
            for vertex in edge:
                self.vertices[vertex].remove(edge)

    def color_graph(self):
        pass






    def __get_adjacency_matrix(self):
        pass    

    def __update_graph_from_matrix():
        pass


if __name__ == '__main__':
    v1 = Vertex(cx=0, cy=0)
    v2 = Vertex(cx=1, cy=1)
    v3 = Vertex(cx=0, cy=1)
    v4 = Vertex(cx=1, cy=0)

    dynamic_graph1 = DynamicSudokuGraph()

    # Add vertices and edges
    dynamic_graph1.add_vertex(v1)
    dynamic_graph1.add_vertex(v2)
    dynamic_graph1.add_vertex(v3)
    dynamic_graph1.add_vertex(v4)
    dynamic_graph1.add_edge(Edge(v1, v2))
    dynamic_graph1.add_edge(Edge(v1, v3))
    dynamic_graph1.add_edge(Edge(v1, v4))
    dynamic_graph1.add_edge(Edge(v2, v3))
    dynamic_graph1.add_edge(Edge(v3, v4))


    # Display the colored graph 1
    dynamic_graph1.color_graph()
    dynamic_graph1.display_colored_graph()
    print("Chromatic Number du graphe 1: ", dynamic_graph1.chromatic_number())

    # Remove a vertex
    dynamic_graph1.remove_vertex(v1)

    # Display the colored graph 1 after removal
    dynamic_graph1.color_graph()
    dynamic_graph1.display_colored_graph()
    print("Chromatic Number du graphe 1 après suppression du sommet 1: ", dynamic_graph1.chromatic_number())

