"""
Fichier de test détaillé avec traçage pas à pas
"""

from game_rules import GameState, Color
from game_engine import GameEngine, MoveGenerator

def trace_case_1():
    """
    Cas 1 du fichier de règles avec traçage détaillé:
    1 (2R)
    16 (2R) 15 (2B) 14 (2B2R) 13 (2R2B)

    Player even (2) plays 14 B
    """
    print("\n" + "="*80)
    print("CAS 1 - TRAÇAGE DÉTAILLÉ")
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

    state.current_player = 2

    print("\nÉtat initial:")
    print(f"Trou 1:  {state.holes[1]}")
    print(f"Trou 13: {state.holes[13]}")
    print(f"Trou 14: {state.holes[14]}")
    print(f"Trou 15: {state.holes[15]}")
    print(f"Trou 16: {state.holes[16]}")

    print("\nJoueur 2 joue le trou 14, couleur BLUE")
    print("Les graines bleues vont uniquement dans les trous adverses (Joueur 1)")

    engine = GameEngine(state)

    # Traçage du sowing
    print("\nDistribution des graines:")
    print("- Trou 14 a 2 graines bleues")
    print("- Trou 15 (graine 1) : trou adverse? NON (trou 15 = Joueur 1 impair? NON, c'est pair)")
    print("- Trou 16 (graine 1 après skip 15) : trou adverse? OUI (trou 16 = Joueur 2 pair) SKIP")
    print("- Trou 1 (graine 1 après skip 16) : trou adverse? OUI (trou 1 = Joueur 1 impair)")

    # Affichage des trous joueur 1 et joueur 2
    print(f"\nTrous Joueur 1 (impairs): {state.get_player_holes(1)}")
    print(f"Trous Joueur 2 (pairs): {state.get_player_holes(2)}")

    success = engine.play_move(14, Color.BLUE)

    if success:
        print("\nAprès le coup:")
        print(f"Trou 1:  {state.holes[1]}")
        print(f"Trou 13: {state.holes[13]}")
        print(f"Trou 14: {state.holes[14]}")
        print(f"Trou 15: {state.holes[15]}")
        print(f"Trou 16: {state.holes[16]}")

        print(f"\nGraines capturées par le Joueur 2: {state.captured_seeds[2]}")
        print(f"Résultat attendu: 10 graines")

        if state.captured_seeds[2] == 10:
            print("✓ TEST RÉUSSI!")
        else:
            print("✗ TEST ÉCHOUÉ!")
            print(f"Différence: Reçu {state.captured_seeds[2]}, attendu 10")
    else:
        print("Le coup n'a pas pu être joué!")

def trace_case_2_1():
    """
    Cas 2.1 avec traçage détaillé
    """
    print("\n" + "="*80)
    print("CAS 2.1 - TRAÇAGE DÉTAILLÉ")
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
    print(f"Trous Joueur 1 (impairs): {state.get_player_holes(1)}")
    print(f"Trous Joueur 2 (pairs): {state.get_player_holes(2)}")

    for h in [1, 2, 3, 4, 5, 16, 15, 14]:
        total = sum(state.holes[h].values())
        print(f"Trou {h:2d}: {state.holes[h]} = {total} graines")

    print("\nJoueur 2 joue le trou 16, couleur BLUE")
    print("Les 3 graines bleues vont uniquement dans les trous adverses (Joueur 1)")

    engine = GameEngine(state)
    success = engine.play_move(16, Color.BLUE)

    if success:
        print("\nAprès le coup:")
        for h in [1, 2, 3, 4, 5, 16, 15, 14]:
            total = sum(state.holes[h].values())
            print(f"Trou {h:2d}: {state.holes[h]} = {total} graines")

        print(f"\nGraines capturées par le Joueur 2: {state.captured_seeds[2]}")
        print(f"Résultat attendu: 10 graines")

        if state.captured_seeds[2] == 10:
            print("✓ TEST RÉUSSI!")
        else:
            print("✗ TEST ÉCHOUÉ!")
    else:
        print("Le coup n'a pas pu être joué!")

if __name__ == "__main__":
    trace_case_1()
    trace_case_2_1()

