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
    'k': {'root': 'kajoinkenne', 'meaning': 'Root for \'Harmony,\' \'Balance,\' or \'The Midpoint.\"', 'age': 'The Age of Zenith'},
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

# 7 Sets of Cycles for Decades, Centuries, Millennia
# Indices 0-6 correspond to the first 7 letters (A-G)
LONG_TERM_SETS = [
    {'root': 'ariats', 'index': 0, 'meaning': 'Set of Genesis'}, 
    {'root': 'batos', 'index': 1, 'meaning': 'Set of Expansion'}, 
    {'root': "c'illias", 'index': 2, 'meaning': 'Set of Consciousness'}, 
    {'root': 'diados', 'index': 3, 'meaning': 'Set of Structure'}, 
    {'root': 'eechuwahs', 'index': 4, 'meaning': 'Set of Motion'}, 
    {'root': "f'illias", 'index': 5, 'meaning': 'Set of Covenant'}, 
    {'root': 'gagois', 'index': 6, 'meaning': 'Set of Alliance'}
]

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


def calculate_long_term_cycles(t_year):
    """Calculates the current Stahoy, Vraen, and Tetnobausse, and their governing 7 Sets."""
    
    # Tetnobausse (Millennium): 1000 T-Years (T: Tetnobausse, M: Millennium)
    # The Tetnobausse is numbered 1-based.
    T_MILLENNIA = math.floor((t_year - 1) / 1000) + 1
    
    # Vraen (Century): 100 T-Years (V: Vraen, C: Century)
    T_CENTURY_IN_MILLENNIUM = math.floor(((t_year - 1) % 1000) / 100) + 1 # 1 to 10
    T_CENTURY_TOTAL = math.floor((t_year - 1) / 100) + 1 # Total centuries completed
    
    # Stahoy (Decade): 10 T-Years (S: Stahoy, D: Decade)
    T_DECADE_IN_CENTURY = math.floor(((t_year - 1) % 100) / 10) + 1 # 1 to 10
    T_DECADE_TOTAL = math.floor((t_year - 1) / 10) + 1 # Total decades completed
    
    # --- Cycle Set Calculations (Based on the total number of cycles completed) ---
    NUM_SETS = len(LONG_TERM_SETS)
    
    # Stahoy Set (Decade Cycle): Governed by the total Stahoys completed
    stahoy_set_index = (T_DECADE_TOTAL - 1) % NUM_SETS
    stahoy_set = LONG_TERM_SETS[stahoy_set_index]
    
    # Vraen Set (Century Cycle): Governed by the total Vraen completed
    vraen_set_index = (T_CENTURY_TOTAL - 1) % NUM_SETS
    vraen_set = LONG_TERM_SETS[vraen_set_index]
    
    # Tetnobausse Set (Millennium Cycle): Governed by the total Tetnobausse completed
    tetnobausse_set_index = (T_MILLENNIA - 1) % NUM_SETS
    tetnobausse_set = LONG_TERM_SETS[tetnobausse_set_index]
    
    return {
        'T_DECADE_TOTAL': T_DECADE_TOTAL,
        'T_CENTURY_TOTAL': T_CENTURY_TOTAL,
        'T_MILLENNIA': T_MILLENNIA,
        'T_YEAR_IN_DECADE': ((t_year - 1) % 10) + 1, # 1 to 10
        'stahoy_set': stahoy_set,
        'vraen_set': vraen_set,
        'tetnobausse_set': tetnobausse_set,
    }

def get_tahkmahnelle_time(now):
    """Calculates all Tahkmahnelle time units."""
    
    current_age_name, age_start_date, t_year = get_current_t_age_and_year(now)
    time_in_age = now - age_start_date
    real_days_in_age = time_in_age.total_seconds() / REAL_SECONDS_PER_DAY
    
    # --- Date Components (Ages, Months, Weeks, Days) ---
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
    
    # --- Time Components (Hours, Minutes, Seconds, Ticks) ---
    real_seconds_in_day = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    total_t_index = (real_seconds_in_day * TOTAL_T_SECONDS_PER_DAY * T_TICKS_PER_SECOND) / REAL_SECONDS_PER_DAY
    
    t_hour_divisor = T_MINUTES_PER_HOUR * T_SECONDS_PER_MINUTE * T_TICKS_PER_SECOND
    t_hour = math.floor(total_t_index / t_hour_divisor) % T_HOURS_PER_DAY
    remaining_index = total_t_index % t_hour_divisor

    t_minute_divisor = T_SECONDS_PER_MINUTE * T_TICKS_PER_SECOND
    t_minute = math.floor(remaining_index / t_minute_divisor) % T_MINUTES_PER_HOUR
    remaining_index = remaining_index % t_minute_divisor
    
    t_second_divisor = T_TICKS_PER_SECOND
    t_second = math.floor(remaining_index / t_second_divisor) % T_SECONDS_PER_MINUTE
    remaining_index = remaining_index % t_second_divisor
    
    t_tick = math.floor(remaining_index)
    
    long_term_cycles = calculate_long_term_cycles(t_year)
    
    return {
        'T-Tick': t_tick, 'T-Second': t_second, 'T-Minute': t_minute, 'T-Hour': t_hour,
        'T-Day': t_day_display, 'T-Week': t_week_display, 'T-Month': t_month_display,
        'T-Age': current_age_name, 'T-Year': t_year,
        'T-Day-Name': t_day_name, 'T-Week-Name': t_week_name, 'T-Month-Name': t_month_name,
        **long_term_cycles
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
    
    hour_positions = { 0: (0, 4), 1: (1, 6), 2: (4, 8), 3: (7, 6),
                       4: (8, 4), 5: (7, 2), 6: (4, 0), 7: (1, 2) }
    
    face = [list('         ') for _ in range(9)]
    for i in range(8):
        r, c = hour_positions[i]
        face[r][c] = str(i)
        
    center_r, center_c = 4, 4
    face[center_r][center_c] = 'X' 

    hour_pos = hour_positions[H]
    face[hour_pos[0]][hour_pos[1]] = 'H'

    minute_symbol_col = hour_pos[1]
    minute_symbol_row = hour_pos[0]
    
    if M > 3: 
        minute_symbol_col += (1 if hour_pos[1] < center_c else -1)
        minute_symbol_row += (1 if hour_pos[0] < center_r else -1)

    minute_symbol_row = max(0, min(8, minute_symbol_row))
    minute_symbol_col = max(0, min(8, minute_symbol_col))

    if face[minute_symbol_row][minute_symbol_col] == ' ':
        face[minute_symbol_row][minute_symbol_col] = 'o' 

    ascii_clock = "\n".join(["       " + "".join(row) for row in face])

    return digital_output, ascii_clock


# --- 2. Language System (LoA Index) Functions ---

def display_loa_explanation(t_time=None):
    """Prints the comprehensive explanation of the LoA concept and time fusion."""
    
    LONG_TERM_SETS_STR = "\n".join([
        f"  - **{s['root'].capitalize()}** (Set {s['index']+1}): {s['meaning']}" 
        for s in LONG_TERM_SETS
    ])
    
    LOA_EXPLANATION = f"""
### LoA Linguistic Chronology & Cycles ###

The Tahkmahnelle system fuses language, time, and cosmic history. Every foundational root (A-Z) 
serves as both a philosophical concept and the name for a cyclical period.

**Micro-Cycles (Intra-Age):**
- T-Days (5 total): Named by the roots **A** through **E** (e.g., 'ariatnah').
- T-Weeks (9 total): Named by the roots **F** through **N**.
- T-Months (3 total): Named by the roots **O** through **Q**.

**Macro-Cycles (Long-Term Chronology):**
These cycles define the eras and are governed by a rotating set of 7 **Primal Sets**.
- **Stahoy** (Decade): 10 T-Years.
- **Vraen** (Century): 10 Stahoys (100 T-Years).
- **Tetnobausse** (Millennium): 10 Vraen (1000 T-Years, named after root 't').

**The 7 Governing Sets:**
These sets cycle through the ages, defining the character of each Stahoy, Vraen, and Tetnobausse.
{LONG_TERM_SETS_STR}
"""
    print("=" * 90)
    print("      TAHKMAHNELLE LOA INDEX: LINGUISTIC & CHRONOLOGICAL GLOSSARY")
    print("=" * 90)
    print(LOA_EXPLANATION)
    print("-" * 90)
    
    if t_time:
        print(f"Current Chronological Sets (T-Year {t_time['T-Year']}):")
        print(f"  Millennium Set ({t_time['T_MILLENNIA']}. Tetnobausse): {t_time['tetnobausse_set']['root'].capitalize()}")
        print(f"  Century Set ({t_time['T_CENTURY_TOTAL']}. Vraen): {t_time['vraen_set']['root'].capitalize()}")
        print(f"  Decade Set ({t_time['T_DECADE_TOTAL']}. Stahoy): {t_time['stahoy_set']['root'].capitalize()}")
        print("-" * 90)
    
    input("Press Enter to return to the menu...")


# --- 3. Spatial System (X, Y, Z) Functions ---

def render_spatial_grid(x, y, z):
    """Renders a simplified ASCII 3D coordinate space visualization."""
    
    MAX_COORD = 10
    x_display = min(MAX_COORD, max(0, x))
    y_display = min(MAX_COORD, max(0, y))
    z_display = min(MAX_COORD, max(0, z))
    
    grid = []
    
    # Y-axis (vertical) - 11 lines (0 to 10)
    for row in range(MAX_COORD + 1):
        line = list("." * (MAX_COORD * 2 + 1))
        
        # Mark Y-axis label
        if row == MAX_COORD // 2:
            line.insert(0, 'Y')
        else:
            line.insert(0, ' ')
        
        # Draw the Z-axis (depth) projection line (runs diagonally up-left from origin (0,0))
        # This is a very rough representation
        
        # Place the current location marker '@'
        if row == MAX_COORD - y_display: 
            # X position is doubled for better ASCII spacing
            x_pos = 1 + x_display * 2 
            
            # Apply Z offset (pushing the marker diagonally up-left for perspective)
            # This is complex in 2D ASCII, so we simplify the horizontal displacement
            x_pos -= z_display // 2
            
            x_pos = max(1, min(len(line) - 1, x_pos))

            if 0 < x_pos < len(line) and 0 <= row < MAX_COORD + 1:
                line[x_pos] = '@'
                
        grid.append("".join(line))
        
    # Add X-axis label (horizontal)
    x_axis_label = " " + "0" + "--" * (MAX_COORD // 2) + "X" + "--" * (MAX_COORD // 2)
    grid.append(x_axis_label)
    
    # Key
    key = (
        f"Current Spatial Location: X={x}, Y={y}, Z={z}\n"
        f"Axes: Resources (X) | Knowledge (Y) | Depth (Z) | Range: (0-{MAX_COORD})"
    )
    
    return "\n".join(grid), key


# --- 4. Unified Visualizer (New Feature) ---

def run_unified_viz():
    """Runs the main display loop showing Time, Language context, and Space."""
    
    print("Starting Tahkmahnelle Omni-Viz (T-Year 5849)...")
    time.sleep(1) 
    
    UPDATE_INTERVAL = 0.046 # 46 milliseconds
    x, y, z = 5, 5, 5 # Initial spatial coordinates

    try:
        while True:
            now = datetime.datetime.now()
            t_time = get_tahkmahnelle_time(now)
            digital_out, analog_out = render_t_clock(t_time)
            grid_viz, spatial_key = render_spatial_grid(x, y, z)
            
            clear_screen()
            print("=" * 90)
            print("                 TAHKMAHNELLE OMNI-VISUALIZER (T-Year 5849)")
            print("=" * 90)
            
            # --- 1. TIME/CHRONOLOGY DISPLAY ---
            print("--- 1. SOLAR CHRONOLOGER ---")
            print(f"Current T-Time: {digital_out}")
            print(analog_out)
            print(f"W (Concise): T:{t_time['T-Tick']:03d} S:{t_time['T-Second']:01d} M:{t_time['T-Minute']:01d} H:{t_time['T-Hour']:01d} | D:{t_time['T-Day']:01d} Wk:{t_time['T-Week']:01d} Mo:{t_time['T-Month']:01d} | Yr:{t_time['T-Year']}")
            print("-" * 90)

            # --- 2. LANGUAGE/CYCLICAL CONTEXT DISPLAY ---
            print("--- 2. LINGUISTIC & MACRO-CYCLES (LoA Index) ---")
            print(f"Current **Age**: {t_time['T-Age']}")
            print(f"Micro-Cycle Names: Day **{t_time['T-Day-Name']}** | Week **{t_time['T-Week-Name']}** | Month **{t_time['T-Month-Name']}**")
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
            
            print(f"Real Time: {now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} | Update: {UPDATE_INTERVAL*1000}ms")
            print("Press Ctrl+C to return to the Main Menu and adjust coordinates.")
            
            time.sleep(UPDATE_INTERVAL) 
            
    except KeyboardInterrupt:
        # Allow user to update spatial coordinates before returning to menu
        clear_screen()
        print("\nOmni-Visualizer paused. Do you want to update the Spatial Coordinates?")
        
        while True:
            try:
                print(f"Current Position: X={x}, Y={y}, Z={z}")
                command = input("Enter command (X+N, Y-N, Z+N) or 'MENU': ").upper().strip()
                if command == 'MENU':
                    break
                
                if len(command) < 3 or command[1] not in ['+', '-'] or command[0] not in ['X', 'Y', 'Z']:
                    print("[Error] Invalid command. Try X+1 or Y-3.")
                    continue
                
                axis = command[0]
                op = command[1]
                value = int(command[2:])
                
                current_val = {'X': x, 'Y': y, 'Z': z}[axis]
                new_val = current_val + value if op == '+' else current_val - value
                new_val = max(0, min(10, new_val))
                
                if axis == 'X': x = new_val
                elif axis == 'Y': y = new_val
                elif axis == 'Z': z = new_val

                print(f"Position updated to X={x}, Y={y}, Z={z}.")

            except ValueError:
                print("[Error] Value must be an integer.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                
        clear_screen()
        print("Returned to Main Menu.")


def main_menu():
    """Presents the interactive command-line interface."""
    clear_screen()
    script_name = sys.argv[0] if sys.argv else "Tahkmahnelle_MegaViz.py"
    
    print("\n" + "#" * 90)
    print(f"      TAHKMAHNELLE MEGA-VISUALIZER: Time, Language, and Space ({script_name})")
    print("#" * 90)
    
    while True:
        print("\n--- Select a System View ---")
        print("1. Run Unified Visualizer (Continuous Real-Time Display)")
        print("2. Access LoA Index & Chronological Glossary")
        print("3. Exit Application")
        
        choice = input("Enter your choice (1-3): ").lower().strip()
        
        if choice == '1':
            run_unified_viz()
            clear_screen()
            print("Returned to Main Menu.")
        elif choice == '2':
            clear_screen()
            # Fetch time data once for context in the explanation
            now = datetime.datetime.now()
            t_time = get_tahkmahnelle_time(now)
            display_loa_explanation(t_time)
            clear_screen()
        elif choice == '3' or choice in ['exit', 'quit']:
            print("\nTahkmahnelle Mega-Visualizer offline. Synchronization complete.")
            break
        else:
            print("\n[Error] Invalid input. Please enter a number from 1 to 3.")

# --- Execution ---
if __name__ == "__main__":
    main_menu()

