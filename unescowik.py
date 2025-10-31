"""
================================================================================
BUT Science des Données - Semestre 3
SAÉ VCOD - Collecte de données Web

Projet : Scraping des sites UNESCO en France
Auteur : Gabriel Sagot
Date : Octobre 2025

Description :
Ce script récupère la liste des sites du patrimoine mondial UNESCO en France
depuis Wikipedia, extrait leurs coordonnées géographiques, et produit des
visualisations (graphiques et carte interactive).
================================================================================
"""

# ============================================================================
# IMPORTS DES LIBRAIRIES
# ============================================================================
import requests    # Bibliothèque pour faire des requêtes HTTP (communiquer avec des sites web)

from bs4 import BeautifulSoup   #B ibliothèque de parsing HTML (analyse et extraction de données)

import pandas as pd  # Bibliothèque de manipulation de données (DataFrames)

import matplotlib.pyplot as plt  

import folium  # Bibliothèque de cartographie interactive (cartes web)

import re # Bibliothèque de regex (expressions régulières - recherche de motifs dans du texte)

import webbrowser

import os # Bibliothèque pour interagir avec le système d'exploitation (fichiers, chemins)

# ============================================================================
# CONFIGURATION GLOBALE
# ============================================================================
URL_WIKIPEDIA = "https://fr.wikipedia.org/wiki/Liste_du_patrimoine_mondial_en_France"

# En-têtes HTTP pour simuler un navigateur (évite certains blocages)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}


# ============================================================================
# FONCTIONS DE SCRAPING
# ============================================================================

# Fonction pour se connecter à Wikipedia et récupérer le HTML de la page
def se_connecter_au_site(url, headers):
    """
    Étape 1 : Se connecter à la page Wikipedia et obtenir le code source HTML
    
    Paramètres :
        url (str) : URL de la page à scraper
        headers (dict) : En-têtes HTTP pour la requête
    
    Retourne :
        BeautifulSoup : Objet soup contenant le code HTML parsé
        None : Si une erreur se produit
    """
    try:
        # === CONNEXION ET RÉCUPÉRATION DE LA PAGE === Si erreur, on passe aux "exept" plus bas
        
        print("📡 Tentative de connexion au site Wikipedia...")
        
        # Envoi de la requête HTTP GET vers l'URL avec un délai max de 10 secondes
        response = requests.get(url, headers=headers, timeout=10)
        
        # Force l'encodage UTF-8 pour gérer les accents français
        response.encoding = 'utf-8'
        
        # === VÉRIFICATION DE LA RÉPONSE ===
        
        # Code 200 = succès, sinon erreur (404, 403, etc.)
        if response.status_code == 200:
            print("✓ Connexion réussie\n")
            
            # Parse le HTML brut en objet BeautifulSoup manipulable
            soup = BeautifulSoup(response.text, "html.parser")
            return soup
        else:
            # Affiche le code d'erreur HTTP (ex: 404, 403)
            print(f"✗ Erreur HTTP {response.status_code}\n")
            return None
    
    # === GESTION DES ERREURS ===
    
    # Serveur trop lent (> 10 secondes)
    except requests.exceptions.Timeout:
        print("✗ Erreur : Timeout - Le serveur met trop de temps à répondre\n")
        return None
    
    # Impossible de joindre le serveur (pas d'internet, URL invalide)
    except requests.exceptions.ConnectionError:
        print("✗ Erreur : Impossible de se connecter au site\n")
        return None
    
    # Toutes les autres erreurs imprévues
    except Exception as e:
        print(f"✗ Erreur inattendue lors de la connexion : {e}\n")
        return None

# Fonction pour trouver et extraire le tableau contenant la liste des sites UNESCO
def extraire_tableau_sites(soup):
    """
    Étape 2 : Extraire le tableau contenant les sites UNESCO
    
    Paramètres :
        soup (BeautifulSoup) : Objet contenant le HTML parsé
    
    Retourne :
        Tag : Élément <table> contenant les sites
        None : Si le tableau n'est pas trouvé
    """
    try:
        # === RECHERCHE DU TABLEAU ===
        
        print("🔍 Recherche du tableau des sites UNESCO...")
        
        # find_all cherche TOUTES les balises <table> ayant class="wikitable"
        # Retourne une liste d'éléments (ex: [table1, table2, table3])
        tableaux = soup.find_all('table', {'class': 'wikitable'})
        
        # === SÉLECTION DU BON TABLEAU ===
        
        # Vérifie qu'il y a au moins 2 tableaux sur la page
        if len(tableaux) >= 2:
            
            # Index 1 = 2ème tableau (index 0 serait le 1er tableau)
            # Sur Wikipedia, le 2ème tableau contient la liste des sites
            tableau_sites = tableaux[1]
            
            # Compte le nombre de lignes <tr> (moins 1 car la 1ère ligne = en-tête)
            print(f"✓ Tableau trouvé ({len(tableau_sites.find_all('tr'))-1} lignes)\n")
            
            # Retourne l'élément <table> pour l'utiliser ensuite
            return tableau_sites
        else:
            # Pas assez de tableaux trouvés
            print("✗ Tableau non trouvé\n")
            return None
    
    # === GESTION DES ERREURS ===
    
    # Attrape toute erreur (ex: soup est None, problème d'attribut)
    except Exception as e:
        print(f"✗ Erreur lors de l'extraction du tableau : {e}\n")
        return None

# Fonction pour parcourir le tableau et extraire toutes les données de chaque site
def extraire_donnees_sites(tableau):
    """
    Étape 3 : Extraire les données de chaque site depuis le tableau
    
    Cette fonction parcourt chaque ligne du tableau et extrait :
    - Le nom du site
    - La région
    - L'année d'inscription
    - Le type (Culturel/Naturel/Mixte)
    - Les coordonnées géographiques
    
    Paramètres :
        tableau (Tag) : Élément <table> contenant les sites
    
    Retourne :
        dict : Dictionnaire contenant 5 listes (sites, regions, types, annees, coordonnees)
    """
    print("📊 Extraction des données de chaque site...")
    
    # Initialisation des listes 
    sites = []
    regions = []
    types_sites = []
    annees = []
    coordonnees = []
    
    try:
        # Parcours de toutes les lignes du tableau (sauf la première = en-tête)
        # Utilisation de find_all comme dans le cours
        lignes = tableau.find_all('tr')[1:]
        
        for ligne in lignes:
            # On cherche toutes les cellules <td> de la ligne
            cellules = ligne.find_all('td')
            
            # Vérification qu'on a bien assez de cellules
            if len(cellules) >= 6:
                
                # --- EXTRACTION DU NOM DU SITE ---
                # find avec class comme dans le cours, puis .text.strip()
                site_nom = cellules[0].get_text(strip=True)
                
                # --- EXTRACTION DE LA RÉGION ---
                region = cellules[1].get_text(strip=True)
                
                # --- EXTRACTION DE L'ANNÉE ---
                annee_texte = cellules[2].get_text(strip=True)
                # Recherche d'un nombre à 4 chiffres (année)
                annee_trouvee = re.findall(r'\d{4}', annee_texte)
                if annee_trouvee:
                    annee = int(annee_trouvee[0])
                else:
                    annee = None
                
                # --- EXTRACTION DU TYPE ---
                type_texte = cellules[4].get_text(strip=True)
                if 'Naturel' in type_texte:
                    type_site = 'Naturel'
                elif 'Mixte' in type_texte:
                    type_site = 'Mixte'
                else:
                    type_site = 'Culturel'
                
                # --- EXTRACTION DES COORDONNÉES ---
                # On cherche d'abord un lien avec la classe 'external text'
                lien_coords = cellules[5].find('a', {'class': 'external text'})
                if lien_coords:
                    coords_texte = lien_coords.get_text(strip=True)
                else:
                    # Sinon on prend le texte brut de la cellule
                    coords_texte = cellules[5].get_text(strip=True)
                
                # Ajout dans les listes
                sites.append(site_nom)
                regions.append(region)
                types_sites.append(type_site)
                annees.append(annee)
                coordonnees.append(coords_texte)
        
        print(f"✓ {len(sites)} sites extraits avec succès\n")
        
        # Retour d'un dictionnaire pour faciliter la création du DataFrame
        return {
            'Site': sites,
            'Region': regions,
            'Type': types_sites,
            'Annee': annees,
            'Coordonnees_brutes': coordonnees
        }
        
    except Exception as e:
        print(f"✗ Erreur lors de l'extraction des données : {e}\n")
        return None


# ============================================================================
# FONCTIONS DE CONVERSION DES COORDONNÉES
# ============================================================================

# Fonction utilitaire pour convertir des coordonnées DMS (Degrés/Minutes/Secondes) en DD (Degrés Décimaux)
def dms2dd(degrees, minutes, seconds, direction):
    """
    Convertit des coordonnées DMS (Degrés, Minutes, Secondes) en DD (Degrés Décimaux)
    
    Fonction fournie dans le cours (exercice 6.2)
    
    Paramètres :
        degrees (str/float) : Degrés
        minutes (str/float) : Minutes
        seconds (str/float) : Secondes
        direction (str) : Direction (N/S/E/O)
    
    Retourne :
        float : Coordonnée en degrés décimaux
    """
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    
    # Si direction Sud ou Ouest, la coordonnée est négative
    if direction in ('S', 'O', 'W', 'sud', 'ouest'):
        dd *= -1
    
    return dd


# Fonction pour analyser et convertir différents formats de coordonnées GPS
def parse_coordonnees(coord_string):
    """
    Analyse une chaîne de coordonnées et la convertit en latitude/longitude décimales
    
    Gère différents formats :
    - Format DMS : "48° 51′ 29″ N, 2° 17′ 40″ E"
    - Format décimal : "48.858, 2.294"
    
    Paramètres :
        coord_string (str) : Chaîne contenant les coordonnées
    
    Retourne :
        tuple : (latitude, longitude) ou (None, None) si échec
    """
    # Vérification que la chaîne n'est pas vide
    if not coord_string or coord_string.strip() == '':
        return None, None
    
    try:
        # --- FORMAT AVEC VIRGULE (séparation lat/lon) ---
        if ',' in coord_string:
            parties = coord_string.split(',')
            
            if len(parties) == 2:
                partie_lat = parties[0].strip()
                partie_lon = parties[1].strip()
                
                # LATITUDE : Recherche du format DMS
                match_lat = re.findall(
                    r'(\d+)[°\s]+(\d+)[′\'\s]+(\d+)[″"\s]+([NSEO])',
                    partie_lat,
                    re.IGNORECASE
                )
                
                if match_lat:
                    lat_deg, lat_min, lat_sec, lat_dir = match_lat[0]
                    latitude = dms2dd(lat_deg, lat_min, lat_sec, lat_dir)
                else:
                    # Tentative format décimal
                    lat_decimal = re.findall(r'([-]?\d+\.?\d*)', partie_lat)
                    if lat_decimal:
                        latitude = float(lat_decimal[0])
                    else:
                        return None, None
                
                # LONGITUDE : Recherche du format DMS
                match_lon = re.findall(
                    r'(\d+)[°\s]+(\d+)[′\'\s]+(\d+)[″"\s]+([NSEO])',
                    partie_lon,
                    re.IGNORECASE
                )
                
                if match_lon:
                    lon_deg, lon_min, lon_sec, lon_dir = match_lon[0]
                    longitude = dms2dd(lon_deg, lon_min, lon_sec, lon_dir)
                else:
                    # Tentative format décimal
                    lon_decimal = re.findall(r'([-]?\d+\.?\d*)', partie_lon)
                    if lon_decimal:
                        longitude = float(lon_decimal[0])
                    else:
                        return None, None
                
                return latitude, longitude
        
        # --- FORMAT DÉCIMAL DIRECT ---
        decimales = re.findall(r'([-]?\d+\.?\d+)', coord_string)
        if len(decimales) >= 2:
            return float(decimales[0]), float(decimales[1])
        
    except Exception as e:
        # Gestion des erreurs silencieuse pour ne pas polluer la sortie
        return None, None
    
    return None, None


# Fonction pour convertir les coordonnées brutes de tous les sites du DataFrame
def convertir_toutes_coordonnees(dataframe):
    """
    Convertit toutes les coordonnées brutes du DataFrame en latitude/longitude
    
    Paramètres :
        dataframe (DataFrame) : DataFrame contenant une colonne 'Coordonnees_brutes'
    
    Retourne :
        DataFrame : DataFrame avec 2 nouvelles colonnes 'Latitude' et 'Longitude'
    """
    print("🗺️  Conversion des coordonnées géographiques...")
    
    latitudes = []
    longitudes = []
    erreurs = 0
    
    try:
        # Parcours de chaque ligne du DataFrame
        for index, row in dataframe.iterrows():
            coord_brute = row['Coordonnees_brutes']
            
            # Appel de la fonction de parsing
            lat, lon = parse_coordonnees(coord_brute)
            
            latitudes.append(lat)
            longitudes.append(lon)
            
            if lat is None or lon is None:
                erreurs += 1
        
        # Ajout des colonnes au DataFrame
        dataframe['Latitude'] = latitudes
        dataframe['Longitude'] = longitudes
        
        nb_ok = len(dataframe) - erreurs
        print(f"✓ {nb_ok} sites avec coordonnées valides")
        
        if erreurs > 0:
            print(f"⚠️  {erreurs} sites sans coordonnées\n")
        else:
            print()
        
        return dataframe
        
    except Exception as e:
        print(f"✗ Erreur lors de la conversion : {e}\n")
        return dataframe


# Fonction pour ajouter manuellement les coordonnées GPS des sites qui n'en ont pas
def corriger_coordonnees_manquantes(dataframe):
    """
    Corrige manuellement les coordonnées manquantes pour certains sites
    
    Note : Certains sites UNESCO sont "en série" (plusieurs lieux).
    On utilise un point représentatif pour la visualisation.
    
    Paramètres :
        dataframe (DataFrame) : DataFrame avec coordonnées
    
    Retourne :
        DataFrame : DataFrame avec coordonnées corrigées
    """
    print("🔧 Correction des coordonnées manquantes...")
    
    try:
        nb_avant = dataframe['Latitude'].isna().sum()
        
        # Exemple : Sites des mémoriaux de la Première Guerre mondiale
        # On utilise Notre-Dame-de-Lorette comme point représentatif
        dataframe.loc[dataframe['Latitude'].isna(), 'Latitude'] = 50.40
        dataframe.loc[dataframe['Longitude'].isna(), 'Longitude'] = 2.71
        
        nb_apres = dataframe['Latitude'].isna().sum()
        nb_corriges = nb_avant - nb_apres
        
        if nb_corriges > 0:
            print(f"✓ {nb_corriges} coordonnées corrigées\n")
        else:
            print("✓ Aucune correction nécessaire\n")
        
        return dataframe
        
    except Exception as e:
        print(f"⚠️  Erreur lors de la correction : {e}\n")
        return dataframe


# ============================================================================
# FONCTIONS DE VISUALISATION - GRAPHIQUES
# ============================================================================

# Fonction pour créer un graphique des 10 régions avec le plus de sites UNESCO
def creer_graphique_regions(dataframe):
    """
    Crée un graphique en barres horizontales du top 10 des régions
    
    Paramètres :
        dataframe (DataFrame) : DataFrame contenant une colonne 'Region'
    """
    try:
        print("📊 Création du graphique des régions...")
        
        plt.figure(figsize=(12, 8))
        
        # Comptage et tri des régions (top 10)
        top_regions = dataframe['Region'].value_counts().head(10).sort_values()
        
        # Création du graphique en barres horizontales
        top_regions.plot(kind='barh', color='#2E86AB')
        
        plt.title('Top 10 des régions - Sites UNESCO en France', 
                  fontsize=15, fontweight='bold')
        plt.xlabel('Nombre de sites', fontsize=12)
        plt.ylabel('Région', fontsize=12)
        plt.tight_layout()
        plt.show()
        
        print("✓ Graphique des régions affiché\n")
        
    except Exception as e:
        print(f"✗ Erreur lors de la création du graphique : {e}\n")


# Fonction pour créer un graphique des inscriptions UNESCO par décennie
def creer_graphique_decennies(dataframe):
    """
    Crée un graphique en barres des inscriptions par décennie
    
    Paramètres :
        dataframe (DataFrame) : DataFrame contenant une colonne 'Annee'
    """
    try:
        print("📊 Création du graphique par décennie...")
        
        # On ne garde que les lignes avec une année valide
        df_avec_annee = dataframe.dropna(subset=['Annee']).copy()
        
        # Calcul de la décennie (ex: 1998 → 1990)
        df_avec_annee['Decennie'] = (df_avec_annee['Annee'] // 10 * 10).astype(int)
        
        plt.figure(figsize=(12, 6))
        
        # Comptage par décennie
        comptage_decennies = df_avec_annee['Decennie'].value_counts().sort_index()
        comptage_decennies.plot(kind='bar', color='#A23B72')
        
        plt.title('Inscriptions au patrimoine UNESCO par décennie', 
                  fontsize=15, fontweight='bold')
        plt.xlabel('Décennie', fontsize=12)
        plt.ylabel('Nombre de sites inscrits', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
        print("✓ Graphique des décennies affiché\n")
        
    except Exception as e:
        print(f"✗ Erreur lors de la création du graphique : {e}\n")


# Fonction pour créer un graphique montrant la répartition Culturel/Naturel/Mixte
def creer_graphique_types(dataframe):
    """
    Crée un graphique en barres des types de sites
    
    Paramètres :
        dataframe (DataFrame) : DataFrame contenant une colonne 'Type'
    """
    try:
        print("📊 Création du graphique des types...")
        
        plt.figure(figsize=(9, 6))
        
        # Comptage par type
        comptage_types = dataframe['Type'].value_counts()
        comptage_types.plot(kind='bar', 
                           color=['#F18F01', '#006466', '#C73E1D'])
        
        plt.title('Répartition des sites UNESCO par type', 
                  fontsize=15, fontweight='bold')
        plt.xlabel('Type de site', fontsize=12)
        plt.ylabel('Nombre de sites', fontsize=12)
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.show()
        
        print("✓ Graphique des types affiché\n")
        
    except Exception as e:
        print(f"✗ Erreur lors de la création du graphique : {e}\n")


# ============================================================================
# FONCTION DE VISUALISATION - CARTE FOLIUM
# ============================================================================

# Fonction pour créer une carte interactive Folium avec marqueurs pour chaque site UNESCO
def creer_carte_interactive(dataframe, nom_fichier='carte_unesco_france.html'):
    """
    Crée une carte interactive avec Folium montrant tous les sites UNESCO
    
    Inspiré de l'exercice 6.2 du cours
    
    Paramètres :
        dataframe (DataFrame) : DataFrame avec colonnes Latitude, Longitude, Site, Type
        nom_fichier (str) : Nom du fichier HTML à générer
    """
    try:
        print("🗺️  Création de la carte interactive Folium...")
        
        # On ne garde que les sites avec coordonnées valides
        df_carte = dataframe.dropna(subset=['Latitude', 'Longitude']).copy()
        
        # Création de la carte centrée sur la France
        # tiles='Stamen Toner' comme dans le cours (exercice 6.2)
        carte = folium.Map(
            location=[47, 2],      # Centre de la France
            zoom_start=6,
            tiles='OpenStreetMap'  # Ou 'Stamen Toner' si disponible
        )
        
        # Dictionnaire de couleurs par type
        couleurs = {
            'Culturel': 'blue',
            'Naturel': 'green',
            'Mixte': 'orange'
        }
        
        # Ajout d'un marqueur pour chaque site
        for index, row in df_carte.iterrows():
            
            # Détermination de la couleur selon le type
            couleur = couleurs.get(row['Type'], 'gray')
            
            # Création du contenu de la popup
            popup_html = f"""
            <div style="font-family: Arial; width: 200px;">
                <b>{row['Site']}</b><br>
                📍 {row['Region']}<br>
                📅 {int(row['Annee']) if pd.notna(row['Annee']) else 'N/A'}<br>
                🏛️ {row['Type']}
            </div>
            """
            
            # Ajout du marqueur (cf cours)
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color=couleur, icon='info-sign')
            ).add_to(carte)
        
        # Sauvegarde de la carte
        carte.save(nom_fichier)
        print(f"✓ Carte sauvegardée : {nom_fichier}")
        
        # Ouverture automatique dans le navigateur (comme dans le cours)
        webbrowser.open_new_tab(nom_fichier)
        print(f"✓ Carte ouverte dans le navigateur\n")
        
    except Exception as e:
        print(f"✗ Erreur lors de la création de la carte : {e}\n")


# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

# Fonction principale qui orchestre toutes les étapes du scraping et de la visualisation
def main():
    """
    Fonction principale orchestrant toutes les étapes du projet
    
    Étapes :
    1. Connexion et scraping du site Wikipedia
    2. Extraction des données dans un DataFrame
    3. Conversion des coordonnées géographiques
    4. Création des visualisations (graphiques + carte)
    """
    print("="*80)
    print(" PROJET SAÉ VCOD - SCRAPING DES SITES UNESCO EN FRANCE")
    print("="*80)
    print()
    
    # --- ÉTAPE 1 : CONNEXION AU SITE ---
    soup = se_connecter_au_site(URL_WIKIPEDIA, HEADERS)
    
    if soup is None:
        print("❌ Impossible de continuer sans connexion")
        return
    
    # --- ÉTAPE 2 : EXTRACTION DU TABLEAU ---
    tableau = extraire_tableau_sites(soup)
    
    if tableau is None:
        print("❌ Impossible de continuer sans le tableau")
        return
    
    # --- ÉTAPE 3 : EXTRACTION DES DONNÉES ---
    donnees = extraire_donnees_sites(tableau)
    
    if donnees is None:
        print("❌ Impossible de continuer sans données")
        return
    
    # --- ÉTAPE 4 : CRÉATION DU DATAFRAME ---
    print("📋 Création du DataFrame pandas...")
    df = pd.DataFrame(donnees)
    print(f"✓ DataFrame créé : {len(df)} lignes × {len(df.columns)} colonnes\n")
    
    # Affichage d'un aperçu
    print("Aperçu des 3 premières lignes :")
    print(df.head(3))
    print()
    
    # --- ÉTAPE 5 : CONVERSION DES COORDONNÉES ---
    df = convertir_toutes_coordonnees(df)
    df = corriger_coordonnees_manquantes(df)
    
    # --- ÉTAPE 6 : CRÉATION DES GRAPHIQUES ---
    print("="*80)
    print(" VISUALISATIONS - GRAPHIQUES")
    print("="*80)
    print()
    
    creer_graphique_regions(df)
    creer_graphique_decennies(df)
    creer_graphique_types(df)
    
    # --- ÉTAPE 7 : CRÉATION DE LA CARTE ---
    print("="*80)
    print(" VISUALISATION - CARTE INTERACTIVE")
    print("="*80)
    print()
    
    creer_carte_interactive(df)
    
    # --- FIN ---
    print("="*80)
    print(" ✅ PROJET TERMINÉ AVEC SUCCÈS")
    print("="*80)
    print()
    print(f"📊 Statistiques finales :")
    print(f"   • {len(df)} sites UNESCO en France")
    print(f"   • {df['Latitude'].notna().sum()} sites géolocalisés")
    print(f"   • {len(df['Region'].unique())} régions représentées")
    print(f"   • {len(df['Type'].unique())} types de sites")
    print()


# ============================================================================
# POINT D'ENTRÉE DU PROGRAMME
# ============================================================================

if __name__ == "__main__":
    """
    Point d'entrée : ce bloc s'exécute uniquement si le script est lancé directement
    (pas si importé comme module)
    """
    main()

## ============================================================================
# FONCTION DE VISUALISATION - CARTE INTERACTIVE AVANCÉE
# ============================================================================

# Fonction pour vérifier si des coordonnées GPS sont situées en France (métropole ou DOM-TOM)
def verifier_coordonnees_france(latitude, longitude):
    """
    Vérifie si des coordonnées GPS sont situées en France (métropole ou DOM-TOM)
    
    Zones géographiques couvertes :
    - France métropolitaine : 41°-51° N, -5°-10° E
    - La Réunion : -25° à -20° N, 55°-60° E
    - Guadeloupe/Martinique : 14°-18° N, -63° à -60° E
    - Nouvelle-Calédonie : -23° à -21° N, 164°-168° E
    - Polynésie française : -18° à -8° N, -141° à -138° E
    - TAAF : -50° à -37° N, 50°-78° E
    
    Paramètres :
        latitude (float) : Latitude en degrés décimaux
        longitude (float) : Longitude en degrés décimaux
    
    Retourne :
        bool : True si les coordonnées sont en France, False sinon
    """
    try:
        # Vérification France métropolitaine
        if 41 <= latitude <= 51 and -5 <= longitude <= 10:
            return True
        
        # Vérification La Réunion
        if -25 <= latitude <= -20 and 55 <= longitude <= 60:
            return True
        
        # Vérification Guadeloupe/Martinique
        if 14 <= latitude <= 18 and -63 <= longitude <= -60:
            return True
        
        # Vérification Nouvelle-Calédonie
        if -23 <= latitude <= -21 and 164 <= longitude <= 168:
            return True
        
        # Vérification Polynésie française
        if -18 <= latitude <= -8 and -141 <= longitude <= -138:
            return True
        
        # Vérification TAAF (Terres australes et antarctiques françaises)
        if -50 <= latitude <= -37 and 50 <= longitude <= 78:
            return True
        
        return False
        
    except Exception as e:
        print(f"⚠️  Erreur lors de la vérification des coordonnées : {e}")
        return False


# Fonction pour obtenir la couleur et l'icône associées à un type de site
def obtenir_configuration_type(type_site):
    """
    Retourne la configuration visuelle (couleur et icône) pour un type de site
    
    Paramètres :
        type_site (str) : Type du site ('Culturel', 'Naturel', ou 'Mixte')
    
    Retourne :
        dict : Dictionnaire avec 'color' et 'icon'
    """
    # Configuration des couleurs et icônes par type de site
    configurations = {
        'Culturel': {
            'color': '#3498db',      # Bleu
            'icon': 'fa-landmark'    # Icône monument
        },
        'Naturel': {
            'color': '#27ae60',      # Vert
            'icon': 'fa-tree'        # Icône arbre
        },
        'Mixte': {
            'color': '#e67e22',      # Orange
            'icon': 'fa-mountain-sun' # Icône montagne/soleil
        }
    }
    
    # Retour de la config ou config par défaut si type inconnu
    return configurations.get(type_site, {
        'color': '#95a5a6',       # Gris
        'icon': 'fa-map-marker'   # Marqueur standard
    })


# Fonction pour générer le contenu HTML stylé d'une popup de marqueur sur la carte
def creer_popup_html(row, config_couleur):
    """
    Crée le contenu HTML stylé pour la popup d'un marqueur
    
    Paramètres :
        row (Series) : Ligne du DataFrame contenant les infos du site
        config_couleur (dict) : Configuration de couleur et icône
    
    Retourne :
        str : Code HTML de la popup
    """
    popup_html = f"""
    <div style="font-family: 'Segoe UI', Tahoma, sans-serif; width: 250px;">
        <h4 style="color: {config_couleur['color']}; 
                   margin: 0 0 10px 0; 
                   font-size: 16px; 
                   border-bottom: 2px solid {config_couleur['color']}; 
                   padding-bottom: 5px;">
            <i class="fa {config_couleur['icon']}" style="margin-right: 8px;"></i>
            {row['Site']}
        </h4>
        
        <p style="margin: 5px 0; color: #555; font-size: 13px;">
            <i class="fa fa-map-pin" style="color: {config_couleur['color']}; margin-right: 5px;"></i>
            <strong>Région:</strong> {row['Region']}
        </p>
        
        <p style="margin: 5px 0; color: #555; font-size: 13px;">
            <i class="fa fa-tag" style="color: {config_couleur['color']}; margin-right: 5px;"></i>
            <strong>Type:</strong> {row['Type']}
        </p>
        
        <p style="margin: 5px 0; color: #555; font-size: 13px;">
            <i class="fa fa-calendar" style="color: {config_couleur['color']}; margin-right: 5px;"></i>
            <strong>Inscrit en:</strong> {int(row['Annee']) if pd.notna(row['Annee']) else 'N/A'}
        </p>
    </div>
    """
    
    return popup_html


# Fonction pour créer la légende interactive affichée sur la carte Folium
def creer_legende_html(dataframe):
    """
    Crée le code HTML de la légende affichée sur la carte
    
    Paramètres :
        dataframe (DataFrame) : DataFrame complet pour compter les sites par type
    
    Retourne :
        str : Code HTML de la légende
    """
    # Comptage des sites par type
    nb_culturel = len(dataframe[dataframe['Type'] == 'Culturel'])
    nb_naturel = len(dataframe[dataframe['Type'] == 'Naturel'])
    nb_mixte = len(dataframe[dataframe['Type'] == 'Mixte'])
    nb_total = len(dataframe.dropna(subset=['Latitude', 'Longitude']))
    
    legende_html = f"""
    <div style="position: fixed; 
                top: 10px; 
                right: 10px; 
                width: 200px; 
                background-color: white; 
                border: 2px solid #ddd;
                border-radius: 10px;
                padding: 15px;
                font-family: 'Segoe UI', Tahoma, sans-serif;
                font-size: 14px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                z-index: 9999;">
        
        <!-- En-tête de la légende -->
        <h4 style="margin: 0 0 12px 0; 
                   color: #2c3e50; 
                   font-size: 16px; 
                   border-bottom: 2px solid #3498db; 
                   padding-bottom: 8px;">
            <i class="fa fa-layer-group" style="margin-right: 8px;"></i>Légende
        </h4>
        
        <!-- Type Culturel -->
        <div style="margin: 8px 0;">
            <i class="fa fa-landmark" style="color: #3498db; margin-right: 8px;"></i>
            <span style="color: #555;">Culturel ({nb_culturel})</span>
        </div>
        
        <!-- Type Naturel -->
        <div style="margin: 8px 0;">
            <i class="fa fa-tree" style="color: #27ae60; margin-right: 8px;"></i>
            <span style="color: #555;">Naturel ({nb_naturel})</span>
        </div>
        
        <!-- Type Mixte -->
        <div style="margin: 8px 0;">
            <i class="fa fa-mountain-sun" style="color: #e67e22; margin-right: 8px;"></i>
            <span style="color: #555;">Mixte ({nb_mixte})</span>
        </div>
        
        <!-- Séparateur -->
        <hr style="border: none; border-top: 1px solid #ddd; margin: 12px 0;">
        
        <!-- Total -->
        <div style="text-align: center; color: #7f8c8d; font-size: 12px;">
            <strong>Total: {nb_total} sites</strong>
        </div>
    </div>
    """
    
    return legende_html


# Fonction avancée pour créer une carte interactive avec plugins, légende et marqueurs personnalisés (écrase la version simple)
def creer_carte_interactive(dataframe, nom_fichier='carte_unesco_france.html'):
    """
    Crée une carte interactive avancée avec Folium montrant tous les sites UNESCO
    
    Fonctionnalités :
    - Marqueurs colorés et personnalisés par type de site
    - Popups avec informations détaillées
    - Légende interactive
    - Filtrage géographique (France métropolitaine + DOM-TOM)
    - Bouton plein écran
    - Mini-carte de navigation
    - Style moderne CartoDB Positron
    
    Paramètres :
        dataframe (DataFrame) : DataFrame avec colonnes Latitude, Longitude, Site, Type, etc.
        nom_fichier (str) : Nom du fichier HTML à générer (défaut: 'carte_unesco_france.html')
    """
    try:
        print("🗺️  Création de la carte interactive avancée...")
        
        # Import du module plugins pour fonctionnalités avancées
        from folium import plugins
        
        # --- ÉTAPE 1 : FILTRAGE DES DONNÉES ---
        # On ne garde que les sites avec coordonnées valides
        df_carte = dataframe.dropna(subset=['Latitude', 'Longitude']).copy()
        print(f"   → {len(df_carte)} sites avec coordonnées valides")
        
        # --- ÉTAPE 2 : CRÉATION DE LA CARTE DE BASE ---
        # Carte moderne avec style CartoDB Positron (plus clair et élégant)
        carte = folium.Map(
            location=[46.6, 2.5],           # Centre de la France
            zoom_start=6,                    # Niveau de zoom initial
            tiles='CartoDB positron',        # Style de carte moderne
            control_scale=True               # Affichage de l'échelle
        )
        print("   → Carte de base créée avec style CartoDB Positron")
        
        # --- ÉTAPE 3 : AJOUT DES MARQUEURS ---
        marqueurs_ajoutes = 0
        marqueurs_ignores = 0
        
        for index, row in df_carte.iterrows():
            lat = row['Latitude']
            lon = row['Longitude']
            
            # Vérification que le site est bien en France
            if not verifier_coordonnees_france(lat, lon):
                print(f"   ⚠️  Hors France : {row['Site']} ({lat:.2f}, {lon:.2f})")
                marqueurs_ignores += 1
                continue
            
            # Récupération de la configuration (couleur/icône) selon le type
            config = obtenir_configuration_type(row['Type'])
            
            # Création du contenu HTML de la popup
            popup_html = creer_popup_html(row, config)
            
            # Création et ajout du marqueur sur la carte
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"<b>{row['Site']}</b>",  # Info-bulle au survol
                icon=folium.Icon(
                    color='white',               # Fond du marqueur
                    icon_color=config['color'],  # Couleur de l'icône
                    icon=config['icon'],         # Icône Font Awesome
                    prefix='fa'                  # Préfixe pour Font Awesome
                )
            ).add_to(carte)
            
            marqueurs_ajoutes += 1
        
        print(f"   → {marqueurs_ajoutes} marqueurs ajoutés")
        if marqueurs_ignores > 0:
            print(f"   → {marqueurs_ignores} marqueurs ignorés (hors France)")
        
        # --- ÉTAPE 4 : AJOUT DE LA LÉGENDE ---
        legende_html = creer_legende_html(dataframe)
        carte.get_root().html.add_child(folium.Element(legende_html))
        print("   → Légende ajoutée")
        
        # --- ÉTAPE 5 : AJOUT DES PLUGINS INTERACTIFS ---
        
        # Plugin 1 : Bouton plein écran
        plugins.Fullscreen(
            position='topleft',              # Position en haut à gauche
            title='Plein écran',
            title_cancel='Quitter le plein écran',
            force_separate_button=True
        ).add_to(carte)
        print("   → Plugin plein écran ajouté")
        
        # Plugin 2 : Mini-carte de navigation
        plugins.MiniMap(
            toggle_display=True              # Possibilité de masquer/afficher
        ).add_to(carte)
        print("   → Mini-carte de navigation ajoutée")
        
        # --- ÉTAPE 6 : SAUVEGARDE ET OUVERTURE ---
        carte.save(nom_fichier)
        print(f"✓ Carte sauvegardée : {nom_fichier}")

        # Ouverture dans le navigateur avec chemin absolu
        chemin_absolu = os.path.abspath(nom_fichier)
        webbrowser.open('file://' + chemin_absolu)
        print(f"✓ Carte ouverte dans le navigateur\n")
        
    except ImportError as e:
        print(f"✗ Erreur : Module manquant - {e}")
        print("   Installez folium avec : pip install folium\n")
    except Exception as e:
        print(f"✗ Erreur lors de la création de la carte : {e}\n")