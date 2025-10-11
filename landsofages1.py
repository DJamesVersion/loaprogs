# landsofages1.py
import os
import sys
import time

# --- ANSI COLOR CODES ---
class Color:
    HEADER = '\033[95m'
    MAGIC = '\033[94m'      # Blue
    HEALTH = '\033[92m'     # Green
    ENEMY = '\033[91m'      # Red
    ITEM = '\033[93m'       # Yellow
    BOLD = '\033[1m'
    RESET = '\033[0m'

# --- GLOBAL GAME VARIABLES ---
PLAYER_NAME = ""
PLAYER_CLASS = ""
HEALTH = 100
POWER = 50
HAS_BATOBWATCHAEH = False

# --- UTILITIES ---

def clear_screen():
    """Clears the terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def game_over():
    clear_screen()
    print(Color.BOLD + Color.ENEMY + "\n" * 5)
    print("{:^60}".format("💀 THE ECHOES FADE... GAME OVER! 💀"))
    print("\n" * 5 + Color.RESET)
    sys.exit()

def display_status():
    """Renders the player status using ANSI colors."""
    artifact_status = "B-atobwatchaeh (Aquired)" if HAS_BATOBWATCHAEH else "None"
    
    print(Color.BOLD + "=" * 60 + Color.RESET)
    print(f"{Color.BOLD}NAME:{Color.RESET} {PLAYER_NAME} | {Color.BOLD}CLASS:{Color.RESET} {PLAYER_CLASS}")
    print(f"{Color.HEALTH}HEALTH:{Color.RESET} {HEALTH} | {Color.MAGIC}POWER:{Color.RESET} {POWER}")
    print(f"{Color.ITEM}ARTIFACT:{Color.RESET} {artifact_status}")
    print(Color.BOLD + "=" * 60 + Color.RESET)

def take_damage(amount):
    """Reduces health and checks for game over."""
    global HEALTH
    HEALTH -= amount
    print(f"{Color.ENEMY}You take {amount} damage. Health remaining: {HEALTH}{Color.RESET}")
    if HEALTH <= 0:
        game_over()
        
def wait_for_enter(prompt="Press ENTER to continue..."):
    """Pauses execution until the user presses Enter."""
    input(f"\n{Color.BOLD}{prompt}{Color.RESET}")

# --- SCENES (Key Plot Points) ---

# A - Ariatnah: Start
def scene_ariatnah():
    global PLAYER_CLASS, POWER, HEALTH
    clear_screen()
    print(Color.HEADER + "#####################################################" + Color.RESET)
    print(Color.HEADER + "## A: ARIATNAH - The Village of Whispering Echoes  ##" + Color.RESET)
    print(Color.HEADER + "#####################################################" + Color.RESET)
    print("You wake in **A-riatnah**, a village untouched by the true history of Tahkmahnelle.")
    print("The **J-ampejinne** (Elder Council) call you, the Seeker, to choose a path.")
    
    print("\nWhich path do you choose?")
    print("1) The Scholar (**C-'illiatnah**): +20 Power")
    print("2) The Fighter (**F-'illianarre**): +30 Health")
    print("3) The Rogue (**I-llianarre**)")
    print("4) The Sage (**Y-'uilliatachaeh**): +30 Power")
    
    choice = input("\nEnter your choice (1-4): ").strip()

    if choice == '1':
        PLAYER_CLASS = "C-illiatnah (Scholar)"
        POWER += 20
    elif choice == '2':
        PLAYER_CLASS = "F-illianarre (Fighter)"
        HEALTH += 30
    elif choice == '3':
        PLAYER_CLASS = "I-llianarre (Rogue)"
    elif choice == '4':
        PLAYER_CLASS = "Y-uilliatachaeh (Sage)"
        POWER += 30
    else:
        print(f"{Color.ENEMY}Invalid choice. The path of the Scholar is thrust upon you.{Color.RESET}")
        PLAYER_CLASS = "C-illiatnah (Scholar)"
        POWER += 20
    
    print(f"\nThe J-ampejinne nod. You are now the {Color.BOLD}{PLAYER_CLASS}{Color.RESET}.")
    wait_for_enter("Press ENTER to continue to the D-iadowatchaeh...")
    scene_diadowatchaeh()

# D - Diadowatchaeh: Choice
def scene_diadowatchaeh():
    global HAS_BATOBWATCHAEH, HEALTH
    clear_screen()
    print(Color.HEADER + "#####################################################" + Color.RESET)
    print(Color.HEADER + "## D: DIADOWATCHAEH - The Shadowed Path            ##" + Color.RESET)
    print(Color.HEADER + "#####################################################" + Color.RESET)
    display_status()
    print("You stand at the edge of the **D-iadowatchaeh**, the dark forest.")
    print("Legend says the **B-atobwatchaeh** (Artifact) is hidden here, guarded by the **N-ano** (Shadow).")
    
    print("\nWhat is your action?")
    print("1) Search for the **B-atobwatchaeh** immediately (Risking N-ano's trap).")
    print("2) Try to bypass the forest and seek the **K-ajoinkenne** (Mountain Peaks).")
    
    choice = input("\nEnter your choice (1-2): ").strip()

    if choice == '1':
        print(f"{Color.ENEMY}A shadowy tendril, the **Z-azoykenne** (Corruption), lashes out!{Color.RESET}")
        take_damage(25)
        print("You fought it off and found a glimmering artifact!")
        HAS_BATOBWATCHAEH = True
        print(f"{Color.ITEM}You have acquired the B-atobwatchaeh! (+15 HEALTH){Color.RESET}")
        HEALTH += 15
        wait_for_enter("Press ENTER to leave the dark forest...")
        scene_kajoinkenne()
    elif choice == '2':
        print("You carefully skirt the D-iadowatchaeh, avoiding the Z-azoykenne.")
        wait_for_enter("Press ENTER to begin the climb to K-ajoinkenne...")
        scene_kajoinkenne()
    else:
        print(f"{Color.ENEMY}You hesitate and waste time. You take a minor injury from an X-iangxong.{Color.RESET}")
        take_damage(5)
        wait_for_enter()
        scene_diadowatchaeh() # Loop back

# K - Kajoinkenne: Mountain Peaks
def scene_kajoinkenne():
    clear_screen()
    print(Color.HEADER + "#####################################################" + Color.RESET)
    print(Color.HEADER + "## K: KAJOINKENNE - The Mountain Peaks             ##" + Color.RESET)
    print(Color.HEADER + "#####################################################" + Color.RESET)
    display_status()
    print("You reach the **K-ajoinkenne**. The winds carry the power of **S-iataeh** (Air).")
    print("A solitary figure, the **R-oykenne** (King) is seen overseeing the construction of a fortress.")
    print("You must find the **L-enemketobontette** (Great Library) to learn about **M-omaw** (The Quest).")

    print("\nYour path divides again.")
    print("1) Use the **G-agoikenne** (Portal) to bypass the R-oykenne's territory (Risky).")
    print("2) Sneak through the construction to find the library (Need I-llianarre skills).")
    
    choice = input("\nEnter your choice (1-2): ").strip()

    if choice == '1':
        print(f"{Color.ENEMY}You enter the G-agoikenne! The power drain is intense.{Color.RESET}")
        take_damage(10)
        scene_lenemketobontette()
    elif choice == '2':
        if "Rogue" in PLAYER_CLASS:
            print(f"{Color.HEALTH}Your rogue skills let you slip past the guards with ease. A success!{Color.RESET}")
            scene_lenemketobontette()
        else:
            print(f"{Color.ENEMY}You are caught by the guards! You must fight.{Color.RESET}")
            take_damage(40)
            print("You barely escape and flee into the portal!")
            scene_lenemketobontette()
    else:
        print(f"{Color.ENEMY}You rest for too long. A mountain monster strikes!{Color.RESET}")
        take_damage(10)
        scene_kajoinkenne()

# L - Lenemketobontette: The Library/End Game Setup
def scene_lenemketobontette():
    clear_screen()
    print(Color.HEADER + "#####################################################" + Color.RESET)
    print(Color.HEADER + "## L: LENEMKETOBONTETTE - The Great Library        ##" + Color.RESET)
    print(Color.HEADER + "#####################################################" + Color.RESET)
    display_status()
    print("Within the **L-enemketobontette**, you discover the truth: **M-omaw** is not a deity, but the balanced state of Tahkmahnelle.")
    print("The R-oykenne is trying to seize the **O-ichenne** (Orb) to fully channel the **Z-azoykenne** (Corruption).")
    print("You find the text describing the **Q-uaristenne** (Final Puzzle) and the power of **U-illiatachaeh** (Universal Key).")
    
    wait_for_enter("\nYour final step is to solve the Q-uaristenne and confront the R-oykenne in the T-etnobautte (Final Trial). Press ENTER...")
    scene_tetnobautte()

# T - Tetnobautte: Final Trial
def scene_tetnobautte():
    clear_screen()
    print(Color.HEADER + "#####################################################" + Color.RESET)
    print(Color.HEADER + "## T: TETNOBAUTTE - The Final Trial                ##" + Color.RESET)
    print(Color.HEADER + "#####################################################" + Color.RESET)
    display_status()
    print("You stand before the R-oykenne, who holds the pulsing O-ichenne, ready to unleash the Z-azoykenne.")
    
    # Q-uaristenne (Final Puzzle)
    print("\nTHE Q-UARISTENNE: What is the source of **S-tihuu** (Earth) and **S-iataeh** (Air)?")
    final_answer = input("Enter your answer (One Word, Hint: The world itself): ").strip()
    
    if final_answer.lower() in ["tahkmahnelle", "t-ahkmahnelle", "tetnobautte"]:
        print(f"{Color.MAGIC}The Q-uaristenne is solved! The U-illiatachaeh (Universal Key) is revealed!{Color.RESET}")
        if HAS_BATOBWATCHAEH:
            print(f"{Color.HEALTH}Using the B-atobwatchaeh, you channel the U-illiatachaeh into the O-ichenne, purifying it.{Color.RESET}")
            print(Color.BOLD + "\n🏆 VICTORY! Tahkmahnelle is saved, and M-omaw is restored! 🏆" + Color.RESET)
        else:
            print("You solve the puzzle, but without the B-atobwatchaeh, you can only seal the Z-azoykenne away for a time.")
            print(Color.ITEM + "\nACHIEVEMENT: TEMPORARY PEACE." + Color.RESET)
    else:
        print(f"{Color.ENEMY}The puzzle is wrong! The R-oykenne laughs and unleashes his power.{Color.RESET}")
        take_damage(100) # Instant Game Over (redundant but clean)
    
    print("\nThank you for playing LandsofAges.")
    sys.exit()

# --- MAIN GAME EXECUTION ---

def start_game():
    global PLAYER_NAME
    clear_screen()
    print(Color.BOLD + Color.HEADER + "=" * 60 + Color.RESET)
    print(Color.BOLD + Color.HEADER + "{:^60}".format("WELCOME TO LANDSOFAGES: A TAHKMAHNELLE EPIC") + Color.RESET)
    print(Color.BOLD + Color.HEADER + "=" * 60 + Color.RESET)
    
    PLAYER_NAME = input("Enter your Seeker's name: ").strip()
    
    if not PLAYER_NAME:
        PLAYER_NAME = "Unnamed Seeker"
    
    print(f"\nHello, {PLAYER_NAME}. Your journey begins in **A-riatnah** (A).")
    wait_for_enter("Press ENTER to begin...")
    
    scene_ariatnah()

if __name__ == "__main__":
    start_game()
