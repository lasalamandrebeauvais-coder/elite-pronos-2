# 🔄 DOCUMENT DE REPRISE - ELITE PRONOS 2
# Session Jokers - Point de sauvegarde

**Date de sauvegarde :** 8 Janvier 2026  
**Dernière étape complétée :** Étape 41 - Vérification table jokers  
**Prochaine étape :** Créer la structure pour le système de jokers

---

## 📍 OÙ ON EN EST

### ✅ CE QUI EST TERMINÉ
1. **Module Calcul des Gains** : 100% fonctionnel
   - Calcul automatique des points
   - Détection Grand Chelem
   - Mise à jour historique
   - Tous les tests validés

2. **Bot de Sourcing amélioré** :
   - Récupération automatique des résultats depuis l'API
   - Lancement automatique du calcul quand 4 matchs terminés
   - Mise à jour du statut des matchs

### 🔄 EN COURS : SYSTÈME DE JOKERS

**Objectif actuel :** Développer le système complet de jokers avec animations

---

## 🎯 SPÉCIFICATIONS DES JOKERS (Validées)

### 1. JOKER "POINTS DOUBLES" (👑x2)
- **Activation :** Pendant la saisie des pronos
- **Effet :** Gains totaux de la semaine × 2
- **Restriction :** Multiplicateur strictement personnel, non transférable
- **Animation :** Halo doré sur la grille + explosion de particules dorées au résultat

### 2. JOKER "POINTS VOLÉS" (✋➡️)
- **Activation :** Pendant la saisie des pronos
- **Effet :** Copie les pronos d'un autre joueur
- **Restriction cible :** Ne peut cibler QUE les joueurs à 100 points (pas ceux à 140)
- **Verrouillage :** Saisie des scores devient inaccessible
- **Radar de Recrutement :** Tableau avec stats de tous les joueurs éligibles
  - Points totaux
  - Nombre de bons pronos
  - Indice de forme (3 dernières semaines)
  - Indication si la cible a aussi utilisé un joker volé
- **Chaîne automatique :** Si A vole B et B vole C → A récupère les pronos de C
- **Non-cumul :** Le voleur ne récupère que les pronos bruts, jamais le multiplicateur x2
- **Animation :** Grille grisée + coffre-fort qui s'ouvre

### 3. RÈGLE DE SÉCURITÉ (OUBLI)
- **Déclenchement :** Aucun prono validé avant date limite
- **Action auto :** Active le joker "Points Volés"
- **Cible par défaut :** Dernier du classement général
- **Si le dernier a aussi oublié :** Remonte au joueur précédent, etc.
- **Animation :** Bouée de sauvetage avec message "OUF ! Le système vous a sauvé"

---

## 🗄️ STRUCTURE BASE DE DONNÉES

### Table `jokers` (Actuelle - OK)
```sql
- id (INTEGER, PK)
- utilisateur_id (INTEGER, FK)
- type_joker (TEXT) : "points_doubles" ou "points_voles"
- utilise (INTEGER) : 0 ou 1
- semaine_utilisation (INTEGER)
- cible_vol_id (INTEGER) : ID du joueur volé (NULL si doubles)
- date_utilisation (TIMESTAMP)
```

### Table `stock_jokers` (À CRÉER - Décision en cours)
**Option recommandée :** Créer une table séparée pour gérer le stock
```sql
- id (INTEGER, PK)
- utilisateur_id (INTEGER, FK)
- jokers_doubles_disponibles (INTEGER) : Nombre de jokers doubles restants
- jokers_voles_disponibles (INTEGER) : Nombre de jokers volés restants
- derniere_mise_a_jour (TIMESTAMP)
```

**Alternative :** Modifier la table utilisateurs pour ajouter ces colonnes

---

## 📋 DÉCISIONS PRISES

✅ **Budget vol :** Le voleur ne peut cibler QUE les joueurs à 100 points (pas ceux à 140)  
✅ **Animations :** Logique + Animations complètes (système professionnel)  
✅ **Activation :** Pendant la saisie des pronos (pas avant)  
✅ **Oubli :** Active automatiquement le joker "Points Volés" sur le dernier du classement

---

## 🔧 PROCHAINES ÉTAPES À RÉALISER

### Étape 42 : Créer la table stock_jokers
- Ajouter la table dans `database_manager.py`
- Initialiser le stock pour tous les joueurs existants

### Étape 43 : Modifier l'interface saisie_pronos.py
- Ajouter section choix du joker en haut
- 2 cases à cocher exclusives (1 seul actif)
- Afficher le stock disponible

### Étape 44 : Créer le Radar de Recrutement
- Module `radar_recrutement.py`
- Fenêtre popup avec tableau
- Filtrer uniquement joueurs à 100 points
- Afficher stats et forme

### Étape 45 : Logique de la chaîne
- Fonction récursive pour remonter la chaîne
- Détection des boucles infinies
- Enregistrement dans la table jokers

### Étape 46 : Modifier calcul_gains.py
- Intégrer le multiplicateur x2 pour Points Doubles
- Gérer la copie des pronos pour Points Volés
- Ne pas transférer le multiplicateur lors d'un vol

### Étape 47 : Animations visuelles
- CSS pour halo doré
- Animations particules (canvas ou CSS)
- Grille grisée pour vol
- Coffre-fort et bouée

### Étape 48 : Gestion de l'oubli automatique
- Script cron ou vérification manuelle
- Activation auto joker voleur
- Sélection du dernier du classement

---

## 💻 FICHIERS À MODIFIER/CRÉER

### À MODIFIER :
1. `modules/database_manager.py` : Ajouter table stock_jokers
2. `modules/saisie_pronos.py` : Interface de sélection joker
3. `modules/calcul_gains.py` : Intégrer les jokers dans le calcul

### À CRÉER :
1. `modules/radar_recrutement.py` : Interface de sélection de cible
2. `modules/gestion_jokers.py` : Logique chaîne et validations
3. Script de test pour les jokers

---

## 📝 COMMANDES UTILES

### Vérifier la table jokers
```bash
python verif_table_jokers.py
```

### Tester le calcul des gains
```bash
python test_calcul.py
```

### Lancer le bot de sourcing
```python
from modules.sourcing_bot import SourcingBot
bot = SourcingBot()
bot.run(semaine=2)
```

### Mettre à jour résultats et calculer
```python
bot.update_results(semaine=2)
```

---

## 🎨 CHOIX D'IMPLÉMENTATION VISUELS

### Joker Points Doubles
- **Icône :** 👑x2 ou 💎x2
- **Couleur :** Doré (#FFD700)
- **Effet hover :** Légère pulsation
- **Animation activation :** Halo qui s'étend depuis le centre

### Joker Points Volés
- **Icône :** ✋➡️ ou 🎯
- **Couleur :** Bleu électrique (#00BFFF)
- **Effet hover :** Légère rotation
- **Animation activation :** Grille qui se grise progressivement

### Radar de Recrutement
- **Style :** Popup modale centrée
- **Fond :** Semi-transparent avec blur
- **Tableau :** Lignes alternées, hover highlight
- **Indicateurs forme :** Pastilles colorées (Vert/Orange/Rouge)

---

## 🔑 POINTS CLÉS À NE PAS OUBLIER

1. **Un seul joker par semaine** : Les 2 cases ne peuvent jamais être cochées ensemble
2. **Vérifier le budget** : Voleur ne peut cibler que joueurs à 100 pts
3. **Chaîne récursive** : Remonter jusqu'au joueur qui a vraiment fait ses pronos
4. **Pas de cumul** : Voleur ne récupère JAMAIS le x2 de sa cible
5. **Oubli = Voleur auto** : Jamais de joker Points Doubles auto
6. **Animations non bloquantes** : L'utilisateur doit pouvoir continuer

---

## 📊 ÉTAT DES MODULES

| Module | Statut | Complétude |
|--------|--------|------------|
| config.py | ✅ Terminé | 100% |
| database_manager.py | 🔄 À modifier | 95% (table stock_jokers à ajouter) |
| inscription.py | ✅ Terminé | 100% |
| login.py | ✅ Terminé | 100% |
| dashboard.py | ✅ Terminé | 100% |
| saisie_pronos.py | 🔄 À modifier | 80% (jokers à intégrer) |
| sourcing_bot.py | ✅ Terminé | 100% |
| calcul_gains.py | 🔄 À modifier | 90% (multiplicateur jokers à ajouter) |
| radar_recrutement.py | ❌ À créer | 0% |
| gestion_jokers.py | ❌ À créer | 0% |

---

## 🗣️ QUESTION EN ATTENTE

**Étape 41 - Choix de structure :**

"Option B : Créer une nouvelle table `stock_jokers`
- Table séparée pour le stock de chaque joueur
- Table `jokers` garde l'historique d'utilisation
- Plus propre et modulaire"

**Attente de confirmation pour :**
- Créer la table stock_jokers (recommandé)
- OU modifier la table utilisateurs

**Réponse attendue :** "OK" pour Option B ou "Je préfère A" pour modifier utilisateurs

---

## 💾 FICHIERS DE RÉFÉRENCE

- `RECAPITULATIF_COMPLET_V2.md` : Documentation complète du projet
- `sourcing_bot_final.py` : Version finale du bot avec calcul auto
- Descriptif jokers du client : Voir document joint dans la session

---

## 🚀 POUR REPRENDRE

**Dire à Claude :**

"Bonjour ! Je reprends le développement d'Elite Pronos 2. On était à l'étape 41, on doit créer le système de jokers. J'ai le document de reprise. On était sur le point de décider entre Option A ou B pour la structure de la table stock_jokers. Je choisis l'Option B (table séparée). On peut continuer ?"

**Ensuite suivre les étapes 42 à 48 dans l'ordre.**

---

**Session sauvegardée le 8 Janvier 2026 - Prêt à reprendre ! 🚀**
