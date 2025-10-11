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
    print(COLOR_HEADER + "===================================================" + COLOR_RESET)
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
        self.clues = 0
        self.tahkmahnelle_trust = 5  # Trust level (0 = hostile, 10 = loyal)
        self.witness_silenced = False
        self.evidence_acquired = False
        self.justice_served = False
        self.player_name = "Investigator"

game = GameState()

# --- Scene Definitions ---

def scene_prologue():
    """Scene 1: Introduction and initial briefing."""
    print(COLOR_TITLE + """
   __                                    ___ 
  / /  ___   __ _  _ __   ___   _ __    |__ \\
 / /  / _ \ / _` || '_ \ / _ \ | '_ \    / /
/ /__|  __/| (_| || | | | (_) || | | |  |_|
\____/\___| \__,_||_| |_|\___/ |_| |_|  (_)
    """ + COLOR_RESET)
    
    print(COLOR_TITLE + "=== TAHKMAHNELLE: ADVANCED ADVENTURE ===" + COLOR_RESET)
    print_slow("\nWelcome, Investigator. You have been summoned by the Royal Edict.")
    
    game.player_name = get_input("What is your code name?").title()
    if not game.player_name:
        game.player_name = "Investigator"

    print_slow(f"\nAh, {game.player_name}. The Royal3 Lands of Ages are in peril. The ancient Tahkmahnelle Mining Guild, once a symbol of stability, is now riddled with corruption.")
    print_slow("Your mission is to infiltrate, investigate, and present irrefutable evidence of unlawful extraction and betrayal against the Crown.")
    
    print_scene_header("SECTOR 1: THE TAINTED SHORE")
    print_slow("You arrive at the edge of the Sunken Quarry, where Tahkmahnelle's operations begin. It is here you must gather your first clue.")
    
    choice = get_input("Do you search the abandoned 'Processing Hut' (1) or the secure 'Main Dock' (2)?")
    
    if choice == '1':
        print_slow("You enter the desolate Processing Hut. A thin layer of dust covers everything, but you find a discarded, encrypted ledger.")
        game.clues += 1
        print_slow(COLOR_SUCCESS + "CLUE ACQUIRED: Encrypted Ledger." + COLOR_RESET)
    else:
        print_slow("You attempt to access the Main Dock. The security is unexpectedly high; a large guard spots you. You are forced to retreat, losing valuable time.")
        print_slow(COLOR_ALERT + "CLUE MISSED: High Risk Encounter." + COLOR_RESET)
        game.tahkmahnelle_trust -= 1
    
    time.sleep(1)
    scene_deep_exploration()

def scene_deep_exploration():
    """Scene 2: Deeper investigation and risk/reward decision."""
    print_scene_header("SECTOR 2: THE WHISPERING CAVERNS")
    print_slow("Deep within the mines, the air is thick with the smell of extracted 'Aegis Stone'—far more than is legally permitted.")
    print_slow("You locate a foreman, Elara, who seems distraught. She is a potential witness to the illegal operations.")

    choice = get_input("How do you approach Elara? Subtly offer protection (1) or aggressively demand the truth (2)?")
    
    if choice == '1':
        print_slow("You quietly explain your Royal mandate and offer her safe passage out of the Lands of Ages. She agrees, but demands you secure the 'Key Cache'.")
        game.clues += 1
        print_slow(COLOR_SUCCESS + "CLUE ACQUIRED: Witness Elara (Conditional). Key Cache location revealed." + COLOR_RESET)
        scene_key_cache(True)
    elif choice == '2':
        print_slow("Your aggressive approach frightens Elara. Before she can speak, a shadow passes over the entrance. She is quickly and silently removed by Tahkmahnelle enforcers.")
        game.witness_silenced = True
        print_slow(COLOR_ALERT + "CRITICAL FAILURE: Key Witness Silenced." + COLOR_RESET)
        scene_key_cache(False)
    else:
        print_slow("You hesitate, unsure how to proceed. Elara vanishes into the darkness. You must find the cache alone.")
        scene_key_cache(False)

def scene_key_cache(elara_assisted):
    """Scene 3: Retrieving the crucial evidence from the Key Cache."""
    print_scene_header("SECTOR 3: THE VAULT OF AGES")
    
    if elara_assisted:
        print_slow("Thanks to Elara, you know the cache is beneath a false floor. You approach cautiously.")
        # Automatic success path for acquiring evidence
        print_slow("You easily locate the hidden compartment. Inside is a detailed manifest proving the illegal trade.")
        game.clues += 2
        game.evidence_acquired = True
        print_slow(COLOR_SUCCESS + "EVIDENCE ACQUIRED: The Master Manifest. Case closed." + COLOR_RESET)
    else:
        print_slow("The Vault is heavily guarded. Without a guide, you must risk direct confrontation to find the Cache.")
        
        if game.tahkmahnelle_trust > 4:
            print_slow("You manage to sneak past the guards using the 'Main Dock' information you gathered previously. The cache is located, but it's booby-trapped.")
            game.evidence_acquired = True
            game.clues += 1
            print_slow(COLOR_SUCCESS + "EVIDENCE ACQUIRED: Partial Manifest. Case can proceed." + COLOR_RESET)
        else:
            print_slow("The lack of trust and high alert levels make entry impossible. You trigger an alarm and must flee before securing the evidence.")
            game.evidence_acquired = False
            print_slow(COLOR_ALERT + "EVIDENCE MISSING: You only have your initial ledger and your word." + COLOR_RESET)

    time.sleep(2)
    scene_royal_court()

def scene_royal_court():
    """Scene 4: Final confrontation and judgment."""
    print_scene_header("THE ROYAL COURT OF JUSTICE")
    print_slow("You stand before the Royal Council. Director Tahkmahnelle is also present, smug and defiant.")
    print_slow(f"The Head Royal Advisor addresses you, '{game.player_name}, present your findings against the Tahkmahnelle Guild.'")

    # Determine the verdict based on collected evidence
    if game.evidence_acquired and game.clues >= 3 and not game.witness_silenced:
        # Full Success Path
        print_slow(COLOR_SUCCESS + "\n--- Verdict: IRREFUTABLE ---" + COLOR_RESET)
        print_slow("You present the Master Manifest and introduce the protected witness, Elara. Tahkmahnelle's face falls.")
        print_slow("The evidence is overwhelming. The Council votes unanimously.")
        game.justice_served = True
    elif game.evidence_acquired and game.clues >= 2:
        # Partial Success Path
        print_slow(COLOR_ALERT + "\n--- Verdict: SUBSTANTIAL ---" + COLOR_RESET)
        print_slow("You present the Partial Manifest. Tahkmahnelle employs a masterful legal defense, citing procedural errors.")
        print_slow("The Council is divided, but the documented illegal extraction is enough to warrant his immediate arrest and guild dissolution.")
        game.justice_served = True
    else:
        # Failure Path
        print_slow(COLOR_ALERT + "\n--- Verdict: INSUFFICIENT ---" + COLOR_RESET)
        print_slow("You present only the initial Encrypted Ledger. Tahkmahnelle's counsel dismisses it as a 'misfiled accounting error'.")
        print_slow("Without the Manifest or a witness, the Council must rule in favor of Tahkmahnelle. You have failed.")
        game.justice_served = False
        game.tahkmahnelle_trust = 0 # Now actively hunted

    time.sleep(3)
    scene_epilogue()

def scene_epilogue():
    """Scene 5: Conclusion and final status."""
    print_scene_header("RESOLUTION: ROYAL3 LANDS OF AGES")
    
    if game.justice_served:
        print(COLOR_SUCCESS + "\n<<< JUSTICE PREVAILS! >>>" + COLOR_RESET)
        print_slow(f"Director Tahkmahnelle has been apprehended and the Guild's assets seized.")
        print_slow(f"The Royal3 Lands are safe, for now. Investigator {game.player_name}, your service is etched in the scrolls of ages.")
    else:
        print(COLOR_ALERT + "\n<<< ADVENTURE FAILED >>>" + COLOR_RESET)
        print_slow("Tahkmahnelle walks free. He stares directly at you, a chilling smile on his face.")
        print_slow(f"Your investigation has been terminated. Investigator {game.player_name}, you are now marked as an enemy of the Guild.")
        print_slow("The Royal Edict has been overruled. The fight for justice continues from the shadows.")

    print(COLOR_HEADER + "\n--- STATS ---" + COLOR_RESET)
    print(f"Clues Found: {game.clues}/4")
    print(f"Evidence Status: {'Acquired' if game.evidence_acquired else 'Missing'}")
    print(f"Witness Status: {'Safe' if not game.witness_silenced else 'Silenced'}")
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

