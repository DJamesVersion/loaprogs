import sys
import time
import random
import select

# --- Terminal Setup for Non-Blocking Input (Required for Unix-like systems) ---
# This part is crucial for allowing the game to read input without pausing (non-blocking).
# We attempt to import necessary modules to change terminal settings.

try:
    import tty
    import termios
    # Save the original terminal settings to restore them later
    _original_settings = termios.tcgetattr(sys.stdin)
except ImportError:
    # If the system doesn't have termios (e.g., Windows), we fall back to blocking input
    _termios_available = False
else:
    _termios_available = True

def enable_raw_mode():
    """Sets the terminal to raw mode for non-blocking, single-character input."""
    if _termios_available:
        # tty.setraw() sets the terminal in a mode where characters are available one by one
        # without waiting for the Enter key.
        tty.setraw(sys.stdin)

def disable_raw_mode():
    """Restores the terminal to its original settings."""
    if _termios_available:
        # Restore the original settings upon exiting
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
    elif not _termios_available:
        # Fallback for systems without termios (will block)
        # This will make the game very slow, as you must press ENTER after every key.
        return input("Move (W/S/I/J/K/M, Q to quit): ").lower()
    return None

# --- Game Constants ---
COURT_WIDTH = 60
COURT_HEIGHT = 20
PADDLE_HEIGHT = 4
PADDLE_X_OFFSET = 3
FRAME_RATE = 0.05  # Delay between frames (20 frames per second)
WINNING_SCORE = 5

# --- Game State ---
ball_x = COURT_WIDTH // 2
ball_y = COURT_HEIGHT // 2
# Random initial direction
ball_dx = random.choice([-1, 1])
ball_dy = random.uniform(-0.8, 0.8) # Allow for vertical angle

# Paddle Y positions (top edge)
left_paddle_y = COURT_HEIGHT // 2 - PADDLE_HEIGHT // 2
right_paddle_y = COURT_HEIGHT // 2 - PADDLE_HEIGHT // 2

score_left = 0
score_right = 0
game_over = False

# --- Core Game Functions ---

def clear_screen():
    """Clears the console screen and moves cursor to home position using ANSI codes."""
    # \033[H\033[J are standard ANSI escape codes for clearing the screen
    sys.stdout.write("\033[H\033[J")

def draw_game():
    """Renders the entire game state (court, paddles, ball) to the console."""
    # Top border
    output = " " + ("=" * (COURT_WIDTH + 2)) + "\n"

    # Middle part (court, paddles, ball)
    for y in range(COURT_HEIGHT):
        row = "|"
        for x in range(COURT_WIDTH):
            is_left_paddle = (x == PADDLE_X_OFFSET and
                              y >= left_paddle_y and
                              y < left_paddle_y + PADDLE_HEIGHT)
            is_right_paddle = (x == COURT_WIDTH - 1 - PADDLE_X_OFFSET and
                               y >= right_paddle_y and
                               y < right_paddle_y + PADDLE_HEIGHT)
            is_ball = (x == int(ball_x) and y == int(ball_y))

            if is_left_paddle or is_right_paddle:
                row += "#"  # Paddle
            elif is_ball:
                row += "O"  # Ball
            elif x == COURT_WIDTH // 2:
                row += ":"  # Center divider
            else:
                row += " "  # Empty space
        row += "|\n"
        output += row

    # Bottom border
    output += " " + ("=" * (COURT_WIDTH + 2)) + "\n"

    # Scoreboard and Controls
    output += f"  P1 Score: {score_left:<4} | P2 Score: {score_right:>4} \n"
    output += "  Controls: P1 (W/S), P2 (I/J for Up/Down) | Q to Quit\n"
    output += f"  First to {WINNING_SCORE} wins!\n"

    sys.stdout.write(output)
    sys.stdout.flush() # Display the output immediately

def reset_ball(direction):
    """Resets the ball to the center and gives it a new direction."""
    global ball_x, ball_y, ball_dx, ball_dy

    # Reset position
    ball_x = COURT_WIDTH // 2
    ball_y = COURT_HEIGHT // 2

    # Set initial horizontal direction and reset speed
    ball_dx = direction * 1
    # Set a small random vertical direction
    ball_dy = random.uniform(-0.8, 0.8)

def update_ball():
    """Updates the ball's position and handles collisions."""
    global ball_x, ball_y, ball_dx, ball_dy, score_left, score_right

    # 1. Update Position
    ball_x += ball_dx
    ball_y += ball_dy

    # 2. Check for Top/Bottom Wall Collision
    if ball_y <= 0 or ball_y >= COURT_HEIGHT - 1:
        ball_dy *= -1
        # Clamp ball position to prevent sticking on the border
        if ball_y < 0: ball_y = 0
        if ball_y > COURT_HEIGHT - 1: ball_y = COURT_HEIGHT - 1

    # 3. Check for Paddle Collision (Left Player)
    if ball_dx < 0 and int(ball_x) == PADDLE_X_OFFSET + 1:
        if left_paddle_y <= ball_y < left_paddle_y + PADDLE_HEIGHT:
            ball_dx *= -1.02 # Reverse direction and slightly increase speed
            ball_dx = min(ball_dx, 2.0) # Cap speed
            # Angle change: vertical velocity is adjusted based on where the ball hits the paddle
            hit_relative = (ball_y - left_paddle_y) / PADDLE_HEIGHT
            ball_dy = (hit_relative - 0.5) * 2 * abs(ball_dy) # Makes the bounce steeper near the edges
            ball_y = int(ball_y) # Ensure y is an integer for clean rendering

    # 4. Check for Paddle Collision (Right Player)
    if ball_dx > 0 and int(ball_x) == COURT_WIDTH - 2 - PADDLE_X_OFFSET:
        if right_paddle_y <= ball_y < right_paddle_y + PADDLE_HEIGHT:
            ball_dx *= -1.02 # Reverse direction and slightly increase speed
            ball_dx = max(ball_dx, -2.0) # Cap speed
            # Angle change
            hit_relative = (ball_y - right_paddle_y) / PADDLE_HEIGHT
            ball_dy = (hit_relative - 0.5) * 2 * abs(ball_dy) * -1 # Multiplied by -1 to keep physics consistent
            ball_y = int(ball_y) # Ensure y is an integer for clean rendering

    # 5. Check for Goal (Scoring)
    goal = False
    if ball_x < 0:
        score_right += 1
        reset_ball(direction=1) # Send to the right
        goal = True
    elif ball_x >= COURT_WIDTH:
        score_left += 1
        reset_ball(direction=-1) # Send to the left
        goal = True

    return goal

def handle_input():
    """Reads non-blocking input and moves the paddles."""
    global left_paddle_y, right_paddle_y, game_over

    key = get_input_char()

    if key is not None:
        key = key.lower()
        # Quit
        if key == 'q':
            game_over = True
            return

        # Player 1 (Left) Controls
        if key == 'w' and left_paddle_y > 0:
            left_paddle_y -= 1
        elif key == 's' and left_paddle_y < COURT_HEIGHT - PADDLE_HEIGHT:
            left_paddle_y += 1

        # Player 2 (Right) Controls (using I/J or K/M as proxies for Up/Down)
        if (key == 'i' or key == 'k') and right_paddle_y > 0:
            right_paddle_y -= 1
        elif (key == 'j' or key == 'm') and right_paddle_y < COURT_HEIGHT - PADDLE_HEIGHT:
            right_paddle_y += 1


def main():
    """Main game loop for landofages ping pong."""
    print("Initializing landofages Terminal Ping Pong...")
    print(f"Goal: First player to reach {WINNING_SCORE} points wins.")
    print("Press 'Q' to quit anytime.")
    if _termios_available:
        print("Controls: P1 (W/S), P2 (I/J for Up/Down). Input is non-blocking for smooth play.")
    else:
        print("Note: Non-blocking input not fully supported. You must press ENTER after each key stroke.")
    time.sleep(2)

    try:
        # Set terminal to raw mode for smooth input
        enable_raw_mode()
        clear_screen()

        global game_over, score_left, score_right

        while not game_over:
            start_time = time.time()

            handle_input()
            update_ball()
            draw_game()

            # Check for win condition
            if score_left >= WINNING_SCORE or score_right >= WINNING_SCORE:
                game_over = True
                break

            # Maintain frame rate by calculating sleep time
            elapsed_time = time.time() - start_time
            sleep_time = FRAME_RATE - elapsed_time
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        # Exit gracefully on Ctrl+C
        game_over = True
    finally:
        # ALWAYS restore the terminal settings on exit
        disable_raw_mode()
        clear_screen()

        # Final Scoreboard Message
        final_message = ""
        if score_left > score_right:
            final_message = f"*** Player 1 Wins! Final Score: {score_left} - {score_right} ***"
        elif score_right > score_left:
            final_message = f"*** Player 2 Wins! Final Score: {score_left} - {score_right} ***"
        else:
            final_message = "Game Over. It was a draw!"

        print("\n\n" + "=" * len(final_message))
        print(final_message)
        print("=" * len(final_message) + "\n\n")

if __name__ == "__main__":
    main()

