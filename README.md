# Projet de L3 en CEBD

Heuls Amandine Terese Niels

Projet (Partie 2) :         Mission Climat - Conception

**I/ Implémentation SQLite + Python** *Question 1 (1,5 points) :*

Communes (code\_commune, code\_departement, nom\_commune, statut\_commune, altitude\_moyenne\_commune, superficie\_commune, population\_commune, code\_canton\_commune, code\_arrondissement\_commune)

/\* <cc, cd, n, st, a, su, p, cca, ca> ∈ Communes ⇔ la commune identifiée par le code commune **cc** et le code département **cd** a pour nom **n**, a le statut st, se situe à une altitude de **a** mètres dans le canton identifié par **cca**, dans l’arrondissement identifié par **ca**, possède une superficie de **su** avec une population totale de **p**. \*/

Regions (code\_region, nom\_region)

/\* <cr, n> ∈ Regions ⇔ la région identifiée par le code région **cr** a pour nom **n** \*/

Mesures (date\_mesure, code\_departement, temperature\_min\_mesure, temperature\_max\_mesure, temperature\_moy\_mesure)

/\* <d, cd, tmi, tma, tmo> ∈ Mesures ⇔ la mesure effectuée à la date **d** dans le département **cd** est identifiée par ces derniers, les températures mesurées sont : minimum **tmi**, maximum **tma**, et moyenne **tmo**. \*/

Departements (code\_departement, nom\_departement, code\_region, zone\_climatique\_departement)

/\* <c, n, cr, z> ∈ Departements ⇔ le département identifié par le code **c** a pour nom **n**, se trouvant dans la région identifié par **cr** et la zone climatique **z** \*/

Travaux (id\_travaux, cout\_total\_ht\_travaux, cout\_induit\_ht\_travaux, date\_travaux, type\_logement\_travaux, annee\_construction\_logement\_travaux, code\_region, code\_departement)

/\* <id, ct, ci, dt, t,ac, cr, cd> ∈ Travaux ⇔ les travaux identifiés par **id** ont un coût total hors taxe **ct**, un coût induit hors taxe **ci**, ont été effectués à la date **dt** et concernent un logement de type **t** construit durant l’année **ac** et se situant dans la région de code **cr** et dans le département de code **cd** \*/

**NOTE :** On a remplacé annee\_travaux par date\_travaux afin de pouvoir exécuter la Q6.

Isolations (id\_travaux, poste\_isolation, isolant\_isolation, epaisseur\_isolation, surface\_isolation)

Heuls Amandine Terese Niels

/\* <id, p, is, e, s> ∈ Isolations ⇔ l'isolation identifiée par l'identifiant travaux **id** a été effectuée au poste d’isolation **p**, l’épaisseur d’isolation est de **e** cm pour une surface de **s** m2 \*/

Chauffages (id\_travaux, energie\_avt\_travaux\_chauffage, energie\_installee\_chauffage, generateur\_chauffage, type\_chauffage)

/\* <id, ea, ei, g, t> ∈ Chauffages ⇔ le chauffage identifié par l’identifiant travaux **id**, ayant permis de remplacer l’ancien chauffage d’énergie **ea** par un chauffage d’énergie **ei**. Le nouveau chauffage est un générateur **g** du type **t**. \*/

Photovoltaiques (id\_travaux, puissance\_installee\_photovoltaique, type\_panneau\_photovoltaique)

/\* <id, p, t> ∈ Photovoltaiques ⇔ le système photovoltaïque identifié par l’identifiant travaux **id** possède une puissance **p** et comporte des panneaux solaires du type **t**. \*/

Contraintes d’intégrité référentielles :

Communes[code\_departement] ⊆ Departements[code\_departement] Mesures[code\_departement] ⊆ Departements[code\_departement] Departements[code\_region] ⊆ Regions[code\_region] Travaux[code\_region] ⊆ Regions[code\_region] Travaux[code\_departement] ⊆ Departements[code\_departement] Isolations[id\_travaux] ⊆ Travaux[id\_travaux]

Chauffages[id\_travaux] ⊆ Travaux[id\_travaux] Photovoltaïque[id\_travaux] ⊆ Travaux[id\_travaux]

Contraintes de domaine :

domaine(code\_commune) = domaine(code\_departement) = domaine(code\_canton\_commune) = domaine(code\_arrondissement\_commune) = domaine(code\_region) = domaine(id\_travaux) = domaine(annee\_construction\_logement\_travaux) = domaine(epaisseur\_isolation) = domaine(puissance\_installee\_photovoltaique) =

entiers >= 0

domaine(superficie\_commune) = domaine(altitude\_moyenne\_commune) = domaine(cout\_total\_ht\_travaux) = domaine(cout\_induit\_ht\_travaux) = domaine(surface\_isolation) = domaine(population\_commune) = réels > 0

domaine(temperature\_min\_mesure) = domaine(temperature\_max\_mesure) = domaine(temperature\_moy\_mesure) = réels

domaine(nom\_commune) = domaine(nom\_region) = domaine(nom\_departement) = domaine(zone\_climatique\_departement) = domaine(type\_logement\_travaux) =
domaine(poste\_isolation) = domaine(isolant\_isolation) = domaine(energie\_avt\_travaux\_chauffage) = domaine(energie\_installee\_chauffage) = domaine(generateur\_chauffage) = domaine(type\_chauffage) = domaine(type\_panneau\_photovoltaique) = domaine(statut\_commune) = chaînes de caractères

domaine(date\_mesure) = domaine(date\_travaux) = date 

*Question 2 (14 point) :*

**NOTE :** Pour la Q6, on a remplacé 2022 par 2018 car il n’y a pas eu de travaux en 2022 dans la base de données. On a également remplacé l’Isère par le Loiret pour avoir davantage de données.

**NOTE :** Pour l’insertion des données, on obtient des FOREIGN KEY failed dûs à l’insertion des données NULL.
