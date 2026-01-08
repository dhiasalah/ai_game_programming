"""
Debug test to find where state diverges between Arbitre and bot
"""

from game_rules import GameState, Color
from game_engine import GameEngine

# Replay the game moves to find divergence point
moves = [
    ("1R", 1), ("4R", 2), ("7R", 1), ("10R", 2), ("15R", 1), ("2R", 2),
    ("13R", 1), ("4R", 2), ("1R", 1), ("2R", 2), ("3B", 1), ("8R", 2),
    ("5B", 1), ("10R", 2), ("15R", 1), ("6R", 2), ("7R", 1), ("8R", 2),
    ("7B", 1), ("12B", 2), ("9R", 1), ("10R", 2), ("13R", 1), ("16R", 2),
    ("1R", 1), ("2R", 2), ("5R", 1), ("2B", 2), ("11R", 1), ("4R", 2),
    ("1R", 1), ("2R", 2), ("3B", 1), ("6R", 2), ("5R", 1), ("6R", 2),
    ("9R", 1), ("10R", 2), ("11R", 1), ("8R", 2), ("9R", 1), ("16R", 2),
    ("13R", 1), ("10R", 2), ("1R", 1), ("2R", 2), ("11R", 1), ("16B", 2),
    ("3B", 1), ("14B", 2), ("15R", 1), ("16R", 2), ("1R", 1), ("2R", 2),
    ("7R", 1), ("8R", 2), ("9R", 1), ("10R", 2), ("11R", 1), ("10B", 2),
    ("11B", 1), ("12B", 2), ("13R", 1), ("14B", 2), ("15B", 1), ("16B", 2),
    ("1B", 1), ("10B", 2), ("9B", 1), ("10B", 2), ("11B", 1), ("12B", 2),
    ("3R", 1), ("10R", 2), ("5R", 1), ("8B", 2), ("7R", 1), ("6R", 2),
    ("7R", 1), ("4R", 2), ("13R", 1), ("14R", 2), ("1R", 1), ("4R", 2),
    ("15R", 1), ("6R", 2), ("7R", 1), ("6B", 2), ("11B", 1), ("12B", 2),
    ("3R", 1), ("8R", 2), ("7B", 1), ("14R", 2), ("1B", 1), ("10R", 2),
    ("13B", 1), ("8B", 2), ("9B", 1), ("6B", 2), ("7B", 1)  # This fails!
]

def parse_move(move_str):
    move_str = move_str.strip().upper()
    if 'T' in move_str and len(move_str) >= 3:
        hole = int(move_str[:-2])
        color = Color.TRANSPARENT
        trans_as = Color.RED if move_str[-1] == 'R' else Color.BLUE
        return hole, color, trans_as
    else:
        hole = int(move_str[:-1])
        color = Color.RED if move_str[-1] == 'R' else Color.BLUE
        return hole, color, None

state = GameState()
engine = GameEngine(state)
engine.debug = False

print("Replaying moves...")
for i, (move_str, player) in enumerate(moves):
    hole, color, trans_as = parse_move(move_str)
    
    # Check if move is valid BEFORE applying
    player_holes = state.get_player_holes(player)
    if hole not in player_holes:
        print(f"\nMove {i+1}: {move_str} by Player {player}")
        print(f"  ERROR: Hole {hole} does not belong to Player {player}")
        print(f"  Player {player} holes: {player_holes}")
        break
    
    if state.holes[hole][color] == 0:
        print(f"\nMove {i+1}: {move_str} by Player {player}")
        print(f"  ERROR: No {color.value} seeds in hole {hole}")
        print(f"  Hole {hole} contents: R={state.holes[hole][Color.RED]}, B={state.holes[hole][Color.BLUE]}, T={state.holes[hole][Color.TRANSPARENT]}")
        break
    
    # Force the player
    state.current_player = player
    
    # Apply move
    success = engine.play_move(hole, color, trans_as)
    
    if not success:
        print(f"\nMove {i+1}: {move_str} by Player {player}")
        print(f"  ERROR: Move failed!")
        break
    
    print(f"Move {i+1}: {move_str} OK - Captured: P1={state.captured_seeds[1]}, P2={state.captured_seeds[2]}")

print(f"\nFinal state:")
print(f"Captured: Player1={state.captured_seeds[1]}, Player2={state.captured_seeds[2]}")
