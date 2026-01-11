<<<<<<< HEAD
import tkinter as tk
from tkinter import messagebox
from modules.database_manager import DatabaseManager
from modules.config import COULEUR_FOND, COULEUR_OR, COULEUR_BLANC

class RadarRecrutement:
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.cible_selectionnee = None
        
        self.window = tk.Toplevel()
        self.window.title("Radar de Recrutement - Choisir une cible")
        self.window.geometry("800x600")
        self.window.configure(bg=COULEUR_FOND)
        self.window.resizable(False, False)
        
        self.center_window()
        
        self.joueurs_eligibles = self.load_joueurs_eligibles()
        
        self.create_interface()
        
        self.window.grab_set()
    
    def center_window(self):
        self.window.update_idletasks()
        width = 800
        height = 600
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def load_joueurs_eligibles(self):
        db = DatabaseManager()
        conn = None
        joueurs = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    u.id, 
                    u.pseudo,
                    COALESCE(SUM(h.points_totaux), 0) as total_points,
                    COALESCE(SUM(h.bons_pronos), 0) as bons_pronos,
                    COALESCE(
                        (SELECT grand_chelem FROM historique 
                         WHERE utilisateur_id = u.id 
                         ORDER BY semaine DESC LIMIT 1), 0
                    ) as dernier_grand_chelem
                FROM utilisateurs u
                LEFT JOIN historique h ON u.id = h.utilisateur_id
                WHERE u.id != ? AND u.statut = 'actif'
                GROUP BY u.id, u.pseudo
            """, (self.user_id,))
            
            rows = cursor.fetchall()
            
            for row in rows:
                user_id = row[0]
                pseudo = row[1]
                total_points = row[2]
                bons_pronos = row[3]
                grand_chelem = row[4]
                
                budget = 140 if grand_chelem == 1 else 100
                
                if budget == 100:
                    joueurs.append({
                        'id': user_id,
                        'pseudo': pseudo,
                        'points': total_points,
                        'bons_pronos': bons_pronos,
                        'budget': budget
                    })
            
            print(f"✅ {len(joueurs)} joueur(s) éligible(s) chargé(s)")
            
        except Exception as e:
            print(f"❌ Erreur chargement joueurs : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return joueurs
    
    def create_interface(self):
        titre = tk.Label(
            self.window,
            text="🎯 RADAR DE RECRUTEMENT",
            font=("Impact", 28, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        )
        titre.pack(pady=20)
        
        sous_titre = tk.Label(
            self.window,
            text="Sélectionne un joueur à cibler (uniquement ceux à 100 points)",
            font=("Arial", 12),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND
        )
        sous_titre.pack(pady=5)
        
        if not self.joueurs_eligibles:
            tk.Label(
                self.window,
                text="❌ Aucun joueur éligible disponible",
                font=("Arial", 14, "bold"),
                fg="#FF4444",
                bg=COULEUR_FOND
            ).pack(pady=50)
            
            tk.Button(
                self.window,
                text="Fermer",
                font=("Arial", 14),
                bg=COULEUR_OR,
                fg="black",
                command=self.window.destroy
            ).pack(pady=20)
            return
        
        tableau_frame = tk.Frame(self.window, bg=COULEUR_FOND)
        tableau_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        header_frame = tk.Frame(tableau_frame, bg="#2C2C2C", height=40)
        header_frame.pack(fill="x")
        
        headers = ["PSEUDO", "POINTS TOTAUX", "BONS PRONOS", "ACTION"]
        widths = [200, 150, 150, 150]
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            tk.Label(
                header_frame,
                text=header,
                font=("Arial", 11, "bold"),
                fg=COULEUR_OR,
                bg="#2C2C2C",
                width=width//8
            ).pack(side="left", padx=5)
        
        canvas = tk.Canvas(tableau_frame, bg=COULEUR_FOND, highlightthickness=0)
        scrollbar = tk.Scrollbar(tableau_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COULEUR_FOND)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        for idx, joueur in enumerate(self.joueurs_eligibles):
            bg_color = "#1A1A1A" if idx % 2 == 0 else "#252525"
            
            row_frame = tk.Frame(scrollable_frame, bg=bg_color, height=50)
            row_frame.pack(fill="x", pady=2)
            
            tk.Label(
                row_frame,
                text=joueur['pseudo'],
                font=("Arial", 11, "bold"),
                fg=COULEUR_BLANC,
                bg=bg_color,
                width=25,
                anchor="w"
            ).pack(side="left", padx=10)
            
            tk.Label(
                row_frame,
                text=f"{joueur['points']:.1f}",
                font=("Arial", 11),
                fg=COULEUR_BLANC,
                bg=bg_color,
                width=18
            ).pack(side="left", padx=5)
            
            tk.Label(
                row_frame,
                text=str(joueur['bons_pronos']),
                font=("Arial", 11),
                fg=COULEUR_BLANC,
                bg=bg_color,
                width=18
            ).pack(side="left", padx=5)
            
            tk.Button(
                row_frame,
                text="✅ CIBLER",
                font=("Arial", 10, "bold"),
                bg="#00DD00",
                fg="black",
                width=12,
                command=lambda j=joueur: self.selectionner_cible(j)
            ).pack(side="left", padx=10)
    
    def selectionner_cible(self, joueur):
        reponse = messagebox.askyesno(
            "Confirmation",
            f"Confirmer le vol des pronos de {joueur['pseudo']} ?\n\n"
            f"Tu copieras ses pronos pour cette semaine."
        )
        
        if reponse:
            self.cible_selectionnee = joueur['id']
            print(f"✅ Cible sélectionnée : {joueur['pseudo']} (ID: {joueur['id']})")
            self.window.destroy()
    
    def run(self):
        self.window.wait_window()
=======
import tkinter as tk
from tkinter import messagebox
from modules.database_manager import DatabaseManager
from modules.config import COULEUR_FOND, COULEUR_OR, COULEUR_BLANC

class RadarRecrutement:
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.cible_selectionnee = None
        
        self.window = tk.Toplevel()
        self.window.title("Radar de Recrutement - Choisir une cible")
        self.window.geometry("800x600")
        self.window.configure(bg=COULEUR_FOND)
        self.window.resizable(False, False)
        
        self.center_window()
        
        self.joueurs_eligibles = self.load_joueurs_eligibles()
        
        self.create_interface()
        
        self.window.grab_set()
    
    def center_window(self):
        self.window.update_idletasks()
        width = 800
        height = 600
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def load_joueurs_eligibles(self):
        db = DatabaseManager()
        conn = None
        joueurs = []
        
        try:
            conn = db.create_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    u.id, 
                    u.pseudo,
                    COALESCE(SUM(h.points_totaux), 0) as total_points,
                    COALESCE(SUM(h.bons_pronos), 0) as bons_pronos,
                    COALESCE(
                        (SELECT grand_chelem FROM historique 
                         WHERE utilisateur_id = u.id 
                         ORDER BY semaine DESC LIMIT 1), 0
                    ) as dernier_grand_chelem
                FROM utilisateurs u
                LEFT JOIN historique h ON u.id = h.utilisateur_id
                WHERE u.id != ? AND u.statut = 'actif'
                GROUP BY u.id, u.pseudo
            """, (self.user_id,))
            
            rows = cursor.fetchall()
            
            for row in rows:
                user_id = row[0]
                pseudo = row[1]
                total_points = row[2]
                bons_pronos = row[3]
                grand_chelem = row[4]
                
                budget = 140 if grand_chelem == 1 else 100
                
                if budget == 100:
                    joueurs.append({
                        'id': user_id,
                        'pseudo': pseudo,
                        'points': total_points,
                        'bons_pronos': bons_pronos,
                        'budget': budget
                    })
            
            print(f"✅ {len(joueurs)} joueur(s) éligible(s) chargé(s)")
            
        except Exception as e:
            print(f"❌ Erreur chargement joueurs : {e}")
        
        finally:
            if conn:
                conn.close()
        
        return joueurs
    
    def create_interface(self):
        titre = tk.Label(
            self.window,
            text="🎯 RADAR DE RECRUTEMENT",
            font=("Impact", 28, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        )
        titre.pack(pady=20)
        
        sous_titre = tk.Label(
            self.window,
            text="Sélectionne un joueur à cibler (uniquement ceux à 100 points)",
            font=("Arial", 12),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND
        )
        sous_titre.pack(pady=5)
        
        if not self.joueurs_eligibles:
            tk.Label(
                self.window,
                text="❌ Aucun joueur éligible disponible",
                font=("Arial", 14, "bold"),
                fg="#FF4444",
                bg=COULEUR_FOND
            ).pack(pady=50)
            
            tk.Button(
                self.window,
                text="Fermer",
                font=("Arial", 14),
                bg=COULEUR_OR,
                fg="black",
                command=self.window.destroy
            ).pack(pady=20)
            return
        
        tableau_frame = tk.Frame(self.window, bg=COULEUR_FOND)
        tableau_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        header_frame = tk.Frame(tableau_frame, bg="#2C2C2C", height=40)
        header_frame.pack(fill="x")
        
        headers = ["PSEUDO", "POINTS TOTAUX", "BONS PRONOS", "ACTION"]
        widths = [200, 150, 150, 150]
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            tk.Label(
                header_frame,
                text=header,
                font=("Arial", 11, "bold"),
                fg=COULEUR_OR,
                bg="#2C2C2C",
                width=width//8
            ).pack(side="left", padx=5)
        
        canvas = tk.Canvas(tableau_frame, bg=COULEUR_FOND, highlightthickness=0)
        scrollbar = tk.Scrollbar(tableau_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COULEUR_FOND)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        for idx, joueur in enumerate(self.joueurs_eligibles):
            bg_color = "#1A1A1A" if idx % 2 == 0 else "#252525"
            
            row_frame = tk.Frame(scrollable_frame, bg=bg_color, height=50)
            row_frame.pack(fill="x", pady=2)
            
            tk.Label(
                row_frame,
                text=joueur['pseudo'],
                font=("Arial", 11, "bold"),
                fg=COULEUR_BLANC,
                bg=bg_color,
                width=25,
                anchor="w"
            ).pack(side="left", padx=10)
            
            tk.Label(
                row_frame,
                text=f"{joueur['points']:.1f}",
                font=("Arial", 11),
                fg=COULEUR_BLANC,
                bg=bg_color,
                width=18
            ).pack(side="left", padx=5)
            
            tk.Label(
                row_frame,
                text=str(joueur['bons_pronos']),
                font=("Arial", 11),
                fg=COULEUR_BLANC,
                bg=bg_color,
                width=18
            ).pack(side="left", padx=5)
            
            tk.Button(
                row_frame,
                text="✅ CIBLER",
                font=("Arial", 10, "bold"),
                bg="#00DD00",
                fg="black",
                width=12,
                command=lambda j=joueur: self.selectionner_cible(j)
            ).pack(side="left", padx=10)
    
    def selectionner_cible(self, joueur):
        reponse = messagebox.askyesno(
            "Confirmation",
            f"Confirmer le vol des pronos de {joueur['pseudo']} ?\n\n"
            f"Tu copieras ses pronos pour cette semaine."
        )
        
        if reponse:
            self.cible_selectionnee = joueur['id']
            print(f"✅ Cible sélectionnée : {joueur['pseudo']} (ID: {joueur['id']})")
            self.window.destroy()
    
    def run(self):
        self.window.wait_window()
>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
        return self.cible_selectionnee