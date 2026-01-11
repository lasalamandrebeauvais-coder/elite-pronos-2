import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

try:
    from modules.database_manager import DatabaseManager
    from modules.generateur_resume import GenerateurResume
except:
    from database_manager import DatabaseManager
    from generateur_resume import GenerateurResume

class EmailSender:
    
    def __init__(self):
        # Configuration Gmail
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email_from = "elite.pronos.2@gmail.com"
        self.email_password = "pdyw ulvd ohzc jxkt"
        
        print("📧 Module d'envoi d'emails initialisé")
    
    def envoyer_recap_semaine(self, semaine):
        """
        Envoie le récapitulatif de la semaine à tous les joueurs actifs
        """
        print(f"\n{'='*70}")
        print(f"📧 ENVOI DU RÉCAP - SEMAINE {semaine}")
        print(f"{'='*70}\n")
        
        # Récupérer la liste des joueurs
        joueurs = self.get_joueurs_actifs()
        
        if not joueurs:
            print("⚠️ Aucun joueur actif trouvé")
            return
        
        print(f"👥 {len(joueurs)} destinataire(s)")
        
        # Charger les trophées
        trophees = self.get_trophees_semaine(semaine)
        
        # Charger le top 3
        top3 = self.get_top3_semaine(semaine)
        
        # Générer le résumé IA
        gen_resume = GenerateurResume(semaine)
        resume_ia = gen_resume.generer_resume()
        
        # Envoyer à chaque joueur
        for joueur in joueurs:
            try:
                html = self.creer_template_html(semaine, joueur, trophees, top3, resume_ia)
                self.envoyer_email(
                    joueur['email'],
                    f"🏆 Elite Pronos 2 - Récap Semaine {semaine}",
                    html
                )
                print(f"  ✅ Email envoyé à {joueur['pseudo']} ({joueur['email']})")
            except Exception as e:
                print(f"  ❌ Erreur envoi à {joueur['pseudo']} : {e}")
        
        print(f"\n{'='*70}")
        print("✅ ENVOI TERMINÉ")
        print(f"{'='*70}\n")
    
    def get_joueurs_actifs(self):
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
            print(f"❌ Erreur récupération joueurs : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return joueurs
    
    def get_trophees_semaine(self, semaine):
        db = DatabaseManager()
        conn = None
        trophees = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT u.pseudo, t.categorie, t.valeur
                FROM trophees t
                JOIN utilisateurs u ON t.utilisateur_id = u.id
                WHERE t.semaine = ?
                ORDER BY t.id
            """, (semaine,))
            
            rows = cursor.fetchall()
            
            for row in rows:
                trophees.append({
                    'pseudo': row[0],
                    'categorie': row[1],
                    'valeur': row[2]
                })
        
        except Exception as e:
            print(f"❌ Erreur récupération trophées : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return trophees
    
    def get_top3_semaine(self, semaine):
        db = DatabaseManager()
        conn = None
        top3 = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT u.pseudo, h.points_totaux
                FROM historique h
                JOIN utilisateurs u ON h.utilisateur_id = u.id
                WHERE h.semaine = ?
                ORDER BY h.points_totaux DESC
                LIMIT 3
            """, (semaine,))
            
            rows = cursor.fetchall()
            
            for row in rows:
                top3.append({
                    'pseudo': row[0],
                    'points': row[1]
                })
        
        except Exception as e:
            print(f"❌ Erreur récupération top 3 : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return top3
    
    def creer_template_html(self, semaine, joueur, trophees, top3, resume_ia):
        """
        Crée le template HTML de l'email
        """
        trophees_map = {
            'roi_semaine': {'emoji': '👑', 'nom': 'LE ROI DE LA SEMAINE'},
            'sniper': {'emoji': '🎯', 'nom': 'LE SNIPER'},
            'cactus': {'emoji': '🌵', 'nom': 'LE CACTUS'},
            'banquier': {'emoji': '🎰', 'nom': 'LE BANQUIER'},
            'voleur_coeur': {'emoji': '💘', 'nom': 'LE VOLEUR DE CŒUR'},
            'grand_chelem': {'emoji': '🎪', 'nom': 'GRAND CHELEM'},
            'joker_double': {'emoji': '👑×2', 'nom': 'JOKER POINTS DOUBLES'},
            'joker_oubli': {'emoji': '🦥', 'nom': 'JOKER OUBLI'}
        }
        
        trophees_html = ""
        for t in trophees:
            info = trophees_map.get(t['categorie'], {'emoji': '🏆', 'nom': t['categorie']})
            details = t['pseudo']
            if t.get('valeur') and t['valeur'] > 0:
                details += f" ({t['valeur']:.1f})"
            trophees_html += f"<p style='font-size: 16px; margin: 10px 0;'>{info['emoji']} <strong>{info['nom']}</strong> : {details}</p>"
        
        top3_html = ""
        medailles = ['🥇', '🥈', '🥉']
        for idx, joueur_top in enumerate(top3):
            top3_html += f"<p style='font-size: 16px; margin: 8px 0;'>{medailles[idx]} {joueur_top['pseudo']} - {joueur_top['points']:.1f} pts</p>"
        
        # Convertir le résumé IA en HTML (remplacer \n par <br>)
        resume_ia_html = resume_ia.replace('\n', '<br>')
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #0A1628; color: #FFFFFF; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #1A1A1A; border: 3px solid #FFD700; border-radius: 10px; padding: 30px;">
                <h1 style="text-align: center; color: #FFD700; font-size: 32px;">🎊 RÉCAP SEMAINE {semaine} 🎊</h1>
                <hr style="border: 2px solid #FFD700; margin: 20px 0;">
                
                <p style="font-size: 18px; color: #FFFFFF;">Salut <strong>{joueur['prenom'] or joueur['pseudo']}</strong> ! 👋</p>
                
                <h2 style="color: #FFD700; font-size: 24px; margin-top: 30px;">🎙️ LE RÉCAP DÉJANTÉ</h2>
                <div style="background-color: #2C2C2C; padding: 20px; border-radius: 8px; margin: 15px 0;">
                    <p style="font-size: 15px; line-height: 1.8; color: #FFFFFF;">{resume_ia_html}</p>
                </div>
                
                <h2 style="color: #FFD700; font-size: 24px; margin-top: 30px;">🏆 TROPHÉES DE LA SEMAINE</h2>
                <div style="background-color: #2C2C2C; padding: 20px; border-radius: 8px; margin: 15px 0;">
                    {trophees_html}
                </div>
                
                <h2 style="color: #FFD700; font-size: 24px; margin-top: 30px;">🥇 TOP 3 DE LA SEMAINE</h2>
                <div style="background-color: #2C2C2C; padding: 20px; border-radius: 8px; margin: 15px 0;">
                    {top3_html}
                </div>
                
                <p style="text-align: center; margin-top: 40px; font-size: 16px; color: #FFD700;">
                    <strong>Rendez-vous la semaine prochaine ! 🎮</strong>
                </p>
                
                <p style="text-align: center; margin-top: 20px; font-size: 12px; color: #888888;">
                    Elite Pronos 2 - Que le meilleur gagne ! 🏆
                </p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def envoyer_email(self, email_to, subject, html_content):
        """
        Envoie un email HTML
        """
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email_from
        msg['To'] = email_to
        msg['Subject'] = subject
        
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.email_from, self.email_password)
            server.send_message(msg)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        semaine = int(sys.argv[1])
    else:
        semaine = 1
    
    sender = EmailSender()
    sender.envoyer_recap_semaine(semaine)
