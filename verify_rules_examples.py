"""
Verify the exact examples from the Rules2025 document
"""

class GameVerifier:
    def __init__(self, custom_setup=None):
        self.holes = {}
        for i in range(1, 17):
            self.holes[i] = {'R': 0, 'B': 0, 'T': 0}
        if custom_setup:
            for hole, seeds in custom_setup.items():
                self.holes[hole] = seeds.copy()
        self.captured = {1: 0, 2: 0}
        
    def get_player_holes(self, player):
        if player == 1:
            return [h for h in range(1, 17) if h % 2 == 1]
        else:
            return [h for h in range(1, 17) if h % 2 == 0]
    
    def get_total_seeds(self, hole):
        return self.holes[hole]['R'] + self.holes[hole]['B'] + self.holes[hole]['T']
    
    def print_board(self, holes_to_show=None):
        if holes_to_show is None:
            holes_to_show = range(1, 17)
        for i in holes_to_show:
            h = self.holes[i]
            total = self.get_total_seeds(i)
            parts = []
            if h['R'] > 0: parts.append(f"{h['R']}R")
            if h['B'] > 0: parts.append(f"{h['B']}B")
            if h['T'] > 0: parts.append(f"{h['T']}T")
            seeds_str = ' '.join(parts) if parts else "empty"
            print(f"  Hole {i}: ({seeds_str}) total={total}")
    
    def apply_move(self, move_str, player):
        move_str = move_str.strip().upper()
        
        if 'T' in move_str and len(move_str) >= 3:
            hole = int(move_str[:-2])
            color = 'T'
            trans_as = move_str[-1]
        else:
            hole = int(move_str[:-1])
            color = move_str[-1]
            trans_as = None
        
        # Get seeds to distribute
        if color == 'T':
            trans_seeds = self.holes[hole]['T']
            color_seeds = self.holes[hole][trans_as]
            self.holes[hole]['T'] = 0
            self.holes[hole][trans_as] = 0
            distribution_rule = trans_as
        else:
            trans_seeds = 0
            color_seeds = self.holes[hole][color]
            self.holes[hole][color] = 0
            distribution_rule = color
        
        # Build list of seeds to place
        if color == 'T':
            # Transparent distributed FIRST, then colored
            seeds_to_place = ['T'] * trans_seeds + [trans_as] * color_seeds
        else:
            seeds_to_place = [color] * color_seeds
        
        current = hole
        last_hole = None
        
        print(f"\n  Distributing {len(seeds_to_place)} seeds: {seeds_to_place}")
        print(f"  Distribution rule: {distribution_rule} ({'all holes' if distribution_rule == 'R' else 'opponent holes only'})")
        
        for seed_type in seeds_to_place:
            current = (current % 16) + 1
            
            # Skip source hole
            if current == hole:
                current = (current % 16) + 1
            
            if distribution_rule == 'R':
                self.holes[current][seed_type] += 1
                print(f"    -> Seed {seed_type} to hole {current}")
                last_hole = current
            else:
                # Blue: only opponent holes
                opponent_holes = self.get_player_holes(3 - player)
                while current not in opponent_holes:
                    current = (current % 16) + 1
                    if current == hole:
                        current = (current % 16) + 1
                self.holes[current][seed_type] += 1
                print(f"    -> Seed {seed_type} to hole {current} (opponent hole)")
                last_hole = current
        
        # Capture
        if last_hole is not None:
            self.do_captures(last_hole, player)
        
        return last_hole
    
    def do_captures(self, last_hole, player):
        # IMPORTANT: Capture goes backwards and CAN capture from ANY hole
        # including the player's own holes!
        # The rule says: "it is allowed to take the seeds from its own hole"
        
        current = last_hole
        captured_holes = []
        
        # Keep capturing while we have 2 or 3 seeds
        while True:
            total = self.get_total_seeds(current)
            
            if total == 2 or total == 3:
                captured_holes.append((current, total))
                self.captured[player] += total
                self.holes[current] = {'R': 0, 'B': 0, 'T': 0}
                
                # Move backwards (counter-clockwise)
                current = current - 1
                if current < 1:
                    current = 16
            else:
                break
        
        if captured_holes:
            print(f"  CAPTURE from holes {captured_holes}: total {sum(c[1] for c in captured_holes)} seeds")


def test_case_1():
    """
    Case 1 from rules:
    1 (2R)
    16 (2R)  15 (2B) 14 (2B2R) 13 (2R2B)
    
    Player even plays 14 B
    Expected result: holes 1, 16, 15, 14 are captured (10 seeds)
    """
    print("=" * 60)
    print("TEST CASE 1 from Rules")
    print("=" * 60)
    
    setup = {
        1: {'R': 2, 'B': 0, 'T': 0},
        13: {'R': 2, 'B': 2, 'T': 0},
        14: {'R': 2, 'B': 2, 'T': 0},
        15: {'R': 0, 'B': 2, 'T': 0},
        16: {'R': 2, 'B': 0, 'T': 0},
    }
    # Fill rest with zeros
    for i in range(2, 13):
        setup[i] = {'R': 0, 'B': 0, 'T': 0}
    
    game = GameVerifier(setup)
    
    print("\nInitial state:")
    game.print_board([1, 13, 14, 15, 16])
    
    print("\nPlayer 2 (even) plays 14B")
    # Blue seeds from hole 14 go only to odd holes (player 1's holes)
    # 2 blue seeds: go to holes 15, 1 (but 15 is even! so skip to next odd)
    # Wait - player 2 has even holes, so opponent (player 1) has odd holes
    # Blue from 14 goes to: 15 is odd (yes), 1 is odd (yes) 
    # But wait, let me re-read: Player 2 has EVEN holes, Player 1 has ODD holes
    # So Player 2's opponent holes are ODD holes
    
    game.apply_move("14B", 2)
    
    print("\nResult:")
    game.print_board([1, 13, 14, 15, 16])
    print(f"\nPlayer 2 captured: {game.captured[2]} seeds")
    
    # According to rules, result should be 10 seeds captured
    expected = 10
    if game.captured[2] == expected:
        print(f"✓ CORRECT: Captured {expected} seeds as expected")
    else:
        print(f"✗ ERROR: Expected {expected}, got {game.captured[2]}")


def test_case_2_1():
    """
    Case 2.1 from rules:
    1 (1R) 2 (2R) 3(1B) 4(2B) 5(1R)
    16 (3B1R) 15 (2R) 14 (4B)
    
    Player even plays 16B
    Expected: holes 5,4,3,2,1 captured = 10 seeds
    """
    print("\n" + "=" * 60)
    print("TEST CASE 2.1 from Rules")
    print("=" * 60)
    
    setup = {
        1: {'R': 1, 'B': 0, 'T': 0},
        2: {'R': 2, 'B': 0, 'T': 0},
        3: {'R': 0, 'B': 1, 'T': 0},
        4: {'R': 0, 'B': 2, 'T': 0},
        5: {'R': 1, 'B': 0, 'T': 0},
        14: {'R': 0, 'B': 4, 'T': 0},
        15: {'R': 2, 'B': 0, 'T': 0},
        16: {'R': 1, 'B': 3, 'T': 0},
    }
    for i in [6,7,8,9,10,11,12,13]:
        setup[i] = {'R': 0, 'B': 0, 'T': 0}
    
    game = GameVerifier(setup)
    
    print("\nInitial state:")
    game.print_board([1,2,3,4,5,14,15,16])
    
    print("\nPlayer 2 (even) plays 16B")
    # 3 Blue seeds from hole 16
    # Blue goes only to opponent (odd) holes: 1, 3, 5
    game.apply_move("16B", 2)
    
    print("\nResult:")
    game.print_board([1,2,3,4,5,14,15,16])
    print(f"\nPlayer 2 captured: {game.captured[2]} seeds")
    
    expected = 10
    if game.captured[2] == expected:
        print(f"✓ CORRECT: Captured {expected} seeds as expected")
    else:
        print(f"✗ ERROR: Expected {expected}, got {game.captured[2]}")


def test_case_2_2():
    """
    Case 2.2 from rules:
    1 (1R) 2 (2R) 3(1B) 4(2B) 5(1R)
    16 (3B1R) 15 (2R) 14 (4B)
    
    Player even plays 16R
    Expected: holes 1, 16, 15 captured = 7 seeds
    """
    print("\n" + "=" * 60)
    print("TEST CASE 2.2 from Rules")
    print("=" * 60)
    
    setup = {
        1: {'R': 1, 'B': 0, 'T': 0},
        2: {'R': 2, 'B': 0, 'T': 0},
        3: {'R': 0, 'B': 1, 'T': 0},
        4: {'R': 0, 'B': 2, 'T': 0},
        5: {'R': 1, 'B': 0, 'T': 0},
        14: {'R': 0, 'B': 4, 'T': 0},
        15: {'R': 2, 'B': 0, 'T': 0},
        16: {'R': 1, 'B': 3, 'T': 0},
    }
    for i in [6,7,8,9,10,11,12,13]:
        setup[i] = {'R': 0, 'B': 0, 'T': 0}
    
    game = GameVerifier(setup)
    
    print("\nInitial state:")
    game.print_board([1,2,3,4,5,14,15,16])
    
    print("\nPlayer 2 (even) plays 16R")
    # 1 Red seed from hole 16, goes to all holes: next is 1
    game.apply_move("16R", 2)
    
    print("\nResult:")
    game.print_board([1,2,3,4,5,14,15,16])
    print(f"\nPlayer 2 captured: {game.captured[2]} seeds")
    
    expected = 7
    if game.captured[2] == expected:
        print(f"✓ CORRECT: Captured {expected} seeds as expected")
    else:
        print(f"✗ ERROR: Expected {expected}, got {game.captured[2]}")


if __name__ == "__main__":
    test_case_1()
    test_case_2_1()
    test_case_2_2()
