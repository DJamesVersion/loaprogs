import sys
import time

# --- ANSI Color Codes for Terminal Graphics ---
COLOR_RESET = "\033[0m"
COLOR_TITLE = "\033[96m"  # Cyan/Light Blue
COLOR_PROMPT = "\033[93m"  # Yellow
COLOR_NARRATIVE = "\033[97m"  # White
COLOR_ALERT = "\033[91m"  # Red
COLOR_SUCCESS = "\033[92m"  # Green
COLOR_HEADER = "\033[95m"  # Magenta
COLOR_CHARACTER = "\033[33m"  # Gold

# --- Cipher Mapping (Mandatory for the Plot) ---
CIPHER = {
    'a': 'ariatnah', 'b': 'batobwatchaeh', 'c': "c'illiatnah", 'd': 'diadowatchaeh', 
    'e': 'eecheechuwah', 'f': "f'illianarre", 'g': 'gagoikenne', 'h': "h'uilliatachaeh", 
    'i': 'illianarre', 'j': 'ampejinne', 'k': 'kajoinkenne', 'l': 'lenemketobontette', 
    'm': 'momaw', 'n': 'nona, nano', 'o': 'oichenne', 'p': 'perfuvium', 
    'q': 'quaristenne', 'r': 'roykenne', 's': 'stihuu,siataeh', 't': 'tetnobautte', 
    'u': 'uilliatachaeh', 'v': 'vraelvrae', 'w': 'weetus', 'x': 'xiangxong', 
    'y': "y'uilliatachaeh", 'z': 'zazoykenne'
}

# --- Utility Functions ---

def print_slow(text, delay=0.03):
    """Prints text character by character for dramatic effect."""
    for char in text:
        sys.stdout.write(COLOR_NARRATIVE + char + COLOR_RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print() # Newline after finishing the line

def print_scene_header(title):
    """Prints a styled header for scene transitions."""
    print(COLOR_HEADER + "\n===================================================" + COLOR_RESET)
    print(COLOR_HEADER + f"| {title.center(47)} |" + COLOR_RESET)
    print(COLOR_HEADER + "===================================================" + COLOR_RESET)
    time.sleep(1)

def get_input(prompt):
    """Gets user input with a styled prompt."""
    print(COLOR_PROMPT + f"\n[> {prompt} (Enter)]" + COLOR_RESET)
    return input().strip().lower()

def decode_letter(cipher_word):
    """Decodes a single cipher word back to its letter."""
    for letter, word in CIPHER.items():
        if word == cipher_word:
            return letter.upper()
    return '?'

# --- Game State and Variables ---
class GameState:
    def __init__(self):
        self.clue_pieces = []
        self.evidence_acquired = False
        self.justice_served = False
        self.player_name = "Investigator"
        self.correct_passphrase = "VAULT" # The final word player must submit (V-A-U-L-T)

game = GameState()

# --- Scene Definitions ---

def scene_prologue():
    """Scene 1: Introduction and meeting Jocelyn."""
    print(COLOR_TITLE + """
   __       TAHKMAHNELLE CIPHER PROJECT     ___ 
  / /  ___   __ _  _ __   ___   _ __    |__ \\
 / /  / _ \ / _` || '_ \ / _ \ | '_ \    / /
/ /__|  __/| (_| || | | | (_) || | | |  |_|
\____/\___| \__,_||_| |_|\___/ |_| |_|  (_)
    """ + COLOR_RESET)
    
    print(COLOR_TITLE + "=== ROYAL3 LANDS OF AGES: JUSTICE ADVANCE ===" + COLOR_RESET)
    
    game.player_name = get_input("Investigator, state your code name.")
    if not game.player_name:
        game.player_name = "Kore"

    print_scene_header("SECTOR 1: THE TAINTED SHORE MEETING")
    print_slow("You meet **Jocelyn**, a nervous but determined Royal informant, near the corrupt Tahkmahnelle Quarry.")
    print(COLOR_CHARACTER + "JOCELYN: " + COLOR_RESET, end="")
    print_slow(f"They know I'm here, {game.player_name}. I can only give you the first two pieces of the cipher key. They form the beginning of the **FINAL WORD**.")

    choice = get_input("Do you ask for clarification (1) or immediately secure the message (2)?")
    
    if choice == '1':
        print_slow("Jocelyn shakes her head. 'No time. Just remember: I start with the letter **V** and the letter **A**.'")
        print_slow("She thrusts a slip of paper into your hand. It reads:")
    else:
        print_slow("Jocelyn nods at your efficiency. 'Good. Remember: **V** then **A**.'")
        print_slow("She thrusts a slip of paper into your hand. It reads:")

    # Clues V and A
    clue_v = CIPHER['v']
    clue_a = CIPHER['a']
    print_slow(COLOR_SUCCESS + f"CLUE PIECES ACQUIRED: 1. {clue_v} and 2. {clue_a}" + COLOR_RESET)
    game.clue_pieces.extend(['V', 'A'])
    
    print_slow("Before you can respond, Jocelyn is dragged away by a Tahkmahnelle enforcement squad. You must find Henrietta.")
    time.sleep(1)
    scene_henrietta_study()

def scene_henrietta_study():
    """Scene 2: Meeting Henrietta, the scholar."""
    print_scene_header("SECTOR 2: HENRIETTA'S ISOLATED TOWER")
    print_slow("You find **Henrietta**, a recluse specializing in the ancient languages of Royal3, hunched over scrolls.")
    
    print(COLOR_CHARACTER + "HENRIETTA: " + COLOR_RESET, end="")
    print_slow(f"Ah, {game.player_name}. Jocelyn alerted me. The key you seek is a word from the **Vault Protocol**. What are the two cipher keys you hold?")

    print_slow("You show her the slips of paper.")
    print_slow(f"1. {CIPHER['v']} (V) and 2. {CIPHER['a']} (A).")
    
    print(COLOR_CHARACTER + "HENRIETTA: " + COLOR_RESET, end="")
    print_slow(f"Excellent. The next key is the letter **U**. But it is locked behind a test of knowledge. I will give you a word. Decode the letter that starts it.")
    
    test_word = "tetnobautte" # T
    
    print_slow(f"\nTEST: The code for the Tahkmahnelle Director is **{test_word}**. Which single letter does it represent?")
    
    guess = get_input("Enter the single letter (e.g., K, M, T)").upper()
    
    if guess == 'T':
        print_slow(COLOR_SUCCESS + "CORRECT! 'T' stands for Tahkmahnelle, or 'tetnobautte'. You have the knowledge." + COLOR_RESET)
        
        # Clue U
        clue_u = CIPHER['u']
        print(COLOR_CHARACTER + "HENRIETTA: " + COLOR_RESET, end="")
        print_slow(f"Take this. It is the third piece of the final word. It is **U**, coded as: {clue_u}")
        game.clue_pieces.append('U')
        print_slow(COLOR_SUCCESS + "CLUE PIECE ACQUIRED: 3. U" + COLOR_RESET)

    else:
        print_slow(COLOR_ALERT + "INCORRECT. That is not the letter T. Henrietta sighs, disappointed." + COLOR_RESET)
        print(COLOR_CHARACTER + "HENRIETTA: " + COLOR_RESET, end="")
        print_slow("I cannot give you the piece directly. You must earn it. I can only say the letter is **U**.")
    
    print_slow("Henrietta tells you to seek out Gabriella, the only agent who knows the final steps.")
    time.sleep(2)
    scene_gabriella_ambush()

def scene_gabriella_ambush():
    """Scene 3: Meeting Gabriella, the field agent."""
    print_scene_header("SECTOR 3: THE HIGH RIDGE AMBUSH")
    
    print_slow("You find **Gabriella** pinned down on a rocky outcrop, exchanging fire with Tahkmahnelle snipers.")
    
    print(COLOR_CHARACTER + "GABRIELLA: " + COLOR_RESET, end="")
    print_slow("They found me! I have the final two pieces, but you must distract them while I encode the full message.")
    
    choice = get_input("Do you draw the snipers' fire (1) or provide covering fire (2)?")
    
    if choice == '1':
        print_slow("You make yourself an easy target, sprinting across the ridge. The snipers focus on you, allowing Gabriella precious seconds.")
        game.clue_pieces.extend(['L', 'T'])
        print(COLOR_CHARACTER + "GABRIELLA: " + COLOR_RESET, end="")
        print_slow("Here! The final letters are **L** and **T**! Now run!")
        print_slow(COLOR_SUCCESS + "CLUE PIECES ACQUIRED: 4. L and 5. T" + COLOR_RESET)
    else:
        print_slow("Your covering fire is ineffective. Gabriella is hit and must retreat quickly, managing only to throw you one piece.")
        game.clue_pieces.append('L')
        print(COLOR_CHARACTER + "GABRIELLA: " + COLOR_RESET, end="")
        print_slow("It's **L**... You must find the last letter yourself!")
        print_slow(COLOR_ALERT + "CLUE PIECE ACQUIRED: 4. L (Final piece, T, is missing)." + COLOR_RESET)

    print_slow("\nSafely away, you check your inventory:")
    print_slow(f"Cipher Letters Collected: {'-'.join(game.clue_pieces)}")
    
    if len(game.clue_pieces) < 5:
        print_slow(COLOR_ALERT + "You are missing the final 'T' piece! You must use your knowledge of the Lands to guess it." + COLOR_RESET)
        if 'U' not in game.clue_pieces:
            print_slow(COLOR_ALERT + "You also failed Henrietta's test and missed the 'U' piece! This will be difficult." + COLOR_RESET)
        
    time.sleep(2)
    scene_final_decoding()

def scene_final_decoding():
    """Scene 4: Decrypting the final passphrase to access the Vault."""
    print_scene_header("SECTOR 4: THE ACCESS CONSOLE")
    print_slow("You stand before the main Tahkmahnelle data Vault. A holographic console demands a five-letter passphrase.")
    
    # Use the collected letters to form the prompt
    current_word = "".join(game.clue_pieces)
    
    if len(current_word) < 5:
        print_slow("Your incomplete set of letters leaves gaps. You must submit the full, 5-letter word.")
    else:
        print_slow("Your pieces are complete! Combine the cipher letters to form the crucial 5-letter word.")
    
    print_slow(COLOR_PROMPT + f"Your current collected letters: {current_word}" + COLOR_RESET)
    print_slow(COLOR_NARRATIVE + "The final word is the name of the objective: the **V-A-U-L-T**." + COLOR_RESET)
    
    final_passphrase = get_input("Enter the complete 5-letter passphrase (e.g., STONE)")
    
    if final_passphrase.upper() == game.correct_passphrase:
        print_slow(COLOR_SUCCESS + "\nACCESS GRANTED. The Vault hums open." + COLOR_RESET)
        print_slow("Inside, you find irrefutable data on the Director's treason and illegal Aegis Stone trade.")
        game.evidence_acquired = True
        print_slow(COLOR_SUCCESS + "EVIDENCE ACQUIRED: Tahkmahnelle's Master Logs." + COLOR_RESET)
    else:
        print_slow(COLOR_ALERT + "\nACCESS DENIED. The console flashes red." + COLOR_RESET)
        print_slow("Your time runs out. Tahkmahnelle forces arrive and lockdown the sector.")
        game.evidence_acquired = False

    time.sleep(3)
    scene_epilogue()

def scene_epilogue():
    """Scene 5: Conclusion and final status."""
    print_scene_header("RESOLUTION: ROYAL COURT OF JUSTICE")
    
    if game.evidence_acquired:
        print(COLOR_SUCCESS + "\n<<< JUSTICE PREVAILS! >>>" + COLOR_RESET)
        print_slow("With the Master Logs in hand, you present the evidence. Tahkmahnelle is dismantled and his Director arrested.")
        print_slow(f"Jocelyn, Henrietta, and Gabriella are safe. Investigator {game.player_name}, you have restored order to the Lands of Ages.")
        game.justice_served = True
    else:
        print(COLOR_ALERT + "\n<<< ADVENTURE FAILED >>>" + COLOR_RESET)
        print_slow("Without the Vault's data, Tahkmahnelle's corruption continues. Your only allies are in the shadows.")
        print_slow(f"You narrowly escape the sector, but the fight has just begun. The fate of Royal3 hangs in the balance.")

    print(COLOR_HEADER + "\n--- STATS ---" + COLOR_RESET)
    print(f"Collected Clue Letters: {len(game.clue_pieces)}/5")
    print(f"Final Passphrase: {'Deciphered' if game.evidence_acquired else 'Failed'}")
    print(f"Verdict: {'GUILTY' if game.justice_served else 'FREE'}")
    print(COLOR_HEADER + "------------------" + COLOR_RESET)
    print_slow("\nProgram Terminating.")

# --- Main Game Loop ---

def start_game():
    """Initializes and runs the game sequence."""
    try:
        scene_prologue()
    except EOFError:
        print(COLOR_ALERT + "\n\n[ERROR: Input stream closed. Exiting game.]" + COLOR_RESET)
    except Exception as e:
        print(COLOR_ALERT + f"\n\n[ERROR: An unexpected error occurred: {e}. Exiting game.]" + COLOR_RESET)
    finally:
        print_scene_header("END OF TRANSMISSION")

if __name__ == "__main__":
    start_game()

