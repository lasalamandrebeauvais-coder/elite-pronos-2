<<<<<<< HEAD
# voir_utilisateurs.py - Affiche tous les utilisateurs de la base de données

from modules.database_manager import DatabaseManager

print("=" * 60)
print("📋 LISTE DES UTILISATEURS INSCRITS")
print("=" * 60)

db = DatabaseManager()
conn = db.create_connection()
cursor = conn.cursor()

# Récupère tous les utilisateurs
cursor.execute("""
    SELECT id, pseudo, prenom, email, telephone, pin, statut
    FROM utilisateurs
    ORDER BY id
""")

users = cursor.fetchall()

if not users:
    print("\n❌ Aucun utilisateur trouvé dans la base de données.")
else:
    print(f"\n✅ {len(users)} utilisateur(s) trouvé(s) :\n")
    
    for user in users:
        print("-" * 60)
        print(f"🆔 ID        : {user[0]}")
        print(f"👤 Pseudo    : {user[1]}")
        print(f"📝 Prénom    : {user[2]}")
        print(f"📧 Email     : {user[3]}")
        print(f"📞 Téléphone : {user[4]}")
        print(f"🔐 PIN       : {user[5]}")
        print(f"📊 Statut    : {user[6]}")

print("\n" + "=" * 60)

=======
# voir_utilisateurs.py - Affiche tous les utilisateurs de la base de données

from modules.database_manager import DatabaseManager

print("=" * 60)
print("📋 LISTE DES UTILISATEURS INSCRITS")
print("=" * 60)

db = DatabaseManager()
conn = db.create_connection()
cursor = conn.cursor()

# Récupère tous les utilisateurs
cursor.execute("""
    SELECT id, pseudo, prenom, email, telephone, pin, statut
    FROM utilisateurs
    ORDER BY id
""")

users = cursor.fetchall()

if not users:
    print("\n❌ Aucun utilisateur trouvé dans la base de données.")
else:
    print(f"\n✅ {len(users)} utilisateur(s) trouvé(s) :\n")
    
    for user in users:
        print("-" * 60)
        print(f"🆔 ID        : {user[0]}")
        print(f"👤 Pseudo    : {user[1]}")
        print(f"📝 Prénom    : {user[2]}")
        print(f"📧 Email     : {user[3]}")
        print(f"📞 Téléphone : {user[4]}")
        print(f"🔐 PIN       : {user[5]}")
        print(f"📊 Statut    : {user[6]}")

print("\n" + "=" * 60)

>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
conn.close()