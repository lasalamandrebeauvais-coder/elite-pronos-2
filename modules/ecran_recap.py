<<<<<<< HEAD
import tkinter as tk
from tkinter import Canvas, Scrollbar, Frame
try:
    from modules.config import FENETRE_LARGEUR, FENETRE_HAUTEUR
    from modules.config import COULEUR_FOND, COULEUR_OR, COULEUR_BLANC
except:
    from config import FENETRE_LARGEUR, FENETRE_HAUTEUR
    from config import COULEUR_FOND, COULEUR_OR, COULEUR_BLANC

try:
    from modules.database_manager import DatabaseManager
except:
    from database_manager import DatabaseManager

class EcranRecapWindow:
    
    def __init__(self, semaine):
        self.semaine = semaine
        self.trophees = self.load_trophees()
        
        self.window = tk.Tk()
        self.window.title(f"Elite Pronos 2 - Récap Semaine {semaine}")
        self.window.geometry(f"{FENETRE_LARGEUR}x{FENETRE_HAUTEUR}")
        self.window.configure(bg=COULEUR_FOND)
        self.window.resizable(False, False)
        
        print(f"✅ Écran récap créé pour semaine {semaine}")
        
        self.create_interface()
    
    def create_interface(self):
        canvas = Canvas(self.window, bg=COULEUR_FOND, highlightthickness=0)
        scrollbar = Scrollbar(self.window, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg=COULEUR_FOND)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Titre principal
        titre = tk.Label(
            scrollable_frame,
            text=f"🎊 RÉCAP DE LA SEMAINE {self.semaine} 🎊",
            font=("Impact", 36, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        )
        titre.pack(pady=30)
        
        # Séparateur
        tk.Frame(scrollable_frame, bg=COULEUR_OR, height=3).pack(fill="x", padx=100, pady=10)
        
        # Section Trophées principaux
        if self.trophees['principaux']:
            self.create_section_trophees_principaux(scrollable_frame)
        
        # Section Mentions spéciales
        if self.trophees['mentions']:
            self.create_section_mentions(scrollable_frame)
        
        # Top 3 de la semaine
        self.create_top3(scrollable_frame)
        
        # Boutons
        btn_frame = tk.Frame(scrollable_frame, bg=COULEUR_FOND)
        btn_frame.pack(pady=30)
        
        tk.Button(
            btn_frame,
            text="📊 VOIR LE CLASSEMENT COMPLET",
            font=("Arial", 14, "bold"),
            bg=COULEUR_OR,
            fg="black",
            width=30,
            height=2,
            command=self.ouvrir_classement
        ).pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="✅ CONTINUER",
            font=("Arial", 14, "bold"),
            bg=COULEUR_BLANC,
            fg="black",
            width=30,
            height=2,
            command=self.window.destroy
        ).pack(pady=10)
        
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        print("✅ Interface récap créée")
    
    def create_section_trophees_principaux(self, parent):
        section = tk.Frame(parent, bg="#1A1A1A", relief="raised", borderwidth=3)
        section.pack(fill="x", padx=50, pady=20)
        
        tk.Label(
            section,
            text="🏆 TROPHÉES DE LA SEMAINE",
            font=("Arial", 20, "bold"),
            fg=COULEUR_OR,
            bg="#1A1A1A"
        ).pack(pady=15)
        
        trophees_map = {
            'roi_semaine': {'emoji': '👑', 'nom': 'LE ROI DE LA SEMAINE', 'couleur': COULEUR_OR},
            'fusee': {'emoji': '🚀', 'nom': 'LA FUSÉE', 'couleur': '#FF6B6B'},
            'sniper': {'emoji': '🎯', 'nom': 'LE SNIPER', 'couleur': '#4ECDC4'},
            'cactus': {'emoji': '🌵', 'nom': 'LE CACTUS', 'couleur': '#95E77D'},
            'voleur_coeur': {'emoji': '💘', 'nom': 'LE VOLEUR DE CŒUR', 'couleur': '#FF69B4'},
            'banquier': {'emoji': '🎰', 'nom': 'LE BANQUIER', 'couleur': '#FFD700'}
        }
        
        for trophee in self.trophees['principaux']:
            info = trophees_map.get(trophee['categorie'])
            if info:
                self.create_trophee_card(section, info, trophee)
    
    def create_section_mentions(self, parent):
        section = tk.Frame(parent, bg="#1A1A1A", relief="raised", borderwidth=3)
        section.pack(fill="x", padx=50, pady=20)
        
        tk.Label(
            section,
            text="✨ MENTIONS SPÉCIALES",
            font=("Arial", 18, "bold"),
            fg=COULEUR_OR,
            bg="#1A1A1A"
        ).pack(pady=15)
        
        mentions_map = {
            'grand_chelem': {'emoji': '🎪', 'nom': 'GRAND CHELEM', 'couleur': '#00FF00'},
            'joker_double': {'emoji': '👑×2', 'nom': 'JOKER POINTS DOUBLES', 'couleur': COULEUR_OR},
            'joker_oubli': {'emoji': '🦥', 'nom': 'JOKER OUBLI', 'couleur': '#808080'}
        }
        
        for mention in self.trophees['mentions']:
            info = mentions_map.get(mention['categorie'])
            if info:
                self.create_mention_card(section, info, mention)
    
    def create_trophee_card(self, parent, info, trophee):
        card = tk.Frame(parent, bg="#2C2C2C", relief="raised", borderwidth=2)
        card.pack(fill="x", padx=20, pady=10)
        
        content = tk.Frame(card, bg="#2C2C2C")
        content.pack(pady=15, padx=20, fill="x")
        
        tk.Label(
            content,
            text=info['emoji'],
            font=("Arial", 40),
            bg="#2C2C2C"
        ).pack(side="left", padx=10)
        
        text_frame = tk.Frame(content, bg="#2C2C2C")
        text_frame.pack(side="left", fill="x", expand=True)
        
        tk.Label(
            text_frame,
            text=info['nom'],
            font=("Arial", 16, "bold"),
            fg=info['couleur'],
            bg="#2C2C2C",
            anchor="w"
        ).pack(fill="x")
        
        details = f"{trophee['pseudo']}"
        if trophee.get('valeur') and trophee['valeur'] > 0:
            if trophee['categorie'] == 'roi_semaine':
                details += f" - {trophee['valeur']:.1f} points"
            elif trophee['categorie'] == 'sniper':
                details += f" - {int(trophee['valeur'])} scores exacts"
            elif trophee['categorie'] == 'banquier':
                details += f" - {trophee['valeur']:.1f} pts en 1 match"
            elif trophee['categorie'] == 'fusee':
                details += f" - +{int(trophee['valeur'])} places"
        
        tk.Label(
            text_frame,
            text=details,
            font=("Arial", 14),
            fg=COULEUR_BLANC,
            bg="#2C2C2C",
            anchor="w"
        ).pack(fill="x")
    
    def create_mention_card(self, parent, info, mention):
        card = tk.Frame(parent, bg="#252525")
        card.pack(fill="x", padx=20, pady=5)
        
        tk.Label(
            card,
            text=f"{info['emoji']} {info['nom']} : {mention['pseudo']}",
            font=("Arial", 13, "bold"),
            fg=info['couleur'],
            bg="#252525"
        ).pack(pady=8, padx=15, anchor="w")
    
    def create_top3(self, parent):
        section = tk.Frame(parent, bg="#1A1A1A", relief="raised", borderwidth=3)
        section.pack(fill="x", padx=50, pady=20)
        
        tk.Label(
            section,
            text="🥇 TOP 3 DE LA SEMAINE",
            font=("Arial", 18, "bold"),
            fg=COULEUR_OR,
            bg="#1A1A1A"
        ).pack(pady=15)
        
        db = DatabaseManager()
        conn = None
        
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
            
            top3 = cursor.fetchall()
            medailles = ['🥇', '🥈', '🥉']
            
            for idx, (pseudo, points) in enumerate(top3):
                row = tk.Frame(section, bg="#2C2C2C")
                row.pack(fill="x", padx=30, pady=5)
                
                tk.Label(
                    row,
                    text=f"{medailles[idx]} {idx+1}. {pseudo}",
                    font=("Arial", 15, "bold"),
                    fg=COULEUR_BLANC,
                    bg="#2C2C2C",
                    width=25,
                    anchor="w"
                ).pack(side="left", padx=10, pady=8)
                
                tk.Label(
                    row,
                    text=f"{points:.1f} points",
                    font=("Arial", 14, "bold"),
                    fg=COULEUR_OR,
                    bg="#2C2C2C"
                ).pack(side="right", padx=10)
        
        except Exception as e:
            print(f"❌ Erreur chargement top 3 : {e}")
        
        finally:
            if conn:
                conn.close()
        
        tk.Label(section, text="", bg="#1A1A1A", height=1).pack()
    
    def load_trophees(self):
        db = DatabaseManager()
        conn = None
        trophees = {'principaux': [], 'mentions': []}
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT u.pseudo, t.categorie, t.valeur
                FROM trophees t
                JOIN utilisateurs u ON t.utilisateur_id = u.id
                WHERE t.semaine = ?
                ORDER BY t.id
            """, (self.semaine,))
            
            rows = cursor.fetchall()
            
            categories_principales = ['roi_semaine', 'fusee', 'sniper', 'cactus', 'voleur_coeur', 'banquier']
            categories_mentions = ['grand_chelem', 'joker_double', 'joker_oubli']
            
            for row in rows:
                trophee = {
                    'pseudo': row[0],
                    'categorie': row[1],
                    'valeur': row[2]
                }
                
                if row[1] in categories_principales:
                    trophees['principaux'].append(trophee)
                elif row[1] in categories_mentions:
                    trophees['mentions'].append(trophee)
        
        except Exception as e:
            print(f"❌ Erreur chargement trophées : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return trophees
    
    def ouvrir_classement(self):
        print("📊 Ouverture du classement...")
        self.window.destroy()
        
        try:
            from modules.classement import ClassementWindow
        except:
            from classement import ClassementWindow
        
        # On passe un user_data fictif pour le test
        test_user = {'id': 1, 'pseudo': 'Utilisateur'}
        classement = ClassementWindow(test_user)
        classement.run()
    
    def run(self):
        print("🚀 Lancement de l'écran récap...")
        self.window.mainloop()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        semaine = int(sys.argv[1])
    else:
        semaine = 1
    
    app = EcranRecapWindow(semaine)
=======
import tkinter as tk
from tkinter import Canvas, Scrollbar, Frame
try:
    from modules.config import FENETRE_LARGEUR, FENETRE_HAUTEUR
    from modules.config import COULEUR_FOND, COULEUR_OR, COULEUR_BLANC
except:
    from config import FENETRE_LARGEUR, FENETRE_HAUTEUR
    from config import COULEUR_FOND, COULEUR_OR, COULEUR_BLANC

try:
    from modules.database_manager import DatabaseManager
except:
    from database_manager import DatabaseManager

class EcranRecapWindow:
    
    def __init__(self, semaine):
        self.semaine = semaine
        self.trophees = self.load_trophees()
        
        self.window = tk.Tk()
        self.window.title(f"Elite Pronos 2 - Récap Semaine {semaine}")
        self.window.geometry(f"{FENETRE_LARGEUR}x{FENETRE_HAUTEUR}")
        self.window.configure(bg=COULEUR_FOND)
        self.window.resizable(False, False)
        
        print(f"✅ Écran récap créé pour semaine {semaine}")
        
        self.create_interface()
    
    def create_interface(self):
        canvas = Canvas(self.window, bg=COULEUR_FOND, highlightthickness=0)
        scrollbar = Scrollbar(self.window, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg=COULEUR_FOND)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Titre principal
        titre = tk.Label(
            scrollable_frame,
            text=f"🎊 RÉCAP DE LA SEMAINE {self.semaine} 🎊",
            font=("Impact", 36, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        )
        titre.pack(pady=30)
        
        # Séparateur
        tk.Frame(scrollable_frame, bg=COULEUR_OR, height=3).pack(fill="x", padx=100, pady=10)
        
        # Section Trophées principaux
        if self.trophees['principaux']:
            self.create_section_trophees_principaux(scrollable_frame)
        
        # Section Mentions spéciales
        if self.trophees['mentions']:
            self.create_section_mentions(scrollable_frame)
        
        # Top 3 de la semaine
        self.create_top3(scrollable_frame)
        
        # Boutons
        btn_frame = tk.Frame(scrollable_frame, bg=COULEUR_FOND)
        btn_frame.pack(pady=30)
        
        tk.Button(
            btn_frame,
            text="📊 VOIR LE CLASSEMENT COMPLET",
            font=("Arial", 14, "bold"),
            bg=COULEUR_OR,
            fg="black",
            width=30,
            height=2,
            command=self.ouvrir_classement
        ).pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="✅ CONTINUER",
            font=("Arial", 14, "bold"),
            bg=COULEUR_BLANC,
            fg="black",
            width=30,
            height=2,
            command=self.window.destroy
        ).pack(pady=10)
        
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        print("✅ Interface récap créée")
    
    def create_section_trophees_principaux(self, parent):
        section = tk.Frame(parent, bg="#1A1A1A", relief="raised", borderwidth=3)
        section.pack(fill="x", padx=50, pady=20)
        
        tk.Label(
            section,
            text="🏆 TROPHÉES DE LA SEMAINE",
            font=("Arial", 20, "bold"),
            fg=COULEUR_OR,
            bg="#1A1A1A"
        ).pack(pady=15)
        
        trophees_map = {
            'roi_semaine': {'emoji': '👑', 'nom': 'LE ROI DE LA SEMAINE', 'couleur': COULEUR_OR},
            'fusee': {'emoji': '🚀', 'nom': 'LA FUSÉE', 'couleur': '#FF6B6B'},
            'sniper': {'emoji': '🎯', 'nom': 'LE SNIPER', 'couleur': '#4ECDC4'},
            'cactus': {'emoji': '🌵', 'nom': 'LE CACTUS', 'couleur': '#95E77D'},
            'voleur_coeur': {'emoji': '💘', 'nom': 'LE VOLEUR DE CŒUR', 'couleur': '#FF69B4'},
            'banquier': {'emoji': '🎰', 'nom': 'LE BANQUIER', 'couleur': '#FFD700'}
        }
        
        for trophee in self.trophees['principaux']:
            info = trophees_map.get(trophee['categorie'])
            if info:
                self.create_trophee_card(section, info, trophee)
    
    def create_section_mentions(self, parent):
        section = tk.Frame(parent, bg="#1A1A1A", relief="raised", borderwidth=3)
        section.pack(fill="x", padx=50, pady=20)
        
        tk.Label(
            section,
            text="✨ MENTIONS SPÉCIALES",
            font=("Arial", 18, "bold"),
            fg=COULEUR_OR,
            bg="#1A1A1A"
        ).pack(pady=15)
        
        mentions_map = {
            'grand_chelem': {'emoji': '🎪', 'nom': 'GRAND CHELEM', 'couleur': '#00FF00'},
            'joker_double': {'emoji': '👑×2', 'nom': 'JOKER POINTS DOUBLES', 'couleur': COULEUR_OR},
            'joker_oubli': {'emoji': '🦥', 'nom': 'JOKER OUBLI', 'couleur': '#808080'}
        }
        
        for mention in self.trophees['mentions']:
            info = mentions_map.get(mention['categorie'])
            if info:
                self.create_mention_card(section, info, mention)
    
    def create_trophee_card(self, parent, info, trophee):
        card = tk.Frame(parent, bg="#2C2C2C", relief="raised", borderwidth=2)
        card.pack(fill="x", padx=20, pady=10)
        
        content = tk.Frame(card, bg="#2C2C2C")
        content.pack(pady=15, padx=20, fill="x")
        
        tk.Label(
            content,
            text=info['emoji'],
            font=("Arial", 40),
            bg="#2C2C2C"
        ).pack(side="left", padx=10)
        
        text_frame = tk.Frame(content, bg="#2C2C2C")
        text_frame.pack(side="left", fill="x", expand=True)
        
        tk.Label(
            text_frame,
            text=info['nom'],
            font=("Arial", 16, "bold"),
            fg=info['couleur'],
            bg="#2C2C2C",
            anchor="w"
        ).pack(fill="x")
        
        details = f"{trophee['pseudo']}"
        if trophee.get('valeur') and trophee['valeur'] > 0:
            if trophee['categorie'] == 'roi_semaine':
                details += f" - {trophee['valeur']:.1f} points"
            elif trophee['categorie'] == 'sniper':
                details += f" - {int(trophee['valeur'])} scores exacts"
            elif trophee['categorie'] == 'banquier':
                details += f" - {trophee['valeur']:.1f} pts en 1 match"
            elif trophee['categorie'] == 'fusee':
                details += f" - +{int(trophee['valeur'])} places"
        
        tk.Label(
            text_frame,
            text=details,
            font=("Arial", 14),
            fg=COULEUR_BLANC,
            bg="#2C2C2C",
            anchor="w"
        ).pack(fill="x")
    
    def create_mention_card(self, parent, info, mention):
        card = tk.Frame(parent, bg="#252525")
        card.pack(fill="x", padx=20, pady=5)
        
        tk.Label(
            card,
            text=f"{info['emoji']} {info['nom']} : {mention['pseudo']}",
            font=("Arial", 13, "bold"),
            fg=info['couleur'],
            bg="#252525"
        ).pack(pady=8, padx=15, anchor="w")
    
    def create_top3(self, parent):
        section = tk.Frame(parent, bg="#1A1A1A", relief="raised", borderwidth=3)
        section.pack(fill="x", padx=50, pady=20)
        
        tk.Label(
            section,
            text="🥇 TOP 3 DE LA SEMAINE",
            font=("Arial", 18, "bold"),
            fg=COULEUR_OR,
            bg="#1A1A1A"
        ).pack(pady=15)
        
        db = DatabaseManager()
        conn = None
        
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
            
            top3 = cursor.fetchall()
            medailles = ['🥇', '🥈', '🥉']
            
            for idx, (pseudo, points) in enumerate(top3):
                row = tk.Frame(section, bg="#2C2C2C")
                row.pack(fill="x", padx=30, pady=5)
                
                tk.Label(
                    row,
                    text=f"{medailles[idx]} {idx+1}. {pseudo}",
                    font=("Arial", 15, "bold"),
                    fg=COULEUR_BLANC,
                    bg="#2C2C2C",
                    width=25,
                    anchor="w"
                ).pack(side="left", padx=10, pady=8)
                
                tk.Label(
                    row,
                    text=f"{points:.1f} points",
                    font=("Arial", 14, "bold"),
                    fg=COULEUR_OR,
                    bg="#2C2C2C"
                ).pack(side="right", padx=10)
        
        except Exception as e:
            print(f"❌ Erreur chargement top 3 : {e}")
        
        finally:
            if conn:
                conn.close()
        
        tk.Label(section, text="", bg="#1A1A1A", height=1).pack()
    
    def load_trophees(self):
        db = DatabaseManager()
        conn = None
        trophees = {'principaux': [], 'mentions': []}
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT u.pseudo, t.categorie, t.valeur
                FROM trophees t
                JOIN utilisateurs u ON t.utilisateur_id = u.id
                WHERE t.semaine = ?
                ORDER BY t.id
            """, (self.semaine,))
            
            rows = cursor.fetchall()
            
            categories_principales = ['roi_semaine', 'fusee', 'sniper', 'cactus', 'voleur_coeur', 'banquier']
            categories_mentions = ['grand_chelem', 'joker_double', 'joker_oubli']
            
            for row in rows:
                trophee = {
                    'pseudo': row[0],
                    'categorie': row[1],
                    'valeur': row[2]
                }
                
                if row[1] in categories_principales:
                    trophees['principaux'].append(trophee)
                elif row[1] in categories_mentions:
                    trophees['mentions'].append(trophee)
        
        except Exception as e:
            print(f"❌ Erreur chargement trophées : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return trophees
    
    def ouvrir_classement(self):
        print("📊 Ouverture du classement...")
        self.window.destroy()
        
        try:
            from modules.classement import ClassementWindow
        except:
            from classement import ClassementWindow
        
        # On passe un user_data fictif pour le test
        test_user = {'id': 1, 'pseudo': 'Utilisateur'}
        classement = ClassementWindow(test_user)
        classement.run()
    
    def run(self):
        print("🚀 Lancement de l'écran récap...")
        self.window.mainloop()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        semaine = int(sys.argv[1])
    else:
        semaine = 1
    
    app = EcranRecapWindow(semaine)
>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
    app.run()