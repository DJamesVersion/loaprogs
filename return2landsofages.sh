#!/bin/bash

# --- GLOBAL GAME VARIABLES ---
PLAYER_NAME=""
PLAYER_CLASS=""
HEALTH=120
POWER=60
# Sequel Mechanic: Tracking the Elder Runes
RUNES_FOUND=0
HAS_CHRONOS="false" # C-hronos artifact
HAS_MANTLE="false"  # M-antle protection

# --- HELPER FUNCTIONS (Same as first game) ---

function game_over() {
    echo -e "\n====================================================="
    echo -e "           💀 THE SEQUEL FADES... GAME OVER! 💀"
    echo -e "====================================================="
    echo "Your quest to stabilize Tahkmahnelle has failed."
    exit 0
}

function display_status() {
    echo -e "\n--- STATUS ---"
    echo "NAME: $PLAYER_NAME | CLASS: $PLAYER_CLASS"
    echo "HEALTH: $HEALTH | POWER: $POWER"
    echo "RUNES AQUIRED: $RUNES_FOUND / 5"
    echo "ARTIFACTS: C-hronos ($HAS_CHRONOS) | M-antle ($HAS_MANTLE)"
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

function add_rune() {
    RUNES_FOUND=$((RUNES_FOUND + 1))
    echo -e "\n*** ELDER RUNE ACQUIRED! ($RUNES_FOUND/5) ***"
}

# --- SCENES (Key Plot Points) ---

# A - Awakening (The Start)
function scene_awakening() {
    clear
    echo "#####################################################"
    echo "## A: A-WAKENING - The Sacred Ground               ##"
    echo "#####################################################"
    echo "The world is stable, but magic is a F-licker. You, the Seeker, must complete the Q-uest (Q)."
    
    # Player data is imported/remembered
    read -p "Enter your Seeker's name (or the original): " PLAYER_NAME
    read -p "Enter your original Class (Scholar/Fighter/Rogue/Sage): " input_class
    PLAYER_CLASS="$input_class (Veteran)"
    
    echo "The E-choes of the ancients speak to you, pointing you toward the D-eluge (D)."
    
    read -p "Press ENTER to begin the J-ourney (J)..."
    scene_deluge
}

# D - Deluge (Rune 1)
function scene_deluge() {
    clear
    echo "#####################################################"
    echo "## D: D-ELUGE - The Flooded Coast                 ##"
    echo "#####################################################"
    display_status
    echo "A coastal region flooded by the sealing of Z-azoykenne. The first **Rune** rests here."
    
    echo -e "\nA hostile figure, G-rudge (G), confronts you—a general of the fallen R-oykenne."
    echo "1) Engage G-rudge in combat (Fighter/Power check)."
    echo "2) Attempt to flee and find the Rune stealthily (Rogue/Stealth check)."
    
    read -p "Enter your choice (1-2): " choice

    if [ "$choice" == "1" ]; then
        if (( POWER >= 80 )); then
            echo "Your strength is overwhelming! G-rudge is defeated."
            POWER=$((POWER + 10))
        else
            echo "You struggle. G-rudge escapes, but not before wounding you."
            take_damage 35
        fi
        add_rune
        scene_kraken
    elif [ "$choice" == "2" ]; then
        if [ "$PLAYER_CLASS" == "Rogue (Veteran)" ]; then
            echo "You use the flooded chaos to your advantage, slipping past G-rudge."
        else
            echo "Your stealth fails. G-rudge sees you and drains your power."
            POWER=$((POWER - 15))
        fi
        add_rune
        scene_kraken
    else
        echo "The chaos of the D-eluge swirls around you."
        take_damage 5
        scene_deluge
    fi
}

# K - Kraken (Rune 2)
function scene_kraken() {
    clear
    echo "#####################################################"
    echo "## K: K-RAKEN - The Deep Guard                   ##"
    echo "#####################################################"
    display_status
    echo "The second **Rune** is guarded by the K-raken (K), a monster of elemental S-tihuu (Earth)."
    echo "To defeat it, you need the **C-hronos** (C) artifact to weaken it, which is hidden nearby."

    if [ "$HAS_CHRONOS" == "false" ]; then
        echo -e "\nYou must first find the C-hronos artifact."
        echo "1) Search a nearby sunken structure for the C-hronos."
        echo "2) Try to fight the K-raken without it (Extreme Risk)."
        read -p "Enter your choice (1-2): " sub_choice
        
        if [ "$sub_choice" == "1" ]; then
            echo "You find the artifact! It allows you to freeze time for a split second."
            HAS_CHRONOS="true"
        else
            echo "The K-raken's blow is devastating."
            take_damage 60
            echo "You wisely retreat."
        fi
        scene_kraken # Loop back to face the Kraken
        return
    fi
    
    # If HAS_CHRONOS is true
    echo "Using the C-hronos (C), you find the K-raken's weakness."
    echo "1) Strike the weak point."
    echo "2) Attempt to use the $PLAYER_CLASS's ultimate power."
    
    read -p "Enter your choice (1-2): " final_kraken_choice
    
    if [ "$final_kraken_choice" == "1" ]; then
        echo "The K-raken is slain! You retrieve the **Rune**."
        add_rune
        scene_nexus
    else
        echo "Your power is ineffective. The K-raken lashes out with $W-rath (W)."
        take_damage 25
        echo "You barely survive and flee with the Rune."
        add_rune
        scene_nexus
    fi
}

# N - Nexus (Rune 3)
function scene_nexus() {
    clear
    echo "#####################################################"
    echo "## N: N-EXUS - Convergence of N-ona and N-ano      ##"
    echo "#####################################################"
    display_status
    echo "You reach the N-exus, the center of the world's balancing forces. The third **Rune** is here, guarded by an I-dol (I)."
    
    echo "A cryptic $X-enial (X) approaches you."
    echo "'The **I-dol** demands a Y-ield (Y). What will you sacrifice?'"
    
    echo "1) Sacrifice 30 **POWER** (Y-ield)."
    echo "2) Sacrifice 30 **HEALTH** (Y-ield)."
    echo "3) Destroy the I-dol with brute force (Risk $W-rath$)."
    
    read -p "Enter your choice (1-3): " sacrifice_choice
    
    case "$sacrifice_choice" in
        1) POWER=$((POWER - 30)); echo "Your Power fades, but the I-dol is satisfied.";;
        2) take_damage 30; echo "Your body aches, but the I-dol is satisfied.";;
        3) take_damage 15; echo "The I-dol shatters, but you take minor backlash from $W-rath$.";;
        *) echo "You hesitate. The idol grants you the Rune out of pity.";;
    esac
    
    add_rune
    scene_shadowlands
}

# S - Shadowlands (Rune 4)
function scene_shadowlands() {
    clear
    echo "#####################################################"
    echo "## S: S-HADOWLANDS - Remnants of Z-azoykenne       ##"
    echo "#####################################################"
    display_status
    echo "This land is corrupted by leftover Z-azoykenne influence. The fourth **Rune** lies here."
    
    if [ "$HAS_MANTLE" == "false" ]; then
        echo "You need the M-antle (M) of authority to pass through the corrupted air. You must find it first."
        echo "1) Seek the M-antle in a nearby $V-ortex$ (V)."
        echo "2) Power through the Shadowlands (High damage risk)."
        
        read -p "Enter your choice (1-2): " mantle_choice
        
        if [ "$mantle_choice" == "1" ]; then
            echo "You brave the $V-ortex$ and claim the $M-antle$. (+10 Health)"
            HAS_MANTLE="true"
            HEALTH=$((HEALTH + 10))
        else
            take_damage 45
            echo "The corruption nearly kills you, but you survive to claim the Rune."
            add_rune
        fi
        
        if [ "$HAS_MANTLE" == "true" ]; then
            echo "Protected by the M-antle (M), you safely locate the fourth Rune."
            add_rune
        fi

        read -p "Press ENTER to continue..."
    fi
    scene_treasury
}

# T - Treasury (Rune 5 & Final Confrontation)
function scene_treasury() {
    clear
    echo "#####################################################"
    echo "## T: T-REASURY - The Final Rune                   ##"
    echo "#####################################################"
    display_status
    echo "You find the T-reasury, where the final **Rune** and the **R-ecluse** (R), the vengeful general, await."
    
    if (( RUNES_FOUND < 4 )); then
        echo "You haven't gathered enough Runes! The R-ecluse laughs and seals the way."
        game_over
    fi

    echo "The R-ecluse attempts to undo your work, unleashing a $P-lague$ (P) on the world!"
    echo "You must use the U-nravel (U) spell now to harness the Z-ephyr (Z) and purify the $T-ahkmahnelle$."
    
    echo "1) Cast the U-nravel spell."
    echo "2) Attack the R-ecluse directly."
    
    read -p "Enter your choice (1-2): " final_choice

    if [ "$final_choice" == "1" ] && [ "$RUNES_FOUND" == "5" ]; then
        echo "The five Runes glow intensely. You channel the U-nravel (U) spell. The $Z-ephyr$ (Z) washes over the lands!"
        echo "The R-ecluse is purified, the $P-lague$ is lifted, and $T-ahkmahnelle$ is stabilized."
        
        echo -e "\n🏆 VICTORY! THE SECOND ECHO IS COMPLETE! 🏆"
        echo "The Lands of Ages are truly safe... for now."
    else
        echo "You fail to stabilize the land. The $P-lague$ (P) spreads."
        game_over
    fi
    
    exit 0
}

# --- MAIN GAME EXECUTION ---

function start_game() {
    clear
    echo -e "====================================================="
    echo -e "      WELCOME TO RETURN2LANDSOFAGES: THE SECOND ECHO"
    echo -e "====================================================="
    echo "The Q-uest to stabilize Tahkmahnelle begins now."
    read -p "Press ENTER to continue..."
    
    scene_awakening
}

# Run the game
start_game
