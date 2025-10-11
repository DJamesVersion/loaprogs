import time
import datetime
import math
import os
import sys

# --- I. TAHKMAHNELLE LINGUISTIC & CHRONOLOGICAL DATABASE ---

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
    'i': {'root': 'illianarre', 'meaning': 'Root for \'Truth,\' \'Unveiling,\' or \'Revelation.\"', 'age': 'The Age of Clarity'},
    'j': {'root': 'ampejinne', 'meaning': 'Root for \'Intervention,\' \'Sudden Change,\' or \'Catalyst.\'', 'age': 'The Age of Catalyst'},
    'k': {'root': 'kajoinkenne', 'meaning': 'Root for \'Harmony,\' \'Balance,\' or \'The Midpoint.\"', 'age': 'The Age of Zenith'},
    'l': {'root': 'lenemketobontette', 'meaning': 'Root for \'Long Journey,\' \'Exile,\' or \'Wandering.\"', 'age': 'The Age of Passage'},
    'm': {'root': 'momaw', 'meaning': 'Root for \'Sustenance,\' \'Nourishment,\' or \'The Mother Principle.\"', 'age': 'The Age of Life'},
    'n': {'root': 'nona, nano', 'meaning': 'Root for \'Negation,\' \'Void,\' or \'The Absence.\'', 'age': 'The Age of Silence'},
    'o': {'root': 'oichenne', 'meaning': 'Root for \'Wisdom,\' \'Deep Understanding,\' or \'Enlightenment.\'', 'age': 'The Age of Enlightenment'},
    'p': {'root': 'perfuvium', 'meaning': 'Root for \'Scattering,\' \'Fragmentation,\' or \'Dispersion.\'', 'age': 'The Age of Diaspora'},
    'q': {'root': 'quaristenne', 'meaning': 'Root for \'Question,\' \'The Search,\' or \'Inquiry.\'', 'age': 'The Age of Inquiry'},
    'r': {'root': 'roykenne', 'meaning': 'Root for \'Return,\' \'Recurrence,\' or \'The Cycle.\'', 'age': 'The Age of Cycles'},
    's': {'root': 'stihuu, siataeh', 'meaning': 'Root for \'Vibration,\' \'Sound,\' or \'Spoken Word.\"', 'age': 'The Age of Voice'},
    't': {'root': 'tetnobautte, tahkmahnelle', 'meaning': 'Root for \'Governance,\' \'System,\' or \'The People/Culture.\"', 'age': 'The Age of Culture'},
    'u': {'root': 'uilliatachaeh', 'meaning': 'Root for \'Vision,\' \'Foresight,\' or \'The Future.\"', 'age': 'The Age of Destiny'},
    'v': {'root': 'vraelvrae', 'meaning': 'Root for \'Convergence,\' \'The Meeting Place,\' or \'Unification.\"', 'age': 'The Age of Unity'},
    'w': {'root': 'weetus', 'meaning': 'Root for \'Waiting,\' \'Anticipation,\' or \'Stasis.\'', 'age': 'The Age of Stasis'},
    'x': {'root': 'xiangxong', 'meaning': 'Root for \'Fusion,\' \'Synthesis of Opposites,\' or \'Integration.\"', 'age': 'The Age of Integration'},
    'y': {'root': "y'uilliatachaeh", 'meaning': 'Root for \'Culmination,\' \'The Final Seal,\' or \'End of an Era.\"', 'age': 'The Age of Ending'},
    'z': {'root': 'zazoykenne', 'meaning': 'Root for \'Rebirth,\' \'The Renewal,\' or \'Restart.\"', 'age': 'The Age of Transition (Age-Reset)'}
}

# 7 Sets of Cycles for Decades, Centuries, Millennia (A-G Roots)
LONG_TERM_SETS = [
    {'root': 'ariats', 'meaning': 'Set of Genesis'}, 
    {'root': 'batos', 'meaning': 'Set of Expansion'}, 
    {'root': "c'illias", 'meaning': 'Set of Consciousness'}, 
    {'root': 'diados', 'meaning': 'Set of Structure'}, 
    {'root': 'eechuwahs', 'meaning': 'Set of Motion'}, 
    {'root': "f'illias", 'meaning': 'Set of Covenant'}, 
    {'root': 'gagois', 'meaning': 'Set of Alliance'}
]

# --- II. TIME SYSTEM CONSTANTS ---

T_SECONDS_PER_MINUTE = 9
T_MINUTES_PER_HOUR = 7
T_HOURS_PER_DAY = 8
T_DAYS_PER_WEEK = 5
T_WEEKS_PER_MONTH = 9
T_MONTHS_PER_AGE = 3
T_TICKS_PER_SECOND = 1000 

REAL_SECONDS_PER_DAY = 86400.0
TOTAL_T_SECONDS_PER_DAY = (T_SECONDS_PER_MINUTE * T_MINUTES_PER_HOUR * T_HOURS_PER_DAY)

# T-Year offset relative to the current real year (5849 is the reference T-Year)
YEAR_OFFSET = 5849 - datetime.datetime.now().year

# Age structure definitions (Using equinox/solstice dates as cycle start points)
TAHKMAHNELLE_AGE_CYCLE = [
    {'key': 'C', 'name': 'The Age of Precedent', 'date': (9, 22)}, # Autumn Equinox
    {'key': 'D', 'name': 'The Age of Transition', 'date': (12, 21)}, # Winter Solstice
    {'key': 'A', 'name': 'The Age of Genesis', 'date': (3, 20)},  # Spring Equinox
    {'key': 'B', 'name': 'The Age of Zenith', 'date': (6, 21)}    # Summer Solstice
]

# Get a sorted list of the root names for cycle naming
ROOT_NAMES = [d['root'] for k, d in sorted(TAHKMAHNELLE_DICTIONARY.items())]

# --- III. UTILITY FUNCTIONS ---

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_t_day_name(day_index):
    """Names the 5 T-Days using roots A-E (0-4)."""
    return ROOT_NAMES[day_index % T_DAYS_PER_WEEK]

def get_t_week_name(week_index):
    """Names the 9 T-Weeks using roots F-N (0-8)."""
    return ROOT_NAMES[(week_index % T_WEEKS_PER_MONTH) + T_DAYS_PER_WEEK]

def get_t_month_name(month_index):
    """Names the 3 T-Months using roots O-Q (0-2)."""
    return ROOT_NAMES[(month_index % T_MONTHS_PER_AGE) + T_DAYS_PER_WEEK + T_WEEKS_PER_MONTH]

# --- IV. CORE TIME CALCULATION FUNCTIONS ---

def get_current_t_age_and_year(now):
    """Determines the current Tahkmahnelle Age and Year based on the date."""
    current_year = now.year
    age_starts = []
    
    # Check start dates for the current year and the previous year
    for y in [current_year, current_year - 1]:
        for age_data in TAHKMAHNELLE_AGE_CYCLE:
            month, day = age_data['date']
            try:
                age_starts.append((datetime.datetime(y, month, day), age_data))
            except ValueError:
                # Skip invalid dates (e.g., Feb 29 on non-leap year)
                continue
        
    age_starts.sort(key=lambda x: x[0])
    
    current_age_data = None
    age_start_date = None

    # Find the most recent cycle start date
    for start_date, age_data in reversed(age_starts):
        if start_date <= now:
            current_age_data = age_data
            age_start_date = start_date
            break
            
    # T-Year is offset from the current real year
    t_year = current_year + YEAR_OFFSET
    return current_age_data['name'], age_start_date, t_year


def calculate_long_term_cycles(t_year):
    """Calculates the Stahoy, Vraen, and Tetnobausse, and their governing 7 Sets (Ariats)."""
    
    # T_MILLENNIA: Tetnobausse (1000 T-Years)
    T_MILLENNIA = math.floor((t_year - 1) / 1000) + 1
    TETNOBAUSSE_SET = LONG_TERM_SETS[(T_MILLENNIA - 1) % 7]

    # T_CENTURY_TOTAL: Vraen (100 T-Years)
    T_CENTURY_TOTAL = math.floor((t_year - 1) / 100) + 1
    VRAEN_SET = LONG_TERM_SETS[(T_CENTURY_TOTAL - 1) % 7]

    # T_DECADE_TOTAL: Stahoy (10 T-Years)
    T_DECADE_TOTAL = math.floor((t_year - 1) / 10) + 1
    STAHOY_SET = LONG_TERM_SETS[(T_DECADE_TOTAL - 1) % 7]
    
    # T_YEAR_IN_DECADE
    T_YEAR_IN_DECADE = ((t_year - 1) % 10) + 1 # 1 to 10

    return {
        'T_DECADE_TOTAL': T_DECADE_TOTAL,
        'T_CENTURY_TOTAL': T_CENTURY_TOTAL,
        'T_MILLENNIA': T_MILLENNIA,
        'T_YEAR_IN_DECADE': T_YEAR_IN_DECADE,
        'stahoy_set': STAHOY_SET,
        'vraen_set': VRAEN_SET,
        'tetnobausse_set': TETNOBAUSSE_SET,
    }


def get_tahkmahnelle_time(now):
    """Calculates all Tahkmahnelle time and date units."""
    
    current_age_name, age_start_date, t_year = get_current_t_age_and_year(now)
    time_in_age = now - age_start_date
    real_days_in_age = time_in_age.total_seconds() / REAL_SECONDS_PER_DAY
    
    # --- Date Components (Months, Weeks, Days) ---
    days_in_month = T_WEEKS_PER_MONTH * T_DAYS_PER_WEEK
    
    # Total days since T-Year start (simplified: using 365.25 for average days/year)
    t_days_since_year_start = (now - datetime.datetime(now.year, 1, 1)).total_seconds() / REAL_SECONDS_PER_DAY
    
    t_month_index = math.floor(t_days_since_year_start / days_in_month) % T_MONTHS_PER_AGE
    t_month_name = get_t_month_name(t_month_index)
    
    days_since_month_start = t_days_since_year_start % days_in_month
    t_week_index = math.floor(days_since_month_start / T_DAYS_PER_WEEK) % T_WEEKS_PER_MONTH
    t_week_name = get_t_week_name(t_week_index)
    
    days_since_week_start = days_since_month_start % T_DAYS_PER_WEEK
    t_day_index = math.floor(days_since_week_start) % T_DAYS_PER_WEEK
    t_day_name = get_t_day_name(t_day_index)
    
    # --- Time Components (Hours, Minutes, Seconds, Ticks) ---
    real_seconds_in_day = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    
    # Total T-Tick index (1 T-Second = 1000 T-Ticks)
    conversion_factor = (TOTAL_T_SECONDS_PER_DAY * T_TICKS_PER_SECOND) / REAL_SECONDS_PER_DAY
    total_t_index = real_seconds_in_day * conversion_factor
    
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
    
    long_term_cycles = calculate_long_term_cycles(t_year)
    
    return {
        'T-Tick': t_tick, 'T-Second': t_second, 'T-Minute': t_minute, 'T-Hour': t_hour,
        'T-Day-Name': t_day_name, 'T-Week-Name': t_week_name, 'T-Month-Name': t_month_name,
        'T-Age': current_age_name, 'T-Year': t_year,
        **long_term_cycles
    }

# --- V. RENDERING FUNCTIONS ---

def render_t_clock(t_time):
    """Generates the ASCII analog and digital clock display."""
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
    face[hour_pos[0]][hour_pos[1]] = 'H' # Hour Hand

    # Minute Hand/Combined Index: Use 'o' to show the minute's influence on the hour position
    minute_symbol_col = hour_pos[1]
    minute_symbol_row = hour_pos[0]
    
    # Simple shift based on minute progression (0-6)
    if M > 3: 
        minute_symbol_col += (1 if hour_pos[1] < center_c else -1)
        minute_symbol_row += (1 if hour_pos[0] < center_r else -1)

    minute_symbol_row = max(0, min(8, minute_symbol_row))
    minute_symbol_col = max(0, min(8, minute_symbol_col))

    if face[minute_symbol_row][minute_symbol_col] == ' ':
        face[minute_symbol_row][minute_symbol_col] = 'o' 

    # Render ASCII Clock
    ascii_clock = "\n".join(["       " + "".join(row) for row in face])

    return digital_output, ascii_clock


def render_spatial_grid(x, y, z):
    """Renders a simplified ASCII 3D coordinate space visualization."""
    
    MAX_COORD = 10
    
    # Clamp coordinates for visualization
    x_display = max(0, min(MAX_COORD, x))
    y_display = max(0, min(MAX_COORD, y))
    z_display = max(0, min(MAX_COORD, z))
    
    grid = []
    
    for row in range(MAX_COORD + 1):
        line_content = ['.'] * (MAX_COORD * 2 + 1)
        
        # Add Y label
        y_label = 'Y' if row == MAX_COORD // 2 else ' '
        line_str = [y_label] + line_content
        
        # Place the current location marker '@'
        if row == MAX_COORD - y_display: # Y axis is inverted for console display
            
            x_pos = 1 + x_display * 2 
            x_pos -= z_display // 2 # Apply Z offset for depth illusion
            
            # Ensure position is within the line bounds
            pos_index = max(1, min(len(line_str) - 1, x_pos))

            if 0 < pos_index < len(line_str):
                line_str[pos_index] = '@'
                
        grid.append("".join(line_str))
        
    # Add X-axis label (horizontal)
    x_axis_label = " " + "0" + "--" * (MAX_COORD // 2) + "X" + "--" * (MAX_COORD // 2)
    grid.append(x_axis_label)
    
    # Key
    key = (
        f"Current Spatial Location: X={x}, Y={y}, Z={z}\n"
        "Axes: Resources (X) | Knowledge (Y) | Depth (Z)"
    )
    
    return "\n".join(grid), key


def update_spatial_coords(x, y, z):
    """Allows interactive update of spatial coordinates upon pausing the clock."""
    print("-" * 50)
    print("Spatial System Input Paused.")
    
    while True:
        try:
            print(f"Current Position: X={x}, Y={y}, Z={z}")
            command = input("Enter command (X+N, Y-N, Z+N) or 'RESUME': ").upper().strip()
            
            if command == 'RESUME':
                break
            
            if len(command) < 3 or command[1] not in ['+', '-'] or command[0] not in ['X', 'Y', 'Z']:
                print("[Error] Invalid command format. Use X+1, Y-3, etc.")
                continue
            
            axis = command[0]
            op = command[1]
            value = int(command[2:])
            
            current_val = x if axis == 'X' else (y if axis == 'Y' else z)
            
            if op == '+':
                new_val = current_val + value
            else:
                new_val = current_val - value
            
            # Clamp values between 0 and 10
            new_val = max(0, min(10, new_val))
            
            if axis == 'X': x = new_val
            elif axis == 'Y': y = new_val
            elif axis == 'Z': z = new_val

            print(f"Position updated to X={x}, Y={y}, Z={z}.")

        except ValueError:
            print("[Error] Value must be an integer.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
    print("Spatial synchronization resumed...")
    return x, y, z

# --- VI. APPLICATION FLOW ---

def display_loa_explanation(t_time=None):
    """Prints the comprehensive explanation of the LoA concept and time fusion."""
    clear_screen()
    
    LONG_TERM_SETS_STR = "\n".join([
        f"  - **{s['root'].capitalize()}** (Set {i+1}): {s['meaning']}" 
        for i, s in enumerate(LONG_TERM_SETS)
    ])
    
    LOA_EXPLANATION = f"""
============================================================================================
           TAHKMAHNELLE LOA INDEX: LINGUISTIC & CHRONOLOGICAL GLOSSARY
============================================================================================
The Tahkmahnelle system fuses language, time, and cosmic history. Every foundational root (A-Z) 
serves as both a philosophical concept and the name for a cyclical period.

### MACRO-CYCLE ALIGNMENT: 7 PRIMAL SETS (Ariats)
These cycles define the eras and are governed by a rotating set of 7 **Primal Sets**.

- **Tetnobausse** (Millennium): 10 Vraen (1000 T-Years).
- **Vraen** (Century): 10 Stahoys (100 T-Years).
- **Stahoy** (Decade): 10 T-Years.

**The 7 Governing Sets:**
{LONG_TERM_SETS_STR}

### TKEMNÂTI (26 PRIMAL ROOTS) GLOSSARY
--------------------------------------------------------------------------------------------"""
    print(LOA_EXPLANATION)
    
    for key in sorted(TAHKMAHNELLE_DICTIONARY.keys()):
        entry = TAHKMAHNELLE_DICTIONARY[key]
        print(f"**Root {key.upper()}: {entry['root']}**")
        print(f"  - Meaning: {entry['meaning']}")
        print(f"  - Associated Age/Cycle: {entry['age']}")

    print("============================================================================================")
    
    if t_time:
        print(f"CURRENT ALIGNMENT (T-Year {t_time['T-Year']}):")
        print(f"  Millennium Set ({t_time['T_MILLENNIA']}. Tetnobausse): **{t_time['tetnobausse_set']['root'].capitalize()}**")
        print(f"  Century Set ({t_time['T_CENTURY_TOTAL']}. Vraen): **{t_time['vraen_set']['root'].capitalize()}**")
        print(f"  Decade Set ({t_time['T_DECADE_TOTAL']}. Stahoy): **{t_time['stahoy_set']['root'].capitalize()}**")
        print("-" * 50)
    
    input("Press Enter to return to the Main Menu...")


def run_unified_viz():
    """Runs the main display loop showing Time, Language context, and Space."""
    
    print("Initializing Tahkmahnelle Omni-Viz (T-Year 5849)...")
    time.sleep(1) 
    
    UPDATE_INTERVAL = 0.046 # 46 milliseconds (Approx. 1 T-Tick)
    x, y, z = 5, 5, 5 # Initial spatial coordinates (Center)

    try:
        while True:
            now = datetime.datetime.now()
            t_time = get_tahkmahnelle_time(now)
            digital_out, analog_out = render_t_clock(t_time)
            grid_viz, spatial_key = render_spatial_grid(x, y, z)
            
            clear_screen()
            print("=" * 90)
            print("                 TAHKMAHNELLE MEGA-VISUALIZER (PYTHON)")
            print("=" * 90)
            
            # --- 1. TIME/CHRONOLOGY DISPLAY ---
            print("--- 1. SOLAR CHRONOLOGER (46ms Precision) ---")
            print(f"Current T-Time: {digital_out}")
            print(analog_out)
            
            concise_output = (
                f"W (Concise): T:{t_time['T-Tick']:03d} S:{t_time['T-Second']:01d} M:{t_time['T-Minute']:01d} H:{t_time['T-Hour']:01d} | "
                f"Day: {t_time['T-Day-Name'].capitalize()} | Age: {t_time['T-Age']}"
            )
            print(concise_output)
            print("-" * 90)

            # --- 2. LANGUAGE/CYCLICAL CONTEXT DISPLAY ---
            print("--- 2. LINGUISTIC & MACRO-CYCLES (LoA Index) ---")
            print(f"Current T-Year: **{t_time['T-Year']}**")
            print(f"Named Cycles: Month **{t_time['T-Month-Name']}** | Week **{t_time['T-Week-Name']}** | Day **{t_time['T-Day-Name']}**")
            print(f"Macro-Cycle Set Alignment (7 Primal Sets):")
            print(f"  Millennium ({t_time['T_MILLENNIA']}. Tetnobausse): **{t_time['tetnobausse_set']['root'].capitalize()}**")
            print(f"  Century ({t_time['T_CENTURY_TOTAL']}. Vraen): **{t_time['vraen_set']['root'].capitalize()}**")
            print(f"  Decade ({t_time['T_DECADE_TOTAL']}. Stahoy): **{t_time['stahoy_set']['root'].capitalize()}** (Year {t_time['T_YEAR_IN_DECADE']}/10)")
            print("-" * 90)
            
            # --- 3. SPATIAL SYSTEM DISPLAY ---
            print("--- 3. SPATIAL LOCATOR (X, Y, Z) ---")
            print(grid_viz)
            print(spatial_key)
            print("=" * 90)
            
            print(f"Real Time: {now.strftime('%H:%M:%S.%f')[:-3]} | Update: {UPDATE_INTERVAL*1000:.0f}ms")
            print("Press Ctrl+C to **Pause** and adjust the Spatial Coordinates.")
            
            time.sleep(UPDATE_INTERVAL) 
            
    except KeyboardInterrupt:
        # Pause and allow coordinate update
        x, y, z = update_spatial_coords(x, y, z)
        
        # After update, prompt to resume or exit
        clear_screen()
        print("\nOmni-Visualizer paused.")
        if input("Type 'R' to Resume the visualizer or press Enter to return to the Main Menu: ").upper() == 'R':
            run_unified_viz() # Restart the loop with new coordinates
        else:
            clear_screen()
            print("Returned to Main Menu.")


def main_menu():
    """Presents the interactive command-line interface."""
    clear_screen()
    t_year = datetime.datetime.now().year + YEAR_OFFSET
    script_name = sys.argv[0] if sys.argv else "Tahkmahnelle_MegaViz_Python.py"
    
    print("\n" + "#" * 90)
    print(f"      TAHKMAHNELLE MEGA-VISUALIZER (T-Year {t_year}) - Python Edition")
    print("#" * 90)
    
    while True:
        print("\n--- Select a System View ---")
        print("1. Run **Unified Visualizer** (Real-Time Clock, Cycles, and Spatial Grid)")
        print("2. Access **LoA Index & Chronological Glossary** (Details on Cycles and Roots)")
        print("3. Exit Application")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            run_unified_viz()
        elif choice == '2':
            # Fetch time data once for context in the explanation
            now = datetime.datetime.now()
            t_time = get_tahkmahnelle_time(now)
            display_loa_explanation(t_time)
        elif choice == '3' or choice.lower() in ['exit', 'quit']:
            print("\nTahkmahnelle Mega-Visualizer offline. Synchronization complete.")
            break
        else:
            print("\n[Error] Invalid input. Please enter a number from 1 to 3.")

# --- Execution ---
if __name__ == "__main__":
    main_menu()

