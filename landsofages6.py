import os
import time
import random
import sys

# --- ANSI Color Codes ---
class Color:
    BLUE_HERO = '\033[96m'  # Cyan/Blue for the player
    RAINBOW = '\033[95m'    # Purple/Vibrant for magic
    ENEMY = '\033[91m'      # Red for threats
    GREEN = '\033[92m'      # Green for life/grass
    YELLOW = '\033[93m'     # Yellow for energy/items
    BOLD = '\033[1m'
    RESET = '\033[0m'

# --- Game State ---
player_name = "Blue Hero"
health = 100
magic_aura = 50
inventory = []
current_scene = "BUNNIES_RAINBOWS"
vegetable_name = "CARROT" # Assuming your favorite vegetable is a carrot

# --- Utilities ---
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def scroll_text(text, delay=0.03):
    """Simulates text being typed."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def draw_status():
    """Renders the player status."""
    print(Color.BOLD + "=" * 60 + Color.RESET)
    print(f"{Color.BLUE_HERO}Player: {player_name}{Color.RESET} | Health: {Color.ENEMY}{health}%{Color.RESET} | Aura: {Color.RAINBOW}{magic_aura}{Color.RESET}")
    print(f"Inventory: {inventory}")
    print(Color.BOLD + "=" * 60 + Color.RESET)

def take_damage(amount):
    """Reduces health and checks for game over."""
    global health
    health -= amount
    if health <= 0:
        game_over()

def game_over():
    clear_screen()
    print(Color.BOLD + Color.ENEMY + "\n" * 5)
    print("{:^60}".format("JPW7'S EDICT PREVAILS. MISSION FAILED."))
    print("{:^60}".format("The machine logic has crushed the Royal Forces."))
    print("\n" * 5 + Color.RESET)
    sys.exit()

def victory():
    clear_screen()
    print(Color.BOLD + Color.RAINBOW + "\n" * 5)
    print("{:^60}".format("JPW7'S EARLY EDITS HAVE BEEN OVERLOADED!"))
    print("{:^60}".format("MAGIC RESTORED! LONG LIVE THE ROYAL FORCES!"))
    print("\n" * 5 + Color.RESET)
    sys.exit()

# --- Scenes ---

def scene_bunnies_rainbows():
    """Initial scene: Setting the magical baseline."""
    clear_screen()
    global magic_aura
    
    scroll_text(f"{Color.RAINBOW}You are the {Color.BOLD}{player_name}{Color.RESET}{Color.RAINBOW}, an agent of the Royal Forces of Tahkmahnelle.{Color.RESET}")
    scroll_text(f"The world still holds remnants of the old magic—a field of **Bunnies and Rainbows** that stabilizes your Aura.")
    
    print(f"\n{Color.RAINBOW}*Aura Restored: {magic_aura}*{Color.RESET}")
    
    magic_aura = 75 # Set the starting aura high
    
    scroll_text("\nYour first mission: Locate the secret coding clue from the **Youth in Asia** NPC.")
    
    input(f"\nPress {Color.BOLD}ENTER{Color.RESET} to proceed to the corrupted field...")
    global current_scene
    current_scene = "GRASS_BLUES"

def scene_grass_blues():
    """Encountering environmental corruption and a helpful item."""
    clear_screen()
    global magic_aura, current_scene
    
    draw_status()
    scroll_text(f"\nYou enter a valley tainted by **JPW7's** early coding. The magic is replaced by **Grass Blues**.")
    scroll_text(f"{Color.GREEN}The melancholic atmosphere drains your will and magic.{Color.RESET}")
    
    magic_loss = random.randint(10, 20)
    magic_aura -= magic_loss
    
    if magic_aura <= 0:
        scroll_text(f"{Color.ENEMY}The Grass Blues consume your magic. You are too weak to fight.{Color.RESET}")
        take_damage(50) # Heavy damage if aura is lost
        if health <= 0: return

    scroll_text(f"You find a strange artifact near a dead sentinel.")
    print("1) Investigate the artifact.")
    print("2) Hurry toward the city.")
    
    choice = input("\n> ").strip()
    
    if choice == '1':
        scroll_text(f"It's the {Color.YELLOW}**Od Duck**{Color.RESET}! A relic of pure randomness. It might be useful.")
        inventory.append("Od Duck")
        current_scene = "YOUTH_IN_ASIA_LOC"
    else:
        scroll_text("You hear a distant mechanical whirring. You press on.")
        current_scene = "YOUTH_IN_ASIA_LOC"

def scene_youth_in_asia_loc():
    """The vital NPC encounter."""
    clear_screen()
    global current_scene
    
    draw_status()
    scroll_text(f"You reach the district known as **Youth in Asia**. It's surprisingly intact, shielded by old magic.")
    scroll_text("You find the source of the protection: a young, cybernetically-linked prophet.")
    
    scroll_text("\nPROPHET: 'The solution to the Edict lies in the *Nonsensical Logic Stream* that powers the final lock. To solve it, you need a high-energy **Carrot** and you must defeat the **Blisterfist** guard.'")
    
    if "Od Duck" in inventory:
        scroll_text("PROPHET: 'Since you have the **Od Duck**, I will grant you one **Carrot** for power.'")
        inventory.append(f"{vegetable_name.upper()} Power Cell")
    else:
        scroll_text(f"PROPHET: 'Find a {vegetable_name.upper()} before you proceed. It's the only fuel source for the final mechanism.'")

    input("\nPress ENTER to face the Blisterfist drone...")
    current_scene = "BLISTERFIST_COMBAT"

def scene_blisterfist_combat():
    """Combat challenge and inventory check."""
    clear_screen()
    global current_scene, magic_aura
    
    draw_status()
    scroll_text(f"\n{Color.ENEMY}A massive, metallic drone, the **Blisterfist**, drops from the sky!{Color.RESET}")
    
    # Combat Mechanic based on Aura
    if magic_aura >= 50:
        scroll_text(f"You channel the **Bunnies and Rainbows** aura into a focused blast!")
        scroll_text(f"The **Blisterfist** is stunned, its heavy armor cracked.")
        magic_aura -= 25 # Cost of the attack
    else:
        scroll_text("Your low aura forces you into a physical struggle. The Blisterfist lands a direct hit!")
        take_damage(35)
        
    input("\nPress ENTER to continue the fight...")
    
    # Final Action
    if f"{vegetable_name.upper()} Power Cell" in inventory:
        scroll_text(f"You jam the {vegetable_name.upper()} Power Cell into the drone's exposed core.")
        scroll_text(f"{Color.YELLOW}The high-energy vegetable overloads the machine! **Blisterfist** neutralized!{Color.RESET}")
        inventory.remove(f"{vegetable_name.upper()} Power Cell")
        current_scene = "GIRAFFE_JUG"
    else:
        scroll_text(f"{Color.ENEMY}Without the power cell, the **Blisterfist** repairs itself and forces you to retreat.{Color.RESET}")
        take_damage(20)
        current_scene = "YOUTH_IN_ASIA_LOC"

def scene_giraffe_jug():
    """Final Puzzle and Victory."""
    clear_screen()
    draw_status()
    
    scroll_text(f"\n{Color.RAINBOW}You've reached **JPW7's** primary core, protected by a final, illogical lock.{Color.RESET}")
    scroll_text("The lock displays a riddle reflecting the early chaos of the Edict:")
    
    # The final, illogical puzzle
    print(f"{Color.BOLD}\n-- THE FINAL PUZZLE: THE GIRAFFE IN THE JUG FULL OF JELLY --{Color.RESET}")
    print("Riddle: If the Giraffe is larger than the Jug, and the Jelly is the constant of viscosity, how does one remove the Giraffe without disturbing the Jelly?")
    
    print("\n1) Melt the Jelly with a heat ray.")
    print("2) Use the **Od Duck's** randomizer function.")
    print("3) State: The premise is flawed; the Giraffe was never inside.")
    
    choice = input("\n> ").strip()
    
    if choice == '3':
        scroll_text(f"{Color.BLUE_HERO}You speak the true answer, exposing the flaw in **JPW7's** early cyber-logic.{Color.RESET}")
        scroll_text("The illogical truth overloads the core. The Edict begins to crumble!")
        victory()
    elif "Od Duck" in inventory and choice == '2':
        scroll_text(f"The **Od Duck** randomly generates the correct key, bypassing the logical flaw!")
        victory()
    else:
        scroll_text(f"{Color.ENEMY}The logic core locks down. **JPW7** laughs. You are trapped.{Color.RESET}")
        game_over()


# --- Main Game Loop ---
def start_game():
    clear_screen()
    scroll_text(Color.BOLD + Color.YELLOW + "{:^60}".format("LANDSOFAGES6: CYBERNETIC BUNNIES") + Color.RESET)
    scroll_text(Color.BOLD + "{:^60}".format(f"A Royal Forces Adventure") + Color.RESET)
    scroll_text(Color.BOLD + Color.BLUE + "{:^60}".format(f"The Early Years of JPW7") + Color.RESET)
    
    input("\nPress ENTER to begin as the Blue Hero...")
    
    global current_scene
    current_scene = "BUNNIES_RAINBOWS"
    
    while True:
        if current_scene == "BUNNIES_RAINBOWS":
            scene_bunnies_rainbows()
        elif current_scene == "GRASS_BLUES":
            scene_grass_blues()
        elif current_scene == "YOUTH_IN_ASIA_LOC":
            scene_youth_in_asia_loc()
        elif current_scene == "BLISTERFIST_COMBAT":
            scene_blisterfist_combat()
        elif current_scene == "GIRAFFE_JUG":
            scene_giraffe_jug()
        else:
            break
            
if __name__ == "__main__":
    start_game()
