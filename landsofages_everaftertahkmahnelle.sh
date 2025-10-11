#!/bin/bash

# --- GLOBAL GAME STATE ---
PLAYER_NAME="Hero"
HEALTH=100
POWER=50
TURN=1
CURRENT_AGE=1

# Age-specific status
HAS_BATOBWATCHAEH="false"
RUNES_FOUND=0
JPW7_TIME_LEFT=100  # Used for the timer in Age 2 and enemy progress in Age 3
RESOURCES=0         # Used as Fighters in Age 3 and Colony Resources in Age 4
TERRAFORM_SCORE=0   # Goal for Age 4

# --- UTILITIES ---

function clear_screen() {
    clear
}

function game_over() {
    clear_screen
    echo -e "\n=========================================================================="
    echo -e "                 💀 TAHKMAHNELLE'S EVERAFTER IS LOST! 💀"
    echo -e "=========================================================================="
    exit 0
}

function victory() {
    clear_screen
    echo -e "\n=========================================================================="
    echo -e "          👑 THE EVERAFTER IS WON! TAHKMAHNELLE'S LEGACY ENDURES! 👑"
    echo -e "=========================================================================="
    exit 0
}

function display_status() {
    echo -e "\n=========================================================================="
    echo "AGE: $CURRENT_AGE/4 | TURN: $TURN | HERO: $PLAYER_NAME"
    echo "HEALTH: $HEALTH | POWER: $POWER | RESOURCES (Fighters/Colony): $RESOURCES"
    
    case $CURRENT_AGE in
        1) echo "Age I: Runes: $RUNES_FOUND/5 | B-atobwatchaeh: $( [ "$HAS_BATOBWATCHAEH" = "true" ] && echo 'Yes' || echo 'No' )" ;;
        2) echo "Age II: JPW7 Chaos Timer: $JPW7_TIME_LEFT turns left." ;;
        3) echo "Age III: X-iangxong Progress: $((100 - JPW7_TIME_LEFT))% (Goal: 100 Fighters)" ;;
        4) echo "Age IV: Terraform Score: $TERRAFORM_SCORE/100" ;;
    esac
    echo "=========================================================================="
}

function take_damage() {
    local amount=$1
    HEALTH=$((HEALTH - amount))
    echo "!! HAZARD !! Lost $amount Health. ($HEALTH)"
    if (( HEALTH <= 0 )); then
        game_over
    fi
}

function advance_turn() {
    local progress_cost=1
    TURN=$((TURN + 1))

    case $CURRENT_AGE in
        2)
            # Age II: JPW7 Timer reduces
            JPW7_TIME_LEFT=$((JPW7_TIME_LEFT - 10))
            if (( JPW7_TIME_LEFT <= 0 )); then
                game_over
            fi
            ;;
        3)
            # Age III: Enemy Progress increases (JPW7_TIME_LEFT is inversely related)
            JPW7_TIME_LEFT=$((JPW7_TIME_LEFT - 10))
            if (( 100 - JPW7_TIME_LEFT >= 100 )); then
                 game_over
            fi
            ;;
    esac
}

# --- AGE I: THE GREAT SEARCH (LA1 & LA2) ---

function age1_scene() {
    echo -e "\n-- AGE I: THE GREAT SEARCH (A-riatnah) --"
    
    if [ "$HAS_BATOBWATCHAEH" = "false" ]; then
        echo "1) Seek the B-atobwatchaeh (Artifact)."
    fi
    
    if (( RUNES_FOUND < 5 )); then
        echo "2) Seek an Elder Rune (Runes found: $RUNES_FOUND/5)."
    fi
    
    if [ "$HAS_BATOBWATCHAEH" = "true" ] && (( RUNES_FOUND == 5 )); then
        echo "3) Complete the Great Search and advance to AGE II."
    fi
    
    read -p "Enter action: " choice
    
    case $choice in
        1)
            if [ "$HAS_BATOBWATCHAEH" = "false" ]; then
                HAS_BATOBWATCHAEH="true"
                POWER=$((POWER - 20))
                echo "Artifact recovered! B-atobwatchaeh secured."
            else
                echo "Already have the artifact."
            fi
            ;;
        2)
            if (( RUNES_FOUND < 5 )); then
                RUNES_FOUND=$((RUNES_FOUND + 1))
                echo "An Elder Rune is secured! The E-choes guide you."
                take_damage 5
            else
                echo "All Runes found."
            fi
            ;;
        3)
            if [ "$HAS_BATOBWATCHAEH" = "true" ] && (( RUNES_FOUND == 5 )); then
                echo "AGE I Complete! The world is magically stabilized."
                CURRENT_AGE=2
                JPW7_TIME_LEFT=100 # Reset timer for new age
            else
                echo "Conditions not met to advance."
            fi
            ;;
        *)
            echo "Invalid choice. Wasting time."
            ;;
    esac
    advance_turn
}

# --- AGE II: THE EDICT OF CHAOS (LA6) ---

function age2_scene() {
    echo -e "\n-- AGE II: THE EDICT OF CHAOS (JPW7) --"
    echo "Threat: JPW7's cybernetic rule. Timer: $JPW7_TIME_LEFT months."
    
    echo "1) Search for the **Od Duck** relic (Clue to the Giraffe in the Jug)."
    echo "2) Boost **POWER** (Preparing for Blisterfist)."
    
    if (( JPW7_TIME_LEFT < 50 )); then
        echo "3) Attempt final **Giraffe in the Jug** puzzle to overload JPW7."
    fi
    
    read -p "Enter action: " choice
    
    case $choice in
        1)
            if [[ ! " ${INVENTORY[@]} " =~ " Od Duck " ]]; then
                INVENTORY+=("Od Duck")
                echo "The chaotic Od Duck is found! Now seek the Carrot."
            else
                echo "You already have this relic."
            fi
            ;;
        2)
            POWER=$((POWER + 20))
            echo "Power boosted! Ready to face the Blisterfist."
            ;;
        3)
            if (( JPW7_TIME_LEFT < 50 )); then
                echo "AGE II Complete! JPW7's early edicts are neutralized."
                CURRENT_AGE=3
                JPW7_TIME_LEFT=100 # Reset progress for Age III
            else
                echo "Not enough data yet. Need to search more."
                take_damage 15
            fi
            ;;
        *)
            echo "Invalid choice. The Blisterfist drone notices you."
            take_damage 10
            ;;
    esac
    advance_turn 
}

# --- AGE III: THE FINAL EDICT (LA3 & LA4) ---

function age3_scene() {
    echo -e "\n-- AGE III: THE FINAL EDICT (R-oykenne War) --"
    local fighter_strength=$RESOURCES
    echo "Fighters (F-'illianarre): $fighter_strength. Target: 100"
    
    echo "1) Gather **S-tihuu** (Materials) and **S-iataeh** (Magic)."
    echo "2) Recruit **F-'illianarre** (Fighters) (Cost: 30 Resources)."
    
    if (( fighter_strength >= 100 )); then
        echo "3) Infiltrate the **N-exus** to **U-nravel** the **W-rath**."
    fi
    
    read -p "Enter action: " choice

    case $choice in
        1)
            RESOURCES=$((RESOURCES + 40))
            POWER=$((POWER + 10))
            echo "S-tihuu and S-iataeh gathered. Resources: $RESOURCES."
            ;;
        2)
            if (( RESOURCES >= 30 )); then
                RESOURCES=$((RESOURCES - 30))
                RESOURCES=$((RESOURCES + 20)) # +20 Fighter strength (stored in RESOURCES)
                echo "F-'illianarre unit deployed! Strength: $RESOURCES."
            else
                echo "Insufficient resources to recruit."
            fi
            ;;
        3)
            if (( fighter_strength >= 100 )); then
                if [ "$HAS_BATOBWATCHAEH" = "true" ]; then
                    echo "AGE III Complete! R-oykenne's final threat neutralized."
                    CURRENT_AGE=4
                    RESOURCES=150 # Starting resources for colony
                    POWER=10    # Starting ship level
                else
                    take_damage 50
                    echo "Failed to U-nravel without the B-atobwatchaeh! Massive backlash."
                fi
            else
                echo "Not enough F-'illianarre to cover your infiltration!"
            fi
            ;;
        *)
            echo "Invalid choice. Wasting time while the X-iangxong advances."
            ;;
    esac
    advance_turn
}

# --- AGE IV: COLONIZATION (LA5 & RFA2LA) ---

function age4_scene() {
    echo -e "\n-- AGE IV: COLONIZATION (TAHKMAHNELLE45) --"
    echo "Terraform Score: $TERRAFORM_SCORE/100. Resources: $RESOURCES."
    
    if (( TERRAFORM_SCORE >= 100 )); then
        victory
    fi

    echo "1) Gather **Colony Resources**."
    echo "2) Build/Terraform Colony (Cost: 50 Resources)."
    
    read -p "Enter action: " choice

    case $choice in
        1)
            RESOURCES=$((RESOURCES + 30))
            echo "Resources gathered. Current: $RESOURCES."
            ;;
        2)
            if (( RESOURCES >= 50 )); then
                RESOURCES=$((RESOURCES - 50))
                TERRAFORM_SCORE=$((TERRAFORM_SCORE + 20))
                echo "Terraforming successful! Score: $TERRAFORM_SCORE/100."
            else
                echo "Need 50 resources to terraform."
            fi
            ;;
        *)
            echo "Invalid choice."
            ;;
    esac
    advance_turn
}

# --- MAIN GAME EXECUTION ---

function start_game() {
    clear_screen
    echo -e "=========================================================================="
    echo -e "              WELCOME TO LANDSOFAGES: EVERAFTERTAHKMAHNELLE"
    echo -e "=========================================================================="
    
    read -p "Enter your Hero's name: " PLAYER_NAME
    if [ -z "$PLAYER_NAME" ]; then PLAYER_NAME="Blue Hero"; fi
    
    echo "The Saga begins in Age I: The Great Search."
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
start_game

