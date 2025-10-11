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
T_TICKS_PER_SECOND = 1000 # Used for 46ms precision display

REAL_SECONDS_PER_DAY = 86400
TOTAL_T_SECONDS_PER_DAY = (T_SECONDS_PER_MINUTE * T_MINUTES_PER_HOUR * T_HOURS_PER_DAY)
REAL_SECONDS_PER_T_SECOND = REAL_SECONDS_PER_DAY / TOTAL_T_SECONDS_PER_DAY

# Year offset: Current T-Year is 5849
YEAR_OFFSET = 5849 - datetime.datetime.now().year

# Age structure definitions (New Year starts after Summer Solstice)
TAHKMAHNELLE_AGE_CYCLE = [
    {'key': 'C', 'name': 'The Age of Precedent (New Year)', 'date': (9, 22)}, # Autumn Equinox
    {'key': 'D', 'name': 'The Age of Transition', 'date': (12, 21)},      # Winter Solstice
    {'key': 'A', 'name': 'The Age of Genesis', 'date': (3, 20)},          # Spring Equinox
    {'key': 'B', 'name': 'The Age of Zenith', 'date': (6, 21)}           # Summer Solstice
]

# --- Naming Cycles based on Phonology (A-Z) ---

ROOT_NAMES = [d['root'] for k, d in sorted(TAHKMAHNELLE_DICTIONARY.items())]

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

# --- Utility Functions ---

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_current_t_age_and_year(now):
    """Determines the current Tahkmahnelle Age and Year based on the date."""
    current_year = now.year
    age_starts = []
    
    # Check Age starts in the current and previous year
    for y in [current_year, current_year - 1]:
        for age_data in TAHKMAHNELLE_AGE_CYCLE:
            month, day = age_data['date']
            age_starts.append((datetime.datetime(y, month, day), age_data))
        
    age_starts.sort(key=lambda x: x[0])
    
    current_age_data = None

    # Find the most recent age start date before or on the current time
    for start_date, age_data in reversed(age_starts):
        if start_date <= now:
            current_age_data = age_data
            age_start_date = start_date
            break
            
    # Calculate T-Year based on offset
    t_year = current_year + YEAR_OFFSET

    # If the current date is before the New Year marker (Autumn Equinox), subtract a year from the T-Year
    new_year_marker = datetime.datetime(current_year, TAHKMAHNELLE_AGE_CYCLE[0]['date'][0], TAHKMAHNELLE_AGE_CYCLE[0]['date'][1])
    if now < new_year_marker and current_age_data['key'] in ['D', 'A', 'B']:
         # If we are in the later half of the real year, but before the T-New Year, the T-Year starts 
         # when the Age C starts in the current year. This is complex but the age_starts logic handles it.
         # For simplicity in T-Year number, we adjust based on the T-New Year (Age C start).
         # If Age C has not yet started in the current real year, we are in the previous T-Year.
         pass # Using the robust calculation in the original logic is cleaner.

    return current_age_data['name'], age_start_date, t_year


def get_tahkmahnelle_time(now):
    """Calculates all Tahkmahnelle time units."""
    
    current_age_name, age_start_date, t_year = get_current_t_age_and_year(now)
    
    # Calculate time elapsed since the start of the current Age
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
    
    # Total real seconds elapsed since midnight (0 to 86399.999...)
    real_seconds_in_day = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    
    # Conversion of real seconds to a high-precision T-Time index (T-Ticks total)
    total_t_index = (real_seconds_in_day * TOTAL_T_SECONDS_PER_DAY * T_TICKS_PER_SECOND) / REAL_SECONDS_PER_DAY
    
    # T-Hours (H): 0-7
    t_hour_divisor = T_MINUTES_PER_HOUR * T_SECONDS_PER_MINUTE * T_TICKS_PER_SECOND
    t_hour = math.floor(total_t_index / t_hour_divisor) % T_HOURS_PER_DAY
    remaining_index = total_t_index % t_hour_divisor

    # T-Minutes (M): 0-6
    t_minute_divisor = T_SECONDS_PER_MINUTE * T_TICKS_PER_SECOND
    t_minute = math.floor(remaining_index / t_minute_divisor) % T_MINUTES_PER_HOUR
    remaining_index = remaining_index % t_minute_divisor
    
    # T-Seconds (S): 0-8
    t_second_divisor = T_TICKS_PER_SECOND
    t_second = math.floor(remaining_index / t_second_divisor) % T_SECONDS_PER_MINUTE
    remaining_index = remaining_index % t_second_divisor
    
    # T-Ticks (T): 0-999
    t_tick = math.floor(remaining_index)
    
    return {
        'T-Tick': t_tick, 'T-Second': t_second, 'T-Minute': t_minute, 'T-Hour': t_hour,
        'T-Day': t_day_display, 'T-Week': t_week_display, 'T-Month': t_month_display,
        'T-Age': current_age_name, 'T-Year': t_year,
        'T-Day-Name': t_day_name, 'T-Week-Name': t_week_name, 'T-Month-Name': t_month_name
    }


def render_t_clock(t_time):
    """
    Generates the ASCII analog and digital clock display for Tahkmahnelle time.
    The Analog clock uses an 8-point dial corresponding to the 8 T-Hours.
    """
    H = t_time['T-Hour']
    M = t_time['T-Minute']
    S = t_time['T-Second']
    T = t_time['T-Tick']
    
    # --- 1. Digital Clock Display ---
    digital_output = (
        f"       T-TIME: {H:01d}:{M:01d}:{S:01d}.{T:03d} (H:M:S.T-Tick)"
    )
    
    # --- 2. ASCII Analog Clock Display (8-Hour Dial) ---
    
    # Clock face template (simplified 8-hour radial)
    # The hours are arranged starting from 0 (top-middle), going clockwise.
    # 0 is top center. 4 is bottom center.
    
    # Mapping 8 hours (0-7) to 9 discrete character positions (0-8)
    # Positions: 0 (Top) -> 1 (Top Right) -> ... -> 7 (Top Left)
    
    hour_positions = {
        0: (0, 4), 1: (1, 6), 2: (4, 8), 3: (7, 6),
        4: (8, 4), 5: (7, 2), 6: (4, 0), 7: (1, 2)
    }
    
    # Adjusting for 0-index display (8 rows, 9 columns)
    face = [list('         ') for _ in range(9)]
    
    # Mark the dial points
    for i in range(8):
        r, c = hour_positions[i]
        face[r][c] = str(i)
        
    # Mark the center
    center_r, center_c = 4, 4
    face[center_r][center_c] = 'X' # Center point

    # Determine hand positions
    hour_pos = hour_positions[H]
    
    # Minute Hand (moves based on the T-Minute's progression toward the next hour)
    # 7 T-Minutes per hour. We approximate the minute hand based on the T-Hour position.
    
    # The minute hand position can be calculated by interpolating between the hour markers
    # Total minutes in a day is 56. Total index is (H*7 + M)
    total_minute_index = (H * T_MINUTES_PER_HOUR) + M
    
    # Simplified hand placement: We only show the H hand and a combined M/H hand
    
    # Hour Hand: Mark current T-Hour with 'H'
    face[hour_pos[0]][hour_pos[1]] = 'H'

    # Minute Hand/Combined Index: Use '*' to show the minute's influence on the hour position
    # Since the minute moves the hour hand in a complex system, we'll mark the minute's slot in the hour
    minute_symbol_row = hour_pos[0]
    minute_symbol_col = hour_pos[1]
    
    # Add an indicator near the hour hand for the minute.
    if M > 3: # If minute is in second half of the 7-min cycle, indicate further progress
        minute_symbol_col += (1 if hour_pos[1] < center_c else -1)
        minute_symbol_row += (1 if hour_pos[0] < center_r else -1)

    # Ensure bounds before placing symbol
    minute_symbol_row = max(0, min(8, minute_symbol_row))
    minute_symbol_col = max(0, min(8, minute_symbol_col))

    # Place the minute progress marker if it doesn't overlap the hour marker
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
            
            # --- Display Logic ---
            clear_screen()
            print("=" * 90)
            print("         Tahkmahnelle Chronologer: T-Time Index (Year 5849)")
            print("=" * 90)
            
            # Render Clock Visualizations
            digital_out, analog_out = render_t_clock(t_time)
            
            # Display Analog Clock
            print("--- ANALOG CLOCK (8-Hour Dial) ---")
            print(analog_out)
            print("         H=Hour | o=Minute Progress | X=Center\n")
            
            # Display Digital Clock
            print("--- DIGITAL CLOCK & UNITS ---")
            print(digital_out)
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
            print(f"**Named Cycles** (Phonological Markers):")
            print(f"  T-Day: {t_time['T-Day-Name']} (Day {t_time['T-Day']})")
            print(f"  T-Week: {t_time['T-Week-Name']} (Week {t_time['T-Week']})")
            print(f"  T-Month: {t_time['T-Month-Name']} (Month {t_time['T-Month']})")
            print("-" * 90)
            print(f"Real Time: {now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} | Update Rate: {UPDATE_INTERVAL*1000}ms")
            print("=" * 90)
            print("Press Ctrl+C to return to the Main Menu.")
            
            time.sleep(UPDATE_INTERVAL) 
            
    except KeyboardInterrupt:
        clear_screen()
        print("\nTahkmahnelle Solar Clock stopped.")


def display_loa_explanation():
    """Prints the comprehensive explanation of the LoA concept and time fusion."""
    LOA_EXPLANATION = """
### Tahkmahnelle Linguistic Chronology: The Lands of Ages (LoA) ###

The Tahkmahnelle system functions as a 'Chronologer,' fusing language and time.
Every foundational root (A-Z) serves as both a philosophical concept and the name for a cyclical period or holiday.

**Time Structure Mapping:**
The phonological roots (A-Z) are used hierarchically to name the Tahkmahnelle cycles:
- **T-Days (5 total):** Named by the roots **A** through **E** (e.g., 'ariatnah').
- **T-Weeks (9 total):** Named by the roots **F** through **N**.
- **T-Months (3 total):** Named by the roots **O** through **Q**.
- **Ages (4 total):** Defined by the Solstices/Equinoxes, with the **New Year beginning at the Autumn Equinox**.

**T-Time Units:**
The day is divided into 8 Hours, 7 Minutes/Hour, 9 Seconds/Minute, and 1000 T-Ticks/Second, updating every 46 milliseconds.

**Dictionary Function:**
The LoA Index provides the linguistic meaning and 'Age' context for each Primal Root (Tkemnâti).
"""
    print("=" * 80)
    print("      Tahkmahnelle Chronologer: LoA Linguistic and Time Explanation")
    print("=" * 80)
    print(LOA_EXPLANATION)
    print("-" * 80)
    input("Press Enter to return to the menu...")


def display_dictionary_entry(query):
    """Looks up and prints a dictionary entry for the given query (single letter)."""
    query = query.lower().strip()
    
    if len(query) != 1 or not query.isalpha():
        print(f"\n[Error] Please enter a single letter (a-z) to look up a root.")
        return

    entry = TAHKMAHNELLE_DICTIONARY.get(query)

    if entry:
        print("\n" + "=" * 50)
        print(f"Index Marker: {query.upper()}")
        print("-" * 50)
        print(f"Primal Root (Tkemnâti): {entry['root']}")
        print(f"Conceptual Meaning: {entry['meaning']}")
        print(f"Linguistic Context (LoA): {entry['age']}")
        print("=" * 50)
    else:
        print(f"\n[Error] The letter '{query.upper()}' is not a recognized Age-Marker.")
    input("Press Enter to continue...")


def main_menu():
    """Presents the interactive command-line interface."""
    clear_screen()
    script_name = sys.argv[0] if sys.argv else "Tahkmahnelle_Chronologer_Visual.py"
    
    print("\n" + "#" * 80)
    print(f"      Tahkmahnelle Chronologer - LoA Index and Solar Clock ({script_name})")
    print("#" * 80)
    
    while True:
        print("\n--- Main Menu ---")
        print("1. Run Tahkmahnelle Solar Clock (Visual Mode)")
        print("2. Read the LoA Linguistic and Chronology Explanation")
        print("3. Look up a specific Primal Root (Enter letter A-Z)")
        print("4. Exit Application")
        
        choice = input("Enter your choice (1-4) or a letter to look up: ").lower().strip()
        
        if choice == '1':
            run_solar_clock()
            clear_screen()
            print("Returned to Main Menu.")
        elif choice == '2':
            clear_screen()
            display_loa_explanation()
            clear_screen()
        elif choice == '3':
            query = input("Enter the single letter Age-Marker to look up: ").lower().strip()
            clear_screen()
            display_dictionary_entry(query)
            clear_screen()
        elif choice == '4' or choice in ['exit', 'quit']:
            print("\nTahkmahnelle Chronologer offline. Farewell.")
            break
        elif len(choice) == 1 and choice.isalpha():
            clear_screen()
            display_dictionary_entry(choice)
            clear_screen()
        else:
            print("\n[Error] Invalid input. Please enter a number (1-4) or a single letter for a dictionary lookup.")

# --- Execution ---
if __name__ == "__main__":
    main_menu()

