from graph_utils import Graph
import numpy as np


class SudokuConnections : 
    """
    le classe SudokuConnections fait le rapport entre le graphe et la grille de Sudoku
    Chaque case de la grille de Sudoku est un sommet du graphe
    """
    def __init__(self) :  # constructor

        self.graph = Graph() # Graph Object

        # la grille contiendra 81  cases soit 9*9 
        self.rows = 9 
        self.cols = 9
        self.total_blocks = self.rows*self.cols #81

        self.__generateGraph() # on genere les sommets du graphes 
        self.connectEdges() # et on les connectes selon les contraintes du Sudoku 

        self.allIds = self.graph.getAllNodesIds() # recuperer tous les identifiants des sommets du graph

        

    def __generateGraph(self) : 
        """
        Génère des nœuds avec un identifiant compris entre 1 et 81.
         Tous deux inclus
        """
        for idx in range(1, self.total_blocks+1) : 
            _ = self.graph.addNode(idx)

    def connectEdges(self) : 
        """
        Connectez les nœuds selon les contraintes Sudoku :
         # LIGNES
        depuis le début de chaque numéro d'identification, connectez tous les
        nombres successifs jusqu'à atteindre un multiple de 9
         # COLS (ajouter 9 (+9))
         à partir du début du numéro d'identification. +9 pour chaque connexion
         jusqu'à ce que vous atteigniez un nombre >= 73 et <= 81
         # BLOCS
         Connectez tous les éléments du bloc qui ne
         viennent dans la même colonne ou ligne.
         1 2 3
         10 11 12 
         19 20 21
         1 -> 11, 12, 20, 21
         2 -> 10, 19, 12, 21
         3 -> 10, 11, 19, 20
         De même pour 10, 11, 12, 19, 20, 21.
        """
        matrix = self.__getGridMatrix() 

        head_connections = dict() 

        for row in range(9) :
            for col in range(9) : 
                
                head = matrix[row][col] #id of the node
                connections = self.__whatToConnect(matrix, row, col)
                
                head_connections[head] = connections
        # connect all the edges

        self.__connectThose(head_connections=head_connections)
        
    def __connectThose(self, head_connections) : 
        """
        Cette fonction recupere les connection a effectuer et les tranqforme 
        en arrete pour le graphe
        """
        for head in head_connections.keys() : #head is the start idx
            connections = head_connections[head]
            for key in connections :  #get list of all the connections
                for v in connections[key] : 
                    self.graph.addEdge(src=head, dst=v)

 
    def __whatToConnect(self, matrix, rows, cols) :

        """
        matrice : stocke l'identifiant de chaque nœud représentant chaque cellule
        renvoie le dictionnaire
        connexions - dictionnaire
        rows : [tous les identifiants des lignes]
        cols : [tous les identifiants dans les cols]
        blocs : [tous les identifiants du bloc]
    
        ** à connecter à la tête.
        """
        connections = dict()

        row = []
        col = []
        block = []

        """
        Ici on recupere les identifiants des somments 
        situé sur la meme ligne car elles sont tous adjacents entre eux
        """
        for c in range(cols+1, 9) : 
            row.append(matrix[rows][c])
        
        connections["rows"] = row 

        """
        Ici on recupere les identifiants des somments 
        situé sur la meme colonne car elles sont tous adjacents entre eux
        """
        for r in range(rows+1, 9):
            col.append(matrix[r][cols])
        
        connections["cols"] = col

        """
        Ici on recupere les identifiants des somments 
        situé sur la meme blocks car elles sont tous adjacents entre eux
        """
        
        """
        il y'a 9 block dans la grille 

        """
        if rows%3 == 0 :   # la premier rangé de block 

            if cols%3 == 0 : # le premier block
                
                block.append(matrix[rows+1][cols+1])
                block.append(matrix[rows+1][cols+2])
                block.append(matrix[rows+2][cols+1])
                block.append(matrix[rows+2][cols+2])

            elif cols%3 == 1 :# le deuxiemme  block
                
                block.append(matrix[rows+1][cols-1])
                block.append(matrix[rows+1][cols+1])
                block.append(matrix[rows+2][cols-1])
                block.append(matrix[rows+2][cols+1])
                
            elif cols%3 == 2 : # le troisieme block
                
                block.append(matrix[rows+1][cols-2])
                block.append(matrix[rows+1][cols-1])
                block.append(matrix[rows+2][cols-2])
                block.append(matrix[rows+2][cols-1])

        elif rows%3 == 1 : # la deuxieme rangé de block 
            
            if cols%3 == 0 :# le premier block
                
                block.append(matrix[rows-1][cols+1])
                block.append(matrix[rows-1][cols+2])
                block.append(matrix[rows+1][cols+1])
                block.append(matrix[rows+1][cols+2])

            elif cols%3 == 1 :# le deuxieme block
                
                block.append(matrix[rows-1][cols-1])
                block.append(matrix[rows-1][cols+1])
                block.append(matrix[rows+1][cols-1])
                block.append(matrix[rows+1][cols+1])
                
            elif cols%3 == 2 : # le troisieme block
                
                block.append(matrix[rows-1][cols-2])
                block.append(matrix[rows-1][cols-1])
                block.append(matrix[rows+1][cols-2])
                block.append(matrix[rows+1][cols-1])

        elif rows%3 == 2 : # la troisieme rangé de block 
            
            if cols%3 == 0 : # le premier block
                
                block.append(matrix[rows-2][cols+1])
                block.append(matrix[rows-2][cols+2])
                block.append(matrix[rows-1][cols+1])
                block.append(matrix[rows-1][cols+2])

            elif cols%3 == 1 : # le deuxieme block
                
                block.append(matrix[rows-2][cols-1])
                block.append(matrix[rows-2][cols+1])
                block.append(matrix[rows-1][cols-1])
                block.append(matrix[rows-1][cols+1])
                
            elif cols%3 == 2 : # le troisieme block
                
                block.append(matrix[rows-2][cols-2])
                block.append(matrix[rows-2][cols-1])
                block.append(matrix[rows-1][cols-2])
                block.append(matrix[rows-1][cols-1])
        
        connections["blocks"] = block
        return connections

    def __getGridMatrix(self) : 
        """
        Génère la grille ou la matrice 9x9 composée d'identifiants de nœuds.
        
        Cette matrice fera office de mappeur de chaque cellule avec chaque nœud
        via les identifiants de nœuds
        """
        matrix = [[0 for cols in range(self.cols)] 
        for rows in range(self.rows)]

        count = 1
        for rows in range(9) :
            for cols in range(9):
                matrix[rows][cols] = count
                count+=1
        return matrix
    
class SudokuBoard : 
    """
    La classe SodukuBoard s'appuie sur la classer SudokuConnections
    et ajoute les fonction de resolution par colloriage
    """
    def __init__(self, board : list) : 

        self.board = board.copy() # On lui donne un grille de Sudoku a resoudre
        
        self.sudokuGraph = SudokuConnections() # il cree un objet SudokuConnect dont il va se servir pour modeliser le jeu en graphe
        self.mappedGrid = self.__getMappedMatrix() # recupere tous les identifiants à la position dans la matrice

    def __getMappedMatrix(self) : 
        """
        Cette fonction associe a chaque case de coordonne i,j un identifiants
        """
        matrix = [[0 for cols in range(9)] 
        for rows in range(9)]

        count = 1
        for rows in range(9) : 
            for cols in range(9):
                matrix[rows][cols] = count
                count+=1
        return matrix

    def getSolveGrid(self):
        """Cette fonction resoud le Sudoku par coloriage et retourne la matrice de la
        grille resolu
        """
        self.solveGraphColoring()
        return self.board

    def is_Blank(self) : 
        """
            recupere la presmiere case vide de la grille 
        """
        for row in range(len(self.board)) :
            for col in range(len(self.board[row])) : 
                if self.board[row][col] == 0 : 
                    return (row, col)
        return None

    def isValid(self, num, pos) :
        """
        Cette Fonction verifie que le chiffre num peut etre mise a la position(i, j)
        """
        # ROW
        """Ici on verifie qu'il n'y a pas de chiffre similaire sur la meme ligne"""
        for col in range(len(self.board[0])):
            if self.board[pos[0]][col] == num and pos[0] != col :
                return False 

        # COL
        """Ici on verifie qu'il n'y a pas de chiffre similaire sur la meme colonne"""
        for row in range(len(self.board)):
            if self.board[row][pos[1]] == num and pos[1] != row : 
                return False

        # BLOCK
            """Ici on verifie qu'il n'y a pas de chiffre similaire dans le meme block"""
        x = pos[1]//3
        y = pos[0]//3

        for row in range(y*3, y*3+3) :
            for col in range(x*3, x*3+3) :
                if self.board[row][col] == num and (row, col) != pos : 
                    return False

        return True

    def graphColoringInitializeColor(self):
        """
        Cette fonction rempli les couleurs déjà données
        """
        color = [0] * (self.sudokuGraph.graph.totalV+1)
        given = [] # liste de tous les identifiants dont la valeur est déjà donnée. Cela ne peut pas être modifié
        for row in range(len(self.board)) : 
            for col in range(len(self.board[row])) : 
                if self.board[row][col] != 0 : 
                    #obtenez d'abord l'identifiant du poste
                    idx = self.mappedGrid[row][col]
                    #mettre à jour la couleur
                    color[idx] = self.board[row][col] 
                    given.append(idx) # ajout du sommet parmi les sommet deja colré
        return color, given

    def solveGraphColoring(self, m =9) : 
        """Cette fonction initie la colorationn du graphe """
        color, given = self.graphColoringInitializeColor()  #recuperation des couleur et des sommet deja coloré
        # appel de l'algorithme de coloriage par backtracking
        if self.__graphColorUtility(m =m, color=color, v =1, given=given) is None : 
            return False
        count = 1
        # assignation des casee a leur coleur apres execution de l'algorithme de backtracking
        for row in range(9) : 
            for col in range(9) :
                self.board[row][col] = color[count]
                count += 1
        return color
    
    def __graphColorUtility(self, m, color, v, given) :
        """
        algorithme de coloriage par backtracking
        """
        if v == self.sudokuGraph.graph.totalV +1 : 
            return True
        for c in range(1, m+1) : 
            if self.__isSafe2Color(v, color, c, given) == True :
                color[v] = c
                if self.__graphColorUtility(m, color, v+1, given) : 
                    return True
            if v not in given : 
                color[v] = 0


    def __isSafe2Color(self, v, color, c, given) : 
        """
        utilitaire de l'algorithme de coloriage par backtracking 
        cette fonction verifie qu'une coleur peut etre associe a un sommet 
        """
        if v in given and color[v] == c: 
            return True
        elif v in given : 
            return False

        for i in range(1, self.sudokuGraph.graph.totalV+1) :
            if color[i] == c and self.sudokuGraph.graph.isNeighbour(v, i) :
                return False
        return True


sudoku_examples = np.array([
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ],
    [
        [0, 2, 0, 0, 8, 0, 6, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 7, 4],
        [0, 0, 0, 0, 0, 4, 9, 0, 0],
        [1, 0, 8, 0, 0, 0, 0, 0, 0],
        [7, 0, 0, 0, 0, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 0, 4, 0, 9],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [5, 7, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 6, 0, 9, 0, 0, 5, 0]
    ],
    [
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0]
    ],
    [
        [0, 0, 3, 0, 2, 0, 6, 0, 0],
        [9, 0, 0, 3, 0, 5, 0, 0, 1],
        [0, 0, 1, 8, 0, 6, 4, 0, 0],
        [0, 0, 8, 1, 0, 2, 9, 0, 0],
        [7, 0, 0, 0, 8, 0, 0, 0, 2],
        [0, 0, 6, 7, 0, 8, 2, 0, 0],
        [0, 0, 2, 6, 0, 9, 5, 0, 0],
        [8, 0, 0, 2, 0, 3, 0, 0, 9],
        [0, 0, 5, 0, 1, 0, 3, 0, 0]
    ],
    [
        [1, 0, 0, 0, 0, 7, 0, 9, 0],
        [0, 3, 0, 0, 2, 0, 0, 0, 8],
        [0, 0, 9, 6, 0, 0, 5, 0, 0],
        [0, 0, 5, 3, 0, 0, 9, 0, 0],
        [0, 1, 0, 0, 8, 0, 0, 0, 2],
        [6, 0, 0, 0, 0, 4, 0, 0, 0],
        [3, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 4, 0, 0, 0, 0, 0, 0, 7],
        [0, 0, 7, 0, 0, 0, 3, 0, 0]
    ],
    [
        [0, 0, 1, 0, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 9, 0, 0, 0, 7, 0],
        [0, 2, 0, 0, 0, 0, 4, 0, 0],
        [0, 0, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 0, 5],
        [6, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 4, 0, 0, 0, 8, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    [
        [1, 0, 0, 0, 7, 0, 0, 3, 0],
        [8, 3, 0, 6, 0, 0, 0, 0, 0],
        [0, 0, 2, 9, 0, 0, 6, 0, 8],
        [6, 0, 0, 0, 0, 4, 9, 0, 7],
        [0, 9, 0, 0, 0, 0, 0, 5, 0],
        [3, 0, 7, 5, 0, 0, 0, 0, 4],
        [2, 0, 8, 0, 0, 9, 7, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 4, 3],
        [0, 4, 0, 0, 8, 0, 0, 0, 9]
    ],
])