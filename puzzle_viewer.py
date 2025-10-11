import sys

def display_puzzles(puzzles):
    """
    Displays the list of puzzles available to the user.
    """
    print("\n" + "="*50)
    print("CRYPTIC PUZZLE CHALLENGE VIEWER")
    print("="*50)
    print("Select a puzzle number to view the full text and get a hint.")
    print("-" * 50)
    
    # Display options
    for number, title in puzzles.items():
        # Clean up the display title for better readability
        display_title = title.split(' - ')[0] if ' - ' in title else title
        print(f"[{number}]: {display_title}")

    print("[0]: Exit Application")
    print("-" * 50)

def get_puzzle_data():
    """
    Defines the 8 puzzles and returns them in a dictionary.
    Puzzles are stored as {number: (title, puzzle_string, hint)}.
    """
    # The input puzzles are broken down into their key components
    puzzles_data = {
        '1': {
            'title': 'Numerical Cipher 1',
            'content': '22211000_1218213235/9298011215',
            'hint': 'This puzzle combines grouping and large numbers. Look for common base representations or unique date/serial patterns. The underscore and slash might indicate separate calculation blocks.'
        },
        '2': {
            'title': 'The Song of Tahkmahnelle',
            'content': 'cynus song of Tahkmahnelle',
            'hint': 'This likely points to an anagram, a reference to a fictional work, or a phonetic substitution cipher. The capitalization ("Tahkmahnelle") is a significant clue.'
        },
        '3': {
            'title': 'Alphanumeric Code',
            'content': 'aadd/abheaa_ehd9',
            'hint': 'A classic letter/number substitution. The structure suggests repetition, possibly binary or simple frequency analysis. The digits (9) are usually key separators or modifiers.'
        },
        '4': {
            'title': 'Field of Purity Guardian Caravan',
            'content': 'haran padan aram - field of purity guardian caravan',
            'hint': 'The first three words appear foreign or coded, while the rest are descriptive. This hints at a geographical or directional cipher, or a specific name/phrase translation.'
        },
        '5': {
            'title': 'Algebraic Constraint',
            'content': 'x=abcd (k^46)',
            'hint': 'This looks like an equation where a, b, c, d, and k are single digits or letters representing variables. The exponent (46) suggests modular arithmetic or a large rotation/shift cipher.'
        },
        '6': {
            'title': 'The Lands of Ages Roster',
            'content': 'heromen of lands of ages_super mutant_hyper man_mega hero_turbo man',
            'hint': 'The structure uses a common theme (super-powered individuals) separated by underscores. Consider what these prefixes (super, hyper, mega, turbo) represent numerically or in sequence.'
        },
        '7': {
            'title': 'The Cryptic Shopping List',
            'content': 'bunnies and rainbows, youth in Asia, blister fist, blue hero, grass blues, od duck, your favorite vegetable, giraffe in the jug full of jelly',
            'hint': 'This is a list of seemingly unrelated, bizarre phrases. It is highly likely to be a cryptogram where each phrase corresponds to a single letter or number, or a creative word puzzle like a rebus.'
        },
        '8': {
            'title': 'The Final Sequence',
            'content': '62112111',
            'hint': 'A simple, short sequence of digits. Look for common visual ciphers (like a phone keypad), simple number-to-letter mapping (A=1, B=2...), or a famous number sequence (Fibonacci, etc.).'
        }
    }
    
    # Create a simplified map for the menu display
    menu_map = {k: v['title'] for k, v in puzzles_data.items()}
    return menu_map, puzzles_data


def run_puzzle_viewer():
    """
    Main application loop for the puzzle viewer.
    """
    menu_options, puzzles_data = get_puzzle_data()
    
    while True:
        display_puzzles(menu_options)
        
        user_input = input("Enter your selection (0-8): ").strip()
        
        if user_input == '0':
            print("\nThank you for exploring the puzzles. Good luck solving them!")
            sys.exit(0)
        
        if user_input in puzzles_data:
            puzzle = puzzles_data[user_input]
            print("\n" + "#"*60)
            print(f"PUZZLE {user_input}: {puzzle['title'].upper()}")
            print("#"*60)
            print(f"Cryptic Text:")
            print(f">>> {puzzle['content']}")
            print("\n--- Analyst Hint ---")
            print(f"{puzzle['hint']}")
            print("--------------------\n")
            input("Press Enter to return to the main menu...")
        else:
            print("\nInvalid selection. Please enter a number between 1 and 8, or 0 to exit.")

if __name__ == "__main__":
    run_puzzle_viewer()

