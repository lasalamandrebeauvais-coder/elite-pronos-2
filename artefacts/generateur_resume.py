import random

try:
    from modules.database_manager import DatabaseManager
except:
    from database_manager import DatabaseManager

class GenerateurResume:
    
    def __init__(self, semaine):
        self.semaine = semaine
        print(f"🎙️ Générateur de résumé initialisé - Semaine {semaine}")
    
    def generer_resume(self):
        """
        Génère un résumé hilarant de la semaine
        """
        print(f"\n{'='*70}")
        print(f"🎙️ GÉNÉRATION DU RÉSUMÉ - SEMAINE {self.semaine}")
        print(f"{'='*70}\n")
        
        # Charger les données
        trophees = self.get_trophees()
        top3 = self.get_top3()
        stats = self.get_stats_semaine()
        
        # Générer le résumé
        resume = self.creer_resume(trophees, top3, stats)
        
        print(resume)
        print(f"\n{'='*70}")
        print("✅ RÉSUMÉ GÉNÉRÉ")
        print(f"{'='*70}\n")
        
        return resume
    
    def creer_resume(self, trophees, top3, stats):
        """
        Crée le résumé avec des templates aléatoires
        """
        intros = [
            f"🎙️ **LE RÉCAP DÉJANTÉ DE LA SEMAINE {self.semaine}**\n\n",
            f"🎪 **ATTENTION ATTENTION ! VOICI LE SHOW DE LA SEMAINE {self.semaine} !**\n\n",
            f"📢 **OYEZ OYEZ ! LES RÉSULTATS DE LA SEMAINE {self.semaine} SONT LÀ !**\n\n",
            f"🎬 **ACTION ! LA SEMAINE {self.semaine} EN DIRECT !**\n\n"
        ]
        
        resume = random.choice(intros)
        
        # Partie 1 : Le Roi de la semaine
        roi = next((t for t in trophees if t['categorie'] == 'roi_semaine'), None)
        if roi:
            phrases_roi = [
                f"👑 {roi['pseudo']} débarque en trombe avec {roi['valeur']:.1f} points et s'empare de la couronne ! Un vrai conquistador du prono !",
                f"👑 C'est {roi['pseudo']} qui règne cette semaine avec {roi['valeur']:.1f} points ! All hail the king !",
                f"👑 {roi['pseudo']} écrase la concurrence avec {roi['valeur']:.1f} points. Du lourd, du très lourd !",
                f"👑 La couronne revient à {roi['pseudo']} et ses {roi['valeur']:.1f} points ! Un sans-faute stratégique !"
            ]
            resume += random.choice(phrases_roi) + "\n\n"
        
        # Partie 2 : Le Sniper
        sniper = next((t for t in trophees if t['categorie'] == 'sniper'), None)
        if sniper:
            nb_exacts = int(sniper['valeur'])
            phrases_sniper = [
                f"🎯 {sniper['pseudo']} voit juste avec {nb_exacts} score(s) exact(s) ! Du sniper de haut niveau !",
                f"🎯 Chapeau {sniper['pseudo']} ! {nb_exacts} score(s) dans le mille ! De la précision chirurgicale !",
                f"🎯 {sniper['pseudo']} fait mouche {nb_exacts} fois ! C'est ça l'expertise !",
                f"🎯 Mention spéciale à {sniper['pseudo']} qui tape {nb_exacts} fois en plein cœur de cible !"
            ]
            resume += random.choice(phrases_sniper) + "\n\n"
        
        # Partie 3 : Le Banquier
        banquier = next((t for t in trophees if t['categorie'] == 'banquier'), None)
        if banquier:
            phrases_banquier = [
                f"🎰 {banquier['pseudo']} empoche {banquier['valeur']:.1f} points en un seul match ! Le jackpot !",
                f"🎰 Coup de maître de {banquier['pseudo']} qui encaisse {banquier['valeur']:.1f} points d'un coup ! Cha-ching !",
                f"🎰 {banquier['pseudo']} tape dans le tas avec {banquier['valeur']:.1f} points sur un match ! C'est la banque qui saute !",
                f"🎰 La machine à sous {banquier['pseudo']} délivre {banquier['valeur']:.1f} points sur un seul pari ! Magique !"
            ]
            resume += random.choice(phrases_banquier) + "\n\n"
        
        # Partie 4 : Le Cactus (gentle roasting)
        cactus = next((t for t in trophees if t['categorie'] == 'cactus'), None)
        if cactus:
            phrases_cactus = [
                f"🌵 {cactus['pseudo']} nous fait un carton... de 0 points ! On se refait la semaine prochaine champion ! 💪",
                f"🌵 Semaine difficile pour {cactus['pseudo']} qui repart bredouille. Mais on y croit pour la suite ! 🚀",
                f"🌵 {cactus['pseudo']} prend une semaine sabbatique niveau points. Le comeback sera épique ! ⚡",
                f"🌵 Score mystère pour {cactus['pseudo']} : 0 points ! La remontée n'en sera que plus belle ! 🔥"
            ]
            resume += random.choice(phrases_cactus) + "\n\n"
        
        # Partie 5 : Mentions spéciales
        grand_chelem = [t for t in trophees if t['categorie'] == 'grand_chelem']
        if grand_chelem:
            noms = ", ".join([t['pseudo'] for t in grand_chelem])
            resume += f"🎪 **GRAND CHELEM** pour {noms} ! 4/4 scores exacts, c'est du délire ! 🔥🔥🔥\n\n"
        
        joker_double = [t for t in trophees if t['categorie'] == 'joker_double']
        if joker_double:
            for jd in joker_double:
                pseudo = jd['pseudo']
                phrases_joker = [
                    f"👑×2 {pseudo} sort le joker Points Doubles ! Stratège de haut vol !",
                    f"👑×2 {pseudo} joue la carte du multiplicateur ! Du grand art tactique !",
                    f"👑×2 Le joker ×2 de {pseudo} fait des ravages ! Respect !",
                    f"👑×2 {pseudo} double la mise avec son joker ! Audacieux !"
                ]
                resume += random.choice(phrases_joker) + "\n\n"
        
        # Partie 6 : Top 3
        if top3:
            resume += "🏆 **LE PODIUM DE LA SEMAINE** :\n"
            medailles = ['🥇', '🥈', '🥉']
            for idx, joueur in enumerate(top3):
                resume += f"{medailles[idx]} {joueur['pseudo']} - {joueur['points']:.1f} points\n"
            resume += "\n"
        
        # Conclusion
        conclusions = [
            "Rendez-vous la semaine prochaine pour de nouvelles aventures pronostiques ! 🎮",
            "On se retrouve bientôt pour un nouveau round de folie ! 🚀",
            "La suite au prochain épisode ! Que le meilleur gagne ! 🏆",
            "C'est pas fini ! On revient plus fort la semaine prochaine ! 💪"
        ]
        resume += random.choice(conclusions)
        
        return resume
    
    def get_trophees(self):
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
            """, (self.semaine,))
            
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
    
    def get_top3(self):
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
            """, (self.semaine,))
            
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
    
    def get_stats_semaine(self):
        db = DatabaseManager()
        conn = None
        stats = {}
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    COUNT(DISTINCT utilisateur_id) as nb_joueurs,
                    AVG(points_totaux) as moyenne_points,
                    MAX(points_totaux) as max_points,
                    SUM(grand_chelem) as nb_grand_chelems
                FROM historique
                WHERE semaine = ?
            """, (self.semaine,))
            
            row = cursor.fetchone()
            
            if row:
                stats = {
                    'nb_joueurs': row[0],
                    'moyenne_points': row[1],
                    'max_points': row[2],
                    'nb_grand_chelems': row[3]
                }
        
        except Exception as e:
            print(f"❌ Erreur récupération stats : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return stats

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        semaine = int(sys.argv[1])
    else:
        semaine = 1
    
    gen = GenerateurResume(semaine)
    resume = gen.generer_resume()
