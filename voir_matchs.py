<<<<<<< HEAD
from modules.database_manager import DatabaseManager

db = DatabaseManager()
conn = db.create_connection()
cursor = conn.cursor()

cursor.execute("SELECT id, equipe_domicile, equipe_exterieur, semaine FROM matchs WHERE semaine = 1")
matchs = cursor.fetchall()

print("MATCHS DE LA SEMAINE 1 :")
for match in matchs:
    print(f"ID: {match[0]} | {match[1]} vs {match[2]} | Semaine: {match[3]}")

=======
from modules.database_manager import DatabaseManager

db = DatabaseManager()
conn = db.create_connection()
cursor = conn.cursor()

cursor.execute("SELECT id, equipe_domicile, equipe_exterieur, semaine FROM matchs WHERE semaine = 1")
matchs = cursor.fetchall()

print("MATCHS DE LA SEMAINE 1 :")
for match in matchs:
    print(f"ID: {match[0]} | {match[1]} vs {match[2]} | Semaine: {match[3]}")

>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
conn.close()