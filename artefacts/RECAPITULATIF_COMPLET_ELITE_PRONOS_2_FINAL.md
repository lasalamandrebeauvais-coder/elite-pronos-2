# 🏆 RÉCAPITULATIF COMPLET : ELITE PRONOS 2 - VERSION FINALE

**Date de création initiale :** 8 Janvier 2026  
**Dernière mise à jour :** 10 Janvier 2026 (Système de jokers complet)  
**Statut :** Plateforme de pronostics sportifs avec système de jokers opérationnel

---

## 📁 STRUCTURE DU PROJET

```
elite_pronos_2/
├── database/
│   └── pronos_expert.db          # Base de données SQLite
├── modules/
│   ├── __pycache__/              # Fichiers Python compilés
│   ├── config.py                 # Configuration globale
│   ├── database_manager.py       # Gestion de la DB
│   ├── inscription.py            # Module d'inscription
│   ├── login.py                  # Module de connexion
│   ├── dashboard.py              # Interface principale
│   ├── saisie_pronos.py          # Saisie des pronos + Jokers ✨
│   ├── sourcing_bot.py           # Bot de récupération matchs + résultats
│   ├── calcul_gains.py           # Calcul des gains + Jokers ✨
│   ├── radar_recrutement.py      # Interface de sélection de cible ✨ NOUVEAU
│   ├── gestion_jokers.py         # Logique de chaîne de vol ✨ NOUVEAU
│   └── cloture_pronos.py         # Script de clôture automatique ✨ NOUVEAU
├── assets/
│   └── avatars/                  # Dossier des photos de profil
│       └── predefinis/           # Avatars par défaut
├── docs/                         # Documentation
├── main.py                       # Point d'entrée principal
├── activer_compte.py             # Script : activer un compte
├── test_calcul.py                # Script : tester le calcul
├── test_ecran.py                 # Script : tester résolution écran
├── verif_table_jokers.py         # Script : vérifier table jokers ✨
├── verif_stock_jokers.py         # Script : vérifier stock jokers ✨
├── initialiser_stock_jokers.py   # Script : initialiser le stock ✨ (dans modules/)
├── voir_utilisateurs.py          # Script : lister les users
├── voir_matchs.py                # Script : lister les matchs
└── voir_pronos_alex.py           # Script : voir pronos d'un joueur
```

---

## 🗄️ BASE DE DONNÉES (SQLite)

**Fichier :** `database/pronos_expert.db`

### Table 1 : utilisateurs
Stocke les profils des joueurs
- `id` (PK, AUTO)
- `pseudo` (UNIQUE, NOT NULL)
- `prenom`, `nom`, `email`, `telephone`
- `pin` (NOT NULL, code secret)
- `avatar_path` (chemin de l'image)
- `statut` (en_attente / actif)
- `date_inscription`

### Table 2 : matchs
Stocke les 4 matchs de la semaine
- `id`, `semaine`
- `equipe_domicile`, `equipe_exterieur`
- `cote_domicile`, `cote_nul`, `cote_exterieur`
- `score_domicile`, `score_exterieur` (mis à jour auto)
- `date_match`, `statut` (en_attente / termine)

### Table 3 : pronostics
Stocke les pronos des joueurs
- `id`, `utilisateur_id` (FK), `match_id` (FK)
- `score_domicile_prono`, `score_exterieur_prono`
- `mise` (10-60 points)
- `points_gagnes` (calculé auto)
- `date_prono`

### Table 4 : historique
Suivi des performances hebdomadaires (rempli auto)
- `id`, `utilisateur_id` (FK), `semaine`
- `points_totaux`, `scores_exacts`, `bons_pronos`
- `grand_chelem` (0/1)
- `joker_utilise`, `date_calcul`

### Table 5 : jokers ✨
Historique d'utilisation des jokers
- `id`, `utilisateur_id` (FK)
- `type_joker` (points_doubles / points_voles)
- `utilise` (0/1)
- `semaine_utilisation`, `cible_vol_id`, `date_utilisation`

### Table 6 : stock_jokers ✨ NOUVEAU
Stock disponible pour chaque joueur
- `id`, `utilisateur_id` (FK, UNIQUE)
- `jokers_doubles_disponibles` (défaut: 3)
- `jokers_voles_disponibles` (défaut: 2)
- `derniere_mise_a_jour`

---

## ⚙️ MODULES DÉVELOPPÉS

### 1. Configuration (config.py)
- Centralise tous les paramètres
- Dimensions : 950x680
- Budget : 100 pts (140 après Grand Chelem)
- Mises : min 10, max 60
- Couleurs : Dark Mode (bleu nuit + doré)

### 2. Gestionnaire DB (database_manager.py)
- Classe `DatabaseManager`
- Méthodes : `create_connection()`, `create_tables()`
- Gestion propre des connexions
- 6 tables créées automatiquement

### 3. Inscription (inscription.py)
- Interface scrollable 950x680
- 2 colonnes : Avatar (gauche) + Formulaire (droite)
- Upload photo + redimensionnement 240x240
- 5 champs obligatoires
- Validations complètes
- Enregistrement avec statut "en_attente"

### 4. Connexion (login.py)
- Interface centrée 600x650
- Champs : Pseudo + PIN
- Vérification DB + gestion statuts
- Ouverture automatique du dashboard si actif
- Hauteur ajustée pour visibilité complète

### 5. Dashboard (dashboard.py)
- En-tête doré : Avatar + Pseudo + Déconnexion
- 3 boîtes stats : Classement, Forme (5 flèches), Jokers ✨
- 4 boutons menu : Pronos, Classement, Amis, Profil
- Footer : Semaine + Date limite

### 6. Bot de Sourcing (sourcing_bot.py)
**Fonctionnalités :**
- API Football-Data.org : `bf58da6a49824f2a8742957b89ca52ee`
- 4 étapes : Récupération SCHEDULED → Roue secours → Sélection priorité L1 → Enregistrement
- Cotes réalistes générées
- 5 ligues : L1, Premier League, La Liga, Bundesliga, Serie A
- `update_results(semaine)` : Récupère les résultats automatiquement
- `launch_calculation()` : Lance le calcul quand 4 matchs terminés
- Mise à jour auto du statut des matchs

### 7. Saisie Pronos (saisie_pronos.py) ✨ ENRICHI
**Fonctionnalités originales :**
- Chargement dynamique depuis DB
- 4 cartes matchs : Écussons + Équipes + Cotes + VS
- Saisie : Score prédit + Slider mise (10-60)
- Validation : Total = Budget exact
- Vérification anti-doublon

**Nouvelles fonctionnalités (jokers) :**
- Section d'activation des jokers en haut
- 2 cases à cocher exclusives (1 seul joker par semaine)
- Affichage du stock disponible
- Intégration du Radar de Recrutement
- Enregistrement du joker + décrémentation du stock

### 8. Calcul des Gains (calcul_gains.py) ✨ ENRICHI
**Fonctionnalités originales :**
- Classe `CalculGains(semaine)`
- Compare pronos vs résultats réels
- Calcul des points :
  - Score exact : +10 points fixes
  - Bon résultat : mise × cote
  - Mauvais résultat : 0 point
- Détection Grand Chelem (4/4 exacts) : +40 points
- Mise à jour automatique des tables

**Nouvelles fonctionnalités (jokers) :**
- Détection du joker Points Doubles
- Application du multiplicateur ×2 APRÈS le bonus Grand Chelem
- Le multiplicateur ne se transfère jamais lors d'un vol

### 9. Radar de Recrutement (radar_recrutement.py) ✨ NOUVEAU
**Fonctionnalités :**
- Fenêtre popup modale 800x600
- Tableau scrollable des joueurs éligibles
- Filtrage automatique : uniquement joueurs à 100 points (pas 140)
- Affichage des stats : Points totaux, Bons pronos
- Sélection de la cible avec confirmation
- Détection du Grand Chelem de la dernière semaine

### 10. Gestion des Jokers (gestion_jokers.py) ✨ NOUVEAU
**Fonctionnalités :**
- `trouver_source_pronos(conn, user_id, semaine)` : Remonte la chaîne de vol
- `copier_pronos(conn, source_id, dest_id, semaine)` : Copie les pronos
- Protection contre les boucles infinies
- Gestion récursive de la chaîne (A vole B qui vole C → A récupère C)

### 11. Clôture des Pronos (cloture_pronos.py) ✨ NOUVEAU
**Fonctionnalités :**
- Script exécutable manuellement : `python modules/cloture_pronos.py 1`
- Détection des oublis (aucun prono validé)
- Activation automatique du joker "Points Volés" sur le dernier du classement
- Copie de tous les pronos volés avec gestion de la chaîne
- Verrouillage de la semaine

---

## 🎯 RÈGLES DU JEU IMPLÉMENTÉES

### Règles de base
✅ Budget : 100 pts (140 après Grand Chelem)  
✅ 4 matchs par semaine  
✅ Mise : 10-60 pts par match  
✅ Total mises = budget exact  
✅ Bonus score exact : +10 points  
✅ Grand Chelem : 4/4 exacts → +40 pts  
✅ Cotes figées au sourcing  
✅ Priorité Ligue 1  
✅ Calcul automatique des gains  
✅ Mise à jour automatique des résultats

### Règles des Jokers ✨ NOUVEAU
✅ **Stock initial :** 3 jokers doubles + 2 jokers volés par joueur  
✅ **Activation :** Pendant la saisie des pronos (1 seul par semaine)  
✅ **Clôture des pronos :** 20h le jour du 1er match L1  

**Joker "Points Doubles" (👑×2) :**
- Gains totaux × 2 (après Grand Chelem)
- Multiplicateur strictement personnel (non transférable)

**Joker "Points Volés" (✋) :**
- Copie les pronos d'un autre joueur
- Cible uniquement les joueurs à 100 points (pas 140)
- Radar de Recrutement pour choisir la cible
- Chaîne automatique (A vole B qui vole C → A récupère C)
- Le voleur ne récupère JAMAIS le multiplicateur ×2

**Joker "Oubli" (🆘) :**
- Activation automatique si aucun prono validé avant 20h
- Cible : dernier du classement général
- Utilise un joker volé du stock

---

## ✅ FLUX UTILISATEUR COMPLET

1. **Inscription** → Formulaire + Avatar → Statut "en_attente"
2. **Activation** (admin) → `activer_compte.py` → Statut "actif"
3. **Connexion** → Pseudo + PIN → Dashboard (affiche stock de jokers)
4. **Sourcing** (admin/auto) → `bot.run(semaine=1)` → 4 matchs en DB
5. **Pronos** → Saisie scores + mises + **Activation joker optionnelle** ✨ → Validation → DB
6. **Clôture** (20h jour J) → `cloture_pronos.py` → Copie des pronos volés + Oublis ✨
7. **Attente des résultats** → Les matchs se jouent
8. **Mise à jour auto** → `bot.update_results(semaine=1)` → Récupère scores depuis API
9. **Calcul auto** → Compare résultats → Calcule gains **avec jokers** ✨ → Historique
10. **Classement** (à développer) → Leaderboard

---

## 🚀 COMMANDES PRINCIPALES

### Lancer l'application
```bash
python main.py
```

### Gestion des utilisateurs
```bash
python voir_utilisateurs.py
python activer_compte.py
```

### Sourcing des matchs (début de semaine)
```python
from modules.sourcing_bot import SourcingBot
bot = SourcingBot()
bot.run(semaine=2)
```

### Clôture des pronos (20h jour J) ✨ NOUVEAU
```bash
python modules/cloture_pronos.py 1
```

### Mise à jour des résultats et calcul (fin de semaine)
```python
from modules.sourcing_bot import SourcingBot
bot = SourcingBot()
bot.update_results(semaine=2)
# Le calcul se lance automatiquement si 4 matchs terminés
```

### Tests et vérifications
```bash
python test_calcul.py
python verif_table_jokers.py
python verif_stock_jokers.py
```

### Initialisation du stock de jokers ✨ NOUVEAU
```bash
python modules/initialiser_stock_jokers.py
```

---

## 📦 DÉPENDANCES

```bash
python -m pip install pillow requests
```

---

## 🎯 CE QUI EST TERMINÉ

### ✅ Phase 1 : Plateforme de base (8 janvier 2026)
- Inscription complète
- Connexion sécurisée
- Dashboard fonctionnel
- Saisie des pronos
- Sourcing automatique
- Calcul des gains

### ✅ Phase 2 : Système de Jokers (10 janvier 2026)
- Table `stock_jokers` créée
- Stock initialisé (3 doubles + 2 volés)
- Interface de sélection dans saisie_pronos
- Radar de Recrutement opérationnel
- Logique de chaîne de vol
- Script de clôture automatique
- Intégration dans le calcul des gains
- Tests complets validés ✅

---

## 🔜 CE QUI RESTE À DÉVELOPPER

### Priorité 1 : Module Classement
- Leaderboard général
- Classement précision
- Historique 5 semaines
- Affichage du stock de jokers

### Priorité 2 : Interface Admin
- Valider inscriptions
- Gérer semaines
- Lancer sourcing/calculs/clôture via interface
- Dashboard admin complet
- Gestion manuelle des jokers

### Priorité 3 : Écran "Gala"
- Annonce vainqueur
- Annonce Grand Chelems
- Animations festives
- Tableau d'honneur

### Priorité 4 : Automatisation
- Script cron pour clôture à 20h
- Sourcing automatique de la semaine suivante
- Notifications par email

### Priorité 5 : Améliorations
- Module "Pronos des Amis"
- Module "Mon Profil" (édition)
- Statistiques détaillées
- Export des résultats

---

## 💡 POINTS TECHNIQUES IMPORTANTS

- **Résolution écran :** 1280x720 avec scroll
- **Connexions DB :** Toujours `finally` pour fermer
- **Lancement :** Depuis `main.py` uniquement
- **API Football-Data :** Ne fournit PAS les cotes (générées)
- **localStorage :** JAMAIS (pas supporté)
- **Calcul gains :** Automatique via bot.update_results()
- **Clôture pronos :** 20h le jour du 1er match L1 ✨
- **Jokers :** Stock géré automatiquement, multiplicateur non transférable ✨
- **Chaîne de vol :** Récursive avec protection contre boucles infinies ✨

---

## 📊 COMPTES DE TEST

**Compte 1 :**
- **Pseudo :** alex123
- **PIN :** 1234
- **Statut :** actif
- **Stock jokers :** 3 doubles | 2 volés

**Compte 2 :**
- **Pseudo :** alex345
- **PIN :** 5483
- **Statut :** actif
- **Stock jokers :** 3 doubles | 2 volés

---

## 🐛 BUGS RÉSOLUS

### Session 8 janvier 2026 (Calcul gains)
- Erreur d'import `CalculateurGains`
- Méthode `calculer_semaine()` introuvable
- Format de données incorrect
- IDs de matchs incorrects
- Erreurs d'indentation

### Session 10 janvier 2026 (Système de jokers)
- Problème fenêtre login (bouton caché) → Hauteur ajustée à 650px
- Joueurs inactifs dans le Radar → Activation manuelle
- Détection Grand Chelem incorrecte → Requête SQL modifiée (MAX → LIMIT 1)
- Database locked → Passage de la connexion en paramètre
- Doublons de jokers → Nettoyage et vérifications

---

## 🎊 STATISTIQUES PROJET

**Session initiale (8 janvier 2026) :**
- Fichiers créés : 12
- Lignes de code : ~2500
- Tables DB : 5
- Modules fonctionnels : 7

**Session calcul gains (8 janvier 2026) :**
- Nouveaux modules : 2
- Scripts de test : 5
- Bugs résolus : 5
- Lignes de code ajoutées : ~800

**Session jokers (10 janvier 2026) :**
- Nouveaux modules : 3 (radar_recrutement, gestion_jokers, cloture_pronos)
- Nouvelle table : 1 (stock_jokers)
- Scripts de vérification : 3
- Bugs résolus : 5
- Lignes de code ajoutées : ~1200

**Total actuel :**
- **Fichiers totaux :** 25+
- **Lignes de code :** ~4500
- **Tables DB :** 6
- **Modules opérationnels :** 11
- **Fonctionnalités complètes :** Inscription → Pronos → Jokers → Calcul automatique

---

## 🎯 SYSTÈME DE JOKERS - DÉTAILS TECHNIQUES

### Architecture
```
Interface Saisie Pronos
    ↓
Activation Joker (2 cases exclusives)
    ↓
[Points Doubles] → Enregistrement direct
[Points Volés] → Radar Recrutement → Sélection cible
    ↓
Enregistrement dans table jokers + Décrémentation stock
    ↓
Clôture (20h jour J)
    ↓
Détection oublis + Copie pronos volés (avec chaîne)
    ↓
Calcul des gains
    ↓
Application multiplicateur ×2 si Points Doubles
```

### Tables impliquées
- `stock_jokers` : Stock disponible par joueur
- `jokers` : Historique d'utilisation
- `pronostics` : Pronos copiés automatiquement
- `historique` : Points avec multiplicateur appliqué

### Modules impliqués
- `saisie_pronos.py` : Interface + Activation
- `radar_recrutement.py` : Sélection de cible
- `gestion_jokers.py` : Logique de chaîne
- `cloture_pronos.py` : Copie automatique
- `calcul_gains.py` : Application du ×2

---

## 📝 PROCHAINE SESSION

**Objectif suggéré :** Développer le module Classement
- Affichage du leaderboard
- Classement par précision
- Historique des 5 dernières semaines
- Intégration du stock de jokers dans l'affichage

---

**Projet créé le 8 Janvier 2026**  
**Session marathon intensive : 8 Janvier 2026**  
**Session système de jokers : 10 Janvier 2026**  
**Status : Phase 2 Terminée - Système de jokers 100% opérationnel ✅**  
**Phase 3 à venir : Module Classement + Interface Admin 🔄**
