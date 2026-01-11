import sqlite3
import os

def migrate_database():
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'pronos_expert.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA table_info(pronostics)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'pronostic' not in columns:
        print("🔧 Migration : Ajout de la colonne 'pronostic'...")
        cursor.execute("ALTER TABLE pronostics ADD COLUMN pronostic TEXT")
        
        cursor.execute("""
            UPDATE pronostics 
            SET pronostic = CASE 
                WHEN score_domicile_prono > score_exterieur_prono THEN '1'
                WHEN score_domicile_prono < score_exterieur_prono THEN '2'
                ELSE 'N'
            END
            WHERE score_domicile_prono IS NOT NULL
        """)
        
        conn.commit()
        print("✅ Migration terminée !")
    
    conn.close()

if __name__ == "__main__":
    migrate_database()
