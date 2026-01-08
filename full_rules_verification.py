"""
Complete verification of game moves against ALL official rules from Rules2025.txt
"""

class RulesVerifier:
    def __init__(self):
        # Initialize board: holes 1-16, each with 2R, 2B, 2T
        self.holes = {}
        for i in range(1, 17):
            self.holes[i] = {'R': 2, 'B': 2, 'T': 2}
        self.captured = {1: 0, 2: 0}
        self.move_count = 0
        self.errors = []
        
    def get_player_holes(self, player):
        """Player 1: odd holes (1,3,5,7,9,11,13,15), Player 2: even holes (2,4,6,8,10,12,14,16)"""
        if player == 1:
            return [h for h in range(1, 17) if h % 2 == 1]
        else:
            return [h for h in range(1, 17) if h % 2 == 0]
    
    def get_total_seeds(self, hole):
        return self.holes[hole]['R'] + self.holes[hole]['B'] + self.holes[hole]['T']
    
    def get_seeds_on_board(self):
        total = 0
        for i in range(1, 17):
            total += self.get_total_seeds(i)
        return total
    
    def print_board(self):
        print("\n=== BOARD STATE ===")
        for i in range(1, 17):
            h = self.holes[i]
            owner = "P1" if i % 2 == 1 else "P2"
            print(f"  Hole {i:2d} ({owner}): {h['R']}R {h['B']}B {h['T']}T = {self.get_total_seeds(i)}")
        print(f"Captured: P1={self.captured[1]}, P2={self.captured[2]}")
        print(f"Seeds on board: {self.get_seeds_on_board()}")
        print("=" * 30)
    
    def verify_and_apply_move(self, move_str, player):
        """Verify and apply a move, checking ALL rules"""
        move_str = move_str.strip().upper()
        errors = []
        
        # Parse move
        if 'T' in move_str and len(move_str) >= 3:
            hole = int(move_str[:-2])
            color = 'T'
            trans_as = move_str[-1]
        else:
            hole = int(move_str[:-1])
            color = move_str[-1]
            trans_as = None
        
        # RULE 1: Player must play from their own holes
        player_holes = self.get_player_holes(player)
        if hole not in player_holes:
            errors.append(f"RULE VIOLATION: Player {player} cannot play from hole {hole} (owns {player_holes})")
        
        # RULE 2: Must have seeds of that color in the hole
        if self.holes[hole][color] == 0:
            errors.append(f"RULE VIOLATION: No {color} seeds in hole {hole}")
        
        # RULE 3: If transparent, must specify R or B
        if color == 'T' and trans_as is None:
            errors.append("RULE VIOLATION: Transparent must specify R or B (e.g., 3TR or 3TB)")
        
        if errors:
            return False, errors
        
        # Apply the move according to rules
        if color == 'T':
            # Transparent seeds + designated color seeds
            trans_seeds = self.holes[hole]['T']
            color_seeds = self.holes[hole][trans_as]
            self.holes[hole]['T'] = 0
            self.holes[hole][trans_as] = 0
            distribution_rule = trans_as
            # Transparent distributed FIRST, then colored
            seeds_to_place = [('T', trans_as)] * trans_seeds + [(trans_as, trans_as)] * color_seeds
        else:
            seeds_count = self.holes[hole][color]
            self.holes[hole][color] = 0
            distribution_rule = color
            seeds_to_place = [(color, color)] * seeds_count
        
        # Distribute seeds
        current = hole
        last_hole = None
        
        for seed_color, rule in seeds_to_place:
            # Move to next hole clockwise
            current = (current % 16) + 1
            
            # RULE: Skip source hole
            if current == hole:
                current = (current % 16) + 1
            
            if rule == 'R':
                # RED rule: goes into ALL holes
                self.holes[current][seed_color] += 1
                last_hole = current
            else:
                # BLUE rule: goes ONLY into opponent's holes
                opponent_holes = self.get_player_holes(3 - player)
                while current not in opponent_holes:
                    current = (current % 16) + 1
                    if current == hole:
                        current = (current % 16) + 1
                self.holes[current][seed_color] += 1
                last_hole = current
        
        # CAPTURE: from ANY hole (including own), going backwards
        captures = []
        if last_hole is not None:
            current = last_hole
            while True:
                total = self.get_total_seeds(current)
                if total == 2 or total == 3:
                    captures.append((current, total))
                    self.captured[player] += total
                    self.holes[current] = {'R': 0, 'B': 0, 'T': 0}
                    # Move counter-clockwise
                    current = current - 1
                    if current < 1:
                        current = 16
                else:
                    break
        
        self.move_count += 1
        
        return True, captures


def main():
    # All moves from the game
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
        ("13B", 1), ("8B", 2), ("9B", 1), ("6B", 2), ("7B", 1), ("2B", 2),
        ("5B", 1), ("16B", 2), ("3B", 1), ("14B", 2), ("1B", 1), ("12B", 2),
        ("13B", 1), ("2B", 2), ("3B", 1), ("14B", 2), ("15B", 1), ("16B", 2),
        ("1B", 1), ("2B", 2), ("3B", 1), ("10B", 2), ("13B", 1), ("8B", 2),
        ("11B", 1), ("6B", 2), ("9B", 1), ("4R", 2), ("7B", 1), ("10B", 2),
        ("5R", 1), ("8B", 2), ("11B", 1), ("6R", 2), ("7R", 1), ("8R", 2),
        ("9R", 1), ("10R", 2), ("13R", 1), ("12B", 2), ("9B", 1), ("10B", 2),
        ("15B", 1), ("16B", 2), ("1B", 1), ("2B", 2), ("3B", 1), ("12R", 2),
        ("1R", 1), ("4R", 2), ("7R", 1), ("14R", 2), ("9R", 1), ("4B", 2),
        ("7B", 1), ("8B", 2), ("5B", 1), ("6R", 2), ("1B", 1), ("2B", 2),
    ]
    
    verifier = RulesVerifier()
    
    print("=" * 70)
    print("COMPLETE GAME VERIFICATION AGAINST OFFICIAL RULES")
    print("=" * 70)
    
    total_errors = 0
    captures_log = []
    
    for i, (move, player) in enumerate(moves):
        valid, result = verifier.verify_and_apply_move(move, player)
        
        if not valid:
            print(f"\n❌ Move {i+1}: Player {player} plays {move}")
            for error in result:
                print(f"   ERROR: {error}")
            total_errors += 1
            verifier.print_board()
            break
        else:
            captures = result
            if captures:
                captures_log.append((i+1, player, move, captures))
                print(f"Move {i+1}: P{player} {move:4s} -> Captured {sum(c[1] for c in captures)} from holes {[c[0] for c in captures]}")
            else:
                print(f"Move {i+1}: P{player} {move:4s} -> OK")
        
        # Check game end conditions after each move
        if verifier.captured[1] >= 49:
            print(f"\n🏆 GAME OVER: Player 1 wins with {verifier.captured[1]} seeds!")
            break
        if verifier.captured[2] >= 49:
            print(f"\n🏆 GAME OVER: Player 2 wins with {verifier.captured[2]} seeds!")
            break
        if verifier.get_seeds_on_board() < 10:
            print(f"\n⚠️ GAME OVER: Less than 10 seeds on board ({verifier.get_seeds_on_board()})")
            break
    
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    print(f"Total moves verified: {verifier.move_count}")
    print(f"Total errors found: {total_errors}")
    print(f"Final score: Player 1 = {verifier.captured[1]}, Player 2 = {verifier.captured[2]}")
    print(f"Seeds remaining on board: {verifier.get_seeds_on_board()}")
    
    if total_errors == 0:
        print("\n✅ ALL MOVES ARE VALID ACCORDING TO THE OFFICIAL RULES")
    else:
        print(f"\n❌ FOUND {total_errors} RULE VIOLATIONS")
    
    # Show final board state
    verifier.print_board()


if __name__ == "__main__":
    main()
