<<<<<<< HEAD
# sourcing_bot.py - Module de récupération des matchs

import requests
import sqlite3
from modules.database_manager import DatabaseManager
from datetime import datetime, timedelta

class SourcingBot:
    """
    Bot pour récupérer les matchs depuis Football-Data.org
    et sélectionner les 4 matchs les plus équilibrés.
    """
    
    def __init__(self):
        self.api_token = "bf58da6a49824f2a8742957b89ca52ee"
        self.base_url = "https://api.football-data.org/v4"
        self.headers = {"X-Auth-Token": self.api_token}
        
        # IDs des compétitions
        self.competitions = {
            "L1": 2015,           # Ligue 1 (France)
            "PL": 2021,           # Premier League (Angleterre)
            "LaLiga": 2014,       # La Liga (Espagne)
            "Bundesliga": 2002,   # Bundesliga (Allemagne)
            "SerieA": 2019        # Serie A (Italie)
        }
        
        print("✅ Bot de sourcing initialisé")
    
    def get_matches_week(self):
        """
        ÉTAPE 1 : Récupère les matchs PROGRAMMÉS (SCHEDULED).
        """
        print("\n🔍 ÉTAPE 1 : Récupération des matchs programmés...")
        
        all_matches = []
        
        date_from = datetime.now().strftime("%Y-%m-%d")
        date_to = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        
        for comp_name, comp_id in self.competitions.items():
            try:
                url = f"{self.base_url}/competitions/{comp_id}/matches"
                params = {
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "status": "SCHEDULED"
                }
                
                response = requests.get(url, headers=self.headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    matches = data.get("matches", [])
                    
                    print(f"  ✅ {comp_name}: {len(matches)} matchs programmés")
                    
                    for match in matches:
                        all_matches.append({
                            "competition": comp_name,
                            "domicile": match["homeTeam"]["name"],
                            "exterieur": match["awayTeam"]["name"],
                            "date": match["utcDate"],
                            "status": match["status"]
                        })
                else:
                    print(f"  ⚠️ {comp_name}: Erreur {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ Erreur pour {comp_name}: {e}")
        
        print(f"\n📊 Total SCHEDULED: {len(all_matches)} matchs")
        
        # ÉTAPE 2 : ROUE DE SECOURS si moins de 4 matchs
        if len(all_matches) < 4:
            print(f"\n⚠️ ÉTAPE 2 : Moins de 4 matchs trouvés, activation de la roue de secours...")
            all_matches.extend(self.get_backup_matches(4 - len(all_matches)))
        
        return all_matches
    
    def get_backup_matches(self, count):
        """
        ROUE DE SECOURS : Récupère des matchs équilibrés sans filtre de statut.
        """
        print(f"\n🔄 Recherche de {count} match(s) de secours...")
        
        backup_matches = []
        
        date_from = datetime.now().strftime("%Y-%m-%d")
        date_to = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        
        for comp_name, comp_id in self.competitions.items():
            if len(backup_matches) >= count:
                break
                
            try:
                url = f"{self.base_url}/competitions/{comp_id}/matches"
                params = {
                    "dateFrom": date_from,
                    "dateTo": date_to
                }
                
                response = requests.get(url, headers=self.headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    matches = data.get("matches", [])
                    
                    for match in matches:
                        if len(backup_matches) >= count:
                            break
                            
                        backup_matches.append({
                            "competition": comp_name,
                            "domicile": match["homeTeam"]["name"],
                            "exterieur": match["awayTeam"]["name"],
                            "date": match["utcDate"],
                            "status": match["status"]
                        })
                        
            except Exception as e:
                print(f"  ❌ Erreur backup {comp_name}: {e}")
        
        print(f"  ✅ {len(backup_matches)} match(s) de secours récupéré(s)")
        return backup_matches
    
    def get_odds_for_match(self, match):
        """
        Génère des cotes réalistes selon les règles du jeu.
        """
        import random
        
        cote_home = round(random.uniform(2.10, 2.60), 2)
        cote_away = round(random.uniform(2.40, 3.10), 2)
        cote_draw = round(random.uniform(3.00, 3.40), 2)
        
        return cote_home, cote_draw, cote_away
    
    def select_balanced_matches(self, matches, count=4):
        """
        ÉTAPE 3 : Sélectionne 4 matchs avec PRIORITÉ LIGUE 1.
        """
        print(f"\n🎯 ÉTAPE 3 : Sélection des {count} matchs (Priorité L1)...")
        
        import random
        
        matches_with_odds = []
        
        for match in matches:
            cote_home, cote_draw, cote_away = self.get_odds_for_match(match)
            
            ecart = abs(cote_home - cote_away)
            
            matches_with_odds.append({
                **match,
                "cote_1": cote_home,
                "cote_n": cote_draw,
                "cote_2": cote_away,
                "ecart": ecart
            })
        
        # Trie par écart (plus équilibrés en premier)
        matches_with_odds.sort(key=lambda m: m["ecart"])
        
        # Sépare L1 et autres
        l1_matches = [m for m in matches_with_odds if m["competition"] == "L1"]
        other_matches = [m for m in matches_with_odds if m["competition"] != "L1"]
        
        # Mélange pour variété
        random.shuffle(l1_matches)
        random.shuffle(other_matches)
        
        print(f"  📊 {len(l1_matches)} matchs L1 disponibles")
        print(f"  📊 {len(other_matches)} matchs autres ligues disponibles")
        
        # Sélection : Priorité L1, complément avec autres
        selected = l1_matches[:count]
        
        if len(selected) < count:
            selected.extend(other_matches[:count - len(selected)])
        
        print(f"\n✅ {len(selected)} matchs sélectionnés :")
        for m in selected:
            print(f"  • {m['competition']}: {m['domicile']} vs {m['exterieur']}")
        
        return selected[:count]
    
    def save_matches_to_db(self, matches, semaine):
        """
        ÉTAPE 4 : Enregistre les matchs dans la base de données.
        """
        print(f"\n💾 ÉTAPE 4 : Enregistrement des matchs (Semaine {semaine})...")
        
        db = DatabaseManager()
        conn = None
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            # Supprime les matchs de cette semaine
            cursor.execute("DELETE FROM matchs WHERE semaine = ?", (semaine,))
            print(f"  🗑️ Anciens matchs supprimés")
            
            for match in matches:
                cursor.execute("""
                    INSERT INTO matchs 
                    (semaine, equipe_domicile, equipe_exterieur, 
                     cote_domicile, cote_nul, cote_exterieur, 
                     date_match, statut)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'en_attente')
                """, (
                    semaine,
                    match["domicile"],
                    match["exterieur"],
                    match["cote_1"],
                    match["cote_n"],
                    match["cote_2"],
                    match["date"]
                ))
                
                print(f"  ✅ {match['competition']}: {match['domicile']} vs {match['exterieur']}")
                print(f"     Cotes: {match['cote_1']} / {match['cote_n']} / {match['cote_2']}")
            
            conn.commit()
            print(f"\n🎉 {len(matches)} matchs enregistrés avec succès !")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'enregistrement: {e}")
            
        finally:
            if conn:
                conn.close()
    
    def run(self, semaine=1):
        """
        Lance le processus complet de sourcing.
        """
        print("=" * 60)
        print("🤖 DÉMARRAGE DU BOT DE SOURCING")
        print("=" * 60)
        
        # 1. Récupère les matchs
        matches = self.get_matches_week()
        
        if not matches:
            print("❌ Aucun match trouvé !")
            return False
        
        # 2. Sélectionne les 4 plus équilibrés
        selected = self.select_balanced_matches(matches, count=4)
        
        # 3. Enregistre en base
        self.save_matches_to_db(selected, semaine)
        
        print("\n" + "=" * 60)
        print("✅ BOT DE SOURCING TERMINÉ")
        print("=" * 60)
        
        return True
    
    def update_results(self, semaine):
        """
        Récupère les résultats des matchs terminés et lance le calcul des gains.
        """
        print("\n" + "=" * 60)
        print(f"📊 MISE À JOUR DES RÉSULTATS - SEMAINE {semaine}")
        print("=" * 60)
        
        db = DatabaseManager()
        conn = None
        results_updated = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, equipe_domicile, equipe_exterieur, date_match
                FROM matchs
                WHERE semaine = ? AND statut = 'en_attente'
            """, (semaine,))
            
            matchs = cursor.fetchall()
            
            print(f"\n🔍 {len(matchs)} match(s) à vérifier...")
            
            for match in matchs:
                match_id = match[0]
                equipe_dom = match[1]
                equipe_ext = match[2]
                date_match = match[3]
                
                score_dom, score_ext = self.get_match_result(equipe_dom, equipe_ext, date_match)
                
                if score_dom is not None and score_ext is not None:
                    cursor.execute("""
                        UPDATE matchs
                        SET score_domicile = ?, score_exterieur = ?, statut = 'termine'
                        WHERE id = ?
                    """, (score_dom, score_ext, match_id))
                    
                    results_updated.append({
                        "match_id": match_id,
                        "score_dom": score_dom,
                        "score_ext": score_ext
                    })
                    
                    print(f"  ✅ {equipe_dom} {score_dom}-{score_ext} {equipe_ext}")
                else:
                    print(f"  ⏳ {equipe_dom} vs {equipe_ext} - Match non terminé")
            
            conn.commit()
            
            if len(results_updated) == 4:
                print(f"\n🎯 4 matchs terminés ! Lancement du calcul des gains...")
                self.launch_calculation(semaine, results_updated)
            else:
                print(f"\n⏳ Seulement {len(results_updated)}/4 matchs terminés")
            
        except Exception as e:
            print(f"❌ Erreur mise à jour résultats : {e}")
        
        finally:
            if conn:
                conn.close()
        
        print("\n" + "=" * 60)
        print("✅ MISE À JOUR TERMINÉE")
        print("=" * 60)
        
        return len(results_updated) == 4
    
    def get_match_result(self, equipe_dom, equipe_ext, date_match):
        """
        Cherche le résultat d'un match terminé dans l'API.
        """
        try:
            match_date = datetime.fromisoformat(date_match.replace("Z", "+00:00"))
            date_str = match_date.strftime("%Y-%m-%d")
            
            for comp_id in self.competitions.values():
                url = f"{self.base_url}/competitions/{comp_id}/matches"
                params = {
                    "dateFrom": date_str,
                    "dateTo": date_str,
                    "status": "FINISHED"
                }
                
                response = requests.get(url, headers=self.headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    matches = data.get("matches", [])
                    
                    for match in matches:
                        home = match["homeTeam"]["name"]
                        away = match["awayTeam"]["name"]
                        
                        if home == equipe_dom and away == equipe_ext:
                            score = match.get("score", {}).get("fullTime", {})
                            return score.get("home"), score.get("away")
            
            return None, None
            
        except Exception as e:
            print(f"    ⚠️ Erreur recherche résultat : {e}")
            return None, None
    
    def launch_calculation(self, semaine, results):
        """
        Lance le calcul des gains automatiquement.
        """
        try:
            from modules.calcul_gains import CalculGains
            
            print("\n" + "🧮" * 30)
            calc = CalculGains(semaine)
            calc.calculer_pour_semaine(results)
            print("🧮" * 30 + "\n")
            
        except Exception as e:
            print(f"❌ Erreur lancement calcul : {e}")


if __name__ == "__main__":
    bot = SourcingBot()
=======
# sourcing_bot.py - Module de récupération des matchs

import requests
import sqlite3
from modules.database_manager import DatabaseManager
from datetime import datetime, timedelta

class SourcingBot:
    """
    Bot pour récupérer les matchs depuis Football-Data.org
    et sélectionner les 4 matchs les plus équilibrés.
    """
    
    def __init__(self):
        self.api_token = "bf58da6a49824f2a8742957b89ca52ee"
        self.base_url = "https://api.football-data.org/v4"
        self.headers = {"X-Auth-Token": self.api_token}
        
        # IDs des compétitions
        self.competitions = {
            "L1": 2015,           # Ligue 1 (France)
            "PL": 2021,           # Premier League (Angleterre)
            "LaLiga": 2014,       # La Liga (Espagne)
            "Bundesliga": 2002,   # Bundesliga (Allemagne)
            "SerieA": 2019        # Serie A (Italie)
        }
        
        print("✅ Bot de sourcing initialisé")
    
    def get_matches_week(self):
        """
        ÉTAPE 1 : Récupère les matchs PROGRAMMÉS (SCHEDULED).
        """
        print("\n🔍 ÉTAPE 1 : Récupération des matchs programmés...")
        
        all_matches = []
        
        date_from = datetime.now().strftime("%Y-%m-%d")
        date_to = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        
        for comp_name, comp_id in self.competitions.items():
            try:
                url = f"{self.base_url}/competitions/{comp_id}/matches"
                params = {
                    "dateFrom": date_from,
                    "dateTo": date_to,
                    "status": "SCHEDULED"
                }
                
                response = requests.get(url, headers=self.headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    matches = data.get("matches", [])
                    
                    print(f"  ✅ {comp_name}: {len(matches)} matchs programmés")
                    
                    for match in matches:
                        all_matches.append({
                            "competition": comp_name,
                            "domicile": match["homeTeam"]["name"],
                            "exterieur": match["awayTeam"]["name"],
                            "date": match["utcDate"],
                            "status": match["status"]
                        })
                else:
                    print(f"  ⚠️ {comp_name}: Erreur {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ Erreur pour {comp_name}: {e}")
        
        print(f"\n📊 Total SCHEDULED: {len(all_matches)} matchs")
        
        # ÉTAPE 2 : ROUE DE SECOURS si moins de 4 matchs
        if len(all_matches) < 4:
            print(f"\n⚠️ ÉTAPE 2 : Moins de 4 matchs trouvés, activation de la roue de secours...")
            all_matches.extend(self.get_backup_matches(4 - len(all_matches)))
        
        return all_matches
    
    def get_backup_matches(self, count):
        """
        ROUE DE SECOURS : Récupère des matchs équilibrés sans filtre de statut.
        """
        print(f"\n🔄 Recherche de {count} match(s) de secours...")
        
        backup_matches = []
        
        date_from = datetime.now().strftime("%Y-%m-%d")
        date_to = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        
        for comp_name, comp_id in self.competitions.items():
            if len(backup_matches) >= count:
                break
                
            try:
                url = f"{self.base_url}/competitions/{comp_id}/matches"
                params = {
                    "dateFrom": date_from,
                    "dateTo": date_to
                }
                
                response = requests.get(url, headers=self.headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    matches = data.get("matches", [])
                    
                    for match in matches:
                        if len(backup_matches) >= count:
                            break
                            
                        backup_matches.append({
                            "competition": comp_name,
                            "domicile": match["homeTeam"]["name"],
                            "exterieur": match["awayTeam"]["name"],
                            "date": match["utcDate"],
                            "status": match["status"]
                        })
                        
            except Exception as e:
                print(f"  ❌ Erreur backup {comp_name}: {e}")
        
        print(f"  ✅ {len(backup_matches)} match(s) de secours récupéré(s)")
        return backup_matches
    
    def get_odds_for_match(self, match):
        """
        Génère des cotes réalistes selon les règles du jeu.
        """
        import random
        
        cote_home = round(random.uniform(2.10, 2.60), 2)
        cote_away = round(random.uniform(2.40, 3.10), 2)
        cote_draw = round(random.uniform(3.00, 3.40), 2)
        
        return cote_home, cote_draw, cote_away
    
    def select_balanced_matches(self, matches, count=4):
        """
        ÉTAPE 3 : Sélectionne 4 matchs avec PRIORITÉ LIGUE 1.
        """
        print(f"\n🎯 ÉTAPE 3 : Sélection des {count} matchs (Priorité L1)...")
        
        import random
        
        matches_with_odds = []
        
        for match in matches:
            cote_home, cote_draw, cote_away = self.get_odds_for_match(match)
            
            ecart = abs(cote_home - cote_away)
            
            matches_with_odds.append({
                **match,
                "cote_1": cote_home,
                "cote_n": cote_draw,
                "cote_2": cote_away,
                "ecart": ecart
            })
        
        # Trie par écart (plus équilibrés en premier)
        matches_with_odds.sort(key=lambda m: m["ecart"])
        
        # Sépare L1 et autres
        l1_matches = [m for m in matches_with_odds if m["competition"] == "L1"]
        other_matches = [m for m in matches_with_odds if m["competition"] != "L1"]
        
        # Mélange pour variété
        random.shuffle(l1_matches)
        random.shuffle(other_matches)
        
        print(f"  📊 {len(l1_matches)} matchs L1 disponibles")
        print(f"  📊 {len(other_matches)} matchs autres ligues disponibles")
        
        # Sélection : Priorité L1, complément avec autres
        selected = l1_matches[:count]
        
        if len(selected) < count:
            selected.extend(other_matches[:count - len(selected)])
        
        print(f"\n✅ {len(selected)} matchs sélectionnés :")
        for m in selected:
            print(f"  • {m['competition']}: {m['domicile']} vs {m['exterieur']}")
        
        return selected[:count]
    
    def save_matches_to_db(self, matches, semaine):
        """
        ÉTAPE 4 : Enregistre les matchs dans la base de données.
        """
        print(f"\n💾 ÉTAPE 4 : Enregistrement des matchs (Semaine {semaine})...")
        
        db = DatabaseManager()
        conn = None
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            # Supprime les matchs de cette semaine
            cursor.execute("DELETE FROM matchs WHERE semaine = ?", (semaine,))
            print(f"  🗑️ Anciens matchs supprimés")
            
            for match in matches:
                cursor.execute("""
                    INSERT INTO matchs 
                    (semaine, equipe_domicile, equipe_exterieur, 
                     cote_domicile, cote_nul, cote_exterieur, 
                     date_match, statut)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'en_attente')
                """, (
                    semaine,
                    match["domicile"],
                    match["exterieur"],
                    match["cote_1"],
                    match["cote_n"],
                    match["cote_2"],
                    match["date"]
                ))
                
                print(f"  ✅ {match['competition']}: {match['domicile']} vs {match['exterieur']}")
                print(f"     Cotes: {match['cote_1']} / {match['cote_n']} / {match['cote_2']}")
            
            conn.commit()
            print(f"\n🎉 {len(matches)} matchs enregistrés avec succès !")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'enregistrement: {e}")
            
        finally:
            if conn:
                conn.close()
    
    def run(self, semaine=1):
        """
        Lance le processus complet de sourcing.
        """
        print("=" * 60)
        print("🤖 DÉMARRAGE DU BOT DE SOURCING")
        print("=" * 60)
        
        # 1. Récupère les matchs
        matches = self.get_matches_week()
        
        if not matches:
            print("❌ Aucun match trouvé !")
            return False
        
        # 2. Sélectionne les 4 plus équilibrés
        selected = self.select_balanced_matches(matches, count=4)
        
        # 3. Enregistre en base
        self.save_matches_to_db(selected, semaine)
        
        print("\n" + "=" * 60)
        print("✅ BOT DE SOURCING TERMINÉ")
        print("=" * 60)
        
        return True
    
    def update_results(self, semaine):
        """
        Récupère les résultats des matchs terminés et lance le calcul des gains.
        """
        print("\n" + "=" * 60)
        print(f"📊 MISE À JOUR DES RÉSULTATS - SEMAINE {semaine}")
        print("=" * 60)
        
        db = DatabaseManager()
        conn = None
        results_updated = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, equipe_domicile, equipe_exterieur, date_match
                FROM matchs
                WHERE semaine = ? AND statut = 'en_attente'
            """, (semaine,))
            
            matchs = cursor.fetchall()
            
            print(f"\n🔍 {len(matchs)} match(s) à vérifier...")
            
            for match in matchs:
                match_id = match[0]
                equipe_dom = match[1]
                equipe_ext = match[2]
                date_match = match[3]
                
                score_dom, score_ext = self.get_match_result(equipe_dom, equipe_ext, date_match)
                
                if score_dom is not None and score_ext is not None:
                    cursor.execute("""
                        UPDATE matchs
                        SET score_domicile = ?, score_exterieur = ?, statut = 'termine'
                        WHERE id = ?
                    """, (score_dom, score_ext, match_id))
                    
                    results_updated.append({
                        "match_id": match_id,
                        "score_dom": score_dom,
                        "score_ext": score_ext
                    })
                    
                    print(f"  ✅ {equipe_dom} {score_dom}-{score_ext} {equipe_ext}")
                else:
                    print(f"  ⏳ {equipe_dom} vs {equipe_ext} - Match non terminé")
            
            conn.commit()
            
            if len(results_updated) == 4:
                print(f"\n🎯 4 matchs terminés ! Lancement du calcul des gains...")
                self.launch_calculation(semaine, results_updated)
            else:
                print(f"\n⏳ Seulement {len(results_updated)}/4 matchs terminés")
            
        except Exception as e:
            print(f"❌ Erreur mise à jour résultats : {e}")
        
        finally:
            if conn:
                conn.close()
        
        print("\n" + "=" * 60)
        print("✅ MISE À JOUR TERMINÉE")
        print("=" * 60)
        
        return len(results_updated) == 4
    
    def get_match_result(self, equipe_dom, equipe_ext, date_match):
        """
        Cherche le résultat d'un match terminé dans l'API.
        """
        try:
            match_date = datetime.fromisoformat(date_match.replace("Z", "+00:00"))
            date_str = match_date.strftime("%Y-%m-%d")
            
            for comp_id in self.competitions.values():
                url = f"{self.base_url}/competitions/{comp_id}/matches"
                params = {
                    "dateFrom": date_str,
                    "dateTo": date_str,
                    "status": "FINISHED"
                }
                
                response = requests.get(url, headers=self.headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    matches = data.get("matches", [])
                    
                    for match in matches:
                        home = match["homeTeam"]["name"]
                        away = match["awayTeam"]["name"]
                        
                        if home == equipe_dom and away == equipe_ext:
                            score = match.get("score", {}).get("fullTime", {})
                            return score.get("home"), score.get("away")
            
            return None, None
            
        except Exception as e:
            print(f"    ⚠️ Erreur recherche résultat : {e}")
            return None, None
    
    def launch_calculation(self, semaine, results):
        """
        Lance le calcul des gains automatiquement.
        """
        try:
            from modules.calcul_gains import CalculGains
            
            print("\n" + "🧮" * 30)
            calc = CalculGains(semaine)
            calc.calculer_pour_semaine(results)
            print("🧮" * 30 + "\n")
            
        except Exception as e:
            print(f"❌ Erreur lancement calcul : {e}")


if __name__ == "__main__":
    bot = SourcingBot()
>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
    bot.run(semaine=1)