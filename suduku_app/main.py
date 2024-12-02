import tkinter as tk
from tkinter import messagebox
from sudoku_utils import SudokuBoard, sudoku_examples
import numpy as np


class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")

        # Matrice représentant la grille de Sudoku  non resolu(0 pour les cases vides)
        self.grid_examples = sudoku_examples
        self.reset_grid()

        # Bouton pour résoudre le Sudoku
        solve_button = tk.Button(self.root, text="Résoudre", command=self.solve_sudoku)
        
        # Bouton pour reinitialiser la grille avec une nouvelle configuration 
        reset_button = tk.Button(self.root, text="recommancer", command=self.reset_grid)
        
        #placement des boutons
        solve_button.grid(row=10, column=0, columnspan=4)
        reset_button.grid(row=10, column=4, columnspan=5)

    def create_grid(self):
        """
        Cette Fonction remplie la grille dans le graphique grace 
        à la matrice Sudoku selectionné
        """
        # parcours de de la matrice
        for i in range(9):
            for j in range(9):
                value = self.grid_values[i][j] # on recuperer le valeur a placé
                color = "blue" if value != 0 else "black" # la couleur des 
                if value == 0: # Si la valeur est 0 on met dans la grille un champ vide 
                    value= " " 
                
                label = tk.Label(
                    self.root, text=str(value), width=4, 
                    height=2, relief="solid", borderwidth=1, bg="white", fg=color
                    )
                label.grid(row=i, column=j)
    

    def update_grid(self, grid):
        """
        Cette fonction fait presque la meme chose que create_grid
        elle prend en parametre un grille deja resolu
        Si la case de la grille initial est égale à zero alors on affiche la case de la grille resolu
        sinon on afficher la case de la grille initial
        """
        # parcours de la grille
        for i in range(9):
            for j in range(9):
                # Si la case de la grille initial est égale à zero alors on affiche la case de la grille resolu
                value = grid[i][j] if self.grid_values[i][j] == 0 else self.grid_values[i][j] 
                # pour les nouvelle valeur de la grille on choisie la couleur rouge
                color = "red" if self.grid_values[i][j] == 0 else "blue"

                label = tk.Label(
                    self.root, text=str(value), width=4, 
                    height=2, relief="solid", borderwidth=1, bg="white", fg=color
                    )
                label.grid(row=i, column=j)

    def solve_sudoku(self):
        """
        Cette fonction resoue le grille de Sudoku et appelle la fonction 
        qui met a jour l'affichage de la grille 
        """

        if self.sudokuBoard.solveGraphColoring():# verifie si une solution a été trouver
            self.update_grid(self.sudokuBoard.board) # mise a jour de la grille
        else:
            messagebox.showinfo("Info", "cette grille n'as pas de solution") # messge d"erreur si 
            self.reset_grid() # on choisi un nouvelle grille de Sudoku à résoudre

    def reset_grid(self):
        """
        Cette fonction choisi aleatoirement un grille de Sudoku à résoudre 
        parmi les examples de Sudoku proposés
        """
        self.grid_values = self.grid_examples[np.random.randint(self.grid_examples.shape[0])]
        self.sudokuBoard = SudokuBoard(self.grid_values)
        self.create_grid()


    
if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
