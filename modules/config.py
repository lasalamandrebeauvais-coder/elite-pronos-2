<<<<<<< HEAD
# config.py - Configuration globale du projet Elite Pronos 2

import os

# ==========================================
# CHEMINS DES FICHIERS
# ==========================================
# Chemin racine du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Chemin de la base de données
DB_PATH = os.path.join(BASE_DIR, "database", "pronos_expert.db")

# Chemin du dossier des avatars
AVATARS_DIR = os.path.join(BASE_DIR, "assets", "avatars")

# ==========================================
# DIMENSIONS DE LA FENÊTRE
# ==========================================
# Dimensions fixes optimisées pour écran 1280x720
FENETRE_LARGEUR = 950
FENETRE_HAUTEUR = 680

print(f"📏 Fenêtre adaptée : {FENETRE_LARGEUR}x{FENETRE_HAUTEUR}")

# ==========================================
# RÈGLES DU JEU
# ==========================================
# Budget par défaut
BUDGET_NORMAL = 100

# Budget après un Grand Chelem
BUDGET_GRAND_CHELEM = 140

# Nombre de matchs par semaine
NOMBRE_MATCHS = 4

# Mise minimum et maximum par match
MISE_MIN = 10
MISE_MAX = 60

# Bonus pour un score exact
BONUS_SCORE_EXACT = 10

# ==========================================
# JOKERS
# ==========================================
# Nombre de jokers "Points Doubles" par saison
JOKERS_DOUBLES = 3

# Nombre de jokers "Points Volés" par saison
JOKERS_VOLES = 2

# ==========================================
# INTERFACE GRAPHIQUE
# ==========================================
# Couleurs du thème
COULEUR_FOND = "#1a1a2e"  # Bleu nuit profond
COULEUR_OR = "#FFD700"     # Doré
COULEUR_BLANC = "#FFFFFF"  # Blanc
COULEUR_ROUGE = "#FF0000"  # Rouge vif
COULEUR_GRIS = "#D3D3D3"   # Gris clair

print("✅ Configuration chargée avec succès !")
# === API CONFIGURATION ===
=======
# config.py - Configuration globale du projet Elite Pronos 2

import os

# ==========================================
# CHEMINS DES FICHIERS
# ==========================================
# Chemin racine du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Chemin de la base de données
DB_PATH = os.path.join(BASE_DIR, "database", "pronos_expert.db")

# Chemin du dossier des avatars
AVATARS_DIR = os.path.join(BASE_DIR, "assets", "avatars")

# ==========================================
# DIMENSIONS DE LA FENÊTRE
# ==========================================
# Dimensions fixes optimisées pour écran 1280x720
FENETRE_LARGEUR = 950
FENETRE_HAUTEUR = 680

print(f"📏 Fenêtre adaptée : {FENETRE_LARGEUR}x{FENETRE_HAUTEUR}")

# ==========================================
# RÈGLES DU JEU
# ==========================================
# Budget par défaut
BUDGET_NORMAL = 100

# Budget après un Grand Chelem
BUDGET_GRAND_CHELEM = 140

# Nombre de matchs par semaine
NOMBRE_MATCHS = 4

# Mise minimum et maximum par match
MISE_MIN = 10
MISE_MAX = 60

# Bonus pour un score exact
BONUS_SCORE_EXACT = 10

# ==========================================
# JOKERS
# ==========================================
# Nombre de jokers "Points Doubles" par saison
JOKERS_DOUBLES = 3

# Nombre de jokers "Points Volés" par saison
JOKERS_VOLES = 2

# ==========================================
# INTERFACE GRAPHIQUE
# ==========================================
# Couleurs du thème
COULEUR_FOND = "#1a1a2e"  # Bleu nuit profond
COULEUR_OR = "#FFD700"     # Doré
COULEUR_BLANC = "#FFFFFF"  # Blanc
COULEUR_ROUGE = "#FF0000"  # Rouge vif
COULEUR_GRIS = "#D3D3D3"   # Gris clair

print("✅ Configuration chargée avec succès !")
# === API CONFIGURATION ===
>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
API_KEY = "bf58da6a49824f2a8742957b89ca52ee"