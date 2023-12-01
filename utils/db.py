import sqlite3
from sqlite3 import IntegrityError
import pandas

# Pointeur sur la base de données
data = sqlite3.connect("data/climat_france.db")
data.execute("PRAGMA foreign_keys = 1")

# Fonction permettant d'exécuter toutes les requêtes sql d'un fichier
# Elles doivent être séparées par un point-virgule
def updateDBfile(data:sqlite3.Connection, file):

    # Lecture du fichier et placement des requêtes dans un tableau
    createFile = open(file, 'r')
    createSql = createFile.read()
    createFile.close()
    sqlQueries = createSql.split(";")

    # Exécution de toutes les requêtes du tableau
    cursor = data.cursor()
    for query in sqlQueries:
        cursor.execute(query)

# Action en cas de clic sur le bouton de création de base de données
def createDB():
    try:
        # On exécute les requêtes du fichier de création
        updateDBfile(data, "data/createDB.sql")
    except Exception as e:
        print ("L'erreur suivante s'est produite lors de la création de la base : " + repr(e) + ".")
    else:
        data.commit()
        print("Base de données créée avec succès.")

# En cas de clic sur le bouton d'insertion de données
#TODO Q4 Modifier la fonction insertDB pour insérer les données dans les nouvelles tables
def insertDB():
    try:
        # '{}' : paramètre de la requête qui doit être interprété comme une chaine de caractères dans l'insert
        # {}   : paramètre de la requête qui doit être interprété comme un nombre dans l'insert
        # la liste de noms en 3e argument de read_csv_file correspond aux noms des colonnes dans le CSV
        # ATTENTION : les attributs dans la BD sont généralement différents des noms de colonnes dans le CSV
        # Exemple : date_mesure dans la BD et date_obs dans le CSV

        # On ajoute les anciennes régions
        read_csv_file(
            "data/csv/Communes.csv", ';',
            "insert into Regions values ({},'{}')",
            ['Code Région', 'Région']
        )

        # On ajoute les nouvelles régions
        read_csv_file(
            "data/csv/AnciennesNouvellesRegions.csv", ';',
            "insert into Regions values ({},'{}')",
            ['Nouveau Code', 'Nom Officiel Région Majuscule']
        )

        # On ajoute les départements référencés avec les anciennes régions
        read_csv_file(
            "data/csv/Communes.csv", ';',
            "insert into Departements values ('{}','{}', {},'')",
            ['Code Département', 'Département', 'Code Région']
        )

        # On renseigne la zone climatique des départements
        read_csv_file(
            "data/csv/ZonesClimatiques.csv", ';',
            "update Departements set zone_climatique = '{}' where code_departement = '{}'",
            ['zone_climatique', 'code_departement']
        )

        # On modifie les codes région des départements pour les codes des nouvelles régions
        read_csv_file(
            "data/csv/AnciennesNouvellesRegions.csv", ';',
            "update Departements set code_region = {} where code_region = {}",
            ['Nouveau Code', 'Anciens Code']
        )

        # On supprime les anciennes régions, sauf si l'ancien code et le nouveau sont identiques (pour ne pas perdre les régions qui n'ont pas changé de code)
        read_csv_file(
            "data/csv/AnciennesNouvellesRegions.csv", ';',
            "delete from Regions where code_region = {} and {} <> {}",
            ['Anciens Code', 'Anciens Code', 'Nouveau Code']
        )
        print("Les erreurs UNIQUE constraint sont normales car on insère une seule fois les Regions et les Départements")
        print("Insertion de mesures en cours...cela peut prendre un peu de temps")

        # On ajoute les mesures
        read_csv_file(
             "data/csv/Mesures.csv", ';',
             "insert into Mesures values ('{}','{}', {}, {}, {})",
             ['code_insee_departement', 'date_obs', 'tmin', 'tmax', 'tmoy']
        )

        # On ajoute les communes
        read_csv_file(
             "data/csv/Communes.csv", ';',
             "insert into Communes values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')",
             ['Code Commune', 'Code Département', 'Commune', 'Statut', 'Altitude Moyenne', 'Superficie', 'Population', 'Code Canton', 'Code Arrondissement']
        )

        # On ajoute les travaux
        query_travaux = "insert into Travaux values (NULL, '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
        columns_travaux = ['cout_total_ht', 'cout_induit_ht', 'date_x', 'type_logement', 'annee_construction',
                           'code_region', 'code_departement']

        # Isolations
        query_isolations = "insert into Isolations values ('{}', '{}', '{}', '{}', '{}')"
        columns_isolations = ['poste_isolation', 'isolant', 'epaisseur', 'surface']
        insert_data("data/csv/Isolation.csv", query_travaux, columns_travaux, query_isolations, columns_isolations)

        # Chauffages
        query_chauffages = "insert into Chauffages values ('{}', '{}', '{}', '{}', '{}')"
        columns_chauffages = ['energie_chauffage_avt_travaux', 'energie_chauffage_installee', 'generateur',
                             'type_chaudiere']
        insert_data("data/csv/Chauffage.csv", query_travaux, columns_travaux, query_chauffages, columns_chauffages)

        # Photovoltaiques
        query_photovoltaiques = "insert into Photovoltaiques values ('{}', '{}', '{}')"
        columns_photovoltaiques = ['puissance_installee', 'type_panneaux']
        insert_data("data/csv/Photovoltaique.csv", query_travaux, columns_travaux, query_photovoltaiques, columns_photovoltaiques)

    except Exception as e:
        print ("L'erreur suivante s'est produite lors de l'insertion des données : " + repr(e) + ".")
    else:
        data.commit()
        # Modification du format de date pour Travaux
        cursor = data.cursor()
        cursor.execute("""
            UPDATE Travaux
            SET date_travaux = strftime('%Y-%m-%d', date(substr(date_travaux, 7, 4) || '-' || substr(date_travaux, 4, 2) || '-' || substr(date_travaux, 1, 2)));
        """)
        data.commit()
        print("Un jeu de test a été inséré dans la base avec succès.")

# En cas de clic sur le bouton de suppression de la base
def deleteDB():
    try:
        updateDBfile(data, "data/deleteDB.sql")
    except Exception as e:
        print ("L'erreur suivante s'est produite lors de la destruction de la base : " + repr(e) + ".")
    else:
        data.commit()
        print("La base de données a été supprimée avec succès.")

def read_csv_file(csvFile, separator, query, columns):
    # Lecture du fichier CSV csvFile avec le séparateur separator
    # pour chaque ligne, exécution de query en la formatant avec les colonnes columns
    df = pandas.read_csv(csvFile, sep=separator)
    df = df.where(pandas.notnull(df), 'null')

    cursor = data.cursor()
    for ix, row in df.iterrows():
        try:
            tab = []
            for i in range(len(columns)):
                # pour échapper les noms avec des apostrophes, on remplace dans les chaines les ' par ''
                if isinstance(row[columns[i]], str):
                    row[columns[i]] = row[columns[i]].replace("'","''")
                tab.append(row[columns[i]])

            formatedQuery = query.format(*tab)

            # On affiche la requête pour comprendre la construction ou débugger !
            #print(formatedQuery)

            cursor.execute(formatedQuery)
        except IntegrityError as err:
            print(err)

def insert_data(csvFile, query_travaux, columns_travaux, query_specific, columns_specific, verbose=False):
    separator = ";"

    df = pandas.read_csv(csvFile, sep=separator)
    df = df.where(pandas.notnull(df), 'null')
    cursor = data.cursor()
    for ix, row in df.iterrows():
        try:
            # Insert into Travaux
            tab_travaux = []
            for i in range(len(columns_travaux)):
                if isinstance(row[columns_travaux[i]], str):
                    row[columns_travaux[i]] = row[columns_travaux[i]].replace("'", "''")
                tab_travaux.append(row[columns_travaux[i]])

            formated_query_travaux = query_travaux.format(*tab_travaux)
            if verbose:
                print(formated_query_travaux)
            cursor.execute(formated_query_travaux)
            last_id = cursor.lastrowid

            # Insert with last_id into specific table
            tab_specific = []
            for i in range(len(columns_specific)):
                if isinstance(row[columns_specific[i]], str):
                    row[columns_specific[i]] = row[columns_specific[i]].replace("'", "''")
                tab_specific.append(row[columns_specific[i]])

            formated_query_specific = query_specific.format(last_id, *tab_specific)
            if verbose:
                print(formated_query_specific)
            cursor.execute(formated_query_specific)

        except IntegrityError as err:
            print(err)