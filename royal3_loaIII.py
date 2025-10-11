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
COLOR_CHARACTER = "\033[36m" # Light Cyan (Hero Men)
COLOR_TAHKMAHNELLE = "\033[32m" # Green (Redeemed Tahkmahnelle)

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
        self.shield_pieces = []
        self.aegis_activated = False
        self.player_name = "Agent"
        self.correct_passphrase = "VAULT" # Cipher word that activates the shield: V-A-U-L-T

game = GameState()

# --- Scene Definitions ---

def scene_prologue():
    """Scene 1: Introduction, meeting the reformed Tahkmahnelle and Battle Shields."""
    print(COLOR_TITLE + """
 ██████╗ ██████╗  █████╗  ██╗   ██╗ ██╗     
 ██╔══██╗██╔══██╗██╔══██╗ ██║   ██║ ██║     
 ██████╔╝██████╔╝███████║ ██║   ██║ ██║     
 ██╔══██╗██╔══██╗██╔══██║ ██║   ██║ ██║     
 ██║  ██║██║  ██║██║  ██║  ██████╔╝ ███████╗
 ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═════╝  ╚══════╝
    """ + COLOR_RESET)
    
    print(COLOR_TITLE + "=== ROYAL3 LANDS OF AGES III: THE BLIGHT THREAT ===" + COLOR_RESET)
    
    game.player_name = get_input("Pilot, report your callsign.").title()
    if not game.player_name:
        game.player_name = "Agent"

    print_scene_header("SECTOR 1: THE TAHKMAHNELLE COMMAND CENTER (REFORMED)")
    print_slow("You are in the rebuilt Tahkmahnelle center. It is now a beacon of justice.")
    
    print(COLOR_TAHKMAHNELLE + "DIRECTOR TAHKMAHNELLE: " + COLOR_RESET, end="")
    print_slow(f"Welcome, {game.player_name}. The ancient 'Blight' is resurfacing, tied to secrets we corrupted long ago. Only the **Aegis Shield** can stop it. Its five components are hidden.")
    
    print(COLOR_CHARACTER + "BATTLE SHIELDS (TEAM LEAD): " + COLOR_RESET, end="")
    print_slow("Our team is scattered, each securing a piece of the cipher. You must gather the keys and decode the **activation word**.")
    
    print_slow("\nBattle Shields hands you an ancient scroll fragment.")
    
    # Clues V and A provided by Battle Shields himself
    clue_v = CIPHER['v']
    clue_a = CIPHER['a']
    print_slow(COLOR_SUCCESS + f"KEY PIECES ACQUIRED: The first two letters are **V** and **A**, coded as: 1. {clue_v} and 2. {clue_a}" + COLOR_RESET)
    game.shield_pieces.extend(['V', 'A'])
    
    print_slow("You must now rendezvous with the field units.")
    time.sleep(1)
    scene_field_unit_alpha()

def scene_field_unit_alpha():
    """Scene 2: Meeting EO1 and EO2 for the U piece."""
    print_scene_header("SECTOR 2: THE ANCIENT DIG SITE")
    print_slow("You find **EO1** and **EO2** excavating a newly exposed ruin. The Blight's influence is already corrupting the air.")
    
    print(COLOR_CHARACTER + "EO1: " + COLOR_RESET, end="")
    print_slow("The next key is sealed here. It's the letter **U**, but the Blight has warped the seal. We need a specific tool to break it.")

    print(COLOR_CHARACTER + "EO2: " + COLOR_RESET, end="")
    print_slow("We can use either the **Perfuvium (P)** sonic drill, or the **Momaw (M)** plasma cutter. Choose wisely, one will destroy the key.")
    
    # Correct choice leads to U, which is coded as 'uilliatachaeh'
    correct_cipher_word = CIPHER['p'] # Perfuvium
    
    choice = get_input(f"Use the Perfuvium (P) or the Momaw (M)? Enter the cipher word: {CIPHER['p']} or {CIPHER['m']}")
    
    if choice == correct_cipher_word:
        print_slow(COLOR_SUCCESS + "SUCCESS: The Perfuvium sonic drill (P) neutralizes the seal without harm." + COLOR_RESET)
        
        # Clue U
        clue_u = CIPHER['u']
        print(COLOR_CHARACTER + "EO1: " + COLOR_RESET, end="")
        print_slow(f"Key Secured! It's **U**, coded as: {clue_u}")
        game.shield_pieces.append('U')
        print_slow(COLOR_SUCCESS + "KEY PIECE ACQUIRED: 3. U" + COLOR_RESET)
    else:
        print_slow(COLOR_ALERT + "FAILURE: The Plasma Cutter (M) was too strong. The key fragment is vaporized." + COLOR_RESET)
        print(COLOR_CHARACTER + "EO2: " + COLOR_RESET, end="")
        print_slow("We've failed, Agent. You'll have to proceed without the **U** piece.")
    
    time.sleep(2)
    scene_jake_daemon_test()

def scene_jake_daemon_test():
    """Scene 3: Meeting JakeW and Daemon for the L piece and a loyalty test."""
    print_scene_header("SECTOR 3: THE HIGH MOUNTAIN OUTPOST")
    print_slow("You meet **JakeW** and **Daemon**, securing a communications relay. They are jumpy, suspecting spies among the ranks.")
    
    print(COLOR_CHARACTER + "JAKEW: " + COLOR_RESET, end="")
    print_slow("To get the next piece, you must prove you understand the cipher. The core principle of the Lands is **Lenemketobontette**.")
    
    print(COLOR_CHARACTER + "DAEMON: " + COLOR_RESET, end="")
    print_slow("What single letter of the alphabet does the phrase **Lenemketobontette** stand for?")
    
    correct_letter = 'L'
    
    guess = get_input("Enter the single letter (e.g., K, L, M)").upper()
    
    if guess == correct_letter:
        print_slow(COLOR_SUCCESS + "ALLEGIANCE PROVEN! 'L' for Lenemketobontette, the letter of loyalty." + COLOR_RESET)
        
        # Clue L
        clue_l = CIPHER['l']
        print(COLOR_CHARACTER + "JAKEW: " + COLOR_RESET, end="")
        print_slow(f"Here is your piece: **L**, coded as: {clue_l}")
        game.shield_pieces.append('L')
        print_slow(COLOR_SUCCESS + "KEY PIECE ACQUIRED: 4. L" + COLOR_RESET)

    else:
        print_slow(COLOR_ALERT + "WRONG. You failed the test, Agent. Suspicion confirmed. You do not get the **L** piece. Go now, and do not fail the mission." + COLOR_RESET)
    
    print_slow("JakeW points you toward the extraction zone to meet the final unit.")
    time.sleep(2)
    scene_jayway_jray_extraction()

def scene_jayway_jray_extraction():
    """Scene 4: Final extraction and acquiring the T piece from JayWay and J-Ray."""
    print_scene_header("SECTOR 4: THE EXTRACTION ZONE")
    print_slow("You find **JayWay** and **J-Ray** cornered by Blight-controlled automatons. They are using the last key piece as bait.")
    
    print(COLOR_CHARACTER + "J-RAY: " + COLOR_RESET, end="")
    print_slow("We have the final letter, **T**, but we need covering fire to escape! Tell us the *full* cipher word for the letter 'I' to confirm you are real!")

    correct_cipher_word = CIPHER['i'] # illianarre
    
    guess = get_input(f"What is the cipher word for 'I'? (Hint: i-***ar*re)")
    
    if guess == correct_cipher_word:
        print_slow(COLOR_SUCCESS + "CORRECT! Illianarre! You provide expert covering fire while they disarm the automatons.")
        
        # Clue T
        clue_t = CIPHER['t']
        print(COLOR_CHARACTER + "JAYWAY: " + COLOR_RESET, end="")
        print_slow(f"We're clear! Take the final piece: **T**, coded as: {clue_t}")
        game.shield_pieces.append('T')
        print_slow(COLOR_SUCCESS + "KEY PIECE ACQUIRED: 5. T" + COLOR_RESET)
    else:
        print_slow(COLOR_ALERT + "INCORRECT. JayWay and J-Ray are forced to use the key as a distraction bomb to clear the area. They escape, but the key is lost.")
    
    print_slow("\nYou now have all available pieces. It is time to assemble the shield.")
    
    time.sleep(2)
    scene_final_activation()

def scene_final_activation():
    """Scene 5: Decrypting the final passphrase and activating the shield."""
    print_scene_header("SECTOR 5: THE AEGIS CONDUIT")
    print_slow("You stand at the ancient conduit, the heart of Royal3's defense. A five-component slot awaits the activation word.")
    
    # Use the collected letters to form the prompt
    current_word = "".join(game.shield_pieces)
    
    print_slow(COLOR_SUCCESS + f"Cipher Letters Collected: {'-'.join(game.shield_pieces)}" + COLOR_RESET)
    
    if len(game.shield_pieces) < 5:
        print_slow(COLOR_ALERT + f"WARNING: You are missing {5 - len(game.shield_pieces)} key components. You must guess the full five-letter passphrase." + COLOR_RESET)
        
    print_slow(COLOR_NARRATIVE + "The activation word is the essence of the shield's location: the **V-A-U-L-T**." + COLOR_RESET)
    
    final_passphrase = get_input("Enter the complete 5-letter activation word")
    
    if final_passphrase.upper() == game.correct_passphrase:
        print_slow(COLOR_SUCCESS + "\nACCESS KEY ACCEPTED. The Conduit roars to life!" + COLOR_RESET)
        print_slow("The legendary Aegis Shield—**VAULT**—materializes, covering the Lands of Ages. The Blight is repelled.")
        game.aegis_activated = True
    else:
        print_slow(COLOR_ALERT + "\nACCESS KEY REJECTED. The Conduit remains dormant." + COLOR_RESET)
        print_slow("The Blight advances. You failed to piece together the final word.")
        game.aegis_activated = False

    time.sleep(3)
    scene_epilogue()

def scene_epilogue():
    """Scene 6: Conclusion and final status."""
    print_scene_header("CONCLUSION: ROYAL3 LANDS OF AGES III")
    
    if game.aegis_activated:
        print(COLOR_SUCCESS + "\n<<< THE SHIELD ENDURES! >>>" + COLOR_RESET)
        print_slow("The Blight is defeated. Director Tahkmahnelle and the hero men—Battle Shields, EO1, EO2, JakeW, Daemon, JayWay, and J-Ray—salute your service.")
        print_slow(f"The secrets long ago hidden have revived Royal3, thanks to Agent {game.player_name}.")
    else:
        print(COLOR_ALERT + "\n<<< BLIGHT CONTINUES >>>" + COLOR_RESET)
        print_slow("The Blight consumes the outer sectors. You must go into deep cover, hoping to find the remaining cipher pieces for another attempt.")
        print_slow("The hero men scatter, preparing for the next phase of the endless war.")

    print(COLOR_HEADER + "\n--- MISSION REPORT ---" + COLOR_RESET)
    print(f"Collected Shield Keys: {len(game.shield_pieces)}/5")
    print(f"Activation Status: {'Aegis Shield Active' if game.aegis_activated else 'Blight Advance'}")
    print(COLOR_HEADER + "----------------------" + COLOR_RESET)
    print_slow("\nProgram Terminating. Your legacy awaits.")

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

