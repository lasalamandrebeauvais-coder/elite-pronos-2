import time
import schedule
from datetime import datetime, timedelta

from modules.database_manager import DatabaseManager
from modules.sourcing_bot import SourcingBot
from modules.notifications import SystemeNotifications
from modules.calcul_trophees import CalculTrophees
from modules.email_sender import EmailSender
from modules.generateur_resume import GenerateurResume

class DaemonAutomation:
    
    def __init__(self):
        self.db = DatabaseManager()
        print("🤖 Daemon d'automatisation Elite Pronos 2")
        print("="*70)
    
    def run(self):
        """
        Boucle principale du daemon
        """
        print(f"🚀 Démarrage du daemon - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("⏰ Vérifications toutes les heures")
        print("="*70 + "\n")
        
        # Planifier les vérifications toutes les heures
        schedule.every().hour.at(":00").do(self.verifier_actions)
        
        # Première vérification immédiate
        self.verifier_actions()
        
        # Boucle infinie
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    def verifier_actions(self):
        """
        Vérifie quelles actions doivent être exécutées
        """
        now = datetime.now()
        print(f"\n{'='*70}")
        print(f"🔍 VÉRIFICATION - {now.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"{'='*70}\n")
        
        self.verifier_sourcing()
        self.verifier_cloture()
        self.verifier_calcul()
        self.verifier_notifications()
        
        print(f"{'='*70}")
        print(f"✅ Vérification terminée\n")
    
    def verifier_sourcing(self):
        """
        Vérifie si le sourcing doit être lancé
        """
        print("📊 Vérification sourcing...")
        
        conn = None
        
        try:
            conn = self.db.create_connection()
            cursor = conn.cursor()
            
            now = datetime.now()
            
            cursor.execute("""
                SELECT semaine, date_premier_match, type_calendrier, delai_depuis_precedente
                FROM journees_calendrier
                WHERE statut = 'a_venir'
                AND sourcing_effectue = 0
                ORDER BY semaine
            """)
            
            rows = cursor.fetchall()
            
            for row in rows:
                semaine, date_match_str, type_cal, delai = row
                date_match = datetime.strptime(date_match_str, "%Y-%m-%d %H:%M:%S")
                
                if type_cal == "serre" or (delai and delai < 7):
                    cursor.execute("""
                        SELECT statut FROM journees_calendrier
                        WHERE semaine = ?
                    """, (semaine - 1,))
                    
                    precedente = cursor.fetchone()
                    
                    if precedente and precedente[0] == "terminee":
                        print(f"  🔥 Calendrier serré - Semaine {semaine}")
                        print(f"  🚀 Lancement sourcing")
                        self.executer_sourcing(semaine)
                        return
                
                else:
                    jours_avant = (date_match - now).days
                    
                    if 6 <= jours_avant <= 8:
                        print(f"  📅 Semaine {semaine} - J-{jours_avant}")
                        print(f"  🚀 Lancement sourcing")
                        self.executer_sourcing(semaine)
                        return
            
            print("  ℹ️ Aucun sourcing à effectuer")
        
        except Exception as e:
            print(f"  ❌ Erreur : {e}")
        
        finally:
            if conn:
                conn.close()
    
    def executer_sourcing(self, semaine):
        """
        Execute le sourcing
        """
        try:
            bot = SourcingBot()
            bot.run(semaine=semaine)
            
            conn = self.db.create_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE journees_calendrier
                SET sourcing_effectue = 1
                WHERE semaine = ?
            """, (semaine,))
            conn.commit()
            conn.close()
            
            self.envoyer_notification_sourcing(semaine)
            
            print(f"  ✅ Sourcing semaine {semaine} terminé")
        
        except Exception as e:
            print(f"  ❌ Erreur sourcing : {e}")
    
    def envoyer_notification_sourcing(self, semaine):
        """
        Notification nouvelle journée
        """
        print(f"  📧 Envoi notification nouvelle journée...")
        
        conn = None
        
        try:
            conn = self.db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT date_premier_match, date_cloture_pronos, type_calendrier
                FROM journees_calendrier
                WHERE semaine = ?
            """, (semaine,))
            
            row = cursor.fetchone()
            if not row:
                return
            
            date_match = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            date_cloture = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
            type_cal = row[2]
            
            cursor.execute("""
                SELECT id, pseudo, prenom, email
                FROM utilisateurs
                WHERE statut = 'actif' AND email IS NOT NULL
            """)
            
            joueurs = cursor.fetchall()
            
            email_sender = EmailSender()
            
            for joueur in joueurs:
                html = self.creer_email_sourcing(joueur, semaine, date_match, date_cloture, type_cal)
                
                try:
                    email_sender.envoyer_email(
                        joueur[3],
                        f"🎮 Elite Pronos 2 - Journée {semaine} disponible !",
                        html
                    )
                    print(f"    ✅ Email envoyé à {joueur[1]}")
                except Exception as e:
                    print(f"    ❌ Erreur pour {joueur[1]} : {e}")
        
        except Exception as e:
            print(f"  ❌ Erreur notification : {e}")
        
        finally:
            if conn:
                conn.close()
    
    def creer_email_sourcing(self, joueur, semaine, date_match, date_cloture, type_cal):
        """
        Template email nouvelle journée
        """
        alerte = ""
        if type_cal == "serre":
            alerte = """
            <div style="background-color: #FF6B6B; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <p style="font-size: 16px; font-weight: bold; color: white; margin: 0; text-align: center;">
                    🔥 CALENDRIER SERRÉ ! Fais vite tes pronos !
                </p>
            </div>
            """
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #0A1628; color: #FFFFFF; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #1A1A1A; border: 3px solid #FFD700; border-radius: 10px; padding: 30px;">
                <h1 style="text-align: center; color: #FFD700; font-size: 28px;">🎮 NOUVELLE JOURNÉE DISPONIBLE !</h1>
                <hr style="border: 2px solid #FFD700; margin: 20px 0;">
                
                <p style="font-size: 18px; color: #FFFFFF;">Salut <strong>{joueur[2] or joueur[1]}</strong> ! 👋</p>
                
                <p style="font-size: 16px; line-height: 1.8;">
                    La <strong>Journée {semaine}</strong> est maintenant disponible !<br>
                    Tu peux dès maintenant faire tes pronos.
                </p>
                
                {alerte}
                
                <div style="background-color: #2C2C2C; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h2 style="color: #FFD700; font-size: 20px; margin-top: 0;">📅 INFOS JOURNÉE {semaine}</h2>
                    <p style="font-size: 16px; line-height: 1.8;">
                        ⚽ <strong>1er match :</strong> {date_match.strftime('%A %d %B à %Hh%M')}<br>
                        🔒 <strong>Clôture :</strong> {date_cloture.strftime('%A %d %B à %Hh')}
                    </p>
                </div>
                
                <p style="text-align: center; margin-top: 30px;">
                    <a href="#" style="display: inline-block; background-color: #FFD700; color: black; padding: 15px 40px; text-decoration: none; border-radius: 8px; font-size: 18px; font-weight: bold;">
                        🎮 FAIRE MES PRONOS
                    </a>
                </p>
                
                <p style="text-align: center; margin-top: 20px; font-size: 12px; color: #888888;">
                    Elite Pronos 2 - Que le meilleur gagne ! 🏆
                </p>
            </div>
        </body>
        </html>
        """
        return html
    
    def verifier_cloture(self):
        """
        Vérifie si clôture à faire
        """
        print("🔒 Vérification clôture...")
        
        conn = None
        
        try:
            conn = self.db.create_connection()
            cursor = conn.cursor()
            
            now = datetime.now()
            
            cursor.execute("""
                SELECT semaine, date_cloture_pronos
                FROM journees_calendrier
                WHERE statut = 'a_venir'
                ORDER BY semaine
                LIMIT 1
            """)
            
            row = cursor.fetchone()
            
            if row:
                semaine, date_cloture_str = row
                date_cloture = datetime.strptime(date_cloture_str, "%Y-%m-%d %H:%M:%S")
                
                diff_minutes = (now - date_cloture).total_seconds() / 60
                
                if -5 <= diff_minutes <= 5:
                    print(f"  🔒 Heure de clôture - Semaine {semaine}")
                    self.executer_cloture(semaine)
                else:
                    minutes_restantes = (date_cloture - now).total_seconds() / 60
                    if minutes_restantes > 0:
                        print(f"  ℹ️ Clôture dans {int(minutes_restantes)} minutes")
                    else:
                        print(f"  ℹ️ Aucune clôture à effectuer")
            else:
                print("  ℹ️ Aucune journée à clôturer")
        
        except Exception as e:
            print(f"  ❌ Erreur : {e}")
        
        finally:
            if conn:
                conn.close()
    
    def executer_cloture(self, semaine):
        """
        Execute la clôture
        """
        try:
            import subprocess
            subprocess.run(["python", "modules/cloture_pronos.py", str(semaine)])
            
            conn = self.db.create_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE journees_calendrier
                SET statut = 'en_cours'
                WHERE semaine = ?
            """, (semaine,))
            conn.commit()
            conn.close()
            
            print(f"  ✅ Clôture semaine {semaine} effectuée")
        
        except Exception as e:
            print(f"  ❌ Erreur clôture : {e}")
    
    def verifier_calcul(self):
        """
        Vérifie si calcul à faire
        """
        print("💰 Vérification calcul...")
        
        conn = None
        
        try:
            conn = self.db.create_connection()
            cursor = conn.cursor()
            
            now = datetime.now()
            
            cursor.execute("""
                SELECT semaine, date_dernier_match
                FROM journees_calendrier
                WHERE statut = 'en_cours'
                ORDER BY semaine
            """)
            
            rows = cursor.fetchall()
            
            for row in rows:
                semaine, date_dernier_str = row
                date_dernier = datetime.strptime(date_dernier_str, "%Y-%m-%d %H:%M:%S")
                
                heures_apres = (now - date_dernier).total_seconds() / 3600
                
                if heures_apres >= 3:
                    cursor.execute("""
                        SELECT COUNT(*) FROM matchs
                        WHERE semaine = ? AND resultat IS NULL
                    """, (semaine,))
                    
                    matchs_sans_resultat = cursor.fetchone()[0]
                    
                    if matchs_sans_resultat == 0:
                        print(f"  💰 Tous les matchs terminés - Semaine {semaine}")
                        self.executer_calcul(semaine)
                    else:
                        print(f"  ⏳ {matchs_sans_resultat} match(s) sans résultat")
                else:
                    print(f"  ℹ️ Attente fin matchs (dans {int(3-heures_apres)}h)")
            
            if not rows:
                print("  ℹ️ Aucune journée en cours")
        
        except Exception as e:
            print(f"  ❌ Erreur : {e}")
        
        finally:
            if conn:
                conn.close()
    
    def executer_calcul(self, semaine):
        """
        Execute calcul complet
        """
        try:
            print(f"  💰 Calcul des gains...")
            bot = SourcingBot()
            bot.update_results(semaine=semaine)
            
            print(f"  🏆 Calcul des trophées...")
            calc = CalculTrophees(semaine)
            calc.calculer_trophees()
            
            print(f"  🎙️ Génération du résumé...")
            gen = GenerateurResume(semaine)
            resume = gen.generer_resume()
            
            print(f"  📧 Envoi des récaps...")
            sender = EmailSender()
            sender.envoyer_recap_semaine(semaine)
            
            conn = self.db.create_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE journees_calendrier
                SET statut = 'terminee'
                WHERE semaine = ?
            """, (semaine,))
            conn.commit()
            conn.close()
            
            print(f"  ✅ Workflow complet semaine {semaine} terminé")
        
        except Exception as e:
            print(f"  ❌ Erreur calcul : {e}")
    
    def verifier_notifications(self):
        """
        Vérifie notifications
        """
        print("📧 Vérification notifications...")
        
        try:
            notif = SystemeNotifications()
            notif.verifier_et_envoyer()
        except Exception as e:
            print(f"  ❌ Erreur notifications : {e}")

if __name__ == "__main__":
    daemon = DaemonAutomation()
    daemon.run()
