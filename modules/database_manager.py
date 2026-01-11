# database_manager.py - Gestion de la base de données

import sqlite3
import os
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'pronos_expert.db')


class DatabaseManager:
    """
    Classe pour gérer toutes les opérations de base de données.
    Elle crée les tables et fournit des méthodes pour interagir avec la DB.
    """
    
    def __init__(self):
        """
        Initialise la connexion à la base de données.
        Si la base n'existe pas, elle sera créée automatiquement.
        """
        self.db_path = DB_PATH
        print(f"📂 Chemin de la base de données : {self.db_path}")
    
    def create_connection(self):
        """
        Crée et retourne une connexion à la base de données.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            print("✅ Connexion à la base de données établie")
            return conn
        except sqlite3.Error as e:
            print(f"❌ Erreur de connexion : {e}")
            return None
    
    def create_tables(self):
        """
        Crée toutes les tables nécessaires au projet.
        """
        conn = self.create_connection()
        if conn is None:
            return
        
        cursor = conn.cursor()
        
        # ===================================
        # TABLE 1 : UTILISATEURS
        # ===================================
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS journees_calendrier (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    semaine INTEGER NOT NULL UNIQUE,
                    date_premier_match TEXT,
                    date_cloture_pronos TEXT,
                    date_dernier_match TEXT,
                    delai_depuis_precedente INTEGER,
                    type_calendrier TEXT DEFAULT 'normal',
                    statut TEXT DEFAULT 'a_venir',
                    sourcing_effectue INTEGER DEFAULT 0,
                    notification_j2_envoyee INTEGER DEFAULT 0,
                    notification_j1_envoyee INTEGER DEFAULT 0,
                    notification_2h_envoyee INTEGER DEFAULT 0
                )
            """)
        print("✅ Table 'utilisateurs' créée/vérifiée")
        
        # ===================================
        # TABLE 2 : MATCHS
        # ===================================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS matchs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                semaine INTEGER NOT NULL,
                equipe_domicile TEXT NOT NULL,
                equipe_exterieur TEXT NOT NULL,
                cote_domicile REAL NOT NULL,
                cote_nul REAL NOT NULL,
                cote_exterieur REAL NOT NULL,
                score_domicile INTEGER,
                score_exterieur INTEGER,
                date_match TIMESTAMP NOT NULL,
                statut TEXT DEFAULT 'en_attente'
            )
        """)
        print("✅ Table 'matchs' créée/vérifiée")
        
        # ===================================
        # TABLE 3 : PRONOSTICS
        # ===================================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pronostics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                utilisateur_id INTEGER NOT NULL,
                match_id INTEGER NOT NULL,
                score_domicile_prono INTEGER NOT NULL,
                score_exterieur_prono INTEGER NOT NULL,
                mise INTEGER NOT NULL,
                points_gagnes REAL DEFAULT 0,
                date_prono TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id),
                FOREIGN KEY (match_id) REFERENCES matchs(id)
            )
        """)
        print("✅ Table 'pronostics' créée/vérifiée")
        
        # ===================================
        # TABLE 4 : HISTORIQUE
        # ===================================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historique (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                utilisateur_id INTEGER NOT NULL,
                semaine INTEGER NOT NULL,
                points_totaux REAL DEFAULT 0,
                scores_exacts INTEGER DEFAULT 0,
                bons_pronos INTEGER DEFAULT 0,
                grand_chelem INTEGER DEFAULT 0,
                joker_utilise TEXT,
                date_calcul TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
            )
        """)
        print("✅ Table 'historique' créée/vérifiée")
        
        # ===================================
        # TABLE 5 : JOKERS
        # ===================================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jokers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                utilisateur_id INTEGER NOT NULL,
                type_joker TEXT NOT NULL,
                utilise INTEGER DEFAULT 0,
                semaine_utilisation INTEGER,
                cible_vol_id INTEGER,
                date_utilisation TIMESTAMP,
                FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id),
                FOREIGN KEY (cible_vol_id) REFERENCES utilisateurs(id)
            )
        """)
        print("✅ Table 'jokers' créée/vérifiée")
        
        # ===================================
        # TABLE 6 : STOCK_JOKERS (NOUVEAU)
        # ===================================
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_jokers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                utilisateur_id INTEGER NOT NULL UNIQUE,
                jokers_doubles_disponibles INTEGER DEFAULT 1,
                jokers_voles_disponibles INTEGER DEFAULT 1,
                derniere_mise_a_jour TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
            )
        """)
        print("✅ Table 'stock_jokers' créée/vérifiée")
        
        # Sauvegarde et fermeture
        conn.commit()
        conn.close()
        print("🔒 Connexion fermée")

# ===================================
# TEST