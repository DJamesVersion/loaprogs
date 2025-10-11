#!/bin/bash
# Lands of Ages (LoA) Solitaire Guide - A Unix CLI Map and Rules App

# --- ANSI Color Definitions ---
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# --- Variables ---
APP_TITLE="LoA SOLITAIRE GUIDE"
VERSION="1.0"

# Function to display the main menu
show_menu() {
    clear
    echo -e "${GREEN}-------------------------------------------${NC}"
    echo -e "${GREEN}        $APP_TITLE (v$VERSION)           ${NC}"
    echo -e "${GREEN}-------------------------------------------${NC}"
    echo -e "Welcome, Adventurer! What land shall we explore?"
    echo ""
    echo -e " ${YELLOW}1${NC}. View the ${BLUE}Lands Map (Tableau Layout)${NC}"
    echo -e " ${YELLOW}2${NC}. View ${BLUE}Setup and Core Rules${NC}"
    echo -e " ${YELLOW}3${NC}. View ${BLUE}Scoring and Strategy Tips${NC}"
    echo -e " ${RED}Q${NC}. Exit Guide"
    echo ""
    echo -e "${GREEN}-------------------------------------------${NC}"
}

# Function to display the LoA Tableau Map
show_map() {
    clear
    echo -e "${GREEN}--- THE LANDS OF AGES (5x4 Tableau) ---${NC}"
    echo ""
    # The map is typically a 5 column by 4 row tableau.
    # We use different colors for different strategic zones.

    # Row 1: High Card Lands (Foundation Precursors)
    echo -e "  R1 | ${RED}CASTLE${NC} | ${YELLOW}COAST${NC}  | ${YELLOW}COAST${NC}  | ${YELLOW}COAST${NC}  | ${RED}TOWER${NC}  |"

    # Row 2: Central/Fields Lands (Primary Working Area)
    echo -e "  R2 | ${BLUE}FOREST${NC} | ${GREEN}FIELDS${NC} | ${GREEN}FIELDS${NC} | ${GREEN}FIELDS${NC} | ${BLUE}FOREST${NC} |"

    # Row 3: Mid/Ruins Lands (Secondary Working Area)
    echo -e "  R3 | ${BLUE}SWAMP${NC}  | ${RED}RUINS${NC}  | ${RED}RUINS${NC}  | ${RED}RUINS${NC}  | ${BLUE}SWAMP${NC}  |"

    # Row 4: Outer/Mountain Lands (Hardest to Clear)
    echo -e "  R4 | ${YELLOW}MOUNTAIN${NC} | ${BLUE}SEA${NC}    | ${BLUE}SEA${NC}    | ${BLUE}SEA${NC}    | ${YELLOW}MOUNTAIN${NC} |"
    echo ""
    echo "Legend:"
    echo -e " - ${RED}Red Lands${NC}: Often hold key cards (Kings/Queens/Aces)."
    echo -e " - ${BLUE}Blue Lands${NC}: Edge zones; clearing them unlocks central areas."
    echo -e " - ${GREEN}Green Lands${NC}: Primary card movement and building space."
    echo ""
    read -p "Press [ENTER] to return to the menu..."
}

# Function to display the rules and setup
show_rules() {
    clear
    echo -e "${GREEN}--- SETUP AND CORE RULES ---${NC}"
    echo ""
    echo -e "${YELLOW}I. SETUP (Using Two Decks)${NC}"
    echo " 1. Foundations (8 piles): Place the first eight Aces up here. Build up by suit to King."
    echo " 2. Tableau (20 piles): Deal 5 cards face-up to each of the 20 'Lands' (see map)."
    echo " 3. Reserves (2 piles): Place one face-up card on each of the two Reserve spots."
    echo " 4. Stock/Waste: Remaining cards are the Stock."
    echo ""
    echo -e "${YELLOW}II. MOVEMENT RULES${NC}"
    echo " - ${BLUE}Tableau Building${NC}: Cards can be moved between Lands (tableau piles)."
    echo "   - You can build down by rank, but the suit must be the ${RED}SAME COLOR${NC}."
    echo "   - Full sequences can be moved (e.g., 5-4-3 of Red/Black suits)."
    echo " - ${BLUE}Empty Lands${NC}: Only a King (or a sequence starting with a King) may fill an empty Land pile."
    echo " - ${BLUE}Reserves${NC}: Cards from the Reserves can be played to the Foundations or the Tableau."
    echo " - ${BLUE}Stock${NC}: The Stock is turned over one card at a time to the Waste pile. Only the top Waste card is available."
    echo ""
    read -p "Press [ENTER] to return to the menu..."
}

# Function to display strategy tips
show_strategy() {
    clear
    echo -e "${GREEN}--- SCORING AND STRATEGY TIPS ---${NC}"
    echo ""
    echo -e "${YELLOW}Scoring Goal:${NC} Move all 104 cards to the 8 Foundation piles."
    echo ""
    echo -e "${YELLOW}General Strategy:${NC}"
    echo " 1. ${BLUE}Focus on the Edges:${NC} The Mountain and Swamp Lands often lock up critical cards. Prioritize exposing the face-down cards in these outer columns (1 & 5)."
    echo " 2. ${BLUE}Create Empty Lands:${NC} Empty Land piles are your most valuable resource, allowing you to move King sequences and re-arrange the entire tableau."
    echo " 3. ${BLUE}Consolidate in Fields:${NC} Use the central 'Fields' (R2, C2-C4) to create long, same-color runs, which can be moved together easily when needed."
    echo " 4. ${BLUE}Watch the Reserves:${NC} The two Reserve cards are immediate-access life savers. Don't use them prematurely; save them to free up a stuck card in the Tableau."
    echo " 5. ${BLUE}Avoid Excessive Building:${NC} While building down is necessary, don't bury high-ranking cards (10, J, Q) you might soon need for the Foundations under long sequences."
    echo ""
    read -p "Press [ENTER] to return to the menu..."
}

# Main Application Loop
while true; do
    show_menu
    read -p "Enter your choice (1, 2, 3, or Q): " choice

    # Convert choice to lowercase for flexible input
    case "${choice,,}" in
        1) show_map ;;
        2) show_rules ;;
        3) show_strategy ;;
        q)
            clear
            echo -e "${GREEN}Exiting LoA Guide. May your lands be cleared!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice. Please enter 1, 2, 3, or Q.${NC}"
            sleep 1.5
            ;;
    esac
done

# End of script

