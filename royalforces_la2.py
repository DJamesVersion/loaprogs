# royalforces_la2.py
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
    PLANET_HAB = '\033[94m' # Blue
    PLANET_UNHAB = '\033[91m' # Red
    DWARF = '\033[96m'     # Cyan
    BOLD = '\033[1m'
    RESET = '\033[0m'

# --- GLOBAL GAME VARIABLES ---
MONTH = 1
MAX_MONTHS = 15
COLONY_RESOURCES = 100 # Starting resource pool
TERRAFORM_SCORE = 0  # Goal: 100
CURRENT_LOCATION = "TAHKMAHNELLE ORBIT"
SHIP_LEVEL = 1       # Affects travel speed and resource gathering
HAS_MAP = False      # Required to navigate to TAHKMAHNELLE45

# --- PLANET DATA ---
PLANETS = {
    # Name: (Habitability, Resource_Gain, Time_Cost, Status_Color)
    "lenemketobontette": (False, 0, 2, Color.PLANET_UNHAB),
    "stihuu": (True, 30, 1, Color.PLANET_HAB),
    "tetnobautte": (True, 40, 1, Color.PLANET_HAB),
    "vraelvrae": (True, 50, 2, Color.PLANET_HAB),
    "lenemketobontettestihuu": (False, 0, 3, Color.PLANET_UNHAB),
    "TAHKMAHNELLE45": (True, 0, 0, Color.DWARF) # Destination
}

# --- UTILITIES ---

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def game_over(reason="Enemy forces intercepted your signal"):
    clear_screen()
    print(Color.BOLD + Color.ENEMY + "\n" * 5)
    print("{:^60}".format("MISSION ABORTED: TAHKMAHNELLE45 COMPROMISED!"))
    print(f"{:^60}".format(f"Reason: {reason}."))
    print("\n" * 5 + Color.RESET)
    sys.exit()

def victory():
    clear_screen()
    print(Color.BOLD + Color.DWARF + "\n" * 5)
    print("{:^60}".format("🚀 COLONY ESTABLISHED! TAHKMAHNELLE45 SECURE! 🚀"))
    print(f"{:^60}".format(f"The Royal Forces secured the future in {MONTH} months."))
    print("\n" * 5 + Color.RESET)
    sys.exit()

def display_status():
    """Renders the colonization status."""
    time_color = Color.TIME if MONTH < 10 else Color.ENEMY
    
    print(Color.BOLD + "=" * 60 + Color.RESET)
    print(f"{Color.HEADER}LOCATION:{Color.RESET} {CURRENT_LOCATION} | {time_color}MONTH:{Color.RESET} {MONTH}/{MAX_MONTHS}")
    print("-" * 60)
    print(f"{Color.HEALTH}RESOURCES:{Color.RESET} {COLONY_RESOURCES:<8} | {Color.DWARF}TERRAFORM SCORE:{Color.RESET} {TERRAFORM_SCORE}/100")
    print(f"Ship Level: {SHIP_LEVEL} | Navigation: {'ACTIVE' if HAS_MAP else 'INACTIVE'}")
    print(Color.BOLD + "=" * 60 + Color.RESET)

def advance_month(cost=1):
    """Increments the month count and checks for game over."""
    global MONTH
    MONTH += cost
    
    if MONTH > MAX_MONTHS:
        game_over("Time limit exceeded")

# --- SCENES/ACTIONS ---

def scene_main_orbit():
    """The central hub for travel and upgrades."""
    global CURRENT_LOCATION, SHIP_LEVEL, COLONY_RESOURCES, HAS_MAP

    clear_screen()
    display_status()
    
    print("\n--- ORBITAL COMMAND ACTIONS ---")
    print("1) Travel to a Planet")
    print("2) Upgrade Ship Capacity/Speed (Cost: 100 Resources per Level)")
    print("3) Search for the **TAHKMAHNELLE45** Map (Cost: 50 Resources, requires Ship Level 2)")
    print("0) Pass Time / Maintain Orbit (Advance 1 Month)")
    
    choice = input("\nEnter Action (1/2/3/0): ").strip()
    
    if choice == '1':
        scene_travel_selection()
        return
    
    elif choice == '2':
        cost = SHIP_LEVEL * 100
        if COLONY_RESOURCES >= cost:
            COLONY_RESOURCES -= cost
            SHIP_LEVEL += 1
            print(f"{Color.HEALTH}Ship upgraded to Level {SHIP_LEVEL}! Efficiency increased.{Color.RESET}")
        else:
            print(f"{Color.ENEMY}Insufficient resources. Need {cost} resources.{Color.RESET}")
    
    elif choice == '3':
        if HAS_MAP:
            print(f"{Color.DWARF}You already possess the map! Go to Travel (1).{Color.RESET}")
        elif SHIP_LEVEL >= 2 and COLONY_RESOURCES >= 50:
            COLONY_RESOURCES -= 50
            HAS_MAP = True
            print(f"{Color.DWARF}The secret navigational map to TAHKMAHNELLE45 has been found!{Color.RESET}")
        else:
            print(f"{Color.ENEMY}Need Ship Level 2 and 50 resources to attempt the search.{Color.RESET}")
    
    elif choice == '0':
        print("Holding position and performing routine maintenance.")
        advance_month(1)
        
    else:
        print(f"{Color.ENEMY}Invalid command.{Color.RESET}")

    time.sleep(1.5)

def scene_travel_selection():
    """Allows selection of destination planet."""
    global CURRENT_LOCATION
    
    clear_screen()
    display_status()
    
    print("\n--- TRAVEL DESTINATIONS ---")
    
    options = {}
    i = 1
    
    # List all main solar system planets
    for name, data in PLANETS.items():
        if name == "TAHKMAHNELLE45" and not HAS_MAP: continue
        
        hab = "Habitable" if data[0] else "Uninhabitable"
        cost = max(1, data[2] - (SHIP_LEVEL // 2)) # Ship level reduces travel time
        
        print(f"{i}) {data[3]}{name}{Color.RESET} ({hab}) - Est. Time: {cost} months")
        options[str(i)] = (name, cost)
        i += 1
    
    print(f"{i}) Return to TAHKMAHNELLE ORBIT")
    options[str(i)] = ("TAHKMAHNELLE ORBIT", 0)
    
    choice = input("\nEnter destination number: ").strip()
    
    if choice in options:
        dest, time_cost = options[choice]
        if dest == CURRENT_LOCATION:
            print("You are already there!")
            time.sleep(1)
            return
            
        print(f"Initiating jump to {dest}. Travel Time: {time_cost} months.")
        
        # Uninhabitable hazards
        if PLANETS.get(dest, (False, 0, 0))[0] is False:
            if random.random() < 0.4:
                print(f"{Color.ENEMY}Navigation hazard near {dest}! Lost 10 Resources.{Color.RESET}")
                global COLONY_RESOURCES
                COLONY_RESOURCES = max(0, COLONY_RESOURCES - 10)
        
        advance_month(time_cost)
        CURRENT_LOCATION = dest
        
    else:
        print(f"{Color.ENEMY}Invalid destination.{Color.RESET}")
        time.sleep(1.5)

def scene_planet_action():
    """Actions specific to the destination planet."""
    global CURRENT_LOCATION, COLONY_RESOURCES, TERRAFORM_SCORE, SHIP_LEVEL
    
    planet_data = PLANETS[CURRENT_LOCATION]
    
    if CURRENT_LOCATION == "TAHKMAHNELLE45":
        scene_dwarf_planet_action()
        return

    clear_screen()
    display_status()
    
    print(f"\n--- ACTIONS AT {CURRENT_LOCATION} ({'Habitable' if planet_data[0] else 'Uninhabitable'}) ---")
    
    if planet_data[0] is False:
        print("This planet is **Uninhabitable**. Cannot gather resources here.")
        print("1) Return to TAHKMAHNELLE ORBIT")
    else:
        base_gain = planet_data[1] + (SHIP_LEVEL * 10) # Resource gain boosted by Ship Level
        print(f"1) Gather Resources (Gain: {base_gain} Resources, 1 Month Cost)")
        print("2) Return to TAHKMAHNELLE ORBIT")
        
    choice = input("\nEnter Action (1/2): ").strip()
    
    if planet_data[0] is True and choice == '1':
        COLONY_RESOURCES += base_gain
        advance_month(1)
        print(f"{Color.HEALTH}Gathering complete. Gained {base_gain} Resources!{Color.RESET}")
    elif choice == '2' or (planet_data[0] is False and choice == '1'):
        CURRENT_LOCATION = "TAHKMAHNELLE ORBIT"
        print("Returning to Orbit...")
        time.sleep(1)
    else:
        print(f"{Color.ENEMY}Invalid command.{Color.RESET}")
        time.sleep(1.5)

def scene_dwarf_planet_action():
    """Actions specific to the destination planet."""
    global COLONY_RESOURCES, TERRAFORM_SCORE, CURRENT_LOCATION
    
    clear_screen()
    display_status()
    
    print(f"\n--- TAHKMAHNELLE45 COLONY SITE ACTIONS ---")
    
    if TERRAFORM_SCORE >= 100:
        victory()
        
    # Cost scales up slightly as the score increases
    cost = 50 + (TERRAFORM_SCORE // 10)
    terraform_gain = 10 + (SHIP_LEVEL * 2) # Terraform gain boosted by Ship Level

    print(f"1) Build/Terraform Colony (Cost: {cost} Resources, Gain: {terraform_gain} Terraform Score)")
    print("2) Return to TAHKMAHNELLE ORBIT")

    choice = input("\nEnter Action (1/2): ").strip()

    if choice == '1':
        if COLONY_RESOURCES >= cost:
            COLONY_RESOURCES -= cost
            TERRAFORM_SCORE += terraform_gain
            print(f"{Color.DWARF}Terraforming successful. Score +{terraform_gain}. ({TERRAFORM_SCORE}/100){Color.RESET}")
            advance_month(1)
        else:
            print(f"{Color.ENEMY}Insufficient resources. Need {cost} resources for terraforming.{Color.RESET}")
            time.sleep(1.5)
    elif choice == '2':
        CURRENT_LOCATION = "TAHKMAHNELLE ORBIT"
        print("Returning to Orbit...")
        time.sleep(1)
    else:
        print(f"{Color.ENEMY}Invalid command.{Color.RESET}")
        time.sleep(1.5)

# --- MAIN GAME EXECUTION ---

def start_game():
    clear_screen()
    print(Color.BOLD + Color.HEADER + "=" * 60 + Color.RESET)
    print(Color.BOLD + Color.HEADER + "{:^60}".format("ROYALFORCES2LANDSOFAGES") + Color.RESET)
    print(Color.BOLD + Color.DWARF + "{:^60}".format("Colonization of TAHKMAHNELLE45") + Color.RESET)
    print(Color.BOLD + Color.HEADER + "=" * 60 + Color.RESET)
    
    print("Welcome, Commander. Your mission is to establish a colony on the secret dwarf planet, **TAHKMAHNELLE45**.")
    print(f"You have {MAX_MONTHS} months before the enemy forces detect the hidden location and compromise the mission.")
    input("Press ENTER to begin the operation...")
    
    while True:
        if CURRENT_LOCATION == "TAHKMAHNELLE ORBIT":
            scene_main_orbit()
        elif CURRENT_LOCATION in PLANETS:
            scene_planet_action()
        else:
            # Fallback (shouldn't happen)
            CURRENT_LOCATION = "TAHKMAHNELLE ORBIT"

if __name__ == "__main__":
    start_game()
