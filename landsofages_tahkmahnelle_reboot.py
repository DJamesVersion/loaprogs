# landsofages_tahkmahnelle_reboot.py
# Copyright LoA Corporation SLPOE (Reboot Edition)

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

# --- CORE GAME CLASS ---

class LandsofAgesGame:
    def __init__(self):
        self.player_name = "Blue Hero"
        self.health = 100
        self.power = 50
        self.turn = 1
        self.current_age = 1
        
        # State variables
        self.inventory = set()
        self.runes_found = 0
        self.fighter_strength = 0
        self.terraform_score = 0

    def clear_screen(self):
        """Clears the terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def game_over(self, reason="The saga ends in failure."):
        """Displays game over screen and exits."""
        self.clear_screen()
        print(Color.BOLD + Color.ENEMY + "\n" * 5)
        print("{:^70}".format("💀 MISSION FAILURE - TAHKMAHNELLE IS LOST 💀"))
        print(f"{:^70}".format(f"Cause: {reason}"))
        print("\n" * 5 + Color.RESET)
        sys.exit()

    def victory(self):
        """Displays victory screen and exits."""
        self.clear_screen()
        print(Color.BOLD + Color.HEALTH + "\n" * 5)
        print("{:^70}".format("👑 VICTORY! TAHKMAHNELLE'S EVERAFTER IS SECURE! 👑"))
        print(f"{:^70}".format(f"The saga was completed in {self.turn} turns."))
        print("\n" * 5 + Color.RESET)
        sys.exit()

    def display_status(self):
        """Renders the comprehensive game status."""
        print(Color.BOLD + "=" * 70 + Color.RESET)
        print(f"{Color.MAGIC}AGE: {self.current_age}/4 | TURN: {self.turn} | HERO: {self.player_name}{Color.RESET}")
        print(f"{Color.HEALTH}HEALTH:{Color.RESET} {self.health} | {Color.MAGIC}POWER:{Color.RESET} {self.power} | {Color.ITEM}INVENTORY:{Color.RESET} {', '.join(self.inventory) if self.inventory else 'None'}")
        
        # Age-specific status
        if self.current_age == 1:
            print(f"Goal Status: Runes: {self.runes_found}/5 | Has B-atobwatchaeh: {'Yes' if 'B-atobwatchaeh' in self.inventory else 'No'}")
        elif self.current_age == 2:
            print(f"Goal Status: JPW7 Chaos Level: {self.power} | Has Od Duck & Carrot: {'Yes' if 'Od Duck' in self.inventory and 'Carrot' in self.inventory else 'No'}")
        elif self.current_age == 3:
            threat = int(self.turn/5 * 10)
            print(f"Goal Status: F-'illianarre Strength: {self.fighter_strength} | X-iangxong Threat: {threat}%")
        elif self.current_age == 4:
            print(f"Goal Status: Terraform Score: {self.terraform_score}/100 | Ship Level: {self.power // 25}")
            
        print(Color.BOLD + "=" * 70 + Color.RESET)

    def take_damage(self, amount, hazard="Hazard"):
        """Reduces health and checks for game over."""
        self.health = max(0, self.health - amount)
        print(f"{Color.ENEMY}!! {hazard} !! Lost {amount} Health. ({self.health}){Color.RESET}")
        if self.health <= 0:
            self.game_over("Health depleted by constant threats.")

    def advance_turn(self):
        """Increments turn and applies passive age effects/checks."""
        self.turn += 1
        
        # Age III Catastrophe Check (Time limit)
        if self.current_age == 3 and self.turn > 15:
            self.game_over("The X-iangxong War Machine reached the capital due to mission delay.")
        
    # --- AGE I: THE GREAT SEARCH (LA1 & LA2) ---

    def age1_scene(self):
        print(Color.HEADER + "\n-- AGE I: THE GREAT SEARCH (A-riatnah) --" + Color.RESET)
        print("The **J-ampejinne** bid you begin your **Q-uest** to find the artifacts and stabilize the world.")
        
        choices = {}
        i = 1

        if 'B-atobwatchaeh' not in self.inventory:
            print(f"{i}) Search the **D-iadowatchaeh** for the **B-atobwatchaeh** (Costs 20 Power).")
            choices[str(i)] = 'ARTIFACT'
            i += 1
        
        if self.runes_found < 5:
            print(f"{i}) Seek an **Elder Rune** in the lands (Runes found: {self.runes_found}/5).")
            choices[str(i)] = 'RUNE'
            i += 1
        
        if 'B-atobwatchaeh' in self.inventory and self.runes_found == 5:
            print(f"{i}) COMPLETE Q-UEST: Advance to AGE II.")
            choices[str(i)] = 'ADVANCE'
            i += 1
        
        choice = input("\nEnter choice: ").strip().upper()

        if choice in choices:
            action = choices[choice]
            if action == 'ARTIFACT':
                if self.power >= 20:
                    self.inventory.add('B-atobwatchaeh')
                    self.power -= 20
                    print(f"{Color.ITEM}The **B-atobwatchaeh** is recovered! Power -20.{Color.RESET}")
                else:
                    self.take_damage(20, "D-iadowatchaeh Traps (No Power)")
            
            elif action == 'RUNE':
                self.runes_found += 1
                if random.random() < 0.3:
                    self.inventory.add('Z-ephyr')
                    print(f"{Color.ITEM}Rune secured! You also find a stabilizing **Z-ephyr**!{Color.RESET}")
                else:
                     print(f"{Color.MAGIC}An Elder Rune is secured! The **E-choes** guide you.{Color.RESET}")
                
                self.take_damage(5, "F-licker residual damage")
            
            elif action == 'ADVANCE':
                print(f"{Color.HEADER}AGE I Complete! Magic stabilized. Now for the chaos...{Color.RESET}")
                self.current_age = 2
                self.inventory.discard('Z-ephyr') # Z-ephyr's purpose is fulfilled
                return 

        self.advance_turn()

    # --- AGE II: THE EDICT OF CHAOS (LA6) ---

    def age2_scene(self):
        print(Color.HEADER + "\n-- AGE II: THE EDICT OF CHAOS (JPW7) --" + Color.RESET)
        print("The world is covered in an artificial **Bunnies and Rainbows** aura. You must find the **Giraffe in the Jug** clue.")
        
        choices = {}
        i = 1
        
        if 'Od Duck' not in self.inventory:
            print(f"{i}) Search the **Grass Blues** field for the chaotic **Od Duck** relic.")
            choices[str(i)] = 'DUCK'
            i += 1
        if 'Carrot' not in self.inventory:
            print(f"{i}) Seek the **Youth in Asia** NPC for the power source (**Carrot**).")
            choices[str(i)] = 'CARROT'
            i += 1
        
        print(f"{i}) Confront the **Blisterfist** drone (Power Check).")
        choices[str(i)] = 'FIST'
        i += 1
        
        if 'Od Duck' in self.inventory and 'Carrot' in self.inventory:
            print(f"{i}) Final Action: Attempt the **Giraffe in the Jug** puzzle to neutralize JPW7.")
            choices[str(i)] = 'ADVANCE'
            i += 1
            
        choice = input("\nEnter choice: ").strip().upper()

        if choice in choices:
            action = choices[choice]
            if action == 'DUCK':
                self.inventory.add('Od Duck')
                print(f"{Color.ITEM}The chaotic **Od Duck** is found!{Color.RESET}")
            elif action == 'CARROT':
                self.inventory.add('Carrot')
                print(f"{Color.ITEM}The **Carrot** power source is secured!{Color.RESET}")
            elif action == 'FIST':
                if self.power > 60:
                    self.power += 10
                    print(f"{Color.HEALTH}You overload the **Blisterfist**! Power +10.{Color.RESET}")
                else:
                    self.take_damage(35, "Blisterfist Strike")
            elif action == 'ADVANCE':
                print(f"{Color.HEADER}AGE II Complete! JPW7's cybernetic logic is neutralized by absurdity.{Color.RESET}")
                self.current_age = 3
                self.fighter_strength = 10 
                self.inventory.discard('Od Duck') 
                self.inventory.discard('Carrot')
                self.turn = 10 # Reset turn count for Age III threat tracker
                return 

        self.advance_turn()
        
    # --- AGE III: THE FINAL EDICT (LA3 & LA4) ---

    def age3_scene(self):
        threat = int(self.turn/5 * 10)
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
        
        if self.fighter_strength >= 100:
            print(f"{i}) Final Action: Infiltrate the **N-exus** to **U-nravel** the **W-rath**.")
            choices[str(i)] = 'ADVANCE'
            i += 1
            
        choice = input("\nEnter choice: ").strip().upper()

        if choice in choices:
            action = choices[choice]
            if action == 'GATHER':
                self.power += 20
                print(f"{Color.ITEM}S-tihuu and S-iataeh gathered. Power +20.{Color.RESET}")
            
            elif action == 'RECRUIT':
                if self.power >= 10:
                    self.power -= 10
                    self.fighter_strength += 25
                    print(f"{Color.HEALTH}**F-'illianarre** unit deployed! Strength +25.{Color.RESET}")
                else:
                    print(f"{Color.ENEMY}Insufficient Power to recruit.{Color.RESET}")

            elif action == 'ADVANCE':
                if 'B-atobwatchaeh' in self.inventory:
                    print(f"{Color.HEADER}AGE III Complete! The **W-rath** is **U-nravelled** at the **N-exus**.{Color.RESET}")
                    self.current_age = 4
                    self.turn = 1 # Reset turn count for new age
                    self.power = 75 # Starting power/resources for Age IV
                    return
                else:
                    self.take_damage(50, "W-rath Explosion (No B-atobwatchaeh)")
                    print(f"{Color.ENEMY}Failed to U-nravel without the **B-atobwatchaeh**.{Color.RESET}")

        self.advance_turn()

    # --- AGE IV: COLONIZATION (LA5 & RFA2LA) ---

    def age4_scene(self):
        ship_level = self.power // 25
        print(Color.HEADER + "\n-- AGE IV: COLONIZATION (TAHKMAHNELLE45) --" + Color.RESET)
        print(f"Goal: Establish permanent colony on **TAHKMAHNELLE45**. Ship Level: {ship_level}.")
        
        if self.terraform_score >= 100:
            self.victory()
        
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
            
        choice = input("\nEnter choice: ").strip().upper()

        if choice in choices:
            action = choices[choice]
            if action == 'GATHER':
                self.power += 10 + (ship_level * 5)
                print(f"{Color.HEALTH}Colony Resources gathered! Power +{10 + (ship_level * 5)}.{Color.RESET}")
            
            elif action == 'BUILD':
                cost = 20
                gain = 10 + ship_level
                if self.power >= cost:
                    self.power -= cost
                    self.terraform_score += gain
                    print(f"{Color.MAGIC}Terraforming successful! Score +{gain}. ({self.terraform_score}/100){Color.RESET}")
                else:
                    print(f"{Color.ENEMY}Need 20 Power to terraform.{Color.RESET}")

            elif action == 'UPGRADE':
                cost = 50
                if self.power >= cost:
                    self.power += 25  # Increase capacity after paying cost
                    self.power -= cost
                    print(f"{Color.ITEM}Ship upgraded! New Level: {self.power // 25}.{Color.RESET}")
                else:
                    print(f"{Color.ENEMY}Need 50 Power to upgrade the ship.{Color.RESET}")
        
        self.advance_turn()


    # --- MAIN GAME LOOP ---

    def run(self):
        self.clear_screen()
        print(Color.BOLD + Color.HEADER + "=" * 70 + Color.RESET)
        print(Color.BOLD + Color.HEADER + "{:^70}".format("LANDSOFAGES-TAHKMAHNELLE-REBOOT") + Color.RESET)
        print(Color.BOLD + Color.MAGIC + "{:^70}".format("Copyright LoA Corporation SLPOE (Reboot Edition)") + Color.RESET)
        print(Color.BOLD + Color.HEADER + "=" * 70 + Color.RESET)
        
        self.player_name = input("Enter your Hero's name: ").strip() or "Blue Hero"
        
        print(f"\nWelcome, {self.player_name}. Your four-stage journey to secure Tahkmahnelle begins now.")
        input("Press ENTER to begin...")
        
        while True:
            self.clear_screen()
            self.display_status()
            
            if self.current_age == 1:
                self.age1_scene()
            elif self.current_age == 2:
                self.age2_scene()
            elif self.current_age == 3:
                self.age3_scene()
            elif self.current_age == 4:
                self.age4_scene()
            else:
                break

# --- Execution ---

if __name__ == "__main__":
    game = LandsofAgesGame()
    game.run()

