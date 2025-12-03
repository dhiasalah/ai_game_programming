"""
Script de test pour vérifier que le bot fonctionne correctement
"""

from bot import AwaleGame, AIBot

def test_basic_move():
    """Test un coup basique"""
    game = AwaleGame()

    # Afficher l'état initial
    print("État initial:")
    print(f"Joueur courant: {game.current_player}")
    print(f"Trous du joueur 0: R={game.red[0:15:2]} B={game.blue[0:15:2]} T={game.transparent[0:15:2]}")

    # Joueur 0 joue 1R (trou 1, couleur rouge)
    result = game.apply_move("1R")
    print(f"\nCoup '1R' appliqué: {result}")
    print(f"Joueur courant après le coup: {game.current_player}")
    print(f"Trou 1 après le coup: R={game.red[0]} B={game.blue[0]} T={game.transparent[0]}")

    # Vérifier les coups valides
    valid_moves = game.get_valid_moves(0)
    print(f"\nCoups valides pour joueur 0: {valid_moves}")

def test_ai_bot():
    """Test le bot IA"""
    game = AwaleGame()
    bot = AIBot(depth=2)

    print("\n=== Test du Bot IA ===")
    print("État initial du jeu")

    # Joueur 0 demande un coup
    move = bot.get_move(game, 0)
    print(f"Bot (joueur 0) suggère le coup: {move}")

    # Appliquer ce coup
    result = game.apply_move(move)
    print(f"Coup appliqué avec succès: {result}")
    print(f"Joueur courant: {game.current_player}")

def test_game_sequence():
    """Test une séquence de coups"""
    game = AwaleGame()
    bot = AIBot(depth=2)

    print("\n=== Séquence de coups ===")

    for round_num in range(3):
        print(f"\n--- Tour {round_num + 1} ---")

        current_player = game.current_player
        valid_moves = game.get_valid_moves(current_player)

        if not valid_moves:
            print(f"Joueur {current_player} n'a pas de coups valides")
            break

        # Bot calcule le meilleur coup
        move = bot.get_move(game, current_player)
        print(f"Joueur {current_player} joue: {move}")

        # Appliquer le coup
        game.apply_move(move)
        print(f"Scores: P0={game.score[0]} P1={game.score[1]}")

if __name__ == "__main__":
    test_basic_move()
    test_ai_bot()
    test_game_sequence()
    print("\n✓ Tous les tests sont terminés!")

