#!/bin/bash
#
# HUD File Manager (Single-Panel TUI Simulation)
#
# USAGE: bash hud_file_manager.sh
# Requires 'tput', 'ls', and a modern shell (bash/zsh) for array support.
#
################################################################################

# --- Configuration and Terminal Colors ---

# Define standard TPUT commands for colors and cursor control
# Colors: 30-37 (foreground), 40-47 (background)
export TPUT_CLEAR=$(tput clear)
export TPUT_RESET=$(tput sgr0)
export TPUT_BOLD=$(tput bold)
export TPUT_CYAN=$(tput setaf 6)  # HUD Primary Color (Cyan)
export TPUT_GREEN=$(tput setaf 2) # Directory Color (Green)
export TPUT_YELLOW=$(tput setaf 3) # Metadata Color (Yellow)
export TPUT_WHITE=$(tput setaf 7) # File Color (White)
export TPUT_REVERSE=$(tput rev)   # Selection Highlight

# Global State Variables
CURRENT_DIR=$(pwd)
CURRENT_INDEX=0
FILES=()
FILE_COUNT=0
MAX_LINES=$(tput lines)
MAX_COLS=$(tput cols)
LIST_LINES=0 # Calculated dynamically

# --- Core Functions ---

function get_files() {
    # Populates the FILES array with directory contents.
    # Directory entries are prefixed with a "/" for identification.
    
    # Clear arrays and reset count
    FILES=()
    FILE_COUNT=0
    
    # Add '..' entry for navigation unless already at root
    if [[ "$CURRENT_DIR" != "/" ]]; then
        FILES+=("../")
    fi
    
    # Get all files and directories, hiding dotfiles (use -A to include . and .. for reference)
    local items=($(ls -AF "$CURRENT_DIR"))
    
    for item in "${items[@]}"; do
        # Ignore '.' and the '..' if we already added it explicitly
        if [[ "$item" == "." || "$item" == ".." || "$item" == "../" ]]; then
            continue
        fi
        FILES+=("$item")
    done

    FILE_COUNT=${#FILES[@]}
}

function draw_header() {
    # Draws the active path and header line.
    echo "${TPUT_BOLD}${TPUT_CYAN}"
    echo "--- HUD File Manager --- Current Directory: ${CURRENT_DIR}"
    echo "${TPUT_RESET}"
}

function draw_footer() {
    # Draws file metadata and help text.
    
    # Metadata region starts at the bottom, reserving 6 lines
    local START_LINE=$((MAX_LINES - 6))
    tput cup $START_LINE 0

    echo "${TPUT_BOLD}${TPUT_YELLOW}--------------------------------------------------------------------------------${TPUT_RESET}"
    echo "${TPUT_BOLD}${TPUT_YELLOW} File Info ${TPUT_RESET}"
    
    if [[ $FILE_COUNT -gt 0 ]]; then
        local selected_file="${FILES[$CURRENT_INDEX]}"
        local filename="${selected_file%%/}" # Remove trailing slash for stat

        # Get file stats (using POSIX 'stat' for broad compatibility)
        local stats=$(stat -c "%A %h %U %G %s %y" "$CURRENT_DIR/$filename")
        
        echo "  ${TPUT_WHITE}Selected:${TPUT_RESET} $selected_file"
        echo "  ${TPUT_WHITE}Details: ${TPUT_RESET} $stats"
    fi
    
    echo "${TPUT_BOLD}${TPUT_YELLOW}--------------------------------------------------------------------------------${TPUT_RESET}"
    echo "  ${TPUT_WHITE}Navigation:${TPUT_RESET} (Type the line number and Enter to select/CD) ${TPUT_BOLD}${TPUT_CYAN}Q${TPUT_RESET}${TPUT_WHITE}: Quit"
}

function draw_list() {
    # Draws the list of files with highlight.
    
    # Calculate screen geometry
    MAX_LINES=$(tput lines)
    MAX_COLS=$(tput cols)
    LIST_LINES=$((MAX_LINES - 8)) # Reserve 1 for header, 7 for footer/info

    tput cup 2 0 # Start drawing list below header

    for ((i=0; i<FILE_COUNT && i<LIST_LINES; i++)); do
        local filename="${FILES[$i]}"
        local display_index=$((i + 1))
        local line_prefix="${display_index}."
        local color="${TPUT_WHITE}"
        
        # Determine color (ends with '/' is a directory)
        if [[ "$filename" == */ ]]; then
            color="${TPUT_GREEN}"
        fi
        
        local display_line="${line_prefix} ${filename}"
        
        # Check if this is the selected item
        if [[ $i -eq $CURRENT_INDEX ]]; then
            # Highlight with reverse video
            echo "${TPUT_REVERSE}${TPUT_CYAN}${display_line}"
            echo -ne "${TPUT_RESET}"
        else
            echo "${TPUT_BOLD}${color}${display_line}"
            echo -ne "${TPUT_RESET}"
        fi
    done
    
    # Clear remaining lines below the list
    for ((i=FILE_COUNT + 2; i<=LIST_LINES; i++)); do
        tput cup $i 0
        echo -n "${TPUT_RESET}"
        printf "%*s" $MAX_COLS "" # Print MAX_COLS spaces to clear the line
    done
}

function main_loop() {
    # The main application loop.
    local INPUT=""
    
    while true; do
        get_files # 1. Update file list
        
        # Clear screen and draw the interface
        $TPUT_CLEAR
        draw_header
        draw_list
        draw_footer
        
        # 2. Get Input
        tput cup $((MAX_LINES - 1)) 0
        echo -ne "${TPUT_BOLD}${TPUT_CYAN}Command/Index > ${TPUT_RESET}"
        read -r INPUT
        
        # 3. Process Input
        case "$INPUT" in
            [Qq])
                # Quit
                break
                ;;
            # Handle numeric input for selection/cd
            [0-9]* )
                local index=$((INPUT - 1))
                if [[ $index -ge 0 && $index -lt $FILE_COUNT ]]; then
                    CURRENT_INDEX=$index
                    
                    # If directory, perform CD
                    local selected_item="${FILES[$CURRENT_INDEX]}"
                    if [[ "$selected_item" == */ ]]; then
                        local target_dir="${selected_item%%/}"
                        
                        # Try to change directory
                        if cd "$CURRENT_DIR/$target_dir" 2>/dev/null; then
                            CURRENT_DIR=$(pwd)
                            CURRENT_INDEX=0 # Reset index on CD
                        else
                            # Permission Denied or other error
                            tput cup $((MAX_LINES - 1)) 0
                            echo "${TPUT_REVERSE}${TPUT_RED}ERROR: Cannot access '$target_dir'${TPUT_RESET}"
                            sleep 1
                        fi
                    fi
                fi
                ;;
            *)
                # Unknown command/input
                tput cup $((MAX_LINES - 1)) 0
                echo "${TPUT_REVERSE}${TPUT_RED}Unknown command or invalid index.${TPUT_RESET}"
                sleep 0.5
                ;;
        esac
    done
}

# --- Execution ---

# Ensure terminal reset on exit (Trap Ctrl+C and exit)
trap "tput reset; exit" SIGINT EXIT

# Initialize first run
get_files

# Start the application
main_loop

# Final cleanup
tput reset

