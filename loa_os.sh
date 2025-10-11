#!/bin/bash
# LoA OS Shell Emulator (v3.0)
# This script simulates a DOS-like command line environment using Bash.

# --- ANSI Color Configuration ---
# Uses standard ANSI colors for a retro green-on-black terminal look.
GREEN='\033[32m'
BRIGHT_GREEN='\033[92m'
RED='\033[31m'
YELLOW='\033[33m'
CYAN='\033[36m'
RESET='\033[0m'
CLEAR_LINE='\r\033[K'

# --- Global Configuration and State ---
VERSION="3.0.0 (Shell Edition)"
APP_NAME="LoA Operating System"
DATA_DIR="$HOME/.loa_os_data"
MOUNTED_DRIVES=("C") # Array of mounted drive letters (without the colon)

# State Variables
CURRENT_DRIVE="C"
CURRENT_PATH_REAL="$DATA_DIR/C" # Absolute path on the real filesystem
CURRENT_PATH_VIRTUAL="C:\\"     # Path displayed in the prompt
PROMPT="${BRIGHT_GREEN}C:\\>${RESET} "

# --- Utility Functions ---

function clear_screen() {
    clear
}

function print_slowly() {
    local text="$1"
    local delay=${2:-0.005}

    # Print characters one by one
    for (( i=0; i<${#text}; i++ )); do
        printf "%c" "${text:$i:1}"
        sleep "$delay"
    done
    printf "\n"
}

function update_prompt() {
    # 1. Update the virtual path display
    local virtual_path_display
    
    # Calculate path relative to the drive root
    if [[ "$CURRENT_PATH_REAL" == "$DATA_DIR/$CURRENT_DRIVE" ]]; then
        virtual_path_display="${CURRENT_DRIVE}:\\"
    else
        # Remove the /home/user/.loa_os_data/C part to get the relative DOS path
        virtual_path_display="${CURRENT_DRIVE}:\\${CURRENT_PATH_REAL#$DATA_DIR/$CURRENT_DRIVE/}"
        # Replace forward slashes with backslashes
        virtual_path_display="${virtual_path_display//\//\\}"
    fi

    CURRENT_PATH_VIRTUAL="$virtual_path_display"
    PROMPT="${BRIGHT_GREEN}${virtual_path_display}>${RESET} "
}

function get_drive_root() {
    echo "$DATA_DIR/$1"
}

# --- Built-in Program Logic ---

function builtin_loa_program() {
    print_slowly $YELLOW"***** Running LOA.EXE *****"$RESET 0.01
    print_slowly "> Initiating Aspiration Protocol..." 0.02
    print_slowly "> Verifying Core Beliefs..." 0.03
    print_slowly "> Processing Input..." 0.03
    
    printf "\n    ${CYAN}Success is not final, failure is not fatal:${RESET}\n"
    printf "    ${CYAN}it is the courage to continue that counts.${RESET}\n"
    printf "    - W. Churchill\n"
    
    print_slowly "\n> Mission Complete." 0.02
    print_slowly $YELLOW"***** Program Terminated *****"$RESET 0.01
}

function execute_program() {
    local command_name="$1"
    
    # Check for built-in EXE
    if [[ "$command_name" == "LOA.EXE" ]]; then
        builtin_loa_program
        return 0 # Success
    fi

    # Check for script execution (LoA Script or .BAT)
    # The command should exist as a file in the current directory and be executable
    if [[ -x "$CURRENT_PATH_REAL/$command_name" ]]; then
        printf "\n${CYAN}Executing LoA Script: %s...${RESET}\n" "$command_name"
        
        # Use a subshell to execute the script in the simulated environment
        (
            IFS=$'\n'
            # Set up the environment for the script
            LOA_OS_RUNNING=1
            export LOA_OS_RUNNING # Allow sub-processes to know they are in the emulator
            
            # Read script content line by line and process it through the shell logic
            while IFS= read -r line; do
                local cleaned_line=$(echo "$line" | tr -d '\r') # Remove Windows carriage returns
                if [[ -z "$cleaned_line" ]]; then continue; fi

                printf "[%s] > %s\n" "$command_name" "$cleaned_line"
                # Call the main processing function recursively (non-blocking)
                process_command "$cleaned_line"

            done < "$CURRENT_PATH_REAL/$command_name"
        )
        printf "${CYAN}Execution of %s complete.${RESET}\n" "$command_name"
        return 0
    fi
    
    return 1 # Not found
}

# --- Command Handlers ---

function cmd_ver() {
    printf "%s [Version %s]\n" "$APP_NAME" "$VERSION"
}

function cmd_cls() {
    clear_screen
}

function cmd_exit() {
    print_slowly "Shutting down LoA OS. Goodbye!" 0.03
    exit 0
}

function cmd_help() {
    printf "${BRIGHT_GREEN}Available LoA OS Commands:${RESET}\n\n"
    printf "CLS     - Clears the screen.\n"
    printf "DIR     - Displays a list of files and subdirectories.\n"
    printf "CD      - Changes the current directory or drive (e.g., CD .., CD D:).\n"
    printf "MOUNT   - Mounts a new virtual drive (Usage: MOUNT <drive_letter>:).\n"
    printf "ECHO    - Displays messages.\n"
    printf "EDIT    - Creates or modifies a file (Usage: EDIT <filename>). Uses 'nano' or 'vi'.\n"
    printf "VER     - Displays the LoA OS version.\n"
    printf "ABOUT   - Displays information about the system's purpose.\n"
    printf "<FILE>  - Execute an EXE or simple LoA Script file (requires execute permission).\n"
    printf "HELP    - Displays this list of commands.\n"
    printf "EXIT    - Terminates the LoA OS session.\n"
}

function cmd_dir() {
    local drive_label="${CURRENT_DRIVE}_LOA_VIRT" # Simple label simulation
    
    printf "\n Volume in drive %s is %s\n" "${CURRENT_DRIVE}:" "$drive_label"
    printf " Volume Serial Number is LOA-1994\n\n"
    printf " Directory of %s\n\n" "$CURRENT_PATH_VIRTUAL"

    local file_count=0
    local dir_count=0
    
    # Loop through contents of the real directory
    while IFS= read -r item; do
        if [[ "$item" == "." || "$item" == ".." ]]; then continue; fi
        
        local date_modified=$(date -r "$CURRENT_PATH_REAL/$item" "+%m/%d/%Y")
        local time_modified=$(date -r "$CURRENT_PATH_REAL/$item" "+%I:%Mp")
        
        if [[ -d "$CURRENT_PATH_REAL/$item" ]]; then
            # Directory
            printf " %-10s %-7s %-10s  %s\n" "$date_modified" "$time_modified" "${CYAN}<DIR>${RESET}" "$item"
            dir_count=$((dir_count + 1))
        else
            # File
            local file_size=$(stat -c "%s" "$CURRENT_PATH_REAL/$item")
            printf " %-10s %-7s %10s %s\n" "$date_modified" "$time_modified" "$file_size" "$item"
            file_count=$((file_count + 1))
        fi
    done < <(ls -a "$CURRENT_PATH_REAL")

    # Simulated free space
    local free_bytes=33554432 
    
    printf "\n %10s File(s)\n" "$file_count"
    printf " %10s Dir(s) %14s bytes free\n" "$dir_count" "$free_bytes"
}

function cmd_cd() {
    local target="$1"
    
    if [[ -z "$target" ]]; then
        printf "Current Directory: %s\n" "$CURRENT_PATH_VIRTUAL"
        return 0
    fi

    local target_upper=$(echo "$target" | tr '[:lower:]' '[:upper:]')

    # 1. Drive switching (e.g., D:)
    if [[ "$target_upper" =~ ^[A-Z]:$ ]]; then
        local drive_letter="${target_upper%:}"
        
        if [[ " ${MOUNTED_DRIVES[@]} " =~ " $drive_letter " ]]; then
            CURRENT_DRIVE="$drive_letter"
            CURRENT_PATH_REAL="$(get_drive_root "$drive_letter")"
            update_prompt
            return 0
        else
            printf "${RED}The system cannot find the drive specified: %s${RESET}\n" "$target"
            return 1
        fi
    fi

    # 2. Directory navigation (e.g., PROGRAMS, ..)
    local new_path="$CURRENT_PATH_REAL/$target"
    
    if [[ -d "$new_path" ]]; then
        # Use realpath for normalization, which also handles '..' correctly
        local new_path_normalized=$(realpath -L "$new_path" 2>/dev/null)
        
        # Check if the change stays within the current drive's root
        if [[ "$new_path_normalized" =~ ^$(get_drive_root "$CURRENT_DRIVE")(/.*)?$ ]]; then
            CURRENT_PATH_REAL="$new_path_normalized"
            update_prompt
            return 0
        else
            printf "${RED}Access denied. Cannot navigate outside the drive root: %s${RESET}\n" "$target"
            return 1
        fi
    else
        printf "${RED}The system cannot find the path specified: %s${RESET}\n" "$target"
        return 1
    fi
}

function cmd_mount() {
    local drive_spec="$1"
    
    if [[ -z "$drive_spec" ]]; then
        printf "Usage: MOUNT <drive_letter>:\n"
        printf "\nMounted Drives:\n"
        for d in "${MOUNTED_DRIVES[@]}"; do
            printf "  %s:\n" "$d"
        done
        return 0
    fi
    
    local drive_letter=$(echo "$drive_spec" | tr '[:lower:]' '[:upper:]' | tr -d ':')
    
    if [[ ! "$drive_letter" =~ ^[A-Z]$ ]]; then
        printf "${RED}Error: Invalid drive letter format. Must be a single letter (e.g., D:).${RESET}\n"
        return 1
    fi
    
    if [[ " ${MOUNTED_DRIVES[@]} " =~ " $drive_letter " ]]; then
        printf "${RED}Error: Drive %s: is already mounted.${RESET}\n" "$drive_letter"
        return 1
    fi
    
    # Create the backing directory for the new drive
    mkdir -p "$(get_drive_root "$drive_letter")"
    MOUNTED_DRIVES+=("$drive_letter")
    
    printf "${GREEN}Drive %s: mounted successfully. Backed by %s/${drive_letter}${RESET}\n" "$drive_letter" "$DATA_DIR"
}

function cmd_echo() {
    shift # Remove the command itself
    printf "%s\n" "$*"
}

function cmd_edit() {
    local filename="$1"
    
    if [[ -z "$filename" ]]; then
        printf "Usage: EDIT <filename>\n"
        return 1
    fi
    
    local filepath="$CURRENT_PATH_REAL/$filename"
    
    # Check if a directory with the same name exists
    if [[ -d "$filepath" ]]; then
        printf "${RED}Cannot edit a directory: %s${RESET}\n" "$filename"
        return 1
    fi
    
    printf "\n${YELLOW}--- LoA OS Simple Editor --- (Using system editor. Save and exit to finish)${RESET}\n"
    
    # Determine which editor to use (nano is generally more beginner-friendly)
    if command -v nano &> /dev/null; then
        nano "$filepath"
    elif command -v vi &> /dev/null; then
        vi "$filepath"
    else
        printf "${RED}Error: Neither 'nano' nor 'vi' found. Please install an editor or use a different system.${RESET}\n"
        return 1
    fi
    
    # The file creation/modification is handled by the system editor.
    printf "\n${GREEN}File '%s' saved. (Use 'DIR' to verify.)${RESET}\n" "$filename"
}

function cmd_about() {
    printf "${CYAN}======================================================${RESET}\n"
    printf "  ${BRIGHT_GREEN}${APP_NAME} (Shell Simulation)${RESET}\n"
    printf "${CYAN}======================================================${RESET}\n"
    printf "  This emulator is built entirely in Bash.\n"
    printf "  It simulates disk operations by managing a data directory:\n"
    printf "  %s\n\n" "$DATA_DIR"
    printf "  LoA stands for \"${BRIGHT_GREEN}The Operating System of Aspiration${RESET}\".\n"
}

# --- Main Logic ---

function boot_sequence() {
    clear_screen
    
    local boot_messages=(
        "\n  ${BRIGHT_GREEN}.  LoA OS - The Operating System of Aspiration  .${RESET}"
        "  ................................................${RESET}\n"
        "Copyright (C) 2025 LoA Corporation. All Rights Reserved."
        "LoA OS Version $VERSION\n"
        "Memory Check: 640 KB Base Memory ${GREEN}OK.${RESET}"
        "Extended Memory: 32768 KB ${GREEN}OK.${RESET}"
        "Searching for drives... Drive C: found."
        "Loading COMMAND.COM... ${GREEN}Done.${RESET}\n"
        "Type HELP for a list of available commands."
    )

    for message in "${boot_messages[@]}"; do
        print_slowly "$message" 0.002
        sleep 0.1
    done
}

function initialize_fs() {
    # Create the root data directory if it doesn't exist
    mkdir -p "$DATA_DIR" || { echo "Error: Cannot create data directory: $DATA_DIR"; exit 1; }

    # Create the C: drive root directory
    mkdir -p "$(get_drive_root "C")/SYSTEM"
    mkdir -p "$(get_drive_root "C")/PROGRAMS"

    # Create initial files if they don't exist
    if [[ ! -f "$(get_drive_root "C")/README.TXT" ]]; then
        echo "Welcome to LoA OS! Type HELP for commands. Try: CD PROGRAMS, DIR, or LOA.EXE." > "$(get_drive_root "C")/README.TXT"
    fi
    if [[ ! -f "$(get_drive_root "C")/COMMAND.COM" ]]; then
        echo "System Kernel" > "$(get_drive_root "C")/COMMAND.COM"
    fi
    
    # Create the LOA.EXE script which will execute the built-in function
    if [[ ! -f "$(get_drive_root "C")/LOA.EXE" ]]; then
        printf "LOA.EXE\n" > "$(get_drive_root "C")/LOA.EXE"
        chmod +x "$(get_drive_root "C")/LOA.EXE" # Must be executable for the script engine
    fi
    
    # Ensure current path is the C: root
    CURRENT_PATH_REAL="$(get_drive_root "C")"
    update_prompt
}

function process_command() {
    local input_line="$1"
    local command=$(echo "$input_line" | awk '{print toupper($1)}')
    local args="${input_line#* }"

    case "$command" in
        "VER") cmd_ver "$args" ;;
        "CLS") cmd_cls "$args" ;;
        "HELP") cmd_help "$args" ;;
        "DIR") cmd_dir "$args" ;;
        "CD") cmd_cd "$args" ;;
        "MOUNT") cmd_mount "$args" ;;
        "ECHO") cmd_echo "$args" ;;
        "EDIT") cmd_edit "$args" ;;
        "ABOUT") cmd_about "$args" ;;
        "EXIT") cmd_exit "$args" ;;
        *)
            # Attempt to execute the command as a file/program
            if ! execute_program "$command"; then
                printf "${RED}Bad command or file name: %s${RESET}\n" "$command"
            fi
            ;;
    esac
}

function command_loop() {
    # Ensure the script uses Bash features
    if [ -z "$BASH_VERSION" ]; then
        echo "This script requires Bash."
        exit 1
    fi
    
    # Main input loop
    while true; do
        read -re -p "$PROMPT" input_line
        
        # Strip leading/trailing whitespace and process
        input_line=$(echo "$input_line" | xargs)

        if [[ -z "$input_line" ]]; then
            continue
        fi

        # Process the command
        process_command "$input_line"
    done
}

# --- Execution Start ---
initialize_fs
boot_sequence
command_loop

