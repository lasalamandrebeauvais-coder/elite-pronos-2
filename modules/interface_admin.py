<<<<<<< HEAD
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

try:
    from modules.config import FENETRE_LARGEUR, FENETRE_HAUTEUR
    from modules.config import COULEUR_FOND, COULEUR_OR, COULEUR_BLANC, COULEUR_ROUGE
    from modules.database_manager import DatabaseManager
except:
    from config import FENETRE_LARGEUR, FENETRE_HAUTEUR
    from config import COULEUR_FOND, COULEUR_OR, COULEUR_BLANC, COULEUR_ROUGE
    from database_manager import DatabaseManager

class InterfaceAdmin:
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Elite Pronos 2 - Interface Admin")
        self.window.geometry(f"{FENETRE_LARGEUR}x{FENETRE_HAUTEUR}")
        self.window.configure(bg=COULEUR_FOND)
        self.window.resizable(False, False)
        
        print("✅ Interface Admin créée")
        
        self.create_interface()
    
    def create_interface(self):
        # Titre
        titre = tk.Label(
            self.window,
            text="⚙️ INTERFACE ADMIN",
            font=("Impact", 32, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        )
        titre.pack(pady=20)
        
        # Notebook avec onglets
        style = ttk.Style()
        style.theme_create("admin_theme", parent="alt", settings={
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
        style.theme_use("admin_theme")
        
        notebook = ttk.Notebook(self.window)
        notebook.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Onglet 1 : Vue d'ensemble
        tab_vue = tk.Frame(notebook, bg=COULEUR_FOND)
        notebook.add(tab_vue, text="📊 Vue d'ensemble")
        self.create_vue_ensemble(tab_vue)
        
        # Onglet 2 : Inscriptions
        tab_inscriptions = tk.Frame(notebook, bg=COULEUR_FOND)
        notebook.add(tab_inscriptions, text="👥 Inscriptions")
        self.create_gestion_inscriptions(tab_inscriptions)
        
        # Onglet 3 : Gestion Matchs
        tab_matchs = tk.Frame(notebook, bg=COULEUR_FOND)
        notebook.add(tab_matchs, text="⚽ Gestion Matchs")
        self.create_gestion_matchs(tab_matchs)
        
        # Bouton Quitter
        tk.Button(
            self.window,
            text="🚪 QUITTER",
            font=("Arial", 14, "bold"),
            bg=COULEUR_ROUGE,
            fg=COULEUR_BLANC,
            width=15,
            command=self.window.destroy
        ).pack(pady=10)
    
    def create_vue_ensemble(self, parent):
        canvas = tk.Canvas(parent, bg=COULEUR_FOND, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        # Stats box
        stats_frame = tk.Frame(canvas, bg="#1A1A1A", relief="raised", borderwidth=3)
        stats_frame.pack(pady=30, padx=50, fill="x")
        
        tk.Label(
            stats_frame,
            text="📊 STATISTIQUES",
            font=("Arial", 20, "bold"),
            fg=COULEUR_OR,
            bg="#1A1A1A"
        ).pack(pady=15)
        
        stats = self.get_stats_globales()
        
        infos = [
            ("👥 Joueurs actifs", stats['actifs']),
            ("⏳ Inscriptions en attente", stats['en_attente']),
            ("📅 Semaine en cours", stats['semaine_actuelle']),
            ("⚽ Matchs cette semaine", stats['matchs_semaine'])
        ]
        
        for label, valeur in infos:
            row = tk.Frame(stats_frame, bg="#2C2C2C")
            row.pack(fill="x", padx=20, pady=5)
            
            tk.Label(
                row,
                text=label,
                font=("Arial", 14),
                fg=COULEUR_BLANC,
                bg="#2C2C2C",
                width=30,
                anchor="w"
            ).pack(side="left", padx=10, pady=8)
            
            tk.Label(
                row,
                text=str(valeur),
                font=("Arial", 14, "bold"),
                fg=COULEUR_OR,
                bg="#2C2C2C"
            ).pack(side="right", padx=10)
    
    def get_stats_globales(self):
        db = DatabaseManager()
        conn = None
        stats = {
            'actifs': 0,
            'en_attente': 0,
            'semaine_actuelle': 1,
            'matchs_semaine': 0
        }
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM utilisateurs WHERE statut = 'actif'")
            stats['actifs'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM utilisateurs WHERE statut = 'en_attente'")
            stats['en_attente'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT MAX(semaine) FROM matchs")
            max_semaine = cursor.fetchone()[0]
            stats['semaine_actuelle'] = max_semaine if max_semaine else 1
            
            cursor.execute("SELECT COUNT(*) FROM matchs WHERE semaine = ?", (stats['semaine_actuelle'],))
            stats['matchs_semaine'] = cursor.fetchone()[0]
        
        except Exception as e:
            print(f"❌ Erreur stats : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return stats
    
    def create_gestion_inscriptions(self, parent):
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
            text="👥 INSCRIPTIONS EN ATTENTE",
            font=("Arial", 18, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        ).pack(pady=20)
        
        inscriptions = self.get_inscriptions_attente()
        
        if not inscriptions:
            tk.Label(
                scrollable_frame,
                text="✅ Aucune inscription en attente",
                font=("Arial", 14),
                fg=COULEUR_BLANC,
                bg=COULEUR_FOND
            ).pack(pady=50)
        else:
            for inscription in inscriptions:
                self.create_inscription_card(scrollable_frame, inscription)
    
    def create_inscription_card(self, parent, inscription):
        card = tk.Frame(parent, bg="#2C2C2C", relief="raised", borderwidth=2)
        card.pack(fill="x", padx=30, pady=10)
        
        info_frame = tk.Frame(card, bg="#2C2C2C")
        info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)
        
        tk.Label(
            info_frame,
            text=f"🎮 {inscription['pseudo']}",
            font=("Arial", 16, "bold"),
            fg=COULEUR_OR,
            bg="#2C2C2C",
            anchor="w"
        ).pack(fill="x")
        
        tk.Label(
            info_frame,
            text=f"{inscription['prenom']} {inscription['nom']}",
            font=("Arial", 12),
            fg=COULEUR_BLANC,
            bg="#2C2C2C",
            anchor="w"
        ).pack(fill="x")
        
        tk.Label(
            info_frame,
            text=f"📧 {inscription['email'] if inscription['email'] else 'Pas d email'}",
            font=("Arial", 11),
            fg="#AAAAAA",
            bg="#2C2C2C",
            anchor="w"
        ).pack(fill="x")
        
        btn_frame = tk.Frame(card, bg="#2C2C2C")
        btn_frame.pack(side="right", padx=20)
        
        tk.Button(
            btn_frame,
            text="✅ VALIDER",
            font=("Arial", 11, "bold"),
            bg="#00AA00",
            fg=COULEUR_BLANC,
            width=10,
            command=lambda: self.valider_inscription(inscription['id'])
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame,
            text="❌ REFUSER",
            font=("Arial", 11, "bold"),
            bg=COULEUR_ROUGE,
            fg=COULEUR_BLANC,
            width=10,
            command=lambda: self.refuser_inscription(inscription['id'])
        ).pack(side="left", padx=5)
    
    def get_inscriptions_attente(self):
        db = DatabaseManager()
        conn = None
        inscriptions = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, pseudo, prenom, nom, email
                FROM utilisateurs
                WHERE statut = 'en_attente'
                ORDER BY date_inscription DESC
            """)
            
            rows = cursor.fetchall()
            
            for row in rows:
                inscriptions.append({
                    'id': row[0],
                    'pseudo': row[1],
                    'prenom': row[2],
                    'nom': row[3],
                    'email': row[4]
                })
        
        except Exception as e:
            print(f"❌ Erreur inscriptions : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return inscriptions
    
    def valider_inscription(self, user_id):
        reponse = messagebox.askyesno(
            "Validation",
            "Valider cette inscription et activer le compte ?"
        )
        
        if reponse:
            db = DatabaseManager()
            conn = None
            
            try:
                conn = db.create_connection()
                cursor = conn.cursor()
                
                cursor.execute("UPDATE utilisateurs SET statut = 'actif' WHERE id = ?", (user_id,))
                
                cursor.execute("""
                    INSERT OR IGNORE INTO stock_jokers (utilisateur_id, jokers_doubles_disponibles, jokers_voles_disponibles)
                    VALUES (?, 3, 2)
                """, (user_id,))
                
                conn.commit()
                
                messagebox.showinfo("Succès", "✅ Compte activé avec succès !")
                
                self.window.destroy()
                self.__init__()
                self.run()
            
            except Exception as e:
                messagebox.showerror("Erreur", f"❌ Erreur : {e}")
            
            finally:
                if conn:
                    conn.close()
    
    def refuser_inscription(self, user_id):
        reponse = messagebox.askyesno(
            "Refus",
            "Refuser cette inscription et supprimer le compte ?"
        )
        
        if reponse:
            db = DatabaseManager()
            conn = None
            
            try:
                conn = db.create_connection()
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM utilisateurs WHERE id = ?", (user_id,))
                conn.commit()
                
                messagebox.showinfo("Succès", "✅ Compte supprimé")
                
                self.window.destroy()
                self.__init__()
                self.run()
            
            except Exception as e:
                messagebox.showerror("Erreur", f"❌ Erreur : {e}")
            
            finally:
                if conn:
                    conn.close()
    
    def create_gestion_matchs(self, parent):
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
        
        header_frame = tk.Frame(scrollable_frame, bg=COULEUR_FOND)
        header_frame.pack(pady=20, fill="x")
        
        tk.Label(
            header_frame,
            text="⚽ GESTION DES MATCHS",
            font=("Arial", 18, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        ).pack()
        
        semaine_frame = tk.Frame(header_frame, bg=COULEUR_FOND)
        semaine_frame.pack(pady=10)
        
        tk.Label(
            semaine_frame,
            text="Semaine :",
            font=("Arial", 14),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND
        ).pack(side="left", padx=10)
        
        self.matchs_semaine_var = tk.StringVar(value="1")
        semaine_spinbox = tk.Spinbox(
            semaine_frame,
            from_=1,
            to=38,
            textvariable=self.matchs_semaine_var,
            font=("Arial", 14),
            width=5
        )
        semaine_spinbox.pack(side="left")
        
        tk.Button(
            semaine_frame,
            text="🔄 ACTUALISER",
            font=("Arial", 12, "bold"),
            bg=COULEUR_OR,
            fg="black",
            command=lambda: self.refresh_matchs()
        ).pack(side="left", padx=10)
        
        self.matchs_container = tk.Frame(scrollable_frame, bg=COULEUR_FOND)
        self.matchs_container.pack(fill="both", expand=True, padx=20)
        
        self.load_matchs(self.matchs_container)
    
    def refresh_matchs(self):
        for widget in self.matchs_container.winfo_children():
            widget.destroy()
        
        self.load_matchs(self.matchs_container)
    
    def load_matchs(self, parent):
        semaine = int(self.matchs_semaine_var.get())
        
        db = DatabaseManager()
        conn = None
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, equipe_domicile, equipe_exterieur, cote_domicile, cote_nul, cote_exterieur, date_match
                FROM matchs
                WHERE semaine = ?
                ORDER BY date_match
            """, (semaine,))
            
            matchs = cursor.fetchall()
            
            if not matchs:
                tk.Label(
                    parent,
                    text=f"⚠️ Aucun match pour la semaine {semaine}",
                    font=("Arial", 14),
                    fg=COULEUR_BLANC,
                    bg=COULEUR_FOND
                ).pack(pady=50)
            else:
                for match in matchs:
                    self.create_match_card(parent, match)
        
        except Exception as e:
            print(f"❌ Erreur chargement matchs : {e}")
        
        finally:
            if conn:
                conn.close()
    
    def create_match_card(self, parent, match):
        match_id, dom, ext, cote_d, cote_n, cote_e, date_match = match
        
        card = tk.Frame(parent, bg="#2C2C2C", relief="raised", borderwidth=2)
        card.pack(fill="x", pady=10)
        
        info_frame = tk.Frame(card, bg="#2C2C2C")
        info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)
        
        tk.Label(
            info_frame,
            text=f"⚽ {dom} vs {ext}",
            font=("Arial", 14, "bold"),
            fg=COULEUR_OR,
            bg="#2C2C2C",
            anchor="w"
        ).pack(fill="x")
        
        tk.Label(
            info_frame,
            text=f"Cotes : {cote_d} - {cote_n} - {cote_e}",
            font=("Arial", 11),
            fg=COULEUR_BLANC,
            bg="#2C2C2C",
            anchor="w"
        ).pack(fill="x")
        
        tk.Label(
            info_frame,
            text=f"📅 {date_match}",
            font=("Arial", 10),
            fg="#AAAAAA",
            bg="#2C2C2C",
            anchor="w"
        ).pack(fill="x")
        
        tk.Button(
            card,
            text="✏️ MODIFIER",
            font=("Arial", 11, "bold"),
            bg=COULEUR_OR,
            fg="black",
            width=12,
            command=lambda: self.modifier_match(match_id)
        ).pack(side="right", padx=20)
    
    def modifier_match(self, match_id):
        edit_window = tk.Toplevel(self.window)
        edit_window.title("Modifier le match")
        edit_window.geometry("500x400")
        edit_window.configure(bg=COULEUR_FOND)
        
        tk.Label(
            edit_window,
            text="✏️ MODIFIER LE MATCH",
            font=("Arial", 18, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        ).pack(pady=20)
        
        db = DatabaseManager()
        conn = None
        match_data = None
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM matchs WHERE id = ?", (match_id,))
            match_data = cursor.fetchone()
        finally:
            if conn:
                conn.close()
        
        if not match_data:
            messagebox.showerror("Erreur", "Match introuvable")
            edit_window.destroy()
            return
        
        form_frame = tk.Frame(edit_window, bg=COULEUR_FOND)
        form_frame.pack(pady=20, padx=40, fill="both")
        
        fields = {}
        labels = ["Équipe Domicile", "Équipe Extérieur", "Cote Domicile", "Cote Nul", "Cote Extérieur"]
        indices = [2, 3, 4, 5, 6]
        
        for label, idx in zip(labels, indices):
            row = tk.Frame(form_frame, bg=COULEUR_FOND)
            row.pack(fill="x", pady=5)
            
            tk.Label(
                row,
                text=f"{label} :",
                font=("Arial", 12),
                fg=COULEUR_BLANC,
                bg=COULEUR_FOND,
                width=18,
                anchor="w"
            ).pack(side="left")
            
            entry = tk.Entry(row, font=("Arial", 12), width=20)
            entry.insert(0, str(match_data[idx]))
            entry.pack(side="left", padx=10)
            
            fields[label] = entry
        
        btn_frame = tk.Frame(edit_window, bg=COULEUR_FOND)
        btn_frame.pack(pady=30)
        
        def sauvegarder():
            try:
                db = DatabaseManager()
                conn = db.create_connection()
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE matchs
                    SET equipe_domicile = ?, equipe_exterieur = ?, 
                        cote_domicile = ?, cote_nul = ?, cote_exterieur = ?
                    WHERE id = ?
                """, (
                    fields["Équipe Domicile"].get(),
                    fields["Équipe Extérieur"].get(),
                    float(fields["Cote Domicile"].get()),
                    float(fields["Cote Nul"].get()),
                    float(fields["Cote Extérieur"].get()),
                    match_id
                ))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Succès", "✅ Match modifié")
                edit_window.destroy()
                self.refresh_matchs()
            
            except Exception as e:
                messagebox.showerror("Erreur", f"❌ {e}")
        
        tk.Button(
            btn_frame,
            text="💾 SAUVEGARDER",
            font=("Arial", 12, "bold"),
            bg="#00AA00",
            fg=COULEUR_BLANC,
            width=15,
            command=sauvegarder
        ).pack(side="left", padx=10)
        
        tk.Button(
            btn_frame,
            text="❌ ANNULER",
            font=("Arial", 12, "bold"),
            bg=COULEUR_ROUGE,
            fg=COULEUR_BLANC,
            width=15,
            command=edit_window.destroy
        ).pack(side="left", padx=10)
    
    def run(self):
        print("🚀 Lancement interface admin...")
        self.window.mainloop()

if __name__ == "__main__":
    app = InterfaceAdmin()
=======
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

try:
    from modules.config import FENETRE_LARGEUR, FENETRE_HAUTEUR
    from modules.config import COULEUR_FOND, COULEUR_OR, COULEUR_BLANC, COULEUR_ROUGE
    from modules.database_manager import DatabaseManager
except:
    from config import FENETRE_LARGEUR, FENETRE_HAUTEUR
    from config import COULEUR_FOND, COULEUR_OR, COULEUR_BLANC, COULEUR_ROUGE
    from database_manager import DatabaseManager

class InterfaceAdmin:
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Elite Pronos 2 - Interface Admin")
        self.window.geometry(f"{FENETRE_LARGEUR}x{FENETRE_HAUTEUR}")
        self.window.configure(bg=COULEUR_FOND)
        self.window.resizable(False, False)
        
        print("✅ Interface Admin créée")
        
        self.create_interface()
    
    def create_interface(self):
        # Titre
        titre = tk.Label(
            self.window,
            text="⚙️ INTERFACE ADMIN",
            font=("Impact", 32, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        )
        titre.pack(pady=20)
        
        # Notebook avec onglets
        style = ttk.Style()
        style.theme_create("admin_theme", parent="alt", settings={
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
        style.theme_use("admin_theme")
        
        notebook = ttk.Notebook(self.window)
        notebook.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Onglet 1 : Vue d'ensemble
        tab_vue = tk.Frame(notebook, bg=COULEUR_FOND)
        notebook.add(tab_vue, text="📊 Vue d'ensemble")
        self.create_vue_ensemble(tab_vue)
        
        # Onglet 2 : Inscriptions
        tab_inscriptions = tk.Frame(notebook, bg=COULEUR_FOND)
        notebook.add(tab_inscriptions, text="👥 Inscriptions")
        self.create_gestion_inscriptions(tab_inscriptions)
        
        # Onglet 3 : Gestion Matchs
        tab_matchs = tk.Frame(notebook, bg=COULEUR_FOND)
        notebook.add(tab_matchs, text="⚽ Gestion Matchs")
        self.create_gestion_matchs(tab_matchs)
        
        # Bouton Quitter
        tk.Button(
            self.window,
            text="🚪 QUITTER",
            font=("Arial", 14, "bold"),
            bg=COULEUR_ROUGE,
            fg=COULEUR_BLANC,
            width=15,
            command=self.window.destroy
        ).pack(pady=10)
    
    def create_vue_ensemble(self, parent):
        canvas = tk.Canvas(parent, bg=COULEUR_FOND, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        # Stats box
        stats_frame = tk.Frame(canvas, bg="#1A1A1A", relief="raised", borderwidth=3)
        stats_frame.pack(pady=30, padx=50, fill="x")
        
        tk.Label(
            stats_frame,
            text="📊 STATISTIQUES",
            font=("Arial", 20, "bold"),
            fg=COULEUR_OR,
            bg="#1A1A1A"
        ).pack(pady=15)
        
        stats = self.get_stats_globales()
        
        infos = [
            ("👥 Joueurs actifs", stats['actifs']),
            ("⏳ Inscriptions en attente", stats['en_attente']),
            ("📅 Semaine en cours", stats['semaine_actuelle']),
            ("⚽ Matchs cette semaine", stats['matchs_semaine'])
        ]
        
        for label, valeur in infos:
            row = tk.Frame(stats_frame, bg="#2C2C2C")
            row.pack(fill="x", padx=20, pady=5)
            
            tk.Label(
                row,
                text=label,
                font=("Arial", 14),
                fg=COULEUR_BLANC,
                bg="#2C2C2C",
                width=30,
                anchor="w"
            ).pack(side="left", padx=10, pady=8)
            
            tk.Label(
                row,
                text=str(valeur),
                font=("Arial", 14, "bold"),
                fg=COULEUR_OR,
                bg="#2C2C2C"
            ).pack(side="right", padx=10)
    
    def get_stats_globales(self):
        db = DatabaseManager()
        conn = None
        stats = {
            'actifs': 0,
            'en_attente': 0,
            'semaine_actuelle': 1,
            'matchs_semaine': 0
        }
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM utilisateurs WHERE statut = 'actif'")
            stats['actifs'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM utilisateurs WHERE statut = 'en_attente'")
            stats['en_attente'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT MAX(semaine) FROM matchs")
            max_semaine = cursor.fetchone()[0]
            stats['semaine_actuelle'] = max_semaine if max_semaine else 1
            
            cursor.execute("SELECT COUNT(*) FROM matchs WHERE semaine = ?", (stats['semaine_actuelle'],))
            stats['matchs_semaine'] = cursor.fetchone()[0]
        
        except Exception as e:
            print(f"❌ Erreur stats : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return stats
    
    def create_gestion_inscriptions(self, parent):
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
            text="👥 INSCRIPTIONS EN ATTENTE",
            font=("Arial", 18, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        ).pack(pady=20)
        
        inscriptions = self.get_inscriptions_attente()
        
        if not inscriptions:
            tk.Label(
                scrollable_frame,
                text="✅ Aucune inscription en attente",
                font=("Arial", 14),
                fg=COULEUR_BLANC,
                bg=COULEUR_FOND
            ).pack(pady=50)
        else:
            for inscription in inscriptions:
                self.create_inscription_card(scrollable_frame, inscription)
    
    def create_inscription_card(self, parent, inscription):
        card = tk.Frame(parent, bg="#2C2C2C", relief="raised", borderwidth=2)
        card.pack(fill="x", padx=30, pady=10)
        
        info_frame = tk.Frame(card, bg="#2C2C2C")
        info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)
        
        tk.Label(
            info_frame,
            text=f"🎮 {inscription['pseudo']}",
            font=("Arial", 16, "bold"),
            fg=COULEUR_OR,
            bg="#2C2C2C",
            anchor="w"
        ).pack(fill="x")
        
        tk.Label(
            info_frame,
            text=f"{inscription['prenom']} {inscription['nom']}",
            font=("Arial", 12),
            fg=COULEUR_BLANC,
            bg="#2C2C2C",
            anchor="w"
        ).pack(fill="x")
        
        tk.Label(
            info_frame,
            text=f"📧 {inscription['email'] if inscription['email'] else 'Pas d email'}",
            font=("Arial", 11),
            fg="#AAAAAA",
            bg="#2C2C2C",
            anchor="w"
        ).pack(fill="x")
        
        btn_frame = tk.Frame(card, bg="#2C2C2C")
        btn_frame.pack(side="right", padx=20)
        
        tk.Button(
            btn_frame,
            text="✅ VALIDER",
            font=("Arial", 11, "bold"),
            bg="#00AA00",
            fg=COULEUR_BLANC,
            width=10,
            command=lambda: self.valider_inscription(inscription['id'])
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame,
            text="❌ REFUSER",
            font=("Arial", 11, "bold"),
            bg=COULEUR_ROUGE,
            fg=COULEUR_BLANC,
            width=10,
            command=lambda: self.refuser_inscription(inscription['id'])
        ).pack(side="left", padx=5)
    
    def get_inscriptions_attente(self):
        db = DatabaseManager()
        conn = None
        inscriptions = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, pseudo, prenom, nom, email
                FROM utilisateurs
                WHERE statut = 'en_attente'
                ORDER BY date_inscription DESC
            """)
            
            rows = cursor.fetchall()
            
            for row in rows:
                inscriptions.append({
                    'id': row[0],
                    'pseudo': row[1],
                    'prenom': row[2],
                    'nom': row[3],
                    'email': row[4]
                })
        
        except Exception as e:
            print(f"❌ Erreur inscriptions : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return inscriptions
    
    def valider_inscription(self, user_id):
        reponse = messagebox.askyesno(
            "Validation",
            "Valider cette inscription et activer le compte ?"
        )
        
        if reponse:
            db = DatabaseManager()
            conn = None
            
            try:
                conn = db.create_connection()
                cursor = conn.cursor()
                
                cursor.execute("UPDATE utilisateurs SET statut = 'actif' WHERE id = ?", (user_id,))
                
                cursor.execute("""
                    INSERT OR IGNORE INTO stock_jokers (utilisateur_id, jokers_doubles_disponibles, jokers_voles_disponibles)
                    VALUES (?, 3, 2)
                """, (user_id,))
                
                conn.commit()
                
                messagebox.showinfo("Succès", "✅ Compte activé avec succès !")
                
                self.window.destroy()
                self.__init__()
                self.run()
            
            except Exception as e:
                messagebox.showerror("Erreur", f"❌ Erreur : {e}")
            
            finally:
                if conn:
                    conn.close()
    
    def refuser_inscription(self, user_id):
        reponse = messagebox.askyesno(
            "Refus",
            "Refuser cette inscription et supprimer le compte ?"
        )
        
        if reponse:
            db = DatabaseManager()
            conn = None
            
            try:
                conn = db.create_connection()
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM utilisateurs WHERE id = ?", (user_id,))
                conn.commit()
                
                messagebox.showinfo("Succès", "✅ Compte supprimé")
                
                self.window.destroy()
                self.__init__()
                self.run()
            
            except Exception as e:
                messagebox.showerror("Erreur", f"❌ Erreur : {e}")
            
            finally:
                if conn:
                    conn.close()
    
    def create_gestion_matchs(self, parent):
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
        
        header_frame = tk.Frame(scrollable_frame, bg=COULEUR_FOND)
        header_frame.pack(pady=20, fill="x")
        
        tk.Label(
            header_frame,
            text="⚽ GESTION DES MATCHS",
            font=("Arial", 18, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        ).pack()
        
        semaine_frame = tk.Frame(header_frame, bg=COULEUR_FOND)
        semaine_frame.pack(pady=10)
        
        tk.Label(
            semaine_frame,
            text="Semaine :",
            font=("Arial", 14),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND
        ).pack(side="left", padx=10)
        
        self.matchs_semaine_var = tk.StringVar(value="1")
        semaine_spinbox = tk.Spinbox(
            semaine_frame,
            from_=1,
            to=38,
            textvariable=self.matchs_semaine_var,
            font=("Arial", 14),
            width=5
        )
        semaine_spinbox.pack(side="left")
        
        tk.Button(
            semaine_frame,
            text="🔄 ACTUALISER",
            font=("Arial", 12, "bold"),
            bg=COULEUR_OR,
            fg="black",
            command=lambda: self.refresh_matchs()
        ).pack(side="left", padx=10)
        
        self.matchs_container = tk.Frame(scrollable_frame, bg=COULEUR_FOND)
        self.matchs_container.pack(fill="both", expand=True, padx=20)
        
        self.load_matchs(self.matchs_container)
    
    def refresh_matchs(self):
        for widget in self.matchs_container.winfo_children():
            widget.destroy()
        
        self.load_matchs(self.matchs_container)
    
    def load_matchs(self, parent):
        semaine = int(self.matchs_semaine_var.get())
        
        db = DatabaseManager()
        conn = None
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, equipe_domicile, equipe_exterieur, cote_domicile, cote_nul, cote_exterieur, date_match
                FROM matchs
                WHERE semaine = ?
                ORDER BY date_match
            """, (semaine,))
            
            matchs = cursor.fetchall()
            
            if not matchs:
                tk.Label(
                    parent,
                    text=f"⚠️ Aucun match pour la semaine {semaine}",
                    font=("Arial", 14),
                    fg=COULEUR_BLANC,
                    bg=COULEUR_FOND
                ).pack(pady=50)
            else:
                for match in matchs:
                    self.create_match_card(parent, match)
        
        except Exception as e:
            print(f"❌ Erreur chargement matchs : {e}")
        
        finally:
            if conn:
                conn.close()
    
    def create_match_card(self, parent, match):
        match_id, dom, ext, cote_d, cote_n, cote_e, date_match = match
        
        card = tk.Frame(parent, bg="#2C2C2C", relief="raised", borderwidth=2)
        card.pack(fill="x", pady=10)
        
        info_frame = tk.Frame(card, bg="#2C2C2C")
        info_frame.pack(side="left", fill="x", expand=True, padx=20, pady=15)
        
        tk.Label(
            info_frame,
            text=f"⚽ {dom} vs {ext}",
            font=("Arial", 14, "bold"),
            fg=COULEUR_OR,
            bg="#2C2C2C",
            anchor="w"
        ).pack(fill="x")
        
        tk.Label(
            info_frame,
            text=f"Cotes : {cote_d} - {cote_n} - {cote_e}",
            font=("Arial", 11),
            fg=COULEUR_BLANC,
            bg="#2C2C2C",
            anchor="w"
        ).pack(fill="x")
        
        tk.Label(
            info_frame,
            text=f"📅 {date_match}",
            font=("Arial", 10),
            fg="#AAAAAA",
            bg="#2C2C2C",
            anchor="w"
        ).pack(fill="x")
        
        tk.Button(
            card,
            text="✏️ MODIFIER",
            font=("Arial", 11, "bold"),
            bg=COULEUR_OR,
            fg="black",
            width=12,
            command=lambda: self.modifier_match(match_id)
        ).pack(side="right", padx=20)
    
    def modifier_match(self, match_id):
        edit_window = tk.Toplevel(self.window)
        edit_window.title("Modifier le match")
        edit_window.geometry("500x400")
        edit_window.configure(bg=COULEUR_FOND)
        
        tk.Label(
            edit_window,
            text="✏️ MODIFIER LE MATCH",
            font=("Arial", 18, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        ).pack(pady=20)
        
        db = DatabaseManager()
        conn = None
        match_data = None
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM matchs WHERE id = ?", (match_id,))
            match_data = cursor.fetchone()
        finally:
            if conn:
                conn.close()
        
        if not match_data:
            messagebox.showerror("Erreur", "Match introuvable")
            edit_window.destroy()
            return
        
        form_frame = tk.Frame(edit_window, bg=COULEUR_FOND)
        form_frame.pack(pady=20, padx=40, fill="both")
        
        fields = {}
        labels = ["Équipe Domicile", "Équipe Extérieur", "Cote Domicile", "Cote Nul", "Cote Extérieur"]
        indices = [2, 3, 4, 5, 6]
        
        for label, idx in zip(labels, indices):
            row = tk.Frame(form_frame, bg=COULEUR_FOND)
            row.pack(fill="x", pady=5)
            
            tk.Label(
                row,
                text=f"{label} :",
                font=("Arial", 12),
                fg=COULEUR_BLANC,
                bg=COULEUR_FOND,
                width=18,
                anchor="w"
            ).pack(side="left")
            
            entry = tk.Entry(row, font=("Arial", 12), width=20)
            entry.insert(0, str(match_data[idx]))
            entry.pack(side="left", padx=10)
            
            fields[label] = entry
        
        btn_frame = tk.Frame(edit_window, bg=COULEUR_FOND)
        btn_frame.pack(pady=30)
        
        def sauvegarder():
            try:
                db = DatabaseManager()
                conn = db.create_connection()
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE matchs
                    SET equipe_domicile = ?, equipe_exterieur = ?, 
                        cote_domicile = ?, cote_nul = ?, cote_exterieur = ?
                    WHERE id = ?
                """, (
                    fields["Équipe Domicile"].get(),
                    fields["Équipe Extérieur"].get(),
                    float(fields["Cote Domicile"].get()),
                    float(fields["Cote Nul"].get()),
                    float(fields["Cote Extérieur"].get()),
                    match_id
                ))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Succès", "✅ Match modifié")
                edit_window.destroy()
                self.refresh_matchs()
            
            except Exception as e:
                messagebox.showerror("Erreur", f"❌ {e}")
        
        tk.Button(
            btn_frame,
            text="💾 SAUVEGARDER",
            font=("Arial", 12, "bold"),
            bg="#00AA00",
            fg=COULEUR_BLANC,
            width=15,
            command=sauvegarder
        ).pack(side="left", padx=10)
        
        tk.Button(
            btn_frame,
            text="❌ ANNULER",
            font=("Arial", 12, "bold"),
            bg=COULEUR_ROUGE,
            fg=COULEUR_BLANC,
            width=15,
            command=edit_window.destroy
        ).pack(side="left", padx=10)
    
    def run(self):
        print("🚀 Lancement interface admin...")
        self.window.mainloop()

if __name__ == "__main__":
    app = InterfaceAdmin()
>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
    app.run()