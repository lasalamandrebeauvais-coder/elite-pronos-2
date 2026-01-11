<<<<<<< HEAD
# inscription.py - Module d'inscription des joueurs

import tkinter as tk
from tkinter import messagebox, Canvas, Scrollbar, Frame, filedialog
from PIL import Image, ImageTk
from modules.database_manager import DatabaseManager
import sqlite3
import os
import shutil
from modules.config import FENETRE_LARGEUR, FENETRE_HAUTEUR
from modules.config import COULEUR_FOND, COULEUR_OR, COULEUR_BLANC, AVATARS_DIR

class InscriptionWindow:
    """
    Classe pour gérer la fenêtre d'inscription.
    Crée une interface graphique style Dark Mode Premium avec défilement.
    """
    
    def __init__(self):
        """
        Initialise la fenêtre d'inscription.
        """
        # Crée la fenêtre principale
        self.window = tk.Tk()
        self.window.title("Elite Pronos 2 - Inscription")
        
        # Définit les dimensions
        self.window.geometry(f"{FENETRE_LARGEUR}x{FENETRE_HAUTEUR}")
        
        # Couleur de fond (bleu nuit)
        self.window.configure(bg=COULEUR_FOND)
        
        # Empêche le redimensionnement
        self.window.resizable(False, False)
        
        print("✅ Fenêtre d'inscription créée")
        
        # Variables pour l'avatar
        self.avatar_path = None
        self.avatar_image = None
        
        # Appelle la méthode pour créer l'interface
        self.create_interface()
    
    def create_interface(self):
        """
        Crée tous les éléments de l'interface avec défilement.
        """
        # Canvas avec scrollbar
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
        
        # TITRE PRINCIPAL
        titre = tk.Label(
            scrollable_frame,
            text="PRÊT À DÉTRÔNER TES POTES ?",
            font=("Impact", 32, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        )
        titre.pack(pady=20)
        
        # SOUS-TITRE
        sous_titre = tk.Label(
            scrollable_frame,
            text="ENTRE DANS L'ARÈNE",
            font=("Impact", 20),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND
        )
        sous_titre.pack(pady=10)
        
        # CONTENEUR PRINCIPAL
        main_frame = tk.Frame(scrollable_frame, bg=COULEUR_FOND)
        main_frame.pack(pady=20, padx=50)
        
        # COLONNE GAUCHE (Avatar)
        left_frame = tk.Frame(main_frame, bg=COULEUR_FOND, width=400)
        left_frame.pack(side=tk.LEFT, padx=20)
        
        # === ZONE AVATAR ===
        
        # Titre de la section
        avatar_titre = tk.Label(
            left_frame,
            text="TON AVATAR",
            font=("Impact", 18, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        )
        avatar_titre.pack(pady=(0, 20))
        
        # Cadre de prévisualisation avec bordure dorée
        self.avatar_frame = tk.Frame(
            left_frame,
            bg=COULEUR_OR,
            width=250,
            height=250
        )
        self.avatar_frame.pack(pady=10)
        self.avatar_frame.pack_propagate(False)
        
        # Label pour afficher l'image
        self.avatar_label = tk.Label(
            self.avatar_frame,
            text="Aucune image",
            font=("Arial", 12),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND,
            width=32,
            height=14
        )
        self.avatar_label.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Bouton : Télécharger une photo
        btn_upload = tk.Button(
            left_frame,
            text="📤 TÉLÉCHARGER UNE PHOTO",
            font=("Arial", 12, "bold"),
            bg=COULEUR_BLANC,
            fg="black",
            width=25,
            height=2,
            command=self.upload_avatar
        )
        btn_upload.pack(pady=10)
        
        # Bouton : Choisir un avatar prédéfini
        btn_avatar = tk.Button(
            left_frame,
            text="🎭 CHOISIR UN AVATAR",
            font=("Arial", 12, "bold"),
            bg=COULEUR_BLANC,
            fg="black",
            width=25,
            height=2,
            command=self.choisir_avatar
        )
        btn_avatar.pack(pady=10)
        
        # COLONNE DROITE (Formulaire)
        right_frame = tk.Frame(main_frame, bg=COULEUR_FOND, width=400)
        right_frame.pack(side=tk.LEFT, padx=20)
        
        # Champ PRÉNOM (OBLIGATOIRE)
        self.create_field(right_frame, "Prénom * :", 0)
        self.entry_prenom = tk.Entry(right_frame, font=("Arial", 14), bg=COULEUR_BLANC, fg="black", width=30)
        self.entry_prenom.grid(row=1, column=0, pady=5, padx=10, sticky="w")
        
        # Champ PSEUDO (OBLIGATOIRE)
        self.create_field(right_frame, "Pseudo * :", 2)
        self.entry_pseudo = tk.Entry(right_frame, font=("Arial", 14), bg=COULEUR_BLANC, fg="black", width=30)
        self.entry_pseudo.grid(row=3, column=0, pady=5, padx=10, sticky="w")
        
        # Champ EMAIL (OBLIGATOIRE)
        self.create_field(right_frame, "Email * :", 4)
        self.entry_email = tk.Entry(right_frame, font=("Arial", 14), bg=COULEUR_BLANC, fg="black", width=30)
        self.entry_email.grid(row=5, column=0, pady=5, padx=10, sticky="w")
        
        # Champ TÉLÉPHONE (OBLIGATOIRE)
        self.create_field(right_frame, "Téléphone * :", 6)
        self.entry_telephone = tk.Entry(right_frame, font=("Arial", 14), bg=COULEUR_BLANC, fg="black", width=30)
        self.entry_telephone.grid(row=7, column=0, pady=5, padx=10, sticky="w")
        
        # Champ CODE PIN (OBLIGATOIRE)
        self.create_field(right_frame, "Code PIN * :", 8)
        self.entry_pin = tk.Entry(right_frame, font=("Arial", 14), bg=COULEUR_BLANC, fg="black", width=30, show="*")
        self.entry_pin.grid(row=9, column=0, pady=5, padx=10, sticky="w")
        
        # BOUTON DE VALIDATION
        btn_valider = tk.Button(
            right_frame,
            text="VALIDER L'INSCRIPTION",
            font=("Impact", 16, "bold"),
            bg=COULEUR_OR,
            fg="black",
            width=25,
            height=2,
            command=self.valider_inscription
        )
        btn_valider.grid(row=10, column=0, pady=30, padx=10)
        
        # Activation du scroll avec la molette de la souris
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        print("✅ Interface avec défilement créée")
    
    def create_field(self, parent, text, row):
        """
        Crée un label pour un champ de saisie.
        """
        label = tk.Label(
            parent,
            text=text,
            font=("Arial", 12, "bold"),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND
        )
        label.grid(row=row, column=0, pady=(15, 5), padx=10, sticky="w")
    
    def upload_avatar(self):
        """
        Ouvre une fenêtre pour sélectionner une image depuis l'ordinateur.
        """
        # Ouvre la fenêtre de sélection de fichier
        file_path = filedialog.askopenfilename(
            title="Choisir une photo",
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Tous les fichiers", "*.*")
            ]
        )
        
        # Si l'utilisateur a sélectionné un fichier
        if file_path:
            try:
                # Charge l'image
                image = Image.open(file_path)
                
                # Redimensionne l'image à 240x240 (pour tenir dans le cadre)
                image = image.resize((240, 240), Image.Resampling.LANCZOS)
                
                # Convertit l'image pour Tkinter
                self.avatar_image = ImageTk.PhotoImage(image)
                
                # Affiche l'image dans le label
                self.avatar_label.configure(image=self.avatar_image, text="")
                
                # Sauvegarde le chemin de l'image
                self.avatar_path = file_path
                
                print(f"✅ Avatar chargé : {file_path}")
                
            except Exception as e:
                messagebox.showerror(
                    "Erreur",
                    f"Impossible de charger l'image :\n{str(e)}"
                )
                print(f"❌ Erreur chargement image : {e}")
    
    def choisir_avatar(self):
        """
        Permet de choisir un avatar prédéfini.
        """
        messagebox.showinfo("Info", "Fonction de choix d'avatar en cours de développement...")
    
    def valider_inscription(self):
        """
        Valide et enregistre l'inscription dans la base de données.
        """
        # Récupération des données
        pseudo = self.entry_pseudo.get().strip()
        prenom = self.entry_prenom.get().strip()
        email = self.entry_email.get().strip()
        telephone = self.entry_telephone.get().strip()
        pin = self.entry_pin.get().strip()
        
        # === VALIDATIONS ===
        
        # 1. Vérification que TOUS les champs sont remplis
        if not prenom:
            messagebox.showerror("Erreur", "Le Prénom est obligatoire !")
            return
        
        if not pseudo:
            messagebox.showerror("Erreur", "Le Pseudo est obligatoire !")
            return
        
        if not email:
            messagebox.showerror("Erreur", "L'Email est obligatoire !")
            return
        
        if not telephone:
            messagebox.showerror("Erreur", "Le Téléphone est obligatoire !")
            return
        
        if not pin:
            messagebox.showerror("Erreur", "Le Code PIN est obligatoire !")
            return
        
        # 2. Validation de la longueur du pseudo
        if len(pseudo) < 3:
            messagebox.showerror("Erreur", "Le Pseudo doit contenir au moins 3 caractères !")
            return
        
        # 3. Validation du PIN (4 caractères minimum)
        if len(pin) < 4:
            messagebox.showerror("Erreur", "Le PIN doit contenir au moins 4 caractères !")
            return
        
        # 4. Validation basique de l'email (contient @ et .)
        if "@" not in email or "." not in email:
            messagebox.showerror("Erreur", "L'Email n'est pas valide !")
            return
        
        # === GESTION DE L'AVATAR (AVANT LA BASE DE DONNÉES) ===
        avatar_final_path = None
        
        if self.avatar_path:
            # Crée le nom du fichier : pseudo + extension
            extension = os.path.splitext(self.avatar_path)[1]
            avatar_filename = f"{pseudo}{extension}"
            
            # Chemin de destination
            destination = os.path.join(AVATARS_DIR, avatar_filename)
            
            # Copie l'image vers le dossier avatars
            try:
                shutil.copy2(self.avatar_path, destination)
                avatar_final_path = f"assets/avatars/{avatar_filename}"
                print(f"✅ Avatar copié vers : {destination}")
            except Exception as e:
                print(f"⚠️ Erreur copie avatar : {e}")
        
        # === ENREGISTREMENT DANS LA BASE ===
        
        db = DatabaseManager()
        conn = None
        
        try:
            # Connexion à la base de données
            conn = db.create_connection()
            
            if conn is None:
                messagebox.showerror("Erreur", "Impossible de se connecter à la base de données !")
                return
            
            cursor = conn.cursor()
            
            # Insertion des données avec avatar
            cursor.execute("""
                INSERT INTO utilisateurs (pseudo, prenom, email, telephone, pin, avatar_path, statut)
                VALUES (?, ?, ?, ?, ?, ?, 'en_attente')
            """, (pseudo, prenom, email, telephone, pin, avatar_final_path))
            
            # Sauvegarde
            conn.commit()
            
            # Message de succès
            messagebox.showinfo(
                "INSCRIPTION RÉUSSIE",
                f"Bienvenue dans l'arène {pseudo} !\n\n"
                f"Ton compte est en attente de validation.\n"
                f"Tu seras notifié dès qu'un admin t'aura activé."
            )
            
            print(f"✅ Inscription enregistrée : {pseudo}")
            
            # Réinitialise les champs
            self.entry_pseudo.delete(0, tk.END)
            self.entry_prenom.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
            self.entry_telephone.delete(0, tk.END)
            self.entry_pin.delete(0, tk.END)
            
            # Réinitialise l'avatar
            self.avatar_path = None
            self.avatar_image = None
            self.avatar_label.configure(image="", text="Aucune image")
            
        except sqlite3.IntegrityError:
            # Le pseudo existe déjà (contrainte UNIQUE)
            messagebox.showerror(
                "Erreur",
                f"Le pseudo '{pseudo}' est déjà pris !\n"
                f"Choisis-en un autre."
            )
            print(f"❌ Pseudo déjà existant : {pseudo}")
            
        except Exception as e:
            # Autre erreur
            messagebox.showerror(
                "Erreur",
                f"Une erreur s'est produite :\n{str(e)}"
            )
            print(f"❌ Erreur lors de l'inscription : {e}")
            
        finally:
            # Ferme TOUJOURS la connexion, même en cas d'erreur
            if conn:
                conn.close()
                print("🔒 Connexion fermée")
    
    def run(self):
        """
        Lance la fenêtre (boucle principale).
        """
        print("🚀 Lancement de la fenêtre...")
        self.window.mainloop()

# ===================================
# TEST DU MODULE
# ===================================
if __name__ == "__main__":
    print("🧪 Test du module d'inscription\n")
    
    # Crée et lance la fenêtre
    app = InscriptionWindow()
=======
# inscription.py - Module d'inscription des joueurs

import tkinter as tk
from tkinter import messagebox, Canvas, Scrollbar, Frame, filedialog
from PIL import Image, ImageTk
from modules.database_manager import DatabaseManager
import sqlite3
import os
import shutil
from modules.config import FENETRE_LARGEUR, FENETRE_HAUTEUR
from modules.config import COULEUR_FOND, COULEUR_OR, COULEUR_BLANC, AVATARS_DIR

class InscriptionWindow:
    """
    Classe pour gérer la fenêtre d'inscription.
    Crée une interface graphique style Dark Mode Premium avec défilement.
    """
    
    def __init__(self):
        """
        Initialise la fenêtre d'inscription.
        """
        # Crée la fenêtre principale
        self.window = tk.Tk()
        self.window.title("Elite Pronos 2 - Inscription")
        
        # Définit les dimensions
        self.window.geometry(f"{FENETRE_LARGEUR}x{FENETRE_HAUTEUR}")
        
        # Couleur de fond (bleu nuit)
        self.window.configure(bg=COULEUR_FOND)
        
        # Empêche le redimensionnement
        self.window.resizable(False, False)
        
        print("✅ Fenêtre d'inscription créée")
        
        # Variables pour l'avatar
        self.avatar_path = None
        self.avatar_image = None
        
        # Appelle la méthode pour créer l'interface
        self.create_interface()
    
    def create_interface(self):
        """
        Crée tous les éléments de l'interface avec défilement.
        """
        # Canvas avec scrollbar
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
        
        # TITRE PRINCIPAL
        titre = tk.Label(
            scrollable_frame,
            text="PRÊT À DÉTRÔNER TES POTES ?",
            font=("Impact", 32, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        )
        titre.pack(pady=20)
        
        # SOUS-TITRE
        sous_titre = tk.Label(
            scrollable_frame,
            text="ENTRE DANS L'ARÈNE",
            font=("Impact", 20),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND
        )
        sous_titre.pack(pady=10)
        
        # CONTENEUR PRINCIPAL
        main_frame = tk.Frame(scrollable_frame, bg=COULEUR_FOND)
        main_frame.pack(pady=20, padx=50)
        
        # COLONNE GAUCHE (Avatar)
        left_frame = tk.Frame(main_frame, bg=COULEUR_FOND, width=400)
        left_frame.pack(side=tk.LEFT, padx=20)
        
        # === ZONE AVATAR ===
        
        # Titre de la section
        avatar_titre = tk.Label(
            left_frame,
            text="TON AVATAR",
            font=("Impact", 18, "bold"),
            fg=COULEUR_OR,
            bg=COULEUR_FOND
        )
        avatar_titre.pack(pady=(0, 20))
        
        # Cadre de prévisualisation avec bordure dorée
        self.avatar_frame = tk.Frame(
            left_frame,
            bg=COULEUR_OR,
            width=250,
            height=250
        )
        self.avatar_frame.pack(pady=10)
        self.avatar_frame.pack_propagate(False)
        
        # Label pour afficher l'image
        self.avatar_label = tk.Label(
            self.avatar_frame,
            text="Aucune image",
            font=("Arial", 12),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND,
            width=32,
            height=14
        )
        self.avatar_label.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Bouton : Télécharger une photo
        btn_upload = tk.Button(
            left_frame,
            text="📤 TÉLÉCHARGER UNE PHOTO",
            font=("Arial", 12, "bold"),
            bg=COULEUR_BLANC,
            fg="black",
            width=25,
            height=2,
            command=self.upload_avatar
        )
        btn_upload.pack(pady=10)
        
        # Bouton : Choisir un avatar prédéfini
        btn_avatar = tk.Button(
            left_frame,
            text="🎭 CHOISIR UN AVATAR",
            font=("Arial", 12, "bold"),
            bg=COULEUR_BLANC,
            fg="black",
            width=25,
            height=2,
            command=self.choisir_avatar
        )
        btn_avatar.pack(pady=10)
        
        # COLONNE DROITE (Formulaire)
        right_frame = tk.Frame(main_frame, bg=COULEUR_FOND, width=400)
        right_frame.pack(side=tk.LEFT, padx=20)
        
        # Champ PRÉNOM (OBLIGATOIRE)
        self.create_field(right_frame, "Prénom * :", 0)
        self.entry_prenom = tk.Entry(right_frame, font=("Arial", 14), bg=COULEUR_BLANC, fg="black", width=30)
        self.entry_prenom.grid(row=1, column=0, pady=5, padx=10, sticky="w")
        
        # Champ PSEUDO (OBLIGATOIRE)
        self.create_field(right_frame, "Pseudo * :", 2)
        self.entry_pseudo = tk.Entry(right_frame, font=("Arial", 14), bg=COULEUR_BLANC, fg="black", width=30)
        self.entry_pseudo.grid(row=3, column=0, pady=5, padx=10, sticky="w")
        
        # Champ EMAIL (OBLIGATOIRE)
        self.create_field(right_frame, "Email * :", 4)
        self.entry_email = tk.Entry(right_frame, font=("Arial", 14), bg=COULEUR_BLANC, fg="black", width=30)
        self.entry_email.grid(row=5, column=0, pady=5, padx=10, sticky="w")
        
        # Champ TÉLÉPHONE (OBLIGATOIRE)
        self.create_field(right_frame, "Téléphone * :", 6)
        self.entry_telephone = tk.Entry(right_frame, font=("Arial", 14), bg=COULEUR_BLANC, fg="black", width=30)
        self.entry_telephone.grid(row=7, column=0, pady=5, padx=10, sticky="w")
        
        # Champ CODE PIN (OBLIGATOIRE)
        self.create_field(right_frame, "Code PIN * :", 8)
        self.entry_pin = tk.Entry(right_frame, font=("Arial", 14), bg=COULEUR_BLANC, fg="black", width=30, show="*")
        self.entry_pin.grid(row=9, column=0, pady=5, padx=10, sticky="w")
        
        # BOUTON DE VALIDATION
        btn_valider = tk.Button(
            right_frame,
            text="VALIDER L'INSCRIPTION",
            font=("Impact", 16, "bold"),
            bg=COULEUR_OR,
            fg="black",
            width=25,
            height=2,
            command=self.valider_inscription
        )
        btn_valider.grid(row=10, column=0, pady=30, padx=10)
        
        # Activation du scroll avec la molette de la souris
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        print("✅ Interface avec défilement créée")
    
    def create_field(self, parent, text, row):
        """
        Crée un label pour un champ de saisie.
        """
        label = tk.Label(
            parent,
            text=text,
            font=("Arial", 12, "bold"),
            fg=COULEUR_BLANC,
            bg=COULEUR_FOND
        )
        label.grid(row=row, column=0, pady=(15, 5), padx=10, sticky="w")
    
    def upload_avatar(self):
        """
        Ouvre une fenêtre pour sélectionner une image depuis l'ordinateur.
        """
        # Ouvre la fenêtre de sélection de fichier
        file_path = filedialog.askopenfilename(
            title="Choisir une photo",
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Tous les fichiers", "*.*")
            ]
        )
        
        # Si l'utilisateur a sélectionné un fichier
        if file_path:
            try:
                # Charge l'image
                image = Image.open(file_path)
                
                # Redimensionne l'image à 240x240 (pour tenir dans le cadre)
                image = image.resize((240, 240), Image.Resampling.LANCZOS)
                
                # Convertit l'image pour Tkinter
                self.avatar_image = ImageTk.PhotoImage(image)
                
                # Affiche l'image dans le label
                self.avatar_label.configure(image=self.avatar_image, text="")
                
                # Sauvegarde le chemin de l'image
                self.avatar_path = file_path
                
                print(f"✅ Avatar chargé : {file_path}")
                
            except Exception as e:
                messagebox.showerror(
                    "Erreur",
                    f"Impossible de charger l'image :\n{str(e)}"
                )
                print(f"❌ Erreur chargement image : {e}")
    
    def choisir_avatar(self):
        """
        Permet de choisir un avatar prédéfini.
        """
        messagebox.showinfo("Info", "Fonction de choix d'avatar en cours de développement...")
    
    def valider_inscription(self):
        """
        Valide et enregistre l'inscription dans la base de données.
        """
        # Récupération des données
        pseudo = self.entry_pseudo.get().strip()
        prenom = self.entry_prenom.get().strip()
        email = self.entry_email.get().strip()
        telephone = self.entry_telephone.get().strip()
        pin = self.entry_pin.get().strip()
        
        # === VALIDATIONS ===
        
        # 1. Vérification que TOUS les champs sont remplis
        if not prenom:
            messagebox.showerror("Erreur", "Le Prénom est obligatoire !")
            return
        
        if not pseudo:
            messagebox.showerror("Erreur", "Le Pseudo est obligatoire !")
            return
        
        if not email:
            messagebox.showerror("Erreur", "L'Email est obligatoire !")
            return
        
        if not telephone:
            messagebox.showerror("Erreur", "Le Téléphone est obligatoire !")
            return
        
        if not pin:
            messagebox.showerror("Erreur", "Le Code PIN est obligatoire !")
            return
        
        # 2. Validation de la longueur du pseudo
        if len(pseudo) < 3:
            messagebox.showerror("Erreur", "Le Pseudo doit contenir au moins 3 caractères !")
            return
        
        # 3. Validation du PIN (4 caractères minimum)
        if len(pin) < 4:
            messagebox.showerror("Erreur", "Le PIN doit contenir au moins 4 caractères !")
            return
        
        # 4. Validation basique de l'email (contient @ et .)
        if "@" not in email or "." not in email:
            messagebox.showerror("Erreur", "L'Email n'est pas valide !")
            return
        
        # === GESTION DE L'AVATAR (AVANT LA BASE DE DONNÉES) ===
        avatar_final_path = None
        
        if self.avatar_path:
            # Crée le nom du fichier : pseudo + extension
            extension = os.path.splitext(self.avatar_path)[1]
            avatar_filename = f"{pseudo}{extension}"
            
            # Chemin de destination
            destination = os.path.join(AVATARS_DIR, avatar_filename)
            
            # Copie l'image vers le dossier avatars
            try:
                shutil.copy2(self.avatar_path, destination)
                avatar_final_path = f"assets/avatars/{avatar_filename}"
                print(f"✅ Avatar copié vers : {destination}")
            except Exception as e:
                print(f"⚠️ Erreur copie avatar : {e}")
        
        # === ENREGISTREMENT DANS LA BASE ===
        
        db = DatabaseManager()
        conn = None
        
        try:
            # Connexion à la base de données
            conn = db.create_connection()
            
            if conn is None:
                messagebox.showerror("Erreur", "Impossible de se connecter à la base de données !")
                return
            
            cursor = conn.cursor()
            
            # Insertion des données avec avatar
            cursor.execute("""
                INSERT INTO utilisateurs (pseudo, prenom, email, telephone, pin, avatar_path, statut)
                VALUES (?, ?, ?, ?, ?, ?, 'en_attente')
            """, (pseudo, prenom, email, telephone, pin, avatar_final_path))
            
            # Sauvegarde
            conn.commit()
            
            # Message de succès
            messagebox.showinfo(
                "INSCRIPTION RÉUSSIE",
                f"Bienvenue dans l'arène {pseudo} !\n\n"
                f"Ton compte est en attente de validation.\n"
                f"Tu seras notifié dès qu'un admin t'aura activé."
            )
            
            print(f"✅ Inscription enregistrée : {pseudo}")
            
            # Réinitialise les champs
            self.entry_pseudo.delete(0, tk.END)
            self.entry_prenom.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
            self.entry_telephone.delete(0, tk.END)
            self.entry_pin.delete(0, tk.END)
            
            # Réinitialise l'avatar
            self.avatar_path = None
            self.avatar_image = None
            self.avatar_label.configure(image="", text="Aucune image")
            
        except sqlite3.IntegrityError:
            # Le pseudo existe déjà (contrainte UNIQUE)
            messagebox.showerror(
                "Erreur",
                f"Le pseudo '{pseudo}' est déjà pris !\n"
                f"Choisis-en un autre."
            )
            print(f"❌ Pseudo déjà existant : {pseudo}")
            
        except Exception as e:
            # Autre erreur
            messagebox.showerror(
                "Erreur",
                f"Une erreur s'est produite :\n{str(e)}"
            )
            print(f"❌ Erreur lors de l'inscription : {e}")
            
        finally:
            # Ferme TOUJOURS la connexion, même en cas d'erreur
            if conn:
                conn.close()
                print("🔒 Connexion fermée")
    
    def run(self):
        """
        Lance la fenêtre (boucle principale).
        """
        print("🚀 Lancement de la fenêtre...")
        self.window.mainloop()

# ===================================
# TEST DU MODULE
# ===================================
if __name__ == "__main__":
    print("🧪 Test du module d'inscription\n")
    
    # Crée et lance la fenêtre
    app = InscriptionWindow()
>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
    app.run()