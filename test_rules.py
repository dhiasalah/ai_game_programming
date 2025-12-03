"""
Fichier de test - Vérifie les règles du jeu avec les exemples fournis
"""

from game_rules import GameState, Color
from game_engine import GameEngine, MoveGenerator

def test_case_1():
    """
    Cas 1 du fichier de règles:
    1 (2R)
    16 (2R) 15 (2B) 14 (2B2R) 13 (2R2B)

    Player even plays 14 B
    Expected: Trous 1, 16, 15, 14 capturés (10 graines)
    """
    print("\n" + "="*80)
    print("CAS DE TEST 1")
    print("="*80)

    # Configuration initiale
    state = GameState()

    # Réinitialise le plateau selon les conditions du test
    for h in range(1, 17):
        state.holes[h] = {Color.RED: 0, Color.BLUE: 0, Color.TRANSPARENT: 0}

    state.holes[1] = {Color.RED: 2, Color.BLUE: 0, Color.TRANSPARENT: 0}
    state.holes[16] = {Color.RED: 2, Color.BLUE: 0, Color.TRANSPARENT: 0}
    state.holes[15] = {Color.RED: 0, Color.BLUE: 2, Color.TRANSPARENT: 0}
    state.holes[14] = {Color.RED: 2, Color.BLUE: 2, Color.TRANSPARENT: 0}
    state.holes[13] = {Color.RED: 2, Color.BLUE: 2, Color.TRANSPARENT: 0}

    state.current_player = 2  # Joueur pair

    print("\nÉtat initial:")
    print(f"Trou 1: {state.holes[1]}")
    print(f"Trou 16: {state.holes[16]}")
    print(f"Trou 15: {state.holes[15]}")
    print(f"Trou 14: {state.holes[14]}")
    print(f"Trou 13: {state.holes[13]}")

    # Joueur 2 joue 14B
    engine = GameEngine(state)
    print("\nJoueur 2 joue le trou 14, couleur BLUE...")

    success = engine.play_move(14, Color.BLUE)

    if success:
        print("\nAprès le coup:")
        print(f"Trou 1: {state.holes[1]}")
        print(f"Trou 16: {state.holes[16]}")
        print(f"Trou 15: {state.holes[15]}")
        print(f"Trou 14: {state.holes[14]}")
        print(f"Trou 13: {state.holes[13]}")

        print(f"\nGraines capturées par le Joueur 2: {state.captured_seeds[2]}")
        print(f"Résultat attendu: 10 graines")

        if state.captured_seeds[2] == 10:
            print("✓ TEST RÉUSSI!")
        else:
            print("✗ TEST ÉCHOUÉ!")
    else:
        print("Le coup n'a pas pu être joué!")

def test_case_2_1():
    """
    Cas 2.1 du fichier de règles:
    1 (1R) 2 (2R) 3(1B) 4(2B) 5(1R)
    16 (3B1R) 15 (2R) 14 (4B)

    Player even plays 16B
    Expected: Trous 5,4,3,2,1 capturés (10 graines)
    """
    print("\n" + "="*80)
    print("CAS DE TEST 2.1")
    print("="*80)

    state = GameState()

    # Réinitialise le plateau
    for h in range(1, 17):
        state.holes[h] = {Color.RED: 0, Color.BLUE: 0, Color.TRANSPARENT: 0}

    state.holes[1] = {Color.RED: 1, Color.BLUE: 0, Color.TRANSPARENT: 0}
    state.holes[2] = {Color.RED: 2, Color.BLUE: 0, Color.TRANSPARENT: 0}
    state.holes[3] = {Color.RED: 0, Color.BLUE: 1, Color.TRANSPARENT: 0}
    state.holes[4] = {Color.RED: 0, Color.BLUE: 2, Color.TRANSPARENT: 0}
    state.holes[5] = {Color.RED: 1, Color.BLUE: 0, Color.TRANSPARENT: 0}
    state.holes[16] = {Color.RED: 1, Color.BLUE: 3, Color.TRANSPARENT: 0}
    state.holes[15] = {Color.RED: 2, Color.BLUE: 0, Color.TRANSPARENT: 0}
    state.holes[14] = {Color.RED: 0, Color.BLUE: 4, Color.TRANSPARENT: 0}

    state.current_player = 2

    print("\nÉtat initial:")
    for h in [1, 2, 3, 4, 5, 16, 15, 14]:
        print(f"Trou {h}: {state.holes[h]}")

    engine = GameEngine(state)
    print("\nJoueur 2 joue le trou 16, couleur BLUE...")

    success = engine.play_move(16, Color.BLUE)

    if success:
        print("\nAprès le coup:")
        for h in [1, 2, 3, 4, 5, 16, 15, 14]:
            print(f"Trou {h}: {state.holes[h]}")

        print(f"\nGraines capturées par le Joueur 2: {state.captured_seeds[2]}")
        print(f"Résultat attendu: 10 graines")

        if state.captured_seeds[2] == 10:
            print("✓ TEST RÉUSSI!")
        else:
            print("✗ TEST ÉCHOUÉ!")
    else:
        print("Le coup n'a pas pu être joué!")

def test_case_2_2():
    """
    Cas 2.2 du fichier de règles:
    1 (1R) 2 (2R) 3(1B) 4(2B) 5(1R)
    16 (3B1R) 15 (2R) 14 (4B)

    Player even plays 16R
    Expected: Trous 1, 16, 15 capturés (7 graines)
    """
    print("\n" + "="*80)
    print("CAS DE TEST 2.2")
    print("="*80)

    state = GameState()

    # Réinitialise le plateau
    for h in range(1, 17):
        state.holes[h] = {Color.RED: 0, Color.BLUE: 0, Color.TRANSPARENT: 0}

    state.holes[1] = {Color.RED: 1, Color.BLUE: 0, Color.TRANSPARENT: 0}
    state.holes[2] = {Color.RED: 2, Color.BLUE: 0, Color.TRANSPARENT: 0}
    state.holes[3] = {Color.RED: 0, Color.BLUE: 1, Color.TRANSPARENT: 0}
    state.holes[4] = {Color.RED: 0, Color.BLUE: 2, Color.TRANSPARENT: 0}
    state.holes[5] = {Color.RED: 1, Color.BLUE: 0, Color.TRANSPARENT: 0}
    state.holes[16] = {Color.RED: 1, Color.BLUE: 3, Color.TRANSPARENT: 0}
    state.holes[15] = {Color.RED: 2, Color.BLUE: 0, Color.TRANSPARENT: 0}
    state.holes[14] = {Color.RED: 0, Color.BLUE: 4, Color.TRANSPARENT: 0}

    state.current_player = 2

    print("\nÉtat initial:")
    for h in [1, 2, 3, 4, 5, 16, 15, 14]:
        print(f"Trou {h}: {state.holes[h]}")

    engine = GameEngine(state)
    print("\nJoueur 2 joue le trou 16, couleur RED...")

    success = engine.play_move(16, Color.RED)

    if success:
        print("\nAprès le coup:")
        for h in [1, 2, 3, 4, 5, 16, 15, 14]:
            print(f"Trou {h}: {state.holes[h]}")

        print(f"\nGraines capturées par le Joueur 2: {state.captured_seeds[2]}")
        print(f"Résultat attendu: 7 graines")

        if state.captured_seeds[2] == 7:
            print("✓ TEST RÉUSSI!")
        else:
            print("✗ TEST ÉCHOUÉ!")
    else:
        print("Le coup n'a pas pu être joué!")

def test_transparent_seeds():
    """
    Test pour vérifier la gestion des graines transparentes
    """
    print("\n" + "="*80)
    print("TEST DES GRAINES TRANSPARENTES")
    print("="*80)

    state = GameState()
    state.current_player = 1

    print("\nÉtat initial du trou 1:")
    print(f"{state.holes[1]}")

    print("\nCoups valides pour le Joueur 1:")
    valid_moves = MoveGenerator.get_all_moves(state, 1)

    transparent_moves = [m for m in valid_moves if m[1] == Color.TRANSPARENT]
    print(f"Nombre de coups avec graines transparentes: {len(transparent_moves)}")

    for hole, color, transparent_as in transparent_moves:
        print(f"  - Trou {hole}, Transparent comme {transparent_as.value}")

    if len(transparent_moves) > 0:
        print("\n✓ Les graines transparentes sont correctement gérées!")
    else:
        print("\n✗ Problème avec les graines transparentes!")

def run_all_tests():
    """Exécute tous les tests"""
    print("\n" + "="*80)
    print("SUITE DE TESTS - VÉRIFICATION DES RÈGLES")
    print("="*80)

    test_case_1()
    test_case_2_1()
    test_case_2_2()
    test_transparent_seeds()

    print("\n" + "="*80)
    print("TESTS TERMINÉS")
    print("="*80)

if __name__ == "__main__":
    run_all_tests()

