# landsofages_everaftertahkmahnelle.py
import os
import sys
import time
import random

# --- ANSI COLOR CODES ---
class Color:
    MAGIC = '\033[94m'      # Blue Hero / Magic
    HEALTH = '\033[92m'     # Green
    ENEMY = '\033[91m'      # Red / Threat
    ITEM = '\033[93m'       # Yellow / Item
    HEADER = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# --- GLOBAL GAME STATE ---
PLAYER_NAME = "Blue Hero"
HEALTH = 100
POWER = 50
TURN = 1
CURRENT_AGE = 1

# Shared Inventory & Status
INVENTORY = []
RUNES_FOUND = 0
RESOURCES = 0 # General resource pool for Age IV
TERRAFORM_SCORE = 0 # Final goal for Age IV
JPW7_TIME_LEFT = 10 # Timer for Age II (LA6)

# --- UTILITIES ---

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def game_over(reason=""):
    clear_screen()
    print(Color.BOLD + Color.ENEMY + "\n" * 5)
    print("{:^70}".format("💀 THE SAGA ENDS. TAHKMAHNELLE'S EVERAFTER IS LOST. 💀"))
    print(f"{:^70}".format(f"Cause: {reason}"))
    print("\n" * 5 + Color.RESET)
    sys.exit()

def victory():
    clear_screen()
    print(Color.BOLD + Color.HEADER + "\n" * 5)
    print("{:^70}".format("👑 THE EVERAFTER IS WON! TAHKMAHNELLE'S LEGACY ENDURES! 👑"))
    print(f"{:^70}".format(f"The Blue Hero established the future in {TURN} turns."))
    print("\n" * 5 + Color.RESET)
    sys.exit()

def display_status():
    """Renders the comprehensive game status."""
    print(Color.BOLD + "=" * 70 + Color.RESET)
    print(f"{Color.MAGIC}AGE: {CURRENT_AGE}/4 | TURN: {TURN} | HERO: {PLAYER_NAME}{Color.RESET}")
    print(f"{Color.HEALTH}HEALTH:{Color.RESET} {HEALTH} | {Color.MAGIC}POWER:{Color.RESET} {POWER} | {Color.ITEM}RESOURCES:{Color.RESET} {RESOURCES}")
    
    # Age-specific status
    if CURRENT_AGE == 1:
        print(f"LA1/LA2 Status: Runes: {RUNES_FOUND}/5 | Has B-atobwatchaeh: {'Yes' if 'B-atobwatchaeh' in INVENTORY else 'No'}")
    elif CURRENT_AGE == 2:
        print(f"LA6 Status: JPW7 Time Left: {JPW7_TIME_LEFT} | Items: {', '.join(INVENTORY)}")
    elif CURRENT_AGE == 3:
        print(f"LA3/LA4 Status: F-'illianarre Strength: {RESOURCES} | X-iangxong Progress: {100 - JPW7_TIME_LEFT}%")
    elif CURRENT_AGE == 4:
        print(f"LA5/RFA2LA Status: Terraform Score: {TERRAFORM_SCORE}/100 | Ship Level: {POWER // 10}") # Power used as ship level
        
    print(Color.BOLD + "=" * 70 + Color.RESET)

def take_damage(amount, hazard="Hazard"):
    """Reduces health and checks for game over."""
    global HEALTH
    HEALTH -= amount
    print(f"{Color.ENEMY}!! {hazard} !! Lost {amount} Health. ({HEALTH}){Color.RESET}")
    if HEALTH <= 0:
        game_over("Health depleted.")

def advance_turn(age_progress=1):
    """Increments turn, handles age-specific time/threat events."""
    global TURN, JPW7_TIME_LEFT
    TURN += 1

    if CURRENT_AGE == 2:
        JPW7_TIME_LEFT -= age_progress
        if JPW7_TIME_LEFT <= 0:
            game_over("JPW7's cybernetic logic overwhelmed the magic.")
    
    if CURRENT_AGE == 3:
        # Enemy progress is the inverse of time left
        progress_gain = 10
        JPW7_TIME_LEFT -= progress_gain
        if 100 - JPW7_TIME_LEFT >= 100:
             game_over("The X-iangxong War Machine reached the capital.")

# --- AGE I: THE GREAT SEARCH (LA1 & LA2) ---

def age1_scene_ariatnah():
    global CURRENT_AGE, RUNES_FOUND, INVENTORY, POWER
    
    print("\n-- AGE I: THE GREAT SEARCH --")
    print("Location: A-riatnah. The J-ampejinne bid you begin your Q-uest to stabilize the world.")
    
    if 'B-atobwatchaeh' not in INVENTORY:
        print("1) Search the D-iadowatchaeh for the **B-atobwatchaeh** (50 Power check).")
    
    if RUNES_FOUND < 5:
        print(f"2) Seek an **Elder Rune** in the lands (Runes found: {RUNES_FOUND}/5).")
    
    if 'B-atobwatchaeh' in INVENTORY and RUNES_FOUND == 5:
        print("3) Complete the Great Search and advance to the next Age.")
        
    choice = input("\n> ").strip()

    if choice == '1':
        if POWER >= 50:
            INVENTORY.append('B-atobwatchaeh')
            POWER -= 20
            print(f"{Color.ITEM}Artifact recovered! B-atobwatchaeh now in your possession.{Color.RESET}")
        else:
            take_damage(20, "D-iadowatchaeh Traps")
    
    elif choice == '2' and RUNES_FOUND < 5:
        RUNES_FOUND += 1
        print(f"{Color.MAGIC}An Elder Rune is secured! The E-choes guide you on...{Color.RESET}")
        take_damage(5, "F-licker residual damage")
        if RUNES_FOUND == 3:
            INVENTORY.append('Z-ephyr') # Z-ephyr granted as a reward
            print(f"{Color.ITEM}**Z-ephyr** stabilizer granted!{Color.RESET}")

    elif choice == '3' and RUNES_FOUND == 5 and 'B-atobwatchaeh' in INVENTORY:
        print(f"{Color.HEADER}AGE I Complete! The world is magically stabilized.{Color.RESET}")
        CURRENT_AGE = 2
        INVENTORY = [item for item in INVENTORY if item in ['Od Duck', 'Carrot'] or 'B-atobwatchaeh'] # Cleanup inventory for next age
        global JPW7_TIME_LEFT; JPW7_TIME_LEFT = 100 # Reset timer for new age
        global RESOURCES; RESOURCES = 0
    
    advance_turn(1)

# --- AGE II: THE EDICT OF CHAOS (LA6) ---

def age2_scene_jpw7_chaos():
    global CURRENT_AGE, INVENTORY, POWER, JPW7_TIME_LEFT
    
    print("\n-- AGE II: THE EDICT OF CHAOS --")
    print(f"Threat: JPW7's cybernetic rule. Timer: {JPW7_TIME_LEFT} months.")
    
    # Initial encounter/setup
    if JPW7_TIME_LEFT == 100:
        print("The world is bathed in an artificial **Bunnies and Rainbows** aura, masking the underlying **Grass Blues** corruption.")
        print(f"You must find the **Giraffe in the Jug** clue to overload JPW7's early coding.")
        JPW7_TIME_LEFT -= 1 # Initial time cost
    
    print("\nActions:")
    if 'Od Duck' not in INVENTORY:
        print("1) Search the Grass Blues field for the **Od Duck** relic.")
    if 'Carrot' not in INVENTORY:
        print("2) Seek the **Youth in Asia** NPC for a power source (**Carrot**).")
    print("3) Confront the **Blisterfist** drone (High risk, Power check).")
    print("4) Attempt the final **Giraffe in the Jug** puzzle (Requires items).")
    
    choice = input("\n> ").strip()

    if choice == '1' and 'Od Duck' not in INVENTORY:
        INVENTORY.append('Od Duck')
        print(f"{Color.ITEM}The chaotic **Od Duck** is found!{Color.RESET}")
    elif choice == '2' and 'Carrot' not in INVENTORY:
        INVENTORY.append('Carrot')
        print(f"{Color.ITEM}The Youth in Asia NPC grants you the high-energy **Carrot**!{Color.RESET}")
    elif choice == '3':
        if POWER > 60:
            print(f"{Color.HEALTH}You overload the **Blisterfist** with raw magic!{Color.RESET}")
        else:
            take_damage(35, "Blisterfist Strike")
    elif choice == '4':
        if 'Od Duck' in INVENTORY and 'Carrot' in INVENTORY:
            print("You use the Carrot to fuel the Od Duck, which generates the illogical answer!")
            print(f"{Color.HEADER}AGE II Complete! JPW7's early edicts are neutralized.{Color.RESET}")
            CURRENT_AGE = 3
            global JPW7_TIME_LEFT; JPW7_TIME_LEFT = 10 # Reset timer for new age
            INVENTORY = ['B-atobwatchaeh']
        else:
            print(f"{Color.ENEMY}The logic gates remain locked. Need Od Duck and Carrot.{Color.RESET}")
    
    advance_turn(10)

# --- AGE III: THE FINAL EDICT (LA3 & LA4) ---

def age3_scene_roykenne_war():
    global CURRENT_AGE, RESOURCES, JPW7_TIME_LEFT, HEALTH
    
    print("\n-- AGE III: THE FINAL EDICT --")
    print(f"Threat: R-oykenne's X-iangxong war machine. Progress: {100 - JPW7_TIME_LEFT}%.")
    
    # Resources are the Fighters (F-'illianarre)
    fighter_strength = RESOURCES
    
    print("1) Gather **S-tihuu** (Materials) and **S-iataeh** (Magic) (Costs 1 Turn).")
    print("2) Recruit **F-'illianarre** (Fighters) (Costs 30 Resources).")
    print("3) Research at **L-enemketobontette** (Convert Power to Resources).")
    print("4) Infiltrate the **N-exus** to **U-nravel** the **W-rath** (Requires >100 Fighters).")
    
    choice = input("\n> ").strip()

    if choice == '1':
        RESOURCES += 40
        POWER += 10
        print(f"{Color.ITEM}S-tihuu and S-iataeh gathered.{Color.RESET}")
    
    elif choice == '2':
        if RESOURCES >= 30:
            RESOURCES -= 30
            RESOURCES += 20 # Fighter strength is stored in RESOURCES
            print(f"{Color.HEALTH}F-'illianarre unit deployed! Strength: {RESOURCES}{Color.RESET}")
        else:
            print(f"{Color.ENEMY}Insufficient resources to recruit.{Color.RESET}")

    elif choice == '3':
        if POWER >= 20:
            POWER -= 20
            RESOURCES += 30
            print(f"{Color.MAGIC}Magic converted to resources at L-enemketobontette.{Color.RESET}")
        else:
            print(f"{Color.ENEMY}Insufficient Power to research.{Color.RESET}")

    elif choice == '4' and fighter_strength >= 100:
        if 'B-atobwatchaeh' in INVENTORY:
            print(f"{Color.HEALTH}Using the B-atobwatchaeh, you **U-nravel** the **W-rath** at the N-exus.{Color.RESET}")
            print(f"{Color.HEADER}AGE III Complete! The R-oykenne's final threat is neutralized.{Color.RESET}")
            CURRENT_AGE = 4
            global RESOURCES; RESOURCES = 150
            global POWER; POWER = 10 # Reset power as ship level
        else:
            take_damage(50, "W-rath Explosion")
            print(f"{Color.ENEMY}Failed to U-nravel without the B-atobwatchaeh.{Color.RESET}")
    elif choice == '4':
         print(f"{Color.ENEMY}Need >100 F-'illianarre to cover your infiltration!{Color.RESET}")

    advance_turn(1)

# --- AGE IV: COLONIZATION (LA5 & RFA2LA) ---

def age4_scene_colonization():
    global CURRENT_AGE, RESOURCES, TERRAFORM_SCORE, POWER
    
    print("\n-- AGE IV: COLONIZATION --")
    print(f"Goal: Establish permanent colony on TAHKMAHNELLE45.")
    
    # Power acts as Ship Level for this final age
    ship_level = POWER // 10
    
    print(f"1) Gather **Colony Resources** (Boosted by Ship Level {ship_level}).")
    print("2) Build/Terraform Colony (Cost: 50 Resources).")
    print("3) Upgrade Ship Capacity/Speed (Cost: 100 Resources per Level).")
    
    if TERRAFORM_SCORE >= 100:
        victory()
    
    choice = input("\n> ").strip()

    if choice == '1':
        gain = 25 + (ship_level * 5)
        RESOURCES += gain
        print(f"{Color.HEALTH}Gathering successful. Resources +{gain}.{Color.RESET}")
    
    elif choice == '2':
        cost = 50 + (TERRAFORM_SCORE // 10)
        if RESOURCES >= cost:
            RESOURCES -= cost
            gain = 10 + (ship_level * 3)
            TERRAFORM_SCORE += gain
            print(f"{Color.DWARF}Terraforming successful! Score +{gain}. ({TERRAFORM_SCORE}/100){Color.RESET}")
        else:
            print(f"{Color.ENEMY}Need {cost} resources to terraform.{Color.RESET}")

    elif choice == '3':
        cost = (ship_level + 1) * 100
        if RESOURCES >= cost:
            RESOURCES -= cost
            POWER += 10
            print(f"{Color.ITEM}Ship upgraded! New Level: {POWER // 10}.{Color.RESET}")
        else:
            print(f"{Color.ENEMY}Insufficient resources to upgrade.{Color.RESET}")
            
    advance_turn(1)

# --- MAIN GAME EXECUTION ---

def start_game():
    clear_screen()
    print(Color.BOLD + Color.HEADER + "=" * 70 + Color.RESET)
    print(Color.BOLD + Color.HEADER + "{:^70}".format("LANDSOFAGES: EVERAFTERTAHKMAHNELLE") + Color.RESET)
    print(Color.BOLD + Color.MAGIC + "{:^70}".format("The Complete Saga") + Color.RESET)
    print(Color.BOLD + Color.HEADER + "=" * 70 + Color.RESET)
    
    global PLAYER_NAME
    PLAYER_NAME = input("Enter your Hero's name (e.g., Blue Hero): ").strip() or "Blue Hero"
    
    print(f"\nWelcome, {PLAYER_NAME}. Your journey begins in Age I: The Great Search.")
    input("Press ENTER to begin the epic...")
    
    while True:
        clear_screen()
        display_status()
        
        if CURRENT_AGE == 1:
            age1_scene_ariatnah()
        elif CURRENT_AGE == 2:
            age2_scene_jpw7_chaos()
        elif CURRENT_AGE == 3:
            age3_scene_roykenne_war()
        elif CURRENT_AGE == 4:
            age4_scene_colonization()
        else:
            break

if __name__ == "__main__":
    start_game()
