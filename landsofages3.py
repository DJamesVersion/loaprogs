# landsofages3.py
import os
import sys
import time
import random

# --- ANSI COLOR CODES ---
class Color:
    HEADER = '\033[95m'
    MAGIC = '\033[94m'      # Blue (S-iataeh)
    EARTH = '\033[92m'      # Green (S-tihuu)
    ENEMY = '\033[91m'      # Red
    BOLD = '\033[1m'
    RESET = '\033[0m'

# --- GLOBAL GAME VARIABLES ---
MONTH = 1
ROYKENNE_PROGRESS = 0    # 100 wins the game for the enemy
FIGHTER_STRENGTH = 10    # F-'illianarre force level

# Resources
SIATAEH_MAGIC = 100       # S-iataeh (Air/Magic)
STIHU_MATERIALS = 100     # S-tihuu (Earth/Materials)

# Faction Influence
JAMPEJINNE_INFLUENCE = 5  # J-ampejinne (Magic faction)
CILLIATNAH_INFLUENCE = 5  # C-'illiatnah (Research faction)

# Artifact
HAS_BATOBWATCHAEH = False # B-atobwatchaeh

# --- UTILITIES ---

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def game_over():
    clear_screen()
    print(Color.BOLD + Color.ENEMY + "\n" * 5)
    print("{:^60}".format("💀 THE X-IANGXONG HAS ARRIVED. TAHKMAHNELLE FALLS. 💀"))
    print("\n" * 5 + Color.RESET)
    sys.exit()

def victory():
    clear_screen()
    print(Color.BOLD + Color.MAGIC + "\n" * 5)
    print("{:^60}".format("👑 THE R-OYKENNE IS DEFEATED! TAHKMAHNELLE SECURE! 👑"))
    print(f"{:^60}".format(f"The Royal Forces secured victory in {MONTH} months."))
    print("\n" * 5 + Color.RESET)
    sys.exit()

def display_status():
    """Renders the strategic status."""
    gagoikenne_status = "ONLINE" if ROYKENNE_PROGRESS < 25 else "DISABLED"
    
    print(Color.BOLD + "=" * 60 + Color.RESET)
    print(f"MONTH: {MONTH} | R-OYKENNE INVASION: {Color.ENEMY}{ROYKENNE_PROGRESS}%{Color.RESET} | GOAL: 100%")
    print("-" * 60)
    print(f"{Color.MAGIC}S-IATAEH (Magic): {SIATAEH_MAGIC:<8}{Color.RESET} | {Color.EARTH}S-TIHUU (Materials): {STIHU_MATERIALS:<8}{Color.RESET}")
    print(f"FIGHTERS (F-'illianarre): {FIGHTER_STRENGTH} | Research: {CILLIATNAH_INFLUENCE}")
    print(f"B-atobwatchaeh Status: {'ACTIVE' if HAS_BATOBWATCHAEH else 'OFFLINE'}")
    print(f"G-agoikenne Defense: {gagoikenne_status}")
    print(Color.BOLD + "=" * 60 + Color.RESET)

def advance_month():
    """Calculates resource generation and enemy progress."""
    global MONTH, ROYKENNE_PROGRESS, SIATAEH_MAGIC, STIHU_MATERIALS, CILLIATNAH_INFLUENCE

    MONTH += 1
    
    # --- 1. Resource Generation ---
    # S-iataeh generation boosted by J-ampejinne influence
    magic_gain = JAMPEJINNE_INFLUENCE * 10
    SIATAEH_MAGIC += magic_gain
    
    # S-tihuu generation is steady
    STIHU_MATERIALS += 30
    
    # --- 2. R-oykenne Progress ---
    # Base progress, slowed by F-'illianarre and G-agoikenne
    base_progress = 10
    
    # Slowdown from F-'illianarre Fighters (1% per 10 fighters)
    fighter_defense = FIGHTER_STRENGTH // 10
    
    # G-agoikenne Portal Defense (effective until 25% invasion)
    if ROYKENNE_PROGRESS < 25:
        base_progress -= 5
    
    invasion_gain = max(0, base_progress - fighter_defense)
    ROYKENNE_PROGRESS += invasion_gain
    
    # --- 3. X-iangxong Threat Check ---
    if ROYKENNE_PROGRESS >= 75:
        print(f"{Color.ENEMY}!! WARNING !! The X-iangxong is mobilizing! Defense is critical!{Color.RESET}")

    if ROYKENNE_PROGRESS >= 100:
        game_over()
        
    print(f"\n{Color.HEADER}--- MONTH {MONTH} REPORT ---{Color.RESET}")
    print(f"Magic Gained: +{magic_gain} | Materials Gained: +30")
    print(f"R-oykenne Progress: +{invasion_gain}%")
    
    # Random event: Faction demands
    if random.random() < 0.2:
        print(f"{Color.MAGIC}The J-ampejinne demand more attention. (-1 C-'illiatnah Influence){Color.RESET}")
        CILLIATNAH_INFLUENCE = max(1, CILLIATNAH_INFLUENCE - 1)
        
    input(f"\nPress ENTER to continue...")

def perform_action(choice):
    """Handles player strategic choices."""
    global STIHU_MATERIALS, SIATAEH_MAGIC, FIGHTER_STRENGTH, CILLIATNAH_INFLUENCE, JAMPEJINNE_INFLUENCE, ROYKENNE_PROGRESS, HAS_BATOBWATCHAEH

    # Resource check helper
    def check_and_pay(m, s):
        if SIATAEH_MAGIC >= m and STIHU_MATERIALS >= s:
            SIATAEH_MAGIC -= m
            STIHU_MATERIALS -= s
            return True
        else:
            print(f"{Color.ENEMY}Insufficient resources! Needs S-iataeh: {m}, S-tihuu: {s}{Color.RESET}")
            return False

    if choice == '1': # DEPLOY FORCES
        cost_m, cost_s = 20, 40
        if check_and_pay(cost_m, cost_s):
            FIGHTER_STRENGTH += 15
            print(f"{Color.EARTH}New F-'illianarre unit deployed! Fighter Strength +15.{Color.RESET}")
        
    elif choice == '2': # RESEARCH (L-enemketobontette)
        print("\n--- RESEARCH / CONVERSION ---")
        print("21) Convert S-iataeh (Magic) to F-'illianarre (Fighter Strength) - Cost: 50 M, 50 S")
        print("22) Upgrade C-'illiatnah Influence (Research Efficiency) - Cost: 100 M, 100 S")
        r_choice = input("Research Option: ").strip()

        if r_choice == '21':
            cost_m, cost_s = 50, 50
            if check_and_pay(cost_m, cost_s):
                # Conversion based on research influence
                gain = 10 + CILLIATNAH_INFLUENCE * 2
                FIGHTER_STRENGTH += gain
                print(f"{Color.MAGIC}L-enemketobontette conversion successful. Fighter Strength +{gain}.{Color.RESET}")
        elif r_choice == '22':
            cost_m, cost_s = 100, 100
            if check_and_pay(cost_m, cost_s):
                CILLIATNAH_INFLUENCE += 1
                print(f"{Color.HEADER}C-'illiatnah Influence improved! Research efficiency increased.{Color.RESET}")
        else:
            print(f"{Color.ENEMY}Invalid research choice.{Color.RESET}")

    elif choice == '3': # DIPLOMACY / ARTIFACT
        print("\n--- DIPLOMACY / ARTIFACT SEARCH ---")
        print("31) Negotiate with J-ampejinne (Boost S-iataeh income) - Cost: 50 S")
        print("32) Search for B-atobwatchaeh (Artifact) - Cost: 150 S, 150 M")
        print("33) Final Victory Push (Requires >100 Fighters and Low R-oykenne Progress)")
        d_choice = input("Diplomacy Option: ").strip()

        if d_choice == '31':
            cost_m, cost_s = 0, 50
            if check_and_pay(cost_m, cost_s):
                JAMPEJINNE_INFLUENCE += 1
                print(f"{Color.MAGIC}J-ampejinne negotiations successful! Magic resource income boosted.{Color.RESET}")
        elif d_choice == '32' and not HAS_BATOBWATCHAEH:
            cost_m, cost_s = 150, 150
            if check_and_pay(cost_m, cost_s):
                if random.random() > 0.3: # 70% chance of success
                    global HAS_BATOBWATCHAEH; HAS_BATOBWATCHAEH = True
                    print(f"{Color.ITEM}The B-atobwatchaeh is recovered! Gives +10 Defense per month.{Color.RESET}")
                else:
                    print(f"{Color.ENEMY}Search failed. Lost resources.{Color.RESET}")
        elif d_choice == '33':
            if FIGHTER_STRENGTH >= 100 and ROYKENNE_PROGRESS < 40:
                print(f"{Color.HEALTH}With overwhelming F-'illianarre strength, you launch the final offensive!{Color.RESET}")
                if HAS_BATOBWATCHAEH:
                    ROYKENNE_PROGRESS -= 50
                else:
                    ROYKENNE_PROGRESS -= 30
                
                if ROYKENNE_PROGRESS <= 0:
                    victory()
                else:
                    print(f"R-oykenne Progress reduced! New Progress: {ROYKENNE_PROGRESS}%.")
            else:
                print(f"{Color.ENEMY}Not strong enough or too late! Needs >100 Fighters and <40% Progress.{Color.RESET}")
        else:
            print(f"{Color.ENEMY}Invalid diplomacy choice or B-atobwatchaeh already active.{Color.RESET}")
    
    elif choice.lower() == 'q':
        sys.exit()

# --- MAIN GAME EXECUTION ---

def start_game():
    clear_screen()
    print(Color.BOLD + Color.HEADER + "=" * 60 + Color.RESET)
    print(Color.BOLD + Color.HEADER + "{:^60}".format("LANDSOFAGES3: THE KING'S FINAL EDICT") + Color.RESET)
    print(Color.BOLD + Color.ENEMY + "{:^60}".format("A Strategy Simulator") + Color.RESET)
    print(Color.BOLD + Color.HEADER + "=" * 60 + Color.RESET)
    
    input("\nPress ENTER to assume command as Chancellor...")
    
    while True:
        clear_screen()
        display_status()

        # Check for B-atobwatchaeh active defense
        if HAS_BATOBWATCHAEH:
            global FIGHTER_STRENGTH
            FIGHTER_STRENGTH += 1 # Minor continuous bonus
            
        print("\n--- ACTIONS (Select 1-3 to spend resources, then 0 to end month) ---")
        print("1) DEPLOY F-'ILLIANARRE (Fighters): Cost 20 M, 40 S")
        print("2) RESEARCH at L-ENEMKETOBONTETTE (Convert Magic/Upgrade Research)")
        print("3) DIPLOMACY & FINAL PUSH (Negotiate/Search for Artifact/Final Attack)")
        print("0) ADVANCE MONTH (End Turn & Check R-oykenne Progress)")
        print("Q) Quit")

        choice = input("\nEnter Action (1/2/3/0/Q): ").strip()
        
        if choice == '0':
            advance_month()
        elif choice in ('1', '2', '3', 'q', 'Q'):
            perform_action(choice)
        else:
            print(f"{Color.ENEMY}Invalid input. Try again.{Color.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    start_game()
