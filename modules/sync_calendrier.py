<<<<<<< HEAD
import requests
from datetime import datetime, timedelta

try:
    from modules.database_manager import DatabaseManager
    from modules.config import API_KEY
except:
    from database_manager import DatabaseManager
    from config import API_KEY

class SyncCalendrier:
    
    def __init__(self):
        self.api_key = API_KEY
        self.league_id = 2015  # Ligue 1
        self.base_url = "https://api.football-data.org/v4"
        print("📅 Synchronisation du calendrier initialisée")
    
    def synchroniser_saison(self, saison="2024"):
        """
        Récupère tout le calendrier de la saison et remplit la table journees_calendrier
        """
        print(f"\n{'='*70}")
        print(f"📅 SYNCHRONISATION CALENDRIER LIGUE 1 - SAISON {saison}")
        print(f"{'='*70}\n")
        
        # Récupérer tous les matchs de la saison
        matchs = self.get_matchs_saison()
        
        if not matchs:
            print("❌ Impossible de récupérer le calendrier")
            return
        
        # Organiser par journée
        journees = self.organiser_par_journee(matchs)
        
        # Calculer les deadlines et enregistrer
        self.enregistrer_journees(journees)
        
        print(f"\n{'='*70}")
        print("✅ SYNCHRONISATION TERMINÉE")
        print(f"{'='*70}\n")
    
    def get_matchs_saison(self):
        """
        Récupère tous les matchs de Ligue 1 pour la saison
        """
        print("🔍 Récupération du calendrier via API...")
        
        headers = {"X-Auth-Token": self.api_key}
        url = f"{self.base_url}/competitions/{self.league_id}/matches"
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                matchs = data.get("matches", [])
                print(f"✅ {len(matchs)} matchs récupérés")
                return matchs
            else:
                print(f"❌ Erreur API : {response.status_code}")
                return []
        
        except Exception as e:
            print(f"❌ Erreur : {e}")
            return []
    
    def organiser_par_journee(self, matchs):
        """
        Organise les matchs par journée (matchday)
        """
        print("📊 Organisation par journée...")
        
        journees = {}
        
        for match in matchs:
            matchday = match.get("matchday")
            date_str = match.get("utcDate")
            
            if not matchday or not date_str:
                continue
            
            # Convertir la date
            date_match = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            
            if matchday not in journees:
                journees[matchday] = []
            
            journees[matchday].append(date_match)
        
        print(f"✅ {len(journees)} journées identifiées")
        return journees
    
    def enregistrer_journees(self, journees):
        """
        Enregistre les journées dans la table avec calcul des deadlines
        """
        print("💾 Enregistrement dans la base de données...")
        
        db = DatabaseManager()
        conn = None
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            # Supprimer les anciennes données
            cursor.execute("DELETE FROM journees_calendrier")
            
            journees_triees = sorted(journees.items())
            date_precedente = None
            
            for semaine, dates_matchs in journees_triees:
                # Trier les dates
                dates_matchs.sort()
                
                date_premier_match = dates_matchs[0]
                date_dernier_match = dates_matchs[-1]
                
                # Calculer la date de clôture : 1 jour avant le 1er match à 20h
                date_cloture = date_premier_match - timedelta(days=1)
                date_cloture = date_cloture.replace(hour=20, minute=0, second=0)
                
                # Calculer le délai depuis la journée précédente
                delai = None
                type_calendrier = "normal"
                
                if date_precedente:
                    delai = (date_premier_match - date_precedente).days
                    if delai < 7:
                        type_calendrier = "serre"
                
                # Déterminer le statut
                now = datetime.now()
                if date_dernier_match < now:
                    statut = "terminee"
                elif date_premier_match < now:
                    statut = "en_cours"
                else:
                    statut = "a_venir"
                
                # Insérer dans la base
                cursor.execute("""
                    INSERT INTO journees_calendrier 
                    (semaine, date_premier_match, date_cloture_pronos, date_dernier_match, 
                     delai_depuis_precedente, type_calendrier, statut)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    semaine,
                    date_premier_match.strftime("%Y-%m-%d %H:%M:%S"),
                    date_cloture.strftime("%Y-%m-%d %H:%M:%S"),
                    date_dernier_match.strftime("%Y-%m-%d %H:%M:%S"),
                    delai,
                    type_calendrier,
                    statut
                ))
                
                # Afficher
                delai_str = f"{delai}j" if delai else "N/A"
                type_icon = "🔥" if type_calendrier == "serre" else "📅"
                print(f"  {type_icon} Semaine {semaine:2d} : {date_premier_match.strftime('%d/%m')} | Clôture : {date_cloture.strftime('%d/%m 20h')} | Délai : {delai_str}")
                
                date_precedente = date_dernier_match
            
            conn.commit()
            print(f"\n✅ {len(journees)} journées enregistrées")
        
        except Exception as e:
            print(f"❌ Erreur : {e}")
        
        finally:
            if conn:
                conn.close()
    
    def afficher_calendrier(self):
        """
        Affiche le calendrier enregistré
        """
        db = DatabaseManager()
        conn = None
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT semaine, date_premier_match, date_cloture_pronos, 
                       delai_depuis_precedente, type_calendrier, statut
                FROM journees_calendrier
                ORDER BY semaine
            """)
            
            rows = cursor.fetchall()
            
            print(f"\n{'='*80}")
            print(f"📅 CALENDRIER LIGUE 1 - {len(rows)} JOURNÉES")
            print(f"{'='*80}")
            print(f"{'Sem':>4} | {'1er match':^16} | {'Clôture':^16} | {'Délai':>6} | {'Type':^8} | {'Statut':^10}")
            print(f"{'-'*80}")
            
            for row in rows:
                semaine, date_match, date_cloture, delai, type_cal, statut = row
                
                date_match_dt = datetime.strptime(date_match, "%Y-%m-%d %H:%M:%S")
                date_cloture_dt = datetime.strptime(date_cloture, "%Y-%m-%d %H:%M:%S")
                
                delai_str = f"{delai}j" if delai else "N/A"
                type_icon = "🔥" if type_cal == "serre" else "📅"
                
                print(f"{semaine:4d} | {date_match_dt.strftime('%d/%m/%Y %H:%M'):16} | "
                      f"{date_cloture_dt.strftime('%d/%m/%Y 20h'):16} | "
                      f"{delai_str:>6} | {type_icon} {type_cal:6} | {statut:^10}")
            
            print(f"{'='*80}\n")
        
        except Exception as e:
            print(f"❌ Erreur : {e}")
        
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    import sys
    
    sync = SyncCalendrier()
    
    if len(sys.argv) > 1 and sys.argv[1] == "afficher":
        sync.afficher_calendrier()
    else:
        sync.synchroniser_saison()
        sync.afficher_calendrier()
=======
import requests
from datetime import datetime, timedelta

try:
    from modules.database_manager import DatabaseManager
    from modules.config import API_KEY
except:
    from database_manager import DatabaseManager
    from config import API_KEY

class SyncCalendrier:
    
    def __init__(self):
        self.api_key = API_KEY
        self.league_id = 2015  # Ligue 1
        self.base_url = "https://api.football-data.org/v4"
        print("📅 Synchronisation du calendrier initialisée")
    
    def synchroniser_saison(self, saison="2024"):
        """
        Récupère tout le calendrier de la saison et remplit la table journees_calendrier
        """
        print(f"\n{'='*70}")
        print(f"📅 SYNCHRONISATION CALENDRIER LIGUE 1 - SAISON {saison}")
        print(f"{'='*70}\n")
        
        # Récupérer tous les matchs de la saison
        matchs = self.get_matchs_saison()
        
        if not matchs:
            print("❌ Impossible de récupérer le calendrier")
            return
        
        # Organiser par journée
        journees = self.organiser_par_journee(matchs)
        
        # Calculer les deadlines et enregistrer
        self.enregistrer_journees(journees)
        
        print(f"\n{'='*70}")
        print("✅ SYNCHRONISATION TERMINÉE")
        print(f"{'='*70}\n")
    
    def get_matchs_saison(self):
        """
        Récupère tous les matchs de Ligue 1 pour la saison
        """
        print("🔍 Récupération du calendrier via API...")
        
        headers = {"X-Auth-Token": self.api_key}
        url = f"{self.base_url}/competitions/{self.league_id}/matches"
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                matchs = data.get("matches", [])
                print(f"✅ {len(matchs)} matchs récupérés")
                return matchs
            else:
                print(f"❌ Erreur API : {response.status_code}")
                return []
        
        except Exception as e:
            print(f"❌ Erreur : {e}")
            return []
    
    def organiser_par_journee(self, matchs):
        """
        Organise les matchs par journée (matchday)
        """
        print("📊 Organisation par journée...")
        
        journees = {}
        
        for match in matchs:
            matchday = match.get("matchday")
            date_str = match.get("utcDate")
            
            if not matchday or not date_str:
                continue
            
            # Convertir la date
            date_match = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            
            if matchday not in journees:
                journees[matchday] = []
            
            journees[matchday].append(date_match)
        
        print(f"✅ {len(journees)} journées identifiées")
        return journees
    
    def enregistrer_journees(self, journees):
        """
        Enregistre les journées dans la table avec calcul des deadlines
        """
        print("💾 Enregistrement dans la base de données...")
        
        db = DatabaseManager()
        conn = None
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            # Supprimer les anciennes données
            cursor.execute("DELETE FROM journees_calendrier")
            
            journees_triees = sorted(journees.items())
            date_precedente = None
            
            for semaine, dates_matchs in journees_triees:
                # Trier les dates
                dates_matchs.sort()
                
                date_premier_match = dates_matchs[0]
                date_dernier_match = dates_matchs[-1]
                
                # Calculer la date de clôture : 1 jour avant le 1er match à 20h
                date_cloture = date_premier_match - timedelta(days=1)
                date_cloture = date_cloture.replace(hour=20, minute=0, second=0)
                
                # Calculer le délai depuis la journée précédente
                delai = None
                type_calendrier = "normal"
                
                if date_precedente:
                    delai = (date_premier_match - date_precedente).days
                    if delai < 7:
                        type_calendrier = "serre"
                
                # Déterminer le statut
                now = datetime.now()
                if date_dernier_match < now:
                    statut = "terminee"
                elif date_premier_match < now:
                    statut = "en_cours"
                else:
                    statut = "a_venir"
                
                # Insérer dans la base
                cursor.execute("""
                    INSERT INTO journees_calendrier 
                    (semaine, date_premier_match, date_cloture_pronos, date_dernier_match, 
                     delai_depuis_precedente, type_calendrier, statut)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    semaine,
                    date_premier_match.strftime("%Y-%m-%d %H:%M:%S"),
                    date_cloture.strftime("%Y-%m-%d %H:%M:%S"),
                    date_dernier_match.strftime("%Y-%m-%d %H:%M:%S"),
                    delai,
                    type_calendrier,
                    statut
                ))
                
                # Afficher
                delai_str = f"{delai}j" if delai else "N/A"
                type_icon = "🔥" if type_calendrier == "serre" else "📅"
                print(f"  {type_icon} Semaine {semaine:2d} : {date_premier_match.strftime('%d/%m')} | Clôture : {date_cloture.strftime('%d/%m 20h')} | Délai : {delai_str}")
                
                date_precedente = date_dernier_match
            
            conn.commit()
            print(f"\n✅ {len(journees)} journées enregistrées")
        
        except Exception as e:
            print(f"❌ Erreur : {e}")
        
        finally:
            if conn:
                conn.close()
    
    def afficher_calendrier(self):
        """
        Affiche le calendrier enregistré
        """
        db = DatabaseManager()
        conn = None
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT semaine, date_premier_match, date_cloture_pronos, 
                       delai_depuis_precedente, type_calendrier, statut
                FROM journees_calendrier
                ORDER BY semaine
            """)
            
            rows = cursor.fetchall()
            
            print(f"\n{'='*80}")
            print(f"📅 CALENDRIER LIGUE 1 - {len(rows)} JOURNÉES")
            print(f"{'='*80}")
            print(f"{'Sem':>4} | {'1er match':^16} | {'Clôture':^16} | {'Délai':>6} | {'Type':^8} | {'Statut':^10}")
            print(f"{'-'*80}")
            
            for row in rows:
                semaine, date_match, date_cloture, delai, type_cal, statut = row
                
                date_match_dt = datetime.strptime(date_match, "%Y-%m-%d %H:%M:%S")
                date_cloture_dt = datetime.strptime(date_cloture, "%Y-%m-%d %H:%M:%S")
                
                delai_str = f"{delai}j" if delai else "N/A"
                type_icon = "🔥" if type_cal == "serre" else "📅"
                
                print(f"{semaine:4d} | {date_match_dt.strftime('%d/%m/%Y %H:%M'):16} | "
                      f"{date_cloture_dt.strftime('%d/%m/%Y 20h'):16} | "
                      f"{delai_str:>6} | {type_icon} {type_cal:6} | {statut:^10}")
            
            print(f"{'='*80}\n")
        
        except Exception as e:
            print(f"❌ Erreur : {e}")
        
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    import sys
    
    sync = SyncCalendrier()
    
    if len(sys.argv) > 1 and sys.argv[1] == "afficher":
        sync.afficher_calendrier()
    else:
        sync.synchroniser_saison()
        sync.afficher_calendrier()
>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
