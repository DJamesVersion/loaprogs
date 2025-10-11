import sys
import re

# --- Tahkmahnelle Linguistic Database ---

# Explanation of the "Lands of Ages" (LoA) concept in Tahkmahnelle linguistics.
# This system links phonology (initial sounds/graphemes) to foundational conceptual roots 
# tied to a cosmic or historical 'Age.'
LOA_EXPLANATION = """
### The Lands of Ages (LoA) in Tahkmahnelle Linguistics ###

The Tahkmahnelle language is built upon the philosophical concept of the 'Lands of Ages' (LoA). This is not just a lexicon, but an ontological index where every foundational root corresponds to a specific historical, cosmic, or spiritual phase (an 'Age').

**Phonological Connection:**
Each initial phonological grouping (represented by the letters A-Z in this index) is considered an 'Age-Marker.' When a Tahkmahnelle word is constructed, its primary meaning is immediately contextualized by the 'Age-Marker' it begins with, defining the root's relation to time, creation, or destiny.

**The Index's Purpose:**
The dictionary entries below are the 'Primal Roots' (Tkemnâti) associated with each Age-Marker. To understand any complex Tahkmahnelle phrase, one must first grasp the LoA Root, as it provides the deepest cultural and temporal context for the word's usage. The roots are phonologically related to the initial letter, making this index a key to Tahkmahnelle's unique semantic structure.
"""

# The dictionary of Tahkmahnelle roots (Primal Roots / Tkemnâti) 
# and their conceptual link to the Lands of Ages.
TAHKMAHNELLE_DICTIONARY = {
    'a': {'root': 'ariatnah', 'meaning': 'Root for \'Beginning,\' \'Dawn,\' or \'First Light.\'', 'age': 'The Age of Genesis'},
    'b': {'root': 'batobwatchaeh', 'meaning': 'Root for \'Unfurling,\' \'Expansion,\' or \'To Become Vast.\'', 'age': 'The Age of Growth'},
    'c': {'root': "c'illiatnah", 'meaning': 'Root for \'Consciousness,\' \'Inner Gaze,\' or \'Self-Awareness.\'', 'age': 'The Age of Sentience'},
    'd': {'root': 'diadowatchaeh', 'meaning': 'Root for \'Structure,\' \'Foundation,\' or \'Binding Law.\'', 'age': 'The Age of Order'},
    'e': {'root': 'eecheechuwah', 'meaning': 'Root for \'Flow,\' \'River,\' or \'Eternal Motion.\'', 'age': 'The Age of Continuity'},
    'f': {'root': "f'illianarre", 'meaning': 'Root for \'Covenant,\' \'Sacred Duty,\' or \'Bound by Oath.\'', 'age': 'The Age of Oaths'},
    'g': {'root': 'gagoikenne', 'meaning': 'Root for \'Gathering,\' \'Assembly,\' or \'Community.\'', 'age': 'The Age of Alliance'},
    'h': {'root': "h'uilliatachaeh", 'meaning': 'Root for \'Echo,\' \'Reflection,\' or \'Memory of the Past.\'', 'age': 'The Age of Precedent'},
    'i': {'root': 'illianarre', 'meaning': 'Root for \'Truth,\' \'Unveiling,\' or \'Revelation.\'', 'age': 'The Age of Clarity'},
    'j': {'root': 'ampejinne', 'meaning': 'Root for \'Intervention,\' \'Sudden Change,\' or \'Catalyst.\'', 'age': 'The Age of Catalyst'},
    'k': {'root': 'kajoinkenne', 'meaning': 'Root for \'Harmony,\' \'Balance,\' or \'The Midpoint.\'', 'age': 'The Age of Zenith'},
    'l': {'root': 'lenemketobontette', 'meaning': 'Root for \'Long Journey,\' \'Exile,\' or \'Wandering.\'', 'age': 'The Age of Passage'},
    'm': {'root': 'momaw', 'meaning': 'Root for \'Sustenance,\' \'Nourishment,\' or \'The Mother Principle.\'', 'age': 'The Age of Life'},
    'n': {'root': 'nona, nano', 'meaning': 'Root for \'Negation,\' \'Void,\' or \'The Absence.\'', 'age': 'The Age of Silence'},
    'o': {'root': 'oichenne', 'meaning': 'Root for \'Wisdom,\' \'Deep Understanding,\' or \'Enlightenment.\'', 'age': 'The Age of Enlightenment'},
    'p': {'root': 'perfuvium', 'meaning': 'Root for \'Scattering,\' \'Fragmentation,\' or \'Dispersion.\'', 'age': 'The Age of Diaspora'},
    'q': {'root': 'quaristenne', 'meaning': 'Root for \'Question,\' \'The Search,\' or \'Inquiry.\'', 'age': 'The Age of Inquiry'},
    'r': {'root': 'roykenne', 'meaning': 'Root for \'Return,\' \'Recurrence,\' or \'The Cycle.\'', 'age': 'The Age of Cycles'},
    's': {'root': 'stihuu, siataeh', 'meaning': 'Root for \'Vibration,\' \'Sound,\' or \'Spoken Word.\'', 'age': 'The Age of Voice'},
    't': {'root': 'tetnobautte, tahkmahnelle', 'meaning': 'Root for \'Governance,\' \'System,\' or \'The People/Culture.\'', 'age': 'The Age of Culture'},
    'u': {'root': 'uilliatachaeh', 'meaning': 'Root for \'Vision,\' \'Foresight,\' or \'The Future.\'', 'age': 'The Age of Destiny'},
    'v': {'root': 'vraelvrae', 'meaning': 'Root for \'Convergence,\' \'The Meeting Place,\' or \'Unification.\'', 'age': 'The Age of Unity'},
    'w': {'root': 'weetus', 'meaning': 'Root for \'Waiting,\' \'Anticipation,\' or \'Stasis.\'', 'age': 'The Age of Stasis'},
    'x': {'root': 'xiangxong', 'meaning': 'Root for \'Fusion,\' \'Synthesis of Opposites,\' or \'Integration.\'', 'age': 'The Age of Integration'},
    'y': {'root': "y'uilliatachaeh", 'meaning': 'Root for \'Culmination,\' \'The Final Seal,\' or \'End of an Era.\'', 'age': 'The Age of Ending'},
    'z': {'root': 'zazoykenne', 'meaning': 'Root for \'Rebirth,\' \'The Renewal,\' or \'Restart.\'', 'age': 'The Age of Transition'}
}

def display_loa_explanation():
    """Prints the comprehensive explanation of the Lands of Ages concept."""
    print("=" * 80)
    print("      Tahkmahnelle Linguistics: Lands of Ages (LoA) Explanation")
    print("=" * 80)
    print(LOA_EXPLANATION)
    print("-" * 80)

def display_dictionary_entry(query):
    """Looks up and prints a dictionary entry for the given query (single letter)."""
    # Normalize query to single lowercase letter
    query = query.lower().strip()
    
    if len(query) != 1 or not query.isalpha():
        print(f"\n[Error] Please enter a single letter (a-z) to look up a root.")
        return

    entry = TAHKMAHNELLE_DICTIONARY.get(query)

    if entry:
        print("\n" + "=" * 50)
        print(f"Index Marker: {query.upper()}")
        print("-" * 50)
        print(f"Primal Root (Tkemnâti): {entry['root']}")
        print(f"Conceptual Meaning: {entry['meaning']}")
        print(f"Linguistic Context (LoA): {entry['age']}")
        print("=" * 50)
    else:
        print(f"\n[Error] The letter '{query.upper()}' is not a recognized Age-Marker in the current Tahkmahnelle Index.")

def display_full_dictionary():
    """Prints all dictionary entries in a formatted list."""
    print("\n" + "=" * 80)
    print("         Tahkmahnelle Lands of Ages (LoA) Primal Roots Index")
    print("=" * 80)
    
    # Sort keys alphabetically for clean display
    sorted_keys = sorted(TAHKMAHNELLE_DICTIONARY.keys())
    
    for key in sorted_keys:
        entry = TAHKMAHNELLE_DICTIONARY[key]
        # Format the line: Marker | Root | Meaning | Age
        print(f"[{key.upper()}] {entry['root']:<25} | Meaning: {entry['meaning']:<45} | Age: {entry['age']}")

    print("=" * 80)


def main_menu():
    """Presents the interactive command-line interface."""
    
    # Determine the name of the script for user instructions
    script_name = sys.argv[0] if sys.argv else "LoA_index.py"
    
    print("\n" + "#" * 80)
    print(f"      Welcome to the Tahkmahnelle Lands of Ages (LoA) Index - ({script_name})")
    print("#" * 80)
    
    while True:
        print("\n--- Main Menu ---")
        print("1. Read the Lands of Ages (LoA) Linguistic Explanation")
        print("2. Look up a specific Primal Root (e.g., enter 'A', 'M', or 'Z')")
        print("3. Display the Full Tahkmahnelle Primal Roots Dictionary")
        print("4. Exit Application")
        
        choice = input("Enter your choice (1-4) or a letter to look up: ").lower().strip()
        
        if choice == '1':
            display_loa_explanation()
        elif choice == '2':
            query = input("Enter the single letter Age-Marker to look up: ").lower().strip()
            display_dictionary_entry(query)
        elif choice == '3':
            display_full_dictionary()
        elif choice == '4' or choice in ['exit', 'quit']:
            print("\nThank you for exploring the Tahkmahnelle LoA Index. Farewell.")
            break
        elif len(choice) == 1 and choice.isalpha():
            display_dictionary_entry(choice)
        else:
            print("\n[Error] Invalid input. Please enter a number (1-4) or a single letter for a dictionary lookup.")

# --- Execution ---
if __name__ == "__main__":
    main_menu()

