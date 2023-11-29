create table Regions (
    code_region INTEGER,
    nom_region TEXT,
    constraint pk_regions primary key (code_region),
    constraint ck_regions check (code_region>=0)
);

create table Departements (
    code_departement TEXT,
    nom_departement TEXT,
    code_region INTEGER,
    zone_climatique TEXT,
    constraint pk_departements primary key (code_departement),
    constraint fk_departements foreign key (code_region) references Regions (code_region),
    constraint ck_departements check (code_departement>=0) --AND (zone_climatique='H1' OR zone_climatique='H2' OR zone_climatique='H3')
);

create table Mesures (
    code_departement TEXT,
    date_mesure DATE,
    temperature_min_mesure FLOAT,
    temperature_max_mesure FLOAT,
    temperature_moy_mesure FLOAT,
    constraint pk_mesures primary key (code_departement, date_mesure),
    constraint fk_mesures foreign key (code_departement) references Departements(code_departement)
);

--TODO Q4 Ajouter les créations des nouvelles tables

create table Communes (
    code_commune INTEGER,
    code_departement INTEGER,
    nom_commune TEXT,
    statut_commune TEXT,
    altitude_moyenne_commune FLOAT,
    superficie_commune FLOAT,
    population_commune FLOAT,
    code_canton_commune INTEGER,
    code_arrondissement_commune INTEGER,
    constraint pk_communes primary key (code_commune, code_departement)
    --constraint fk_communes foreign key (code_departement) references Departements(code_departement),
    --constraint ck_communes check (altitude_moyenne_commune>0 AND superficie_commune>0 AND population_commune>0 AND code_canton_commune>=0 AND code_arrondissement_commune>=0)
);

create table Travaux (
    id_travaux INTEGER PRIMARY KEY AUTOINCREMENT,
    cout_total_ht_travaux FLOAT,
    cout_induit_ht_travaux FLOAT,
    annee_travaux INTEGER,
    type_logement_travaux TEXT,
    annee_construction_logement_travaux INTEGER,
    code_region INTEGER,
    code_departement INTEGER,
    constraint fk1_travaux foreign key (code_region) references Regions (code_region),
    constraint fk2_travaux foreign key (code_departement) references Departements (code_departement)
    --constraint ck_travaux check (id_travaux>=0 AND cout_total_ht_travaux>0 AND cout_induit_ht_travaux>0 AND annee_travaux>=0 AND annee_construction_logement_travaux>=0)
);

create table Isolations (
    id_travaux INTEGER,
    poste_isolation TEXT,
    isolant_isolation TEXT,
    epaisseur_isolation INTEGER,
    surface_isolation FLOAT,
    --constraint pk_isolations primary key (id_travaux),
    constraint fk_isolations foreign key (id_travaux) references Travaux (id_travaux),
    --constraint ck1_isolations check (poste_isolation='COMBLES PERDUES' OR poste_isolation='ITI' OR poste_isolation='ITE' OR
    --poste_isolation='RAMPANTS' OR poste_isolation='SARKING' OR poste_isolation='TOITURE TERRASSE' OR poste_isolation='PLANCHER BAS'),
    --constraint ck2_isolations check (isolant_isolation='AUTRES' OR isolant_isolation='LAINE VEGETALE' OR 
    --isolant_isolation='LAINE MINERALE' OR isolant_isolation='PLASTIQUES'),
    constraint ck_isolations check (epaisseur_isolation>=0 AND surface_isolation>0)
);

create table Chauffages (
    id_travaux INTEGER,
    energie_avt_travaux_chauffage TEXT,
    energie_installee_chauffage TEXT,
    generateur_chauffage TEXT,
    type_chauffage TEXT,
    --constraint pk_chauffages primary key (id_travaux)
    constraint fk_chauffages foreign key (id_travaux) references Travaux (id_travaux)
    --constraint ck1_chauffages check (energie_avt_travaux_chauffage='AUTRES' OR energie_avt_travaux_chauffage='BOIS' OR
    --energie_avt_travaux_chauffage='ELECTRICITE' OR energie_avt_travaux_chauffage='FIOUL' OR energie_avt_travaux_chauffage='GAZ'),
    --constraint ck2_chauffages check (energie_installee_chauffage='AUTRES' OR energie_installee_chauffage='BOIS' OR
    --energie_installee_chauffage='ELECTRICITE' OR energie_installee_chauffage='FIOUL' OR energie_installee_chauffage='GAZ'),
    --constraint ck3_chauffages check (generateur_chauffage='AUTRES' OR generateur_chauffage='CHAUDIERE' OR generateur_chauffage='INSERT' OR
    --generateur_chauffage='PAC' OR generateur_chauffage='POELE' OR generateur_chauffage='RADIATEUR'),
    --constraint ck4_chauffages check (type_chauffage='STANDARD' OR type_chauffage='AIR-EAU' OR type_chauffage='A CONDENSATION' OR
    --type_chauffage='AUTRES' OR type_chauffage='AIR-AIR' OR type_chauffage='GEOTHERMIE' OR type_chauffage='HPE')
);

create table Photovoltaiques (
    id_travaux INTEGER,
    puissance_installee_photovoltaique INTEGER,
    type_panneau_photovoltaique TEXT,
    --constraint pk_photovoltaiques primary key (id_travaux),
    constraint fk_photovoltaiques foreign key (id_travaux) references Travaux (id_travaux)
    --constraint ck_photovoltaiques check (puissance_installee_photovoltaique>=0) --AND (type_panneau_photovoltaique='MONOCRISTALLIN' OR type_panneau_photovoltaique='POLYCRISTALLIN')
);