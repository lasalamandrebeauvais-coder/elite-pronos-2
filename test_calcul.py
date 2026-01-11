<<<<<<< HEAD
from modules.calcul_gains import CalculGains

print("\n" + "="*60)
print("TEST AVEC RÉSULTATS VARIÉS")
print("="*60 + "\n")

print("🔬 TEST : Mix de scores exacts, bons résultats et échecs")
print("-" * 60)

scores_test = [
    {"match_id": 13, "score_dom": 2, "score_ext": 1},
    {"match_id": 14, "score_dom": 1, "score_ext": 1},
    {"match_id": 15, "score_dom": 1, "score_ext": 0},
    {"match_id": 16, "score_dom": 3, "score_ext": 2}
]

calc = CalculGains(semaine=1)
calc.calculer_pour_semaine(scores_test)

print("\n" + "="*60)
print("✅ TEST TERMINÉ")
=======
from modules.calcul_gains import CalculGains

print("\n" + "="*60)
print("TEST AVEC RÉSULTATS VARIÉS")
print("="*60 + "\n")

print("🔬 TEST : Mix de scores exacts, bons résultats et échecs")
print("-" * 60)

scores_test = [
    {"match_id": 13, "score_dom": 2, "score_ext": 1},
    {"match_id": 14, "score_dom": 1, "score_ext": 1},
    {"match_id": 15, "score_dom": 1, "score_ext": 0},
    {"match_id": 16, "score_dom": 3, "score_ext": 2}
]

calc = CalculGains(semaine=1)
calc.calculer_pour_semaine(scores_test)

print("\n" + "="*60)
print("✅ TEST TERMINÉ")
>>>>>>> 59349ac3062ac7bdb8121e70c25a96bfbda2a9b8
print("="*60)