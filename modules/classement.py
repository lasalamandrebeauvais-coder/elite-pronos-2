<<<<<<< HEAD
import tkinter as tk
from tkinter import ttk
from modules.config import FENETRE_LARGEUR, FENETRE_HAUTEUR
from modules.config import COULEUR_FOND, COULEUR_OR, COULEUR_BLANC
from modules.database_manager import DatabaseManager

class ClassementWindow:
    
    def __init__(self, user_data):
        self.user_data = user_data
        
        self.window = tk.Tk()
        self.window.title("Elite Pronos 2 - Classement")
        self.window.geometry(f"{FENETRE_LARGEUR}x{FENETRE_HAUTEUR}")
        self.window.configure(bg=COULEUR_FOND)
        self.window.resizable(False, False)
        
        print(f"✅ Fenêtre de classement créée pour {user_data['pseudo']}")
        
        self.create_interface()
    
    def create_interface(self):
        titre = tk.Label(
            self.window,
            text="🏆 CLASSEMENT",
            font=("Impact", 32, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        )
        titre.pack(pady=20)
        
        style = ttk.Style()
        style.theme_create("custom", parent="alt", settings={
            "TNotebook": {
                "configure": {
                    "background": COULEUR_FOND,
                    "tabmargins": [2, 5, 2, 0]
                }
            },
            "TNotebook.Tab": {
                "configure": {
                    "padding": [20, 10],
                    "background": "#2C2C2C",
                    "foreground": COULEUR_BLANC,
                    "font": ("Arial", 12, "bold")
                },
                "map": {
                    "background": [("selected", COULEUR_OR)],
                    "foreground": [("selected", "black")],
                    "expand": [("selected", [1, 1, 1, 0])]
                }
            }
        })
        style.theme_use("custom")
        
        notebook = ttk.Notebook(self.window)
        notebook.pack(expand=True, fill="both", padx=20, pady=20)
        
        tab1 = tk.Frame(notebook, bg=COULEUR_FOND)
        tab2 = tk.Frame(notebook, bg=COULEUR_FOND)
        tab3 = tk.Frame(notebook, bg=COULEUR_FOND)
        
        notebook.add(tab1, text="📊 Classement Général")
        notebook.add(tab2, text="🎯 Précision")
        notebook.add(tab3, text="📈 Historique")
        
        self.create_classement_general(tab1)
        self.create_classement_precision(tab2)
        self.create_historique(tab3)
        
        btn_retour = tk.Button(
            self.window,
            text="← RETOUR",
            font=("Arial", 14, "bold"),
            bg=COULEUR_OR,
            fg="black",
            width=15,
            command=self.window.destroy
        )
        btn_retour.pack(pady=20)
        
        print("✅ Interface de classement créée")
    
    def create_classement_general(self, parent):
        canvas = tk.Canvas(parent, bg=COULEUR_FOND, highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COULEUR_FOND)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        header_frame = tk.Frame(scrollable_frame, bg="#2C2C2C", height=50)
        header_frame.pack(fill="x", padx=20, pady=10)
        
        headers = ["RANG", "PSEUDO", "POINTS", "GC", "JOKERS"]
        widths = [80, 200, 150, 80, 150]
        
        for header, width in zip(headers, widths):
            tk.Label(
                header_frame,
                text=header,
                font=("Arial", 12, "bold"),
                fg=COULEUR_OR,
                bg="#2C2C2C",
                width=width//8
            ).pack(side="left", padx=5)
        
        joueurs = self.load_classement_general()
        
        for idx, joueur in enumerate(joueurs):
            bg_color = "#1A1A1A" if idx % 2 == 0 else "#252525"
            
            if joueur['pseudo'] == self.user_data['pseudo']:
                bg_color = "#2C4C2C"
            
            row_frame = tk.Frame(scrollable_frame, bg=bg_color, height=60)
            row_frame.pack(fill="x", padx=20, pady=2)
            
            medaille = ""
            if idx == 0:
                medaille = "🥇"
            elif idx == 1:
                medaille = "🥈"
            elif idx == 2:
                medaille = "🥉"
            
            tk.Label(
                row_frame,
                text=f"{medaille} {idx+1}",
                font=("Arial", 14, "bold"),
                fg=COULEUR_OR if idx < 3 else COULEUR_BLANC,
                bg=bg_color,
                width=10
            ).pack(side="left", padx=5)
            
            tk.Label(
                row_frame,
                text=f"{joueur['points']:.1f} pts",
                font=("Arial", 13),
                fg=COULEUR_OR,
                bg=bg_color,
                width=18,
                anchor="center"
            ).pack(side="left", padx=5)
            
            tk.Label(
                row_frame,
                text=str(joueur['grand_chelems']),
                font=("Arial", 13),
                fg=COULEUR_BLANC,
                bg=bg_color,
                width=10,
                anchor="center"
            ).pack(side="left", padx=5)
            
            tk.Label(
                row_frame,
                text=f"{joueur['jokers_doubles']}👑 | {joueur['jokers_voles']}✋",
                font=("Arial", 12),
                fg=COULEUR_BLANC,
                bg=bg_color,
                width=18,
                anchor="center"
            ).pack(side="left", padx=5)
            
            tk.Label(
                row_frame,
                text=f"{joueur['jokers_doubles']}👑 | {joueur['jokers_voles']}✋",
                font=("Arial", 12),
                fg=COULEUR_BLANC,
                bg=bg_color,
                width=18
            ).pack(side="left", padx=5)
    
    def create_classement_precision(self, parent):
        canvas = tk.Canvas(parent, bg=COULEUR_FOND, highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COULEUR_FOND)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        header_frame = tk.Frame(scrollable_frame, bg="#2C2C2C", height=50)
        header_frame.pack(fill="x", padx=20, pady=10)
        
        headers = ["RANG", "PSEUDO", "EXACTITUDE", "BON RÉSULTAT", "TOTAL PRONOS"]
        widths = [80, 200, 150, 150, 150]
        
        for header, width in zip(headers, widths):
            tk.Label(
                header_frame,
                text=header,
                font=("Arial", 11, "bold"),
                fg=COULEUR_OR,
                bg="#2C2C2C",
                width=width//8
            ).pack(side="left", padx=5)
        
        joueurs = self.load_classement_precision()
        
        for idx, joueur in enumerate(joueurs):
            bg_color = "#1A1A1A" if idx % 2 == 0 else "#252525"
            
            if joueur['pseudo'] == self.user_data['pseudo']:
                bg_color = "#2C4C2C"
            
            row_frame = tk.Frame(scrollable_frame, bg=bg_color, height=60)
            row_frame.pack(fill="x", padx=20, pady=2)
            
            medaille = ""
            if idx == 0:
                medaille = "🥇"
            elif idx == 1:
                medaille = "🥈"
            elif idx == 2:
                medaille = "🥉"
            
            tk.Label(
                row_frame,
                text=f"{medaille} {idx+1}",
                font=("Arial", 14, "bold"),
                fg=COULEUR_OR if idx < 3 else COULEUR_BLANC,
                bg=bg_color,
                width=10
            ).pack(side="left", padx=5)
            
            tk.Label(
                row_frame,
                text=joueur['pseudo'],
                font=("Arial", 14, "bold"),
                fg=COULEUR_BLANC,
                bg=bg_color,
                width=25,
                anchor="w"
            ).pack(side="left", padx=5)
            
            tk.Label(
                row_frame,
                text=f"{joueur['exactitude']:.1f}%",
                font=("Arial", 13),
                fg=COULEUR_OR,
                bg=bg_color,
                width=18,
                anchor="center"
            ).pack(side="left", padx=5)
            
            tk.Label(
                row_frame,
                text=f"{joueur['bon_resultat']:.1f}%",
                font=("Arial", 13),
                fg=COULEUR_BLANC,
                bg=bg_color,
                width=18,
                anchor="center"
            ).pack(side="left", padx=5)
            
            tk.Label(
                row_frame,
                text=str(joueur['total_pronos']),
                font=("Arial", 13),
                fg=COULEUR_BLANC,
                bg=bg_color,
                width=18,
                anchor="center"
            ).pack(side="left", padx=5)

    
    def create_historique(self, parent):
        canvas = tk.Canvas(parent, bg=COULEUR_FOND, highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COULEUR_FOND)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        tk.Label(
            scrollable_frame,
            text="📊 ÉVOLUTION DES 5 DERNIÈRES SEMAINES",
            font=("Arial", 16, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        ).pack(pady=20)
        
        joueurs_historique = self.load_historique()
        
        for joueur in joueurs_historique:
            player_frame = tk.Frame(scrollable_frame, bg="#2C2C2C", relief="raised", borderwidth=2)
            player_frame.pack(fill="x", padx=30, pady=10)
            
            tk.Label(
                player_frame,
                text=f"👤 {joueur['pseudo']}",
                font=("Arial", 14, "bold"),
                fg=COULEUR_OR,
                bg="#2C2C2C"
            ).pack(pady=10)
            
            semaines_frame = tk.Frame(player_frame, bg="#2C2C2C")
            semaines_frame.pack(pady=10)
            
            for semaine_data in joueur['semaines']:
                semaine_box = tk.Frame(semaines_frame, bg="#1A1A1A", width=120, height=80, relief="raised", borderwidth=1)
                semaine_box.pack(side="left", padx=5, pady=5)
                semaine_box.pack_propagate(False)
                
                tk.Label(
                    semaine_box,
                    text=f"S{semaine_data['semaine']}",
                    font=("Arial", 10, "bold"),
                    fg=COULEUR_BLANC,
                    bg="#1A1A1A"
                ).pack(pady=5)
                
                tk.Label(
                    semaine_box,
                    text=f"{semaine_data['points']:.1f} pts",
                    font=("Arial", 12, "bold"),
                    fg=COULEUR_OR,
                    bg="#1A1A1A"
                ).pack()
                
                if semaine_data['grand_chelem']:
                    tk.Label(
                        semaine_box,
                            text="🎪 GC",
                        font=("Arial", 9),
                        fg="#00FF00",
                        bg="#1A1A1A"
                    ).pack()
    
    def load_classement_general(self):
        db = DatabaseManager()
        conn = None
        joueurs = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    u.pseudo,
                    COALESCE(SUM(h.points_totaux), 0) as total_points,
                    COALESCE(SUM(h.grand_chelem), 0) as grand_chelems,
                    COALESCE(s.jokers_doubles_disponibles, 0) as jokers_doubles,
                    COALESCE(s.jokers_voles_disponibles, 0) as jokers_voles
                FROM utilisateurs u
                LEFT JOIN historique h ON u.id = h.utilisateur_id
                LEFT JOIN stock_jokers s ON u.id = s.utilisateur_id
                WHERE u.statut = 'actif'
                GROUP BY u.id, u.pseudo
                ORDER BY total_points DESC
            """)
            
            rows = cursor.fetchall()
            
            for row in rows:
                joueurs.append({
                    'pseudo': row[0],
                    'points': row[1],
                    'grand_chelems': row[2],
                    'jokers_doubles': row[3],
                    'jokers_voles': row[4]
                })
            
        except Exception as e:
            print(f"❌ Erreur chargement classement : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return joueurs
    
    def load_classement_precision(self):
        db = DatabaseManager()
        conn = None
        joueurs = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    u.pseudo,
                    COALESCE(SUM(h.scores_exacts), 0) as total_exacts,
                    COALESCE(SUM(h.bons_pronos), 0) as total_bons,
                    COUNT(DISTINCT h.semaine) * 4 as total_pronos
                FROM utilisateurs u
                LEFT JOIN historique h ON u.id = h.utilisateur_id
                WHERE u.statut = 'actif'
                GROUP BY u.id, u.pseudo
                HAVING total_pronos > 0
                ORDER BY (CAST(total_exacts AS FLOAT) / total_pronos) DESC
            """)
            
            rows = cursor.fetchall()
            
            for row in rows:
                total_exacts = row[1]
                total_bons = row[2]
                total_pronos = row[3]
                
                exactitude = (total_exacts / total_pronos * 100) if total_pronos > 0 else 0
                bon_resultat = (total_bons / total_pronos * 100) if total_pronos > 0 else 0
                
                joueurs.append({
                    'pseudo': row[0],
                    'exactitude': exactitude,
                    'bon_resultat': bon_resultat,
                    'total_pronos': total_pronos
                })
            
        except Exception as e:
            print(f"❌ Erreur chargement précision : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return joueurs
    
    def load_historique(self):
        db = DatabaseManager()
        conn = None
        joueurs = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT DISTINCT u.id, u.pseudo
                FROM utilisateurs u
                INNER JOIN historique h ON u.id = h.utilisateur_id
                WHERE u.statut = 'actif'
                ORDER BY u.pseudo
            """)
            
            users = cursor.fetchall()
            
            for user in users:
                user_id = user[0]
                pseudo = user[1]
                
                cursor.execute("""
                    SELECT semaine, points_totaux, grand_chelem
                    FROM historique
                    WHERE utilisateur_id = ?
                    ORDER BY semaine DESC
                    LIMIT 5
                """, (user_id,))
                
                semaines_data = []
                for row in cursor.fetchall():
                    semaines_data.append({
                        'semaine': row[0],
                        'points': row[1],
                        'grand_chelem': row[2]
                    })
                
                if semaines_data:
                    joueurs.append({
                        'pseudo': pseudo,
                        'semaines': list(reversed(semaines_data))
                    })
            
        except Exception as e:
            print(f"❌ Erreur chargement historique : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return joueurs
    
    def run(self):
        print("🚀 Lancement du classement...")
        self.window.mainloop()

if __name__ == "__main__":
    test_user = {
        'id': 1,
        'pseudo': 'TestUser'
    }
    
    app = ClassementWindow(test_user)
=======
import tkinter as tk
from tkinter import ttk
from modules.config import FENETRE_LARGEUR, FENETRE_HAUTEUR
from modules.config import COULEUR_FOND, COULEUR_OR, COULEUR_BLANC
from modules.database_manager import DatabaseManager

class ClassementWindow:
    
    def __init__(self, user_data):
        self.user_data = user_data
        
        self.window = tk.Tk()
        self.window.title("Elite Pronos 2 - Classement")
        self.window.geometry(f"{FENETRE_LARGEUR}x{FENETRE_HAUTEUR}")
        self.window.configure(bg=COULEUR_FOND)
        self.window.resizable(False, False)
        
        print(f"✅ Fenêtre de classement créée pour {user_data['pseudo']}")
        
        self.create_interface()
    
    def create_interface(self):
        titre = tk.Label(
            self.window,
            text="🏆 CLASSEMENT",
            font=("Impact", 32, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        )
        titre.pack(pady=20)
        
        style = ttk.Style()
        style.theme_create("custom", parent="alt", settings={
            "TNotebook": {
                "configure": {
                    "background": COULEUR_FOND,
                    "tabmargins": [2, 5, 2, 0]
                }
            },
            "TNotebook.Tab": {
                "configure": {
                    "padding": [20, 10],
                    "background": "#2C2C2C",
                    "foreground": COULEUR_BLANC,
                    "font": ("Arial", 12, "bold")
                },
                "map": {
                    "background": [("selected", COULEUR_OR)],
                    "foreground": [("selected", "black")],
                    "expand": [("selected", [1, 1, 1, 0])]
                }
            }
        })
        style.theme_use("custom")
        
        notebook = ttk.Notebook(self.window)
        notebook.pack(expand=True, fill="both", padx=20, pady=20)
        
        tab1 = tk.Frame(notebook, bg=COULEUR_FOND)
        tab2 = tk.Frame(notebook, bg=COULEUR_FOND)
        tab3 = tk.Frame(notebook, bg=COULEUR_FOND)
        
        notebook.add(tab1, text="📊 Classement Général")
        notebook.add(tab2, text="🎯 Précision")
        notebook.add(tab3, text="📈 Historique")
        
        self.create_classement_general(tab1)
        self.create_classement_precision(tab2)
        self.create_historique(tab3)
        
        btn_retour = tk.Button(
            self.window,
            text="← RETOUR",
            font=("Arial", 14, "bold"),
            bg=COULEUR_OR,
            fg="black",
            width=15,
            command=self.window.destroy
        )
        btn_retour.pack(pady=20)
        
        print("✅ Interface de classement créée")
    
    def create_classement_general(self, parent):
        canvas = tk.Canvas(parent, bg=COULEUR_FOND, highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COULEUR_FOND)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        header_frame = tk.Frame(scrollable_frame, bg="#2C2C2C", height=50)
        header_frame.pack(fill="x", padx=20, pady=10)
        
        headers = ["RANG", "PSEUDO", "POINTS", "GC", "JOKERS"]
        widths = [80, 200, 150, 80, 150]
        
        for header, width in zip(headers, widths):
            tk.Label(
                header_frame,
                text=header,
                font=("Arial", 12, "bold"),
                fg=COULEUR_OR,
                bg="#2C2C2C",
                width=width//8
            ).pack(side="left", padx=5)
        
        joueurs = self.load_classement_general()
        
        for idx, joueur in enumerate(joueurs):
            bg_color = "#1A1A1A" if idx % 2 == 0 else "#252525"
            
            if joueur['pseudo'] == self.user_data['pseudo']:
                bg_color = "#2C4C2C"
            
            row_frame = tk.Frame(scrollable_frame, bg=bg_color, height=60)
            row_frame.pack(fill="x", padx=20, pady=2)
            
            medaille = ""
            if idx == 0:
                medaille = "🥇"
            elif idx == 1:
                medaille = "🥈"
            elif idx == 2:
                medaille = "🥉"
            
            tk.Label(
                row_frame,
                text=f"{medaille} {idx+1}",
                font=("Arial", 14, "bold"),
                fg=COULEUR_OR if idx < 3 else COULEUR_BLANC,
                bg=bg_color,
                width=10
            ).pack(side="left", padx=5)
            
            tk.Label(
                row_frame,
                text=f"{joueur['points']:.1f} pts",
                font=("Arial", 13),
                fg=COULEUR_OR,
                bg=bg_color,
                width=18,
                anchor="center"
            ).pack(side="left", padx=5)
            
            tk.Label(
                row_frame,
                text=str(joueur['grand_chelems']),
                font=("Arial", 13),
                fg=COULEUR_BLANC,
                bg=bg_color,
                width=10,
                anchor="center"
            ).pack(side="left", padx=5)
            
            tk.Label(
                row_frame,
                text=f"{joueur['jokers_doubles']}👑 | {joueur['jokers_voles']}✋",
                font=("Arial", 12),
                fg=COULEUR_BLANC,
                bg=bg_color,
                width=18,
                anchor="center"
            ).pack(side="left", padx=5)
            
            tk.Label(
                row_frame,
                text=f"{joueur['jokers_doubles']}👑 | {joueur['jokers_voles']}✋",
                font=("Arial", 12),
                fg=COULEUR_BLANC,
                bg=bg_color,
                width=18
            ).pack(side="left", padx=5)
    
    def create_classement_precision(self, parent):
        canvas = tk.Canvas(parent, bg=COULEUR_FOND, highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COULEUR_FOND)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        header_frame = tk.Frame(scrollable_frame, bg="#2C2C2C", height=50)
        header_frame.pack(fill="x", padx=20, pady=10)
        
        headers = ["RANG", "PSEUDO", "EXACTITUDE", "BON RÉSULTAT", "TOTAL PRONOS"]
        widths = [80, 200, 150, 150, 150]
        
        for header, width in zip(headers, widths):
            tk.Label(
                header_frame,
                text=header,
                font=("Arial", 11, "bold"),
                fg=COULEUR_OR,
                bg="#2C2C2C",
                width=width//8
            ).pack(side="left", padx=5)
        
        joueurs = self.load_classement_precision()
        
        for idx, joueur in enumerate(joueurs):
            bg_color = "#1A1A1A" if idx % 2 == 0 else "#252525"
            
            if joueur['pseudo'] == self.user_data['pseudo']:
                bg_color = "#2C4C2C"
            
            row_frame = tk.Frame(scrollable_frame, bg=bg_color, height=60)
            row_frame.pack(fill="x", padx=20, pady=2)
            
            medaille = ""
            if idx == 0:
                medaille = "🥇"
            elif idx == 1:
                medaille = "🥈"
            elif idx == 2:
                medaille = "🥉"
            
            tk.Label(
                row_frame,
                text=f"{medaille} {idx+1}",
                font=("Arial", 14, "bold"),
                fg=COULEUR_OR if idx < 3 else COULEUR_BLANC,
                bg=bg_color,
                width=10
            ).pack(side="left", padx=5)
            
            tk.Label(
                row_frame,
                text=joueur['pseudo'],
                font=("Arial", 14, "bold"),
                fg=COULEUR_BLANC,
                bg=bg_color,
                width=25,
                anchor="w"
            ).pack(side="left", padx=5)
            
            tk.Label(
                row_frame,
                text=f"{joueur['exactitude']:.1f}%",
                font=("Arial", 13),
                fg=COULEUR_OR,
                bg=bg_color,
                width=18,
                anchor="center"
            ).pack(side="left", padx=5)
            
            tk.Label(
                row_frame,
                text=f"{joueur['bon_resultat']:.1f}%",
                font=("Arial", 13),
                fg=COULEUR_BLANC,
                bg=bg_color,
                width=18,
                anchor="center"
            ).pack(side="left", padx=5)
            
            tk.Label(
                row_frame,
                text=str(joueur['total_pronos']),
                font=("Arial", 13),
                fg=COULEUR_BLANC,
                bg=bg_color,
                width=18,
                anchor="center"
            ).pack(side="left", padx=5)

    
    def create_historique(self, parent):
        canvas = tk.Canvas(parent, bg=COULEUR_FOND, highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COULEUR_FOND)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        tk.Label(
            scrollable_frame,
            text="📊 ÉVOLUTION DES 5 DERNIÈRES SEMAINES",
            font=("Arial", 16, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        ).pack(pady=20)
        
        joueurs_historique = self.load_historique()
        
        for joueur in joueurs_historique:
            player_frame = tk.Frame(scrollable_frame, bg="#2C2C2C", relief="raised", borderwidth=2)
            player_frame.pack(fill="x", padx=30, pady=10)
            
            tk.Label(
                player_frame,
                text=f"👤 {joueur['pseudo']}",
                font=("Arial", 14, "bold"),
                fg=COULEUR_OR,
                bg="#2C2C2C"
            ).pack(pady=10)
            
            semaines_frame = tk.Frame(player_frame, bg="#2C2C2C")
            semaines_frame.pack(pady=10)
            
            for semaine_data in joueur['semaines']:
                semaine_box = tk.Frame(semaines_frame, bg="#1A1A1A", width=120, height=80, relief="raised", borderwidth=1)
                semaine_box.pack(side="left", padx=5, pady=5)
                semaine_box.pack_propagate(False)
                
                tk.Label(
                    semaine_box,
                    text=f"S{semaine_data['semaine']}",
                    font=("Arial", 10, "bold"),
                    fg=COULEUR_BLANC,
                    bg="#1A1A1A"
                ).pack(pady=5)
                
                tk.Label(
                    semaine_box,
                    text=f"{semaine_data['points']:.1f} pts",
                    font=("Arial", 12, "bold"),
                    fg=COULEUR_OR,
                    bg="#1A1A1A"
                ).pack()
                
                if semaine_data['grand_chelem']:
                    tk.Label(
                        semaine_box,
                            text="🎪 GC",
                        font=("Arial", 9),
                        fg="#00FF00",
                        bg="#1A1A1A"
                    ).pack()
    
    def load_classement_general(self):
        db = DatabaseManager()
        conn = None
        joueurs = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    u.pseudo,
                    COALESCE(SUM(h.points_totaux), 0) as total_points,
                    COALESCE(SUM(h.grand_chelem), 0) as grand_chelems,
                    COALESCE(s.jokers_doubles_disponibles, 0) as jokers_doubles,
                    COALESCE(s.jokers_voles_disponibles, 0) as jokers_voles
                FROM utilisateurs u
                LEFT JOIN historique h ON u.id = h.utilisateur_id
                LEFT JOIN stock_jokers s ON u.id = s.utilisateur_id
                WHERE u.statut = 'actif'
                GROUP BY u.id, u.pseudo
                ORDER BY total_points DESC
            """)
            
            rows = cursor.fetchall()
            
            for row in rows:
                joueurs.append({
                    'pseudo': row[0],
                    'points': row[1],
                    'grand_chelems': row[2],
                    'jokers_doubles': row[3],
                    'jokers_voles': row[4]
                })
            
        except Exception as e:
            print(f"❌ Erreur chargement classement : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return joueurs
    
    def load_classement_precision(self):
        db = DatabaseManager()
        conn = None
        joueurs = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    u.pseudo,
                    COALESCE(SUM(h.scores_exacts), 0) as total_exacts,
                    COALESCE(SUM(h.bons_pronos), 0) as total_bons,
                    COUNT(DISTINCT h.semaine) * 4 as total_pronos
                FROM utilisateurs u
                LEFT JOIN historique h ON u.id = h.utilisateur_id
                WHERE u.statut = 'actif'
                GROUP BY u.id, u.pseudo
                HAVING total_pronos > 0
                ORDER BY (CAST(total_exacts AS FLOAT) / total_pronos) DESC
            """)
            
            rows = cursor.fetchall()
            
            for row in rows:
                total_exacts = row[1]
                total_bons = row[2]
                total_pronos = row[3]
                
                exactitude = (total_exacts / total_pronos * 100) if total_pronos > 0 else 0
                bon_resultat = (total_bons / total_pronos * 100) if total_pronos > 0 else 0
                
                joueurs.append({
                    'pseudo': row[0],
                    'exactitude': exactitude,
                    'bon_resultat': bon_resultat,
                    'total_pronos': total_pronos
                })
            
        except Exception as e:
            print(f"❌ Erreur chargement précision : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return joueurs
    
    def load_historique(self):
        db = DatabaseManager()
        conn = None
        joueurs = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT DISTINCT u.id, u.pseudo
                FROM utilisateurs u
                INNER JOIN historique h ON u.id = h.utilisateur_id
                WHERE u.statut = 'actif'
                ORDER BY u.pseudo
            """)
            
            users = cursor.fetchall()
            
            for user in users:
                user_id = user[0]
                pseudo = user[1]
                
                cursor.execute("""
                    SELECT semaine, points_totaux, grand_chelem
                    FROM historique
                    WHERE utilisateur_id = ?
                    ORDER BY semaine DESC
                    LIMIT 5
                """, (user_id,))
                
                semaines_data = []
                for row in cursor.fetchall():
                    semaines_data.append({
                        'semaine': row[0],
                        'points': row[1],
                        'grand_chelem': row[2]
                    })
                
                if semaines_data:
                    joueurs.append({
                        'pseudo': pseudo,
                        'semaines': list(reversed(semaines_data))
                    })
            
        except Exception as e:
            print(f"❌ Erreur chargement historique : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return joueurs
    
    def run(self):
        print("🚀 Lancement du classement...")
        self.window.mainloop()

if __name__ == "__main__":
    test_user = {
        'id': 1,
        'pseudo': 'TestUser'
    }
    
    app = ClassementWindow(test_user)
>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
    app.run()