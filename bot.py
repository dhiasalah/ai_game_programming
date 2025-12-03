"""
Bot pour la plateforme awale-arena
Format compatible:
- Entrée: mouvements au format "NX" ou "NTX" (N=numéro trou, X=R/B/T, T=transparent)
- Sortie: coup au même format
- Logique IA conservée de la version actuelle
"""

import sys
import random
from typing import List, Optional, Tuple

class AwaleGame:
    """Classe pour gérer le jeu Awale avec format compatible awale-arena"""

    def __init__(self):
        """
        Initialise le plateau 16 trous
        Joueur 1: trous 1,3,5,7,9,11,13,15 (impairs)
        Joueur 2: trous 2,4,6,8,10,12,14,16 (pairs)
        Chaque trou commence avec R=2, B=2, T=2
        """
        self.red = [2] * 16      # Index 0-15 représente trous 1-16
        self.blue = [2] * 16
        self.transparent = [2] * 16
        self.score = [0, 0]      # Score des 2 joueurs
        self.current_player = 0  # 0 pour joueur 1, 1 pour joueur 2

    def get_pit_color_array(self, color: str):
        """Retourne l'array correspondant à la couleur"""
        color_upper = color.upper()
        if color_upper == 'R':
            return self.red
        elif color_upper == 'B':
            return self.blue
        else:  # 'T'
            return self.transparent

    def convert_hole_number_to_index(self, hole_number: int) -> int:
        """Convertit le numéro de trou (1-16) en index (0-15)"""
        return hole_number - 1

    def convert_index_to_hole_number(self, index: int) -> int:
        """Convertit l'index (0-15) en numéro de trou (1-16)"""
        return index + 1

    def distribute_seeds_by_color(self, start_index: int, pit_color: str, pit_index: int) -> int:
        """
        Distribue les graines d'une couleur donnée
        start_index: index du trou où commencer la distribution
        pit_color: 'R', 'B', ou 'T'
        pit_index: index du trou source (à ignorer)

        Retourne l'index du dernier trou où une graine a été placée
        """
        pit_colors = self.get_pit_color_array(pit_color)
        nb_seeds = pit_colors[pit_index]
        pit_colors[pit_index] = 0

        step = 1 if pit_color == 'R' else 2  # 1 pour rouge, 2 pour bleu

        last_index = start_index
        distributed = 0

        while distributed < nb_seeds:
            last_index = (last_index + step) % 16

            # Skip le trou source
            if last_index == pit_index:
                last_index = (last_index + step) % 16

            pit_colors[last_index] += 1
            distributed += 1

        return last_index

    def apply_move(self, move: str) -> bool:
        """
        Applique un mouvement au format "NX" ou "NTX"
        N: numéro du trou (1-16)
        X: couleur (R, B)
        T: optionnel, indique transparent

        Exemples:
        - "3R": joue les graines rouges du trou 3
        - "4B": joue les graines bleues du trou 4
        - "4TR": joue les graines transparentes du trou 4 comme rouges
        - "4TB": joue les graines transparentes du trou 4 comme bleues

        Retourne True si le coup est valide, False sinon
        """
        try:
            # Déterminer si transparent
            is_transparent = 'T' in move.upper()
            pit_color = move[-1].upper()

            if is_transparent:
                pit_index = int(move[:-2]) - 1  # Enlever "TR" ou "TB"
            else:
                pit_index = int(move[:-1]) - 1  # Enlever "R" ou "B"

            # Vérifications
            if pit_index < 0 or pit_index >= 16:
                return False

            # Vérifier que c'est un trou du joueur courant
            player_holes = self._get_player_holes(self.current_player)
            if pit_index not in player_holes:
                return False

            # Vérifier qu'il y a des graines
            if not is_transparent:
                if self.get_pit_color_array(pit_color)[pit_index] == 0:
                    return False
            else:
                if self.transparent[pit_index] == 0:
                    return False

            # Calculer le point de départ et le pas
            start_index = (pit_index - 1 + 16) % 16

            # Si transparent, distribuer d'abord les graines transparentes
            if is_transparent:
                start_index = self.distribute_seeds_by_color(start_index, 'T', pit_index)

            # Ensuite distribuer les graines de la couleur désignée
            last_index = self.distribute_seeds_by_color(start_index, pit_color, pit_index)

            # Capturer les graines si applicable
            self.capture_seeds(last_index)

            # Changer de joueur
            self.current_player = (self.current_player + 1) % 2
            return True

        except (ValueError, IndexError):
            return False

    def capture_seeds(self, last_index: int):
        """
        Capture les graines selon les règles:
        - Capture si exactement 2 ou 3 graines dans le dernier trou
        - Continue en arrière si les conditions sont remplies
        """
        while True:
            nb_seeds_in_pit = self.red[last_index] + self.blue[last_index] + self.transparent[last_index]

            if 1 < nb_seeds_in_pit < 4:
                # Capturer ce trou
                self.score[self.current_player] += nb_seeds_in_pit
                self.red[last_index] = 0
                self.blue[last_index] = 0
                self.transparent[last_index] = 0

                # Vérifier le trou précédent
                last_index = (last_index - 1 + 16) % 16
            else:
                break

    def _get_player_holes(self, player: int) -> List[int]:
        """
        Retourne les indices des trous d'un joueur
        Joueur 0: indices 0,2,4,6,8,10,12,14 (trous 1,3,5,7,9,11,13,15)
        Joueur 1: indices 1,3,5,7,9,11,13,15 (trous 2,4,6,8,10,12,14,16)
        """
        if player == 0:
            return [i for i in range(16) if i % 2 == 0]
        else:
            return [i for i in range(16) if i % 2 == 1]

    def get_valid_moves(self, player: int) -> List[str]:
        """Retourne tous les mouvements valides pour un joueur"""
        valid_moves = []
        player_holes = self._get_player_holes(player)

        for hole_index in player_holes:
            hole_number = self.convert_index_to_hole_number(hole_index)

            if self.red[hole_index] > 0:
                valid_moves.append(f"{hole_number}R")

            if self.blue[hole_index] > 0:
                valid_moves.append(f"{hole_number}B")

            if self.transparent[hole_index] > 0:
                valid_moves.append(f"{hole_number}TR")
                valid_moves.append(f"{hole_number}TB")

        return valid_moves

    def get_board_state(self) -> dict:
        """Retourne l'état du plateau pour affichage/debug"""
        return {
            'red': self.red[:],
            'blue': self.blue[:],
            'transparent': self.transparent[:],
            'score': self.score[:],
            'current_player': self.current_player
        }


class AIBot:
    """Bot IA pour jouer contre la plateforme awale-arena"""

    def __init__(self, depth: int = 4):
        """
        Initialise le bot avec une profondeur de recherche
        depth: profondeur de l'arbre de recherche (2-4 recommandé pour la plateforme)
        """
        self.depth = depth
        self.game = AwaleGame()

    def evaluate_position(self, game_state: dict, player: int) -> float:
        """
        Évalue une position pour un joueur
        Score positif = avantage pour le joueur
        Score négatif = avantage pour l'adversaire
        """
        opponent = 1 - player

        # Différence de score (poids: 10)
        score = (game_state['score'][player] - game_state['score'][opponent]) * 10

        # Différence de graines sur le plateau (poids: 2)
        player_seeds = 0
        opponent_seeds = 0

        player_holes = self._get_player_holes(player)
        opponent_holes = self._get_player_holes(opponent)

        for hole_idx in player_holes:
            player_seeds += (game_state['red'][hole_idx] +
                           game_state['blue'][hole_idx] +
                           game_state['transparent'][hole_idx])

        for hole_idx in opponent_holes:
            opponent_seeds += (game_state['red'][hole_idx] +
                             game_state['blue'][hole_idx] +
                             game_state['transparent'][hole_idx])

        score += (player_seeds - opponent_seeds) * 2

        return float(score)

    def minimax(self, game: AwaleGame, player: int, depth: int,
                alpha: float = float('-inf'), beta: float = float('inf')) -> Tuple[float, Optional[str]]:
        """
        Algorithme Minimax avec Alpha-Beta Pruning
        """
        # État terminal
        if depth == 0:
            return self.evaluate_position(game.get_board_state(), player), None

        current_player = game.current_player

        if current_player == player:
            # Nœud maximisant
            max_eval = float('-inf')
            best_move = None

            moves = game.get_valid_moves(player)

            for move in moves:
                # Créer une copie du jeu
                game_copy = self._copy_game(game)
                game_copy.apply_move(move)

                eval_score, _ = self.minimax(game_copy, player, depth - 1, alpha, beta)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move

                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff

            return max_eval, best_move
        else:
            # Nœud minimisant
            min_eval = float('inf')
            best_move = None

            opponent = 1 - player
            moves = game.get_valid_moves(opponent)

            for move in moves:
                # Créer une copie du jeu
                game_copy = self._copy_game(game)
                game_copy.apply_move(move)

                eval_score, _ = self.minimax(game_copy, player, depth - 1, alpha, beta)

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move

                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff

            return min_eval, best_move

    def get_move(self, game: AwaleGame, player: int) -> Optional[str]:
        """Retourne le meilleur coup selon minimax"""
        _, move = self.minimax(game, player, self.depth)

        if move is None:
            # Fallback: prendre un coup aléatoire valide
            valid_moves = game.get_valid_moves(player)
            if valid_moves:
                return random.choice(valid_moves)

        return move

    def _copy_game(self, game: AwaleGame) -> AwaleGame:
        """Crée une copie profonde du jeu"""
        new_game = AwaleGame()
        new_game.red = game.red[:]
        new_game.blue = game.blue[:]
        new_game.transparent = game.transparent[:]
        new_game.score = game.score[:]
        new_game.current_player = game.current_player
        return new_game

    @staticmethod
    def _get_player_holes(player: int) -> List[int]:
        """Retourne les indices des trous d'un joueur"""
        if player == 0:
            return [i for i in range(16) if i % 2 == 0]
        else:
            return [i for i in range(16) if i % 2 == 1]


def main():
    """
    Fonction principale pour interfacer avec awale-arena
    Lire depuis stdin, traiter les mouvements, envoyer les réponses
    """
    # Récupérer le numéro du joueur (1 ou 2)
    my_player = int(sys.argv[1]) - 1  # Convertir en 0 ou 1

    # Initialiser le jeu et le bot
    game = AwaleGame()
    bot = AIBot(depth=3)  # Profondeur 3 pour un bon équilibre vitesse/qualité

    # Boucle principale
    for line in sys.stdin:
        move = line.strip()

        # Traiter les signaux spéciaux
        if move == "END":
            break

        if move != "START":
            # Appliquer le coup de l'adversaire
            game.apply_move(move)

        # Obtenir les mouvements valides
        valid_moves = game.get_valid_moves(my_player)

        if valid_moves:
            # Utiliser le bot pour calculer le meilleur coup
            my_move = bot.get_move(game, my_player)

            if my_move is None:
                my_move = random.choice(valid_moves)
        else:
            # Aucun coup valide (normalement ne devrait pas arriver ici)
            my_move = "???"

        # Appliquer notre coup
        game.apply_move(my_move)

        # Envoyer le coup à la plateforme
        sys.stdout.write(my_move + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
