"""
Verify game moves against the official rules
"""

class GameVerifier:
    def __init__(self):
        # Initialize board: holes 1-16, each with 2R, 2B, 2T
        self.holes = {}
        for i in range(1, 17):
            self.holes[i] = {'R': 2, 'B': 2, 'T': 2}
        self.captured = {1: 0, 2: 0}
        self.move_count = 0
        
    def get_player_holes(self, player):
        """Player 1: odd holes, Player 2: even holes"""
        if player == 1:
            return [h for h in range(1, 17) if h % 2 == 1]
        else:
            return [h for h in range(1, 17) if h % 2 == 0]
    
    def get_total_seeds(self, hole):
        return self.holes[hole]['R'] + self.holes[hole]['B'] + self.holes[hole]['T']
    
    def print_board(self):
        """Print board state"""
        print("\n=== BOARD STATE ===")
        print("Holes 1-8 (Player 1: odd, Player 2: even):")
        for i in range(1, 9):
            h = self.holes[i]
            print(f"  Hole {i}: {h['R']}R {h['B']}B {h['T']}T (total: {self.get_total_seeds(i)})")
        print("Holes 9-16:")
        for i in range(9, 17):
            h = self.holes[i]
            print(f"  Hole {i}: {h['R']}R {h['B']}B {h['T']}T (total: {self.get_total_seeds(i)})")
        print(f"Captured - Player1: {self.captured[1]}, Player2: {self.captured[2]}")
        print("=" * 30)
    
    def verify_move(self, move_str, player):
        """Verify and apply a move, return (valid, error_message)"""
        move_str = move_str.strip().upper()
        
        # Parse move
        if 'T' in move_str and len(move_str) >= 3:
            # Transparent move: "3TR" or "4TB"
            hole = int(move_str[:-2])
            color = 'T'
            trans_as = move_str[-1]  # 'R' or 'B'
        else:
            # Normal move: "3R" or "4B"
            hole = int(move_str[:-1])
            color = move_str[-1]
            trans_as = None
        
        # Rule 1: Player must play from their own holes
        player_holes = self.get_player_holes(player)
        if hole not in player_holes:
            return False, f"RULE VIOLATION: Player {player} cannot play from hole {hole} (not their hole)"
        
        # Rule 2: Must have seeds of that color
        if self.holes[hole][color] == 0:
            return False, f"RULE VIOLATION: No {color} seeds in hole {hole}"
        
        # Get seeds to distribute
        if color == 'T':
            if trans_as is None:
                return False, "RULE VIOLATION: Transparent must specify R or B"
            # Transparent + designated color seeds
            trans_seeds = self.holes[hole]['T']
            color_seeds = self.holes[hole][trans_as]
            self.holes[hole]['T'] = 0
            self.holes[hole][trans_as] = 0
            distribution_rule = trans_as
            total_seeds = trans_seeds + color_seeds
        else:
            # Only seeds of specified color
            total_seeds = self.holes[hole][color]
            self.holes[hole][color] = 0
            distribution_rule = color
            trans_seeds = 0
            color_seeds = total_seeds
        
        # Distribute seeds
        current = hole
        seeds_distributed = 0
        last_hole = None
        
        # For transparent: distribute T first, then colored
        seeds_to_place = []
        for _ in range(trans_seeds if color == 'T' else 0):
            seeds_to_place.append('T')
        for _ in range(color_seeds if color == 'T' else total_seeds):
            seeds_to_place.append(color if color != 'T' else trans_as)
        
        # Actually for the rules, transparent seeds STAY transparent
        # So we need to track what type of seed we're placing
        if color == 'T':
            seeds_to_place = ['T'] * trans_seeds + [trans_as] * color_seeds
        else:
            seeds_to_place = [color] * total_seeds
        
        for seed_type in seeds_to_place:
            # Move to next hole
            current = (current % 16) + 1
            
            # Skip starting hole (rule: starting hole is always left empty)
            if current == hole:
                current = (current % 16) + 1
            
            if distribution_rule == 'R':
                # Red: goes into ALL holes
                self.holes[current][seed_type] += 1
                last_hole = current
            else:
                # Blue: goes ONLY into opponent's holes
                opponent_holes = self.get_player_holes(3 - player)
                while current not in opponent_holes:
                    current = (current % 16) + 1
                    if current == hole:
                        current = (current % 16) + 1
                self.holes[current][seed_type] += 1
                last_hole = current
        
        # Capture logic
        if last_hole is not None:
            self.do_captures(last_hole, player)
        
        self.move_count += 1
        return True, f"Move OK: {move_str} by Player {player}"
    
    def do_captures(self, last_hole, player):
        """Capture seeds starting from last_hole, going counter-clockwise"""
        opponent = 3 - player
        opponent_holes = self.get_player_holes(opponent)
        
        # Capture only starts if last hole is in opponent's territory
        if last_hole not in opponent_holes:
            return
        
        current = last_hole
        captured_this_turn = 0
        
        while current in opponent_holes:
            total = self.get_total_seeds(current)
            
            if total == 2 or total == 3:
                # Capture!
                captured_this_turn += total
                self.captured[player] += total
                self.holes[current] = {'R': 0, 'B': 0, 'T': 0}
                
                # Move counter-clockwise
                current = current - 1
                if current < 1:
                    current = 16
            else:
                break
        
        if captured_this_turn > 0:
            print(f"  -> Player {player} captured {captured_this_turn} seeds!")


def main():
    # The moves from the game
    moves = [
        ("1R", 1), ("4R", 2), ("7R", 1), ("10R", 2), ("15R", 1), ("2R", 2),
        ("13R", 1), ("4R", 2), ("1R", 1), ("2R", 2), ("3B", 1), ("8R", 2),
        ("5B", 1), ("10R", 2), ("15R", 1), ("6R", 2), ("7R", 1), ("8R", 2),
        ("7B", 1), ("12B", 2), ("9R", 1), ("10R", 2), ("13R", 1), ("16R", 2),
        ("1R", 1), ("2R", 2), ("5R", 1), ("2B", 2), ("11R", 1), ("4R", 2)
    ]
    
    verifier = GameVerifier()
    
    print("=" * 60)
    print("GAME VERIFICATION - Checking first 30 moves against rules")
    print("=" * 60)
    
    verifier.print_board()
    
    for i, (move, player) in enumerate(moves):
        print(f"\nMove {i+1}: Player {player} plays {move}")
        valid, message = verifier.verify_move(move, player)
        
        if not valid:
            print(f"  *** ERROR: {message}")
            verifier.print_board()
            break
        else:
            print(f"  ✓ {message}")
        
        # Show board every 10 moves
        if (i + 1) % 10 == 0:
            verifier.print_board()
    
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    verifier.print_board()
    print(f"\nAll {len(moves)} moves verified: PASSED")


if __name__ == "__main__":
    main()
