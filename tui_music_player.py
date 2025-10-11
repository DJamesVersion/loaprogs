import curses
import time
import os
import subprocess
import glob
import signal
from collections import deque
from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError

# --- CONFIGURATION ---
MUSIC_DIR = '.'  # Look for MP3s in the current directory
PLAYER_COMMAND = 'mpg123'
PROGRESS_BAR_LENGTH = 20

# --- DATA STRUCTURES ---
class Track:
    """Represents a single music track."""
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.artist = 'Unknown Artist'
        self.title = self.filename
        self.duration = 0

        try:
            audio = MP3(filepath)
            self.duration = int(audio.info.length)
            
            # Attempt to get ID3 tags
            if audio.tags:
                self.artist = audio.tags.get('TPE1', ['Unknown Artist'])[0]
                self.title = audio.tags.get('TIT2', [self.filename])[0]
                
        except ID3NoHeaderError:
            pass
        except Exception as e:
            # print(f"Error reading tags for {filepath}: {e}")
            pass

    def __str__(self):
        return f"{self.artist} - {self.title}"

# --- PLAYER CORE LOGIC ---
class Player:
    """Manages the music library, state, and subprocess."""
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.is_running = True
        self.status = "STOPPED" # STOPPED, PLAYING, PAUSED
        self.tracks = self._load_tracks()
        self.current_track_index = 0
        self.player_process = None
        self.start_time = 0
        self.pause_offset = 0

    def _load_tracks(self):
        """Scans the music directory for MP3 files."""
        mp3_files = glob.glob(os.path.join(MUSIC_DIR, '*.mp3'))
        if not mp3_files:
            return deque([Track(f"No .mp3 files found in {MUSIC_DIR}")])
        
        tracks = [Track(f) for f in mp3_files]
        # Use deque for easy rotation (Next/Previous)
        return deque(tracks)

    def get_current_track(self):
        """Returns the currently selected track object."""
        if not self.tracks or self.current_track_index >= len(self.tracks):
            return Track("N/A")
        return self.tracks[self.current_track_index]

    def _calculate_position(self):
        """Calculates the playback position in seconds."""
        if self.status == "PLAYING":
            return self.pause_offset + (time.time() - self.start_time)
        elif self.status == "PAUSED":
            return self.pause_offset
        return 0

    def _format_time(self, seconds):
        """Formats seconds into MM:SS string."""
        minutes = int(seconds) // 60
        seconds = int(seconds) % 60
        return f"{minutes:02d}:{seconds:02d}"

    def get_status_info(self):
        """Returns metadata and time string for display."""
        track = self.get_current_track()
        if track.filepath == "N/A":
             return "No Tracks Loaded", "00:00/00:00", ""

        duration = track.duration
        position = self._calculate_position()
        
        # Prevent position exceeding duration
        if self.status == "PLAYING" and position > duration:
            self.next_track()
            position = 0 # Will reset when new track starts
        elif position > duration:
            position = duration

        time_str = f"{self._format_time(position)}/{self._format_time(duration)}"
        
        # Create progress bar
        if duration > 0:
            progress = int((position / duration) * PROGRESS_BAR_LENGTH)
            progress_bar = "[" + "=" * progress + ">" + "-" * (PROGRESS_BAR_LENGTH - progress - 1) + "]"
        else:
            progress_bar = "[--------------------]"

        return str(track), time_str, progress_bar


    # --- Playback Commands ---

    def play_track(self, index=None):
        """Stops current and starts playing the track at index."""
        if index is not None:
            self.current_track_index = index % len(self.tracks)
        
        if self.status in ["PLAYING", "PAUSED"]:
            self.stop_playback()

        current_track = self.get_current_track()
        if current_track.filepath == "N/A":
            self.status = "STOPPED"
            return
            
        try:
            # Start mpg123 process
            self.player_process = subprocess.Popen(
                [PLAYER_COMMAND, current_track.filepath],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.status = "PLAYING"
            self.start_time = time.time()
            self.pause_offset = 0
        except FileNotFoundError:
            self.status = f"ERROR: '{PLAYER_COMMAND}' not found."
            self.player_process = None
        except Exception as e:
            self.status = f"Playback Error: {e}"
            self.player_process = None

    def pause_playback(self):
        """Toggles pause state."""
        if self.status == "PLAYING" and self.player_process:
            self.player_process.send_signal(signal.SIGSTOP)
            self.pause_offset = self._calculate_position()
            self.status = "PAUSED"
        elif self.status == "PAUSED" and self.player_process:
            self.player_process.send_signal(signal.SIGCONT)
            self.start_time = time.time() # Reset start time for accurate tracking
            self.status = "PLAYING"
        elif self.status == "STOPPED":
            self.play_track()

    def stop_playback(self):
        """Stops the current track."""
        if self.player_process:
            self.player_process.terminate()
            self.player_process.wait()
            self.player_process = None
        self.status = "STOPPED"
        self.start_time = 0
        self.pause_offset = 0

    def next_track(self):
        """Moves to the next track and plays it."""
        self.current_track_index = (self.current_track_index + 1) % len(self.tracks)
        self.play_track()

    def previous_track(self):
        """Moves to the previous track and plays it."""
        self.current_track_index = (self.current_track_index - 1) % len(self.tracks)
        self.play_track()

    def quit_player(self):
        """Cleanly stops playback and exits."""
        self.stop_playback()
        self.is_running = False

# --- TUI DRAWING FUNCTIONS ---

def draw_header(stdscr, max_y, max_x):
    """Draws the application header."""
    header_text = "🎶 TERMUNE: Terminal Music Player 🎶"
    stdscr.addstr(1, (max_x - len(header_text)) // 2, header_text, curses.A_BOLD)
    stdscr.hline(2, 0, curses.ACS_HLINE, max_x)

def draw_status(stdscr, max_y, max_x, player):
    """Draws the status, track info, and progress bar."""
    status_y = 4
    
    # 1. Status and Track Name
    current_status = player.status
    track_name, time_str, progress_bar = player.get_status_info()

    stdscr.addstr(status_y, 2, f"STATUS:", curses.A_BOLD)
    
    status_color = curses.color_pair(3) if current_status == "PLAYING" else curses.color_pair(2)
    stdscr.addstr(status_y, 10, f"{current_status:<8}", status_color)
    
    stdscr.addstr(status_y + 1, 2, f"TRACK:", curses.A_BOLD)
    stdscr.addstr(status_y + 1, 10, f"{track_name[:max_x - 12]}")
    
    # 2. Time and Progress
    stdscr.addstr(status_y + 2, 2, f"TIME:", curses.A_BOLD)
    stdscr.addstr(status_y + 2, 8, time_str)
    
    stdscr.addstr(status_y + 3, 2, f"SEEK:", curses.A_BOLD)
    stdscr.addstr(status_y + 3, 8, progress_bar, curses.color_pair(4))

    # Line separator
    stdscr.hline(status_y + 4, 0, curses.ACS_HLINE, max_x)


def draw_playlist(stdscr, max_y, max_x, player):
    """Draws the scrollable playlist."""
    list_y_start = 6
    list_height = max_y - list_y_start - 3 # Reserve space for footer
    
    current_index = player.current_track_index
    tracks = player.tracks
    
    # Simple fixed window display
    for i in range(list_height):
        list_y = list_y_start + i
        if i >= len(tracks):
            break

        track_index = i
        track = tracks[track_index]

        display_text = f"[{track_index + 1:2d}] {track.filename}"
        
        # Truncate text
        display_text = display_text[:max_x - 4]
        
        attr = curses.A_NORMAL
        if track_index == current_index:
            attr |= curses.A_REVERSE
            if player.status == "PLAYING":
                attr |= curses.color_pair(3) # Green if playing

        stdscr.addstr(list_y, 2, display_text, attr)
        
    stdscr.hline(list_y_start + list_height, 0, curses.ACS_HLINE, max_x)


def draw_footer(stdscr, max_y, max_x):
    """Draws the control hints at the bottom."""
    footer_text = "Controls: P:Play/Pause N:Next B:Prev Q:Quit | ⬆/⬇:Scroll | Enter:Select"
    stdscr.addstr(max_y - 1, (max_x - len(footer_text)) // 2, footer_text, curses.A_BOLD)

# --- MAIN CURSES LOOP ---

def curses_main(stdscr):
    """Initializes curses, sets up colors, and runs the main loop."""
    
    # Setup Colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK) # Default
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Paused/Warn
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Playing/Success
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Progress

    stdscr.nodelay(True) # Non-blocking input
    stdscr.timeout(100)  # Refresh every 100ms
    stdscr.clear()

    player = Player(stdscr)

    while player.is_running:
        # Get screen dimensions
        try:
            max_y, max_x = stdscr.getmaxyx()
        except:
            # Handle terminal resize race conditions
            continue

        stdscr.clear()

        # 1. Draw UI elements
        draw_header(stdscr, max_y, max_x)
        draw_status(stdscr, max_y, max_x, player)
        draw_playlist(stdscr, max_y, max_x, player)
        draw_footer(stdscr, max_y, max_x)

        # 2. Process Input
        try:
            key = stdscr.getch()
        except:
            key = -1 # No key pressed

        if key != -1:
            try:
                char = chr(key).lower()
            except ValueError:
                char = None

            if char == 'q':
                player.quit_player()
            elif char == 'p':
                player.pause_playback()
            elif char == 'n':
                player.next_track()
            elif char == 'b':
                player.previous_track()
            elif key == curses.KEY_UP:
                player.current_track_index = max(0, player.current_track_index - 1)
            elif key == curses.KEY_DOWN:
                player.current_track_index = min(len(player.tracks) - 1, player.current_track_index + 1)
            elif key == 10: # Enter key
                if player.status == "PLAYING" and player.get_current_track().filepath == player.tracks[player.current_track_index].filepath:
                    # If already playing the selected track, stop it
                    player.stop_playback()
                else:
                    # Otherwise, play the selected track
                    player.play_track(player.current_track_index)

        # 3. Check if the currently playing process has finished
        if player.status == "PLAYING" and player.player_process:
            # Check for termination/completion
            if player.player_process.poll() is not None:
                if player.player_process.returncode == 0:
                    # Track finished successfully
                    player.next_track()
                else:
                    # Track failed to play (e.g., corrupted file)
                    player.stop_playback()
                    player.status = "Error playing file."
            
        stdscr.refresh()

if __name__ == '__main__':
    # Initial checks to avoid silent failures
    if not glob.glob('*.mp3'):
        print(f"TERMINAL MUSIC PLAYER SETUP: No .mp3 files found in {MUSIC_DIR}. Please place some files here.")
        print("Exiting...")
    elif not os.path.exists('/usr/bin/mpg123') and not os.path.exists('/usr/local/bin/mpg123'):
        print("DEPENDENCY CHECK FAILED:")
        print("The 'mpg123' executable was not found. Please install it using your system's package manager.")
        print("Example: 'sudo apt install mpg123' or 'brew install mpg123'")
        print("Exiting...")
    else:
        try:
            curses.wrapper(curses_main)
        except curses.error as e:
            print(f"A curses error occurred (likely terminal size or compatibility): {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

