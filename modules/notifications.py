<<<<<<< HEAD
from datetime import datetime, timedelta

try:
    from modules.database_manager import DatabaseManager
    from modules.email_sender import EmailSender
except:
    from database_manager import DatabaseManager
    from email_sender import EmailSender

class SystemeNotifications:
    
    def __init__(self):
        self.email_sender = EmailSender()
        print("📧 Système de notifications initialisé")
    
    def verifier_et_envoyer(self):
        """
        Vérifie l'état du calendrier et envoie les notifications nécessaires
        """
        print(f"\n{'='*70}")
        print(f"📧 VÉRIFICATION DES NOTIFICATIONS")
        print(f"{'='*70}\n")
        
        now = datetime.now()
        
        # Récupérer la prochaine journée à venir
        prochaine_journee = self.get_prochaine_journee()
        
        if not prochaine_journee:
            print("ℹ️ Aucune journée à venir")
            return
        
        semaine = prochaine_journee['semaine']
        date_cloture = datetime.strptime(prochaine_journee['date_cloture_pronos'], "%Y-%m-%d %H:%M:%S")
        date_premier_match = datetime.strptime(prochaine_journee['date_premier_match'], "%Y-%m-%d %H:%M:%S")
        type_calendrier = prochaine_journee['type_calendrier']
        
        print(f"📅 Prochaine journée : Semaine {semaine}")
        print(f"🔒 Clôture : {date_cloture.strftime('%d/%m/%Y à %Hh')}")
        print(f"⚽ 1er match : {date_premier_match.strftime('%d/%m/%Y à %Hh%M')}")
        print(f"🔥 Type : {type_calendrier}")
        
        # Calculer les délais
        heures_avant_cloture = (date_cloture - now).total_seconds() / 3600
        
        # Notification 1 : Sourcing effectué (déjà faite par le daemon)
        
        # Notification 2 : J-2 (48h avant)
        if 47 <= heures_avant_cloture <= 49 and not prochaine_journee['notification_j2_envoyee']:
            print("\n⏰ ENVOI NOTIFICATION J-2")
            self.envoyer_notification_j2(semaine, date_cloture, date_premier_match, type_calendrier)
            self.marquer_notification(semaine, 'j2')
        
        # Notification 3 : J-1 (24h avant)
        elif 23 <= heures_avant_cloture <= 25 and not prochaine_journee['notification_j1_envoyee']:
            print("\n⏰ ENVOI NOTIFICATION J-1")
            self.envoyer_notification_j1(semaine, date_cloture, date_premier_match, type_calendrier)
            self.marquer_notification(semaine, 'j1')
        
        # Notification 4 : 2h avant clôture
        elif 1.9 <= heures_avant_cloture <= 2.1 and not prochaine_journee['notification_2h_envoyee']:
            print("\n🚨 ENVOI NOTIFICATION DERNIÈRE CHANCE")
            self.envoyer_notification_2h(semaine, date_cloture, date_premier_match, type_calendrier)
            self.marquer_notification(semaine, '2h')
        
        else:
            print(f"ℹ️ Aucune notification à envoyer (dans {heures_avant_cloture:.1f}h)")
        
        print(f"\n{'='*70}\n")
    
    def get_prochaine_journee(self):
        """
        Récupère la prochaine journée à venir
        """
        db = DatabaseManager()
        conn = None
        journee = None
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT semaine, date_premier_match, date_cloture_pronos, 
                       type_calendrier, notification_j2_envoyee, 
                       notification_j1_envoyee, notification_2h_envoyee
                FROM journees_calendrier
                WHERE statut = 'a_venir'
                ORDER BY semaine
                LIMIT 1
            """)
            
            row = cursor.fetchone()
            
            if row:
                journee = {
                    'semaine': row[0],
                    'date_premier_match': row[1],
                    'date_cloture_pronos': row[2],
                    'type_calendrier': row[3],
                    'notification_j2_envoyee': row[4],
                    'notification_j1_envoyee': row[5],
                    'notification_2h_envoyee': row[6]
                }
        
        except Exception as e:
            print(f"❌ Erreur : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return journee
    
    def envoyer_notification_j2(self, semaine, date_cloture, date_premier_match, type_calendrier):
        """
        Notification J-2 : Plus que 2 jours
        """
        joueurs = self.get_joueurs_actifs()
        
        for joueur in joueurs:
            html = self.creer_email_j2(joueur, semaine, date_cloture, date_premier_match, type_calendrier)
            
            try:
                self.email_sender.envoyer_email(
                    joueur['email'],
                    f"⏰ Elite Pronos 2 - Journée {semaine} dans 2 jours !",
                    html
                )
                print(f"  ✅ Email J-2 envoyé à {joueur['pseudo']}")
            except Exception as e:
                print(f"  ❌ Erreur pour {joueur['pseudo']} : {e}")
    
    def envoyer_notification_j1(self, semaine, date_cloture, date_premier_match, type_calendrier):
        """
        Notification J-1 : Dernière journée + liste des joueurs sans pronos
        """
        joueurs_sans_pronos = self.get_joueurs_sans_pronos(semaine)
        
        for joueur in joueurs_sans_pronos:
            html = self.creer_email_j1(joueur, semaine, date_cloture, date_premier_match, type_calendrier)
            
            try:
                self.email_sender.envoyer_email(
                    joueur['email'],
                    f"🔥 Elite Pronos 2 - DERNIÈRE CHANCE Journée {semaine} !",
                    html
                )
                print(f"  ✅ Email J-1 envoyé à {joueur['pseudo']}")
            except Exception as e:
                print(f"  ❌ Erreur pour {joueur['pseudo']} : {e}")
    
    def envoyer_notification_2h(self, semaine, date_cloture, date_premier_match, type_calendrier):
        """
        Notification 2h avant : URGENCE pour ceux qui n'ont pas fait leurs pronos
        """
        joueurs_sans_pronos = self.get_joueurs_sans_pronos(semaine)
        
        for joueur in joueurs_sans_pronos:
            html = self.creer_email_2h(joueur, semaine, date_cloture, date_premier_match, type_calendrier)
            
            try:
                self.email_sender.envoyer_email(
                    joueur['email'],
                    f"🚨🚨 Elite Pronos 2 - URGENT ! 2H AVANT CLÔTURE !",
                    html
                )
                print(f"  ✅ Email 2H envoyé à {joueur['pseudo']}")
            except Exception as e:
                print(f"  ❌ Erreur pour {joueur['pseudo']} : {e}")
    
    def creer_email_j2(self, joueur, semaine, date_cloture, date_premier_match, type_calendrier):
        """
        Template email J-2
        """
        alerte = ""
        if type_calendrier == "serre":
            alerte = """
            <div style="background-color: #FF6B6B; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <p style="font-size: 16px; font-weight: bold; color: white; margin: 0;">
                    🔥 CALENDRIER SERRÉ ! Ne tardez pas !
                </p>
            </div>
            """
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #0A1628; color: #FFFFFF; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #1A1A1A; border: 3px solid #FFD700; border-radius: 10px; padding: 30px;">
                <h1 style="text-align: center; color: #FFD700; font-size: 28px;">⏰ PLUS QUE 2 JOURS !</h1>
                <hr style="border: 2px solid #FFD700; margin: 20px 0;">
                
                <p style="font-size: 18px; color: #FFFFFF;">Salut <strong>{joueur['prenom'] or joueur['pseudo']}</strong> ! 👋</p>
                
                {alerte}
                
                <div style="background-color: #2C2C2C; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h2 style="color: #FFD700; font-size: 20px; margin-top: 0;">📅 JOURNÉE {semaine}</h2>
                    <p style="font-size: 16px; line-height: 1.8;">
                        ⚽ <strong>1er match :</strong> {date_premier_match.strftime('%A %d %B à %Hh%M')}<br>
                        🔒 <strong>Clôture des pronos :</strong> {date_cloture.strftime('%A %d %B à %Hh')}<br>
                        ⏰ <strong>Temps restant :</strong> 2 JOURS
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
    
    def creer_email_j1(self, joueur, semaine, date_cloture, date_premier_match, type_calendrier):
        """
        Template email J-1
        """
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #0A1628; color: #FFFFFF; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #1A1A1A; border: 3px solid #FF6B6B; border-radius: 10px; padding: 30px;">
                <h1 style="text-align: center; color: #FF6B6B; font-size: 28px;">🔥 DERNIÈRE CHANCE !</h1>
                <hr style="border: 2px solid #FF6B6B; margin: 20px 0;">
                
                <p style="font-size: 18px; color: #FFFFFF;">Hey <strong>{joueur['prenom'] or joueur['pseudo']}</strong> ! 👋</p>
                
                <div style="background-color: #FF6B6B; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <p style="font-size: 18px; font-weight: bold; color: white; margin: 0; text-align: center;">
                        ⚠️ TU N'AS PAS ENCORE FAIT TES PRONOS !
                    </p>
                </div>
                
                <div style="background-color: #2C2C2C; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h2 style="color: #FFD700; font-size: 20px; margin-top: 0;">📅 JOURNÉE {semaine}</h2>
                    <p style="font-size: 16px; line-height: 1.8;">
                        ⚽ <strong>1er match :</strong> {date_premier_match.strftime('%A %d %B à %Hh%M')}<br>
                        🔒 <strong>Clôture :</strong> {date_cloture.strftime('%A %d %B à %Hh')}<br>
                        ⏰ <strong>Temps restant :</strong> MOINS DE 24H !
                    </p>
                </div>
                
                <p style="text-align: center; margin-top: 30px;">
                    <a href="#" style="display: inline-block; background-color: #FF6B6B; color: white; padding: 15px 40px; text-decoration: none; border-radius: 8px; font-size: 18px; font-weight: bold;">
                        🚀 VITE, JE PRONOS !
                    </a>
                </p>
                
                <p style="text-align: center; margin-top: 20px; font-size: 12px; color: #888888;">
                    Elite Pronos 2 - Ne rate pas le coche ! 🏆
                </p>
            </div>
        </body>
        </html>
        """
        return html
    
    def creer_email_2h(self, joueur, semaine, date_cloture, date_premier_match, type_calendrier):
        """
        Template email 2H avant
        """
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #0A1628; color: #FFFFFF; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #1A1A1A; border: 3px solid #FF0000; border-radius: 10px; padding: 30px;">
                <h1 style="text-align: center; color: #FF0000; font-size: 32px;">🚨🚨 URGENCE 🚨🚨</h1>
                <hr style="border: 2px solid #FF0000; margin: 20px 0;">
                
                <p style="font-size: 18px; color: #FFFFFF;"><strong>{joueur['prenom'] or joueur['pseudo']}</strong>,</p>
                
                <div style="background-color: #FF0000; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p style="font-size: 20px; font-weight: bold; color: white; margin: 0; text-align: center;">
                        ⏰ PLUS QUE 2 HEURES !
                    </p>
                    <p style="font-size: 16px; color: white; margin: 10px 0 0 0; text-align: center;">
                        Si tu ne fais pas tes pronos, tu auras 0 point cette semaine !
                    </p>
                </div>
                
                <div style="background-color: #2C2C2C; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h2 style="color: #FFD700; font-size: 20px; margin-top: 0;">📅 JOURNÉE {semaine}</h2>
                    <p style="font-size: 16px; line-height: 1.8;">
                        🔒 <strong>Clôture dans :</strong> 2 HEURES !<br>
                        🕐 <strong>Heure limite :</strong> {date_cloture.strftime('%Hh%M')}
                    </p>
                </div>
                
                <p style="text-align: center; margin-top: 30px;">
                    <a href="#" style="display: inline-block; background-color: #FF0000; color: white; padding: 20px 50px; text-decoration: none; border-radius: 8px; font-size: 20px; font-weight: bold; animation: pulse 1s infinite;">
                        🚨 DERNIÈRE CHANCE !
                    </a>
                </p>
                
                <p style="text-align: center; margin-top: 20px; font-size: 12px; color: #888888;">
                    Elite Pronos 2 - C'est maintenant ou jamais ! ⚡
                </p>
            </div>
        </body>
        </html>
        """
        return html
    
    def get_joueurs_actifs(self):
        """
        Récupère tous les joueurs actifs
        """
        db = DatabaseManager()
        conn = None
        joueurs = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, pseudo, prenom, email
                FROM utilisateurs
                WHERE statut = 'actif' AND email IS NOT NULL
            """)
            
            rows = cursor.fetchall()
            
            for row in rows:
                joueurs.append({
                    'id': row[0],
                    'pseudo': row[1],
                    'prenom': row[2],
                    'email': row[3]
                })
        
        except Exception as e:
            print(f"❌ Erreur : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return joueurs
    
    def get_joueurs_sans_pronos(self, semaine):
        """
        Récupère les joueurs qui n'ont pas encore fait leurs pronos pour la semaine
        """
        db = DatabaseManager()
        conn = None
        joueurs = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT u.id, u.pseudo, u.prenom, u.email
                FROM utilisateurs u
                WHERE u.statut = 'actif' 
                AND u.email IS NOT NULL
                AND u.id NOT IN (
                    SELECT DISTINCT utilisateur_id 
                    FROM pronostics 
                    WHERE semaine = ?
                )
            """, (semaine,))
            
            rows = cursor.fetchall()
            
            for row in rows:
                joueurs.append({
                    'id': row[0],
                    'pseudo': row[1],
                    'prenom': row[2],
                    'email': row[3]
                })
        
        except Exception as e:
            print(f"❌ Erreur : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return joueurs
    
    def marquer_notification(self, semaine, type_notif):
        """
        Marque une notification comme envoyée
        """
        db = DatabaseManager()
        conn = None
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            champ = f"notification_{type_notif}_envoyee"
            
            cursor.execute(f"""
                UPDATE journees_calendrier
                SET {champ} = 1
                WHERE semaine = ?
            """, (semaine,))
            
            conn.commit()
        
        except Exception as e:
            print(f"❌ Erreur : {e}")
        
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    notif = SystemeNotifications()
=======
from datetime import datetime, timedelta

try:
    from modules.database_manager import DatabaseManager
    from modules.email_sender import EmailSender
except:
    from database_manager import DatabaseManager
    from email_sender import EmailSender

class SystemeNotifications:
    
    def __init__(self):
        self.email_sender = EmailSender()
        print("📧 Système de notifications initialisé")
    
    def verifier_et_envoyer(self):
        """
        Vérifie l'état du calendrier et envoie les notifications nécessaires
        """
        print(f"\n{'='*70}")
        print(f"📧 VÉRIFICATION DES NOTIFICATIONS")
        print(f"{'='*70}\n")
        
        now = datetime.now()
        
        # Récupérer la prochaine journée à venir
        prochaine_journee = self.get_prochaine_journee()
        
        if not prochaine_journee:
            print("ℹ️ Aucune journée à venir")
            return
        
        semaine = prochaine_journee['semaine']
        date_cloture = datetime.strptime(prochaine_journee['date_cloture_pronos'], "%Y-%m-%d %H:%M:%S")
        date_premier_match = datetime.strptime(prochaine_journee['date_premier_match'], "%Y-%m-%d %H:%M:%S")
        type_calendrier = prochaine_journee['type_calendrier']
        
        print(f"📅 Prochaine journée : Semaine {semaine}")
        print(f"🔒 Clôture : {date_cloture.strftime('%d/%m/%Y à %Hh')}")
        print(f"⚽ 1er match : {date_premier_match.strftime('%d/%m/%Y à %Hh%M')}")
        print(f"🔥 Type : {type_calendrier}")
        
        # Calculer les délais
        heures_avant_cloture = (date_cloture - now).total_seconds() / 3600
        
        # Notification 1 : Sourcing effectué (déjà faite par le daemon)
        
        # Notification 2 : J-2 (48h avant)
        if 47 <= heures_avant_cloture <= 49 and not prochaine_journee['notification_j2_envoyee']:
            print("\n⏰ ENVOI NOTIFICATION J-2")
            self.envoyer_notification_j2(semaine, date_cloture, date_premier_match, type_calendrier)
            self.marquer_notification(semaine, 'j2')
        
        # Notification 3 : J-1 (24h avant)
        elif 23 <= heures_avant_cloture <= 25 and not prochaine_journee['notification_j1_envoyee']:
            print("\n⏰ ENVOI NOTIFICATION J-1")
            self.envoyer_notification_j1(semaine, date_cloture, date_premier_match, type_calendrier)
            self.marquer_notification(semaine, 'j1')
        
        # Notification 4 : 2h avant clôture
        elif 1.9 <= heures_avant_cloture <= 2.1 and not prochaine_journee['notification_2h_envoyee']:
            print("\n🚨 ENVOI NOTIFICATION DERNIÈRE CHANCE")
            self.envoyer_notification_2h(semaine, date_cloture, date_premier_match, type_calendrier)
            self.marquer_notification(semaine, '2h')
        
        else:
            print(f"ℹ️ Aucune notification à envoyer (dans {heures_avant_cloture:.1f}h)")
        
        print(f"\n{'='*70}\n")
    
    def get_prochaine_journee(self):
        """
        Récupère la prochaine journée à venir
        """
        db = DatabaseManager()
        conn = None
        journee = None
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT semaine, date_premier_match, date_cloture_pronos, 
                       type_calendrier, notification_j2_envoyee, 
                       notification_j1_envoyee, notification_2h_envoyee
                FROM journees_calendrier
                WHERE statut = 'a_venir'
                ORDER BY semaine
                LIMIT 1
            """)
            
            row = cursor.fetchone()
            
            if row:
                journee = {
                    'semaine': row[0],
                    'date_premier_match': row[1],
                    'date_cloture_pronos': row[2],
                    'type_calendrier': row[3],
                    'notification_j2_envoyee': row[4],
                    'notification_j1_envoyee': row[5],
                    'notification_2h_envoyee': row[6]
                }
        
        except Exception as e:
            print(f"❌ Erreur : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return journee
    
    def envoyer_notification_j2(self, semaine, date_cloture, date_premier_match, type_calendrier):
        """
        Notification J-2 : Plus que 2 jours
        """
        joueurs = self.get_joueurs_actifs()
        
        for joueur in joueurs:
            html = self.creer_email_j2(joueur, semaine, date_cloture, date_premier_match, type_calendrier)
            
            try:
                self.email_sender.envoyer_email(
                    joueur['email'],
                    f"⏰ Elite Pronos 2 - Journée {semaine} dans 2 jours !",
                    html
                )
                print(f"  ✅ Email J-2 envoyé à {joueur['pseudo']}")
            except Exception as e:
                print(f"  ❌ Erreur pour {joueur['pseudo']} : {e}")
    
    def envoyer_notification_j1(self, semaine, date_cloture, date_premier_match, type_calendrier):
        """
        Notification J-1 : Dernière journée + liste des joueurs sans pronos
        """
        joueurs_sans_pronos = self.get_joueurs_sans_pronos(semaine)
        
        for joueur in joueurs_sans_pronos:
            html = self.creer_email_j1(joueur, semaine, date_cloture, date_premier_match, type_calendrier)
            
            try:
                self.email_sender.envoyer_email(
                    joueur['email'],
                    f"🔥 Elite Pronos 2 - DERNIÈRE CHANCE Journée {semaine} !",
                    html
                )
                print(f"  ✅ Email J-1 envoyé à {joueur['pseudo']}")
            except Exception as e:
                print(f"  ❌ Erreur pour {joueur['pseudo']} : {e}")
    
    def envoyer_notification_2h(self, semaine, date_cloture, date_premier_match, type_calendrier):
        """
        Notification 2h avant : URGENCE pour ceux qui n'ont pas fait leurs pronos
        """
        joueurs_sans_pronos = self.get_joueurs_sans_pronos(semaine)
        
        for joueur in joueurs_sans_pronos:
            html = self.creer_email_2h(joueur, semaine, date_cloture, date_premier_match, type_calendrier)
            
            try:
                self.email_sender.envoyer_email(
                    joueur['email'],
                    f"🚨🚨 Elite Pronos 2 - URGENT ! 2H AVANT CLÔTURE !",
                    html
                )
                print(f"  ✅ Email 2H envoyé à {joueur['pseudo']}")
            except Exception as e:
                print(f"  ❌ Erreur pour {joueur['pseudo']} : {e}")
    
    def creer_email_j2(self, joueur, semaine, date_cloture, date_premier_match, type_calendrier):
        """
        Template email J-2
        """
        alerte = ""
        if type_calendrier == "serre":
            alerte = """
            <div style="background-color: #FF6B6B; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <p style="font-size: 16px; font-weight: bold; color: white; margin: 0;">
                    🔥 CALENDRIER SERRÉ ! Ne tardez pas !
                </p>
            </div>
            """
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #0A1628; color: #FFFFFF; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #1A1A1A; border: 3px solid #FFD700; border-radius: 10px; padding: 30px;">
                <h1 style="text-align: center; color: #FFD700; font-size: 28px;">⏰ PLUS QUE 2 JOURS !</h1>
                <hr style="border: 2px solid #FFD700; margin: 20px 0;">
                
                <p style="font-size: 18px; color: #FFFFFF;">Salut <strong>{joueur['prenom'] or joueur['pseudo']}</strong> ! 👋</p>
                
                {alerte}
                
                <div style="background-color: #2C2C2C; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h2 style="color: #FFD700; font-size: 20px; margin-top: 0;">📅 JOURNÉE {semaine}</h2>
                    <p style="font-size: 16px; line-height: 1.8;">
                        ⚽ <strong>1er match :</strong> {date_premier_match.strftime('%A %d %B à %Hh%M')}<br>
                        🔒 <strong>Clôture des pronos :</strong> {date_cloture.strftime('%A %d %B à %Hh')}<br>
                        ⏰ <strong>Temps restant :</strong> 2 JOURS
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
    
    def creer_email_j1(self, joueur, semaine, date_cloture, date_premier_match, type_calendrier):
        """
        Template email J-1
        """
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #0A1628; color: #FFFFFF; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #1A1A1A; border: 3px solid #FF6B6B; border-radius: 10px; padding: 30px;">
                <h1 style="text-align: center; color: #FF6B6B; font-size: 28px;">🔥 DERNIÈRE CHANCE !</h1>
                <hr style="border: 2px solid #FF6B6B; margin: 20px 0;">
                
                <p style="font-size: 18px; color: #FFFFFF;">Hey <strong>{joueur['prenom'] or joueur['pseudo']}</strong> ! 👋</p>
                
                <div style="background-color: #FF6B6B; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <p style="font-size: 18px; font-weight: bold; color: white; margin: 0; text-align: center;">
                        ⚠️ TU N'AS PAS ENCORE FAIT TES PRONOS !
                    </p>
                </div>
                
                <div style="background-color: #2C2C2C; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h2 style="color: #FFD700; font-size: 20px; margin-top: 0;">📅 JOURNÉE {semaine}</h2>
                    <p style="font-size: 16px; line-height: 1.8;">
                        ⚽ <strong>1er match :</strong> {date_premier_match.strftime('%A %d %B à %Hh%M')}<br>
                        🔒 <strong>Clôture :</strong> {date_cloture.strftime('%A %d %B à %Hh')}<br>
                        ⏰ <strong>Temps restant :</strong> MOINS DE 24H !
                    </p>
                </div>
                
                <p style="text-align: center; margin-top: 30px;">
                    <a href="#" style="display: inline-block; background-color: #FF6B6B; color: white; padding: 15px 40px; text-decoration: none; border-radius: 8px; font-size: 18px; font-weight: bold;">
                        🚀 VITE, JE PRONOS !
                    </a>
                </p>
                
                <p style="text-align: center; margin-top: 20px; font-size: 12px; color: #888888;">
                    Elite Pronos 2 - Ne rate pas le coche ! 🏆
                </p>
            </div>
        </body>
        </html>
        """
        return html
    
    def creer_email_2h(self, joueur, semaine, date_cloture, date_premier_match, type_calendrier):
        """
        Template email 2H avant
        """
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #0A1628; color: #FFFFFF; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #1A1A1A; border: 3px solid #FF0000; border-radius: 10px; padding: 30px;">
                <h1 style="text-align: center; color: #FF0000; font-size: 32px;">🚨🚨 URGENCE 🚨🚨</h1>
                <hr style="border: 2px solid #FF0000; margin: 20px 0;">
                
                <p style="font-size: 18px; color: #FFFFFF;"><strong>{joueur['prenom'] or joueur['pseudo']}</strong>,</p>
                
                <div style="background-color: #FF0000; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p style="font-size: 20px; font-weight: bold; color: white; margin: 0; text-align: center;">
                        ⏰ PLUS QUE 2 HEURES !
                    </p>
                    <p style="font-size: 16px; color: white; margin: 10px 0 0 0; text-align: center;">
                        Si tu ne fais pas tes pronos, tu auras 0 point cette semaine !
                    </p>
                </div>
                
                <div style="background-color: #2C2C2C; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h2 style="color: #FFD700; font-size: 20px; margin-top: 0;">📅 JOURNÉE {semaine}</h2>
                    <p style="font-size: 16px; line-height: 1.8;">
                        🔒 <strong>Clôture dans :</strong> 2 HEURES !<br>
                        🕐 <strong>Heure limite :</strong> {date_cloture.strftime('%Hh%M')}
                    </p>
                </div>
                
                <p style="text-align: center; margin-top: 30px;">
                    <a href="#" style="display: inline-block; background-color: #FF0000; color: white; padding: 20px 50px; text-decoration: none; border-radius: 8px; font-size: 20px; font-weight: bold; animation: pulse 1s infinite;">
                        🚨 DERNIÈRE CHANCE !
                    </a>
                </p>
                
                <p style="text-align: center; margin-top: 20px; font-size: 12px; color: #888888;">
                    Elite Pronos 2 - C'est maintenant ou jamais ! ⚡
                </p>
            </div>
        </body>
        </html>
        """
        return html
    
    def get_joueurs_actifs(self):
        """
        Récupère tous les joueurs actifs
        """
        db = DatabaseManager()
        conn = None
        joueurs = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, pseudo, prenom, email
                FROM utilisateurs
                WHERE statut = 'actif' AND email IS NOT NULL
            """)
            
            rows = cursor.fetchall()
            
            for row in rows:
                joueurs.append({
                    'id': row[0],
                    'pseudo': row[1],
                    'prenom': row[2],
                    'email': row[3]
                })
        
        except Exception as e:
            print(f"❌ Erreur : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return joueurs
    
    def get_joueurs_sans_pronos(self, semaine):
        """
        Récupère les joueurs qui n'ont pas encore fait leurs pronos pour la semaine
        """
        db = DatabaseManager()
        conn = None
        joueurs = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT u.id, u.pseudo, u.prenom, u.email
                FROM utilisateurs u
                WHERE u.statut = 'actif' 
                AND u.email IS NOT NULL
                AND u.id NOT IN (
                    SELECT DISTINCT utilisateur_id 
                    FROM pronostics 
                    WHERE semaine = ?
                )
            """, (semaine,))
            
            rows = cursor.fetchall()
            
            for row in rows:
                joueurs.append({
                    'id': row[0],
                    'pseudo': row[1],
                    'prenom': row[2],
                    'email': row[3]
                })
        
        except Exception as e:
            print(f"❌ Erreur : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return joueurs
    
    def marquer_notification(self, semaine, type_notif):
        """
        Marque une notification comme envoyée
        """
        db = DatabaseManager()
        conn = None
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            champ = f"notification_{type_notif}_envoyee"
            
            cursor.execute(f"""
                UPDATE journees_calendrier
                SET {champ} = 1
                WHERE semaine = ?
            """, (semaine,))
            
            conn.commit()
        
        except Exception as e:
            print(f"❌ Erreur : {e}")
        
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    notif = SystemeNotifications()
>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
    notif.verifier_et_envoyer()