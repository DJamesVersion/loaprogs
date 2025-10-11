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

# Age structure definitions
# The New Year starts *after* the Summer Solstice, meaning the cycle begins with the Autumn Equinox.
TAHKMAHNELLE_AGE_CYCLE = [
    # T-Year starts here (Autumn Equinox)
    {'key': 'C', 'name': 'The Age of Precedent (New Year)', 'date': (9, 22)},
    {'key': 'D', 'name': 'The Age of Transition', 'date': (12, 21)},
    {'key': 'A', 'name': 'The Age of Genesis', 'date': (3, 20)},
    {'key': 'B', 'name': 'The Age of Zenith', 'date': (6, 21)}
]

# --- Naming Cycles based on Phonology (A-Z) ---

# Get a sorted list of the root names
ROOT_NAMES = [d['root'] for k, d in sorted(TAHKMAHNELLE_DICTIONARY.items())]

def get_t_day_name(day_index):
    """Names the 5 T-Days using roots A-E (0-4)."""
    if 0 <= day_index < 5:
        # Use first 5 roots: ariatnah, batobwatchaeh, c'illiatnah, diadowatchaeh, eecheechuwah
        return ROOT_NAMES[day_index]
    return f"Day {day_index + 1}"

def get_t_week_name(week_index):
    """Names the 9 T-Weeks using roots F-N (0-8)."""
    if 0 <= week_index < 9:
        # Use roots F through N (index 5 to 13)
        return ROOT_NAMES[week_index + 5]
    return f"Week {week_index + 1}"

def get_t_month_name(month_index):
    """Names the 3 T-Months using roots O-Q (0-2)."""
    if 0 <= month_index < 3:
        # Use roots O through Q (index 14 to 16)
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
    age_start_date = None

    # Find the most recent age start date before or on the current time
    for start_date, age_data in reversed(age_starts):
        if start_date <= now:
            current_age_data = age_data
            age_start_date = start_date
            break
            
    # Calculate T-Year based on offset. If the New Year (Sep 22) has passed, use current year + offset.
    t_year = current_year + YEAR_OFFSET
    
    # If the current date is before the New Year (Sep 22) in the current year,
    # the T-Year is considered to be the *previous* T-Year, so subtract 1.
    new_year_marker = datetime.datetime(current_year, TAHKMAHNELLE_AGE_CYCLE[0]['date'][0], TAHKMAHNELLE_AGE_CYCLE[0]['date'][1])
    if now < new_year_marker and current_age_data['key'] in ['D', 'A', 'B']:
        # This correction is only needed if the current real year is part of the previous T-Year cycle
        # We rely on the sorted age_starts to correctly identify the current age and its start date.
        # The year offset handles the overall T-Year number.
        pass

    return current_age_data['name'], age_start_date, t_year


def get_tahkmahnelle_time(now):
    """Calculates all Tahkmahnelle time units."""
    
    current_age_name, age_start_date, t_year = get_current_t_age_and_year(now)
    
    # Calculate time elapsed since the start of the current Age
    time_in_age = now - age_start_date
    real_days_in_age = time_in_age.total_seconds() / REAL_SECONDS_PER_DAY
    
    # --- Month, Week, Day Calculation (Based on whole day units) ---
    
    days_in_month = T_WEEKS_PER_MONTH * T_DAYS_PER_WEEK
    
    # T-Month (Mo): 0-indexed within the T_MONTHS_PER_AGE cycle (0, 1, 2)
    t_month_index = math.floor(real_days_in_age / days_in_month) % T_MONTHS_PER_AGE
    t_month_display = t_month_index + 1 
    t_month_name = get_t_month_name(t_month_index)
    
    # Days elapsed since the start of the current T-Month (in real days)
    days_since_month_start = real_days_in_age % days_in_month
    
    # T-Week (Wk): 0-indexed within T_WEEKS_PER_MONTH (0-8)
    t_week_index = math.floor(days_since_month_start / T_DAYS_PER_WEEK) % T_WEEKS_PER_MONTH
    t_week_display = t_week_index + 1
    t_week_name = get_t_week_name(t_week_index)
    
    # Days elapsed since the start of the current T-Week (in real days)
    days_since_week_start = days_since_month_start % T_DAYS_PER_WEEK
    
    # T-Day (D): 0-indexed within T_DAYS_PER_WEEK (0-4)
    t_day_index = math.floor(days_since_week_start) % T_DAYS_PER_WEEK
    t_day_display = t_day_index + 1 
    t_day_name = get_t_day_name(t_day_index)
    
    # --- Hour, Minute, Second, Tick Calculation (Time within the day) ---
    
    # Total real seconds elapsed since midnight (0 to 86399.999...)
    real_seconds_in_day = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    
    # Conversion of real seconds to a high-precision T-Time index (T-Ticks total)
    total_t_index = (real_seconds_in_day * TOTAL_T_SECONDS_PER_DAY * T_TICKS_PER_SECOND) / REAL_SECONDS_PER_DAY
    
    # 5. T-Hours (H): 0-7
    t_hour_divisor = T_MINUTES_PER_HOUR * T_SECONDS_PER_MINUTE * T_TICKS_PER_SECOND
    t_hour = math.floor(total_t_index / t_hour_divisor) % T_HOURS_PER_DAY
    remaining_index = total_t_index % t_hour_divisor

    # 6. T-Minutes (M): 0-6
    t_minute_divisor = T_SECONDS_PER_MINUTE * T_TICKS_PER_SECOND
    t_minute = math.floor(remaining_index / t_minute_divisor) % T_MINUTES_PER_HOUR
    remaining_index = remaining_index % t_minute_divisor
    
    # 7. T-Seconds (S): 0-8
    t_second_divisor = T_TICKS_PER_SECOND
    t_second = math.floor(remaining_index / t_second_divisor) % T_SECONDS_PER_MINUTE
    remaining_index = remaining_index % t_second_divisor
    
    # 8. T-Ticks (T): 0-999
    t_tick = math.floor(remaining_index)
    
    return {
        'T-Tick': t_tick, 'T-Second': t_second, 'T-Minute': t_minute, 'T-Hour': t_hour,
        'T-Day': t_day_display, 'T-Week': t_week_display, 'T-Month': t_month_display,
        'T-Age': current_age_name, 'T-Year': t_year,
        'T-Day-Name': t_day_name, 'T-Week-Name': t_week_name, 'T-Month-Name': t_month_name
    }

# --- LoA Index Functions ---

LOA_EXPLANATION = """
### Tahkmahnelle Linguistic Chronology: The Lands of Ages (LoA) ###

The Tahkmahnelle system functions as a 'Chronologer,' fusing language and time.
Every foundational root (A-Z) serves as both a philosophical concept and the name for a cyclical period or holiday.

**Time Structure Mapping:**
The phonological roots (A-Z) are used hierarchically to name the Tahkmahnelle cycles:
- **T-Days (5 total):** Named by the roots **A** through **E**.
- **T-Weeks (9 total):** Named by the roots **F** through **N**.
- **T-Months (3 total):** Named by the roots **O** through **Q**.
- **Ages (4 total):** Defined by the Solstices/Equinoxes, cycling through the T-Year.

**T-Year Definition:**
The Tahkmahnelle New Year begins immediately following the Summer Solstice, coinciding with the Autumn Equinox (The Age of Precedent), which marks the start of the T-Year cycle.
"""

def display_loa_explanation():
    """Prints the comprehensive explanation of the LoA concept and time fusion."""
    print("=" * 80)
    print("      Tahkmahnelle Chronologer: LoA Linguistic and Time Explanation")
    print("=" * 80)
    print(LOA_EXPLANATION)
    print("-" * 80)

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

# --- Main Application Loop ---

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
            print(f"Current Real Time (RT): {now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} (Updates every {UPDATE_INTERVAL*1000}ms)")
            print("-" * 90)
            
            # W - ticks, seconds, minutes, hours, days, weeks, months, ages, year (concise running time)
            concise_output = (
                f"W - T:{t_time['T-Tick']:03d}, S:{t_time['T-Second']:01d}, M:{t_time['T-Minute']:01d}, H:{t_time['T-Hour']:01d}, "
                f"D:{t_time['T-Day']:01d}/{T_DAYS_PER_WEEK}, Wk:{t_time['T-Week']:01d}/{T_WEEKS_PER_MONTH}, "
                f"Mo:{t_time['T-Month']:01d}/{T_MONTHS_PER_AGE}, Yr:{t_time['T-Year']}"
            )
            
            print(f"Tahkmahnelle45time Index: {concise_output}")
            print("-" * 90)
            print(f"Current Age: {t_time['T-Age']}")
            print(f"Named Cycle (Holiday Cycle):")
            print(f"  T-Day: {t_time['T-Day-Name']} (Day {t_time['T-Day']})")
            print(f"  T-Week: {t_time['T-Week-Name']} (Week {t_time['T-Week']})")
            print(f"  T-Month: {t_time['T-Month-Name']} (Month {t_time['T-Month']})")
            print("=" * 90)
            print("Press Ctrl+C to return to the Main Menu.")
            
            time.sleep(UPDATE_INTERVAL) 
            
    except KeyboardInterrupt:
        clear_screen()
        print("\nTahkmahnelle Solar Clock stopped.")


def main_menu():
    """Presents the interactive command-line interface."""
    clear_screen()
    script_name = sys.argv[0] if sys.argv else "Tahkmahnelle_Chronologer.py"
    
    print("\n" + "#" * 80)
    print(f"      Tahkmahnelle Chronologer - LoA Index and Solar Clock ({script_name})")
    print("#" * 80)
    
    while True:
        print("\n--- Main Menu ---")
        print("1. Run Tahkmahnelle Solar Clock (T-Year 5849)")
        print("2. Read the LoA Linguistic and Chronology Explanation")
        print("3. Look up a specific Primal Root (Enter letter A-Z)")
        print("4. Exit Application")
        
        choice = input("Enter your choice (1-4) or a letter to look up: ").lower().strip()
        
        if choice == '1':
            run_solar_clock()
            clear_screen()
            print("Returned to Main Menu.")
        elif choice == '2':
            display_loa_explanation()
        elif choice == '3':
            query = input("Enter the single letter Age-Marker to look up: ").lower().strip()
            display_dictionary_entry(query)
        elif choice == '4' or choice in ['exit', 'quit']:
            print("\nTahkmahnelle Chronologer offline. Farewell.")
            break
        elif len(choice) == 1 and choice.isalpha():
            display_dictionary_entry(choice)
        else:
            print("\n[Error] Invalid input. Please enter a number (1-4) or a single letter for a dictionary lookup.")

# --- Execution ---
if __name__ == "__main__":
    main_menu()

