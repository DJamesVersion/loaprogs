#!/bin/bash

# --- GLOBAL GAME VARIABLES ---
PLAYER_NAME=""
PLAYER_CLASS=""
HEALTH=100
POWER=50
HAS_BATOBWATCHAEH="false"

# --- HELPER FUNCTIONS ---

function game_over() {
    echo -e "\n====================================================="
    echo -e "           💀 THE ECHOES FADE... GAME OVER! 💀"
    echo -e "====================================================="
    echo "Your journey in Tahkmahnelle ends here."
    exit 0
}

function display_status() {
    echo -e "\n--- STATUS ---"
    echo "NAME: $PLAYER_NAME | CLASS: $PLAYER_CLASS"
    echo "HEALTH: $HEALTH | POWER: $POWER"
    echo "ARTIFACT: $( [ "$HAS_BATOBWATCHAEH" = "true" ] && echo 'B-atobwatchaeh (Aquired)' || echo 'None' )"
    echo "--------------"
}

function take_damage() {
    local damage=$1
    HEALTH=$((HEALTH - damage))
    echo "You take $damage damage."
    if (( HEALTH <= 0 )); then
        game_over
    fi
}

# --- SCENES (Key Plot Points) ---

# A - Ariatnah: Start
function scene_ariatnah() {
    clear
    echo "#####################################################"
    echo "## A: ARIATNAH - The Village of Whispering Echoes  ##"
    echo "#####################################################"
    echo "You wake in A-riatnah, a village untouched by the true history of Tahkmahnelle."
    echo "The J-ampejinne (Elder Council) call you, the Seeker, to choose a path."
    
    echo -e "\nWhich path do you choose?"
    echo "1) The Scholar (C-'illiatnah)"
    echo "2) The Fighter (F-'illianarre)"
    echo "3) The Rogue (I-llianarre)"
    echo "4) The Sage (Y-'uilliatachaeh)"
    read -p "Enter your choice (1-4): " class_choice

    case "$class_choice" in
        1) PLAYER_CLASS="C-illiatnah (Scholar)"; POWER=$((POWER + 20));;
        2) PLAYER_CLASS="F-illianarre (Fighter)"; HEALTH=$((HEALTH + 30));;
        3) PLAYER_CLASS="I-llianarre (Rogue)";;
        4) PLAYER_CLASS="Y-uilliatachaeh (Sage)"; POWER=$((POWER + 30));;
        *) echo "Invalid choice. The path of the Scholar is thrust upon you."; PLAYER_CLASS="C-illiatnah (Scholar)"; POWER=$((POWER + 20));;
    esac
    
    echo "The J-ampejinne nod. You are now the $PLAYER_CLASS."
    read -p "Press ENTER to continue to the D-iadowatchaeh..."
    scene_diadowatchaeh
}

# D - Diadowatchaeh: Choice
function scene_diadowatchaeh() {
    clear
    echo "#####################################################"
    echo "## D: DIADOWATCHAEH - The Shadowed Path            ##"
    echo "#####################################################"
    display_status
    echo "You stand at the edge of the D-iadowatchaeh, the dark forest."
    echo "Legend says the B-atobwatchaeh (Artifact) is hidden here, guarded by the N-ano (Shadow)."
    
    echo -e "\nWhat is your action?"
    echo "1) Search for the B-atobwatchaeh immediately (Risking N-ano's trap)."
    echo "2) Try to bypass the forest and seek the K-ajoinkenne (Mountain Peaks)."
    
    read -p "Enter your choice (1-2): " choice

    if [ "$choice" == "1" ]; then
        echo "A shadowy tendril, the Z-azoykenne (Corruption), lashes out!"
        take_damage 25
        echo "You fought it off and found a glimmering artifact!"
        HAS_BATOBWATCHAEH="true"
        echo "You have acquired the B-atobwatchaeh! (+15 HEALTH)"
        HEALTH=$((HEALTH + 15))
        read -p "Press ENTER to leave the dark forest..."
        scene_kajoinkenne
    elif [ "$choice" == "2" ]; then
        echo "You carefully skirt the D-iadowatchaeh, avoiding the Z-azoykenne."
        read -p "Press ENTER to begin the climb to K-ajoinkenne..."
        scene_kajoinkenne
    else
        echo "You hesitate and waste time. You take a minor injury from an X-iangxong."
        take_damage 5
        scene_diadowatchaeh # Loop back or force the next scene
    fi
}

# K - Kajoinkenne: Mountain Peaks
function scene_kajoinkenne() {
    clear
    echo "#####################################################"
    echo "## K: KAJOINKENNE - The Mountain Peaks             ##"
    echo "#####################################################"
    display_status
    echo "You reach the K-ajoinkenne. The winds carry the power of S-iataeh (Air)."
    echo "A solitary figure, the R-oykenne (King) is seen overseeing the construction of a fortress."
    echo "You must find the L-enemketobontette (Great Library) to learn about M-omaw (The Quest)."

    echo -e "\nYour path divides again."
    echo "1) Use the G-agoikenne (Portal) to bypass the R-oykenne's territory (Risky)."
    echo "2) Sneak through the construction to find the library (Need I-llianarre skills)."
    
    read -p "Enter your choice (1-2): " choice

    if [ "$choice" == "1" ]; then
        echo "You enter the G-agoikenne! The power drain is intense."
        take_damage 10
        scene_lenemketobontette
    elif [ "$choice" == "2" ]; then
        if [ "$PLAYER_CLASS" == "I-llianarre (Rogue)" ]; then
            echo "Your rogue skills let you slip past the guards with ease. A success!"
            scene_lenemketobontette
        else
            echo "You are caught by the guards! You must fight."
            take_damage 40
            echo "You barely escape and flee into the portal!"
            scene_lenemketobontette
        fi
    else
        echo "You rest for too long. A mountain monster strikes!"
        take_damage 10
        scene_kajoinkenne
    fi
}

# L - Lenemketobontette: The Library/End Game Setup
function scene_lenemketobontette() {
    clear
    echo "#####################################################"
    echo "## L: LENEMKETOBONTETTE - The Great Library        ##"
    echo "#####################################################"
    display_status
    echo "Within the L-enemketobontette, you discover the truth: M-omaw is not a deity, but the balanced state of Tahkmahnelle."
    echo "The R-oykenne is trying to seize the O-ichenne (Orb) to fully channel the Z-azoykenne (Corruption)."
    echo "You find the text describing the Q-uaristenne (Final Puzzle) and the power of U-illiatachaeh (Universal Key)."
    
    echo -e "\nYour final step is to solve the Q-uaristenne and confront the R-oykenne in the T-etnobautte (Final Trial)."
    read -p "Press ENTER to face the final challenge..."
    scene_tetnobautte
}

# T - Tetnobautte: Final Trial
function scene_tetnobautte() {
    clear
    echo "#####################################################"
    echo "## T: TETNOBAUTTE - The Final Trial                ##"
    echo "#####################################################"
    display_status
    echo "You stand before the R-oykenne, who holds the pulsing O-ichenne, ready to unleash the Z-azoykenne."
    
    # Q-uaristenne (Final Puzzle)
    echo -e "\nTHE Q-UARISTENNE: What is the source of $S-tihuu (Earth) and $S-iataeh (Air)?"
    read -p "Enter your answer (One Word): " final_answer
    
    if [ "$final_answer" == "Tahkmahnelle" ] || [ "$final_answer" == "T-ahkmahnelle" ] || [ "$final_answer" == "TETNOBAUTTE" ]; then
        echo "The Q-uaristenne is solved! The U-illiatachaeh (Universal Key) is revealed!"
        if [ "$HAS_BATOBWATCHAEH" == "true" ]; then
            echo "Using the B-atobwatchaeh, you channel the U-illiatachaeh into the O-ichenne, purifying it."
            echo -e "\n🏆 VICTORY! Tahkmahnelle is saved, and M-omaw is restored! 🏆"
        else
            echo "You solve the puzzle, but without the B-atobwatchaeh, you can only seal the Z-azoykenne away for a time."
            echo -e "\nACHIEVEMENT: TEMPORARY PEACE."
        fi
    else
        echo "The puzzle is wrong! The R-oykenne laughs and unleashes his power."
        take_damage 100 # Instant Game Over
    fi
    
    echo -e "\nThank you for playing LandsofAges."
    exit 0
}

# --- MAIN GAME EXECUTION ---

function start_game() {
    clear
    echo -e "====================================================="
    echo -e "      WELCOME TO LANDSOFAGES: A TAHKMAHNELLE EPIC"
    echo -e "====================================================="
    
    read -p "Enter your Seeker's name: " PLAYER_NAME
    
    if [ -z "$PLAYER_NAME" ]; then
        PLAYER_NAME="Unnamed Seeker"
    fi
    
    echo "Hello, $PLAYER_NAME. Your journey begins in A-riatnah (A)."
    read -p "Press ENTER to begin..."
    
    scene_ariatnah
}

# Run the game
start_game
