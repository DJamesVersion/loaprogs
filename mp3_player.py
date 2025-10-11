import subprocess
import sys
import os

# --- Configuration ---
MP3_FILE_NAME = "audio.mp3"
DEFAULT_MESSAGE = "Check your desktop or console for the audio player."

def play_audio(filepath):
    """
    Plays the specified audio file using a platform-appropriate command.
    """
    platform = sys.platform

    if not os.path.exists(filepath):
        print(f"\n[ERROR] File not found: '{filepath}'")
        print("Please ensure your MP3 file is in the same directory and named exactly 'audio.mp3'.")
        return

    command = None
    player_note = ""

    # 1. Determine the command based on the operating system
    if platform.startswith('win'):
        # Windows: Use 'start' to open the file with the default media player
        command = ['start', '', filepath]
        player_note = "Using Windows 'start' command."
    elif platform.startswith('darwin'):
        # macOS: Use 'afplay' (built-in command line audio player)
        command = ['afplay', filepath]
        player_note = "Using macOS 'afplay' command."
    elif platform.startswith('linux'):
        # Linux: Try 'mpg123' first, then 'aplay' or 'xdg-open'
        # mpg123 is excellent for MP3s but often requires installation.
        command = ['mpg123', filepath]
        player_note = "Using Linux 'mpg123' command (may require installation)."
    else:
        print(f"[ERROR] Unsupported platform: {platform}")
        return

    print("=======================================")
    print("      Python Command-Line Player       ")
    print("=======================================")
    print(f"Platform Detected: {player_note}")
    print(f"Attempting to play: {filepath}")
    print(f"Executing: {' '.join(command)}")

    # 2. Execute the command
    try:
        # Use subprocess.Popen for non-blocking execution (especially on Windows/macOS)
        # On Linux, mpg123 will block unless we run it in the background, but this is simpler.
        # The 'start' command on Windows and 'afplay' on macOS generally allow the script to continue.
        subprocess.Popen(command, shell=(platform.startswith('win')))
        print(f"\nSuccess! {DEFAULT_MESSAGE}")

    except FileNotFoundError:
        # This occurs if the command itself (e.g., 'mpg123' or 'afplay') is not found
        print("\n[ERROR] Playback utility not found.")
        if platform.startswith('linux'):
            print("If you are on Linux, ensure 'mpg123' is installed (e.g., 'sudo apt install mpg123').")
        print("Please verify your system's required audio playback tools are accessible.")
    except Exception as e:
        print(f"\n[CRITICAL ERROR] Failed to execute playback command: {e}")

if __name__ == "__main__":
    # Get the directory of the script and construct the full path to the MP3 file
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    audio_path = os.path.join(script_dir, MP3_FILE_NAME)
    
    play_audio(audio_path)

