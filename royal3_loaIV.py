import sys
import time

# --- ANSI Color Codes for Terminal Graphics ---
COLOR_RESET = "\033[0m"
COLOR_TITLE = "\033[96m"    # Cyan/Light Blue
COLOR_PROMPT = "\033[93m"   # Yellow
COLOR_NARRATIVE = "\033[97m" # White
COLOR_ALERT = "\033[91m"    # Red (for danger/mistakes)
COLOR_SUCCESS = "\033[92m"  # Green (for success/clues)
COLOR_HEADER = "\033[95m"   # Magenta
COLOR_ROYAL = "\033[33m"    # Gold (Royal Family)
COLOR_MAGIC = "\033[36m"    # Light Cyan (Magic Theme)

# --- Cipher Mapping (Secrets Long Ago Hidden) ---
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

# --- Game State and Variables ---
class GameState:
    def __init__(self):
        self.magic_keys = []
        self.scepter_activated = False
        self.player_name = "Agent"
        self.correct_passphrase = "HEIR" # Cipher word that activates the Scepter: H-E-I-R

game = GameState()

# --- Scene Definitions ---

def scene_prologue():
    """Scene 1: Introduction, meeting Queen EadsL and receiving the first keys."""
    print(COLOR_TITLE + """
   __                                    ___ 
  / /  ___   __ _  _ __   ___   _ __    |__ \\
 / /  / _ \ / _` || '_ \ / _ \ | '_ \    / /
/ /__|  __/| (_| || | | | (_) || | | |  |_|
\____/\___| \__,_||_| |_|\___/ |_| |_|  (_)
    """ + COLOR_RESET)
    
    print(COLOR_TITLE + "=== ROYAL3 LANDS OF AGES IV: SCION OF THE SCEPTER ===" + COLOR_RESET)
    
    game.player_name = get_input("Pilot, state your code name for the Royal Guard.").title()
    if not game.player_name:
        game.player_name = "Valiant"

    print_scene_header("SECTOR 1: THRONE ROOM OF THE REDEEMED")
    print_slow("You kneel before **Queen EadsL**, Mother of the Royal House. The air crackles with latent magic.")
    
    print(COLOR_ROYAL + "QUEEN EADSL (Mother): " + COLOR_RESET, end="")
    print_slow(f"Welcome, {game.player_name}. My child, **jpw7**, must claim the Scepter of True Magic to secure our realm. It requires four ancient keys.")
    print_slow("The Scepter's activation code spells out the destiny of the bloodline: **HEIR**.")
    
    print(COLOR_ROYAL + "EADSL: " + COLOR_RESET, end="")
    print_slow("I provide the first two pieces of the **HEIR** cipher.")
    
    # Clues H and E provided by EadsL
    clue_h = CIPHER['h']
    clue_e = CIPHER['e']
    print_slow(COLOR_SUCCESS + f"KEY PIECES ACQUIRED: The first two letters are **H** and **E**, coded as: 1. {clue_h} and 2. {clue_e}" + COLOR_RESET)
    game.magic_keys.extend(['H', 'E'])
    
    print_slow("She tells you to seek **JWE6** in the Hall of Ordeals.")
    time.sleep(1)
    scene_jwe6_trial()

def scene_jwe6_trial():
    """Scene 2: Meeting King JWE6 for the I piece via a cipher test."""
    print_scene_header("SECTOR 2: THE HALL OF ORDEALS")
    print_slow("You find **King JWE6** (Father), standing beside a massive, magically sealed gate. This gate guards the third key.")
    
    print(COLOR_ROYAL + "KING JWE6 (Father): " + COLOR_RESET, end="")
    print_slow("The ancient text warns against those who do not understand the power of our lineage. You must identify the key for 'MAGIC'.")
    
    # Correct key is I (illianarre)
    correct_cipher_word = CIPHER['i'] 
    
    print_slow(f"The word for 'I' in the code is the cipher for **ILLIANARRE**. What is the single letter it represents?")
    
    guess = get_input("Enter the single letter (e.g., A, I, L)").upper()
    
    if guess == 'I':
        print_slow(COLOR_SUCCESS + "TRIAL PASSED! 'I' for Illianarre. Your knowledge is true. The seal breaks.")
        
        # Clue I
        clue_i = CIPHER['i']
        print(COLOR_ROYAL + "JWE6: " + COLOR_RESET, end="")
        print_slow(f"Take this. It is the third piece of the Scepter code: **I**, coded as: {clue_i}")
        game.magic_keys.append('I')
        print_slow(COLOR_SUCCESS + "KEY PIECE ACQUIRED: 3. I" + COLOR_RESET)
    else:
        print_slow(COLOR_ALERT + "TRIAL FAILED. That is not 'I'. The King smiles sadly.")
        print(COLOR_ROYAL + "JWE6: " + COLOR_RESET, end="")
        print_slow("You must find the **I** key elsewhere, or proceed without it. Seek **jpw7** in the Nursery of Whispers.")
    
    time.sleep(2)
    scene_jpw7_secret()

def scene_jpw7_secret():
    """Scene 3: Meeting the heir jpw7 and finding the final key R."""
    print_scene_header("SECTOR 3: NURSERY OF WHISPERS")
    print_slow("You enter the Nursery, which hums with protective spells. The young heir, **jpw7**, plays with glowing, intangible spheres.")
    
    print(COLOR_ROYAL + "JPW7 (The Child): " + COLOR_RESET, end="")
    print_slow("My destiny is coded in my name, Agent. The final key, **R**, is hidden in plain sight. It relates to the word **ROYKENNE**.")
    
    choice = get_input("Do you search the toys (1) or ask what ROYKENNE means (2)?")
    
    if choice == '2':
        print_slow("You ask for the meaning. The child laughs with pure magic.")
        print(COLOR_ROYAL + "JPW7: " + COLOR_RESET, end="")
        print_slow("'Roykenne' is the secret word for **Royal House**! The R-key is on the **R**oyal **R**ing I wear!")
        
        # Clue R
        clue_r = CIPHER['r']
        print_slow(f"The child hands you a silver ring with the cipher inscribed.")
        print_slow(COLOR_SUCCESS + f"KEY PIECE ACQUIRED: 4. R, coded as: {clue_r}" + COLOR_RESET)
        game.magic_keys.append('R')
    else:
        print_slow(COLOR_ALERT + "You waste time searching through mundane toys. The child is impatient and simply hands you the ring.")
        
        # Clue R (Guaranteed, but less dramatic)
        clue_r = CIPHER['r']
        print_slow(f"The child hands you the Royal Ring, stating the key is **R**.")
        game.magic_keys.append('R')
        print_slow(COLOR_SUCCESS + "KEY PIECE ACQUIRED: 4. R" + COLOR_RESET)
        
    print_slow("\nWith all available keys secured, you head to the Scepter Chamber.")
    
    time.sleep(2)
    scene_final_activation()

def scene_final_activation():
    """Scene 4: Decrypting the final passphrase and activating the Scepter."""
    print_scene_header("SECTOR 4: THE SCEPTER CHAMBER")
    print_slow("The chamber is a whirlwind of arcane energy. The Scepter of True Magic floats above a pedestal, awaiting its master.")
    
    # Use the collected letters to form the prompt
    current_word = "".join(game.magic_keys)
    
    print_slow(COLOR_MAGIC + f"Cipher Keys Collected: {'-'.join(game.magic_keys)}" + COLOR_RESET)
    
    if len(game.magic_keys) < 4:
        print_slow(COLOR_ALERT + f"WARNING: You are missing {4 - len(game.magic_keys)} key components! You must guess the full four-letter activation word." + COLOR_RESET)
        
    print_slow(COLOR_NARRATIVE + "The Scepter's activation code is the child's destiny: **H-E-I-R**." + COLOR_RESET)
    
    final_passphrase = get_input("Enter the complete 4-letter activation word")
    
    if final_passphrase.upper() == game.correct_passphrase:
        print_slow(COLOR_SUCCESS + "\nACTIVATION CODE ACCEPTED. The Scepter descends!" + COLOR_RESET)
        print_slow("Pure magic flows through the chamber. The Scepter of True Magic is now ready for the heir.")
        game.scepter_activated = True
    else:
        print_slow(COLOR_ALERT + "\nACTIVATION FAILED. The Scepter remains locked." + COLOR_RESET)
        print_slow("The magic withdraws. The Royal House remains vulnerable until the Scepter is claimed.")
        game.scepter_activated = False

    time.sleep(3)
    scene_epilogue()

def scene_epilogue():
    """Scene 5: Conclusion and the new age."""
    print_scene_header("CONCLUSION: ROYAL3 LANDS OF AGES IV")
    
    if game.scepter_activated:
        print(COLOR_SUCCESS + "\n<<< THE NEW AGE OF MAGIC BEGINS! >>>" + COLOR_RESET)
        print_slow("With the Scepter activated, the young heir, jpw7, is crowned. Magic is victorious across the Lands of Ages.")
        print_slow(f"The Royal House—EadsL, JWE6, and jpw7—thank Agent {game.player_name}. Their lineage is secure.")
        print_slow("Secrets of the bloodline are now unlocked, promising adventures for centuries to come.")
    else:
        print(COLOR_ALERT + "\n<<< MAGICAL STAGNATION >>>" + COLOR_RESET)
        print_slow("The Scepter lies dormant. EadsL and JWE6 must find a way to complete the cipher.")
        print_slow("You are tasked with one final, secret mission: find the original cipher scrolls and protect the heir.")

    print(COLOR_HEADER + "\n--- ROYAL INHERITANCE REPORT ---" + COLOR_RESET)
    print(f"Collected Cipher Keys: {len(game.magic_keys)}/4")
    print(f"Scepter Status: {'Activated' if game.scepter_activated else 'Locked'}")
    print(f"Heir Destiny: {'Fulfilled' if game.scepter_activated else 'Uncertain'}")
    print(COLOR_HEADER + "--------------------------------" + COLOR_RESET)
    print_slow("\nProgram Terminating. Long live the Royal House!")

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

