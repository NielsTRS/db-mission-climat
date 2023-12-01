import tkinter as tk
from utils import display
from tkinter import ttk


class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(600, 400, self)
        self.title('Q2 : département le plus froid par région')
        display.defineGridDisplay(self, 2, 1)
        ttk.Label(self,
                  text="Modifier cette fonction en s'inspirant du code de F1, pour qu'elle affiche le(s) département(s) avec la température moyenne (c.a.d. moyenne des moyennes de toutes les mesures) la plus basse par région. \nSchéma attendu : (nom_region, nom_departement, temperature_moy_min)",
                  wraplength=500, anchor="center", font=('Helvetica', '10', 'bold')).grid(sticky="we", row=0)

        # TODO Q2 Modifier la suite du code (en se basant sur le code de F1) pour répondre à Q2

        # On définit les colonnes que l'on souhaite afficher dans la fenêtre et la requête
        columns = ('nom_region', 'nom_departement', 'temperature_min_moy')
        query = """
                WITH TempMoyByDep AS (
                    SELECT code_region, code_departement, AVG(temperature_moy_mesure) AS temperature_moy_dep
                    FROM Regions
                    JOIN Departements USING (code_region)
                    JOIN Mesures USING (code_departement)
                    GROUP BY code_region, code_departement
                ), TempMinMoyByRegion AS (
                    SELECT nom_region, MIN(temperature_moy_dep) AS temperature_min_moy
                    FROM TempMoyByDep JOIN Regions USING (code_region)
                    GROUP BY nom_region
                )
                SELECT nom_region, nom_departement, temperature_min_moy
                FROM TempMinMoyByRegion
                JOIN TempMoyByDep ON (temperature_moy_dep = temperature_min_moy)
                JOIN Departements USING (code_departement);
                """

        # On utilise la fonction createTreeViewDisplayQuery pour afficher les résultats de la requête
        # TODO Q1 Aller voir le code de createTreeViewDisplayQuery dans utils/display.py
        tree = display.createTreeViewDisplayQuery(self, columns, query, 200)
        tree.grid(row=0, sticky="nswe")
