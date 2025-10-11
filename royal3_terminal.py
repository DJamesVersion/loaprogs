# royal3_terminal.py
import time
import os

# --- 1. ANSI COLOR CODES (The "Graphics" Engine) ---
# Note: These colors work in most modern UNIX/Linux terminals.
class Color:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m' # Reset color
    BOLD = '\033[1m'
    BACKGROUND_DARK = '\033[40m'
    BACKGROUND_BLUE = '\033[44m'

# --- 2. GAME STATE ---
current_scene = "A_AWAKENING"
player_health = 100
runes_collected = 0
story_text = ""

# --- 3. VISUALIZATION FUNCTIONS (ASCII Art & Effects) ---

def clear_screen():
    """Clears the terminal for a new scene."""
    # Command to clear screen (works on most UNIX-like systems)
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_hud():
    """Draws the player status (Q-uest tracker)."""
    print(Color.BOLD + "-" * 50 + Color.END)
    print(f"  Health: {Color.RED}{player_health}{Color.END} | Runes: {Color.YELLOW}{runes_collected}/5{Color.END}")
    # P-lague Check (Example of a Debuff visualization)
    if player_health < 50:
         print(f"  {Color.GREEN}{Color.BOLD}P-lague{Color.END}: Afflicted! Seeking H-uilliatachaeh.")
    print(Color.BOLD + "-" * 50 + Color.END)

def draw_scene_awakening():
    """Visualization for A-wakening (A)."""
    print(Color.BLUE + "=" * 60 + Color.END)
    print(f"{Color.BLUE}|{Color.END}  {Color.BOLD}A-WAKENING{Color.END}: The Royal Crypt  {Color.BLUE}|{Color.END}")
    print(Color.BLUE + "=" * 60 + Color.END)
    print("A sacred space, waiting for the Seeker's choice.")
    # E-choes (E): Example of a flickering text effect
    print(f"{Color.CYAN}E-choes whisper: 'Choose your new Royal path.'{Color.END}")

def draw_scene_deluge():
    """Visualization for D-eluge (D) and G-rudge (G)."""
    print(Color.BACKGROUND_BLUE + "~" * 60 + Color.END)
    print(Color.BLUE + "   D-ELUGE: The waves crash around you.   " + Color.END)
    print(Color.BACKGROUND_BLUE + "≈" * 60 + Color.END)
    
    # G-rudge (G): ASCII Enemy Sprite
    print(Color.RED + Color.BOLD + "    (G) R-udge General    " + Color.END)
    print("      /\\_/")
    print("     |X_X|  <- GRUDGE")
    print("     /   \\")

def draw_scene_kraken():
    """Visualization for K-raken (K)."""
    print(Color.PURPLE + "=" * 60 + Color.END)
    print("  K-RAKEN: The Tentacled Terror  ")
    # K-raken (K): Large ASCII Tentacle Art
    print("  @##@      @##@")
    print("   \\___/\\___/   <-- TENTACLES")
    print(Color.PURPLE + "=" * 60 + Color.END)

# --- 4. GAME LOGIC / SCENE MANAGEMENT ---

def set_scene(scene_name, text_content):
    """Changes the scene and updates the story text."""
    global current_scene, story_text
    current_scene = scene_name
    story_text = text_content
    # J-ourney (J): Time delay for an effective transition
    print(f"\n{Color.YELLOW}— J-ourneying to a new land...{Color.END}")
    time.sleep(1) 

def handle_input():
    """Manages the main loop and user choices."""
    global player_health, runes_collected

    choice = input("\nEnter your choice (1, 2, or 'status'): ").strip().lower()

    if choice == 'status':
        clear_screen()
        draw_hud()
        print(Color.CYAN + story_text + Color.END)
        return

    clear_screen()

    if current_scene == "A_AWAKENING":
        if choice == '1':
            set_scene("D_DELUGE", "You choose the path of the D-eluge. A menacing figure awaits.")
        else:
            print("Invalid choice. The path of the D-eluge opens anyway.")
            set_scene("D_DELUGE", "You are forced onto the path of the D-eluge.")

    elif current_scene == "D_DELUGE":
        # F-licker (F): Unstable energy damage event
        if choice == '1':
            player_health -= 25
            print(f"{Color.RED}F-licker{Color.END} energy strikes! You fought off G-rudge but are wounded.")
            runes_collected += 1
            set_scene("K_KRAKEN", "The first Rune is yours. Now, the icy depths of K-raken's lair.")
        else:
            player_health -= 5
            print("You sneak past G-rudge. Minor F-licker damage taken.")
            runes_collected += 1
            set_scene("K_KRAKEN", "The first Rune is yours. Now, the icy depths of K-raken's lair.")
            
    # Add more scene logic for K_KRAKEN, N_NEXUS, etc.

# --- 5. MAIN GAME LOOP ---

def start_game():
    clear_screen()
    print(Color.BOLD + "=================================================" + Color.END)
    print(Color.BOLD + Color.PURPLE + "   ROYAL3_LANDSOFAGES-00: The Visual Echo" + Color.END)
    print(Color.BOLD + "=================================================" + Color.END)
    input("Press ENTER to begin your quest to restore the Royal Line...")
    
    set_scene("A_AWAKENING", "The journey begins in the royal A-wakening.")

    while True:
        clear_screen()
        draw_hud()

        # Render the specific scene visualization
        if current_scene == "A_AWAKENING":
            draw_scene_awakening()
            print("\n1) Journey to the D-eluge (D)")
        elif current_scene == "D_DELUGE":
            draw_scene_deluge()
            print("\n1) Fight G-rudge (G) directly.")
            print("2) Try to avoid G-rudge.")
        elif current_scene == "K_KRAKEN":
            draw_scene_kraken()
            print("\n1) Seek the C-hronos (C) artifact.")
            print("2) Engage the K-raken (K).")
            
        print(Color.CYAN + "\n" + story_text + Color.END)

        if runes_collected == 5:
            # Z-ephyr (Z) - Final Victory Visualization
            clear_screen()
            print(Color.BOLD + Color.BACKGROUND_BLUE + "\n" * 5)
            print(" " * 15 + "✨ THE Z-EPHYR PURIFIES THE LANDS! ✨" + " " * 15)
            print(" " * 15 + "👑 ROYAL LINE RESTORED! VICTORY! 👑" + " " * 15)
            print("\n" * 5 + Color.END)
            break
            
        if player_health <= 0:
            print(Color.BOLD + Color.RED + "\n--- THE ROYAL LINE ENDS HERE. GAME OVER ---" + Color.END)
            break
            
        handle_input()

if __name__ == "__main__":
    start_game()
