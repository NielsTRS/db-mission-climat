import tkinter as tk
from tkinter import ttk
from utils import display
from utils import db

class Window(tk.Toplevel):

    treeView = None
    entry = None
    listbox = None
    errorLabel = None

    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre et des lignes/colonnes
        display.centerWindow(600, 450, self)
        self.title('Q3 : départements pour une région donnée (version dynamique)')
        display.defineGridDisplay(self, 3, 3)
        self.grid_rowconfigure(3, weight=10) #On donne un poids plus important à la dernière ligne pour l'affichage du tableau
        ttk.Label(self, text="On a repris le code de F2. Modifier l'interface pour proposer un choix de la région sans saisie manuelle (par exemple un proposer un menu déroulant avec les valeurs extraites de la base, ou toute autre idée).",
                  wraplength=500, anchor="center", font=('Helvetica', '10', 'bold')).grid(sticky="we", row=0,columnspan=3)

        ttk.Label(self, text='Veuillez indiquer une région :', anchor="center", font=('Helvetica', '10', 'bold')).grid(row=1, column=0)
        #TODO Q3 C'est cette partie que l'on souhaite changer pour un choix dynamique de la région
        self.entry = tk.Entry(self)
        self.entry.grid(row=1, column=1)
        self.entry.bind('<KeyRelease>', self.update_suggestions)

        ttk.Button(self, text='Valider', command=self.searchRegion).grid(row=1, column=2)

        # On place un label sans texte, il servira à afficher les erreurs
        self.errorLabel = ttk.Label(self, anchor="center", font=('Helvetica', '10', 'bold'))
        self.errorLabel.grid(columnspan=3, row=2, sticky="we")

        # On prépare un treeView vide pour l'affichage de nos résultats
        columns = ('code_departement', 'nom_departement',)
        self.treeView = ttk.Treeview(self, columns=columns, show='headings')
        for column in columns:
            self.treeView.column(column, anchor=tk.CENTER, width=15)
            self.treeView.heading(column, text=column)
        self.treeView.grid(columnspan=3, row=3, sticky='nswe')

        self.listbox = tk.Listbox(self)
        self.listbox.grid(row=2, column=1, sticky="ew")
        self.listbox.grid_forget()
        self.listbox.bind('<ButtonRelease-1>', self.select_from_listbox)

    # Fonction qui récupère la valeur saisie, exécute la requête et affiche les résultats
    # La fonction prend un argument optionnel event car elle peut être appelée de deux manières :
    # Soit via le bouton Valider, dans ce cas aucun event n'est fourni
    # Soit via le bind qui a été fait sur la case de saisie quand on appuie sur Entrée, dans ce cas bind fournit un event (que l'on utilise pas ici)
    # TODO Q3 Modifier la fonction searchRegion pour un choix dynamique de la région

    def get_regions_from_database(self):
        cursor = db.data.cursor()
        cursor.execute("""
            SELECT DISTINCT nom_region FROM Regions
        """)
        regions = [row[0] for row in cursor.fetchall()]
        return regions

    def update_suggestions(self, event):
        typed_text = self.entry.get()
        regions = self.get_regions_from_database()

        # Filtrage des régions en fonction de ce que tape l'utilisateur
        suggestions = [region for region in regions if typed_text.lower() in region.lower()]

        # Mise à jour de la liste
        self.listbox.delete(0, tk.END)
        for suggestion in suggestions:
            self.listbox.insert(tk.END, suggestion)

        if suggestions:
            self.listbox.grid(row=2, column=1, sticky="ew")
        else:
            self.listbox.grid_forget()

    def select_from_listbox(self, event):
        selected_item = self.listbox.get(self.listbox.curselection())
        self.entry.delete(0, tk.END)
        self.entry.insert(0, selected_item)
        self.listbox.grid_forget()

    def searchRegion(self):
        self.treeView.delete(*self.treeView.get_children())
        region = self.entry.get()

        if len(region) == 0:
            self.errorLabel.config(foreground='red', text="Veuillez sélectionner une région !")
        else:
            try:
                cursor = db.data.cursor()
                result = cursor.execute("""SELECT code_departement, nom_departement
                                            FROM Departements JOIN Regions USING (code_region)
                                            WHERE nom_region = ?
                                            ORDER BY code_departement""", [region])
            except Exception as e:
                self.errorLabel.config(foreground='red', text="Erreur : " + repr(e))
            else:
                i = 0
                for row in result:
                    self.treeView.insert('', tk.END, values=row)
                    i += 1
                if i == 0:
                    self.errorLabel.config(foreground='orange', text="Aucun résultat pour la région \"" + region + "\" !")
                else:
                    self.errorLabel.config(foreground='green', text="Voici les résultats pour la région \"" + region + "\" :")