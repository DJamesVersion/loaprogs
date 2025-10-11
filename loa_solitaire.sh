#!/bin/bash
# Lands of Ages (LoA) Solitaire Game Implementation in Bash

# ----------------------------------------------------
# --- CONFIGURATION AND ANSI COLORS ---
# ----------------------------------------------------

# ANSI Colors
RED='\033[0;31m'    # For Hearts and Diamonds
BLACK='\033[0;30m'  # For Spades and Clubs
GREEN='\033[0;32m'  # Game accents/success
BLUE='\033[0;34m'   # Tableau text/headers
YELLOW='\033[0;33m' # UI highlights
NC='\033[0m'        # No Color (reset)
BG_LIGHT='\033[47m' # Light background for cards

# Card Map
declare -A CARD_RANKS=(
    [1]="A" [2]="2" [3]="3" [4]="4" [5]="5" [6]="6" [7]="7"
    [8]="8" [9]="9" [10]="T" [11]="J" [12]="Q" [13]="K"
)

# Game State Variables
# Tableau: T1-T20 (5 columns x 4 rows)
# Foundations: F1-F8
# Reserves: R1-R2
# Note: In Bash, arrays are 0-indexed. We use associative arrays where possible.
declare -a TABLEAU # Array holding 20 tableau pile strings
declare -a FOUNDATIONS # Array holding 8 foundation pile strings
declare -a RESERVES # Array holding 2 reserve card strings
declare STOCK=""
declare WASTE=""

# ----------------------------------------------------
# --- HELPER FUNCTIONS ---
# ----------------------------------------------------

# Function to get the color code for a card
get_color() {
    local suit="$1"
    if [[ "$suit" == "H" || "$suit" == "D" ]]; then
        echo -e "${RED}"
    else
        echo -e "${BLACK}"
    fi
}

# Function to format a card string for display
format_card() {
    local card_code="$1" # Format: 13H (Rank-Suit)
    local rank="${card_code%?}"
    local suit="${card_code: -1}"

    # Get Rank Symbol
    local rank_symbol="${CARD_RANKS[$rank]}"

    # Get Suit Symbol
    local suit_symbol=""
    case "$suit" in
        C) suit_symbol="♣"; color="${BLACK}"; ;;
        D) suit_symbol="♦"; color="${RED}"; ;;
        H) suit_symbol="♥"; color="${RED}"; ;;
        S) suit_symbol="♠"; color="${BLACK}"; ;;
        *) suit_symbol="?"; color="${RED}"; ;;
    esac

    # Return formatted card: [RankSuit]
    # We use a standard background for contrast, then reset
    echo -e "${BG_LIGHT}${color}${rank_symbol}${suit_symbol}${NC}"
}

# Function to get the rank and color of a card
get_card_details() {
    local card_code="$1"
    local rank="${card_code%?}"
    local suit="${card_code: -1}"
    local color
    if [[ "$suit" == "H" || "$suit" == "D" ]]; then
        color="R" # Red
    else
        color="B" # Black
    fi
    echo "$rank $color"
}

# ----------------------------------------------------
# --- GAME LOGIC FUNCTIONS ---
# ----------------------------------------------------

# Function to create and shuffle a standard 104-card deck
init_deck() {
    local ranks="1 2 3 4 5 6 7 8 9 10 11 12 13" # A to K
    local suits="C D H S" # Clubs, Diamonds, Hearts, Spades
    local deck1=""
    local deck2=""

    # Create two full decks
    for r in $ranks; do
        for s in $suits; do
            deck1+="$r$s "
            deck2+="$r$s "
        done
    done

    # Combine and shuffle
    STOCK="$deck1$deck2"
    # Basic shuffle: split into lines and sort randomly, then join back
    STOCK=$(echo "$STOCK" | tr ' ' '\n' | shuf | tr '\n' ' ')
    STOCK="${STOCK%% }" # Trim trailing space
}

# Function to deal initial cards
deal_cards() {
    local i
    local card

    # 1. Deal 5 cards face-up to 20 Tableau Piles (T1-T20)
    for i in {0..19}; do
        local pile=""
        for _ in {1..5}; do
            card="${STOCK%% *}" # Get first card
            pile+="$card "
            STOCK="${STOCK#* }" # Remove first card
        done
        TABLEAU[$i]="${pile%% }" # Trim trailing space
    done

    # 2. Deal 1 card to 2 Reserves (R1-R2)
    for i in {0..1}; do
        RESERVES[$i]="${STOCK%% *}"
        STOCK="${STOCK#* }"
    done

    # 3. Initialize Foundations and Waste
    for i in {0..7}; do
        FOUNDATIONS[$i]="" # Foundations start empty
    done
    WASTE=""
}

# Function to draw a card from Stock to Waste
draw_card() {
    if [[ -z "$STOCK" ]]; then
        if [[ -z "$WASTE" ]]; then
            echo -e "${RED}Stock is empty. Game over if no more moves possible!${NC}"
            return 1
        else
            echo -e "${YELLOW}Stock is empty! Cannot draw.${NC}"
            return 1
        fi
    fi

    local card="${STOCK%% *}"
    WASTE="$card $WASTE"
    STOCK="${STOCK#* }"
    STOCK="${STOCK%% }" # Trim trailing space if necessary
    echo -e "${GREEN}Drawn ${card}. Now on top of Waste.${NC}"
    return 0
}

# ----------------------------------------------------
# --- UI FUNCTIONS ---
# ----------------------------------------------------

# Function to display the game board
display_board() {
    clear
    echo -e "${YELLOW}========================================================================================${NC}"
    echo -e "${YELLOW}                       ${GREEN}LANDS OF AGES (LoA) SOLITAIRE${YELLOW}                    ${NC}"
    echo -e "${YELLOW}========================================================================================${NC}"

    # --- FOUNDATIONS (F1-F8) and STOCK/WASTE ---
    echo -e "${BLUE}FOUNDATIONS (Build A->K by Suit) ${NC} | ${BLUE}STOCK / WASTE / RESERVES${NC}"
    echo -n " "
    for i in {0..7}; do
        local top_card="${FOUNDATIONS[$i]%% *}"
        local display_card="[ F$((i+1)) ]"
        if [[ -n "$top_card" ]]; then
            display_card="$(format_card "$top_card")"
        fi
        echo -n "$display_card "
    done

    echo -n " | "

    # Stock
    local stock_count
    stock_count=$(echo "$STOCK" | wc -w | tr -d ' ')
    if [[ "$stock_count" -gt 0 ]]; then
        echo -n "${YELLOW}[ STK:$stock_count ]${NC} "
    else
        echo -n "${RED}[ STK: 0 ]${NC} "
    fi

    # Waste
    local waste_top="${WASTE%% *}"
    local waste_display="[ WST ]"
    if [[ -n "$waste_top" ]]; then
        waste_display="$(format_card "$waste_top")"
    fi
    echo -n "$waste_display "

    # Reserves
    for i in {0..1}; do
        local reserve_card="${RESERVES[$i]}"
        local reserve_display="[ R$((i+1)) ]"
        if [[ -n "$reserve_card" ]]; then
            reserve_display="$(format_card "$reserve_card")"
        fi
        echo -n "$reserve_display "
    done
    echo ""
    echo -e "${YELLOW}----------------------------------------------------------------------------------------${NC}"

    # --- TABLEAU (T1-T20) ---
    echo -e "${BLUE}TABLEAU (Build K->A same COLOR suit)${NC}"
    echo -e "   C1    C2    C3    C4    C5"

    local max_depth=0
    local i
    for i in {0..19}; do
        local depth
        depth=$(echo "${TABLEAU[$i]}" | wc -w | tr -d ' ')
        if [[ "$depth" -gt "$max_depth" ]]; then
            max_depth="$depth"
        fi
    done

    # Display row by row (up to max_depth)
    for d in $(seq 1 $max_depth); do
        echo -n "R$d|"
        for c in {0..4}; do # Columns 1 to 5
            local pile_index # T1=0, T2=1, ..., T20=19
            pile_index=$((c + ((d-1) * 5)))

            if [[ $pile_index -lt 20 ]]; then
                # Get the card at this depth (1-indexed)
                local card_list="${TABLEAU[$pile_index]}"
                local card=""
                local current_depth=0
                # Find the card at the current depth
                for card_code in $card_list; do
                    current_depth=$((current_depth + 1))
                    if [[ $current_depth -eq $d ]]; then
                        card="$card_code"
                        break
                    fi
                done

                # Print card or spacer
                if [[ -n "$card" ]]; then
                    echo -n "$(format_card "$card")"
                else
                    echo -n "      " # Spacer
                fi
                echo -n "|"
            fi
        done
        echo ""
    done

    # Display Tableau Labels (T1-T20)
    echo -n "   "
    for i in {1..20}; do
        local label="T$i"
        if [[ $i -le 5 ]]; then
            echo -n " $label |"
        elif [[ $((i % 5)) -eq 1 && $i -ne 1 ]]; then
            echo -e "\n   | $label |"
        elif [[ $i -gt 5 ]]; then
            echo -n " $label |"
        fi
    done
    echo ""
    echo -e "${YELLOW}========================================================================================${NC}"
}

# ----------------------------------------------------
# --- VALIDATION FUNCTIONS ---
# ----------------------------------------------------

# Validate a move from source to destination
validate_move() {
    local source_pile="$1"
    local dest_pile="$2"
    local card_rank_src card_color_src
    local card_rank_dest card_color_dest

    # --- Tableau to Tableau (T-to-T) ---
    if [[ "$source_pile" =~ ^T([0-9]{1,2})$ ]] && [[ "$dest_pile" =~ ^T([0-9]{1,2})$ ]]; then
        local src_idx=$(( ${BASH_REMATCH[1]} - 1 ))
        local dest_idx=$(( ${BASH_REMATCH[3]} - 1 ))

        local src_pile="${TABLEAU[$src_idx]}"
        local dest_pile_content="${TABLEAU[$dest_idx]}"

        # 1. Get the card being moved (the last card of the source pile)
        local card_to_move="${src_pile##* }"
        if [[ -z "$card_to_move" || "$card_to_move" == "$src_pile" ]]; then
             card_to_move="$src_pile" # Handle single-card pile
        fi
        if [[ -z "$card_to_move" ]]; then
            echo -e "${RED}Error: Source Tableau pile T$((src_idx+1)) is empty.${NC}"
            return 1
        fi

        # 2. Get the target card (top of the destination pile)
        local top_dest_card="${dest_pile_content##* }"

        # If destination is empty, only a King can move there
        if [[ -z "$top_dest_card" ]]; then
            # Extract rank of moving card
            read card_rank_src card_color_src < <(get_card_details "$card_to_move")
            if [[ "$card_rank_src" -ne 13 ]]; then # 13 is King
                echo -e "${RED}Rule: Only a King (K) can move to an empty Tableau Land.${NC}"
                return 1
            fi
            return 0 # Valid move: King to empty pile
        fi

        # 3. Check Tableau rules (Down by rank, Same color suit)
        read card_rank_src card_color_src < <(get_card_details "$card_to_move")
        read card_rank_dest card_color_dest < <(get_card_details "$top_dest_card")

        # Check Rank: Down by 1 (e.g., 5 onto 6)
        if [[ $((card_rank_src + 1)) -ne "$card_rank_dest" ]]; then
            echo -e "${RED}Rule: Rank must be built down (e.g., Q onto K, 3 onto 4).${NC}"
            return 1
        fi

        # Check Color: Same Color Suit (e.g., Hearts onto Diamonds is OK; Hearts onto Spades is NOT OK)
        if [[ "$card_color_src" != "$card_color_dest" ]]; then
            echo -e "${RED}Rule: Suit color must match (Red onto Red, Black onto Black).${NC}"
            return 1
        fi

        return 0 # Valid T-to-T move
    fi

    # --- Waste to Tableau (W-to-T) ---
    if [[ "$source_pile" == "W" ]] && [[ "$dest_pile" =~ ^T([0-9]{1,2})$ ]]; then
        local dest_idx=$(( ${BASH_REMATCH[1]} - 1 ))
        local card_to_move="${WASTE%% *}"
        local top_dest_card="${TABLEAU[$dest_idx]##* }"

        if [[ -z "$card_to_move" ]]; then
            echo -e "${RED}Error: Waste pile is empty.${NC}"
            return 1
        fi

        # If destination is empty, only a King can move there
        if [[ -z "$top_dest_card" ]]; then
            read card_rank_src card_color_src < <(get_card_details "$card_to_move")
            if [[ "$card_rank_src" -ne 13 ]]; then
                echo -e "${RED}Rule: Only a King (K) can move to an empty Tableau Land.${NC}"
                return 1
            fi
            return 0
        fi

        # Check Tableau rules
        read card_rank_src card_color_src < <(get_card_details "$card_to_move")
        read card_rank_dest card_color_dest < <(get_card_details "$top_dest_card")

        if [[ $((card_rank_src + 1)) -ne "$card_rank_dest" ]]; then
            echo -e "${RED}Rule: Rank must be built down from Waste (e.g., 6 onto 7).${NC}"
            return 1
        fi
        if [[ "$card_color_src" != "$card_color_dest" ]]; then
            echo -e "${RED}Rule: Suit color must match from Waste.${NC}"
            return 1
        fi

        return 0 # Valid W-to-T move
    fi

    # --- Any to Foundation (X-to-F) ---
    if [[ "$dest_pile" =~ ^F([1-8])$ ]]; then
        local dest_idx=$(( ${BASH_REMATCH[1]} - 1 ))
        local card_to_move=""

        # Determine the card being moved
        if [[ "$source_pile" =~ ^T([0-9]{1,2})$ ]]; then
            local src_idx=$(( ${BASH_REMATCH[1]} - 1 ))
            card_to_move="${TABLEAU[$src_idx]##* }"
            if [[ -z "$card_to_move" ]]; then
                echo -e "${RED}Error: Source Tableau pile T$((src_idx+1)) is empty.${NC}"
                return 1
            fi
        elif [[ "$source_pile" == "W" ]]; then
            card_to_move="${WASTE%% *}"
            if [[ -z "$card_to_move" ]]; then
                echo -e "${RED}Error: Waste pile is empty.${NC}"
                return 1
            fi
        elif [[ "$source_pile" =~ ^R([1-2])$ ]]; then
            local src_idx=$(( ${BASH_REMATCH[1]} - 1 ))
            card_to_move="${RESERVES[$src_idx]}"
            if [[ -z "$card_to_move" ]]; then
                echo -e "${RED}Error: Reserve R$((src_idx+1)) is empty.${NC}"
                return 1
            fi
        else
            echo -e "${RED}Error: Invalid source for Foundation move.${NC}"
            return 1
        fi

        # Check Foundation rules (Up by Rank, Same Suit)
        local top_dest_card="${FOUNDATIONS[$dest_idx]##* }"

        read card_rank_src card_color_src < <(get_card_details "$card_to_move")
        local card_suit_src="${card_to_move: -1}"

        # If foundation is empty, only an Ace can start it
        if [[ -z "$top_dest_card" ]]; then
            if [[ "$card_rank_src" -ne 1 ]]; then # 1 is Ace
                echo -e "${RED}Rule: Foundation F$((dest_idx+1)) must be started with an Ace (A).${NC}"
                return 1
            fi
            return 0 # Valid move: Ace to empty foundation
        fi

        # Check Rank: Up by 1 (e.g., 5 onto 4)
        read card_rank_dest card_color_dest < <(get_card_details "$top_dest_card")
        local card_suit_dest="${top_dest_card: -1}"

        if [[ "$card_rank_src" -ne $((card_rank_dest + 1)) ]]; then
            echo -e "${RED}Rule: Rank must be built up to Foundation (e.g., 6 onto 5).${NC}"
            return 1
        fi

        # Check Suit: Same Suit
        if [[ "$card_suit_src" != "$card_suit_dest" ]]; then
            echo -e "${RED}Rule: Suit must match in Foundation (e.g., Heart onto Heart).${NC}"
            return 1
        fi

        return 0 # Valid X-to-F move
    fi

    # --- Reserve to Tableau (R-to-T) ---
    if [[ "$source_pile" =~ ^R([1-2])$ ]] && [[ "$dest_pile" =~ ^T([0-9]{1,2})$ ]]; then
        local src_idx=$(( ${BASH_REMATCH[1]} - 1 ))
        local dest_idx=$(( ${BASH_REMATCH[3]} - 1 ))
        local card_to_move="${RESERVES[$src_idx]}"
        local top_dest_card="${TABLEAU[$dest_idx]##* }"

        if [[ -z "$card_to_move" ]]; then
            echo -e "${RED}Error: Reserve R$((src_idx+1)) is empty.${NC}"
            return 1
        fi

        # If destination is empty, only a King can move there
        if [[ -z "$top_dest_card" ]]; then
            read card_rank_src card_color_src < <(get_card_details "$card_to_move")
            if [[ "$card_rank_src" -ne 13 ]]; then
                echo -e "${RED}Rule: Only a King (K) can move Reserve R$((src_idx+1)) to an empty Tableau Land.${NC}"
                return 1
            fi
            return 0
        fi

        # Check Tableau rules
        read card_rank_src card_color_src < <(get_card_details "$card_to_move")
        read card_rank_dest card_color_dest < <(get_card_details "$top_dest_card")

        if [[ $((card_rank_src + 1)) -ne "$card_rank_dest" ]]; then
            echo -e "${RED}Rule: Rank must be built down from Reserve (e.g., 6 onto 7).${NC}"
            return 1
        fi
        if [[ "$card_color_src" != "$card_color_dest" ]]; then
            echo -e "${RED}Rule: Suit color must match from Reserve.${NC}"
            return 1
        fi

        return 0 # Valid R-to-T move
    fi

    echo -e "${RED}Error: Invalid move command or target combination (e.g., W to W, F to T, etc.).${NC}"
    return 1
}

# ----------------------------------------------------
# --- EXECUTION FUNCTIONS ---
# ----------------------------------------------------

# Executes a validated move
execute_move() {
    local source_pile="$1"
    local dest_pile="$2"
    local card_to_move=""
    local src_idx=""
    local dest_idx=""

    # 1. IDENTIFY CARD TO MOVE AND REMOVE IT FROM SOURCE
    if [[ "$source_pile" =~ ^T([0-9]{1,2})$ ]]; then
        src_idx=$(( ${BASH_REMATCH[1]} - 1 ))
        card_to_move="${TABLEAU[$src_idx]##* }"
        TABLEAU[$src_idx]="${TABLEAU[$src_idx]% $card_to_move}"
        TABLEAU[$src_idx]="${TABLEAU[$src_idx]%% }" # Trim trailing space
    elif [[ "$source_pile" == "W" ]]; then
        card_to_move="${WASTE%% *}"
        WASTE="${WASTE#* }"
        WASTE="${WASTE%% }"
    elif [[ "$source_pile" =~ ^R([1-2])$ ]]; then
        src_idx=$(( ${BASH_REMATCH[1]} - 1 ))
        card_to_move="${RESERVES[$src_idx]}"
        RESERVES[$src_idx]=""
    else
        # Should not happen if validation passed
        return 1
    fi

    # 2. ADD CARD TO DESTINATION
    if [[ "$dest_pile" =~ ^T([0-9]{1,2})$ ]]; then
        dest_idx=$(( ${BASH_REMATCH[1]} - 1 ))
        if [[ -n "${TABLEAU[$dest_idx]}" ]]; then
            TABLEAU[$dest_idx]+=" "
        fi
        TABLEAU[$dest_idx]+="$card_to_move"
    elif [[ "$dest_pile" =~ ^F([1-8])$ ]]; then
        dest_idx=$(( ${BASH_REMATCH[1]} - 1 ))
        if [[ -n "${FOUNDATIONS[$dest_idx]}" ]]; then
            FOUNDATIONS[$dest_idx]+=" "
        fi
        FOUNDATIONS[$dest_idx]+="$card_to_move"
    else
        # Should not happen if validation passed
        return 1
    fi

    echo -e "${GREEN}SUCCESS: Moved $(format_card "$card_to_move") from $source_pile to $dest_pile.${NC}"
    return 0
}

# Check for win condition (All 8 foundations contain Kings)
check_win() {
    local i
    for i in {0..7}; do
        local top_card="${FOUNDATIONS[$i]##* }"
        local rank
        rank=$(get_card_details "$top_card" | awk '{print $1}')
        if [[ "$rank" -ne 13 ]]; then # Rank 13 is King
            return 1 # Not won yet
        fi
    done
    return 0 # All Kings on foundations
}

# Main game loop setup
setup_game() {
    init_deck
    deal_cards
    # Initial print
    display_board
}

# Main Game Loop
game_loop() {
    local input
    local source
    local destination
    local status_message="Welcome to Lands of Ages Solitaire! Type 'help' for commands."

    setup_game

    while true; do
        display_board
        echo -e "\n${YELLOW}STATUS:${NC} $status_message"
        status_message="" # Clear status after display

        # Check for win
        if check_win; then
            echo -e "\n${GREEN}========================================================================================${NC}"
            echo -e "${GREEN}CONGRATULATIONS! YOU HAVE CLEARED ALL THE LANDS AND WON THE GAME!${NC}"
            echo -e "${GREEN}========================================================================================${NC}"
            break
        fi

        echo -e "\n${BLUE}COMMANDS:${NC} Move [Source] [Dest] (e.g., T1 T5, W F1, R1 T10) | Draw [D] | Quit [Q]"
        read -r -p "Enter Command: " input
        input=$(echo "$input" | tr '[:lower:]' '[:upper:]') # Convert to uppercase

        case "$input" in
            Q)
                echo -e "${YELLOW}Quitting game. Farewell, traveler!${NC}"
                break
                ;;
            D)
                draw_card
                ;;
            HELP)
                status_message="Move: [Source] is T1-T20 (Tableau), W (Waste), R1-R2 (Reserve). [Dest] is T1-T20 or F1-F8 (Foundation)."
                ;;
            *)
                # Assuming input is "SRC DST"
                source=$(echo "$input" | awk '{print $1}')
                destination=$(echo "$input" | awk '{print $2}')

                if [[ -z "$source" || -z "$destination" ]]; then
                    status_message="${RED}Invalid command format. Use 'SRC DST' or 'D' or 'Q'.${NC}"
                    continue
                fi

                if validate_move "$source" "$destination"; then
                    if ! execute_move "$source" "$destination"; then
                        status_message="${RED}Execution Error. Please report bug: $source to $destination${NC}"
                    fi
                else
                    status_message="${RED}Illegal move: $source to $destination.${NC}"
                fi
                ;;
        esac

        sleep 1
    done
}

# Execute the game
game_loop

# End of script

