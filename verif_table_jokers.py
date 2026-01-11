<<<<<<< HEAD
from modules.database_manager import DatabaseManager

db = DatabaseManager()
conn = db.create_connection()
cursor = conn.cursor()

# Vérifie la structure de la table jokers
cursor.execute("PRAGMA table_info(jokers)")
columns = cursor.fetchall()

print("STRUCTURE DE LA TABLE JOKERS :")
print("=" * 60)
for col in columns:
    print(f"  {col[1]} ({col[2]}) - NOT NULL: {col[3]}")

# Vérifie le contenu
cursor.execute("SELECT * FROM jokers")
jokers = cursor.fetchall()

print(f"\nCONTENU ACTUEL : {len(jokers)} joker(s)")
print("=" * 60)

=======
from modules.database_manager import DatabaseManager

db = DatabaseManager()
conn = db.create_connection()
cursor = conn.cursor()

# Vérifie la structure de la table jokers
cursor.execute("PRAGMA table_info(jokers)")
columns = cursor.fetchall()

print("STRUCTURE DE LA TABLE JOKERS :")
print("=" * 60)
for col in columns:
    print(f"  {col[1]} ({col[2]}) - NOT NULL: {col[3]}")

# Vérifie le contenu
cursor.execute("SELECT * FROM jokers")
jokers = cursor.fetchall()

print(f"\nCONTENU ACTUEL : {len(jokers)} joker(s)")
print("=" * 60)

>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
conn.close()