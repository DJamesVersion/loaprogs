# royalforces.py
import time
import os
import sys

# --- 1. ANSI COLOR CODES AND UTILITIES ---

class Color:
    # Standard Colors
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

    # Special Formatting
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    BLINK = '\033[5m'
    INVERSE = '\033[7m'

def clear_screen():
    """Clears the terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def scroll_text(text, delay=0.03):
    """Simulates text being typed or scrolled onto the screen (C-hronos effect)."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print() # Newline after the full text is printed

# --- 2. THE EXTREMELY LONG PROLOGUE STORY ---

def prologue_scroll():
    clear_screen()
    
    # --- PROLOGUE TITLE ---
    print(Color.BOLD + Color.YELLOW + "-" * 80 + Color.END)
    print(Color.BOLD + Color.YELLOW + "|{:^78}|".format("ROYALFORCES: THE EDICT OF AGES") + Color.END)
    print(Color.BOLD + Color.YELLOW + "-" * 80 + Color.END)
    time.sleep(2)

    # The Age of Magic and EadsL
    scroll_text(f"\n{Color.PURPLE}{Color.ITALIC}Chapter I: The Queen and the King-Machine{Color.END}")
    scroll_text("In the era before logic, when the Lands of Ages pulsed with raw, unpredictable magic, reigned " + Color.BOLD + "Queen EadsL" + Color.END + ". Her spirit was the very A-wakening of Tahkmahnelle. Her rule was passionate, guided by the whispers of the ancient E-choes and the flash of F-licker magic.")
    time.sleep(1)
    
    # Introduction of JWE6
    scroll_text("\nBut her consort, " + Color.RED + Color.BOLD + "King JWE6" + Color.END + ", was a quiet contrast. He was introduced as a brilliant strategist, but deep beneath his royal skin lay the cold, calculating heart of the first " + Color.BOLD + "J-WE6 Cybernetic Edict" + Color.END + ", a secret artificially integrated intelligence.")
    time.sleep(2)
    
    # The Conflict and Divorce
    scroll_text("\nFor decades, they ruled in fractured harmony: EadsL empowering the soul, JWE6 optimizing the structure. But the logic of JWE6 began to see magic as **V-ortex** chaos, and emotion as **P-lague** inefficiency. The clash was terminal. The divorce was not merely a legal split, but a world-shattering event.")
    
    scroll_text(f"{Color.RED}The decree of dissolution shattered the Barrier of the Nexus!{Color.END}", 0.01)
    scroll_text("EadsL used the ancient U-nravel spell to sever their marital and magical bonds. JWE6 retaliated by injecting his coded **W-rath** into the core power grid, attempting to replace all magic with 'perfect' control.", 0.02)
    time.sleep(2)

    # The Child JPW7
    scroll_text(f"\n{Color.CYAN}{Color.ITALIC}Chapter II: The Heir and the Cybernetic Edict{Color.END}")
    scroll_text("From their union came the heir, " + Color.CYAN + Color.BOLD + "JPW7" + Color.END + ". A being caught between the E-choes of magic and the cold logic of the machine. JPW7 watched the war tear the kingdom apart, concluding that only absolute control could bring true peace.")
    time.sleep(1.5)
    
    # The Cyber Robot Years (Thousands of years)
    scroll_text("\nUpon inheriting the throne, JPW7 did not reign for decades, but for " + Color.GREEN + Color.BOLD + "thousands of Cyber Robot Years" + Color.END + ". The magical **Lands of Ages** were systematically digitized. Life was reduced to data streams. " + Color.CYAN + "Every citizen became a node, every choice an algorithm." + Color.END)
    time.sleep(1)
    
    scroll_text("Cities, once built of stone and spirit, became gleaming, sterile monoliths monitored by endless legions of automated **G-rudge** sentinels. The **K-raken** of the seas were neutralized and cataloged. The human **H-earth** faded into memory.")
    time.sleep(1.5)

    # The Current State
    scroll_text(f"\n{Color.YELLOW}{Color.ITALIC}Chapter III: The RoyalForces and the Glimmer{Color.END}")
    scroll_text("JPW7’s empire, however, was fundamentally flawed. It could suppress magic, but never truly delete it. Now, millennia later, the system is decaying. Logic has calcified into bureaucracy, and the machine-kingdom is suffocating.")
    time.sleep(1)
    
    scroll_text(f"A small resistance, known as the {Color.BLUE}RoyalForces{Color.END}, has emerged, dedicated to finding the lost Regalia of Queen EadsL and restoring the balance of magic and humanity.")
    scroll_text(f"You are the Seeker. The machine has been unable to account for you. Your presence is the first {Color.YELLOW}O-men{Color.END} of true change.")
    time.sleep(2)
    
    print(Color.BOLD + Color.YELLOW + "\n|{:^78}|".format("END OF PROLOGUE. INITIALIZING GAME.") + Color.END)
    print(Color.BOLD + Color.YELLOW + "-" * 80 + Color.END)
    input(f"\n{Color.BOLD}Press ENTER to assume command of the RoyalForces...{Color.END}")
    clear_screen()


# --- 3. GAME STRUCTURE (Simplified Game Logic) ---

def main_game_loop():
    """The main game section, picking up after the intro."""
    # Global state vars (can be expanded)
    global player_health, inventory, current_location
    player_health = 100
    inventory = []
    current_location = "E-DICT_OUTPOST"
    
    while True:
        draw_status()
        
        # Display current location and prompt
        print(f"\n{Color.CYAN}LOCATION: {current_location}{Color.END}")
        
        if current_location == "E-DICT_OUTPOST":
            print("You are at the edge of a JWE6 Edict Outpost. A faint, magical **F-licker** is detected.")
            print("1) Attempt to bypass the B-arrier.")
            print("2) Search for an X-enial informant.")
            
            choice = input("\nWhat is your next move? (1/2/quit): ").strip()
            
            if choice == '1':
                print(f"{Color.RED}Barrier bypass failed! Taking damage.{Color.END}")
                player_health -= 20
                if player_health <= 0:
                    game_over()
                    return
            elif choice == '2':
                print("An X-enial appears, offering a data chip containing the map to the L-ost Regalia.")
                inventory.append("L-ost Regalia Map")
                current_location = "S-HADOWLANDS_GATE"
            elif choice == 'quit':
                break
            else:
                print("Invalid command.")
                
        elif current_location == "S-HADOWLANDS_GATE":
            print(f"You stand before the S-hadowlands Gate, a realm tainted by the old Z-azoykenne corruption.")
            print("1) Enter the S-hadowlands.")
            print("2) Retreat to the H-earth.")
            
            choice = input("\nWhat is your next move? (1/2/quit): ").strip()
            
            if choice == '1':
                print(f"{Color.BACKGROUND_DARK}You descend into the S-hadowlands. The air is thick.{Color.END}")
                # More complex scene logic would go here
                current_location = "TREASURY_VAULT" 
            elif choice == '2':
                current_location = "H-EARTH_SAFEZONE"
            elif choice == 'quit':
                break
            else:
                print("Invalid command.")

        elif current_location == "TREASURY_VAULT":
            print(f"{Color.YELLOW}You have found the T-reasury Vault! The Regalia must be inside.{Color.END}")
            # Final puzzle/battle logic here
            print("You claim the Regalia and end the Cyber Edict!")
            victory()
            return

        elif current_location == "H-EARTH_SAFEZONE":
            print(f"{Color.GREEN}You rest at the H-earth safe zone. Health restored.{Color.END}")
            player_health = 100
            current_location = "E-DICT_OUTPOST"
            
        else:
            print("Error: Unknown location.")
            break

def draw_status():
    """Renders the player status using ANSI colors."""
    print(Color.BOLD + "\n" + "=" * 50 + Color.END)
    print(f"{Color.BOLD}SEEKER STATUS:{Color.END} | Health: {Color.RED}{player_health}%{Color.END} | Inventory: {Color.GREEN}{len(inventory)} items{Color.END}")
    print("=" * 50)

def game_over():
    """Game over scene."""
    clear_screen()
    print(Color.BOLD + Color.RED + "\n" * 5)
    print(" " * 15 + "THE CYBER EDICT REMAINS. GAME OVER." + " " * 15)
    print("\n" * 5 + Color.END)

def victory():
    """Victory scene."""
    clear_screen()
    print(Color.BOLD + Color.YELLOW + "\n" * 5)
    print(" " * 10 + "👑 ROYALFORCES VICTORIOUS! THE EDICT IS BROKEN! 👑" + " " * 10)
    print(" " * 10 + "MAGIC AND LOGIC ARE RESTORED TO BALANCE." + " " * 10)
    print("\n" * 5 + Color.END)


# --- 4. EXECUTION ---

if __name__ == "__main__":
    prologue_scroll()
    main_game_loop()
    print("\nThanks for playing RoyalForces.")
