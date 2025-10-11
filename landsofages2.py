# landsofages2.py
import os
import sys
import time
import random

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
PLAYER_CLASS = "Veteran Seeker" # Assumed class from LA1
HEALTH = 120
POWER = 60
RUNES_FOUND = 0
INVENTORY = []

# --- UTILITIES ---

def clear_screen():
    """Clears the terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def game_over():
    clear_screen()
    print(Color.BOLD + Color.ENEMY + "\n" * 5)
    print("{:^60}".format("💀 THE SEQUEL FADES... GAME OVER! 💀"))
    print("\n" * 5 + Color.RESET)
    sys.exit()

def display_status():
    """Renders the player status."""
    has_chronos = 'C-hronos' in INVENTORY
    has_mantle = 'M-antle' in INVENTORY
    
    print(Color.BOLD + "=" * 60 + Color.RESET)
    print(f"{Color.BOLD}NAME:{Color.RESET} {PLAYER_NAME} | {Color.BOLD}CLASS:{Color.RESET} {PLAYER_CLASS}")
    print(f"{Color.HEALTH}HEALTH:{Color.RESET} {HEALTH} | {Color.MAGIC}POWER:{Color.RESET} {POWER} | {Color.ITEM}RUNES:{Color.RESET} {RUNES_FOUND}/5")
    print(f"Artifacts: {'C-hronos' if has_chronos else 'None'} | {'M-antle' if has_mantle else 'None'}")
    print(Color.BOLD + "=" * 60 + Color.RESET)

def take_damage(amount):
    """Reduces health and checks for game over."""
    global HEALTH
    HEALTH -= amount
    print(f"{Color.ENEMY}You take {amount} damage. Health remaining: {HEALTH}{Color.RESET}")
    if HEALTH <= 0:
        game_over()
        
def add_rune():
    """Increments rune count and displays a message."""
    global RUNES_FOUND
    RUNES_FOUND += 1
    print(f"\n{Color.BOLD}{Color.ITEM}*** ELDER RUNE ACQUIRED! ({RUNES_FOUND}/5) ***{Color.RESET}")
    time.sleep(1)

def wait_for_enter(prompt="Press ENTER to continue..."):
    """Pauses execution until the user presses Enter."""
    input(f"\n{Color.BOLD}{prompt}{Color.RESET}")

# --- SCENES ---

# A - Awakening (Start)
def scene_awakening():
    global PLAYER_NAME, INVENTORY, CURRENT_SCENE
    clear_screen()
    print(Color.HEADER + "#####################################################" + Color.RESET)
    print(Color.HEADER + "## A: A-WAKENING - The Sacred Ground               ##" + Color.RESET)
    print(Color.HEADER + "#####################################################" + Color.RESET)
    
    # Check if the player is initialized (allows for starting directly at LA2)
    if not PLAYER_NAME:
        PLAYER_NAME = input("Enter your Seeker's name: ").strip()
        if not PLAYER_NAME: PLAYER_NAME = "Unnamed Seeker"
        
    print(f"Welcome back, {PLAYER_NAME}. The stabilization of Tahkmahnelle was a success, but the resultant surge of **F-licker** magic has fractured the lands.")
    print("The **E-choes** (E) guide you: you must complete the **Q-uest** (Q)—find the five Elder Runes.")
    
    wait_for_enter("Press ENTER to begin your J-ourney (J) to the D-eluge...")
    CURRENT_SCENE = "DELUGE"

# D - Deluge (Rune 1)
def scene_deluge():
    global CURRENT_SCENE, POWER, HEALTH
    clear_screen()
    print(Color.HEADER + "#####################################################" + Color.RESET)
    print(Color.HEADER + "## D: D-ELUGE - The Flooded Coast                  ##" + Color.RESET)
    print(Color.HEADER + "#####################################################" + Color.RESET)
    display_status()
    print("The coastal region, **D-eluge** (D), is waterlogged. The first Rune rests here.")
    print(f"**G-rudge** (G), a bitter general of the fallen King, confronts you.")
    
    print("\nWhat is your action?")
    print("1) Engage G-rudge in combat (Power check).")
    print("2) Attempt to flee and find the Rune stealthily.")
    
    choice = input("\nEnter your choice (1/2): ").strip()
    
    if choice == '1':
        if POWER >= 70:
            print(f"{Color.HEALTH}Your power is overwhelming! G-rudge is defeated.{Color.RESET}")
            POWER += 10
        else:
            print(f"{Color.ENEMY}G-rudge escapes, wounding you in the process.{Color.RESET}")
            take_damage(25)
        add_rune()
        CURRENT_SCENE = "KRAKEN"
    elif choice == '2':
        if random.random() < 0.6: # 60% chance of success
            print("You use the chaos of the flood to slip past G-rudge.")
        else:
            print(f"{Color.ENEMY}Your stealth fails. G-rudge drains your power.{Color.RESET}")
            POWER -= 15
        add_rune()
        CURRENT_SCENE = "KRAKEN"
    else:
        print("Invalid choice.")
        wait_for_enter()

# K - Kraken (Rune 2)
def scene_kraken():
    global CURRENT_SCENE, HEALTH, INVENTORY
    clear_screen()
    print(Color.HEADER + "#####################################################" + Color.RESET)
    print(Color.HEADER + "## K: K-RAKEN - The Deep Guard                     ##" + Color.RESET)
    print(Color.HEADER + "#####################################################" + Color.RESET)
    display_status()
    print("The second Rune is guarded by the **K-raken** (K).")

    if 'C-hronos' not in INVENTORY:
        print("You need the **C-hronos** (C) artifact to weaken it.")
        print("1) Search for the C-hronos artifact.")
        print("2) Try to fight the K-raken without it (Extreme Risk).")
        
        sub_choice = input("\nEnter your choice (1/2): ").strip()
        
        if sub_choice == '1':
            print(f"{Color.ITEM}You find the C-hronos artifact! It grants you fleeting control over time.{Color.RESET}")
            INVENTORY.append('C-hronos')
        else:
            print(f"{Color.ENEMY}The K-raken’s blow is devastating!{Color.RESET}")
            take_damage(60)
            print("You wisely retreat to prepare.")
            wait_for_enter()
            return # Loop back to Kraken scene

    # If HAS_CHRONOS is true
    print(f"\nUsing the C-hronos, you find the K-raken's weakness.")
    print("1) Strike the weak point.")
    print(f"2) Attempt to use an item to inflict **W-rath** (W) on the creature.")
    
    final_kraken_choice = input("\nEnter your choice (1/2): ").strip()
    
    if final_kraken_choice == '1':
        print(f"{Color.HEALTH}The K-raken is slain! You retrieve the Rune.{Color.RESET}")
        add_rune()
        CURRENT_SCENE = "NEXUS"
    elif final_kraken_choice == '2' and 'Od Duck' in INVENTORY:
        print(f"{Color.ITEM}You use the Od Duck to channel chaotic W-rath. It works!{Color.RESET}")
        add_rune()
        CURRENT_SCENE = "NEXUS"
    else:
        print(f"{Color.ENEMY}Your attack is ineffective. The K-raken strikes back.{Color.RESET}")
        take_damage(30)
        add_rune()
        CURRENT_SCENE = "NEXUS"

# N - Nexus (Rune 3)
def scene_nexus():
    global CURRENT_SCENE, POWER, HEALTH, INVENTORY
    clear_screen()
    print(Color.HEADER + "#####################################################" + Color.RESET)
    print(Color.HEADER + "## N: N-EXUS - Convergence of Light and Shadow     ##" + Color.RESET)
    print(Color.HEADER + "#####################################################" + Color.RESET)
    display_status()
    print("You reach the **N-exus**, the convergence point. The third Rune is guarded by a false **I-dol** (I).")
    
    print(f"A cryptic **X-enial** (X) approaches you: 'The I-dol demands a **Y-ield** (Y). What will you sacrifice?'")
    
    print("1) Sacrifice 30 **POWER** (Y-ield).")
    print("2) Sacrifice 30 **HEALTH** (Y-ield).")
    print("3) Try to destroy the I-dol.")
    
    sacrifice_choice = input("\nEnter your choice (1-3): ").strip()
    
    if sacrifice_choice == '1':
        POWER -= 30
        print(f"{Color.MAGIC}Your Power fades, but the I-dol is satisfied.{Color.RESET}")
    elif sacrifice_choice == '2':
        take_damage(30)
        print(f"{Color.HEALTH}Your body aches, but the I-dol is satisfied.{Color.RESET}")
    elif sacrifice_choice == '3':
        print(f"{Color.ENEMY}The I-dol shatters, but you take minor backlash.{Color.RESET}")
        take_damage(15)
    else:
        print("You hesitate. The X-enial vanishes, but the Rune is still attainable.")
        
    add_rune()
    wait_for_enter()
    CURRENT_SCENE = "SHADOWLANDS"

# S - Shadowlands (Rune 4)
def scene_shadowlands():
    global CURRENT_SCENE, HEALTH, INVENTORY
    clear_screen()
    print(Color.HEADER + "#####################################################" + Color.RESET)
    print(Color.HEADER + "## S: S-HADOWLANDS - Remnants of Z-azoykenne       ##" + Color.RESET)
    print(Color.HEADER + "#####################################################" + Color.RESET)
    display_status()
    print("This land is corrupted. The fourth Rune lies deep within the **S-hadowlands** (S).")

    if 'M-antle' not in INVENTORY:
        print("You need the **M-antle** (M) of authority to pass through the corrupted air.")
        print("1) Seek the M-antle in a nearby **V-ortex** (V).")
        print("2) Power through the Shadowlands (High damage risk).")
        
        mantle_choice = input("\nEnter your choice (1/2): ").strip()
        
        if mantle_choice == '1':
            print(f"{Color.ITEM}You brave the V-ortex (V) and claim the M-antle! (+10 Health){Color.RESET}")
            INVENTORY.append('M-antle')
            HEALTH += 10
        else:
            print(f"{Color.ENEMY}The corruption nearly kills you!{Color.RESET}")
            take_damage(45)
            
    if 'M-antle' in INVENTORY:
        print("Protected by the M-antle, you safely locate the fourth Rune.")
        add_rune()
    else:
        print("Without the Mantle, you struggle but succeed in finding the Rune.")
        add_rune()

    wait_for_enter()
    CURRENT_SCENE = "TREASURY"

# T - Treasury (Rune 5 & Final Confrontation)
def scene_treasury():
    global CURRENT_SCENE, RUNES_FOUND
    clear_screen()
    print(Color.HEADER + "#####################################################" + Color.RESET)
    print(Color.HEADER + "## T: T-REASURY - The Final Trial                  ##" + Color.RESET)
    print(Color.HEADER + "#####################################################" + Color.RESET)
    display_status()
    
    if RUNES_FOUND < 4:
        print(f"{Color.ENEMY}You haven't gathered enough Runes! The R-ecluse laughs and seals the way.{Color.RESET}")
        game_over()
        
    print("You find the **T-reasury** where the final Rune is guarded by the **R-ecluse** (R), the vengeful general.")
    print("The R-ecluse attempts to unleash a magical **P-lague** (P) on the world!")
    
    print("\nYour final choice:")
    print("1) Cast the **U-nravel** (U) spell to harness the **Z-ephyr** (Z) and purify the land.")
    print("2) Attack the R-ecluse directly.")
    
    final_choice = input("\nEnter your choice (1/2): ").strip()

    if final_choice == '1':
        print(f"{Color.MAGIC}The five Runes glow intensely. You channel the U-nravel spell.{Color.RESET}")
        print(f"{Color.HEALTH}The Z-ephyr (Z) washes over the lands, purifying the P-lague and calming the R-ecluse.{Color.RESET}")
        
        print(Color.BOLD + "\n🏆 VICTORY! THE SECOND ECHO IS COMPLETE! 🏆" + Color.RESET)
        print("The Lands of Ages are truly safe... for now.")
    else:
        print(f"{Color.ENEMY}Your attack fails! The P-lague spreads uncontrollably.{Color.RESET}")
        game_over()
    
    sys.exit()

# --- MAIN GAME EXECUTION ---

def start_game():
    global PLAYER_NAME, CURRENT_SCENE
    clear_screen()
    print(Color.BOLD + Color.HEADER + "=" * 60 + Color.RESET)
    print(Color.BOLD + Color.HEADER + "{:^60}".format("WELCOME TO RETURN2LANDSOFAGES: THE SECOND ECHO") + Color.RESET)
    print(Color.BOLD + Color.HEADER + "=" * 60 + Color.RESET)
    
    PLAYER_NAME = input("Enter your Seeker's name: ").strip()
    if not PLAYER_NAME: PLAYER_NAME = "Unnamed Seeker"
    
    print(f"\nHello, {PLAYER_NAME}. Your **Q-uest** to stabilize the lands begins now.")
    wait_for_enter("Press ENTER to begin...")
    
    CURRENT_SCENE = "AWAKENING"

    # Main game loop handles scene progression
    while True:
        if CURRENT_SCENE == "AWAKENING":
            scene_awakening()
        elif CURRENT_SCENE == "DELUGE":
            scene_deluge()
        elif CURRENT_SCENE == "KRAKEN":
            scene_kraken()
        elif CURRENT_SCENE == "NEXUS":
            scene_nexus()
        elif CURRENT_SCENE == "SHADOWLANDS":
            scene_shadowlands()
        elif CURRENT_SCENE == "TREASURY":
            scene_treasury()
        else:
            break

if __name__ == "__main__":
    start_game()
