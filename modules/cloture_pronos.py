<<<<<<< HEAD
from database_manager import DatabaseManager
from gestion_jokers import GestionJokers

def cloture_pronos_semaine(semaine):
    
    print(f"\n🔒 CLÔTURE DES PRONOS - SEMAINE {semaine}")
    print("=" * 60)
    
    db = DatabaseManager()
    conn = None
    
    try:
        conn = db.create_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, pseudo FROM utilisateurs WHERE statut = 'actif'")
        utilisateurs = cursor.fetchall()
        
        print(f"\n📊 {len(utilisateurs)} joueur(s) actif(s)\n")
        
        for user in utilisateurs:
            user_id = user[0]
            pseudo = user[1]
            
            cursor.execute("""
                SELECT COUNT(*) FROM pronostics p
                JOIN matchs m ON p.match_id = m.id
                WHERE p.utilisateur_id = ? AND m.semaine = ?
            """, (user_id, semaine))
            
            nb_pronos = cursor.fetchone()[0]
            
            if nb_pronos > 0:
                print(f"✅ {pseudo} : {nb_pronos} pronos enregistrés")
            else:
                print(f"⚠️  {pseudo} : AUCUN PRONO → Activation joker oubli")
                
                cursor.execute("""
                    SELECT id FROM utilisateurs 
                    WHERE statut = 'actif' AND id != ?
                    ORDER BY (
                        SELECT COALESCE(SUM(points_totaux), 0) 
                        FROM historique 
                        WHERE utilisateur_id = utilisateurs.id
                    ) ASC
                    LIMIT 1
                """, (user_id,))
                
                dernier = cursor.fetchone()
                
                if dernier:
                    dernier_id = dernier[0]
                    
                    cursor.execute("""
                        INSERT INTO jokers 
                        (utilisateur_id, type_joker, utilise, semaine_utilisation, cible_vol_id, date_utilisation)
                        VALUES (?, 'points_voles', 1, ?, ?, CURRENT_TIMESTAMP)
                    """, (user_id, semaine, dernier_id))
                    
                    cursor.execute("""
                        UPDATE stock_jokers 
                        SET jokers_voles_disponibles = jokers_voles_disponibles - 1
                        WHERE utilisateur_id = ?
                    """, (user_id,))
                    
                    print(f"  🆘 Joker oubli activé → Cible: utilisateur {dernier_id}")
        
        print("\n🔄 COPIE DES PRONOS VOLÉS")
        print("=" * 60)
        
        cursor.execute("""
            SELECT utilisateur_id, cible_vol_id
            FROM jokers
            WHERE type_joker = 'points_voles'
            AND semaine_utilisation = ?
            AND utilise = 1
        """, (semaine,))
        
        vols = cursor.fetchall()
        
        for vol in vols:
            voleur_id = vol[0]
            cible_initiale = vol[1]
            
            cursor.execute("SELECT pseudo FROM utilisateurs WHERE id = ?", (voleur_id,))
            pseudo_voleur = cursor.fetchone()[0]
            
            source_finale = GestionJokers.trouver_source_pronos(conn, cible_initiale, semaine)
            
            print(f"\n👤 {pseudo_voleur} (ID {voleur_id}):")
            print(f"  🎯 Cible initiale : {cible_initiale}")
            print(f"  🎯 Source finale : {source_finale}")
            
            cursor.execute("""
                DELETE FROM pronostics 
                WHERE utilisateur_id = ? 
                AND match_id IN (SELECT id FROM matchs WHERE semaine = ?)
            """, (voleur_id, semaine))
            
            GestionJokers.copier_pronos(conn, source_finale, voleur_id, semaine)
        
        conn.commit()
        
        print("\n" + "=" * 60)
        print("✅ CLÔTURE TERMINÉE")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la clôture : {e}")
    
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        semaine = int(sys.argv[1])
    else:
        semaine = 1
    
=======
from database_manager import DatabaseManager
from gestion_jokers import GestionJokers

def cloture_pronos_semaine(semaine):
    
    print(f"\n🔒 CLÔTURE DES PRONOS - SEMAINE {semaine}")
    print("=" * 60)
    
    db = DatabaseManager()
    conn = None
    
    try:
        conn = db.create_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, pseudo FROM utilisateurs WHERE statut = 'actif'")
        utilisateurs = cursor.fetchall()
        
        print(f"\n📊 {len(utilisateurs)} joueur(s) actif(s)\n")
        
        for user in utilisateurs:
            user_id = user[0]
            pseudo = user[1]
            
            cursor.execute("""
                SELECT COUNT(*) FROM pronostics p
                JOIN matchs m ON p.match_id = m.id
                WHERE p.utilisateur_id = ? AND m.semaine = ?
            """, (user_id, semaine))
            
            nb_pronos = cursor.fetchone()[0]
            
            if nb_pronos > 0:
                print(f"✅ {pseudo} : {nb_pronos} pronos enregistrés")
            else:
                print(f"⚠️  {pseudo} : AUCUN PRONO → Activation joker oubli")
                
                cursor.execute("""
                    SELECT id FROM utilisateurs 
                    WHERE statut = 'actif' AND id != ?
                    ORDER BY (
                        SELECT COALESCE(SUM(points_totaux), 0) 
                        FROM historique 
                        WHERE utilisateur_id = utilisateurs.id
                    ) ASC
                    LIMIT 1
                """, (user_id,))
                
                dernier = cursor.fetchone()
                
                if dernier:
                    dernier_id = dernier[0]
                    
                    cursor.execute("""
                        INSERT INTO jokers 
                        (utilisateur_id, type_joker, utilise, semaine_utilisation, cible_vol_id, date_utilisation)
                        VALUES (?, 'points_voles', 1, ?, ?, CURRENT_TIMESTAMP)
                    """, (user_id, semaine, dernier_id))
                    
                    cursor.execute("""
                        UPDATE stock_jokers 
                        SET jokers_voles_disponibles = jokers_voles_disponibles - 1
                        WHERE utilisateur_id = ?
                    """, (user_id,))
                    
                    print(f"  🆘 Joker oubli activé → Cible: utilisateur {dernier_id}")
        
        print("\n🔄 COPIE DES PRONOS VOLÉS")
        print("=" * 60)
        
        cursor.execute("""
            SELECT utilisateur_id, cible_vol_id
            FROM jokers
            WHERE type_joker = 'points_voles'
            AND semaine_utilisation = ?
            AND utilise = 1
        """, (semaine,))
        
        vols = cursor.fetchall()
        
        for vol in vols:
            voleur_id = vol[0]
            cible_initiale = vol[1]
            
            cursor.execute("SELECT pseudo FROM utilisateurs WHERE id = ?", (voleur_id,))
            pseudo_voleur = cursor.fetchone()[0]
            
            source_finale = GestionJokers.trouver_source_pronos(conn, cible_initiale, semaine)
            
            print(f"\n👤 {pseudo_voleur} (ID {voleur_id}):")
            print(f"  🎯 Cible initiale : {cible_initiale}")
            print(f"  🎯 Source finale : {source_finale}")
            
            cursor.execute("""
                DELETE FROM pronostics 
                WHERE utilisateur_id = ? 
                AND match_id IN (SELECT id FROM matchs WHERE semaine = ?)
            """, (voleur_id, semaine))
            
            GestionJokers.copier_pronos(conn, source_finale, voleur_id, semaine)
        
        conn.commit()
        
        print("\n" + "=" * 60)
        print("✅ CLÔTURE TERMINÉE")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la clôture : {e}")
    
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        semaine = int(sys.argv[1])
    else:
        semaine = 1
    
>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
    cloture_pronos_semaine(semaine)