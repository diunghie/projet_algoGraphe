import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from collections import deque


class Node : 
    """
    cette classe modelise les sommets d'un graohes
    un sommet est definit par son identifiant , une donnée, et   ses sommets adjacents
    """
    def __init__(self, idx, data = 0) : # Constructor   
        """
        id : Integer (1, 2, 3, ...)
        """
        self.id = idx #
        self.data = data
        self.connectedTo = dict()

    def addNeighbour(self, neighbour , weight : int = 0 ) :
        """
        Cette fonction ajoute un nouveau sommet au dictionnaire des sommets adjacents s'il n'est pas deja dans le dictionnaire
        """
        if neighbour.id not in self.connectedTo.keys() :   
            self.connectedTo[neighbour.id] = weight

    # setter
    def setData(self, data) : 
        self.data = data 

    #getter
    def getConnections(self) : 
        return self.connectedTo.keys()

    def getID(self) : 
        return self.id
    
    def getData(self) : 
        return self.data

    def getWeight(self, neighbour) : 
        return self.connectedTo[neighbour.id]

    def __str__(self) : 
        return str(self.data) + " Connected to : "+ \
         str([x.data for x in self.connectedTo])

class Graph : 
    """
    La classe Graph modélise un graphes juste avec un ensemble de sommets
    Les informations sur les arretes sont directement incorporé dans les sommets
    """
    totalV = 0 # total vertices in the graph
    
    def __init__(self) : 
        """
        allNodes = Dictionary (key:value)
                   idx : Node Object
        """
        self.allNodes = dict()

    def addNode(self, idx) : 
        """ ajout d'un sommet """
        if idx in self.allNodes : # on s'assure que le sommet n'est pas deja present dans le dictionnaire des sommets
            return None
        
        Graph.totalV += 1 # incrementation du nombre total de sommets
        node = Node(idx=idx) # creation d'un nouveau sommet
        self.allNodes[idx] = node # ajout du sommet dasn le dictionnaires des sommet
        return node

    def addNodeData(self, idx, data) : 
        """ assignation d'une données a un sommet """
        if idx in self.allNodes :  # verifier que le sommet est present 
            node = self.allNodes[idx] # selection du sommet en question
            node.setData(data) # assignation de la données
        else : 
            print("No ID to add the data.")

    def addEdge(self, src, dst, wt = 0) : 
        """
        creation d'un arrete par ajouts mutuelle de chacun des sommets dans la liste des sommets
        adjacents de l'autre
        """
        self.allNodes[src].addNeighbour(self.allNodes[dst], wt) 
        self.allNodes[dst].addNeighbour(self.allNodes[src], wt)
    
    def isNeighbour(self, u, v) : 
        """
        verifie si u et v sont les identifiants de sommets adjacents
        """
        if u >=1 and u <= 81 and v >=1 and v<= 81 and u !=v : # verifie si les id sont compris en 1 et 81
            if v in self.allNodes[u].getConnections() : 
                return True
        return False

    # getter
    def getNode(self, idx) : 
        if idx in self.allNodes : 
            return self.allNodes[idx]
        return None

    def getAllNodesIds(self) : 
        return self.allNodes.keys()

    # methods
    def DFS(self, start) :
        """
           Deroulement de l'algorithme DFS ( Depth First Search) pour rechercher un données a travers le graphe
        """ 
        # STACK
        visited = [False]*Graph.totalV

        if start in self.allNodes.keys() : 
            self.__DFSUtility(node_id = start, visited=visited) 
        else: 
            print("Start Node not found")

    def __DFSUtility(self, node_id, visited) : 
        visited = self.__setVisitedTrue(visited=visited, node_id=node_id)
        #print
        print(self.allNodes[node_id].getID(), end = " ")

        #Recursive Stack
        for i in self.allNodes[node_id].getConnections() : 
            if visited[self.allNodes[i].getID()] == False : 
                self.__DFSUtility(node_id = self.allNodes[i].getID(), 
                visited=visited)

    def BFS(self, start) : 
        """
           Deroulement de l'algorithme BFS (Breadth First Search) pour rechercher un données a travers le graphe
        """ 
        #Queue
        visited = [False]*Graph.totalV

        if start in self.allNodes.keys() : 
            self.__BFSUtility(node_id = start, visited=visited) 
        else : 
            print("Start Node not found")

    def __BFSUtility(self, node_id, visited) :
        queue = []
        visited = self.__setVisitedTrue(visited=visited, node_id=node_id)

        queue.append(node_id)

        while queue != [] : 
            x = queue.pop(0) 
            #print
            print(self.allNodes[x].getID(), end = " ")

            for i in self.allNodes[x].getConnections() : 
                idx = self.allNodes[i].getID()
                if visited[idx]  == False : 
                    queue.append(idx)
                    visited = self.__setVisitedTrue(visited=visited,
                     node_id=idx)
        


    def __setVisitedTrue(self, visited, node_id) : 
        """
        Utilitaire pour les algorithmes BFS et DFS

        Grâce à cette fonction, nous définirons visit[id] = True
        Prétraitement node_id si nécessaire
        Puisque désormais node_id est un entier, il n'est pas nécessaire de le prétraiter
        """
        visited[node_id] = True
        return visited