import time
import tkinter as tk
from tkinter import ttk, messagebox
from graph_utils import DynamicGraph


class GraphEditor:

    def __init__(self, master):
        self.master = master
        self.master.title("Coloriage de Graphe")
        
        # on cree notre instance de  graphe dynamique
        self.dynamic_graph = DynamicGraph()


        self.vertices = {} # le dictionnaire qui va stocker les sommets
        self.counter = 1 # le compteurs de sommets
        self.edit_mode = True # cette attribut permet d'autoriser la modification du grame

        # On a un frame à gauche qui va contenir les bontons de manipulation
        self.left_frame = ttk.Frame(self.master)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # on appel la fonction qui va placé les composants du frame de gauche
        self.fill_left_frame()
       
        # Canvas à droite ou on va dessiner notre notre graphe
        self.fill_right_frame()


        
        

    def update_combobox(self):
        vertex_numbers = [str(i) for i in range(1, self.counter)]
        self.vertex_selection_1['values'] = vertex_numbers
        self.vertex_selection_2['values'] = vertex_numbers



    def add_vertex(self, event):
        """
        cette fonction cree les sommets de notre graphe en cliquant sur le canva
        """
        if self.edit_mode: # On verifie que le mode edition est activé
            x, y = event.x, event.y # on recupere les coordonnée du clique
            # on cree on cercle avec le numro du sommet dedans 
            vertex = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="blue")
            label = self.canvas.create_text(x, y, text=str(self.counter), fill="white" )
            # ajoute le sommet dans notre dictionnaire des sommets
            self.vertices[vertex] = (x, y, label, self.counter)
            # On ajoute le sommet dans le graphe dynamique
            self.dynamic_graph.add_vertex(self.counter)

            # incrementation du compteur
            self.counter += 1

            # mis à jour du combo box des sommets existants
            self.update_combobox()
        
    def create_edge(self):
        """
        Cette fonction ajoute un arête entre 2 sommets
        """
        if self.edit_mode:# On verifie que le mode edition est activé
            # verfication de sureté 
            if len (self.vertex_selection_1.get()) == 0 or len (self.vertex_selection_2.get()) ==0: 
                messagebox.showinfo("info", "Impossible de creer cette arete")
            
            else:
                vertex_number_1 = int(self.vertex_selection_1.get()) # on recupere le premier sommet séléction
                vertex_number_2 = int(self.vertex_selection_2.get()) # on recupere le deuxieme sommet séléction

                # on verifie que les sommet séléctionnée sont differents
                if vertex_number_1 != vertex_number_2: 

                    # verifie que l'arret n'existe pas deja
                    if self.dynamic_graph.edge_exists((vertex_number_1, vertex_number_2)):
                        return messagebox.showinfo("info", "Cette arête existe deja")
                    
                    # Si tout va bien on ajoute le arête dasn le graphedynamique
                    self.dynamic_graph.add_edge((vertex_number_1, vertex_number_2))
                    

                    vertex_1 = self.find_vertex_by_number(vertex_number_1)
                    vertex_2 = self.find_vertex_by_number(vertex_number_2)

                    # On recupere les coordonnées des sommets
                    if vertex_1 and vertex_2:
                        x1, y1, _, _ = self.vertices[vertex_1]
                        x2, y2, _, _ = self.vertices[vertex_2]
                         # on trace l'arête au niveau du canva
                        self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)
        else:
                messagebox.showinfo("info", "Coloration terminée , veillez reinitialiser le graphe")

    def find_vertex_by_number(self, number):
        """
        Cette fonction recupere un vertex a partir de son numero
        """
        for vertex, (_, _, _, vertex_num) in self.vertices.items():
            if vertex_num == number:
                return vertex
        return None
    
    def reset_application(self):
        """
        Cette fonction reinitialise le l'application  
        """
        self.canvas.delete("all")
        self.vertices = {}
        self.counter = 1
        self.edit_mode = True
        self.update_combobox()
        self.dynamic_graph.reset_graph()
    
    def fill_left_frame(self):
        """
        Cette fonction place les composants du frame de gauche 
       """
        # Grille dans le frame à gauche
        # On place les labels des Combo box
        ttk.Label(self.left_frame, text="Sélectionnez le sommet 1:").grid(row=0, column=0, pady=5)
        ttk.Label(self.left_frame, text="Sélectionnez le sommet 2:").grid(row=1, column=0, pady=5)

        self.vertex_selection_1 = ttk.Combobox(self.left_frame, state="readonly")
        self.vertex_selection_2 = ttk.Combobox(self.left_frame, state="readonly")

        # On place les Combo box
        self.vertex_selection_1.grid(row=0, column=1, pady=5)
        self.vertex_selection_2.grid(row=1, column=1, pady=5)

        # Le bouton pour ajouter l'arete
        ttk.Button(self.left_frame, text="Ajouter l'arête", command=self.create_edge).grid(row=2, column=0, columnspan=2, pady=10)

        # On ajoute les boutons pour de coloriage du graphe et de reinitialisation de 
        ttk.Button(self.left_frame, text="Colorier le graphe", command=self.color_graph).grid(row=3, column=0, pady=5)
        # On ajoute les boutons de reinitialisation de l'application
        ttk.Button(self.left_frame, text="Réinitialiser", command=self.reset_application).grid(row=3, column=1, pady=5)

        ttk.Button(self.left_frame, text="Aidez moi", command=self.show_help).grid(row=4, column=0, columnspan=2, pady=10)
        # on appelle la fonction de mis a jour de la liste des combo box (liste deroulant)
        self.update_combobox()
        
    def fill_right_frame(self):
        """
        Cette Fonction cree la canva ou sera dessiner notre graphe
        """
        self.canvas = tk.Canvas(self.master, bg="white", width=400, height=400)
        self.canvas.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)



        self.canvas.bind("<Button-1>", self.add_vertex)

    def color_graph(self):
        """
        Cette fonction bloque l'édition du graphe , appelle la coloration du graphe  
        puis affiche l'attribution des couleurs dans le canvas
        """
        self.edit_mode = not self.edit_mode # bloquage de l'edition du graphe 
        self.dynamic_graph.color_graph() # coloriage du graphe 
        for vertex in self.vertices:# parcours des sommets
            # recuperation des coordonées du sommet
            x, y, _, vertex_num = self.vertices[vertex]
            # ajoute de la couleur du sommet
            self.canvas.create_text(x-10, y-15, text=f"couleur : {self.dynamic_graph.colors[vertex_num]}", fill="red")
        
        self.canvas.create_text(200, 10, text=f"Nombre chromatique : {self.dynamic_graph.chromatic_number()}", fill="blue")
            
    def show_help(self):
        # Création de la fenêtre flottante
        floating_window = tk.Toplevel(self.master)
        floating_window.title("Aidez moi")
        floating_window.geometry("700x300")

        # Ajout de la zone de texte non éditable à la fenêtre flottante
        canvas = tk.Canvas(floating_window, bg="white", width=600, height=300)
        canvas.pack(padx=10, pady=10)

        # Ajout du texte au canevas
        messages = [
            "",
            "Pour ajouter un sommet, cliquez sur le rectangle blanc à votre droite",
            "Pour ajouter des arêtes, sélectionnez deux sommets avec les listes déroulantes",
            "Puis cliquez sur 'Ajouter l'arête'",
            "Pour colorier votre graphe, cliquez sur 'Colorier le graphe'",
            "Cliquez sur 'Réinitialiser' pour redémarrer l'application"
        ]

        y_position = 20
        for message in messages:
            canvas.create_text(300, y_position, text=message, fill="black", anchor="center")
            y_position += 30


       

        # Ajout d'un bouton pour fermer la fenêtre flottante
        ttk.Button(floating_window, text="Fermer", command=floating_window.destroy).pack(pady=10)


        # messagebox.showinfo("Aidez moi", 
        #                     "Pour ajouter un sommet cliquez sur le rectangle blanc à votre droite\n"
        #                     "Pour ajouter des arêtes selectionnez deux sommets avec les listes déroulantes puis cliquez sur ''ajouter l'arête'\n"
        #                     "Pour colorier votre graphe cliquez sur 'Colorier le graphe'\n"
        #                     "Cliquez sur 'Réinitialiser' pour redemarer l'application\n")


def main():
    root = tk.Tk()
    app = GraphEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
