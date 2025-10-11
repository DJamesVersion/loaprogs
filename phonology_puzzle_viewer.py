import sys

def get_phonology_map():
    """
    Defines the letter-to-phonology mapping provided by the user.
    Uses the primary substitution for consistency.
    """
    mapping = {
        'a': 'ariatnah', 'b': 'batobwatchaeh', 'c': "c'illiatnah", 'd': 'diadowatchaeh',
        'e': 'eecheechuwah', 'f': "f'illianarre", 'g': 'gagoikenne', 'h': "h'uilliatachaeh",
        'i': 'illianarre', 'j': 'ampejinne', 'k': 'kajoinkenne', 'l': 'lenemketobontette',
        'm': 'momaw', 'n': 'nona', 'o': 'oichenne', 'p': 'perfuvium',
        'q': 'quaristenne', 'r': 'roykenne', 's': 'stihuu', 't': 'tetnobautte',
        'u': 'uilliatachaeh', 'v': 'vraelvrae', 'w': 'weetus', 'x': 'xiangxong',
        'y': "y'uilliatachaeh", 'z': 'zazoykenne'
    }
    # Add exceptions for specific words in the original puzzles
    mapping['T'] = 'Tahkmahnelle' # Specific word override for Puzzle 2
    return mapping

def encode_puzzle(original_text, phonology_map):
    """
    Encodes the original text using the phonology map.
    Preserves non-alphabetic characters.
    """
    encoded_parts = []
    
    # Simple tokenization for the very long Puzzle 7
    if len(original_text.split()) > 10:
        words = original_text.lower().split()
        for word in words:
            encoded_word = []
            for char in word:
                if 'a' <= char <= 'z':
                    encoded_word.append(phonology_map.get(char, char))
                elif char == 't' and 'Tahkmahnelle' in original_text:
                    # Special case for Tahkmahnelle in Puzzle 2 (not used here, but good practice)
                    encoded_word.append('Tahkmahnelle')
                else:
                    encoded_word.append(char)
            encoded_parts.append(' '.join(encoded_word))
        return ', '.join(encoded_parts)
    
    # Process for shorter, more coded strings
    for char in original_text:
        if 'a' <= char.lower() <= 'z':
            # Handle specific letter overrides, like 'T' in Tahkmahnelle
            if char == 'T':
                encoded_parts.append(phonology_map.get('T', char))
            else:
                encoded_parts.append(phonology_map.get(char.lower(), char))
        else:
            encoded_parts.append(char)
            
    # For coded strings, join without spaces to maintain original structure integrity
    return ''.join(encoded_parts)

def get_puzzle_data():
    """
    Defines the 8 original puzzles and encodes them using the phonology map.
    """
    phonology_map = get_phonology_map()
    
    # Original Puzzles
    original_puzzles = {
        '1': {'title': 'Numerical Cipher 1', 'content': '22211000_1218213235/9298011215'},
        '2': {'title': 'The Song of Tahkmahnelle', 'content': 'cynus song of Tahkmahnelle'},
        '3': {'title': 'Alphanumeric Code', 'content': 'aadd/abheaa_ehd9'},
        '4': {'title': 'Field of Purity Guardian Caravan', 'content': 'haran padan aram - field of purity guardian caravan'},
        '5': {'title': 'Algebraic Constraint', 'content': 'x=abcd (k^46)'},
        '6': {'title': 'The Lands of Ages Roster', 'content': 'heromen of lands of ages_super mutant_hyper man_mega hero_turbo man'},
        '7': {'title': 'The Cryptic Shopping List', 'content': 'bunnies and rainbows, youth in Asia, blister fist, blue hero, grass blues, od duck, your favorite vegetable, giraffe in the jug full of jelly'},
        '8': {'title': 'The Final Sequence', 'content': '62112111'}
    }

    # Encoded Puzzles and New Hints
    puzzles_data = {}
    for num, data in original_puzzles.items():
        encoded_content = encode_puzzle(data['content'], phonology_map)
        
        # New hints focus on translating the phonology back to the original alphabet.
        new_hint = (
            f"This puzzle uses the letter-to-word phonology cipher. "
            f"The challenge is to match each long word (e.g., '{phonology_map['a']}') "
            f"back to its single starting letter ('a') to reconstruct the original message/code. "
            f"Pay special attention to the unique structure created by the non-alphabetic characters."
        )

        puzzles_data[num] = {
            'title': f"Phonology Encoded: {data['title']}",
            'content': encoded_content,
            'hint': new_hint
        }
    
    # Create a simplified map for the menu display
    menu_map = {k: v['title'] for k, v in puzzles_data.items()}
    return menu_map, puzzles_data

def display_puzzles(puzzles):
    """
    Displays the list of puzzles available to the user.
    """
    print("\n" + "="*70)
    print("PHONOLOGY-ENCODED CRYPTIC PUZZLE VIEWER")
    print("="*70)
    print("Select a puzzle number to view the full text and get a hint.")
    print("-" * 70)
    
    # Display options
    for number, title in puzzles.items():
        # Clean up the display title for better readability
        display_title = title.split(': ')[-1]
        print(f"[{number}]: {display_title}")

    print("[0]: Exit Application")
    print("-" * 70)

def run_puzzle_viewer():
    """
    Main application loop for the puzzle viewer.
    """
    menu_options, puzzles_data = get_puzzle_data()
    
    while True:
        display_puzzles(menu_options)
        
        user_input = input("Enter your selection (0-8): ").strip()
        
        if user_input == '0':
            print("\nExiting. Good luck decoding the phonological ciphers!")
            sys.exit(0)
        
        if user_input in puzzles_data:
            puzzle = puzzles_data[user_input]
            print("\n" + "#"*80)
            print(f"PUZZLE {user_input}: {puzzle['title'].upper()}")
            print("#"*80)
            print(f"Encoded Text:")
            print(f">>> {puzzle['content']}")
            print("\n--- Decoding Hint ---")
            print(f"{puzzle['hint']}")
            print("--------------------\n")
            input("Press Enter to return to the main menu...")
        else:
            print("\nInvalid selection. Please enter a number between 1 and 8, or 0 to exit.")

if __name__ == "__main__":
    run_puzzle_viewer()

