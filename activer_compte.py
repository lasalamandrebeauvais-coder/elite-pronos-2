<<<<<<< HEAD
# activer_compte.py - Active un compte en attente

from modules.database_manager import DatabaseManager

print("=" * 60)
print("🔓 ACTIVATION DE COMPTE")
print("=" * 60)

# Pseudo à activer (modifie ici si besoin)
pseudo = "alex345"

print(f"\n👤 Activation du compte : {pseudo}")

db = DatabaseManager()
conn = db.create_connection()
cursor = conn.cursor()

try:
    # Vérifie si le compte existe
    cursor.execute("SELECT id, pseudo, statut FROM utilisateurs WHERE pseudo = ?", (pseudo,))
    user = cursor.fetchone()
    
    if not user:
        print(f"\n❌ Aucun utilisateur trouvé avec le pseudo '{pseudo}'")
    elif user[2] == 'actif':
        print(f"\n⚠️ Le compte '{pseudo}' est déjà actif !")
    else:
        # Active le compte
        cursor.execute("UPDATE utilisateurs SET statut = 'actif' WHERE pseudo = ?", (pseudo,))
        conn.commit()
        print(f"\n✅ Le compte '{pseudo}' a été activé avec succès ! 🎉")
        print(f"   Tu peux maintenant te connecter.")
        
except Exception as e:
    print(f"\n❌ Erreur : {e}")
finally:
    conn.close()

=======
# activer_compte.py - Active un compte en attente

from modules.database_manager import DatabaseManager

print("=" * 60)
print("🔓 ACTIVATION DE COMPTE")
print("=" * 60)

# Pseudo à activer (modifie ici si besoin)
pseudo = "alex345"

print(f"\n👤 Activation du compte : {pseudo}")

db = DatabaseManager()
conn = db.create_connection()
cursor = conn.cursor()

try:
    # Vérifie si le compte existe
    cursor.execute("SELECT id, pseudo, statut FROM utilisateurs WHERE pseudo = ?", (pseudo,))
    user = cursor.fetchone()
    
    if not user:
        print(f"\n❌ Aucun utilisateur trouvé avec le pseudo '{pseudo}'")
    elif user[2] == 'actif':
        print(f"\n⚠️ Le compte '{pseudo}' est déjà actif !")
    else:
        # Active le compte
        cursor.execute("UPDATE utilisateurs SET statut = 'actif' WHERE pseudo = ?", (pseudo,))
        conn.commit()
        print(f"\n✅ Le compte '{pseudo}' a été activé avec succès ! 🎉")
        print(f"   Tu peux maintenant te connecter.")
        
except Exception as e:
    print(f"\n❌ Erreur : {e}")
finally:
    conn.close()

>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
print("\n" + "=" * 60)