<<<<<<< HEAD
from modules.database_manager import DatabaseManager

db = DatabaseManager()
conn = db.create_connection()
cursor = conn.cursor()

cursor.execute("""
    SELECT p.match_id, p.score_domicile_prono, p.score_exterieur_prono, p.mise,
           m.equipe_domicile, m.equipe_exterieur,
           m.cote_domicile, m.cote_nul, m.cote_exterieur
    FROM pronostics p
    INNER JOIN matchs m ON p.match_id = m.id
    INNER JOIN utilisateurs u ON p.utilisateur_id = u.id
    WHERE u.pseudo = 'alex345' AND m.semaine = 1
""")

pronos = cursor.fetchall()

print("PRONOS DE ALEX345 (Semaine 1) :")
print("=" * 80)
for p in pronos:
    print(f"Match {p[0]} : {p[4]} vs {p[5]}")
    print(f"  Prono : {p[1]}-{p[2]} | Mise : {p[3]} pts")
    print(f"  Cotes : Dom={p[6]} | Nul={p[7]} | Ext={p[8]}")
    print("-" * 80)

=======
from modules.database_manager import DatabaseManager

db = DatabaseManager()
conn = db.create_connection()
cursor = conn.cursor()

cursor.execute("""
    SELECT p.match_id, p.score_domicile_prono, p.score_exterieur_prono, p.mise,
           m.equipe_domicile, m.equipe_exterieur,
           m.cote_domicile, m.cote_nul, m.cote_exterieur
    FROM pronostics p
    INNER JOIN matchs m ON p.match_id = m.id
    INNER JOIN utilisateurs u ON p.utilisateur_id = u.id
    WHERE u.pseudo = 'alex345' AND m.semaine = 1
""")

pronos = cursor.fetchall()

print("PRONOS DE ALEX345 (Semaine 1) :")
print("=" * 80)
for p in pronos:
    print(f"Match {p[0]} : {p[4]} vs {p[5]}")
    print(f"  Prono : {p[1]}-{p[2]} | Mise : {p[3]} pts")
    print(f"  Cotes : Dom={p[6]} | Nul={p[7]} | Ext={p[8]}")
    print("-" * 80)

>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
conn.close()