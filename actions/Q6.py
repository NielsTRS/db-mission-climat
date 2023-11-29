import tkinter as tk
from utils import display
from utils import db
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(1000, 600, self)
        self.title('Q6 : Graphique correlation temperatures minimales - coût de travaux (Isère / 2022)')
        display.defineGridDisplay(self, 2, 1)
   #     ttk.Label(self, text="""Pour l’Isère et l'année 2022, donner deux courbes sur le même graphique  :
   #- par mois, l’évolution de la moyenne des températures minimales
   #- par mois, l’évolution des totaux de coûts de travaux tout type confondu""",
   #               wraplength=500, anchor="center", font=('Helvetica', '10', 'bold')).grid(sticky="we", row=0)
        query = """
                    SELECT M.date_mesure, AVG(M.temperature_min_mesure), SUM(T.cout_total_ht_travaux)
                    FROM Mesures M
                    JOIN Travaux T ON (M.code_departement = T.code_departement AND strftime('%Y', M.date_mesure) = T.annee_travaux)
                    WHERE M.code_departement = 38 AND strftime('%Y', M.date_mesure) = '2022'
                    GROUP BY M.date_mesure
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
        tabx = []
        for row in result:
            tabx.append(row[0])
            tabmin.append(row[1])

        # Formatage des dates pour l'affichage sur l'axe x
        datetime_dates = [datetime.strptime(date, '%Y-%m-%d') for date in tabx]

        # Ajout de la figure et du subplot qui contiendront le graphique
        fig = Figure(figsize=(10, 6), dpi=100)
        plot1 = fig.add_subplot(111)

        # Affichage des courbes
        plot1.plot(range(len(datetime_dates)), tabmin, color='b', label='temp. min')

        # Configuration de l'axe x pour n'afficher que le premier jour de chaque mois
        xticks = [i for i, date in enumerate(datetime_dates) if date.day == 1]
        xticklabels = [date.strftime('%m-%d') for date in datetime_dates if date.day == 1]
        plot1.set_xticks(xticks)
        plot1.set_xticklabels(xticklabels, rotation=45)
        plot1.legend()

        # Affichage du graphique
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
