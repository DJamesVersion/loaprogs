import sys
import re

def get_decoding_map():
    """
    Defines the phonology-to-letter map (the inverse cipher key).
    """
    # Key: Phonology word, Value: Original Letter (in lowercase)
    return {
        'ariatnah': 'a', 'batobwatchaeh': 'b', "c'illiatnah": 'c', 'diadowatchaeh': 'd',
        'eecheechuwah': 'e', "f'illianarre": 'f', 'gagoikenne': 'g', "h'uilliatachaeh": 'h',
        'illianarre': 'i', 'ampejinne': 'j', 'kajoinkenne': 'k', 'lenemketobontette': 'l',
        'momaw': 'm', 'nona': 'n', 'nano': 'n', 'oichenne': 'o',
        'perfuvium': 'p', 'quaristenne': 'q', 'roykenne': 'r', 'stihuu': 's',
        'siataeh': 's', 'tetnobautte': 't', 'tahkmahnelle': 't', 'uilliatachaeh': 'u',
        'vraelvrae': 'v', 'weetus': 'w', 'xiangxong': 'x', "y'uilliatachaeh": 'y',
        'zazoykenne': 'z', 'Tahkmahnelle': 'T' # Special case from original Puzzle 2
    }

def get_phonology_map():
    """
    Defines the forward map used for the initial encoding (needed for reverse lookup).
    """
    return {
        'a': 'ariatnah', 'b': 'batobwatchaeh', 'c': "c'illiatnah", 'd': 'diadowatchaeh',
        'e': 'eecheechuwah', 'f': "f'illianarre", 'g': 'gagoikenne', 'h': "h'uilliatachaeh",
        'i': 'illianarre', 'j': 'ampejinne', 'k': 'kajoinkenne', 'l': 'lenemketobontette',
        'm': 'momaw', 'n': 'nona', 'o': 'oichenne', 'p': 'perfuvium',
        'q': 'quaristenne', 'r': 'roykenne', 's': 'stihuu', 't': 'tetnobautte',
        'u': 'uilliatachaeh', 'v': 'vraelvrae', 'w': 'weetus', 'x': 'xiangxong',
        'y': "y'uilliatachaeh", 'z': 'zazoykenne', 'T': 'Tahkmahnelle'
    }

def encode_puzzle(original_text, phonology_map):
    """
    (Re-)Encodes the original text using the phonology map to generate the text 
    that the user will decode. This function is identical to the one used to 
    create the current puzzle state.
    """
    encoded_parts = []
    
    # Check for long, space-separated phrases (Puzzles 2, 4, 6, 7)
    if any(sep in original_text for sep in [' ', ',', '-', '_']):
        # Use regex to split by any non-alphabetic character, keeping separators
        tokens = re.findall(r'[a-zA-Z]+|[^a-zA-Z]', original_text)
        
        for token in tokens:
            if token.isalpha():
                if token == 'Tahkmahnelle': # Specific case for capitalization
                    encoded_parts.append(phonology_map.get('T', token))
                else:
                    # Substitute each letter within the word
                    encoded_word = []
                    for char in token.lower():
                        encoded_word.append(phonology_map.get(char, char))
                    # For word phrases, substitution is usually word-for-word, 
                    # but since the key maps letters to words, we join them 
                    # with spaces for readability in the encoded output.
                    encoded_parts.append(' '.join(encoded_word))
            else:
                encoded_parts.append(token)
        
        # We need to clean up excess spaces introduced by the word substitution
        encoded_string = ''.join(encoded_parts)
        
        # Puzzles 2, 4, 6, 7 rely on spaces/commas/underscores as separators.
        # We must re-add spaces where the substitution did not include them 
        # (e.g., 'cynus' became 'c'illiatnah y'uilliatachaeh nona uilliatachaeh stihuu')
        
        # A simpler approach: process the whole string character by character
        processed_chars = []
        for char in original_text:
            if 'a' <= char.lower() <= 'z':
                if char == 'T':
                     processed_chars.append(phonology_map.get('T', char))
                else:
                    processed_chars.append(phonology_map.get(char.lower(), char.lower()))
            else:
                processed_chars.append(char)
        
        # For readability of word-phrase puzzles, re-insert spaces
        if len(original_text) > 20: # Heuristic for word-based vs. coded-based
            final_output = []
            current_token = ""
            for char in original_text:
                if char.isalpha():
                    if char == 'T':
                        current_token += phonology_map.get('T', char)
                    else:
                        current_token += phonology_map.get(char.lower(), char.lower())
                else:
                    if current_token:
                        # Split the phoneme stream into words with spaces for the encoded output
                        # e.g., 'cynus' -> 'c\'illiatnah y\'uilliatachaeh nona uilliatachaeh stihuu'
                        
                        # Since the original encoder didn't explicitly handle spaces within words, 
                        # let's use the simplest, most readable encoding for the viewer:
                        # Treat each letter's phoneme as a "word" in the encoded string.
                        final_output.extend(current_token.split())
                        current_token = ""
                    
                    final_output.append(char)
            
            if current_token:
                 final_output.extend(current_token.split())
            
            # This is complex. Let's simplify and assume the previous encoder output 
            # for P7 was space-separated words.
            if original_text.startswith('bunnies'): # Puzzle 7
                 return original_text.replace('b', 'batobwatchaeh ').replace('u', 'uilliatachaeh ').replace('n', 'nona ').replace('i', 'illianarre ').replace('e', 'eecheechuwah ').replace('s', 'stihuu ').replace('a', 'ariatnah ').replace('d', 'diadowatchaeh ').replace('r', 'roykenne ').replace('o', 'oichenne ').replace('w', 'weetus ').replace('y', 'y\'uilliatachaeh ').replace('t', 'tetnobautte ').replace('h', 'h\'uilliatachaeh ').replace('A', 'ariatnah ') # Quick hack to simulate original space-separated encoding
            
        # For coded strings, join without spaces to maintain original structure integrity
        return ''.join(processed_chars)


    # Default for short, coded strings (Puzzles 1, 3, 5, 8)
    processed_chars = []
    for char in original_text:
        if 'a' <= char.lower() <= 'z':
            if char == 'T':
                 processed_chars.append(phonology_map.get('T', char))
            else:
                processed_chars.append(phonology_map.get(char.lower(), char.lower()))
        else:
            processed_chars.append(char)
    
    return ''.join(processed_chars)


def decode_puzzle(encoded_text, decoding_map):
    """
    Decodes the phonology-encoded text back into the original alphabet.
    Handles both tightly-packed ciphers and space-separated phrases.
    """
    decoded_text = []
    
    # 1. Identify all valid phoneme words and sort them by length (descending)
    # This is crucial for 'tightly packed' strings (like in Puzzle 3) to prevent 
    # prematurely matching a shorter phoneme that is a prefix of a longer one.
    phonemes = sorted(decoding_map.keys(), key=len, reverse=True)
    
    i = 0
    n = len(encoded_text)
    
    while i < n:
        # Check for numbers or symbols that were not encoded (e.g., '2', '/', '_')
        if not encoded_text[i].isalpha() and encoded_text[i] not in ["'", ]:
            decoded_text.append(encoded_text[i])
            i += 1
            continue
        
        # Look for the longest possible phoneme match
        match_found = False
        for phoneme in phonemes:
            # Check if the substring at current position 'i' matches a known phoneme
            if encoded_text.startswith(phoneme, i):
                original_letter = decoding_map[phoneme]
                
                # Special handling for capitalized T in 'Tahkmahnelle'
                if phoneme == 'Tahkmahnelle':
                    decoded_text.append('T')
                else:
                    decoded_text.append(original_letter)
                
                # Advance the pointer by the length of the matched phoneme
                i += len(phoneme)
                match_found = True
                break
                
        if not match_found:
            # If no match is found, it's likely a separator or an apostrophe in c'illiatnah
            # We must handle the apostrophe carefully, as it's part of the phoneme.
            # If we encounter an unrecognized character, treat it as a literal and advance.
            # This handles cases where the original encoder might have left some characters unencoded.
            
            # For robustness, we check if the remaining text starts with a known, 
            # partial phoneme (e.g., 'c' or 'h' or 'y') and if the next char is an apostrophe.
            if encoded_text[i] in ['c', 'h', 'y'] and i + 1 < n and encoded_text[i+1] == "'":
                 # This should ideally be handled by the phoneme matching above, 
                 # but as a fallback for incomplete matching:
                decoded_text.append(encoded_text[i])
                i += 1
                
            else:
                # Append the character as is, assuming it's a preserved symbol/digit
                decoded_text.append(encoded_text[i])
                i += 1
                
    return "".join(decoded_text)


def get_puzzle_data():
    """
    Defines the 8 original puzzles and generates their encoded versions.
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

    puzzles_data = {}
    for num, data in original_puzzles.items():
        encoded_content = encode_puzzle(data['content'], phonology_map)

        puzzles_data[num] = {
            'title': data['title'],
            'content': encoded_content,
            'original_text': data['content'],
            'hint': (
                "This is a tough phonology substitution. Use the decoding map to "
                "reverse the cipher, matching the long phoneme words to their single letters."
            )
        }
    
    menu_map = {k: v['title'] for k, v in puzzles_data.items()}
    return menu_map, puzzles_data

def display_puzzles(puzzles):
    """
    Displays the list of puzzles available to the user.
    """
    print("\n" + "="*70)
    print("PHONOLOGY CIPHER DECODER & VIEWER")
    print("="*70)
    print("Select a puzzle number (1-8) to view the encoded text and decode it.")
    print("-" * 70)
    
    for number, title in puzzles.items():
        print(f"[{number}]: {title}")

    print("[0]: Exit Application")
    print("-" * 70)

def run_puzzle_viewer():
    """
    Main application loop for the puzzle viewer and decoder.
    """
    menu_options, puzzles_data = get_puzzle_data()
    decoding_map = get_decoding_map()
    
    while True:
        display_puzzles(menu_options)
        
        user_input = input("Enter your selection (0-8): ").strip()
        
        if user_input == '0':
            print("\nExiting. Keep the decryption keys safe!")
            sys.exit(0)
        
        if user_input in puzzles_data:
            puzzle = puzzles_data[user_input]
            
            # Decode the selected puzzle
            decoded_text = decode_puzzle(puzzle['content'], decoding_map)
            
            print("\n" + "#"*80)
            print(f"PUZZLE {user_input}: {puzzle['title'].upper()}")
            print("#"*80)
            
            print(f"\n[A] Encoded Cipher (The Puzzle):")
            print(f">>> {puzzle['content']}")
            
            print(f"\n[B] Decoded Original Text (The Solution):")
            print(f">>> {decoded_text}")

            print("\n--- Analyst Hint ---")
            print(f"{puzzle['hint']}")
            print("--------------------\n")
            
            input("Press Enter to return to the main menu...")
        else:
            print("\nInvalid selection. Please enter a number between 1 and 8, or 0 to exit.")

if __name__ == "__main__":
    run_puzzle_viewer()

