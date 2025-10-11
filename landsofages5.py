# landsofages5.py
import os
import time
import sys

# --- ANSI Color Codes ---
class Color:
    HEADER = '\033[95m'
    MAGIC = '\033[94m'      # Blue
    CYBER = '\033[93m'      # Yellow
    RESOURCE = '\033[92m'   # Green
    ENEMY = '\033[91m'      # Red
    BOLD = '\033[1m'
    RESET = '\033[0m'

# --- Game State ---
# Resources
magic_aura = 50       # A-riatnah output
cyber_power = 20      # L-enemketobontette output
stihuu_raw = 100      # S-tihuu (Earth) raw material

# Infrastructure & Personnel
illianarre_agents = 5   # I-llianarre (Manpower)
cilliatnah_scholars = 1 # C-'illiatnah (Research conversion)
fillianarre_fighters = 2# F-'illianarre (Defense)

# Infrastructure Status
project_ariatah_level = 1
project_lenemketobontette_level = 1
project_gagoikenne_built = False
has_power_orb = False
turn_count = 1

# --- Utilities ---
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_hud():
    """Renders the resource and personnel status."""
    print(Color.BOLD + "=" * 60 + Color.RESET)
    print(f"TURN: {turn_count} | Z-azoykenne Corruption: {turn_count * 0.5}%")
    print("-" * 60)
    print(f"{Color.MAGIC}MAGIC AURA: {magic_aura:<8}{Color.RESET} | {Color.CYBER}CYBER POWER: {cyber_power:<8}{Color.RESET} | {Color.RESOURCE}S-TIHUU RAW: {stihuu_raw:<8}{Color.RESET}")
    print(f"Agents (I-llianarre): {illianarre_agents} | Scholars (C-'illiatnah): {cilliatnah_scholars} | Fighters (F-'illianarre): {fillianarre_fighters}")
    print(Color.BOLD + "=" * 60 + Color.RESET)

def advance_turn():
    """Calculates resource generation and handles events."""
    global magic_aura, cyber_power, stihuu_raw, illianarre_agents, turn_count

    turn_count += 1
    
    # 1. Base Resource Generation (Modified by Z-azoykenne)
    corruption_factor = 1 - (turn_count * 0.005) # Z-azoykenne effect
    
    # A-riatnah (Magic Aura)
    magic_gain = int(project_ariatah_level * illianarre_agents * 5 * corruption_factor)
    magic_aura += magic_gain
    
    # L-enemketobontette (Cyber Power)
    cyber_gain = int(project_lenemketobontette_level * illianarre_agents * 3 * corruption_factor)
    cyber_power += cyber_gain
    
    # Raw Materials
    stihuu_raw += illianarre_agents * 10
    
    print(f"\n{Color.HEADER}--- TURN {turn_count} REPORT ---{Color.RESET}")
    print(f"Magic Gained: +{magic_gain} | Cyber Gained: +{cyber_gain} | S-tihuu Gathered: +{illianarre_agents * 10}")
    
    # 2. Random Event: G-rudge Attack
    if turn_count % 5 == 0 and fillianarre_fighters < 5:
        threat = random.randint(1, 10)
        if threat > fillianarre_fighters:
            damage = threat * 10
            magic_aura -= damage
            cyber_power -= damage
            print(f"{Color.ENEMY}!! G-RUDGE ATTACK !! Fighters (F-'illianarre) failed to defend. Lost {damage} Aura and Power!{Color.RESET}")
            if magic_aura < 0 or cyber_power < 0:
                print(f"{Color.ENEMY}The corruption has overwhelmed the infrastructure.{Color.RESET}")
                game_over()
    
    # 3. Check Victory Condition
    if has_power_orb:
        victory()

def perform_action(choice):
    """Handles player actions (Build, Research, Recruit)."""
    global stihuu_raw, magic_aura, cyber_power
    global project_ariatah_level, project_lenemketobontette_level, illianarre_agents, fillianarre_fighters, cilliatnah_scholars, project_gagoikenne_built, has_power_orb

    # --- Project Costs ---
    COSTS = {
        # S-tihuu, Magic, Cyber
        "ARIATNAH_UP": (150, 50, 0),
        "LENEMKETOBONTETTE_UP": (150, 0, 50),
        "RECRUIT_AGENT": (50, 20, 0),
        "RECRUIT_FIGHTER": (80, 50, 0),
        "RECRUIT_SCHOLAR": (100, 30, 30),
        "GAGOIKENNE_BUILD": (300, 150, 150),
        "OICHENNE_CRAFT": (500, 300, 300)
    }

    def check_and_pay(cost_key):
        s, m, c = COSTS.get(cost_key, (10000, 10000, 10000)) # Fail-safe high cost
        if stihuu_raw >= s and magic_aura >= m and cyber_power >= c:
            stihuu_raw -= s
            magic_aura -= m
            cyber_power -= c
            return True
        else:
            print(f"{Color.ENEMY}Insufficient resources! Needs S-tihuu: {s}, Magic: {m}, Cyber: {c}{Color.RESET}")
            return False

    if choice == '1': # BUILD / UPGRADE
        print(f"\n--- BUILD/UPGRADE (S-tihuu: {stihuu_raw}) ---")
        print("11) Upgrade A-riatnah (Village): Level +1 (Cost: 150 S, 50 M)")
        print("12) Upgrade L-enemketobontette (Hub): Level +1 (Cost: 150 S, 50 C)")
        print("13) Build G-agoikenne (Portal Gateway) (Cost: 300 S, 150 M, 150 C)")
        build_choice = input("Build Option: ").strip()

        if build_choice == '11' and check_and_pay("ARIATNAH_UP"):
            project_ariatah_level += 1
            print(f"{Color.MAGIC}A-riatnah upgraded to Level {project_ariatah_level}! Magic Aura output increased.{Color.RESET}")
        elif build_choice == '12' and check_and_pay("LENEMKETOBONTETTE_UP"):
            project_lenemketobontette_level += 1
            print(f"{Color.CYBER}L-enemketobontette upgraded to Level {project_lenemketobontette_level}! Cyber Power output increased.{Color.RESET}")
        elif build_choice == '13' and not project_gagoikenne_built and check_and_pay("GAGOIKENNE_BUILD"):
            project_gagoikenne_built = True
            print(f"{Color.RESOURCE}G-agoikenne Portal Gateway built! Opens new raw material routes.{Color.RESET}")
            global stihuu_raw; stihuu_raw += 100 # Immediate bonus
        else:
            print(f"{Color.ENEMY}Invalid choice or insufficient funds.{Color.RESET}")

    elif choice == '2': # RECRUIT / TRAIN
        print("\n--- RECRUIT / TRAIN ---")
        print("21) Recruit I-llianarre Agent (Manpower) (Cost: 50 S, 20 M)")
        print("22) Train F-'illianarre Fighter (Defense) (Cost: 80 S, 50 M)")
        print("23) Train C-'illiatnah Scholar (Research) (Cost: 100 S, 30 M, 30 C)")
        recruit_choice = input("Recruit Option: ").strip()

        if recruit_choice == '21' and check_and_pay("RECRUIT_AGENT"):
            illianarre_agents += 1
            print(f"{Color.RESOURCE}New I-llianarre Agent recruited. Resource gathering boosted.{Color.RESET}")
        elif recruit_choice == '22' and check_and_pay("RECRUIT_FIGHTER"):
            fillianarre_fighters += 1
            print(f"{Color.RESOURCE}New F-'illianarre Fighter trained. Defense boosted.{Color.RESET}")
        elif recruit_choice == '23' and check_and_pay("RECRUIT_SCHOLAR"):
            cilliatnah_scholars += 1
            print(f"{Color.RESOURCE}New C-'illiatnah Scholar trained. Research capability gained.{Color.RESET}")
        else:
            print(f"{Color.ENEMY}Invalid choice or insufficient funds.{Color.RESET}")

    elif choice == '3': # RESEARCH / CRAFT
        print("\n--- RESEARCH / CRAFT ---")
        print(f"31) Research: Convert 10 M Aura to 10 C Power (Requires: {cilliatnah_scholars} Scholars)")
        print("32) Craft O-ichenne (Power Orb) (Final Goal) (Cost: 500 S, 300 M, 300 C)")
        research_choice = input("Craft Option: ").strip()

        if research_choice == '31':
            if cilliatnah_scholars > 0:
                conversion = cilliatnah_scholars * 10
                if magic_aura >= conversion:
                    magic_aura -= conversion
                    cyber_power += conversion
                    print(f"{Color.CYBER}{conversion} Aura converted to {conversion} Power via C-'illiatnah Scholars.{Color.RESET}")
                else:
                    print(f"{Color.ENEMY}Not enough Magic Aura for conversion.{Color.RESET}")
            else:
                print(f"{Color.ENEMY}Need C-'illiatnah Scholars to perform research!{Color.RESET}")
        elif research_choice == '32' and check_and_pay("OICHENNE_CRAFT"):
            has_power_orb = True
            print(f"{Color.HEADER}*** The O-ICHENNE (Power Orb) is crafted! Mission success imminent! ***{Color.RESET}")
        else:
            print(f"{Color.ENEMY}Invalid choice or insufficient funds.{Color.RESET}")
    
    elif choice.lower() == 'q':
        sys.exit()

def game_over():
    clear_screen()
    print(Color.BOLD + Color.ENEMY + "\n" * 5)
    print("{:^60}".format("THE Z-AZOYKENNE CORRUPTION WINS. GAME OVER."))
    print("{:^60}".format("The Royal Forces' rebuilding effort has failed."))
    print("\n" * 5 + Color.RESET)
    sys.exit()

def victory():
    clear_screen()
    print(Color.BOLD + Color.MAGIC + "\n" * 5)
    print("{:^60}".format("✨ O-ICHENNE ACTIVATED! TAHKMAHNELLE STABILIZED! ✨"))
    print("{:^60}".format(f"The Royal Forces have successfully completed the rebuilding effort in {turn_count} turns."))
    print("\n" * 5 + Color.RESET)
    sys.exit()

# --- Main Game Loop ---
def start_game():
    clear_screen()
    print(Color.BOLD + Color.HEADER + "{:^60}".format("LANDSOFAGES5: THE REBUILDING EDICT") + Color.RESET)
    print(Color.BOLD + Color.RESOURCE + "{:^60}".format("Command the Royal Forces!") + Color.RESET)
    
    input("\nPress ENTER to begin the strategic rebuilding of Tahkmahnelle...")
    
    while True:
        clear_screen()
        draw_hud()

        # Display Infrastructure Status
        print("\n--- INFRASTRUCTURE STATUS ---")
        print(f"A-riatnah (Village): Level {project_ariatah_level}")
        print(f"L-enemketobontette (Hub): Level {project_lenemketobontette_level}")
        print(f"G-agoikenne (Portal): {'ONLINE' if project_gagoikenne_built else 'OFFLINE'}")
        
        # Display Goal Status
        print(f"\nGOAL: {'✅' if has_power_orb else '❌'} Craft O-ichenne (Power Orb)")
        
        # Player Options
        print("\n--- ACTIONS ---")
        print("1) BUILD / UPGRADE Infrastructure")
        print("2) RECRUIT / TRAIN Personnel")
        print("3) RESEARCH / CRAFT")
        print("0) ADVANCE TURN (End Turn)")
        print("Q) Quit")

        choice = input("\nEnter Action (1/2/3/0/Q): ").strip()
        
        if choice == '0':
            advance_turn()
        elif choice in ('1', '2', '3', 'q', 'Q'):
            perform_action(choice)
        else:
            print(f"{Color.ENEMY}Invalid input. Try again.{Color.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    import random # Import needed for random events in advance_turn
    start_game()
