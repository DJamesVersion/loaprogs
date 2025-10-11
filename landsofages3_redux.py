# landsofages3_redux.py
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
TURN = 1
MAX_TURNS = 10
ROYKENNE_PROGRESS = 0    # 100 wins the game for the enemy
FIGHTER_STRENGTH = 10    # F-'illianarre force level

# Resources
SIATAEH_MAGIC = 100       # S-iataeh (Air/Magic)
STIHU_MATERIALS = 100     # S-tihuu (Earth/Materials)

# Faction Influence (Determines Resource Generation)
JAMPEJINNE_BONUS = 15  # J-ampejinne (Magic income per turn)
CILLIATNAH_BONUS = 5   # C-'illiatnah (Research conversion efficiency)

# --- UTILITIES ---

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def game_over():
    clear_screen()
    print(Color.BOLD + Color.ENEMY + "\n" * 5)
    print("{:^60}".format("💀 THE X-IANGXONG HAS BREACHED THE G-AGOIKENNE! 💀"))
    print("{:^60}".format("The R-oykenne's final edict is absolute."))
    print("\n" * 5 + Color.RESET)
    sys.exit()

def victory():
    clear_screen()
    print(Color.BOLD + Color.MAGIC + "\n" * 5)
    print("{:^60}".format("👑 R-OYKENNE DEFEATED! TAHKMAHNELLE SECURE! 👑"))
    print(f"{:^60}".format(f"The Final Edict was stopped in {TURN} months."))
    print("\n" * 5 + Color.RESET)
    sys.exit()

def display_status():
    """Renders the strategic status."""
    invasion_color = Color.ENEMY if ROYKENNE_PROGRESS > 50 else Color.YELLOW
    
    print(Color.BOLD + "=" * 60 + Color.RESET)
    print(f"MONTH: {TURN}/{MAX_TURNS} | {Color.ENEMY}R-OYKENNE INVASION:{Color.RESET} {invasion_color}{ROYKENNE_PROGRESS}%{Color.RESET}")
    print("-" * 60)
    print(f"{Color.MAGIC}S-IATAEH (Magic): {SIATAEH_MAGIC:<8}{Color.RESET} | {Color.EARTH}S-TIHUU (Materials): {STIHU_MATERIALS:<8}{Color.RESET}")
    print(f"FIGHTERS (F-'illianarre): {FIGHTER_STRENGTH}")
    print(f"Magic Income (J-ampejinne): +{JAMPEJINNE_BONUS} | Research Efficiency (C-'illiatnah): {CILLIATNAH_BONUS}")
    print(Color.BOLD + "=" * 60 + Color.RESET)

def advance_month():
    """Calculates resource generation and enemy progress."""
    global TURN, ROYKENNE_PROGRESS, SIATAEH_MAGIC, STIHU_MATERIALS, JAMPEJINNE_BONUS

    TURN += 1
    
    # --- 1. Resource Generation ---
    SIATAEH_MAGIC += JAMPEJINNE_BONUS
    STIHU_MATERIALS += 25 # Base Stihuu generation
    
    # --- 2. R-oykenne Progress ---
    base_progress = 12
    
    # Slowdown from F-'illianarre Fighters (1% per 10 fighters)
    fighter_defense = FIGHTER_STRENGTH // 10
    
    # G-agoikenne Defense (Portal Gateway) slows the initial advance
    gagoikenne_defense = 4 if TURN < 5 else 0
    
    invasion_gain = max(0, base_progress - fighter_defense - gagoikenne_defense)
    ROYKENNE_PROGRESS += invasion_gain
    
    print(f"\n{Color.HEADER}--- MONTH {TURN} REPORT ---{Color.RESET}")
    print(f"Magic Gained: +{JAMPEJINNE_BONUS} | Materials Gained: +25")
    print(f"R-oykenne Progress: +{invasion_gain}% (Current: {ROYKENNE_PROGRESS}%)")
    
    # Check for loss conditions
    if ROYKENNE_PROGRESS >= 100:
        game_over()
    if TURN > MAX_TURNS:
        print(f"{Color.ENEMY}Time ran out! The X-iangxong is too close.{Color.RESET}")
        game_over()
    
    # Check for Victory Condition
    if FIGHTER_STRENGTH >= 150 and ROYKENNE_PROGRESS < 40:
        print(f"{Color.MAGIC}The F-'illianarre forces are overwhelming! Launching final counter-assault...{Color.RESET}")
        ROYKENNE_PROGRESS -= 50
        if ROYKENNE_PROGRESS <= 0:
            victory()

def perform_action(choice):
    """Handles player strategic choices."""
    global STIHU_MATERIALS, SIATAEH_MAGIC, FIGHTER_STRENGTH, CILLIATNAH_BONUS, JAMPEJINNE_BONUS, ROYKENNE_PROGRESS

    # Resource check helper
    def check_and_pay(m, s):
        if SIATAEH_MAGIC >= m and STIHU_MATERIALS >= s:
            SIATAEH_MAGIC -= m
            STIHU_MATERIALS -= s
            return True
        else:
            print(f"{Color.ENEMY}Insufficient resources! Needs S-iataeh: {m}, S-tihuu: {s}{Color.RESET}")
            return False

    if choice == '1': # DEPLOY F-'ILLIANARRE (Fighters)
        cost_m, cost_s = 20, 50
        if check_and_pay(cost_m, cost_s):
            FIGHTER_STRENGTH += 20
            print(f"{Color.EARTH}New F-'illianarre unit deployed! Fighter Strength +20.{Color.RESET}")
        
    elif choice == '2': # L-ENEMKETOBONTETTE RESEARCH
        print("\n--- RESEARCH / CONVERSION (L-enemketobontette) ---")
        print("21) **C-'illiatnah** Research: Improve conversion efficiency (Cost: 100 M, 100 S)")
        print("22) Convert Magic (S-iataeh) to Fighters (F-'illianarre) (Cost: 60 M, 30 S)")
        r_choice = input("Research Option: ").strip()

        if r_choice == '21':
            cost_m, cost_s = 100, 100
            if check_and_pay(cost_m, cost_s):
                global CILLIATNAH_BONUS
                CILLIATNAH_BONUS += 2
                print(f"{Color.HEADER}C-'illiatnah Research efficiency improved!{Color.RESET}")
        elif r_choice == '22':
            cost_m, cost_s = 60, 30
            if check_and_pay(cost_m, cost_s):
                # Conversion based on C-'illiatnah Research bonus
                gain = 10 + CILLIATNAH_BONUS
                FIGHTER_STRENGTH += gain
                print(f"{Color.MAGIC}Magic converted to Fighters! Strength +{gain}.{Color.RESET}")
        else:
            print(f"{Color.ENEMY}Invalid research choice.{Color.RESET}")

    elif choice == '3': # DIPLOMACY & SPECIAL ACTIONS
        print("\n--- DIPLOMACY / SPECIAL ACTIONS ---")
        print("31) Negotiate with **J-ampejinne** (Boost S-iataeh income) (Cost: 50 S)")
        print("32) Defensive Counter-Spell on **G-agoikenne** (Reduce R-oykenne Progress) (Cost: 150 M)")
        d_choice = input("Special Action: ").strip()

        if d_choice == '31':
            cost_m, cost_s = 0, 50
            if check_and_pay(cost_m, cost_s):
                global JAMPEJINNE_BONUS
                JAMPEJINNE_BONUS += 10
                print(f"{Color.MAGIC}J-ampejinne negotiations successful! Magic income +10.{Color.RESET}")
        elif d_choice == '32':
            cost_m, cost_s = 150, 0
            if check_and_pay(cost_m, cost_s):
                reduction = random.randint(10, 20)
                ROYKENNE_PROGRESS = max(0, ROYKENNE_PROGRESS - reduction)
                print(f"{Color.MAGIC}Counter-Spell successful! R-oykenne Progress reduced by {reduction}%.{Color.RESET}")
        else:
            print(f"{Color.ENEMY}Invalid action.{Color.RESET}")
    
    elif choice.lower() == 'q':
        sys.exit()

# --- MAIN GAME EXECUTION ---

def start_game():
    clear_screen()
    print(Color.BOLD + Color.HEADER + "=" * 60 + Color.RESET)
    print(Color.BOLD + Color.HEADER + "{:^60}".format("LANDSOFAGES3: THE KING'S FINAL EDICT (REDUX)") + Color.RESET)
    print(Color.BOLD + Color.ENEMY + "{:^60}".format("The X-iangxong is Coming") + Color.RESET)
    print(Color.BOLD + Color.HEADER + "=" * 60 + Color.RESET)
    
    input("\nPress ENTER to assume command as Chancellor...")
    
    while True:
        clear_screen()
        display_status()
            
        print("\n--- ACTIONS (Select 1-3 to spend resources, then 0 to end month) ---")
        print("1) DEPLOY F-'ILLIANARRE (Fighters): Spend S-tihuu/S-iataeh to increase strength.")
        print("2) RESEARCH at L-ENEMKETOBONTETTE (Improve efficiency or convert magic).")
        print("3) DIPLOMACY & SPECIAL ACTIONS (Boost income or launch defensive spells).")
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

