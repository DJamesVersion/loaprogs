# landsofages_tahkmahnelle.py
# Copyright LoA Corporation SLPOE

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

# --- GLOBAL GAME STATE ---
PLAYER_NAME = "Blue Hero"
HEALTH = 100
POWER = 50
TURN = 1
CURRENT_AGE = 1

# Shared Inventory & Status
INVENTORY = set() # Use a set for easy keyword lookup
RUNES_FOUND = 0
FIGHTER_STRENGTH = 0 # Used for military power
TERRAFORM_SCORE = 0  # Final goal for the final age

# --- UTILITIES ---

def clear_screen():
    """Clears the terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def game_over(reason="The saga ends in failure."):
    """Displays game over screen and exits."""
    clear_screen()
    print(Color.BOLD + Color.ENEMY + "\n" * 5)
    print("{:^70}".format("💀 MISSION FAILURE 💀"))
    print(f"{:^70}".format(f"Cause: {reason}"))
    print("\n" * 5 + Color.RESET)
    sys.exit()

def victory():
    """Displays victory screen and exits."""
    clear_screen()
    print(Color.BOLD + Color.HEALTH + "\n" * 5)
    print("{:^70}".format("👑 VICTORY! TAHKMAHNELLE'S EVERAFTER IS SECURE! 👑"))
    print(f"{:^70}".format(f"The saga was completed in {TURN} turns."))
    print("\n" * 5 + Color.RESET)
    sys.exit()

def display_status():
    """Renders the comprehensive game status."""
    print(Color.BOLD + "=" * 70 + Color.RESET)
    print(f"{Color.MAGIC}AGE: {CURRENT_AGE}/4 | TURN: {TURN} | HERO: {PLAYER_NAME}{Color.RESET}")
    print(f"{Color.HEALTH}HEALTH:{Color.RESET} {HEALTH} | {Color.MAGIC}POWER:{Color.RESET} {POWER} | {Color.ITEM}INVENTORY:{Color.RESET} {', '.join(INVENTORY) if INVENTORY else 'None'}")
    
    # Age-specific status
    if CURRENT_AGE == 1:
        print(f"Goal Status: Runes: {RUNES_FOUND}/5 | Has B-atobwatchaeh: {'Yes' if 'B-atobwatchaeh' in INVENTORY else 'No'}")
    elif CURRENT_AGE == 2:
        print(f"Goal Status: JPW7 Chaos Level: {POWER} | Has Od Duck: {'Yes' if 'Od Duck' in INVENTORY else 'No'}")
    elif CURRENT_AGE == 3:
        print(f"Goal Status: F-'illianarre Strength: {FIGHTER_STRENGTH} | X-iangxong Threat: {int(TURN/5 * 10)}%")
    elif CURRENT_AGE == 4:
        print(f"Goal Status: Terraform Score: {TERRAFORM_SCORE}/100 | Ship Level: {POWER // 25}")
        
    print(Color.BOLD + "=" * 70 + Color.RESET)

def take_damage(amount, hazard="Hazard"):
    """Reduces health and checks for game over."""
    global HEALTH
    HEALTH = max(0, HEALTH - amount)
    print(f"{Color.ENEMY}!! {hazard} !! Lost {amount} Health. ({HEALTH}){Color.RESET}")
    if HEALTH <= 0:
        game_over("Health depleted by constant threats.")

def advance_turn(damage_type="Normal"):
    """Increments turn and applies passive age effects."""
    global TURN, HEALTH
    TURN += 1
    
    # Simulate passive threats or P-lague
    if damage_type == "P-lague":
        take_damage(random.randint(5, 15), "P-lague Corruption")
    elif damage_type == "Normal":
        # Check for catastrophic time failure in Age 3 if we wait too long
        if CURRENT_AGE == 3 and TURN > 15:
            game_over("The X-iangxong War Machine reached the capital.")
        
# --- AGE I: THE GREAT SEARCH (LA1 & LA2) ---

def age1_scene():
    global CURRENT_AGE, RUNES_FOUND, POWER, INVENTORY
    
    print(Color.HEADER + "\n-- AGE I: THE GREAT SEARCH (A-riatnah) --" + Color.RESET)
    print("The **J-ampejinne** bid you begin your **Q-uest** to find the artifacts and stabilize the world.")
    
    choices = {}
    i = 1

    if 'B-atobwatchaeh' not in INVENTORY:
        print(f"{i}) Search the **D-iadowatchaeh** for the **B-atobwatchaeh** (Costs 20 Power).")
        choices[str(i)] = 'ARTIFACT'
        i += 1
    
    if RUNES_FOUND < 5:
        print(f"{i}) Seek an **Elder Rune** in the lands (Runes found: {RUNES_FOUND}/5).")
        choices[str(i)] = 'RUNE'
        i += 1
    
    if 'B-atobwatchaeh' in INVENTORY and RUNES_FOUND == 5:
        print(f"{i}) COMPLETE Q-UEST: Advance to AGE II.")
        choices[str(i)] = 'ADVANCE'
        i += 1
    
    choice = input("\nEnter choice: ").strip()

    if choice == choices.get('1') or choice == choices.get('2'):
        if choice == 'ARTIFACT':
            if POWER >= 20:
                INVENTORY.add('B-atobwatchaeh')
                POWER -= 20
                print(f"{Color.ITEM}The **B-atobwatchaeh** is recovered! Power -20.{Color.RESET}")
            else:
                take_damage(20, "D-iadowatchaeh Traps (No Power)")
        
        elif choice == 'RUNE':
            RUNES_FOUND += 1
            if random.random() < 0.3:
                INVENTORY.add('Z-ephyr')
                print(f"{Color.ITEM}Rune secured! You also find a stabilizing **Z-ephyr**!{Color.RESET}")
            else:
                 print(f"{Color.MAGIC}An Elder Rune is secured! The **E-choes** guide you.{Color.RESET}")
            
            take_damage(5, "F-licker residual damage")
        
        elif choice == 'ADVANCE':
            print(f"{Color.HEADER}AGE I Complete! Magic stabilized. Now for the chaos...{Color.RESET}")
            CURRENT_AGE = 2
            return # Skip advance_turn as we switch age
    
    advance_turn()

# --- AGE II: THE EDICT OF CHAOS (LA6) ---

def age2_scene():
    global CURRENT_AGE, POWER, INVENTORY, HEALTH
    
    print(Color.HEADER + "\n-- AGE II: THE EDICT OF CHAOS (JPW7) --" + Color.RESET)
    print("The world is covered in **Bunnies and Rainbows**, masking the **Grass Blues** corruption. You must find the **Giraffe in the Jug** clue.")
    
    choices = {}
    i = 1
    
    if 'Od Duck' not in INVENTORY:
        print(f"{i}) Search for the chaotic **Od Duck** relic.")
        choices[str(i)] = 'DUCK'
        i += 1
    if 'Carrot' not in INVENTORY:
        print(f"{i}) Seek the **Youth in Asia** NPC for the power source (**Carrot**).")
        choices[str(i)] = 'CARROT'
        i += 1
    
    print(f"{i}) Confront the **Blisterfist** drone (Power Check).")
    choices[str(i)] = 'FIST'
    i += 1
    
    if 'Od Duck' in INVENTORY and 'Carrot' in INVENTORY:
        print(f"{i}) Final Action: Attempt the **Giraffe in the Jug** puzzle (Requires items).")
        choices[str(i)] = 'ADVANCE'
        i += 1
        
    choice = input("\nEnter choice: ").strip()

    if choice == choices.get('1') or choice == choices.get('2') or choice == choices.get('3') or choice == choices.get('4'):
        if choice == 'DUCK':
            INVENTORY.add('Od Duck')
            print(f"{Color.ITEM}The chaotic **Od Duck** is found!{Color.RESET}")
        elif choice == 'CARROT':
            INVENTORY.add('Carrot')
            print(f"{Color.ITEM}The **Carrot** power source is secured!{Color.RESET}")
        elif choice == 'FIST':
            if POWER > 60:
                POWER += 10
                print(f"{Color.HEALTH}You overload the **Blisterfist**! Power +10.{Color.RESET}")
            else:
                take_damage(35, "Blisterfist Strike")
        elif choice == 'ADVANCE':
            print(f"{Color.HEADER}AGE II Complete! JPW7's cybernetic logic is neutralized by absurdity.{Color.RESET}")
            CURRENT_AGE = 3
            global FIGHTER_STRENGTH
            FIGHTER_STRENGTH = 10 # Initial fighters
            INVENTORY.discard('Od Duck') # Keep only core artifacts
            INVENTORY.discard('Carrot')
            return
    
    advance_turn()

# --- AGE III: THE FINAL EDICT (LA3 & LA4) ---

def age3_scene():
    global CURRENT_AGE, FIGHTER_STRENGTH, POWER, HEALTH, INVENTORY
    
    threat = int(TURN/5 * 10)
    print(Color.HEADER + "\n-- AGE III: THE FINAL EDICT (R-oykenne War) --" + Color.RESET)
    print(f"The **R-oykenne's** **X-iangxong** threat level is at {threat}%. You need 100 Fighters for the final push.")
    
    choices = {}
    i = 1

    print(f"{i}) Gather **S-tihuu** (Materials) and **S-iataeh** (Magic).")
    choices[str(i)] = 'GATHER'
    i += 1
    print(f"{i}) Recruit **F-'illianarre** (Fighters) (Cost: 10 Power).")
    choices[str(i)] = 'RECRUIT'
    i += 1
    
    if FIGHTER_STRENGTH >= 100:
        print(f"{i}) Final Action: Infiltrate the **N-exus** to **U-nravel** the **W-rath**.")
        choices[str(i)] = 'ADVANCE'
        i += 1
        
    choice = input("\nEnter choice: ").strip()

    if choice == choices.get('1') or choice == choices.get('2') or choice == choices.get('3'):
        if choice == 'GATHER':
            POWER += 20
            print(f"{Color.ITEM}S-tihuu and S-iataeh gathered. Power +20.{Color.RESET}")
        
        elif choice == 'RECRUIT':
            if POWER >= 10:
                POWER -= 10
                FIGHTER_STRENGTH += 25
                print(f"{Color.HEALTH}**F-'illianarre** unit deployed! Strength +25.{Color.RESET}")
            else:
                print(f"{Color.ENEMY}Insufficient Power to recruit.{Color.RESET}")

        elif choice == 'ADVANCE':
            if 'B-atobwatchaeh' in INVENTORY:
                print(f"{Color.HEADER}AGE III Complete! The **W-rath** is **U-nravelled** at the **N-exus**.{Color.RESET}")
                CURRENT_AGE = 4
                return
            else:
                take_damage(50, "W-rath Explosion (No B-atobwatchaeh)")
                print(f"{Color.ENEMY}Failed to U-nravel without the **B-atobwatchaeh**.{Color.RESET}")

    advance_turn()

# --- AGE IV: COLONIZATION (LA5 & RFA2LA) ---

def age4_scene():
    global CURRENT_AGE, TERRAFORM_SCORE, POWER
    
    ship_level = POWER // 25
    print(Color.HEADER + "\n-- AGE IV: COLONIZATION (TAHKMAHNELLE45) --" + Color.RESET)
    print(f"Goal: Establish permanent colony on **TAHKMAHNELLE45**. Ship Level: {ship_level}.")
    
    if TERRAFORM_SCORE >= 100:
        victory()
    
    choices = {}
    i = 1

    print(f"{i}) Gather **Colony Resources** (Boosted by Ship Level).")
    choices[str(i)] = 'GATHER'
    i += 1
    print(f"{i}) Build/Terraform Colony (Cost: 20 Power, Gain: 10 + Ship Level).")
    choices[str(i)] = 'BUILD'
    i += 1
    print(f"{i}) Upgrade Ship Capacity (Costs 50 Power).")
    choices[str(i)] = 'UPGRADE'
    i += 1
        
    choice = input("\nEnter choice: ").strip()

    if choice == choices.get('1') or choice == choices.get('2') or choice == choices.get('3'):
        if choice == 'GATHER':
            POWER += 10 + (ship_level * 5)
            print(f"{Color.HEALTH}Colony Resources gathered! Power +{10 + (ship_level * 5)}.{Color.RESET}")
        
        elif choice == 'BUILD':
            cost = 20
            gain = 10 + ship_level
            if POWER >= cost:
                POWER -= cost
                TERRAFORM_SCORE += gain
                print(f"{Color.MAGIC}Terraforming successful! Score +{gain}. ({TERRAFORM_SCORE}/100){Color.RESET}")
            else:
                print(f"{Color.ENEMY}Need 20 Power to terraform.{Color.RESET}")

        elif choice == 'UPGRADE':
            cost = 50
            if POWER >= cost:
                POWER += 25
                POWER -= cost
                print(f"{Color.ITEM}Ship upgraded! New Level: {POWER // 25}.{Color.RESET}")
            else:
                print(f"{Color.ENEMY}Need 50 Power to upgrade the ship.{Color.RESET}")
    
    advance_turn()

# --- MAIN GAME EXECUTION ---

def start_game():
    clear_screen()
    print(Color.BOLD + Color.HEADER + "=" * 70 + Color.RESET)
    print(Color.BOLD + Color.HEADER + "{:^70}".format("LANDSOFAGES-TAHKMAHNELLE: THE DEFINITIVE SAGA") + Color.RESET)
    print(Color.BOLD + Color.MAGIC + "{:^70}".format("Copyright LoA Corporation SLPOE") + Color.RESET)
    print(Color.BOLD + Color.HEADER + "=" * 70 + Color.RESET)
    
    global PLAYER_NAME
    PLAYER_NAME = input("Enter your Hero's name: ").strip() or "Blue Hero"
    
    print(f"\nWelcome, {PLAYER_NAME}. Your four-stage journey to secure Tahkmahnelle begins now.")
    input("Press ENTER to begin...")
    
    while True:
        clear_screen()
        display_status()
        
        if CURRENT_AGE == 1:
            age1_scene()
        elif CURRENT_AGE == 2:
            age2_scene()
        elif CURRENT_AGE == 3:
            age3_scene()
        elif CURRENT_AGE == 4:
            age4_scene()
        else:
            break

if __name__ == "__main__":
    start_game()
