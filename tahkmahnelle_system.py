import os
import time

# --- ANSI COLOR CODES ---
class Color:
    SUN = '\033[93m'       # Yellow for the sun
    PLANET_HAB = '\033[92m'  # Green for habitable planets
    PLANET_UNHAB = '\033[91m' # Red for uninhabitable planets
    DWARF = '\033[96m'     # Cyan for the secret dwarf planet
    TEXT = '\033[97m'      # White for general text
    RESET = '\033[0m'      # Reset color

def clear_screen():
    """Clears the terminal for a clean display."""
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_system(planets):
    """
    Renders the Tahkmahnelle Solar System using ASCII art and colors.
    """
    clear_screen()
    
    # Title
    print(Color.TEXT + "="*60 + Color.RESET)
    print(Color.TEXT + "{:^60}".format("TAHKMAHNELLE SOLAR SYSTEM EDICT") + Color.RESET)
    print(Color.TEXT + "="*60 + Color.RESET)
    print("\n")

    # The Sun (Centerpiece)
    print(" " * 30 + Color.SUN + "  (🌞)" + Color.RESET)
    print(" " * 30 + Color.SUN + "TAHKMAHNELLE" + Color.RESET)
    print(" " * 30 + Color.SUN + "  (★)" + Color.RESET)
    print("\n" * 2)

    # Display Planets in Orbit Rows
    
    # List to hold the formatted output for each planet
    planet_lines = []

    for name, conditions, color in planets:
        status_symbol = "✅" if "Habitable" in conditions else "❌"
        line = (
            f"   {status_symbol}  "
            f"{color}{name: <25}{Color.RESET} "
            f"[{conditions}]"
        )
        planet_lines.append(line)

    # --- Render the orbits and planets ---

    # Orbital Row 1 (Planets 1, 2)
    # The longest orbit line (used to ensure separation)
    row1_line = " " * 15 + Color.TEXT + "---" + Color.RESET + " " * 20
    
    print(planet_lines[0] + row1_line + planet_lines[1])
    print("\n" * 1)
    
    # Orbital Row 2 (Planets 3, 4)
    row2_line = " " * 10 + Color.TEXT + "------" + Color.RESET + " " * 15
    print(planet_lines[2] + row2_line + planet_lines[3])
    print("\n" * 1)

    # Orbital Row 3 (Planets 5, 6)
    row3_line = " " * 5 + Color.TEXT + "---------" + Color.RESET + " " * 10
    print(planet_lines[4] + row3_line + planet_lines[5])
    print("\n" * 1)

    # Orbital Row 4 (Planet 7)
    # Dwarf planet is secret, so it's placed outside the main orbit display
    print(" " * 10 + planet_lines[6])
    print("\n" * 1)
    
    # Dwarf Planet (Secret)
    print(Color.DWARF + " " * 40 + "(●) TAHKMAHNELLE45 (Secret Dwarf Planet - Habitable)" + Color.RESET)
    print("\n" * 2)

    print(Color.TEXT + "-"*60 + Color.RESET)
    print(Color.TEXT + "Key: {}Habitable{} | {}Uninhabitable{} | {}Secret{}".format(
        Color.PLANET_HAB, Color.TEXT, Color.PLANET_UNHAB, Color.TEXT, Color.DWARF, Color.TEXT) + Color.RESET)
    print(Color.TEXT + "-"*60 + Color.RESET)
    print("Press ENTER to refresh or 'q' to quit.")


def tahkmahnelle_solar_system_app():
    """
    The main application loop.
    """
    
    # --- Planet Data ---
    # (Name, Conditions, Color Code)
    planets = [
        # Planet 1 (Unhabitable)
        ("1: lenemketobontette", "Uninhabitable", Color.PLANET_UNHAB),
        # Planet 2 (Habitable)
        ("2: stihuu", "Habitable", Color.PLANET_HAB),
        # Planet 3 (Habitable)
        ("3: tetnobautte", "Habitable", Color.PLANET_HAB),
        # Planet 4 (Habitable)
        ("4: vraelvrae", "Habitable", Color.PLANET_HAB),
        # Planet 5 (Unhabitable)
        ("5: lenemketobontettestihuu", "Uninhabitable", Color.PLANET_UNHAB),
        # Planet 6 (Unhabitable)
        ("6: stihuutetnobautte", "Uninhabitable", Color.PLANET_UNHAB),
        # Planet 7 (Unhabitable)
        ("7: tetnobauttestihuu", "Uninhabitable", Color.PLANET_UNHAB),
    ]

    while True:
        draw_system(planets)
        
        # User input to control the display
        user_input = input(Color.TEXT + "Command: " + Color.RESET).strip().lower()
        
        if user_input == 'q':
            clear_screen()
            print("Solar System display closed.")
            break
        elif user_input == '':
            # Refresh (sleep for a moment to simulate a cycle)
            time.sleep(0.5)
        else:
            print("Invalid command.")
            time.sleep(1)

if __name__ == "__main__":
    tahkmahnelle_solar_system_app()
