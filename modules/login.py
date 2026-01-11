<<<<<<< HEAD
# login.py - Module de connexion des joueurs

import tkinter as tk
from tkinter import messagebox
from modules.database_manager import DatabaseManager
import sqlite3
from modules.config import FENETRE_LARGEUR, FENETRE_HAUTEUR
from modules.config import COULEUR_FOND, COULEUR_OR, COULEUR_BLANC

class LoginWindow:
    """
    Classe pour gérer la fenêtre de connexion.
    Permet aux joueurs de se connecter avec leur Pseudo et PIN.
    """
    
    def __init__(self):
        """
        Initialise la fenêtre de connexion.
        """
        # Crée la fenêtre principale
        self.window = tk.Tk()
        self.window.title("Elite Pronos 2 - Connexion")
        
        # Définit les dimensions (plus petite que l'inscription)
        largeur = 600
        hauteur = 650
        self.window.geometry(f"{largeur}x{hauteur}")
        
        # Couleur de fond (bleu nuit)
        self.window.configure(bg=COULEUR_FOND)
        
        # Empêche le redimensionnement
        self.window.resizable(False, False)
        
        # Centre la fenêtre sur l'écran
        self.center_window(largeur, hauteur)
        
        print("✅ Fenêtre de connexion créée")
        
        # Variable pour stocker l'utilisateur connecté
        self.user_data = None
        
        # Appelle la méthode pour créer l'interface
        self.create_interface()
    
    def center_window(self, width, height):
        """
        Centre la fenêtre sur l'écran.
        """
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_interface(self):
        """
        Crée tous les éléments de l'interface de connexion.
        """
        # LOGO / TITRE PRINCIPAL
        titre = tk.Label(
            self.window,
            text="ELITE PRONOS 2",
            font=("Impact", 40, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        )
        titre.pack(pady=40)
        
        # SOUS-TITRE
        sous_titre = tk.Label(
            self.window,
            text="CONNEXION À L'ARÈNE",
            font=("Impact", 18),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND
        )
        sous_titre.pack(pady=10)
        
        # CONTENEUR CENTRAL
        form_frame = tk.Frame(self.window, bg=COULEUR_FOND)
        form_frame.pack(pady=30)
        
        # === CHAMP PSEUDO ===
        label_pseudo = tk.Label(
            form_frame,
            text="Pseudo :",
            font=("Arial", 14, "bold"),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND
        )
        label_pseudo.pack(pady=(10, 5))
        
        self.entry_pseudo = tk.Entry(
            form_frame,
            font=("Arial", 16),
            bg=COULEUR_BLANC,
            fg="black",
            width=25,
            justify="center"
        )
        self.entry_pseudo.pack(pady=5)
        
        # === CHAMP PIN ===
        label_pin = tk.Label(
            form_frame,
            text="Code PIN :",
            font=("Arial", 14, "bold"),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND
        )
        label_pin.pack(pady=(20, 5))
        
        self.entry_pin = tk.Entry(
            form_frame,
            font=("Arial", 16),
            bg=COULEUR_BLANC,
            fg="black",
            width=25,
            show="*",
            justify="center"
        )
        self.entry_pin.pack(pady=5)
        
        # Permet de valider avec la touche Entrée
        self.entry_pin.bind("<Return>", lambda e: self.se_connecter())
        
        # === BOUTON SE CONNECTER ===
        btn_login = tk.Button(
            form_frame,
            text="🔓 SE CONNECTER",
            font=("Arial", 16, "bold"),
            bg=COULEUR_OR,
            fg="black",
            width=20,
            height=2,
            command=self.se_connecter
        )
        btn_login.pack(pady=30)
        
        # === LIEN INSCRIPTION ===
        label_inscription = tk.Label(
            self.window,
            text="Pas encore de compte ?",
            font=("Arial", 10),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND
        )
        label_inscription.pack()
        
        btn_inscription = tk.Button(
            self.window,
            text="Créer un compte",
            font=("Arial", 10, "underline"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND,
            bd=0,
            cursor="hand2",
            command=self.ouvrir_inscription
        )
        btn_inscription.pack()
        
        print("✅ Interface de connexion créée")
    
    def se_connecter(self):
        """
        Vérifie les identifiants et connecte l'utilisateur.
        """
        # Récupération des données
        pseudo = self.entry_pseudo.get().strip()
        pin = self.entry_pin.get().strip()
        
        # Validation des champs
        if not pseudo:
            messagebox.showerror("Erreur", "Le Pseudo est obligatoire !")
            return
        
        if not pin:
            messagebox.showerror("Erreur", "Le Code PIN est obligatoire !")
            return
        
        # Vérification dans la base de données
        db = DatabaseManager()
        conn = None
        
        try:
            conn = db.create_connection()
            
            if conn is None:
                messagebox.showerror("Erreur", "Impossible de se connecter à la base de données !")
                return
            
            cursor = conn.cursor()
            
            # Recherche de l'utilisateur
            cursor.execute("""
                SELECT id, pseudo, prenom, email, avatar_path, statut
                FROM utilisateurs
                WHERE pseudo = ? AND pin = ?
            """, (pseudo, pin))
            
            user = cursor.fetchone()
            
            if user is None:
                # Identifiants incorrects
                messagebox.showerror(
                    "Erreur",
                    "Pseudo ou PIN incorrect !\n\n"
                    "Vérifie tes identifiants et réessaye."
                )
                print(f"❌ Tentative de connexion échouée : {pseudo}")
                
            elif user[5] == 'en_attente':
                # Compte en attente de validation
                messagebox.showwarning(
                    "Compte en attente",
                    f"Ton compte est en attente de validation.\n\n"
                    f"Un administrateur doit approuver ton inscription.\n"
                    f"Tu recevras une notification dès que ce sera fait."
                )
                print(f"⏳ Connexion refusée (en attente) : {pseudo}")
                
            else:
                # Connexion réussie
                self.user_data = {
                    'id': user[0],
                    'pseudo': user[1],
                    'prenom': user[2],
                    'email': user[3],
                    'avatar_path': user[4],
                    'statut': user[5]
                }
                
                print(f"✅ Connexion réussie : {pseudo} (ID: {user[0]})")
                
                # Ferme la fenêtre de connexion
                self.window.destroy()
                
                # Ouvre le dashboard
                from modules.dashboard import DashboardWindow
                dashboard = DashboardWindow(self.user_data)
                dashboard.run()
            
        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Une erreur s'est produite :\n{str(e)}"
            )
            print(f"❌ Erreur lors de la connexion : {e}")
            
        finally:
            if conn:
                conn.close()
                print("🔒 Connexion fermée")
    
    def ouvrir_inscription(self):
        """
        Ouvre la fenêtre d'inscription.
        """
        print("📝 Ouverture de la fenêtre d'inscription...")
        self.window.destroy()
        
        # Import ici pour éviter les imports circulaires
        from modules.inscription import InscriptionWindow
        inscription = InscriptionWindow()
        inscription.run()
    
    def run(self):
        """
        Lance la fenêtre (boucle principale).
        """
        print("🚀 Lancement de la fenêtre de connexion...")
        self.window.mainloop()
        
        # Retourne les données de l'utilisateur connecté (ou None)
        return self.user_data

# ===================================
# TEST DU MODULE
# ===================================
if __name__ == "__main__":
    print("🧪 Test du module de connexion\n")
    
    # Crée et lance la fenêtre
    app = LoginWindow()
    user = app.run()
    
    if user:
=======
# login.py - Module de connexion des joueurs

import tkinter as tk
from tkinter import messagebox
from modules.database_manager import DatabaseManager
import sqlite3
from modules.config import FENETRE_LARGEUR, FENETRE_HAUTEUR
from modules.config import COULEUR_FOND, COULEUR_OR, COULEUR_BLANC

class LoginWindow:
    """
    Classe pour gérer la fenêtre de connexion.
    Permet aux joueurs de se connecter avec leur Pseudo et PIN.
    """
    
    def __init__(self):
        """
        Initialise la fenêtre de connexion.
        """
        # Crée la fenêtre principale
        self.window = tk.Tk()
        self.window.title("Elite Pronos 2 - Connexion")
        
        # Définit les dimensions (plus petite que l'inscription)
        largeur = 600
        hauteur = 650
        self.window.geometry(f"{largeur}x{hauteur}")
        
        # Couleur de fond (bleu nuit)
        self.window.configure(bg=COULEUR_FOND)
        
        # Empêche le redimensionnement
        self.window.resizable(False, False)
        
        # Centre la fenêtre sur l'écran
        self.center_window(largeur, hauteur)
        
        print("✅ Fenêtre de connexion créée")
        
        # Variable pour stocker l'utilisateur connecté
        self.user_data = None
        
        # Appelle la méthode pour créer l'interface
        self.create_interface()
    
    def center_window(self, width, height):
        """
        Centre la fenêtre sur l'écran.
        """
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_interface(self):
        """
        Crée tous les éléments de l'interface de connexion.
        """
        # LOGO / TITRE PRINCIPAL
        titre = tk.Label(
            self.window,
            text="ELITE PRONOS 2",
            font=("Impact", 40, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        )
        titre.pack(pady=40)
        
        # SOUS-TITRE
        sous_titre = tk.Label(
            self.window,
            text="CONNEXION À L'ARÈNE",
            font=("Impact", 18),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND
        )
        sous_titre.pack(pady=10)
        
        # CONTENEUR CENTRAL
        form_frame = tk.Frame(self.window, bg=COULEUR_FOND)
        form_frame.pack(pady=30)
        
        # === CHAMP PSEUDO ===
        label_pseudo = tk.Label(
            form_frame,
            text="Pseudo :",
            font=("Arial", 14, "bold"),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND
        )
        label_pseudo.pack(pady=(10, 5))
        
        self.entry_pseudo = tk.Entry(
            form_frame,
            font=("Arial", 16),
            bg=COULEUR_BLANC,
            fg="black",
            width=25,
            justify="center"
        )
        self.entry_pseudo.pack(pady=5)
        
        # === CHAMP PIN ===
        label_pin = tk.Label(
            form_frame,
            text="Code PIN :",
            font=("Arial", 14, "bold"),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND
        )
        label_pin.pack(pady=(20, 5))
        
        self.entry_pin = tk.Entry(
            form_frame,
            font=("Arial", 16),
            bg=COULEUR_BLANC,
            fg="black",
            width=25,
            show="*",
            justify="center"
        )
        self.entry_pin.pack(pady=5)
        
        # Permet de valider avec la touche Entrée
        self.entry_pin.bind("<Return>", lambda e: self.se_connecter())
        
        # === BOUTON SE CONNECTER ===
        btn_login = tk.Button(
            form_frame,
            text="🔓 SE CONNECTER",
            font=("Arial", 16, "bold"),
            bg=COULEUR_OR,
            fg="black",
            width=20,
            height=2,
            command=self.se_connecter
        )
        btn_login.pack(pady=30)
        
        # === LIEN INSCRIPTION ===
        label_inscription = tk.Label(
            self.window,
            text="Pas encore de compte ?",
            font=("Arial", 10),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND
        )
        label_inscription.pack()
        
        btn_inscription = tk.Button(
            self.window,
            text="Créer un compte",
            font=("Arial", 10, "underline"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND,
            bd=0,
            cursor="hand2",
            command=self.ouvrir_inscription
        )
        btn_inscription.pack()
        
        print("✅ Interface de connexion créée")
    
    def se_connecter(self):
        """
        Vérifie les identifiants et connecte l'utilisateur.
        """
        # Récupération des données
        pseudo = self.entry_pseudo.get().strip()
        pin = self.entry_pin.get().strip()
        
        # Validation des champs
        if not pseudo:
            messagebox.showerror("Erreur", "Le Pseudo est obligatoire !")
            return
        
        if not pin:
            messagebox.showerror("Erreur", "Le Code PIN est obligatoire !")
            return
        
        # Vérification dans la base de données
        db = DatabaseManager()
        conn = None
        
        try:
            conn = db.create_connection()
            
            if conn is None:
                messagebox.showerror("Erreur", "Impossible de se connecter à la base de données !")
                return
            
            cursor = conn.cursor()
            
            # Recherche de l'utilisateur
            cursor.execute("""
                SELECT id, pseudo, prenom, email, avatar_path, statut
                FROM utilisateurs
                WHERE pseudo = ? AND pin = ?
            """, (pseudo, pin))
            
            user = cursor.fetchone()
            
            if user is None:
                # Identifiants incorrects
                messagebox.showerror(
                    "Erreur",
                    "Pseudo ou PIN incorrect !\n\n"
                    "Vérifie tes identifiants et réessaye."
                )
                print(f"❌ Tentative de connexion échouée : {pseudo}")
                
            elif user[5] == 'en_attente':
                # Compte en attente de validation
                messagebox.showwarning(
                    "Compte en attente",
                    f"Ton compte est en attente de validation.\n\n"
                    f"Un administrateur doit approuver ton inscription.\n"
                    f"Tu recevras une notification dès que ce sera fait."
                )
                print(f"⏳ Connexion refusée (en attente) : {pseudo}")
                
            else:
                # Connexion réussie
                self.user_data = {
                    'id': user[0],
                    'pseudo': user[1],
                    'prenom': user[2],
                    'email': user[3],
                    'avatar_path': user[4],
                    'statut': user[5]
                }
                
                print(f"✅ Connexion réussie : {pseudo} (ID: {user[0]})")
                
                # Ferme la fenêtre de connexion
                self.window.destroy()
                
                # Ouvre le dashboard
                from modules.dashboard import DashboardWindow
                dashboard = DashboardWindow(self.user_data)
                dashboard.run()
            
        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Une erreur s'est produite :\n{str(e)}"
            )
            print(f"❌ Erreur lors de la connexion : {e}")
            
        finally:
            if conn:
                conn.close()
                print("🔒 Connexion fermée")
    
    def ouvrir_inscription(self):
        """
        Ouvre la fenêtre d'inscription.
        """
        print("📝 Ouverture de la fenêtre d'inscription...")
        self.window.destroy()
        
        # Import ici pour éviter les imports circulaires
        from modules.inscription import InscriptionWindow
        inscription = InscriptionWindow()
        inscription.run()
    
    def run(self):
        """
        Lance la fenêtre (boucle principale).
        """
        print("🚀 Lancement de la fenêtre de connexion...")
        self.window.mainloop()
        
        # Retourne les données de l'utilisateur connecté (ou None)
        return self.user_data

# ===================================
# TEST DU MODULE
# ===================================
if __name__ == "__main__":
    print("🧪 Test du module de connexion\n")
    
    # Crée et lance la fenêtre
    app = LoginWindow()
    user = app.run()
    
    if user:
>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
        print(f"\n✅ Utilisateur connecté : {user}")