#!/bin/bash

# landsofages_tahkmahnelle_reboot.sh
# Copyright LoA Corporation SLPOE (Reboot Edition)

# --- ANSI COLOR CODES (Simulated for Bash) ---
C_HEADER='\033[95m'
C_MAGIC='\033[94m'      # Blue
C_HEALTH='\033[92m'     # Green
C_ENEMY='\033[91m'      # Red
C_ITEM='\033[93m'       # Yellow
C_BOLD='\033[1m'
C_RESET='\033[0m'

# --- GLOBAL GAME STATE ---
PLAYER_NAME="Hero"
HEALTH=100
POWER=50 # Universal resource for magic, fighters, and colony funds
TURN=1
CURRENT_AGE=1

# State variables (Keywords represented by boolean flags or counters)
RUNES_FOUND=0
FIGHTER_STRENGTH=0
TERRAFORM_SCORE=0

# Keyword Flags (0=False, 1=True)
HAS_BATOBWATCHAEH=0
HAS_ODDUCK=0
HAS_CARROT=0

# --- UTILITIES ---

function clear_screen() {
    clear
}

function game_over() {
    clear_screen
    echo -e "${C_BOLD}${C_ENEMY}\n\n\n\n\n"
    echo -e "${C_ENEMY}{:^70}${C_RESET}" | sed "s/{\:^70}/💀 MISSION FAILURE - TAHKMAHNELLE IS LOST 💀/g"
    echo -e "${C_ENEMY}Cause: $1${C_RESET}"
    echo -e "\n\n\n\n\n${C_RESET}"
    exit 0
}

function victory() {
    clear_screen
    echo -e "${C_BOLD}${C_HEALTH}\n\n\n\n\n"
    echo -e "${C_HEALTH}{:^70}${C_RESET}" | sed "s/{\:^70}/👑 VICTORY! TAHKMAHNELLE'S EVERAFTER IS SECURE! 👑/g"
    echo -e "${C_HEALTH}The saga was completed in $TURN turns.${C_RESET}"
    echo -e "\n\n\n\n\n${C_RESET}"
    exit 0
}

function display_status() {
    local inventory_list=""
    (( HAS_BATOBWATCHAEH == 1 )) && inventory_list+="B-atobwatchaeh, "
    (( HAS_ODDUCK == 1 )) && inventory_list+="Od Duck, "
    (( HAS_CARROT == 1 )) && inventory_list+="Carrot, "
    inventory_list="${inventory_list%, }"

    echo -e "${C_BOLD}======================================================================${C_RESET}"
    echo -e "${C_MAGIC}AGE: $CURRENT_AGE/4 | TURN: $TURN | HERO: $PLAYER_NAME${C_RESET}"
    echo -e "${C_HEALTH}HEALTH:${C_RESET} $HEALTH | ${C_MAGIC}POWER:${C_RESET} $POWER | ${C_ITEM}INVENTORY:${C_RESET} $inventory_list"
    
    # Age-specific status
    if (( CURRENT_AGE == 1 )); then
        local has_artifact="No"
        (( HAS_BATOBWATCHAEH == 1 )) && has_artifact="Yes"
        echo "Goal Status: Runes: $RUNES_FOUND/5 | Has B-atobwatchaeh: $has_artifact"
    elif (( CURRENT_AGE == 2 )); then
        local items_found="No"
        (( HAS_ODDUCK == 1 && HAS_CARROT == 1 )) && items_found="Yes"
        echo "Goal Status: Chaos Level: $POWER | Has Od Duck & Carrot: $items_found"
    elif (( CURRENT_AGE == 3 )); then
        local threat=$(( TURN / 5 * 10 ))
        echo "Goal Status: F-'illianarre Strength: $FIGHTER_STRENGTH | X-iangxong Threat: ${threat}%"
    elif (( CURRENT_AGE == 4 )); then
        local ship_level=$(( POWER / 25 ))
        echo "Goal Status: Terraform Score: $TERRAFORM_SCORE/100 | Ship Level: $ship_level"
    fi
    echo -e "${C_BOLD}======================================================================${C_RESET}"
}

function take_damage() {
    local amount=$1
    local hazard=$2
    HEALTH=$((HEALTH - amount))
    echo -e "${C_ENEMY}!! $hazard !! Lost $amount Health. ($HEALTH)${C_RESET}"
    if (( HEALTH <= 0 )); then
        game_over "Health depleted by constant threats."
    fi
}

function advance_turn() {
    TURN=$((TURN + 1))
    
    # Age III Catastrophe Check (Time limit)
    if (( CURRENT_AGE == 3 )) && (( TURN > 15 )); then
        game_over "The X-iangxong War Machine reached the capital due to mission delay."
    fi
}

# --- AGE I: THE GREAT SEARCH (LA1 & LA2) ---

function age1_scene() {
    echo -e "${C_HEADER}\n-- AGE I: THE GREAT SEARCH (A-riatnah) --${C_RESET}"
    echo "The **J-ampejinne** bid you begin your **Q-uest** to find the artifacts and stabilize the world."
    
    local choice
    
    echo "1) Search the D-iadowatchaeh for the **B-atobwatchaeh** (Costs 20 Power)."
    echo "2) Seek an **Elder Rune** in the lands (Runes found: $RUNES_FOUND/5)."
    
    if (( HAS_BATOBWATCHAEH == 1 )) && (( RUNES_FOUND == 5 )); then
        echo "3) COMPLETE Q-UEST: Advance to AGE II."
    fi
    
    read -p "Enter choice: " choice

    case $choice in
        1)
            if (( HAS_BATOBWATCHAEH == 0 )); then
                if (( POWER >= 20 )); then
                    HAS_BATOBWATCHAEH=1
                    POWER=$((POWER - 20))
                    echo -e "${C_ITEM}The **B-atobwatchaeh** is recovered! Power -20.${C_RESET}"
                else
                    take_damage 20 "D-iadowatchaeh Traps (No Power)"
                fi
            else
                echo "Artifact already secured."
            fi
            ;;
        2)
            if (( RUNES_FOUND < 5 )); then
                RUNES_FOUND=$((RUNES_FOUND + 1))
                if (( RANDOM % 3 == 0 )); then
                    # Simulate finding Z-ephyr
                    echo -e "${C_ITEM}Rune secured! You also find a stabilizing **Z-ephyr**!${C_RESET}"
                else
                     echo -e "${C_MAGIC}An Elder Rune is secured! The **E-choes** guide you.${C_RESET}"
                fi
                take_damage 5 "F-licker residual damage"
            else
                echo "All Runes found."
            fi
            ;;
        3)
            if (( HAS_BATOBWATCHAEH == 1 )) && (( RUNES_FOUND == 5 )); then
                echo -e "${C_HEADER}AGE I Complete! Magic stabilized. Now for the chaos...${C_RESET}"
                CURRENT_AGE=2
                # Reset turn count for new age
                TURN=1
                # The B-atobwatchaeh is needed later, keep it.
                return 
            else
                echo "Cannot advance yet. Complete the objectives."
            fi
            ;;
        *)
            echo "Invalid choice. Time is lost."
            ;;
    esac
    advance_turn
}

# --- AGE II: THE EDICT OF CHAOS (LA6) ---

function age2_scene() {
    echo -e "${C_HEADER}\n-- AGE II: THE EDICT OF CHAOS (JPW7) --${C_RESET}"
    echo "The world is covered in an artificial **Bunnies and Rainbows** aura. Find the **Giraffe in the Jug** clue."
    
    local choice
    
    echo "1) Search for the chaotic **Od Duck** relic."
    echo "2) Seek the **Youth in Asia** NPC for the power source (**Carrot**)."
    echo "3) Confront the **Blisterfist** drone (Power Check)."
    
    if (( HAS_ODDUCK == 1 )) && (( HAS_CARROT == 1 )); then
        echo "4) Final Action: Attempt the **Giraffe in the Jug** puzzle."
    fi
        
    read -p "Enter choice: " choice

    case $choice in
        1)
            if (( HAS_ODDUCK == 0 )); then
                HAS_ODDUCK=1
                echo -e "${C_ITEM}The chaotic **Od Duck** is found!${C_RESET}"
            else
                echo "You already have the Od Duck."
            fi
            ;;
        2)
            if (( HAS_CARROT == 0 )); then
                HAS_CARROT=1
                echo -e "${C_ITEM}The **Carrot** power source is secured!${C_RESET}"
            else
                echo "You already have the Carrot."
            fi
            ;;
        3)
            if (( POWER > 60 )); then
                POWER=$((POWER + 10))
                echo -e "${C_HEALTH}You overload the **Blisterfist**! Power +10.${C_RESET}"
            else
                take_damage 35 "Blisterfist Strike"
            fi
            ;;
        4)
            if (( HAS_ODDUCK == 1 )) && (( HAS_CARROT == 1 )); then
                echo -e "${C_HEADER}AGE II Complete! JPW7's cybernetic logic is neutralized by absurdity.${C_RESET}"
                CURRENT_AGE=3
                FIGHTER_STRENGTH=10
                TURN=10 # Set initial turn for Age III threat tracker
                HAS_ODDUCK=0 # Items served their purpose
                HAS_CARROT=0
                return
            else
                echo "Need both Od Duck and Carrot to solve the puzzle."
            fi
            ;;
        *)
            echo "Invalid choice. Time is lost."
            ;;
    esac
    advance_turn
}
        
# --- AGE III: THE FINAL EDICT (LA3 & LA4) ---

function age3_scene() {
    local threat=$(( TURN / 5 * 10 ))
    echo -e "${C_HEADER}\n-- AGE III: THE FINAL EDICT (R-oykenne War) --${C_RESET}"
    echo "The **R-oykenne's** **X-iangxong** threat level is at ${threat}%. You need 100 Fighters for the final push."
    
    local choice

    echo "1) Gather **S-tihuu** (Materials) and **S-iataeh** (Magic) (Power +20)."
    echo "2) Recruit **F-'illianarre** (Fighters) (Cost: 10 Power, Strength +25)."
    
    if (( FIGHTER_STRENGTH >= 100 )); then
        echo "3) Final Action: Infiltrate the **N-exus** to **U-nravel** the **W-rath**."
    fi
        
    read -p "Enter choice: " choice

    case $choice in
        1)
            POWER=$((POWER + 20))
            echo -e "${C_ITEM}S-tihuu and S-iataeh gathered. Power +20.${C_RESET}"
            ;;
        2)
            if (( POWER >= 10 )); then
                POWER=$((POWER - 10))
                FIGHTER_STRENGTH=$((FIGHTER_STRENGTH + 25))
                echo -e "${C_HEALTH}**F-'illianarre** unit deployed! Strength +25.${C_RESET}"
            else
                echo -e "${C_ENEMY}Insufficient Power to recruit.${C_RESET}"
            fi
            ;;
        3)
            if (( FIGHTER_STRENGTH >= 100 )); then
                if (( HAS_BATOBWATCHAEH == 1 )); then
                    echo -e "${C_HEADER}AGE III Complete! The **W-rath** is **U-nravelled** at the **N-exus**.${C_RESET}"
                    CURRENT_AGE=4
                    TURN=1
                    POWER=75 # Starting power/resources for Age IV
                    return
                else
                    take_damage 50 "W-rath Explosion (No B-atobwatchaeh)"
                    echo -e "${C_ENEMY}Failed to U-nravel without the **B-atobwatchaeh**!${C_RESET}"
                fi
            else
                echo "Not enough F-'illianarre to cover your infiltration!"
            fi
            ;;
        *)
            echo "Invalid choice. Wasting critical time."
            ;;
    esac
    advance_turn
}

# --- AGE IV: COLONIZATION (LA5 & RFA2LA) ---

function age4_scene() {
    local ship_level=$(( POWER / 25 ))
    echo -e "${C_HEADER}\n-- AGE IV: COLONIZATION (TAHKMAHNELLE45) --${C_RESET}"
    echo "Goal: Establish permanent colony on **TAHKMAHNELLE45**. Ship Level: $ship_level."
    
    if (( TERRAFORM_SCORE >= 100 )); then
        victory
    fi
    
    local choice

    echo "1) Gather **Colony Resources** (Power +$(( 10 + ship_level * 5 )))."
    echo "2) Build/Terraform Colony (Cost: 20 Power, Gain: $(( 10 + ship_level )) Score)."
    echo "3) Upgrade Ship Capacity (Costs 50 Power, gives +25 Power capacity)."
        
    read -p "Enter choice: " choice

    case $choice in
        1)
            POWER_GAIN=$(( 10 + ship_level * 5 ))
            POWER=$((POWER + POWER_GAIN))
            echo -e "${C_HEALTH}Colony Resources gathered! Power +$POWER_GAIN.${C_RESET}"
            ;;
        2)
            COST=20
            GAIN=$(( 10 + ship_level ))
            if (( POWER >= COST )); then
                POWER=$((POWER - COST))
                TERRAFORM_SCORE=$((TERRAFORM_SCORE + GAIN))
                echo -e "${C_MAGIC}Terraforming successful! Score +$GAIN. ($TERRAFORM_SCORE/100)${C_RESET}"
            else
                echo -e "${C_ENEMY}Need 20 Power to terraform.${C_RESET}"
            fi
            ;;
        3)
            COST=50
            if (( POWER >= COST )); then
                POWER=$((POWER + 25)) # Capacity increase
                POWER=$((POWER - COST))
                echo -e "${C_ITEM}Ship upgraded! New Level: $(( POWER / 25 )).${C_RESET}"
            else
                echo -e "${C_ENEMY}Need 50 Power to upgrade the ship.${C_RESET}"
            fi
            ;;
        *)
            echo "Invalid choice. Wasting valuable time."
            ;;
    esac
    advance_turn
}

# --- MAIN GAME EXECUTION ---

function run_game() {
    clear_screen
    echo -e "${C_BOLD}${C_HEADER}======================================================================${C_RESET}"
    echo -e "${C_BOLD}${C_HEADER}{:^70}${C_RESET}" | sed "s/{\:^70}/LANDSOFAGES-TAHKMAHNELLE-REBOOT/g"
    echo -e "${C_BOLD}${C_MAGIC}{:^70}${C_RESET}" | sed "s/{\:^70}/Copyright LoA Corporation SLPOE (Reboot Edition)/g"
    echo -e "${C_BOLD}${C_HEADER}======================================================================${C_RESET}"
    
    read -p "Enter your Hero's name: " INPUT_NAME
    if [ -n "$INPUT_NAME" ]; then PLAYER_NAME="$INPUT_NAME"; fi
    
    echo "The four-stage journey to secure Tahkmahnelle begins now."
    read -p "Press ENTER to begin..."
    
    while true; do
        clear_screen
        display_status
        
        case $CURRENT_AGE in
            1) age1_scene ;;
            2) age2_scene ;;
            3) age3_scene ;;
            4) age4_scene ;;
            *) break ;;
        esac
    done
}

# Execute the game
run_game

