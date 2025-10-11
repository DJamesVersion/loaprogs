import sys
import time
import random
import select

# --- Terminal Setup for Non-Blocking Input (Crucial for Unix-like systems) ---
# This setup allows the script to read single keypresses immediately without waiting for Enter.
try:
    import tty
    import termios
    _original_settings = termios.tcgetattr(sys.stdin)
    _termios_available = True
except ImportError:
    _termios_available = False

def enable_raw_mode():
    """Sets the terminal to raw mode for non-blocking, single-character input."""
    if _termios_available:
        tty.setraw(sys.stdin)

def disable_raw_mode():
    """Restores the terminal to its original settings."""
    if _termios_available:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, _original_settings)

def is_input_waiting():
    """Checks if a key has been pressed without blocking."""
    # select.select checks for read readiness on file descriptors
    return sys.stdin in select.select([sys.stdin], [], [], 0)[0]

def get_input_char():
    """Reads a single character if available, otherwise returns None."""
    if _termios_available and is_input_waiting():
        # Read a single byte/character
        return sys.stdin.read(1)
    return None

def clear_screen():
    """Clears the console screen and moves cursor to home position using ANSI codes."""
    sys.stdout.write("\033[H\033[J")

# --- Maze Generation Logic (Depth First Search) ---

def generate_maze(width, height):
    """
    Generates a perfect maze using a randomized Depth First Search (DFS) algorithm.
    The grid size must be odd for proper wall/path separation (e.g., 31x15).
    """
    # Initialize grid with all walls ('#')
    maze = [['#' for _ in range(width)] for _ in range(height)]
    visited = set()
    stack = []

    # Start point (must be an odd-numbered cell)
    start_x, start_y = 1, 1
    maze[start_y][start_x] = ' ' # Clear the starting path
    visited.add((start_x, start_y))
    stack.append((start_x, start_y))

    while stack:
        cx, cy = stack[-1]
        neighbors = []

        # Define potential moves (2 cells away, skipping one wall)
        # (dx, dy, wall_dx, wall_dy)
        directions = [
            (2, 0, 1, 0),  # Right
            (-2, 0, -1, 0), # Left
            (0, 2, 0, 1),  # Down
            (0, -2, 0, -1) # Up
        ]
        random.shuffle(directions)

        for dx, dy, wdx, wdy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 < nx < width - 1 and 0 < ny < height - 1 and (nx, ny) not in visited:
                neighbors.append((nx, ny, wdx, wdy))

        if neighbors:
            nx, ny, wdx, wdy = random.choice(neighbors)

            # 1. Knock down the wall between current and neighbor
            maze[cy + wdy][cx + wdx] = ' '
            # 2. Open the neighbor path
            maze[ny][nx] = ' '
            # 3. Move to the neighbor
            visited.add((nx, ny))
            stack.append((nx, ny))
        else:
            # Backtrack
            stack.pop()

    # Set Start (S) and End (E) points
    # Start: Top-left path (1, 1)
    maze[1][1] = 'S'
    # End: Bottom-right path (width - 2, height - 2)
    maze[height - 2][width - 2] = 'E'

    return maze, 1, 1, width - 2, height - 2 # Returns maze, start_x, start_y, end_x, end_y

# --- Game State and Loop ---

def draw_game(maze, player_x, player_y, message):
    """Renders the maze and the player."""
    output = ""
    # Header
    output += "=" * (len(maze[0]) + 2) + "\n"
    output += f"| {message.ljust(len(maze[0]))} |\n"
    output += "=" * (len(maze[0]) + 2) + "\n"

    for y, row in enumerate(maze):
        output += "|"
        for x, char in enumerate(row):
            if x == player_x and y == player_y:
                output += "@" # Player symbol
            else:
                output += char
        output += "|\n"

    # Footer
    output += "=" * (len(maze[0]) + 2) + "\n"
    output += "Controls: W/A/S/D to move. Q to Quit.\n"
    output += "Find the 'E' to win!\n"

    sys.stdout.write(output)
    sys.stdout.flush()

def main():
    """Main function to run the maze game."""
    # Define maze dimensions (must be odd numbers)
    MAZE_WIDTH = 31
    MAZE_HEIGHT = 15
    FRAME_DELAY = 0.05

    print("Initializing landofages Terminal Maze...")
    if not _termios_available:
         print("WARNING: Non-blocking input is not available on this system.")
         print("You must press ENTER after every key press (W/A/S/D/Q).")
    time.sleep(1)

    try:
        # Generate the maze and get initial positions
        maze, px, py, goal_x, goal_y = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)
        player_x, player_y = px, py
        game_over = False
        game_message = "Move to find the exit 'E'!"

        enable_raw_mode()
        clear_screen()

        while not game_over:
            start_time = time.time()
            dx, dy = 0, 0
            
            # --- Handle Input ---
            key = get_input_char()
            if key is not None:
                key = key.lower()
                if key == 'q':
                    game_over = True
                    game_message = "Quitting game..."
                    break

                if key == 'w': dy = -1
                elif key == 's': dy = 1
                elif key == 'a': dx = -1
                elif key == 'd': dx = 1

            # --- Update Player Position (Collision Detection) ---
            if dx != 0 or dy != 0:
                new_x, new_y = player_x + dx, player_y + dy
                
                # Check bounds and if the next cell is a wall ('#')
                if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT:
                    target_cell = maze[new_y][new_x]

                    if target_cell != '#':
                        player_x, player_y = new_x, new_y
                        game_message = "Keep going!"
                    else:
                        game_message = "Ouch! That's a wall."

            # --- Check Win Condition ---
            if player_x == goal_x and player_y == goal_y:
                game_over = True
                game_message = "!!! VICTORY! YOU FOUND THE EXIT 'E' !!!"

            # --- Draw Game ---
            draw_game(maze, player_x, player_y, game_message)

            # Maintain frame rate
            elapsed_time = time.time() - start_time
            sleep_time = FRAME_DELAY - elapsed_time
            if sleep_time > 0:
                time.sleep(sleep_time)

    except Exception as e:
        print(f"\nAn error occurred: {e}", file=sys.stderr)
    finally:
        # ALWAYS restore the terminal settings on exit
        disable_raw_mode()
        clear_screen()
        # Final message ensures the user sees the result after cleaning the screen
        print(f"\nGame Ended. {game_message}\n")

if __name__ == "__main__":
    main()

