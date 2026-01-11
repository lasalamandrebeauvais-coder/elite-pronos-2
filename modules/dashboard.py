<<<<<<< HEAD
# dashboard.py - Interface principale après connexion

import tkinter as tk
from tkinter import messagebox
from modules.config import FENETRE_LARGEUR, FENETRE_HAUTEUR
from modules.config import COULEUR_FOND, COULEUR_OR, COULEUR_BLANC, COULEUR_ROUGE
from PIL import Image, ImageTk
import os

class DashboardWindow:
    """
    Classe pour gérer l'interface principale (tableau de bord).
    Affichée après une connexion réussie.
    """
    
    def __init__(self, user_data):
        """
        Initialise le tableau de bord.
        
        Args:
            user_data (dict): Données de l'utilisateur connecté
        """
        self.user_data = user_data
        
        # Crée la fenêtre principale
        self.window = tk.Tk()
        self.window.title(f"Elite Pronos 2 - Bienvenue {user_data['pseudo']}")
        
        # Définit les dimensions
        self.window.geometry(f"{FENETRE_LARGEUR}x{FENETRE_HAUTEUR}")
        
        # Couleur de fond
        self.window.configure(bg=COULEUR_FOND)
        
        # Empêche le redimensionnement
        self.window.resizable(False, False)
        
        print(f"✅ Dashboard créé pour {user_data['pseudo']}")
        
        # Appelle la méthode pour créer l'interface
        self.create_interface()
    
    def create_interface(self):
        """
        Crée tous les éléments de l'interface principale.
        """
        # === EN-TÊTE ===
        header_frame = tk.Frame(self.window, bg=COULEUR_OR, height=100)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Conteneur pour centrer le contenu de l'en-tête
        header_content = tk.Frame(header_frame, bg=COULEUR_OR)
        header_content.pack(expand=True)
        
        # Avatar (si disponible)
        avatar_label = tk.Label(
            header_content,
            text="👤",
            font=("Arial", 40),
            bg=COULEUR_OR,
            fg="black"
        )
        avatar_label.pack(side=tk.LEFT, padx=20)
        
        # Informations utilisateur
        info_frame = tk.Frame(header_content, bg=COULEUR_OR)
        info_frame.pack(side=tk.LEFT, padx=10)
        
        pseudo_label = tk.Label(
            info_frame,
            text=f"{self.user_data['pseudo']}",
            font=("Impact", 24, "bold"),
            bg=COULEUR_OR,
            fg="black"
        )
        pseudo_label.pack(anchor="w")
        
        if self.user_data.get('prenom'):
            prenom_label = tk.Label(
                info_frame,
                text=f"{self.user_data['prenom']}",
                font=("Arial", 14),
                bg=COULEUR_OR,
                fg="black"
            )
            prenom_label.pack(anchor="w")
        
        # Bouton déconnexion
        btn_logout = tk.Button(
            header_content,
            text="🚪 DÉCONNEXION",
            font=("Arial", 10, "bold"),
            bg=COULEUR_ROUGE,
            fg=COULEUR_BLANC,
            command=self.deconnexion
        )
        btn_logout.pack(side=tk.RIGHT, padx=20)
        
        # === TITRE PRINCIPAL ===
        titre = tk.Label(
            self.window,
            text="🏆 TABLEAU DE BORD 🏆",
            font=("Impact", 32, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        )
        titre.pack(pady=20)
        
        # === ZONE CENTRALE : STATISTIQUES ===
        stats_frame = tk.Frame(self.window, bg=COULEUR_FOND)
        stats_frame.pack(pady=20)
        
        # Classement
        self.create_stat_box(
            stats_frame,
            "📊 CLASSEMENT",
            "1er",
            0
        )
        
        # Forme du moment (5 dernières perfs)
        self.create_forme_box(stats_frame, 1)
        
        # Jokers disponibles
        self.create_stat_box(
            stats_frame,
            "🃏 MES JOKERS",
            "3 Doubles | 2 Volés",
            2
        )
        
        # === MENU DE NAVIGATION ===
        menu_frame = tk.Frame(self.window, bg=COULEUR_FOND)
        menu_frame.pack(pady=30)
        
        # Bouton : Faire mes pronos
        self.create_menu_button(
            menu_frame,
            "📝 FAIRE MES PRONOS",
            self.faire_pronos,
            0, 0
        )
        
        # Bouton : Voir le classement
        self.create_menu_button(
            menu_frame,
            "📊 CLASSEMENT",
            self.voir_classement,
            0, 1
        )
        
        # Bouton : Pronos des amis
        self.create_menu_button(
            menu_frame,
            "👥 PRONOS DES AMIS",
            self.voir_pronos_amis,
            1, 0
        )
        
        # Bouton : Mon profil
        self.create_menu_button(
            menu_frame,
            "⚙️ MON PROFIL",
            self.mon_profil,
            1, 1
        )
        
        # === FOOTER ===
        footer_frame = tk.Frame(self.window, bg=COULEUR_FOND)
        footer_frame.pack(side=tk.BOTTOM, pady=20)
        
        semaine_label = tk.Label(
            footer_frame,
            text="📅 Semaine 1 | Date limite : Vendredi 23:59",
            font=("Arial", 12),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND
        )
        semaine_label.pack()
        
        print("✅ Interface du dashboard créée")
    
    def create_forme_box(self, parent, column):
        """
        Crée la boîte de forme avec les 5 dernières performances.
        """
        box = tk.Frame(
            parent,
            bg=COULEUR_OR,
            width=250,
            height=120,
            relief="raised",
            borderwidth=3
        )
        box.grid(row=0, column=column, padx=15, pady=10)
        box.pack_propagate(False)
        
        titre_label = tk.Label(
            box,
            text="📈 FORME DU MOMENT",
            font=("Arial", 14, "bold"),
            bg=COULEUR_OR,
            fg="black"
        )
        titre_label.pack(pady=(15, 10))
        
        # Tendance des 5 dernières semaines
        tendance_frame = tk.Frame(box, bg=COULEUR_OR)
        tendance_frame.pack()
        
        # Exemple : ⬆️⬆️➡️⬇️⬆️
        tendances = ["⬆️", "⬆️", "➡️", "⬇️", "⬆️"]
        couleurs = ["#00FF00", "#00FF00", "#808080", "#FF0000", "#00FF00"]
        
        for symbole, couleur in zip(tendances, couleurs):
            tk.Label(
                tendance_frame,
                text=symbole,
                font=("Arial", 20),
                bg=COULEUR_OR,
                fg=couleur
            ).pack(side=tk.LEFT, padx=3)
    
    def create_stat_box(self, parent, titre, valeur, column):
        """
        Crée une boîte de statistique.
        """
        box = tk.Frame(
            parent,
            bg=COULEUR_OR,
            width=250,
            height=120,
            relief="raised",
            borderwidth=3
        )
        box.grid(row=0, column=column, padx=15, pady=10)
        box.pack_propagate(False)
        
        titre_label = tk.Label(
            box,
            text=titre,
            font=("Arial", 14, "bold"),
            bg=COULEUR_OR,
            fg="black"
        )
        titre_label.pack(pady=(15, 5))
        
        valeur_label = tk.Label(
            box,
            text=valeur,
            font=("Arial", 18, "bold"),
            bg=COULEUR_OR,
            fg="black"
        )
        valeur_label.pack(pady=5)
    
    def create_menu_button(self, parent, text, command, row, column):
        """
        Crée un bouton de menu.
        """
        btn = tk.Button(
            parent,
            text=text,
            font=("Arial", 14, "bold"),
            bg=COULEUR_BLANC,
            fg="black",
            width=25,
            height=3,
            command=command
        )
        btn.grid(row=row, column=column, padx=15, pady=10)
    
    def faire_pronos(self):
        """
        Ouvre l'interface de saisie des pronos.
        """
        print("📝 Ouverture de la saisie des pronos...")
        self.window.destroy()
        
        from modules.saisie_pronos import SaisiePronosWindow
        saisie = SaisiePronosWindow(self.user_data)
        saisie.run()
        
        # Retour au dashboard après validation
        from modules.dashboard import DashboardWindow
        dashboard = DashboardWindow(self.user_data)
        dashboard.run()
    
    def voir_classement(self):
        """
        Ouvre l'interface du classement.
        """
        print("📊 Ouverture du classement...")
        self.window.withdraw()
        
        from modules.classement import ClassementWindow
        classement = ClassementWindow(self.user_data)
        classement.run()
        
        self.window.deiconify()
    
    def voir_pronos_amis(self):
        """
        Ouvre l'interface des pronos des amis.
        """
        messagebox.showinfo("Info", "Module 'Pronos des amis' en cours de développement...")
    
    def mon_profil(self):
        """
        Ouvre l'interface du profil utilisateur.
        """
        messagebox.showinfo("Info", "Module 'Mon profil' en cours de développement...")
    
    def deconnexion(self):
        """
        Déconnecte l'utilisateur et retourne à l'écran de login.
        """
        reponse = messagebox.askyesno(
            "Déconnexion",
            "Es-tu sûr de vouloir te déconnecter ?"
        )
        
        if reponse:
            print(f"🚪 Déconnexion de {self.user_data['pseudo']}")
            self.window.destroy()
            
            # Relance la fenêtre de login
            from modules.login import LoginWindow
            login = LoginWindow()
            login.run()
    
    def run(self):
        """
        Lance la fenêtre (boucle principale).
        """
        print("🚀 Lancement du dashboard...")
        self.window.mainloop()

# ===================================
# TEST DU MODULE
# ===================================
if __name__ == "__main__":
    print("🧪 Test du module dashboard\n")
    
    # Données de test
    test_user = {
        'id': 1,
        'pseudo': 'TestUser',
        'prenom': 'Jean',
        'email': 'test@test.com',
        'avatar_path': None,
        'statut': 'actif'
    }
    
    # Crée et lance le dashboard
    app = DashboardWindow(test_user)
=======
# dashboard.py - Interface principale après connexion

import tkinter as tk
from tkinter import messagebox
from modules.config import FENETRE_LARGEUR, FENETRE_HAUTEUR
from modules.config import COULEUR_FOND, COULEUR_OR, COULEUR_BLANC, COULEUR_ROUGE
from PIL import Image, ImageTk
import os

class DashboardWindow:
    """
    Classe pour gérer l'interface principale (tableau de bord).
    Affichée après une connexion réussie.
    """
    
    def __init__(self, user_data):
        """
        Initialise le tableau de bord.
        
        Args:
            user_data (dict): Données de l'utilisateur connecté
        """
        self.user_data = user_data
        
        # Crée la fenêtre principale
        self.window = tk.Tk()
        self.window.title(f"Elite Pronos 2 - Bienvenue {user_data['pseudo']}")
        
        # Définit les dimensions
        self.window.geometry(f"{FENETRE_LARGEUR}x{FENETRE_HAUTEUR}")
        
        # Couleur de fond
        self.window.configure(bg=COULEUR_FOND)
        
        # Empêche le redimensionnement
        self.window.resizable(False, False)
        
        print(f"✅ Dashboard créé pour {user_data['pseudo']}")
        
        # Appelle la méthode pour créer l'interface
        self.create_interface()
    
    def create_interface(self):
        """
        Crée tous les éléments de l'interface principale.
        """
        # === EN-TÊTE ===
        header_frame = tk.Frame(self.window, bg=COULEUR_OR, height=100)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Conteneur pour centrer le contenu de l'en-tête
        header_content = tk.Frame(header_frame, bg=COULEUR_OR)
        header_content.pack(expand=True)
        
        # Avatar (si disponible)
        avatar_label = tk.Label(
            header_content,
            text="👤",
            font=("Arial", 40),
            bg=COULEUR_OR,
            fg="black"
        )
        avatar_label.pack(side=tk.LEFT, padx=20)
        
        # Informations utilisateur
        info_frame = tk.Frame(header_content, bg=COULEUR_OR)
        info_frame.pack(side=tk.LEFT, padx=10)
        
        pseudo_label = tk.Label(
            info_frame,
            text=f"{self.user_data['pseudo']}",
            font=("Impact", 24, "bold"),
            bg=COULEUR_OR,
            fg="black"
        )
        pseudo_label.pack(anchor="w")
        
        if self.user_data.get('prenom'):
            prenom_label = tk.Label(
                info_frame,
                text=f"{self.user_data['prenom']}",
                font=("Arial", 14),
                bg=COULEUR_OR,
                fg="black"
            )
            prenom_label.pack(anchor="w")
        
        # Bouton déconnexion
        btn_logout = tk.Button(
            header_content,
            text="🚪 DÉCONNEXION",
            font=("Arial", 10, "bold"),
            bg=COULEUR_ROUGE,
            fg=COULEUR_BLANC,
            command=self.deconnexion
        )
        btn_logout.pack(side=tk.RIGHT, padx=20)
        
        # === TITRE PRINCIPAL ===
        titre = tk.Label(
            self.window,
            text="🏆 TABLEAU DE BORD 🏆",
            font=("Impact", 32, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        )
        titre.pack(pady=20)
        
        # === ZONE CENTRALE : STATISTIQUES ===
        stats_frame = tk.Frame(self.window, bg=COULEUR_FOND)
        stats_frame.pack(pady=20)
        
        # Classement
        self.create_stat_box(
            stats_frame,
            "📊 CLASSEMENT",
            "1er",
            0
        )
        
        # Forme du moment (5 dernières perfs)
        self.create_forme_box(stats_frame, 1)
        
        # Jokers disponibles
        self.create_stat_box(
            stats_frame,
            "🃏 MES JOKERS",
            "3 Doubles | 2 Volés",
            2
        )
        
        # === MENU DE NAVIGATION ===
        menu_frame = tk.Frame(self.window, bg=COULEUR_FOND)
        menu_frame.pack(pady=30)
        
        # Bouton : Faire mes pronos
        self.create_menu_button(
            menu_frame,
            "📝 FAIRE MES PRONOS",
            self.faire_pronos,
            0, 0
        )
        
        # Bouton : Voir le classement
        self.create_menu_button(
            menu_frame,
            "📊 CLASSEMENT",
            self.voir_classement,
            0, 1
        )
        
        # Bouton : Pronos des amis
        self.create_menu_button(
            menu_frame,
            "👥 PRONOS DES AMIS",
            self.voir_pronos_amis,
            1, 0
        )
        
        # Bouton : Mon profil
        self.create_menu_button(
            menu_frame,
            "⚙️ MON PROFIL",
            self.mon_profil,
            1, 1
        )
        
        # === FOOTER ===
        footer_frame = tk.Frame(self.window, bg=COULEUR_FOND)
        footer_frame.pack(side=tk.BOTTOM, pady=20)
        
        semaine_label = tk.Label(
            footer_frame,
            text="📅 Semaine 1 | Date limite : Vendredi 23:59",
            font=("Arial", 12),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND
        )
        semaine_label.pack()
        
        print("✅ Interface du dashboard créée")
    
    def create_forme_box(self, parent, column):
        """
        Crée la boîte de forme avec les 5 dernières performances.
        """
        box = tk.Frame(
            parent,
            bg=COULEUR_OR,
            width=250,
            height=120,
            relief="raised",
            borderwidth=3
        )
        box.grid(row=0, column=column, padx=15, pady=10)
        box.pack_propagate(False)
        
        titre_label = tk.Label(
            box,
            text="📈 FORME DU MOMENT",
            font=("Arial", 14, "bold"),
            bg=COULEUR_OR,
            fg="black"
        )
        titre_label.pack(pady=(15, 10))
        
        # Tendance des 5 dernières semaines
        tendance_frame = tk.Frame(box, bg=COULEUR_OR)
        tendance_frame.pack()
        
        # Exemple : ⬆️⬆️➡️⬇️⬆️
        tendances = ["⬆️", "⬆️", "➡️", "⬇️", "⬆️"]
        couleurs = ["#00FF00", "#00FF00", "#808080", "#FF0000", "#00FF00"]
        
        for symbole, couleur in zip(tendances, couleurs):
            tk.Label(
                tendance_frame,
                text=symbole,
                font=("Arial", 20),
                bg=COULEUR_OR,
                fg=couleur
            ).pack(side=tk.LEFT, padx=3)
    
    def create_stat_box(self, parent, titre, valeur, column):
        """
        Crée une boîte de statistique.
        """
        box = tk.Frame(
            parent,
            bg=COULEUR_OR,
            width=250,
            height=120,
            relief="raised",
            borderwidth=3
        )
        box.grid(row=0, column=column, padx=15, pady=10)
        box.pack_propagate(False)
        
        titre_label = tk.Label(
            box,
            text=titre,
            font=("Arial", 14, "bold"),
            bg=COULEUR_OR,
            fg="black"
        )
        titre_label.pack(pady=(15, 5))
        
        valeur_label = tk.Label(
            box,
            text=valeur,
            font=("Arial", 18, "bold"),
            bg=COULEUR_OR,
            fg="black"
        )
        valeur_label.pack(pady=5)
    
    def create_menu_button(self, parent, text, command, row, column):
        """
        Crée un bouton de menu.
        """
        btn = tk.Button(
            parent,
            text=text,
            font=("Arial", 14, "bold"),
            bg=COULEUR_BLANC,
            fg="black",
            width=25,
            height=3,
            command=command
        )
        btn.grid(row=row, column=column, padx=15, pady=10)
    
    def faire_pronos(self):
        """
        Ouvre l'interface de saisie des pronos.
        """
        print("📝 Ouverture de la saisie des pronos...")
        self.window.destroy()
        
        from modules.saisie_pronos import SaisiePronosWindow
        saisie = SaisiePronosWindow(self.user_data)
        saisie.run()
        
        # Retour au dashboard après validation
        from modules.dashboard import DashboardWindow
        dashboard = DashboardWindow(self.user_data)
        dashboard.run()
    
    def voir_classement(self):
        """
        Ouvre l'interface du classement.
        """
        print("📊 Ouverture du classement...")
        self.window.withdraw()
        
        from modules.classement import ClassementWindow
        classement = ClassementWindow(self.user_data)
        classement.run()
        
        self.window.deiconify()
    
    def voir_pronos_amis(self):
        """
        Ouvre l'interface des pronos des amis.
        """
        messagebox.showinfo("Info", "Module 'Pronos des amis' en cours de développement...")
    
    def mon_profil(self):
        """
        Ouvre l'interface du profil utilisateur.
        """
        messagebox.showinfo("Info", "Module 'Mon profil' en cours de développement...")
    
    def deconnexion(self):
        """
        Déconnecte l'utilisateur et retourne à l'écran de login.
        """
        reponse = messagebox.askyesno(
            "Déconnexion",
            "Es-tu sûr de vouloir te déconnecter ?"
        )
        
        if reponse:
            print(f"🚪 Déconnexion de {self.user_data['pseudo']}")
            self.window.destroy()
            
            # Relance la fenêtre de login
            from modules.login import LoginWindow
            login = LoginWindow()
            login.run()
    
    def run(self):
        """
        Lance la fenêtre (boucle principale).
        """
        print("🚀 Lancement du dashboard...")
        self.window.mainloop()

# ===================================
# TEST DU MODULE
# ===================================
if __name__ == "__main__":
    print("🧪 Test du module dashboard\n")
    
    # Données de test
    test_user = {
        'id': 1,
        'pseudo': 'TestUser',
        'prenom': 'Jean',
        'email': 'test@test.com',
        'avatar_path': None,
        'statut': 'actif'
    }
    
    # Crée et lance le dashboard
    app = DashboardWindow(test_user)
>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
    app.run()