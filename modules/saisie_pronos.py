<<<<<<< HEAD
# saisie_pronos.py - Module de saisie des pronostics

import tkinter as tk
from tkinter import messagebox, Canvas, Scrollbar, Frame
from modules.config import FENETRE_LARGEUR, FENETRE_HAUTEUR
from modules.config import COULEUR_FOND, COULEUR_OR, COULEUR_BLANC, COULEUR_ROUGE

class SaisiePronosWindow:
    
    def __init__(self, user_data):
        self.user_data = user_data
        self.budget = 100
        self.mises = [0, 0, 0, 0]
        self.scores = [{"domicile": "", "exterieur": ""} for _ in range(4)]
        
        self.joker_actif = None
        self.cible_vol_id = None
        self.stock_jokers = self.load_stock_jokers()
        
        self.matchs = self.load_matches_from_db()
        
        if not self.matchs:
            messagebox.showerror(
                "Erreur",
                "Aucun match disponible pour cette semaine !\n\n"
                "Contacte l'administrateur."
            )
            return
        
        self.window = tk.Tk()
        self.window.title("Elite Pronos 2 - Saisie des Pronos")
        self.window.geometry(f"{FENETRE_LARGEUR}x{FENETRE_HAUTEUR}")
        self.window.configure(bg=COULEUR_FOND)
        self.window.resizable(False, False)
        
        print(f"✅ Fenêtre de saisie créée pour {user_data['pseudo']}")
        
        self.create_interface()
    
    def load_stock_jokers(self):
        from modules.database_manager import DatabaseManager
        
        db = DatabaseManager()
        conn = None
        stock = {"doubles": 0, "voles": 0}
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT jokers_doubles_disponibles, jokers_voles_disponibles
                FROM stock_jokers
                WHERE utilisateur_id = ?
            """, (self.user_data['id'],))
            
            row = cursor.fetchone()
            
            if row:
                stock["doubles"] = row[0]
                stock["voles"] = row[1]
            
        except Exception as e:
            print(f"❌ Erreur chargement stock jokers : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return stock
    
    def load_matches_from_db(self):
        from modules.database_manager import DatabaseManager
        
        db = DatabaseManager()
        conn = None
        matchs = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, equipe_domicile, equipe_exterieur, 
                       cote_domicile, cote_nul, cote_exterieur
                FROM matchs
                WHERE semaine = 1 AND statut = 'en_attente'
                ORDER BY id
                LIMIT 4
            """)
            
            rows = cursor.fetchall()
            
            for row in rows:
                matchs.append({
                    "id": row[0],
                    "domicile": row[1],
                    "exterieur": row[2],
                    "cote_1": row[3],
                    "cote_n": row[4],
                    "cote_2": row[5]
                })
            
            print(f"✅ {len(matchs)} matchs chargés depuis la DB")
            
        except Exception as e:
            print(f"❌ Erreur chargement matchs : {e}")
            
        finally:
            if conn:
                conn.close()
        
        return matchs
    
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
        
        titre = tk.Label(
            scrollable_frame,
            text="📝 SAISIR MES PRONOS",
            font=("Impact", 32, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        )
        titre.pack(pady=20)
        
        self.create_jokers_section(scrollable_frame)
        
        self.label_budget = tk.Label(
            scrollable_frame,
            text=f"💰 Budget disponible : {self.budget} points",
            font=("Arial", 16, "bold"),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND
        )
        self.label_budget.pack(pady=10)
        
        for i, match in enumerate(self.matchs):
            self.create_match_card(scrollable_frame, match, i)
        
        recap_frame = tk.Frame(scrollable_frame, bg=COULEUR_FOND)
        recap_frame.pack(pady=20)
        
        self.label_total = tk.Label(
            recap_frame,
            text=f"Total misé : 0 / {self.budget} points",
            font=("Arial", 14, "bold"),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND
        )
        self.label_total.pack()
        
        btn_valider = tk.Button(
            scrollable_frame,
            text="✅ VALIDER MES PRONOS",
            font=("Arial", 16, "bold"),
            bg=COULEUR_OR,
            fg="black",
            width=30,
            height=2,
            command=self.valider_pronos
        )
        btn_valider.pack(pady=30)
        
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        print("✅ Interface de saisie créée")
    
    def create_jokers_section(self, parent):
        jokers_frame = tk.Frame(parent, bg="#1A1A1A", relief="raised", borderwidth=3)
        jokers_frame.pack(pady=15, padx=50, fill="x")
        
        titre_jokers = tk.Label(
            jokers_frame,
            text="🃏 ACTIVATION JOKER (Optionnel - 1 seul par semaine)",
            font=("Arial", 14, "bold"),
            fg=COULEUR_OR,
            bg="#1A1A1A"
        )
        titre_jokers.pack(pady=10)
        
        choix_frame = tk.Frame(jokers_frame, bg="#1A1A1A")
        choix_frame.pack(pady=10)
        
        self.var_joker_doubles = tk.BooleanVar()
        self.var_joker_voles = tk.BooleanVar()
        
        check_doubles = tk.Checkbutton(
            choix_frame,
            text=f"👑 POINTS DOUBLES (×2) - Stock: {self.stock_jokers['doubles']}",
            variable=self.var_joker_doubles,
            font=("Arial", 12, "bold"),
            fg=COULEUR_OR,
            bg="#1A1A1A",
            selectcolor="#2C2C2C",
            activebackground="#1A1A1A",
            activeforeground=COULEUR_OR,
            command=lambda: self.toggle_joker("doubles")
        )
        check_doubles.pack(side=tk.LEFT, padx=20)
        
        if self.stock_jokers['doubles'] == 0:
            check_doubles.config(state=tk.DISABLED, fg="#555555")
        
        check_voles = tk.Checkbutton(
            choix_frame,
            text=f"✋ POINTS VOLÉS - Stock: {self.stock_jokers['voles']}",
            variable=self.var_joker_voles,
            font=("Arial", 12, "bold"),
            fg="#00BFFF",
            bg="#1A1A1A",
            selectcolor="#2C2C2C",
            activebackground="#1A1A1A",
            activeforeground="#00BFFF",
            command=lambda: self.toggle_joker("voles")
        )
        check_voles.pack(side=tk.LEFT, padx=20)
        
        if self.stock_jokers['voles'] == 0:
            check_voles.config(state=tk.DISABLED, fg="#555555")
        
        self.label_joker_actif = tk.Label(
            jokers_frame,
            text="Aucun joker activé",
            font=("Arial", 11, "italic"),
            fg="#888888",
            bg="#1A1A1A"
        )
        self.label_joker_actif.pack(pady=5)
    
    def toggle_joker(self, type_joker):
        if type_joker == "doubles":
            if self.var_joker_doubles.get():
                self.var_joker_voles.set(False)
                self.joker_actif = "doubles"
                self.cible_vol_id = None
                self.label_joker_actif.config(
                    text="✅ Joker POINTS DOUBLES activé (×2 sur vos gains)",
                    fg=COULEUR_OR
                )
            else:
                self.joker_actif = None
                self.cible_vol_id = None
                self.label_joker_actif.config(
                    text="Aucun joker activé",
                    fg="#888888"
                )
        
        elif type_joker == "voles":
            if self.var_joker_voles.get():
                self.var_joker_doubles.set(False)
                
                from modules.radar_recrutement import RadarRecrutement
                radar = RadarRecrutement(self.user_data['id'])
                cible_id = radar.run()
                
                if cible_id:
                    self.joker_actif = "voles"
                    self.cible_vol_id = cible_id
                    self.label_joker_actif.config(
                        text=f"✅ Joker POINTS VOLÉS activé (Cible: ID {cible_id})",
                        fg="#00BFFF"
                    )
                else:
                    self.var_joker_voles.set(False)
                    self.joker_actif = None
                    self.cible_vol_id = None
                    self.label_joker_actif.config(
                        text="Aucun joker activé",
                        fg="#888888"
                    )
            else:
                self.joker_actif = None
                self.cible_vol_id = None
                self.label_joker_actif.config(
                    text="Aucun joker activé",
                    fg="#888888"
                )
    
    def create_match_card(self, parent, match, index):
        card = tk.Frame(
            parent,
            bg="#2C2C2C",
            relief="raised",
            borderwidth=3
        )
        card.pack(pady=15, padx=50, fill="x")
        
        main_container = tk.Frame(card, bg="#2C2C2C")
        main_container.pack(pady=15, padx=20, fill="x")
        
        top_frame = tk.Frame(main_container, bg="#2C2C2C")
        top_frame.pack(fill="x", pady=10)
        
        left_frame = tk.Frame(top_frame, bg="#2C2C2C")
        left_frame.pack(side=tk.LEFT, expand=True)
        
        tk.Label(
            left_frame,
            text="🛡️",
            font=("Arial", 40),
            bg="#2C2C2C",
            fg=COULEUR_OR
        ).pack()
        
        tk.Label(
            left_frame,
            text=match['domicile'],
            font=("Arial", 16, "bold"),
            bg="#2C2C2C",
            fg=COULEUR_BLANC
        ).pack(pady=5)
        
        tk.Label(
            left_frame,
            text=f"Cote : {match['cote_1']}",
            font=("Arial", 12),
            bg="#2C2C2C",
            fg=COULEUR_OR
        ).pack()
        
        center_frame = tk.Frame(top_frame, bg="#2C2C2C")
        center_frame.pack(side=tk.LEFT, padx=30)
        
        tk.Label(
            center_frame,
            text="VS",
            font=("Impact", 24, "bold"),
            bg="#2C2C2C",
            fg=COULEUR_OR
        ).pack(pady=5)
        
        tk.Label(
            center_frame,
            text=f"Nul : {match['cote_n']}",
            font=("Arial", 11),
            bg="#2C2C2C",
            fg=COULEUR_OR
        ).pack()
        
        right_frame = tk.Frame(top_frame, bg="#2C2C2C")
        right_frame.pack(side=tk.LEFT, expand=True)
        
        tk.Label(
            right_frame,
            text="🛡️",
            font=("Arial", 40),
            bg="#2C2C2C",
            fg=COULEUR_OR
        ).pack()
        
        tk.Label(
            right_frame,
            text=match['exterieur'],
            font=("Arial", 16, "bold"),
            bg="#2C2C2C",
            fg=COULEUR_BLANC
        ).pack(pady=5)
        
        tk.Label(
            right_frame,
            text=f"Cote : {match['cote_2']}",
            font=("Arial", 12),
            bg="#2C2C2C",
            fg=COULEUR_OR
        ).pack()
        
        tk.Frame(main_container, bg=COULEUR_OR, height=2).pack(fill="x", pady=10)
        
        score_frame = tk.Frame(main_container, bg="#2C2C2C")
        score_frame.pack(pady=10)
        
        tk.Label(
            score_frame,
            text="Score prédit :",
            font=("Arial", 12, "bold"),
            bg="#2C2C2C",
            fg=COULEUR_BLANC
        ).pack(side=tk.LEFT, padx=5)
        
        entry_dom = tk.Entry(score_frame, font=("Arial", 16, "bold"), width=3, justify="center")
        entry_dom.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            score_frame,
            text="-",
            font=("Arial", 16, "bold"),
            bg="#2C2C2C",
            fg=COULEUR_BLANC
        ).pack(side=tk.LEFT)
        
        entry_ext = tk.Entry(score_frame, font=("Arial", 16, "bold"), width=3, justify="center")
        entry_ext.pack(side=tk.LEFT, padx=5)
        
        self.scores[index]["entry_domicile"] = entry_dom
        self.scores[index]["entry_exterieur"] = entry_ext
        
        mise_frame = tk.Frame(main_container, bg="#2C2C2C")
        mise_frame.pack(pady=15, fill="x")
        
        tk.Label(
            mise_frame,
            text="Mise (10 - 60 pts) :",
            font=("Arial", 12, "bold"),
            bg="#2C2C2C",
            fg=COULEUR_BLANC
        ).pack(side=tk.LEFT, padx=5)
        
        mise_var = tk.IntVar(value=10)
        self.scores[index]["mise_var"] = mise_var
        
        slider = tk.Scale(
            mise_frame,
            from_=10,
            to=60,
            orient=tk.HORIZONTAL,
            variable=mise_var,
            length=350,
            bg="#2C2C2C",
            fg=COULEUR_OR,
            font=("Arial", 10, "bold"),
            troughcolor=COULEUR_FOND,
            command=lambda v: self.update_total()
        )
        slider.pack(side=tk.LEFT, padx=10)
        
        label_mise = tk.Label(
            mise_frame,
            text="10 points",
            font=("Arial", 14, "bold"),
            bg="#2C2C2C",
            fg=COULEUR_OR
        )
        label_mise.pack(side=tk.LEFT, padx=5)
        self.scores[index]["label_mise"] = label_mise
        
        mise_var.trace_add("write", lambda *args: label_mise.config(text=f"{mise_var.get()} points"))
    
    def update_total(self):
        total = sum(self.scores[i]["mise_var"].get() for i in range(4))
        reste = self.budget - total
        
        couleur = COULEUR_BLANC if reste >= 0 else COULEUR_ROUGE
        self.label_total.config(
            text=f"Total misé : {total} / {self.budget} points (Reste : {reste})",
            fg=couleur
        )
    
    def valider_pronos(self):
        for i in range(4):
            dom = self.scores[i]["entry_domicile"].get().strip()
            ext = self.scores[i]["entry_exterieur"].get().strip()
            
            if not dom or not ext:
                messagebox.showerror("Erreur", f"Le score du match {i+1} est incomplet !")
                return
            
            try:
                int(dom)
                int(ext)
            except ValueError:
                messagebox.showerror("Erreur", f"Le score du match {i+1} doit être des chiffres !")
                return
        
        total = sum(self.scores[i]["mise_var"].get() for i in range(4))
        
        if total != self.budget:
            messagebox.showerror(
                "Erreur",
                f"Le total des mises doit être exactement {self.budget} points !\n"
                f"Actuellement : {total} points"
            )
            return
        
        from modules.database_manager import DatabaseManager
        
        db = DatabaseManager()
        conn = None
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT COUNT(*) FROM pronostics p
                INNER JOIN matchs m ON p.match_id = m.id
                WHERE p.utilisateur_id = ? AND m.semaine = 1
            """, (self.user_data['id'],))
            
            count = cursor.fetchone()[0]
            
            if count > 0:
                messagebox.showwarning(
                    "Attention",
                    "Tu as déjà fait tes pronos pour cette semaine !\n\n"
                    "Contacte un admin si tu veux les modifier."
                )
                return
            
            for i in range(4):
                match_id = self.matchs[i]["id"]
                score_dom = int(self.scores[i]["entry_domicile"].get().strip())
                score_ext = int(self.scores[i]["entry_exterieur"].get().strip())
                mise = self.scores[i]["mise_var"].get()
                
                cursor.execute("""
                    INSERT INTO pronostics 
                    (utilisateur_id, match_id, score_domicile_prono, 
                     score_exterieur_prono, mise, points_gagnes)
                    VALUES (?, ?, ?, ?, ?, 0)
                """, (self.user_data['id'], match_id, score_dom, score_ext, mise))
                
                print(f"  ✅ Prono {i+1}: {score_dom}-{score_ext} (Mise: {mise} pts)")
            
            if self.joker_actif:
                cursor.execute("""
                    INSERT INTO jokers 
                    (utilisateur_id, type_joker, utilise, semaine_utilisation, cible_vol_id, date_utilisation)
                    VALUES (?, ?, 1, 1, ?, CURRENT_TIMESTAMP)
                """, (self.user_data['id'], 
                      'points_doubles' if self.joker_actif == 'doubles' else 'points_voles',
                      self.cible_vol_id))
                
                if self.joker_actif == 'doubles':
                    cursor.execute("""
                        UPDATE stock_jokers 
                        SET jokers_doubles_disponibles = jokers_doubles_disponibles - 1
                        WHERE utilisateur_id = ?
                    """, (self.user_data['id'],))
                else:
                    cursor.execute("""
                        UPDATE stock_jokers 
                        SET jokers_voles_disponibles = jokers_voles_disponibles - 1
                        WHERE utilisateur_id = ?
                    """, (self.user_data['id'],))
                
                print(f"  🃏 Joker enregistré : {self.joker_actif}")
            
            conn.commit()
            
            messagebox.showinfo(
                "🎉 PRONOS ENREGISTRÉS !",
                f"Tes pronos ont été enregistrés avec succès !\n\n"
                f"Budget utilisé : {total} points\n\n"
                f"Que le meilleur gagne ! 🏆"
            )
            
            print(f"✅ Tous les pronos enregistrés pour {self.user_data['pseudo']}")
            
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Une erreur s'est produite :\n{str(e)}"
            )
            print(f"❌ Erreur enregistrement pronos : {e}")
            
        finally:
            if conn:
                conn.close()
    
    def run(self):
        print("🚀 Lancement de la saisie des pronos...")
        self.window.mainloop()

if __name__ == "__main__":
    test_user = {
        'id': 1,
        'pseudo': 'TestUser',
        'prenom': 'Jean'
    }
    
    app = SaisiePronosWindow(test_user)
=======
# saisie_pronos.py - Module de saisie des pronostics

import tkinter as tk
from tkinter import messagebox, Canvas, Scrollbar, Frame
from modules.config import FENETRE_LARGEUR, FENETRE_HAUTEUR
from modules.config import COULEUR_FOND, COULEUR_OR, COULEUR_BLANC, COULEUR_ROUGE

class SaisiePronosWindow:
    
    def __init__(self, user_data):
        self.user_data = user_data
        self.budget = 100
        self.mises = [0, 0, 0, 0]
        self.scores = [{"domicile": "", "exterieur": ""} for _ in range(4)]
        
        self.joker_actif = None
        self.cible_vol_id = None
        self.stock_jokers = self.load_stock_jokers()
        
        self.matchs = self.load_matches_from_db()
        
        if not self.matchs:
            messagebox.showerror(
                "Erreur",
                "Aucun match disponible pour cette semaine !\n\n"
                "Contacte l'administrateur."
            )
            return
        
        self.window = tk.Tk()
        self.window.title("Elite Pronos 2 - Saisie des Pronos")
        self.window.geometry(f"{FENETRE_LARGEUR}x{FENETRE_HAUTEUR}")
        self.window.configure(bg=COULEUR_FOND)
        self.window.resizable(False, False)
        
        print(f"✅ Fenêtre de saisie créée pour {user_data['pseudo']}")
        
        self.create_interface()
    
    def load_stock_jokers(self):
        from modules.database_manager import DatabaseManager
        
        db = DatabaseManager()
        conn = None
        stock = {"doubles": 0, "voles": 0}
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT jokers_doubles_disponibles, jokers_voles_disponibles
                FROM stock_jokers
                WHERE utilisateur_id = ?
            """, (self.user_data['id'],))
            
            row = cursor.fetchone()
            
            if row:
                stock["doubles"] = row[0]
                stock["voles"] = row[1]
            
        except Exception as e:
            print(f"❌ Erreur chargement stock jokers : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return stock
    
    def load_matches_from_db(self):
        from modules.database_manager import DatabaseManager
        
        db = DatabaseManager()
        conn = None
        matchs = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, equipe_domicile, equipe_exterieur, 
                       cote_domicile, cote_nul, cote_exterieur
                FROM matchs
                WHERE semaine = 1 AND statut = 'en_attente'
                ORDER BY id
                LIMIT 4
            """)
            
            rows = cursor.fetchall()
            
            for row in rows:
                matchs.append({
                    "id": row[0],
                    "domicile": row[1],
                    "exterieur": row[2],
                    "cote_1": row[3],
                    "cote_n": row[4],
                    "cote_2": row[5]
                })
            
            print(f"✅ {len(matchs)} matchs chargés depuis la DB")
            
        except Exception as e:
            print(f"❌ Erreur chargement matchs : {e}")
            
        finally:
            if conn:
                conn.close()
        
        return matchs
    
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
        
        titre = tk.Label(
            scrollable_frame,
            text="📝 SAISIR MES PRONOS",
            font=("Impact", 32, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        )
        titre.pack(pady=20)
        
        self.create_jokers_section(scrollable_frame)
        
        self.label_budget = tk.Label(
            scrollable_frame,
            text=f"💰 Budget disponible : {self.budget} points",
            font=("Arial", 16, "bold"),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND
        )
        self.label_budget.pack(pady=10)
        
        for i, match in enumerate(self.matchs):
            self.create_match_card(scrollable_frame, match, i)
        
        recap_frame = tk.Frame(scrollable_frame, bg=COULEUR_FOND)
        recap_frame.pack(pady=20)
        
        self.label_total = tk.Label(
            recap_frame,
            text=f"Total misé : 0 / {self.budget} points",
            font=("Arial", 14, "bold"),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND
        )
        self.label_total.pack()
        
        btn_valider = tk.Button(
            scrollable_frame,
            text="✅ VALIDER MES PRONOS",
            font=("Arial", 16, "bold"),
            bg=COULEUR_OR,
            fg="black",
            width=30,
            height=2,
            command=self.valider_pronos
        )
        btn_valider.pack(pady=30)
        
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        print("✅ Interface de saisie créée")
    
    def create_jokers_section(self, parent):
        jokers_frame = tk.Frame(parent, bg="#1A1A1A", relief="raised", borderwidth=3)
        jokers_frame.pack(pady=15, padx=50, fill="x")
        
        titre_jokers = tk.Label(
            jokers_frame,
            text="🃏 ACTIVATION JOKER (Optionnel - 1 seul par semaine)",
            font=("Arial", 14, "bold"),
            fg=COULEUR_OR,
            bg="#1A1A1A"
        )
        titre_jokers.pack(pady=10)
        
        choix_frame = tk.Frame(jokers_frame, bg="#1A1A1A")
        choix_frame.pack(pady=10)
        
        self.var_joker_doubles = tk.BooleanVar()
        self.var_joker_voles = tk.BooleanVar()
        
        check_doubles = tk.Checkbutton(
            choix_frame,
            text=f"👑 POINTS DOUBLES (×2) - Stock: {self.stock_jokers['doubles']}",
            variable=self.var_joker_doubles,
            font=("Arial", 12, "bold"),
            fg=COULEUR_OR,
            bg="#1A1A1A",
            selectcolor="#2C2C2C",
            activebackground="#1A1A1A",
            activeforeground=COULEUR_OR,
            command=lambda: self.toggle_joker("doubles")
        )
        check_doubles.pack(side=tk.LEFT, padx=20)
        
        if self.stock_jokers['doubles'] == 0:
            check_doubles.config(state=tk.DISABLED, fg="#555555")
        
        check_voles = tk.Checkbutton(
            choix_frame,
            text=f"✋ POINTS VOLÉS - Stock: {self.stock_jokers['voles']}",
            variable=self.var_joker_voles,
            font=("Arial", 12, "bold"),
            fg="#00BFFF",
            bg="#1A1A1A",
            selectcolor="#2C2C2C",
            activebackground="#1A1A1A",
            activeforeground="#00BFFF",
            command=lambda: self.toggle_joker("voles")
        )
        check_voles.pack(side=tk.LEFT, padx=20)
        
        if self.stock_jokers['voles'] == 0:
            check_voles.config(state=tk.DISABLED, fg="#555555")
        
        self.label_joker_actif = tk.Label(
            jokers_frame,
            text="Aucun joker activé",
            font=("Arial", 11, "italic"),
            fg="#888888",
            bg="#1A1A1A"
        )
        self.label_joker_actif.pack(pady=5)
    
    def toggle_joker(self, type_joker):
        if type_joker == "doubles":
            if self.var_joker_doubles.get():
                self.var_joker_voles.set(False)
                self.joker_actif = "doubles"
                self.cible_vol_id = None
                self.label_joker_actif.config(
                    text="✅ Joker POINTS DOUBLES activé (×2 sur vos gains)",
                    fg=COULEUR_OR
                )
            else:
                self.joker_actif = None
                self.cible_vol_id = None
                self.label_joker_actif.config(
                    text="Aucun joker activé",
                    fg="#888888"
                )
        
        elif type_joker == "voles":
            if self.var_joker_voles.get():
                self.var_joker_doubles.set(False)
                
                from modules.radar_recrutement import RadarRecrutement
                radar = RadarRecrutement(self.user_data['id'])
                cible_id = radar.run()
                
                if cible_id:
                    self.joker_actif = "voles"
                    self.cible_vol_id = cible_id
                    self.label_joker_actif.config(
                        text=f"✅ Joker POINTS VOLÉS activé (Cible: ID {cible_id})",
                        fg="#00BFFF"
                    )
                else:
                    self.var_joker_voles.set(False)
                    self.joker_actif = None
                    self.cible_vol_id = None
                    self.label_joker_actif.config(
                        text="Aucun joker activé",
                        fg="#888888"
                    )
            else:
                self.joker_actif = None
                self.cible_vol_id = None
                self.label_joker_actif.config(
                    text="Aucun joker activé",
                    fg="#888888"
                )
    
    def create_match_card(self, parent, match, index):
        card = tk.Frame(
            parent,
            bg="#2C2C2C",
            relief="raised",
            borderwidth=3
        )
        card.pack(pady=15, padx=50, fill="x")
        
        main_container = tk.Frame(card, bg="#2C2C2C")
        main_container.pack(pady=15, padx=20, fill="x")
        
        top_frame = tk.Frame(main_container, bg="#2C2C2C")
        top_frame.pack(fill="x", pady=10)
        
        left_frame = tk.Frame(top_frame, bg="#2C2C2C")
        left_frame.pack(side=tk.LEFT, expand=True)
        
        tk.Label(
            left_frame,
            text="🛡️",
            font=("Arial", 40),
            bg="#2C2C2C",
            fg=COULEUR_OR
        ).pack()
        
        tk.Label(
            left_frame,
            text=match['domicile'],
            font=("Arial", 16, "bold"),
            bg="#2C2C2C",
            fg=COULEUR_BLANC
        ).pack(pady=5)
        
        tk.Label(
            left_frame,
            text=f"Cote : {match['cote_1']}",
            font=("Arial", 12),
            bg="#2C2C2C",
            fg=COULEUR_OR
        ).pack()
        
        center_frame = tk.Frame(top_frame, bg="#2C2C2C")
        center_frame.pack(side=tk.LEFT, padx=30)
        
        tk.Label(
            center_frame,
            text="VS",
            font=("Impact", 24, "bold"),
            bg="#2C2C2C",
            fg=COULEUR_OR
        ).pack(pady=5)
        
        tk.Label(
            center_frame,
            text=f"Nul : {match['cote_n']}",
            font=("Arial", 11),
            bg="#2C2C2C",
            fg=COULEUR_OR
        ).pack()
        
        right_frame = tk.Frame(top_frame, bg="#2C2C2C")
        right_frame.pack(side=tk.LEFT, expand=True)
        
        tk.Label(
            right_frame,
            text="🛡️",
            font=("Arial", 40),
            bg="#2C2C2C",
            fg=COULEUR_OR
        ).pack()
        
        tk.Label(
            right_frame,
            text=match['exterieur'],
            font=("Arial", 16, "bold"),
            bg="#2C2C2C",
            fg=COULEUR_BLANC
        ).pack(pady=5)
        
        tk.Label(
            right_frame,
            text=f"Cote : {match['cote_2']}",
            font=("Arial", 12),
            bg="#2C2C2C",
            fg=COULEUR_OR
        ).pack()
        
        tk.Frame(main_container, bg=COULEUR_OR, height=2).pack(fill="x", pady=10)
        
        score_frame = tk.Frame(main_container, bg="#2C2C2C")
        score_frame.pack(pady=10)
        
        tk.Label(
            score_frame,
            text="Score prédit :",
            font=("Arial", 12, "bold"),
            bg="#2C2C2C",
            fg=COULEUR_BLANC
        ).pack(side=tk.LEFT, padx=5)
        
        entry_dom = tk.Entry(score_frame, font=("Arial", 16, "bold"), width=3, justify="center")
        entry_dom.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            score_frame,
            text="-",
            font=("Arial", 16, "bold"),
            bg="#2C2C2C",
            fg=COULEUR_BLANC
        ).pack(side=tk.LEFT)
        
        entry_ext = tk.Entry(score_frame, font=("Arial", 16, "bold"), width=3, justify="center")
        entry_ext.pack(side=tk.LEFT, padx=5)
        
        self.scores[index]["entry_domicile"] = entry_dom
        self.scores[index]["entry_exterieur"] = entry_ext
        
        mise_frame = tk.Frame(main_container, bg="#2C2C2C")
        mise_frame.pack(pady=15, fill="x")
        
        tk.Label(
            mise_frame,
            text="Mise (10 - 60 pts) :",
            font=("Arial", 12, "bold"),
            bg="#2C2C2C",
            fg=COULEUR_BLANC
        ).pack(side=tk.LEFT, padx=5)
        
        mise_var = tk.IntVar(value=10)
        self.scores[index]["mise_var"] = mise_var
        
        slider = tk.Scale(
            mise_frame,
            from_=10,
            to=60,
            orient=tk.HORIZONTAL,
            variable=mise_var,
            length=350,
            bg="#2C2C2C",
            fg=COULEUR_OR,
            font=("Arial", 10, "bold"),
            troughcolor=COULEUR_FOND,
            command=lambda v: self.update_total()
        )
        slider.pack(side=tk.LEFT, padx=10)
        
        label_mise = tk.Label(
            mise_frame,
            text="10 points",
            font=("Arial", 14, "bold"),
            bg="#2C2C2C",
            fg=COULEUR_OR
        )
        label_mise.pack(side=tk.LEFT, padx=5)
        self.scores[index]["label_mise"] = label_mise
        
        mise_var.trace_add("write", lambda *args: label_mise.config(text=f"{mise_var.get()} points"))
    
    def update_total(self):
        total = sum(self.scores[i]["mise_var"].get() for i in range(4))
        reste = self.budget - total
        
        couleur = COULEUR_BLANC if reste >= 0 else COULEUR_ROUGE
        self.label_total.config(
            text=f"Total misé : {total} / {self.budget} points (Reste : {reste})",
            fg=couleur
        )
    
    def valider_pronos(self):
        for i in range(4):
            dom = self.scores[i]["entry_domicile"].get().strip()
            ext = self.scores[i]["entry_exterieur"].get().strip()
            
            if not dom or not ext:
                messagebox.showerror("Erreur", f"Le score du match {i+1} est incomplet !")
                return
            
            try:
                int(dom)
                int(ext)
            except ValueError:
                messagebox.showerror("Erreur", f"Le score du match {i+1} doit être des chiffres !")
                return
        
        total = sum(self.scores[i]["mise_var"].get() for i in range(4))
        
        if total != self.budget:
            messagebox.showerror(
                "Erreur",
                f"Le total des mises doit être exactement {self.budget} points !\n"
                f"Actuellement : {total} points"
            )
            return
        
        from modules.database_manager import DatabaseManager
        
        db = DatabaseManager()
        conn = None
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT COUNT(*) FROM pronostics p
                INNER JOIN matchs m ON p.match_id = m.id
                WHERE p.utilisateur_id = ? AND m.semaine = 1
            """, (self.user_data['id'],))
            
            count = cursor.fetchone()[0]
            
            if count > 0:
                messagebox.showwarning(
                    "Attention",
                    "Tu as déjà fait tes pronos pour cette semaine !\n\n"
                    "Contacte un admin si tu veux les modifier."
                )
                return
            
            for i in range(4):
                match_id = self.matchs[i]["id"]
                score_dom = int(self.scores[i]["entry_domicile"].get().strip())
                score_ext = int(self.scores[i]["entry_exterieur"].get().strip())
                mise = self.scores[i]["mise_var"].get()
                
                cursor.execute("""
                    INSERT INTO pronostics 
                    (utilisateur_id, match_id, score_domicile_prono, 
                     score_exterieur_prono, mise, points_gagnes)
                    VALUES (?, ?, ?, ?, ?, 0)
                """, (self.user_data['id'], match_id, score_dom, score_ext, mise))
                
                print(f"  ✅ Prono {i+1}: {score_dom}-{score_ext} (Mise: {mise} pts)")
            
            if self.joker_actif:
                cursor.execute("""
                    INSERT INTO jokers 
                    (utilisateur_id, type_joker, utilise, semaine_utilisation, cible_vol_id, date_utilisation)
                    VALUES (?, ?, 1, 1, ?, CURRENT_TIMESTAMP)
                """, (self.user_data['id'], 
                      'points_doubles' if self.joker_actif == 'doubles' else 'points_voles',
                      self.cible_vol_id))
                
                if self.joker_actif == 'doubles':
                    cursor.execute("""
                        UPDATE stock_jokers 
                        SET jokers_doubles_disponibles = jokers_doubles_disponibles - 1
                        WHERE utilisateur_id = ?
                    """, (self.user_data['id'],))
                else:
                    cursor.execute("""
                        UPDATE stock_jokers 
                        SET jokers_voles_disponibles = jokers_voles_disponibles - 1
                        WHERE utilisateur_id = ?
                    """, (self.user_data['id'],))
                
                print(f"  🃏 Joker enregistré : {self.joker_actif}")
            
            conn.commit()
            
            messagebox.showinfo(
                "🎉 PRONOS ENREGISTRÉS !",
                f"Tes pronos ont été enregistrés avec succès !\n\n"
                f"Budget utilisé : {total} points\n\n"
                f"Que le meilleur gagne ! 🏆"
            )
            
            print(f"✅ Tous les pronos enregistrés pour {self.user_data['pseudo']}")
            
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Une erreur s'est produite :\n{str(e)}"
            )
            print(f"❌ Erreur enregistrement pronos : {e}")
            
        finally:
            if conn:
                conn.close()
    
    def run(self):
        print("🚀 Lancement de la saisie des pronos...")
        self.window.mainloop()

if __name__ == "__main__":
    test_user = {
        'id': 1,
        'pseudo': 'TestUser',
        'prenom': 'Jean'
    }
    
    app = SaisiePronosWindow(test_user)
>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
    app.run()