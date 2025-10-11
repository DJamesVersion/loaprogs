#!/bin/bash
# Lands of Spaceages - Text-based Shell Arcade Game
# Characters: Jerry & Tracy (The Ship)
# Mission: Survive and reach 1000 distance to deliver the artifact to the School.

# --- Terminal Setup and Constants ---

# Define Colors using ANSI escape codes
# Color format: \e[<color_code>m
COLOR_RESET="\e[0m"
COLOR_SHIP="\e[33m"      # Yellow
COLOR_ASTEROID="\e[31m"  # Red
COLOR_INFO="\e[36m"      # Cyan
COLOR_GOAL="\e[32m"      # Green

# Game dimensions
MAP_WIDTH=30   # Character columns
MAP_HEIGHT=15  # Character rows (excluding info bar)

# Initial ship position (X is center, Y is near the bottom)
SHIP_X=$((MAP_WIDTH / 2 - 1)) # Ship is 3 characters wide, so -1 centers it
SHIP_Y=$((MAP_HEIGHT - 2))
SHIP_DRAW="<|>"

# Game state
SCORE=0
GAME_SPEED=0.08 # Lower value means faster game (0.08 is standard)
OBSTACLE_DENSITY=4 # How often a new obstacle is added (1 in X chance per tick)

# Obstacles stored as "Y,X" pairs in an array
OBSTACLES=()

# --- Utility Functions ---

# Function to clean up the terminal state (MANDATORY for shell games)
cleanup() {
    tput cnorm      # Show cursor
    tput clear      # Clear screen
    echo -e "${COLOR_RESET}Game Ended. Thanks for flying, Jerry and Tracy!${COLOR_RESET}"
    exit 0
}

# Trap signals (Ctrl+C) to ensure cursor is visible on exit
trap cleanup SIGINT

# Function to initialize the screen
init_screen() {
    tput clear      # Clear the screen
    tput civis      # Hide the cursor
    echo -e "${COLOR_INFO}Lands of Spaceages - Pilot: Jerry & Tracy${COLOR_RESET}"
    echo -e "${COLOR_GOAL}[S] = School/Goal (1000) | Avoid ${COLOR_ASTEROID}*${COLOR_GOAL}"
    # Draw the boundary lines
    echo -e "${COLOR_GOAL}--------------------------------${COLOR_RESET}"
}

# --- Game Logic Functions ---

# Function to generate a new obstacle
spawn_obstacle() {
    # Add a new obstacle at Y=0 (top) and a random X position
    local new_x=$((RANDOM % MAP_WIDTH))
    OBSTACLES+=("0,${new_x}")
}

# Function to move all obstacles down and check for collisions
update_obstacles() {
    local i
    local new_obstacles=()
    
    # Check for new spawn opportunity (based on density)
    if [ $((RANDOM % OBSTACLE_DENSITY)) -eq 0 ]; then
        spawn_obstacle
    fi

    for i in "${!OBSTACLES[@]}"; do
        local obs_coords="${OBSTACLES[$i]}"
        local obs_y=$(echo $obs_coords | cut -d',' -f1)
        local obs_x=$(echo $obs_coords | cut -d',' -f2)
        
        # 1. Collision Check (before moving down)
        # Check if the asteroid is on the player's row (SHIP_Y)
        # AND if the asteroid's X position is within the ship's 3-char width
        if [ "$obs_y" -eq "$SHIP_Y" ]; then
            if [ "$obs_x" -ge "$SHIP_X" ] && [ "$obs_x" -lt "$((SHIP_X + 3))" ]; then
                game_over
            fi
        fi

        # 2. Move Obstacle Down
        local new_y=$((obs_y + 1))
        
        # 3. Check if it went past the screen bottom
        if [ "$new_y" -lt "$MAP_HEIGHT" ]; then
            new_obstacles+=("${new_y},${obs_x}")
        else
            # Successfully dodged: increase the score slightly
            SCORE=$((SCORE + 1))
        fi
    done
    OBSTACLES=("${new_obstacles[@]}")
}

# Function to draw the entire game state
draw_game() {
    # Draw Score/Info (Cursor position 0, 3)
    tput cup 3 0
    echo -e "${COLOR_INFO}Distance: ${SCORE} / 1000 | Controls: A/D${COLOR_RESET}"

    # Draw a boundary line
    tput cup 4 0
    echo -e "${COLOR_GOAL}--------------------------------${COLOR_RESET}"

    # Draw the Ship (Cursor position SHIP_Y + 5)
    tput cup $((SHIP_Y + 5)) $SHIP_X
    echo -e "${COLOR_SHIP}${SHIP_DRAW}${COLOR_RESET}"
    
    # Draw Obstacles
    for obs_coords in "${OBSTACLES[@]}"; do
        local obs_y=$(echo $obs_coords | cut -d',' -f1)
        local obs_x=$(echo $obs_coords | cut -d',' -f2)
        
        # The game area starts at Y=5 (after info lines)
        tput cup $((obs_y + 5)) $obs_x
        echo -e "${COLOR_ASTEROID}*${COLOR_RESET}"
    done
}

# Function to clear the main game area
clear_game_area() {
    local y
    for ((y=5; y<MAP_HEIGHT+5; y++)); do
        tput cup $y 0
        printf "%${MAP_WIDTH}s" " " # Print spaces to clear the line
    done
}

# Function for Game Over state
game_over() {
    tput cup $((MAP_HEIGHT / 2 + 5)) 0
    echo -e "${COLOR_ASTEROID}================================${COLOR_RESET}"
    echo -e "${COLOR_ASTEROID}==   MISSION FAILED! CRASH!   ==${COLOR_RESET}"
    echo -e "${COLOR_ASTEROID}================================${COLOR_RESET}"
    sleep 3
    cleanup
}

# Function for Game Won state
game_won() {
    tput cup $((MAP_HEIGHT / 2 + 5)) 0
    echo -e "${COLOR_GOAL}==================================${COLOR_RESET}"
    echo -e "${COLOR_GOAL}== MISSION SUCCESS! ARTIFACT      ==${COLOR_RESET}"
    echo -e "${COLOR_GOAL}== DELIVERED TO THE SCHOOL! (1000)==${COLOR_RESET}"
    echo -e "${COLOR_GOAL}==================================${COLOR_RESET}"
    sleep 5
    cleanup
}

# --- Main Game Loop ---

init_screen

while true; do
    # 1. Read Input (Non-blocking, 1 character)
    read -rsn1 -t $GAME_SPEED key
    
    # Check for exit (q)
    if [[ "$key" == "q" ]]; then
        cleanup
    fi

    # 2. Update Ship Position (A=Left, D=Right)
    if [[ "$key" == "a" ]] || [[ "$key" == "A" ]]; then
        # Ensure ship doesn't go off the left edge
        if [ "$SHIP_X" -gt 0 ]; then
            SHIP_X=$((SHIP_X - 2)) # Move 2 spaces for faster travel
        fi
    elif [[ "$key" == "d" ]] || [[ "$key" == "D" ]]; then
        # Ensure ship doesn't go off the right edge (SHIP_DRAW is 3 chars wide)
        if [ "$((SHIP_X + 3))" -lt "$MAP_WIDTH" ]; then
            SHIP_X=$((SHIP_X + 2)) # Move 2 spaces
        fi
    fi

    # 3. Game Logic
    update_obstacles
    
    # 4. Check Win Condition
    if [ "$SCORE" -ge 1000 ]; then
        game_won
    fi

    # 5. Drawing (Clear and Redraw)
    clear_game_area
    draw_game
    
    # The sleep time is primarily controlled by the 'read -t' timeout, 
    # but a final slight delay ensures consistent drawing speed.
    sleep 0.01 
done

