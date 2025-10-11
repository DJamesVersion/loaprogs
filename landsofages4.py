# landsofages4.py
import os
import sys
import time
import random

# --- ANSI COLOR CODES ---
class Color:
    HEADER = '\033[95m'
    TIME = '\033[93m'       # Yellow
    HEALTH = '\033[92m'     # Green
    ENEMY = '\033[91m'      # Red
    ITEM = '\033[96m'       # Cyan
    BOLD = '\033[1m'
    RESET = '\033[0m'

# --- GLOBAL GAME VARIABLES ---
PLAYER_NAME = "Operative"
HEALTH = 100
TIME_LEFT = 20  # Total turns before cataclysm
PLAGUE_DRAIN = 5 # P-lague health drain per turn
HAS_OMEN = False
HAS_ZEPHYR = False
CURRENT_LOCATION = "ENTRANCE"

# --- UTILITIES ---

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def game_over(reason="Time ran out"):
    clear_screen()
    print(Color.BOLD + Color.ENEMY + "\n" * 5)
    print("{:^60}".format("MISSION FAILURE: CATACLYSMIC SURGE!"))
    print(f"{:^60}".format(f"Reason: {reason}."))
    print("\n" * 5 + Color.RESET)
    sys.exit()

def victory():
    clear_screen()
    print(Color.BOLD + Color.ITEM + "\n" * 5)
    print("{:^60}".format("✅ WRATH DEACTIVATED! TAHKMAHNELLE IS SAFE! ✅"))
    print(f"{:^60}".format(f"Mission complete with {TIME_LEFT} seconds remaining."))
    print("\n" * 5 + Color.RESET)
    sys.exit()

def display_status():
    """Renders the player status and timer."""
    health_color = Color.HEALTH if HEALTH > 30 else Color.ENEMY
    time_color = Color.TIME if TIME_LEFT > 5 else Color.ENEMY
    
    print(Color.BOLD + "=" * 60 + Color.RESET)
    print(f"{Color.BOLD}OPERATIVE:{Color.RESET} {PLAYER_NAME} | {health_color}HEALTH:{Color.RESET} {HEALTH}")
    print(f"{time_color}TIME LEFT:{Color.RESET} {TIME_LEFT} | {Color.ITEM}PLAGUE DRAIN:{Color.RESET} {PLAGUE_DRAIN}")
    print(f"Clues: {'O-men Found' if HAS_OMEN else 'None'} | Stabilizer: {'Z-ephyr Active' if HAS_ZEPHYR else 'None'}")
    print(Color.BOLD + "=" * 60 + Color.RESET)

def take_damage(amount, hazard="Hazard"):
    """Reduces health."""
    global HEALTH
    HEALTH -= amount
    print(f"{Color.ENEMY}!! {hazard} !! Lost {amount} Health. ({HEALTH}){Color.RESET}")
    if HEALTH <= 0:
        game_over("Health depleted by P-lague and hazards")
        
def advance_time(amount=1, message=""):
    """Reduces time and enforces P-lague drain."""
    global TIME_LEFT, HEALTH, HAS_ZEPHYR
    
    TIME_LEFT -= amount
    print(f"{Color.TIME}{message} Time -{amount}. ({TIME_LEFT}){Color.RESET}")

    if not HAS_ZEPHYR:
        take_damage(PLAGUE_DRAIN, "P-lague Corruption")
    else:
        print(f"{Color.ITEM}Z-ephyr stabilization active. P-lague drain nullified this turn.{Color.RESET}")
        
    if TIME_LEFT <= 0:
        game_over("W-rath device reached critical overload")
    
# --- SCENES ---

def scene_entrance():
    """Initial phase, seeking the O-men clue."""
    global CURRENT_LOCATION, HAS_OMEN
    
    print(Color.HEADER + "\n## R-OYKENNE BASE: ENTRANCE ZONE ##" + Color.RESET)
    print("You infiltrate the abandoned facility. The **P-lague** afflicts you instantly. You must hurry.")
    
    print("\nWhere do the **E-choes** guide you?")
    print("1) Search the maintenance logs (Risk **F-licker** traps).")
    print("2) Move directly toward the central structure (N-exus).")
    
    choice = input("\n> ").strip()
    
    if choice == '1':
        if random.random() < 0.3:
            print(f"{Color.ENEMY}A F-licker electrical surge hits!{Color.RESET}")
            take_damage(15, "F-licker")
        else:
            print(f"{Color.ITEM}You find a cryptic message: 'The last step requires the first.' This is the **O-men**!{Color.RESET}")
            HAS_OMEN = True
        advance_time(1, "Searching logs...")
        CURRENT_LOCATION = "VORTEX_HALL"
    elif choice == '2':
        advance_time(1, "Rushing forward...")
        CURRENT_LOCATION = "VORTEX_HALL"
    else:
        print("Invalid choice.")

def scene_vortex_hall():
    """Encountering the Vortex obstacle."""
    global CURRENT_LOCATION, TIME_LEFT
    
    print(Color.HEADER + "\n## V-ORTEX HALLWAY ##" + Color.RESET)
    print("A twisting **V-ortex** of unstable energy blocks the main route to the N-exus.")
    
    print("\nHow will you pass?")
    print("1) Attempt to navigate the V-ortex (Costs extra Time).")
    print("2) Take a long detour (Costs extra Health).")
    
    choice = input("\n> ").strip()
    
    if choice == '1':
        print("You carefully pick your path through the V-ortex.")
        advance_time(3, "Navigating the V-ortex...")
        CURRENT_LOCATION = "XEANIAL_DEN"
    elif choice == '2':
        take_damage(20, "Detour Hazards")
        advance_time(1, "Taking the long route...")
        CURRENT_LOCATION = "XEANIAL_DEN"
    else:
        print("Invalid choice.")

def scene_xeanial_den():
    """Encountering the X-enial merchant/dealer."""
    global CURRENT_LOCATION, HEALTH, TIME_LEFT, HAS_ZEPHYR
    
    print(Color.HEADER + "\n## X-ENIAL'S MARKETPLACE ##" + Color.RESET)
    print(f"You stumble upon an **X-enial** merchant. They offer help, for a price.")
    
    print("\nTrade options (Requires spending 5 Time or 20 Health):")
    print("1) Purchase **Z-ephyr** Stabilizer (Costs 5 Time).")
    print("2) Purchase Health Regeneration (Costs 20 Health, restores 35 Health).")
    print("3) Ignore the X-enial and move on.")
    
    choice = input("\n> ").strip()
    
    if choice == '1':
        if TIME_LEFT >= 5:
            TIME_LEFT -= 5
            HAS_ZEPHYR = True
            print(f"{Color.ITEM}Z-ephyr Stabilizer purchased! P-lague effect is nullified for now.{Color.RESET}")
        else:
            print(f"{Color.ENEMY}Not enough time to complete the transaction!{Color.RESET}")
    elif choice == '2':
        if HEALTH > 20:
            HEALTH -= 20
            HEALTH += 35
            print(f"{Color.HEALTH}Health exchanged for a stronger regen boost! Health is now {HEALTH}.{Color.RESET}")
        else:
            print(f"{Color.ENEMY}You are too weak to sacrifice that much health!{Color.RESET}")
    
    advance_time(1, "Leaving X-enial's shop...")
    CURRENT_LOCATION = "NEXUS_CORE"

def scene_nexus_core():
    """Final confrontation and U-nravel puzzle."""
    global HAS_OMEN, HEALTH, TIME_LEFT
    clear_screen()
    print(Color.HEADER + "#####################################################" + Color.RESET)
    print(Color.HEADER + "## N: N-EXUS CORE - The W-rath Device              ##" + Color.RESET)
    print(Color.HEADER + "#####################################################" + Color.RESET)
    display_status()
    
    print("You reach the **N-exus** core. The **W-rath** device is humming violently.")
    print(f"You have {TIME_LEFT} seconds left to defuse it using the **U-nravel** protocol.")
    
    print("\n**U-NRAVEL PROTOCOL SEQUENCE**:")
    print("1) Attempt to brute-force the deactivation code.")
    print("2) Input the sequence guided by the **O-men** clue.")
    
    final_choice = input("\nEnter your choice (1/2): ").strip()
    
    if final_choice == '2' and HAS_OMEN:
        print(f"{Color.ITEM}You remember the O-men: 'The last step requires the first.'{Color.RESET}")
        print("Following the clue, the **U-nravel** sequence is successful.")
        victory()
    elif final_choice == '2' and not HAS_OMEN:
        print(f"{Color.ENEMY}You recall the O-men, but lack the context! The device rejects the sequence.{Color.RESET}")
        take_damage(50, "W-rath Backlash")
        advance_time(5, "Rethinking the sequence...")
        # Since time is running low, this might trigger game over, or force the brute force
        
    elif final_choice == '1':
        print("You attempt brute force. This takes precious time.")
        advance_time(3, "Brute-forcing...")
        
        if random.random() < 0.2: # Low chance of success
            print(f"{Color.HEALTH}The brute force **U-nravel** succeeds by sheer luck!{Color.RESET}")
            victory()
        else:
            print(f"{Color.ENEMY}Brute force failed! The timer accelerates.{Color.RESET}")
            game_over("W-rath device accelerated self-destruct")
    
    # If the player survives the failed attempt, they try again next turn (if time allows)
    if TIME_LEFT > 0:
        scene_nexus_core()


# --- MAIN GAME EXECUTION ---

def start_game():
    global PLAYER_NAME
    clear_screen()
    print(Color.BOLD + Color.HEADER + "=" * 60 + Color.RESET)
    print(Color.BOLD + Color.HEADER + "{:^60}".format("LANDSOFAGES4: THE CYBERNETIC TIMER") + Color.RESET)
    print(Color.BOLD + Color.ENEMY + "{:^60}".format("Retrieve the W-rath before overload!") + Color.RESET)
    print(Color.BOLD + Color.HEADER + "=" * 60 + Color.RESET)
    
    PLAYER_NAME = input("Enter your Operative's codename: ").strip()
    if not PLAYER_NAME: PLAYER_NAME = "Unnamed Operative"
    
    print(f"\nOperative {PLAYER_NAME}, the **W-rath** device is active. You have {TIME_LEFT} seconds.")
    print("You are afflicted by the **P-lague** and must manage time carefully.")
    input("Press ENTER to infiltrate the base...")
    
    # Main game loop handles scene progression
    while True:
        clear_screen()
        display_status()
        
        if CURRENT_LOCATION == "ENTRANCE":
            scene_entrance()
        elif CURRENT_LOCATION == "VORTEX_HALL":
            scene_vortex_hall()
        elif CURRENT_LOCATION == "XEANIAL_DEN":
            scene_xeanial_den()
        elif CURRENT_LOCATION == "NEXUS_CORE":
            scene_nexus_core()
        else:
            break

if __name__ == "__main__":
    start_game()
