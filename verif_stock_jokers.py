<<<<<<< HEAD
from modules.database_manager import DatabaseManager

db = DatabaseManager()
conn = db.create_connection()
cursor = conn.cursor()

# Vérifie la structure de la table stock_jokers
cursor.execute("PRAGMA table_info(stock_jokers)")
columns = cursor.fetchall()

print("\nSTRUCTURE DE LA TABLE STOCK_JOKERS :")
print("=" * 60)
for col in columns:
    print(f"  {col[1]} ({col[2]}) - NOT NULL: {col[3]}")

# Vérifie le contenu
cursor.execute("SELECT * FROM stock_jokers")
stocks = cursor.fetchall()

print(f"\nCONTENU ACTUEL : {len(stocks)} ligne(s)")
print("=" * 60)

=======
from modules.database_manager import DatabaseManager

db = DatabaseManager()
conn = db.create_connection()
cursor = conn.cursor()

# Vérifie la structure de la table stock_jokers
cursor.execute("PRAGMA table_info(stock_jokers)")
columns = cursor.fetchall()

print("\nSTRUCTURE DE LA TABLE STOCK_JOKERS :")
print("=" * 60)
for col in columns:
    print(f"  {col[1]} ({col[2]}) - NOT NULL: {col[3]}")

# Vérifie le contenu
cursor.execute("SELECT * FROM stock_jokers")
stocks = cursor.fetchall()

print(f"\nCONTENU ACTUEL : {len(stocks)} ligne(s)")
print("=" * 60)

>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
conn.close()