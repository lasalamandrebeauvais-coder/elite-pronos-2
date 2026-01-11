<<<<<<< HEAD
# calcul_gains.py - Module de calcul des gains

from modules.database_manager import DatabaseManager
import sqlite3

class CalculGains:
    
    def __init__(self, semaine):
        self.semaine = semaine
        print(f"✅ Module de calcul initialisé (Semaine {semaine})")
    
    def get_results_dict(self, score_dom, score_ext):
        if score_dom > score_ext:
            return "1"
        elif score_dom == score_ext:
            return "N"
        else:
            return "2"
    
    def calculer_pour_semaine(self, resultats):
        print(f"\n{'='*60}")
        print(f"🧮 CALCUL DES GAINS - SEMAINE {self.semaine}")
        print(f"{'='*60}")
        
        if len(resultats) != 4:
            print("❌ Erreur : Il faut exactement 4 résultats !")
            return
        
        self.update_match_results(resultats)
        joueurs = self.get_joueurs_avec_pronos()
        
        if not joueurs:
            print("❌ Aucun joueur n'a pronostiqué cette semaine !")
            return
        
        print(f"\n👥 {len(joueurs)} joueur(s) à traiter\n")
        
        for joueur in joueurs:
            self.calculer_pour_joueur(joueur, resultats)
        
        print(f"\n{'='*60}")
        print(f"✅ CALCUL TERMINÉ")
        print(f"{'='*60}\n")
    
    def update_match_results(self, resultats):
        db = DatabaseManager()
        conn = None
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            for res in resultats:
                cursor.execute("""
                    UPDATE matchs
                    SET score_domicile = ?, score_exterieur = ?, statut = 'termine'
                    WHERE id = ?
                """, (res["score_dom"], res["score_ext"], res["match_id"]))
            
            conn.commit()
            print("✅ Résultats réels enregistrés dans la table matchs")
            
        except Exception as e:
            print(f"❌ Erreur mise à jour matchs : {e}")
        finally:
            if conn:
                conn.close()
    
    def get_joueurs_avec_pronos(self):
        db = DatabaseManager()
        conn = None
        joueurs = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT DISTINCT u.id, u.pseudo
                FROM utilisateurs u
                INNER JOIN pronostics p ON u.id = p.utilisateur_id
                INNER JOIN matchs m ON p.match_id = m.id
                WHERE m.semaine = ?
            """, (self.semaine,))
            
            rows = cursor.fetchall()
            
            for row in rows:
                joueurs.append({"id": row[0], "pseudo": row[1]})
            
        except Exception as e:
            print(f"❌ Erreur récupération joueurs : {e}")
        finally:
            if conn:
                conn.close()
        
        return joueurs
    
    def calculer_pour_joueur(self, joueur, resultats):
        print(f"🎮 Calcul pour {joueur['pseudo']}...")
        
        db = DatabaseManager()
        conn = None
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT type_joker 
                FROM jokers 
                WHERE utilisateur_id = ? 
                AND semaine_utilisation = ? 
                AND type_joker = 'points_doubles'
                AND utilise = 1
            """, (joueur['id'], self.semaine))
            
            joker_double = cursor.fetchone()
            
            cursor.execute("""
                SELECT p.id, p.match_id, p.score_domicile_prono, 
                       p.score_exterieur_prono, p.mise,
                       m.cote_domicile, m.cote_nul, m.cote_exterieur
                FROM pronostics p
                INNER JOIN matchs m ON p.match_id = m.id
                WHERE p.utilisateur_id = ? AND m.semaine = ?
                ORDER BY m.id
            """, (joueur['id'], self.semaine))
            
            pronos = cursor.fetchall()
            
            total_gains = 0
            scores_exacts = 0
            bons_pronos = 0
            
            for i, prono in enumerate(pronos):
                prono_id = prono[0]
                match_id = prono[1]
                score_dom_prono = prono[2]
                score_ext_prono = prono[3]
                mise = prono[4]
                cote_1 = prono[5]
                cote_n = prono[6]
                cote_2 = prono[7]
                
                resultat_reel = next((r for r in resultats if r["match_id"] == match_id), None)
                
                if not resultat_reel:
                    print(f"  ⚠️ Match {match_id} : résultat manquant")
                    continue
                
                score_dom_reel = resultat_reel["score_dom"]
                score_ext_reel = resultat_reel["score_ext"]
                
                gain = 0
                
                if score_dom_prono == score_dom_reel and score_ext_prono == score_ext_reel:
                    gain = 10
                    scores_exacts += 1
                    bons_pronos += 1
                    print(f"  🎯 Match {i+1}: Score exact ! +10 pts")
                else:
                    resultat_prono = self.get_results_dict(score_dom_prono, score_ext_prono)
                    resultat_reel_1n2 = self.get_results_dict(score_dom_reel, score_ext_reel)
                    
                    if resultat_prono == resultat_reel_1n2:
                        if resultat_prono == "1":
                            gain = mise * cote_1
                        elif resultat_prono == "N":
                            gain = mise * cote_n
                        else:
                            gain = mise * cote_2
                        
                        bons_pronos += 1
                        print(f"  ✅ Match {i+1}: Bon résultat ! +{gain:.2f} pts")
                    else:
                        print(f"  ❌ Match {i+1}: Échec (0 pt)")
                
                total_gains += gain
                
                cursor.execute("""
                    UPDATE pronostics
                    SET points_gagnes = ?
                    WHERE id = ?
                """, (gain, prono_id))
            
            grand_chelem = 1 if scores_exacts == 4 else 0
            
            if grand_chelem:
                total_gains += 40
                print(f"  🏆 GRAND CHELEM ! +40 points bonus")
            
            if joker_double:
                points_avant = total_gains
                total_gains = total_gains * 2
                print(f"  🃏 JOKER POINTS DOUBLES : {points_avant:.2f} × 2 = {total_gains:.2f} points")
            
            cursor.execute("""
                INSERT INTO historique 
                (utilisateur_id, semaine, points_totaux, scores_exacts, 
                 bons_pronos, grand_chelem)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (joueur['id'], self.semaine, total_gains, scores_exacts, 
                  bons_pronos, grand_chelem))
            
            conn.commit()
            
            print(f"  💰 TOTAL: {total_gains:.2f} points | "
                  f"Bons pronos: {bons_pronos}/4 | Scores exacts: {scores_exacts}/4\n")
            
        except Exception as e:
            print(f"❌ Erreur calcul pour {joueur['pseudo']}: {e}")
        finally:
            if conn:
=======
# calcul_gains.py - Module de calcul des gains

from modules.database_manager import DatabaseManager
import sqlite3

class CalculGains:
    
    def __init__(self, semaine):
        self.semaine = semaine
        print(f"✅ Module de calcul initialisé (Semaine {semaine})")
    
    def get_results_dict(self, score_dom, score_ext):
        if score_dom > score_ext:
            return "1"
        elif score_dom == score_ext:
            return "N"
        else:
            return "2"
    
    def calculer_pour_semaine(self, resultats):
        print(f"\n{'='*60}")
        print(f"🧮 CALCUL DES GAINS - SEMAINE {self.semaine}")
        print(f"{'='*60}")
        
        if len(resultats) != 4:
            print("❌ Erreur : Il faut exactement 4 résultats !")
            return
        
        self.update_match_results(resultats)
        joueurs = self.get_joueurs_avec_pronos()
        
        if not joueurs:
            print("❌ Aucun joueur n'a pronostiqué cette semaine !")
            return
        
        print(f"\n👥 {len(joueurs)} joueur(s) à traiter\n")
        
        for joueur in joueurs:
            self.calculer_pour_joueur(joueur, resultats)
        
        print(f"\n{'='*60}")
        print(f"✅ CALCUL TERMINÉ")
        print(f"{'='*60}\n")
    
    def update_match_results(self, resultats):
        db = DatabaseManager()
        conn = None
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            for res in resultats:
                cursor.execute("""
                    UPDATE matchs
                    SET score_domicile = ?, score_exterieur = ?, statut = 'termine'
                    WHERE id = ?
                """, (res["score_dom"], res["score_ext"], res["match_id"]))
            
            conn.commit()
            print("✅ Résultats réels enregistrés dans la table matchs")
            
        except Exception as e:
            print(f"❌ Erreur mise à jour matchs : {e}")
        finally:
            if conn:
                conn.close()
    
    def get_joueurs_avec_pronos(self):
        db = DatabaseManager()
        conn = None
        joueurs = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT DISTINCT u.id, u.pseudo
                FROM utilisateurs u
                INNER JOIN pronostics p ON u.id = p.utilisateur_id
                INNER JOIN matchs m ON p.match_id = m.id
                WHERE m.semaine = ?
            """, (self.semaine,))
            
            rows = cursor.fetchall()
            
            for row in rows:
                joueurs.append({"id": row[0], "pseudo": row[1]})
            
        except Exception as e:
            print(f"❌ Erreur récupération joueurs : {e}")
        finally:
            if conn:
                conn.close()
        
        return joueurs
    
    def calculer_pour_joueur(self, joueur, resultats):
        print(f"🎮 Calcul pour {joueur['pseudo']}...")
        
        db = DatabaseManager()
        conn = None
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT type_joker 
                FROM jokers 
                WHERE utilisateur_id = ? 
                AND semaine_utilisation = ? 
                AND type_joker = 'points_doubles'
                AND utilise = 1
            """, (joueur['id'], self.semaine))
            
            joker_double = cursor.fetchone()
            
            cursor.execute("""
                SELECT p.id, p.match_id, p.score_domicile_prono, 
                       p.score_exterieur_prono, p.mise,
                       m.cote_domicile, m.cote_nul, m.cote_exterieur
                FROM pronostics p
                INNER JOIN matchs m ON p.match_id = m.id
                WHERE p.utilisateur_id = ? AND m.semaine = ?
                ORDER BY m.id
            """, (joueur['id'], self.semaine))
            
            pronos = cursor.fetchall()
            
            total_gains = 0
            scores_exacts = 0
            bons_pronos = 0
            
            for i, prono in enumerate(pronos):
                prono_id = prono[0]
                match_id = prono[1]
                score_dom_prono = prono[2]
                score_ext_prono = prono[3]
                mise = prono[4]
                cote_1 = prono[5]
                cote_n = prono[6]
                cote_2 = prono[7]
                
                resultat_reel = next((r for r in resultats if r["match_id"] == match_id), None)
                
                if not resultat_reel:
                    print(f"  ⚠️ Match {match_id} : résultat manquant")
                    continue
                
                score_dom_reel = resultat_reel["score_dom"]
                score_ext_reel = resultat_reel["score_ext"]
                
                gain = 0
                
                if score_dom_prono == score_dom_reel and score_ext_prono == score_ext_reel:
                    gain = 10
                    scores_exacts += 1
                    bons_pronos += 1
                    print(f"  🎯 Match {i+1}: Score exact ! +10 pts")
                else:
                    resultat_prono = self.get_results_dict(score_dom_prono, score_ext_prono)
                    resultat_reel_1n2 = self.get_results_dict(score_dom_reel, score_ext_reel)
                    
                    if resultat_prono == resultat_reel_1n2:
                        if resultat_prono == "1":
                            gain = mise * cote_1
                        elif resultat_prono == "N":
                            gain = mise * cote_n
                        else:
                            gain = mise * cote_2
                        
                        bons_pronos += 1
                        print(f"  ✅ Match {i+1}: Bon résultat ! +{gain:.2f} pts")
                    else:
                        print(f"  ❌ Match {i+1}: Échec (0 pt)")
                
                total_gains += gain
                
                cursor.execute("""
                    UPDATE pronostics
                    SET points_gagnes = ?
                    WHERE id = ?
                """, (gain, prono_id))
            
            grand_chelem = 1 if scores_exacts == 4 else 0
            
            if grand_chelem:
                total_gains += 40
                print(f"  🏆 GRAND CHELEM ! +40 points bonus")
            
            if joker_double:
                points_avant = total_gains
                total_gains = total_gains * 2
                print(f"  🃏 JOKER POINTS DOUBLES : {points_avant:.2f} × 2 = {total_gains:.2f} points")
            
            cursor.execute("""
                INSERT INTO historique 
                (utilisateur_id, semaine, points_totaux, scores_exacts, 
                 bons_pronos, grand_chelem)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (joueur['id'], self.semaine, total_gains, scores_exacts, 
                  bons_pronos, grand_chelem))
            
            conn.commit()
            
            print(f"  💰 TOTAL: {total_gains:.2f} points | "
                  f"Bons pronos: {bons_pronos}/4 | Scores exacts: {scores_exacts}/4\n")
            
        except Exception as e:
            print(f"❌ Erreur calcul pour {joueur['pseudo']}: {e}")
        finally:
            if conn:
>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
                conn.close()