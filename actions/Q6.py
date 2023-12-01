import tkinter as tk
from utils import display
from utils import db
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(1000, 600, self)
        self.title('Q6 : Graphique correlation temperatures minimales - coût de travaux (Ain / 2018)')
        display.defineGridDisplay(self, 2, 1)

        query = """
            WITH Data AS (SELECT strftime('%Y-%m', date_travaux) as date, code_departement, SUM(cout_total_ht_travaux) as total
              FROM Travaux
              GROUP BY date, code_departement)

            SELECT D.date, D.total, AVG(M.temperature_min_mesure)
            FROM Data D
            JOIN Mesures M ON (D.code_departement = M.code_departement AND D.date = strftime('%Y-%m', M.date_mesure) AND D.code_departement = 1)
            GROUP BY D.date, D.total;
        """

        # Extraction des données et affichage dans le tableau
        result = []
        try:
            cursor = db.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            print("Erreur : " + repr(e))

        # Extraction et préparation des valeurs à mettre sur le graphique
        tabmin = []
        tabtot = []
        tabx = []
        for row in result:
            tabx.append(row[0])
            tabtot.append(row[1])
            tabmin.append(row[2])

        # Formatage des dates pour l'affichage sur l'axe x
        datetime_dates = [datetime.strptime(date, '%Y-%m') for date in tabx]

        # Ajout de la figure et des subplots qui contiendront le graphique
        fig, ax1 = plt.subplots(figsize=(10, 6), dpi=100)

        # Affichage de la courbe température minimale sur l'axe y1
        color1 = 'tab:blue'
        ax1.set_xlabel('Mois')
        ax1.set_ylabel('Température Minimale', color=color1)
        ax1.plot(datetime_dates, tabmin, color=color1)
        ax1.tick_params(axis='y', labelcolor=color1)
        ax1.set_xticks([i for i, date in enumerate(datetime_dates) if date.day == 1])
        ax1.set_xticklabels([date.strftime('%m-%d') for date in datetime_dates if date.day == 1], rotation=45)

        # Création d'un axe y secondaire (y2) pour la courbe coût travaux
        ax2 = ax1.twinx()
        color2 = 'tab:green'
        ax2.set_ylabel('Coût Travaux', color=color2)
        ax2.plot(datetime_dates, tabtot, color=color2)
        ax2.tick_params(axis='y', labelcolor=color2)

        fig.tight_layout()

        # Affichage du graphique
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
