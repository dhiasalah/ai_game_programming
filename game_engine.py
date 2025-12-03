"""
Moteur de jeu Mancala - Version CORRIGÉE avec règles complètes de capture
Les graines transparentes sont distribuées AVANT les autres graines de la couleur désignée
"""

from game_rules import GameState, Color
from typing import List, Tuple, Set

class GameEngine:
    """Moteur de jeu qui gère l'exécution des coups"""

    def __init__(self, game_state: GameState):
        self.state = game_state
        self.debug = False  # Mettre à True pour voir le détail des captures

    def next_hole(self, current_hole: int) -> int:
        """Retourne le trou suivant en sens horaire"""
        if current_hole == 16:
            return 1
        else:
            return current_hole + 1

    def prev_hole(self, current_hole: int) -> int:
        """Retourne le trou précédent (sens anti-horaire)"""
        if current_hole == 1:
            return 16
        else:
            return current_hole - 1

    def is_opponent_hole(self, hole: int, player: int) -> bool:
        """Vérifie si un trou appartient à l'adversaire"""
        player_holes = self.state.get_player_holes(player)
        return hole not in player_holes

    def play_move(self, hole: int, color: Color, transparent_as: Color = None) -> bool:
        """
        Exécute un coup avec les règles complètes :
        - Si les graines sont rouges : distribuées dans tous les trous
        - Si les graines sont bleues : distribuées uniquement dans les trous adverses
        - Si transparentes : jouées comme la couleur désignée
        - Les graines transparentes sont TOUJOURS distribuées EN PREMIER
        - Le trou initial reste vide pour la couleur sélectionnée

        hole: numéro du trou
        color: couleur sélectionnée
        transparent_as: Red ou Blue si la couleur est Transparent
        """
        player = self.state.current_player

        # Vérification de validité
        if self.state.holes[hole][color] == 0:
            return False

        if hole not in self.state.get_player_holes(player):
            return False

        if color == Color.TRANSPARENT and transparent_as is None:
            return False

        # Déterminer les graines à distribuer
        if color == Color.TRANSPARENT:
            # Les graines transparentes seront distribuées comme la couleur désignée
            transparent_seeds = self.state.holes[hole][Color.TRANSPARENT]
            actual_color = transparent_as
            self.state.holes[hole][Color.TRANSPARENT] = 0

            # Les autres graines de la couleur désignée
            other_seeds = self.state.holes[hole][actual_color]
            self.state.holes[hole][actual_color] = 0
        else:
            # Pas de graines transparentes
            transparent_seeds = 0
            actual_color = color
            other_seeds = self.state.holes[hole][color]
            self.state.holes[hole][color] = 0

        # Total des graines à distribuer
        total_seeds = transparent_seeds + other_seeds
        current_hole = hole
        last_hole_seeded = None

        if self.debug:
            print(f"\n[DEBUG] Joueur {player} joue trou {hole}, couleur {actual_color.value}")
            print(f"[DEBUG] Graines transparentes: {transparent_seeds}, autres: {other_seeds}")

        # ========== PHASE 1 : Distribuer les graines TRANSPARENTES EN PREMIER ==========
        seeds_remaining = transparent_seeds

        while seeds_remaining > 0:
            current_hole = self.next_hole(current_hole)

            # Distribution selon la couleur désignée
            if actual_color == Color.RED:
                # Les graines vont dans tous les trous (distribuées comme TRANSPARENT)
                self.state.holes[current_hole][Color.TRANSPARENT] += 1
                last_hole_seeded = current_hole
                if self.debug:
                    print(f"[DEBUG] Graine transparente -> Trou {current_hole}")
                seeds_remaining -= 1

            elif actual_color == Color.BLUE:
                # Les graines vont uniquement dans les trous adverses (distribuées comme TRANSPARENT)
                if self.is_opponent_hole(current_hole, player):
                    self.state.holes[current_hole][Color.TRANSPARENT] += 1
                    last_hole_seeded = current_hole
                    if self.debug:
                        print(f"[DEBUG] Graine transparente -> Trou adversaire {current_hole}")
                    seeds_remaining -= 1

        # ========== PHASE 2 : Distribuer les AUTRES graines de la couleur désignée ==========
        seeds_remaining = other_seeds

        while seeds_remaining > 0:
            current_hole = self.next_hole(current_hole)

            # Distribution selon la couleur
            if actual_color == Color.RED:
                # Les rouges vont dans tous les trous
                self.state.holes[current_hole][actual_color] += 1
                last_hole_seeded = current_hole
                if self.debug:
                    print(f"[DEBUG] Graine {actual_color.value} -> Trou {current_hole}")
                seeds_remaining -= 1

            elif actual_color == Color.BLUE:
                # Les bleus vont uniquement dans les trous adverses
                if self.is_opponent_hole(current_hole, player):
                    self.state.holes[current_hole][actual_color] += 1
                    last_hole_seeded = current_hole
                    if self.debug:
                        print(f"[DEBUG] Graine {actual_color.value} -> Trou adversaire {current_hole}")
                    seeds_remaining -= 1

        # Capture à partir du dernier trou semé (si une graine a été semée)
        if last_hole_seeded is not None:
            self._capture_seeds(last_hole_seeded, player)

        # Changement de joueur
        self.state.current_player = 3 - player  # Alterne entre 1 et 2

        return True

    def _capture_seeds(self, last_hole: int, player: int):
        """
        Gère la capture des graines
        Règles :
        - La capture commence UNIQUEMENT si le dernier trou semé est dans les trous adverses
        - Remonte en arrière en sens anti-horaire, uniquement dans les trous de l'adversaire
        - Capture les trous avec exactement 2 ou 3 graines (toutes couleurs confondues)
        - S'arrête dès qu'on rencontre un trou qui n'a pas 2-3 graines
        """
        opponent = 3 - player
        opponent_holes = self.state.get_player_holes(opponent)

        # La capture ne s'effectue que si le dernier trou semé est dans les trous adverses
        if last_hole not in opponent_holes:
            if self.debug:
                print(f"[DEBUG] Pas de capture - le dernier trou semé {last_hole} n'est pas un trou adverse")
            return

        if self.debug:
            print(f"[DEBUG] Vérification de capture en partant du trou {last_hole}")

        current_hole = last_hole
        captured_total = 0

        # Remonte en arrière en sens anti-horaire, uniquement dans les trous de l'adversaire
        while current_hole in opponent_holes:
            total_seeds = self.state.get_total_seeds(current_hole)

            if self.debug:
                print(f"[DEBUG] Trou {current_hole}: {total_seeds} graines")

            if total_seeds == 2 or total_seeds == 3:
                # Capture ce trou
                seeds_captured = total_seeds
                captured_total += seeds_captured

                if self.debug:
                    print(f"[DEBUG] ✓ Capture du trou {current_hole} ({seeds_captured} graines)")

                # Réinitialise le trou
                for col in Color:
                    self.state.holes[current_hole][col] = 0

                self.state.captured_seeds[player] += seeds_captured

                # Continue vers le trou précédent
                current_hole = self.prev_hole(current_hole)
            else:
                # Arrête la capture
                if self.debug:
                    print(f"[DEBUG] ✗ Fin de capture - le trou {current_hole} n'a pas 2-3 graines ({total_seeds})")
                break

        if self.debug and captured_total > 0:
            print(f"[DEBUG] Total capturé: {captured_total} graines")

    def get_board_state_string(self) -> str:
        """Retourne une représentation lisible du plateau"""
        return str(self.state)


class MoveGenerator:
    """Générateur de mouvements pour l'IA"""

    @staticmethod
    def get_all_moves(state: GameState, player: int) -> List[Tuple[int, Color, Color]]:
        """
        Génère tous les coups possibles pour un joueur
        Retourne: (hole, color_to_play, transparent_as_color)
        transparent_as_color est None si color_to_play n'est pas Transparent
        """
        moves = []

        for hole in state.get_player_holes(player):
            for color in Color:
                if state.holes[hole][color] > 0:
                    if color == Color.TRANSPARENT:
                        # Les graines transparentes peuvent être jouées comme rouge ou bleu
                        moves.append((hole, color, Color.RED))
                        moves.append((hole, color, Color.BLUE))
                    else:
                        moves.append((hole, color, None))

        return moves

    @staticmethod
    def apply_move(state: GameState, hole: int, color: Color, transparent_as: Color = None) -> GameState:
        """
        Applique un coup à un état et retourne le nouvel état
        """
        new_state = state.copy()
        engine = GameEngine(new_state)
        engine.play_move(hole, color, transparent_as)
        return new_state

