#!/bin/bash

# --- Unix Terminal Jukebox using mpg123 ---

# Configuration
PLAYER_BIN="mpg123"
PLAYLIST_DIR=""
CURRENT_TRACK_INDEX=-1
PLAYER_PID=""

# --- Helper Functions ---

# Function to stop any currently running mpg123 instance
stop_playback() {
    if [ -n "$PLAYER_PID" ]; then
        # Check if the process is still running
        if kill -0 "$PLAYER_PID" 2>/dev/null; then
            echo "[INFO] Stopping track (PID $PLAYER_PID)..."
            kill "$PLAYER_PID" 2>/dev/null
        fi
        PLAYER_PID=""
    fi
}

# Function to clear the screen and display the header/status
display_menu() {
    clear
    echo "======================================================"
    echo "          U N I X   T E R M I N A L   J U K E B O X"
    echo "======================================================"

    if [ ${#PLAYLIST[@]} -eq 0 ]; then
        echo "STATUS: NO PLAYLIST LOADED"
        echo "DIRECTORY: Not set"
        echo "------------------------------------------------------"
    else
        STATUS="STOPPED"
        CURRENT_TRACK_NAME="N/A"
        
        # Determine playback status and current track name
        if [ -n "$PLAYER_PID" ] && kill -0 "$PLAYER_PID" 2>/dev/null; then
            STATUS="PLAYING"
            # Extract only the filename from the path for display
            CURRENT_TRACK_NAME=$(basename "${PLAYLIST[$CURRENT_TRACK_INDEX]}")
        fi
        
        echo "STATUS: $STATUS | TOTAL TRACKS: ${#PLAYLIST[@]}"
        echo "CURRENT TRACK: [$(($CURRENT_TRACK_INDEX + 1))] $CURRENT_TRACK_NAME"
        echo "DIRECTORY: $PLAYLIST_DIR"
        echo "------------------------------------------------------"
    fi

    echo "COMMANDS:"
    echo "  [L]oad Directory    | [P]lay Selected Track"
    echo "  [S]top              | [N]ext / [B]ack"
    echo "  [#] Track Number    | [Q]uit"
    echo "------------------------------------------------------"
}

# Function to load MP3 files from a user-specified directory
load_directory() {
    stop_playback
    
    read -p "Enter the path to your MP3 directory: " DIR_INPUT
    
    if [ -d "$DIR_INPUT" ]; then
        PLAYLIST_DIR="$DIR_INPUT"
        # Find all .mp3 files (case-insensitive) and store them in the PLAYLIST array
        mapfile -t PLAYLIST < <(find "$PLAYLIST_DIR" -maxdepth 1 -type f \( -iname "*.mp3" \) | sort)
        
        if [ ${#PLAYLIST[@]} -eq 0 ]; then
            echo "[ERROR] No MP3 files found in '$PLAYLIST_DIR'."
            CURRENT_TRACK_INDEX=-1
        else
            echo "[SUCCESS] Loaded ${#PLAYLIST[@]} tracks."
            CURRENT_TRACK_INDEX=0 # Select the first track by default
        fi
    else
        echo "[ERROR] Directory '$DIR_INPUT' not found."
        PLAYLIST_DIR=""
        PLAYLIST=()
        CURRENT_TRACK_INDEX=-1
    fi
    sleep 1
}

# Function to play a track by index
play_track() {
    local INDEX=$1
    
    if [ "$INDEX" -ge 0 ] && [ "$INDEX" -lt ${#PLAYLIST[@]} ]; then
        stop_playback # Stop current track before playing new one
        CURRENT_TRACK_INDEX=$INDEX
        TRACK_PATH="${PLAYLIST[$CURRENT_TRACK_INDEX]}"
        TRACK_NAME=$(basename "$TRACK_PATH")

        echo "[PLAYING] $TRACK_NAME"
        
        # Start mpg123 in the background and capture its PID
        "$PLAYER_BIN" -q "$TRACK_PATH" &
        PLAYER_PID=$!
        
    else
        echo "[ERROR] Invalid track index: $INDEX"
    fi
    sleep 1
}

# Function to automatically advance the track if the player process finishes
auto_advance() {
    # Check if a player process ID exists
    if [ -n "$PLAYER_PID" ]; then
        # Check if the process is no longer running (mpg123 finished)
        if ! kill -0 "$PLAYER_PID" 2>/dev/null; then
            echo "[ENDED] Track finished. Auto-advancing..."
            PLAYER_PID=""
            local NEXT_INDEX=$(($CURRENT_TRACK_INDEX + 1))
            
            # Wrap around to the beginning if we hit the end
            if [ "$NEXT_INDEX" -ge ${#PLAYLIST[@]} ]; then
                NEXT_INDEX=0
            fi
            
            # If the playlist is not empty, play the next track
            if [ ${#PLAYLIST[@]} -gt 0 ]; then
                 play_track "$NEXT_INDEX"
            fi
        fi
    fi
}

# --- Main Jukebox Loop ---

# Check for mpg123 availability
if ! command -v "$PLAYER_BIN" &> /dev/null; then
    echo "[CRITICAL ERROR] The required player '$PLAYER_BIN' could not be found."
    echo "Please install it using your distribution's package manager (e.g., 'sudo apt-get install mpg123')."
    exit 1
fi

load_directory # Start by prompting the user to load a directory

while true; do
    # 1. Check if the current track has finished and advance if necessary
    auto_advance
    
    # 2. Display the current state and menu
    display_menu
    
    # 3. Read user command
    read -p "Enter command or track #: " CMD

    case "$CMD" in
        [Ll]*) # Load new directory
            load_directory
            ;;

        [Qq]*) # Quit
            stop_playback
            echo "Shutting down Jukebox. Goodbye!"
            exit 0
            ;;

        [Ss]*) # Stop playback
            stop_playback
            ;;

        [Pp]*) # Play current track
            if [ ${#PLAYLIST[@]} -gt 0 ]; then
                play_track "$CURRENT_TRACK_INDEX"
            else
                echo "[ERROR] Playlist is empty. Use [L]oad first."
            fi
            ;;

        [Nn]*) # Next track
            if [ ${#PLAYLIST[@]} -gt 0 ]; then
                NEXT_INDEX=$(($CURRENT_TRACK_INDEX + 1))
                if [ "$NEXT_INDEX" -ge ${#PLAYLIST[@]} ]; then
                    NEXT_INDEX=0 # Wrap around
                fi
                play_track "$NEXT_INDEX"
            else
                echo "[ERROR] Playlist is empty."
            fi
            ;;

        [Bb]*) # Back (Previous) track
            if [ ${#PLAYLIST[@]} -gt 0 ]; then
                PREV_INDEX=$(($CURRENT_TRACK_INDEX - 1))
                if [ "$PREV_INDEX" -lt 0 ]; then
                    PREV_INDEX=$((${#PLAYLIST[@]} - 1)) # Wrap around
                fi
                play_track "$PREV_INDEX"
            else
                echo "[ERROR] Playlist is empty."
            fi
            ;;

        [0-9]*) # Select track by number
            INPUT_INDEX=$(($CMD - 1))
            if [ ${#PLAYLIST[@]} -gt 0 ]; then
                play_track "$INPUT_INDEX"
            else
                echo "[ERROR] Playlist is empty. Cannot select track."
            fi
            ;;
        
        *)
            # Ignore empty or unknown commands
            if [ -n "$CMD" ]; then
                echo "[ERROR] Unknown command: $CMD"
            fi
            ;;
    esac
    
    # Wait briefly to prevent rapid loop cycling
    sleep 0.1
done

