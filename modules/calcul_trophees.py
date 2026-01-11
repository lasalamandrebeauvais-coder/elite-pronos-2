<<<<<<< HEAD
try:
    from modules.database_manager import DatabaseManager
except:
    from database_manager import DatabaseManager


class CalculTrophees:
    
    def __init__(self, semaine):
        self.semaine = semaine
        print(f"🏆 Initialisation calcul des trophées - Semaine {semaine}")
    
    def calculer_trophees(self):
        print(f"\n{'='*70}")
        print(f"🏆 ATTRIBUTION DES TROPHÉES - SEMAINE {self.semaine}")
        print(f"{'='*70}\n")
        
        db = DatabaseManager()
        conn = None
        trophees = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            # 1. 👑 LE ROI DE LA SEMAINE (meilleur score)
            roi = self.get_roi_semaine(cursor)
            if roi:
                trophees.append(roi)
                print(f"👑 LE ROI DE LA SEMAINE : {roi['pseudo']} ({roi['valeur']:.1f} pts)")
            
            # 2. 🚀 LA FUSÉE (plus grosse remontée)
            fusee = self.get_fusee(cursor)
            if fusee:
                trophees.append(fusee)
                print(f"🚀 LA FUSÉE : {fusee['pseudo']} (+{int(fusee['valeur'])} places)")
            
            # 3. 🎯 LE SNIPER (plus de scores exacts)
            sniper = self.get_sniper(cursor)
            if sniper:
                trophees.append(sniper)
                print(f"🎯 LE SNIPER : {sniper['pseudo']} ({int(sniper['valeur'])} scores exacts)")
            
            # 4. 🌵 LE CACTUS (0 points)
            cactus = self.get_cactus(cursor)
            if cactus:
                trophees.append(cactus)
                print(f"🌵 LE CACTUS : {cactus['pseudo']} (0 pts 😅)")
            
            # 5. 💘 LE VOLEUR DE CŒUR (a volé le leader)
            voleur = self.get_voleur_coeur(cursor)
            if voleur:
                trophees.append(voleur)
                print(f"💘 LE VOLEUR DE CŒUR : {voleur['pseudo']}")
            
            # 6. 🎰 LE BANQUIER (plus gros gain en un match)
            banquier = self.get_banquier(cursor)
            if banquier:
                trophees.append(banquier)
                print(f"🎰 LE BANQUIER : {banquier['pseudo']} ({banquier['valeur']:.1f} pts en 1 match)")
            
            # MENTIONS SPÉCIALES
            print(f"\n{'='*70}")
            print("✨ MENTIONS SPÉCIALES")
            print(f"{'='*70}")
            
            # 🎪 Grand Chelem
            grand_chelems = self.get_grand_chelems(cursor)
            for gc in grand_chelems:
                trophees.append(gc)
                print(f"🎪 GRAND CHELEM : {gc['pseudo']}")
            
            # 👑×2 Joker Points Doubles
            jokers_doubles = self.get_jokers_doubles(cursor)
            for jd in jokers_doubles:
                trophees.append(jd)
                print(f"👑×2 JOKER POINTS DOUBLES : {jd['pseudo']}")
            
            # 🦥 Joker Oubli
            jokers_oubli = self.get_jokers_oubli(cursor)
            for jo in jokers_oubli:
                trophees.append(jo)
                print(f"🦥 JOKER OUBLI : {jo['pseudo']}")
            
            # Enregistrement en base
            for trophee in trophees:
                cursor.execute("""
                    INSERT INTO trophees (semaine, utilisateur_id, categorie, valeur)
                    VALUES (?, ?, ?, ?)
                """, (self.semaine, trophee['user_id'], trophee['categorie'], trophee.get('valeur', 0)))
            
            conn.commit()
            
            print(f"\n{'='*70}")
            print(f"✅ {len(trophees)} TROPHÉES ATTRIBUÉS")
            print(f"{'='*70}\n")
            
            return trophees
            
        except Exception as e:
            print(f"❌ Erreur calcul trophées : {e}")
            return []
        
        finally:
            if conn:
                conn.close()
    
    def get_roi_semaine(self, cursor):
        cursor.execute("""
            SELECT u.id, u.pseudo, h.points_totaux
            FROM historique h
            JOIN utilisateurs u ON h.utilisateur_id = u.id
            WHERE h.semaine = ?
            ORDER BY h.points_totaux DESC
            LIMIT 1
        """, (self.semaine,))
        
        row = cursor.fetchone()
        if row:
            return {
                'user_id': row[0],
                'pseudo': row[1],
                'categorie': 'roi_semaine',
                'valeur': row[2]
            }
        return None
    
    def get_fusee(self, cursor):
        # Pour l'instant, retourne None (on développera plus tard avec un système de classement historique)
        # Cette fonctionnalité nécessite un suivi du rang semaine par semaine
        return None
    
    def get_sniper(self, cursor):
        cursor.execute("""
            SELECT u.id, u.pseudo, h.scores_exacts
            FROM historique h
            JOIN utilisateurs u ON h.utilisateur_id = u.id
            WHERE h.semaine = ?
            ORDER BY h.scores_exacts DESC
            LIMIT 1
        """, (self.semaine,))
        
        row = cursor.fetchone()
        if row and row[2] > 0:
            return {
                'user_id': row[0],
                'pseudo': row[1],
                'categorie': 'sniper',
                'valeur': row[2]
            }
        return None
    
    def get_cactus(self, cursor):
        cursor.execute("""
            SELECT u.id, u.pseudo, h.points_totaux
            FROM historique h
            JOIN utilisateurs u ON h.utilisateur_id = u.id
            WHERE h.semaine = ? AND h.points_totaux = 0
            LIMIT 1
        """, (self.semaine,))
        
        row = cursor.fetchone()
        if row:
            return {
                'user_id': row[0],
                'pseudo': row[1],
                'categorie': 'cactus',
                'valeur': 0
            }
        return None
    
    def get_voleur_coeur(self, cursor):
        cursor.execute("""
            SELECT u.id, u.pseudo, j.cible_vol_id,
                   (SELECT SUM(points_totaux) FROM historique WHERE utilisateur_id = j.cible_vol_id AND semaine < ?) as points_cible
            FROM jokers j
            JOIN utilisateurs u ON j.utilisateur_id = u.id
            WHERE j.semaine_utilisation = ? AND j.type_joker = 'points_voles'
            ORDER BY points_cible DESC
            LIMIT 1
        """, (self.semaine, self.semaine))
        
        row = cursor.fetchone()
        if row:
            return {
                'user_id': row[0],
                'pseudo': row[1],
                'categorie': 'voleur_coeur',
                'valeur': 0
            }
        return None
    
    def get_banquier(self, cursor):
        cursor.execute("""
            SELECT u.id, u.pseudo, MAX(p.points_gagnes) as max_gain
            FROM pronostics p
            JOIN matchs m ON p.match_id = m.id
            JOIN utilisateurs u ON p.utilisateur_id = u.id
            WHERE m.semaine = ?
            GROUP BY u.id, u.pseudo
            ORDER BY max_gain DESC
            LIMIT 1
        """, (self.semaine,))
        
        row = cursor.fetchone()
        if row and row[2] > 0:
            return {
                'user_id': row[0],
                'pseudo': row[1],
                'categorie': 'banquier',
                'valeur': row[2]
            }
        return None
    
    def get_grand_chelems(self, cursor):
        cursor.execute("""
            SELECT u.id, u.pseudo
            FROM historique h
            JOIN utilisateurs u ON h.utilisateur_id = u.id
            WHERE h.semaine = ? AND h.grand_chelem = 1
        """, (self.semaine,))
        
        rows = cursor.fetchall()
        return [{
            'user_id': row[0],
            'pseudo': row[1],
            'categorie': 'grand_chelem',
            'valeur': 0
        } for row in rows]
    
    def get_jokers_doubles(self, cursor):
        cursor.execute("""
            SELECT u.id, u.pseudo
            FROM jokers j
            JOIN utilisateurs u ON j.utilisateur_id = u.id
            WHERE j.semaine_utilisation = ? AND j.type_joker = 'points_doubles'
        """, (self.semaine,))
        
        rows = cursor.fetchall()
        return [{
            'user_id': row[0],
            'pseudo': row[1],
            'categorie': 'joker_double',
            'valeur': 0
        } for row in rows]
    
    def get_jokers_oubli(self, cursor):
        cursor.execute("""
            SELECT u.id, u.pseudo
            FROM jokers j
            JOIN utilisateurs u ON j.utilisateur_id = u.id
            WHERE j.semaine_utilisation = ? 
            AND j.type_joker = 'points_voles'
            AND NOT EXISTS (
                SELECT 1 FROM pronostics p
                JOIN matchs m ON p.match_id = m.id
                WHERE p.utilisateur_id = u.id AND m.semaine = ?
                LIMIT 1
            )
        """, (self.semaine, self.semaine - 1))
        
        rows = cursor.fetchall()
        return [{
            'user_id': row[0],
            'pseudo': row[1],
            'categorie': 'joker_oubli',
            'valeur': 0
        } for row in rows]

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        semaine = int(sys.argv[1])
    else:
        semaine = 1
    
    calcul = CalculTrophees(semaine)
    calcul.calculer_trophees()
=======
try:
    from modules.database_manager import DatabaseManager
except:
    from database_manager import DatabaseManager


class CalculTrophees:
    
    def __init__(self, semaine):
        self.semaine = semaine
        print(f"🏆 Initialisation calcul des trophées - Semaine {semaine}")
    
    def calculer_trophees(self):
        print(f"\n{'='*70}")
        print(f"🏆 ATTRIBUTION DES TROPHÉES - SEMAINE {self.semaine}")
        print(f"{'='*70}\n")
        
        db = DatabaseManager()
        conn = None
        trophees = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            # 1. 👑 LE ROI DE LA SEMAINE (meilleur score)
            roi = self.get_roi_semaine(cursor)
            if roi:
                trophees.append(roi)
                print(f"👑 LE ROI DE LA SEMAINE : {roi['pseudo']} ({roi['valeur']:.1f} pts)")
            
            # 2. 🚀 LA FUSÉE (plus grosse remontée)
            fusee = self.get_fusee(cursor)
            if fusee:
                trophees.append(fusee)
                print(f"🚀 LA FUSÉE : {fusee['pseudo']} (+{int(fusee['valeur'])} places)")
            
            # 3. 🎯 LE SNIPER (plus de scores exacts)
            sniper = self.get_sniper(cursor)
            if sniper:
                trophees.append(sniper)
                print(f"🎯 LE SNIPER : {sniper['pseudo']} ({int(sniper['valeur'])} scores exacts)")
            
            # 4. 🌵 LE CACTUS (0 points)
            cactus = self.get_cactus(cursor)
            if cactus:
                trophees.append(cactus)
                print(f"🌵 LE CACTUS : {cactus['pseudo']} (0 pts 😅)")
            
            # 5. 💘 LE VOLEUR DE CŒUR (a volé le leader)
            voleur = self.get_voleur_coeur(cursor)
            if voleur:
                trophees.append(voleur)
                print(f"💘 LE VOLEUR DE CŒUR : {voleur['pseudo']}")
            
            # 6. 🎰 LE BANQUIER (plus gros gain en un match)
            banquier = self.get_banquier(cursor)
            if banquier:
                trophees.append(banquier)
                print(f"🎰 LE BANQUIER : {banquier['pseudo']} ({banquier['valeur']:.1f} pts en 1 match)")
            
            # MENTIONS SPÉCIALES
            print(f"\n{'='*70}")
            print("✨ MENTIONS SPÉCIALES")
            print(f"{'='*70}")
            
            # 🎪 Grand Chelem
            grand_chelems = self.get_grand_chelems(cursor)
            for gc in grand_chelems:
                trophees.append(gc)
                print(f"🎪 GRAND CHELEM : {gc['pseudo']}")
            
            # 👑×2 Joker Points Doubles
            jokers_doubles = self.get_jokers_doubles(cursor)
            for jd in jokers_doubles:
                trophees.append(jd)
                print(f"👑×2 JOKER POINTS DOUBLES : {jd['pseudo']}")
            
            # 🦥 Joker Oubli
            jokers_oubli = self.get_jokers_oubli(cursor)
            for jo in jokers_oubli:
                trophees.append(jo)
                print(f"🦥 JOKER OUBLI : {jo['pseudo']}")
            
            # Enregistrement en base
            for trophee in trophees:
                cursor.execute("""
                    INSERT INTO trophees (semaine, utilisateur_id, categorie, valeur)
                    VALUES (?, ?, ?, ?)
                """, (self.semaine, trophee['user_id'], trophee['categorie'], trophee.get('valeur', 0)))
            
            conn.commit()
            
            print(f"\n{'='*70}")
            print(f"✅ {len(trophees)} TROPHÉES ATTRIBUÉS")
            print(f"{'='*70}\n")
            
            return trophees
            
        except Exception as e:
            print(f"❌ Erreur calcul trophées : {e}")
            return []
        
        finally:
            if conn:
                conn.close()
    
    def get_roi_semaine(self, cursor):
        cursor.execute("""
            SELECT u.id, u.pseudo, h.points_totaux
            FROM historique h
            JOIN utilisateurs u ON h.utilisateur_id = u.id
            WHERE h.semaine = ?
            ORDER BY h.points_totaux DESC
            LIMIT 1
        """, (self.semaine,))
        
        row = cursor.fetchone()
        if row:
            return {
                'user_id': row[0],
                'pseudo': row[1],
                'categorie': 'roi_semaine',
                'valeur': row[2]
            }
        return None
    
    def get_fusee(self, cursor):
        # Pour l'instant, retourne None (on développera plus tard avec un système de classement historique)
        # Cette fonctionnalité nécessite un suivi du rang semaine par semaine
        return None
    
    def get_sniper(self, cursor):
        cursor.execute("""
            SELECT u.id, u.pseudo, h.scores_exacts
            FROM historique h
            JOIN utilisateurs u ON h.utilisateur_id = u.id
            WHERE h.semaine = ?
            ORDER BY h.scores_exacts DESC
            LIMIT 1
        """, (self.semaine,))
        
        row = cursor.fetchone()
        if row and row[2] > 0:
            return {
                'user_id': row[0],
                'pseudo': row[1],
                'categorie': 'sniper',
                'valeur': row[2]
            }
        return None
    
    def get_cactus(self, cursor):
        cursor.execute("""
            SELECT u.id, u.pseudo, h.points_totaux
            FROM historique h
            JOIN utilisateurs u ON h.utilisateur_id = u.id
            WHERE h.semaine = ? AND h.points_totaux = 0
            LIMIT 1
        """, (self.semaine,))
        
        row = cursor.fetchone()
        if row:
            return {
                'user_id': row[0],
                'pseudo': row[1],
                'categorie': 'cactus',
                'valeur': 0
            }
        return None
    
    def get_voleur_coeur(self, cursor):
        cursor.execute("""
            SELECT u.id, u.pseudo, j.cible_vol_id,
                   (SELECT SUM(points_totaux) FROM historique WHERE utilisateur_id = j.cible_vol_id AND semaine < ?) as points_cible
            FROM jokers j
            JOIN utilisateurs u ON j.utilisateur_id = u.id
            WHERE j.semaine_utilisation = ? AND j.type_joker = 'points_voles'
            ORDER BY points_cible DESC
            LIMIT 1
        """, (self.semaine, self.semaine))
        
        row = cursor.fetchone()
        if row:
            return {
                'user_id': row[0],
                'pseudo': row[1],
                'categorie': 'voleur_coeur',
                'valeur': 0
            }
        return None
    
    def get_banquier(self, cursor):
        cursor.execute("""
            SELECT u.id, u.pseudo, MAX(p.points_gagnes) as max_gain
            FROM pronostics p
            JOIN matchs m ON p.match_id = m.id
            JOIN utilisateurs u ON p.utilisateur_id = u.id
            WHERE m.semaine = ?
            GROUP BY u.id, u.pseudo
            ORDER BY max_gain DESC
            LIMIT 1
        """, (self.semaine,))
        
        row = cursor.fetchone()
        if row and row[2] > 0:
            return {
                'user_id': row[0],
                'pseudo': row[1],
                'categorie': 'banquier',
                'valeur': row[2]
            }
        return None
    
    def get_grand_chelems(self, cursor):
        cursor.execute("""
            SELECT u.id, u.pseudo
            FROM historique h
            JOIN utilisateurs u ON h.utilisateur_id = u.id
            WHERE h.semaine = ? AND h.grand_chelem = 1
        """, (self.semaine,))
        
        rows = cursor.fetchall()
        return [{
            'user_id': row[0],
            'pseudo': row[1],
            'categorie': 'grand_chelem',
            'valeur': 0
        } for row in rows]
    
    def get_jokers_doubles(self, cursor):
        cursor.execute("""
            SELECT u.id, u.pseudo
            FROM jokers j
            JOIN utilisateurs u ON j.utilisateur_id = u.id
            WHERE j.semaine_utilisation = ? AND j.type_joker = 'points_doubles'
        """, (self.semaine,))
        
        rows = cursor.fetchall()
        return [{
            'user_id': row[0],
            'pseudo': row[1],
            'categorie': 'joker_double',
            'valeur': 0
        } for row in rows]
    
    def get_jokers_oubli(self, cursor):
        cursor.execute("""
            SELECT u.id, u.pseudo
            FROM jokers j
            JOIN utilisateurs u ON j.utilisateur_id = u.id
            WHERE j.semaine_utilisation = ? 
            AND j.type_joker = 'points_voles'
            AND NOT EXISTS (
                SELECT 1 FROM pronostics p
                JOIN matchs m ON p.match_id = m.id
                WHERE p.utilisateur_id = u.id AND m.semaine = ?
                LIMIT 1
            )
        """, (self.semaine, self.semaine - 1))
        
        rows = cursor.fetchall()
        return [{
            'user_id': row[0],
            'pseudo': row[1],
            'categorie': 'joker_oubli',
            'valeur': 0
        } for row in rows]

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        semaine = int(sys.argv[1])
    else:
        semaine = 1
    
    calcul = CalculTrophees(semaine)
    calcul.calculer_trophees()
>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
