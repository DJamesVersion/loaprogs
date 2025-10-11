import time
import datetime
import math
import os
import sys

# --- Tahkmahnelle Linguistic Database (LoA Index) ---

# The 26 Primal Roots (Tkemnâti) which also name the cycles and periods of significance.
TAHKMAHNELLE_DICTIONARY = {
    'a': {'root': 'ariatnah', 'meaning': 'Root for \'Beginning,\' \'Dawn,\' or \'First Light.\'', 'age': 'The Age of Genesis'},
    'b': {'root': 'batobwatchaeh', 'meaning': 'Root for \'Unfurling,\' \'Expansion,\' or \'To Become Vast.\'', 'age': 'The Age of Growth'},
    'c': {'root': "c'illiatnah", 'meaning': 'Root for \'Consciousness,\' \'Inner Gaze,\' or \'Self-Awareness.\'', 'age': 'The Age of Sentience'},
    'd': {'root': 'diadowatchaeh', 'meaning': 'Root for \'Structure,\' \'Foundation,\' or \'Binding Law.\'', 'age': 'The Age of Order'},
    'e': {'root': 'eecheechuwah', 'meaning': 'Root for \'Flow,\' \'River,\' or \'Eternal Motion.\'', 'age': 'The Age of Continuity'},
    'f': {'root': "f'illianarre", 'meaning': 'Root for \'Covenant,\' \'Sacred Duty,\' or \'Bound by Oath.\'', 'age': 'The Age of Oaths'},
    'g': {'root': 'gagoikenne', 'meaning': 'Root for \'Gathering,\' \'Assembly,\' or \'Community.\'', 'age': 'The Age of Alliance'},
    'h': {'root': "h'uilliatachaeh", 'meaning': 'Root for \'Echo,\' \'Reflection,\' or \'Memory of the Past.\'', 'age': 'The Age of Precedent'},
    'i': {'root': 'illianarre', 'meaning': 'Root for \'Truth,\' \'Unveiling,\' or \'Revelation.\'', 'age': 'The Age of Clarity'},
    'j': {'root': 'ampejinne', 'meaning': 'Root for \'Intervention,\' \'Sudden Change,\' or \'Catalyst.\'', 'age': 'The Age of Catalyst'},
    'k': {'root': 'kajoinkenne', 'meaning': 'Root for \'Harmony,\' \'Balance,\' or \'The Midpoint.\'', 'age': 'The Age of Zenith'},
    'l': {'root': 'lenemketobontette', 'meaning': 'Root for \'Long Journey,\' \'Exile,\' or \'Wandering.\'', 'age': 'The Age of Passage'},
    'm': {'root': 'momaw', 'meaning': 'Root for \'Sustenance,\' \'Nourishment,\' or \'The Mother Principle.\'', 'age': 'The Age of Life'},
    'n': {'root': 'nona, nano', 'meaning': 'Root for \'Negation,\' \'Void,\' or \'The Absence.\'', 'age': 'The Age of Silence'},
    'o': {'root': 'oichenne', 'meaning': 'Root for \'Wisdom,\' \'Deep Understanding,\' or \'Enlightenment.\'', 'age': 'The Age of Enlightenment'},
    'p': {'root': 'perfuvium', 'meaning': 'Root for \'Scattering,\' \'Fragmentation,\' or \'Dispersion.\'', 'age': 'The Age of Diaspora'},
    'q': {'root': 'quaristenne', 'meaning': 'Root for \'Question,\' \'The Search,\' or \'Inquiry.\'', 'age': 'The Age of Inquiry'},
    'r': {'root': 'roykenne', 'meaning': 'Root for \'Return,\' \'Recurrence,\' or \'The Cycle.\'', 'age': 'The Age of Cycles'},
    's': {'root': 'stihuu, siataeh', 'meaning': 'Root for \'Vibration,\' \'Sound,\' or \'Spoken Word.\'', 'age': 'The Age of Voice'},
    't': {'root': 'tetnobautte, tahkmahnelle', 'meaning': 'Root for \'Governance,\' \'System,\' or \'The People/Culture.\'', 'age': 'The Age of Culture'},
    'u': {'root': 'uilliatachaeh', 'meaning': 'Root for \'Vision,\' \'Foresight,\' or \'The Future.\'', 'age': 'The Age of Destiny'},
    'v': {'root': 'vraelvrae', 'meaning': 'Root for \'Convergence,\' \'The Meeting Place,\' or \'Unification.\'', 'age': 'The Age of Unity'},
    'w': {'root': 'weetus', 'meaning': 'Root for \'Waiting,\' \'Anticipation,\' or \'Stasis.\'', 'age': 'The Age of Stasis'},
    'x': {'root': 'xiangxong', 'meaning': 'Root for \'Fusion,\' \'Synthesis of Opposites,\' or \'Integration.\'', 'age': 'The Age of Integration'},
    'y': {'root': "y'uilliatachaeh", 'meaning': 'Root for \'Culmination,\' \'The Final Seal,\' or \'End of an Era.\'', 'age': 'The Age of Ending'},
    'z': {'root': 'zazoykenne', 'meaning': 'Root for \'Rebirth,\' \'The Renewal,\' or \'Restart.\'', 'age': 'The Age of Transition (Age-Reset)'}
}

# --- Tahkmahnelle Time System Constants ---

T_SECONDS_PER_MINUTE = 9
T_MINUTES_PER_HOUR = 7
T_HOURS_PER_DAY = 8
T_DAYS_PER_WEEK = 5
T_WEEKS_PER_MONTH = 9
T_MONTHS_PER_AGE = 3
T_TICKS_PER_SECOND = 1000 

REAL_SECONDS_PER_DAY = 86400
TOTAL_T_SECONDS_PER_DAY = (T_SECONDS_PER_MINUTE * T_MINUTES_PER_HOUR * T_HOURS_PER_DAY)

# Year offset: Current T-Year is 5849
YEAR_OFFSET = 5849 - datetime.datetime.now().year

# Age structure definitions (New Year starts after Summer Solstice)
TAHKMAHNELLE_AGE_CYCLE = [
    {'key': 'C', 'name': 'The Age of Precedent (New Year)', 'date': (9, 22)}, # Autumn Equinox
    {'key': 'D', 'name': 'The Age of Transition', 'date': (12, 21)},      # Winter Solstice
    {'key': 'A', 'name': 'The Age of Genesis', 'date': (3, 20)},          # Spring Equinox
    {'key': 'B', 'name': 'The Age of Zenith', 'date': (6, 21)}           # Summer Solstice
]

# Get a sorted list of the root names for cycle naming
ROOT_NAMES = [d['root'] for k, d in sorted(TAHKMAHNELLE_DICTIONARY.items())]

# --- General Utility Functions ---

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_t_day_name(day_index):
    """Names the 5 T-Days using roots A-E (0-4)."""
    if 0 <= day_index < 5:
        return ROOT_NAMES[day_index]
    return f"Day {day_index + 1}"

def get_t_week_name(week_index):
    """Names the 9 T-Weeks using roots F-N (0-8)."""
    if 0 <= week_index < 9:
        return ROOT_NAMES[week_index + 5]
    return f"Week {week_index + 1}"

def get_t_month_name(month_index):
    """Names the 3 T-Months using roots O-Q (0-2)."""
    if 0 <= month_index < 3:
        return ROOT_NAMES[month_index + 14]
    return f"Month {month_index + 1}"

# --- 1. Time System (Solar Clock) Functions ---

def get_current_t_age_and_year(now):
    """Determines the current Tahkmahnelle Age and Year based on the date."""
    current_year = now.year
    age_starts = []
    
    for y in [current_year, current_year - 1]:
        for age_data in TAHKMAHNELLE_AGE_CYCLE:
            month, day = age_data['date']
            age_starts.append((datetime.datetime(y, month, day), age_data))
        
    age_starts.sort(key=lambda x: x[0])
    
    current_age_data = None
    age_start_date = None

    for start_date, age_data in reversed(age_starts):
        if start_date <= now:
            current_age_data = age_data
            age_start_date = start_date
            break
            
    t_year = current_year + YEAR_OFFSET
    return current_age_data['name'], age_start_date, t_year


def get_tahkmahnelle_time(now):
    """Calculates all Tahkmahnelle time units."""
    
    current_age_name, age_start_date, t_year = get_current_t_age_and_year(now)
    time_in_age = now - age_start_date
    real_days_in_age = time_in_age.total_seconds() / REAL_SECONDS_PER_DAY
    
    # --- Date Components ---
    days_in_month = T_WEEKS_PER_MONTH * T_DAYS_PER_WEEK
    t_month_index = math.floor(real_days_in_age / days_in_month) % T_MONTHS_PER_AGE
    t_month_display = t_month_index + 1 
    t_month_name = get_t_month_name(t_month_index)
    
    days_since_month_start = real_days_in_age % days_in_month
    t_week_index = math.floor(days_since_month_start / T_DAYS_PER_WEEK) % T_WEEKS_PER_MONTH
    t_week_display = t_week_index + 1 
    t_week_name = get_t_week_name(t_week_index)
    
    days_since_week_start = days_since_month_start % T_DAYS_PER_WEEK
    t_day_index = math.floor(days_since_week_start) % T_DAYS_PER_WEEK
    t_day_display = t_day_index + 1 
    t_day_name = get_t_day_name(t_day_index)
    
    # --- Time Components ---
    real_seconds_in_day = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    total_t_index = (real_seconds_in_day * TOTAL_T_SECONDS_PER_DAY * T_TICKS_PER_SECOND) / REAL_SECONDS_PER_DAY
    
    # T-Hours (H)
    t_hour_divisor = T_MINUTES_PER_HOUR * T_SECONDS_PER_MINUTE * T_TICKS_PER_SECOND
    t_hour = math.floor(total_t_index / t_hour_divisor) % T_HOURS_PER_DAY
    remaining_index = total_t_index % t_hour_divisor

    # T-Minutes (M)
    t_minute_divisor = T_SECONDS_PER_MINUTE * T_TICKS_PER_SECOND
    t_minute = math.floor(remaining_index / t_minute_divisor) % T_MINUTES_PER_HOUR
    remaining_index = remaining_index % t_minute_divisor
    
    # T-Seconds (S)
    t_second_divisor = T_TICKS_PER_SECOND
    t_second = math.floor(remaining_index / t_second_divisor) % T_SECONDS_PER_MINUTE
    remaining_index = remaining_index % t_second_divisor
    
    # T-Ticks (T)
    t_tick = math.floor(remaining_index)
    
    return {
        'T-Tick': t_tick, 'T-Second': t_second, 'T-Minute': t_minute, 'T-Hour': t_hour,
        'T-Day': t_day_display, 'T-Week': t_week_display, 'T-Month': t_month_display,
        'T-Age': current_age_name, 'T-Year': t_year,
        'T-Day-Name': t_day_name, 'T-Week-Name': t_week_name, 'T-Month-Name': t_month_name
    }


def render_t_clock(t_time):
    """Generates the ASCII analog and digital clock display for Tahkmahnelle time."""
    H = t_time['T-Hour']
    M = t_time['T-Minute']
    S = t_time['T-Second']
    T = t_time['T-Tick']
    
    # 1. Digital Clock Display
    digital_output = (
        f"        {H:01d}:{M:01d}:{S:01d}.{T:03d} (H:M:S.T-Tick)"
    )
    
    # 2. ASCII Analog Clock Display (8-Hour Dial)
    
    hour_positions = {
        0: (0, 4), 1: (1, 6), 2: (4, 8), 3: (7, 6),
        4: (8, 4), 5: (7, 2), 6: (4, 0), 7: (1, 2)
    }
    
    face = [list('         ') for _ in range(9)]
    
    # Mark the dial points
    for i in range(8):
        r, c = hour_positions[i]
        face[r][c] = str(i)
        
    center_r, center_c = 4, 4
    face[center_r][center_c] = 'X' # Center point

    # Determine hand positions
    hour_pos = hour_positions[H]
    
    # Hour Hand: Mark current T-Hour with 'H'
    face[hour_pos[0]][hour_pos[1]] = 'H'

    # Minute Hand/Combined Index: Use 'o' to show the minute's influence on the hour position
    minute_symbol_col = hour_pos[1]
    minute_symbol_row = hour_pos[0]
    
    if M > 3: # Simple indicator of minute progression
        minute_symbol_col += (1 if hour_pos[1] < center_c else -1)
        minute_symbol_row += (1 if hour_pos[0] < center_r else -1)

    minute_symbol_row = max(0, min(8, minute_symbol_row))
    minute_symbol_col = max(0, min(8, minute_symbol_col))

    if face[minute_symbol_row][minute_symbol_col] == ' ':
        face[minute_symbol_row][minute_symbol_col] = 'o' 

    # Render ASCII Clock
    ascii_clock = "\n".join(["       " + "".join(row) for row in face])

    return digital_output, ascii_clock


def run_solar_clock():
    """Runs the main display loop for the Tahkmahnelle Solar Clock."""
    
    print("Starting Tahkmahnelle Solar Clock (T-Year 5849)...")
    time.sleep(1) 
    
    UPDATE_INTERVAL = 0.046 # 46 milliseconds
    
    try:
        while True:
            now = datetime.datetime.now()
            t_time = get_tahkmahnelle_time(now)
            
            clear_screen()
            print("=" * 90)
            print("               VISUALIZER 1: TAHKMAHNELLE SOLAR CHRONOLOGER")
            print("=" * 90)
            
            digital_out, analog_out = render_t_clock(t_time)
            
            # Display Analog Clock
            print("--- ANALOG CLOCK (8-Hour Dial) ---")
            print(analog_out)
            print("         H=Hour | o=Minute Progress | X=Center\n")
            
            # Display Digital Clock
            print("--- DIGITAL CLOCK & UNITS ---")
            print(f"Current T-Time: {digital_out}")
            print("-" * 90)
            
            # W - ticks, seconds, minutes, hours, days, weeks, months, ages, year (concise running time)
            concise_output = (
                f"W - T:{t_time['T-Tick']:03d}, S:{t_time['T-Second']:01d}, M:{t_time['T-Minute']:01d}, H:{t_time['T-Hour']:01d}, "
                f"D:{t_time['T-Day']:01d}/{T_DAYS_PER_WEEK}, Wk:{t_time['T-Week']:01d}/{T_WEEKS_PER_MONTH}, "
                f"Mo:{t_time['T-Month']:01d}/{T_MONTHS_PER_AGE}, Yr:{t_time['T-Year']}"
            )
            
            print(f"Tahkmahnelle45time Index: {concise_output}")
            print("-" * 90)
            
            # Display Named Cycles
            print(f"Current **Age**: {t_time['T-Age']}")
            print(f"**Named Cycles**: Day {t_time['T-Day-Name']} | Week {t_time['T-Week-Name']} | Month {t_time['T-Month-Name']}")
            print("=" * 90)
            print(f"Real Time: {now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} | Update Rate: {UPDATE_INTERVAL*1000}ms")
            print("Press Ctrl+C to return to the Main Menu.")
            
            time.sleep(UPDATE_INTERVAL) 
            
    except KeyboardInterrupt:
        clear_screen()
        print("\nSolar Chronologer stopped.")

# --- 2. Language System (LoA Index) Functions ---

def run_loa_index():
    """Runs the interactive dictionary/glossary tool."""
    clear_screen()
    print("=" * 90)
    print("               VISUALIZER 2: LANDS OF AGES (LoA) INDEX & DICTIONARY")
    print("=" * 90)
    
    LOA_EXPLANATION = """
### LoA Linguistic Chronology ###
The Tahkmahnelle system fuses language and time. Every foundational root (A-Z) serves
as both a philosophical concept and the name for a cyclical period or holiday.
- **T-Days (5 total):** Named by the roots A through E.
- **T-Weeks (9 total):** Named by the roots F through N.
- **T-Months (3 total):** Named by the roots O through Q.
"""
    print(LOA_EXPLANATION)
    print("\nAvailable Roots: " + ", ".join([k.upper() for k in sorted(TAHKMAHNELLE_DICTIONARY.keys())]))
    print("-" * 90)

    while True:
        query = input("Enter a single letter root (A-Z) or type 'QUIT' to exit: ").lower().strip()
        
        if query == 'quit':
            break

        if len(query) == 1 and query.isalpha():
            entry = TAHKMAHNELLE_DICTIONARY.get(query)
            if entry:
                print("\n" + "=" * 50)
                print(f"INDEX MARKER: {query.upper()} | ROOT: {entry['root']}")
                print("-" * 50)
                print(f"Conceptual Meaning: {entry['meaning']}")
                print(f"Linguistic Context: {entry['age']}")
                print("=" * 50)
            else:
                print(f"\n[Error] The letter '{query.upper()}' is not a recognized Primal Root.")
        else:
            print("\n[Error] Invalid input. Please enter a single letter or 'QUIT'.")
    
    clear_screen()
    print("Returned to Main Menu.")

# --- 3. Spatial System (X, Y, Z) Functions ---

def render_spatial_grid(x, y, z):
    """Renders a simplified ASCII 3D coordinate space visualization."""
    
    # Define visualization parameters (Max 10 for display purposes)
    MAX_COORD = 10
    
    # Ensure coordinates are within display bounds
    x_display = min(MAX_COORD, max(0, x))
    y_display = min(MAX_COORD, max(0, y))
    z_display = min(MAX_COORD, max(0, z))
    
    grid = []
    
    # Y-axis (vertical) - 11 lines (0 to 10)
    for row in range(MAX_COORD + 1):
        line = list("." * (MAX_COORD + 1) * 2) # Doubling for horizontal stretch
        
        # Mark Y-axis label
        if row == MAX_COORD // 2:
            line.insert(0, 'Y')
        else:
            line.insert(0, ' ')
        
        # Draw the Z-axis (depth) projection line (runs diagonally up-left from origin (0,0))
        # This is a very rough representation
        z_offset = z_display # Represents depth perspective
        
        # Mark the Z-axis projection from the corner
        if row == MAX_COORD:
            line[1:1+z_offset] = ['/'] * z_offset
            
        # Place the current location marker '@'
        if row == MAX_COORD - y_display: # Y axis is inverted for console display
            
            # X position is doubled for better ASCII spacing
            x_pos = 1 + x_display * 2 
            
            # Apply Z offset (pushing the marker diagonally up-left)
            x_pos -= z_display 
            y_pos = row + z_display // 2
            
            # Prevent overflow/overlap
            if 0 < x_pos < len(line) and 0 <= row < MAX_COORD + 1:
                line[x_pos] = '@'
                
        grid.append("".join(line))
        
    # Add X-axis label (horizontal)
    x_axis_label = " " + "0" + "--" * (MAX_COORD // 2) + "X" + "--" * (MAX_COORD // 2)
    grid.append(x_axis_label)
    
    # Key
    key = (
        f"Location: ({x}, {y}, {z}) | Resources (X) | Knowledge (Y) | Depth (Z)\n"
        f"Visualization Focus: (0-{MAX_COORD})"
    )
    
    return "\n".join(grid), key


def run_spatial_system_viz():
    """Interactive tool to locate resources in the X, Y, Z spatial system."""
    clear_screen()
    print("=" * 90)
    print("              VISUALIZER 3: SPATIAL SYSTEM (X, Y, Z) LOCATOR")
    print("=" * 90)
    print("Conceptual Axes:")
    print("X-Axis: Resources (0=Raw, 10=Refined)")
    print("Y-Axis: Library/Knowledge (0=Basic Data, 10=Complex Systems)")
    print("Z-Axis: Storage Depth (0=Surface, 10=Deep Archives)")
    print("-" * 90)

    x, y, z = 5, 5, 5 # Initial center location
    
    while True:
        try:
            grid_viz, key = render_spatial_grid(x, y, z)
            
            clear_screen()
            print("=" * 90)
            print("              VISUALIZER 3: SPATIAL SYSTEM (X, Y, Z) LOCATOR")
            print("=" * 90)
            print(grid_viz)
            print(f"\nCurrent Location: X={x}, Y={y}, Z={z}. Max range: 10.")
            print(f"{key}\n")
            print("Commands: [X], [Y], [Z] +/- N (e.g., X+3, Z-1) or 'QUIT'.")
            
            command = input("Enter command: ").upper().strip()

            if command == 'QUIT':
                break

            if len(command) < 3 or command[1] not in ['+', '-'] or command[0] not in ['X', 'Y', 'Z']:
                print("[Error] Invalid command format. Use X+N, Y-N, etc.")
                time.sleep(1)
                continue

            axis = command[0]
            op = command[1]
            try:
                value = int(command[2:])
            except ValueError:
                print("[Error] Value must be an integer.")
                time.sleep(1)
                continue
            
            current_val = {'X': x, 'Y': y, 'Z': z}[axis]
            
            if op == '+':
                new_val = current_val + value
            else:
                new_val = current_val - value
            
            # Clamp values between 0 and 10
            new_val = max(0, min(10, new_val))
            
            if axis == 'X': x = new_val
            elif axis == 'Y': y = new_val
            elif axis == 'Z': z = new_val
            
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(1)

    clear_screen()
    print("Returned to Main Menu.")

# --- Main Application Menu ---

def main_menu():
    """Presents the interactive command-line interface."""
    clear_screen()
    script_name = sys.argv[0] if sys.argv else "Tahkmahnelle_OmniViz.py"
    
    print("\n" + "#" * 80)
    print(f"      TAHKMAHNELLE OMNI-VISUALIZER ({script_name})")
    print("#" * 80)
    
    while True:
        print("\n--- Select a Visualizer System ---")
        print("1. TIME: Run Tahkmahnelle Solar Chronologer (Clock)")
        print("2. LANGUAGE: Access LoA Index & Dictionary (Glossary)")
        print("3. SPATIAL: Run X, Y, Z System Locator (Resources/Library)")
        print("4. Exit Application")
        
        choice = input("Enter your choice (1-4): ").lower().strip()
        
        if choice == '1':
            run_solar_clock()
            clear_screen()
            print("Returned to Main Menu.")
        elif choice == '2':
            run_loa_index()
        elif choice == '3':
            run_spatial_system_viz()
        elif choice == '4' or choice in ['exit', 'quit']:
            print("\nTahkmahnelle Omni-Visualizer offline. Synchronization complete.")
            break
        else:
            print("\n[Error] Invalid input. Please enter a number from 1 to 4.")

# --- Execution ---
if __name__ == "__main__":
    main_menu()

