<<<<<<< HEAD
class GestionJokers:
    
    @staticmethod
    def trouver_source_pronos(conn, utilisateur_id, semaine):
        cursor = conn.cursor()
        source_id = utilisateur_id
        visite = set()
        
        while True:
            if source_id in visite:
                print(f"⚠️ Boucle détectée ! Arrêt à l'utilisateur {source_id}")
                break
            
            visite.add(source_id)
            
            cursor.execute("""
                SELECT cible_vol_id
                FROM jokers
                WHERE utilisateur_id = ? 
                AND type_joker = 'points_voles'
                AND semaine_utilisation = ?
                AND utilise = 1
            """, (source_id, semaine))
            
            row = cursor.fetchone()
            
            if row and row[0]:
                source_id = row[0]
                print(f"  🔗 Remontée de chaîne : utilisateur {source_id}")
            else:
                break
        
        print(f"  ✅ Source finale des pronos : utilisateur {source_id}")
        return source_id
    
    @staticmethod
    def copier_pronos(conn, source_id, destination_id, semaine):
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT match_id, score_domicile_prono, score_exterieur_prono, mise
            FROM pronostics p
            JOIN matchs m ON p.match_id = m.id
            WHERE p.utilisateur_id = ? AND m.semaine = ?
        """, (source_id, semaine))
        
        pronos_source = cursor.fetchall()
        
        if not pronos_source:
            print(f"⚠️ Aucun prono trouvé pour l'utilisateur {source_id}")
            return False
        
        for prono in pronos_source:
            match_id = prono[0]
            score_dom = prono[1]
            score_ext = prono[2]
            mise = prono[3]
            
            cursor.execute("""
                INSERT INTO pronostics 
                (utilisateur_id, match_id, score_domicile_prono, score_exterieur_prono, mise, points_gagnes)
                VALUES (?, ?, ?, ?, ?, 0)
            """, (destination_id, match_id, score_dom, score_ext, mise))
            
            print(f"  ✅ Prono copié : Match {match_id} - {score_dom}-{score_ext} (Mise: {mise})")
        
        print(f"✅ {len(pronos_source)} pronos copiés de {source_id} vers {destination_id}")
=======
class GestionJokers:
    
    @staticmethod
    def trouver_source_pronos(conn, utilisateur_id, semaine):
        cursor = conn.cursor()
        source_id = utilisateur_id
        visite = set()
        
        while True:
            if source_id in visite:
                print(f"⚠️ Boucle détectée ! Arrêt à l'utilisateur {source_id}")
                break
            
            visite.add(source_id)
            
            cursor.execute("""
                SELECT cible_vol_id
                FROM jokers
                WHERE utilisateur_id = ? 
                AND type_joker = 'points_voles'
                AND semaine_utilisation = ?
                AND utilise = 1
            """, (source_id, semaine))
            
            row = cursor.fetchone()
            
            if row and row[0]:
                source_id = row[0]
                print(f"  🔗 Remontée de chaîne : utilisateur {source_id}")
            else:
                break
        
        print(f"  ✅ Source finale des pronos : utilisateur {source_id}")
        return source_id
    
    @staticmethod
    def copier_pronos(conn, source_id, destination_id, semaine):
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT match_id, score_domicile_prono, score_exterieur_prono, mise
            FROM pronostics p
            JOIN matchs m ON p.match_id = m.id
            WHERE p.utilisateur_id = ? AND m.semaine = ?
        """, (source_id, semaine))
        
        pronos_source = cursor.fetchall()
        
        if not pronos_source:
            print(f"⚠️ Aucun prono trouvé pour l'utilisateur {source_id}")
            return False
        
        for prono in pronos_source:
            match_id = prono[0]
            score_dom = prono[1]
            score_ext = prono[2]
            mise = prono[3]
            
            cursor.execute("""
                INSERT INTO pronostics 
                (utilisateur_id, match_id, score_domicile_prono, score_exterieur_prono, mise, points_gagnes)
                VALUES (?, ?, ?, ?, ?, 0)
            """, (destination_id, match_id, score_dom, score_ext, mise))
            
            print(f"  ✅ Prono copié : Match {match_id} - {score_dom}-{score_ext} (Mise: {mise})")
        
        print(f"✅ {len(pronos_source)} pronos copiés de {source_id} vers {destination_id}")
>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
        return True