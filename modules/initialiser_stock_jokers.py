<<<<<<< HEAD
from database_manager import DatabaseManager

# Connexion à la base
db = DatabaseManager()
conn = db.create_connection()
cursor = conn.cursor()

# Récupère tous les utilisateurs
cursor.execute("SELECT id, pseudo FROM utilisateurs")
utilisateurs = cursor.fetchall()

print(f"\n📊 {len(utilisateurs)} utilisateur(s) trouvé(s)\n")
print("=" * 60)

# Pour chaque utilisateur, initialise son stock de jokers
for user in utilisateurs:
    user_id = user[0]
    pseudo = user[1]
    
    # Vérifie si le joueur a déjà un stock
    cursor.execute("SELECT * FROM stock_jokers WHERE utilisateur_id = ?", (user_id,))
    stock_existe = cursor.fetchone()
    
    if stock_existe:
        print(f"⚠️  {pseudo} : Stock déjà existant (non modifié)")
    else:
        # Crée le stock avec 3 jokers doubles et 2 jokers volés
        cursor.execute("""
            INSERT INTO stock_jokers (utilisateur_id, jokers_doubles_disponibles, jokers_voles_disponibles)
            VALUES (?, 3, 2)
        """, (user_id,))
        print(f"✅ {pseudo} : 3 jokers doubles + 2 jokers volés ajoutés")

# Sauvegarde
conn.commit()

print("=" * 60)
print("✅ Initialisation terminée !\n")

# Affiche le résultat final
cursor.execute("""
    SELECT u.pseudo, s.jokers_doubles_disponibles, s.jokers_voles_disponibles 
    FROM stock_jokers s
    JOIN utilisateurs u ON s.utilisateur_id = u.id
""")
stocks = cursor.fetchall()

print("📦 STOCK FINAL :")
print("=" * 60)
for stock in stocks:
    print(f"  {stock[0]} : {stock[1]} joker(s) doubles | {stock[2]} joker(s) volés")

conn.close()
=======
from database_manager import DatabaseManager

# Connexion à la base
db = DatabaseManager()
conn = db.create_connection()
cursor = conn.cursor()

# Récupère tous les utilisateurs
cursor.execute("SELECT id, pseudo FROM utilisateurs")
utilisateurs = cursor.fetchall()

print(f"\n📊 {len(utilisateurs)} utilisateur(s) trouvé(s)\n")
print("=" * 60)

# Pour chaque utilisateur, initialise son stock de jokers
for user in utilisateurs:
    user_id = user[0]
    pseudo = user[1]
    
    # Vérifie si le joueur a déjà un stock
    cursor.execute("SELECT * FROM stock_jokers WHERE utilisateur_id = ?", (user_id,))
    stock_existe = cursor.fetchone()
    
    if stock_existe:
        print(f"⚠️  {pseudo} : Stock déjà existant (non modifié)")
    else:
        # Crée le stock avec 3 jokers doubles et 2 jokers volés
        cursor.execute("""
            INSERT INTO stock_jokers (utilisateur_id, jokers_doubles_disponibles, jokers_voles_disponibles)
            VALUES (?, 3, 2)
        """, (user_id,))
        print(f"✅ {pseudo} : 3 jokers doubles + 2 jokers volés ajoutés")

# Sauvegarde
conn.commit()

print("=" * 60)
print("✅ Initialisation terminée !\n")

# Affiche le résultat final
cursor.execute("""
    SELECT u.pseudo, s.jokers_doubles_disponibles, s.jokers_voles_disponibles 
    FROM stock_jokers s
    JOIN utilisateurs u ON s.utilisateur_id = u.id
""")
stocks = cursor.fetchall()

print("📦 STOCK FINAL :")
print("=" * 60)
for stock in stocks:
    print(f"  {stock[0]} : {stock[1]} joker(s) doubles | {stock[2]} joker(s) volés")

conn.close()
>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
print("=" * 60)