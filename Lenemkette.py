import datetime
import time
import math
import os
import sys

# --- I. TAHKMAHNELLE LINGUISTIC & CHRONOLOGICAL DATABASE ---

# Dictionary for naming conventions
TAHKMAHNELLE_DICTIONARY = {
    'a': 'ariatnah', 'b': 'batobwatchaeh', 'c': "c'illiatnah", 'd': 'diadowatchaeh', 'e': 'eecheechuwah',
    'f': "f'illianarre", 'g': 'gagoikenne', 'h': "h'uilliatachaeh", 'i': 'illianarre', 'j': 'ampejinne',
    'k': 'kajoinkenne', 'l': 'lenemketobontette', 'm': 'momaw', 'n': 'nona',
    'o': 'oichenne', 'p': 'perfuvium', 'q': 'quaristenne',
}
ROOT_NAMES = [v for k, v in sorted(TAHKMAHNELLE_DICTIONARY.items(), key=lambda item: item[0])]

# 7 Cycle Sets for Macro Time (Ariats, Batos, C'illias, etc. - based on first 7 roots)
CYCLE_SETS = ROOT_NAMES[:7]

# 4 Ages tied to Solstices/Equinoxes (New Year is Autumn Equinox)
TAHKMAHNELLE_AGE_CYCLE = [
    {'key': 'C', 'name': 'The Age of Precedent', 'date': (9, 22)}, # Autumn Equinox
    {'key': 'D', 'name': 'The Age of Transition', 'date': (12, 21)}, # Winter Solstice
    {'key': 'A', 'name': 'The Age of Genesis', 'date': (3, 20)},  # Spring Equinox
    {'key': 'B', 'name': 'The Age of Zenith', 'date': (6, 21)}    # Summer Solstice
]

# --- II. TIME SYSTEM CONSTANTS ---

# Solar Clock (T-Hour, T-Minute, T-Second)
T_SECONDS_PER_MINUTE = 9
T_MINUTES_PER_HOUR = 7
T_HOURS_PER_DAY = 8
T_TICKS_PER_SECOND = 1000 # For 46ms precision visualization

# Calendar Cycles
T_DAYS_PER_WEEK = 5
T_WEEKS_PER_MONTH = 9
T_MONTHS_PER_AGE = 3 # 12 T-Months total (4 Ages * 3 Months)

# Calculated constants
DAYS_IN_T_MONTH = T_WEEKS_PER_MONTH * T_DAYS_PER_WEEK # 45 real days
EARTH_SECONDS_PER_DAY = 86400
T_SECONDS_PER_DAY = T_HOURS_PER_DAY * T_MINUTES_PER_HOUR * T_SECONDS_PER_MINUTE
EARTH_SECONDS_PER_T_SECOND = EARTH_SECONDS_PER_DAY / T_SECONDS_PER_DAY
T_TICK_SLEEP_TIME = 0.046 # 46ms refresh rate

# T-Year offset (5849 is the reference T-Year, aligned with 2025)
YEAR_OFFSET = 5849 - 2025
T_YEAR_REFERENCE = 2025

# --- III. CHRONOLOGICAL MAPPING FUNCTIONS ---

def get_t_day_name(day_index):
    """Names the 5 T-Days using roots A-E (Indices 0-4)."""
    return ROOT_NAMES[day_index % T_DAYS_PER_WEEK]

def get_t_month_name(month_index):
    """Names the 3 T-Months using roots O-Q (Indices 14-16) across the 4 T-Ages."""
    return ROOT_NAMES[(month_index % T_MONTHS_PER_AGE) + T_DAYS_PER_WEEK + T_WEEKS_PER_MONTH]

def get_current_t_age_and_year(date: datetime.date):
    """Determines the current Tahkmahnelle Age and Year based on the date."""
    current_year = date.year
    now = datetime.datetime(date.year, date.month, date.day)
    age_starts = []
    
    for y in [current_year, current_year - 1]:
        for age_data in TAHKMAHNELLE_AGE_CYCLE:
            month, day = age_data['date']
            try:
                age_starts.append((datetime.datetime(y, month, day), age_data))
            except ValueError:
                continue
        
    age_starts.sort(key=lambda x: x[0])
    current_age_data = None

    for start_date, age_data in reversed(age_starts):
        if start_date <= now:
            current_age_data = age_data
            break
            
    t_year = current_year + YEAR_OFFSET
    return current_age_data['name'], t_year

def get_macro_cycle_name(t_year, cycle_length):
    """Returns the name (Ariat, Bato, etc.) for Stahoy, Vraen, or Tetnobausse."""
    # Use modulo 7 on the cycle number to select the name from the 7 sets
    cycle_index = (t_year // cycle_length) % 7
    return CYCLE_SETS[cycle_index].capitalize()

def calculate_t_time_components(now: datetime.datetime, current_t_year):
    """Calculates all solar, calendar, and macro time components."""
    
    # --- 1. Solar/Hourly Time ---
    
    # Get Earth seconds since midnight (0 to 86399.999...)
    real_seconds_of_day = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    
    # Convert real seconds to Tahkmahnelle seconds (0 to T_SECONDS_PER_DAY - 1)
    t_seconds_absolute = real_seconds_of_day / EARTH_SECONDS_PER_T_SECOND
    
    t_hour = math.floor(t_seconds_absolute / (T_MINUTES_PER_HOUR * T_SECONDS_PER_MINUTE)) % T_HOURS_PER_DAY
    remaining_seconds = t_seconds_absolute % (T_MINUTES_PER_HOUR * T_SECONDS_PER_MINUTE)
    
    t_minute = math.floor(remaining_seconds / T_SECONDS_PER_MINUTE) % T_MINUTES_PER_HOUR
    remaining_seconds = remaining_seconds % T_SECONDS_PER_MINUTE
    
    t_second = math.floor(remaining_seconds) % T_SECONDS_PER_MINUTE
    t_tick = math.floor((remaining_seconds - t_second) * T_TICKS_PER_SECOND) % T_TICKS_PER_SECOND

    # --- 2. Calendar Time (Day, Week, Month) ---
    
    reference_date = datetime.date(T_YEAR_REFERENCE, 1, 1)
    total_days_since_reference = (now.date() - reference_date).days 
    
    # T-Month Index (0-11)
    t_month_index_absolute = math.floor(total_days_since_reference / DAYS_IN_T_MONTH) % 12
    t_month_name = get_t_month_name(t_month_index_absolute)
    
    # Day Index within the current T-Month (0-44)
    day_of_t_month_index = total_days_since_reference % DAYS_IN_T_MONTH
    t_day_of_month = day_of_t_month_index + 1 # 1 to 45
    
    # T-Day and T-Week
    t_day_index = day_of_t_month_index % T_DAYS_PER_WEEK
    t_day_name = get_t_day_name(t_day_index)
    t_week_of_month = math.floor(day_of_t_month_index / T_DAYS_PER_WEEK) + 1
    
    # --- 3. Macro Cycles (Stahoy, Vraen, Tetnobausse) ---

    tetnobausse_name = get_macro_cycle_name(current_t_year, 1000)
    vraen_name = get_macro_cycle_name(current_t_year, 100)
    stahoy_name = get_macro_cycle_name(current_t_year, 10)
    
    return {
        'T-H': t_hour, 'T-M': t_minute, 'T-S': t_second, 'T-TICK': t_tick,
        'T-DayName': t_day_name.capitalize(), 'T-DayNum': t_day_of_month,
        'T-WkNum': t_week_of_month, 'T-WkMax': T_WEEKS_PER_MONTH,
        'T-MonthName': t_month_name.capitalize(), 'T-MonthAbs': t_month_index_absolute + 1,
        'T-Y': current_t_year,
        'T-Tetnobausse': tetnobausse_name,
        'T-Vraen': vraen_name,
        'T-Stahoy': stahoy_name
    }

# --- IV. VISUALIZATION AND INTERACTION ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_analog_clock(t_hour):
    """Draws a simple 8-hour ASCII analog clock face."""
    face = ['|', '/', '-', '\\', '|', '/', '-', '\\']
    pointer = face[t_hour % 8]
    
    analog = [
        "   |       ",
        " - | -     ",
        f"   {pointer}       ",
        "  LENEMKETTE ",
        f"   {pointer}       ",
        " - | -     ",
        "   |       ",
    ]
    # Simple placement for visualization purposes
    if t_hour == 0: analog[0] = "   ^   "
    elif t_hour == 1: analog[1] = "  / \\  "
    elif t_hour == 2: analog[3] = "-   -  "
    elif t_hour == 3: analog[3] = "-   >  " # Placeholder for right
    elif t_hour == 4: analog[4] = "  \\ /  "
    elif t_hour == 5: analog[5] = "   v   "
    elif t_hour == 6: analog[6] = "   |   "
    elif t_hour == 7: analog[1] = "<   -  " # Placeholder for left
        
    return "\n".join(analog)

def display_lenemkette(time_data, spatial_coords):
    """Renders the entire Lenemkette display."""
    
    h = time_data['T-H']
    m = time_data['T-M']
    s = time_data['T-S']
    t = time_data['T-TICK']
    
    # --- TIME: SOLAR / HOURLY ---
    time_display = f"""
|---------------------------------------------------------|
|                LENEMKETTE OMNI-CHRONOMETER              |
|---------------------------------------------------------|
|         T-HOURLY TIME (8H:7M:9S.1000TICK)               |
|                                                         |
|  ANALOG:           DIGITAL: {h:01}:{m:01}:{s:01}.{t:03}
{draw_analog_clock(h)}
|---------------------------------------------------------|
"""

    # --- TIME: CALENDAR / CYCLICAL ---
    calendar_display = f"""
|         T-CALENDAR (Year {time_data['T-Y']} Tahkmahnelle45time)         |
|---------------------------------------------------------|
|  T-AGE:       | {time_data['T-Age']}                                   |
|  T-MONTH:     | {time_data['T-MonthName']} ({time_data['T-MonthAbs']}/12)              |
|  T-WEEK:      | Week {time_data['T-WkNum']} of {time_data['T-WkMax']} (Named after a root)        |
|  T-DAY:       | {time_data['T-DayName']} (Day {time_data['T-DayNum']}/45)                |
|---------------------------------------------------------|
"""

    # --- TIME: MACRO CYCLES (Ariats Sets) ---
    macro_display = f"""
|         T-MACRO CYCLES (Governed by 7 Ariats Sets)      |
|---------------------------------------------------------|
|  T-TETNOBAUSSE (Millennium): | Aligned with **{time_data['T-Tetnobausse']}** (Set {((time_data['T-Y'] // 1000) % 7) + 1}/7) |
|  T-VRAEN (Century):          | Aligned with **{time_data['T-Vraen']}** (Set {((time_data['T-Y'] // 100) % 7) + 1}/7)        |
|  T-STAHOY (Decade):          | Aligned with **{time_data['T-Stahoy']}** (Set {((time_data['T-Y'] // 10) % 7) + 1}/7)         |
|---------------------------------------------------------|
"""
    
    # --- SPACE: X, Y, Z SYSTEMS ---
    space_display = f"""
|         SYSTEMS OF SPACES (Resources, Library)          |
|---------------------------------------------------------|
|  X (Resources): | {spatial_coords['x']:<20}    | Controls: (A/D)       |
|  Y (Library):   | {spatial_coords['y']:<20}    | Controls: (W/S)       |
|  Z (Archives):  | {spatial_coords['z']:<20}    | Controls: (Q/E)       |
|---------------------------------------------------------|
| Press Ctrl+C at any time to adjust coordinates.         |
"""
    
    clear_screen()
    print(time_display)
    print(calendar_display)
    print(macro_display)
    print(space_display)


def run_lenemkette():
    """Initializes and runs the main Lenemkette loop."""
    spatial_coords = {'x': 100, 'y': 200, 'z': 300}

    # Setup terminal for non-blocking input (only used for Ctrl+C handling)
    try:
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd)
    except Exception:
        # Pass if tty/termios are unavailable (e.g., non-Linux/MacOS environment)
        pass

    try:
        while True:
            now = datetime.datetime.now()
            t_age, t_year = get_current_t_age_and_year(now.date())
            time_data = calculate_t_time_components(now, t_year)
            
            # Add T-Age to time_data for display
            time_data['T-Age'] = t_age
            
            display_lenemkette(time_data, spatial_coords)
            
            # Sleep for 46ms to simulate the T-Tick rate
            time.sleep(T_TICK_SLEEP_TIME)

    except KeyboardInterrupt:
        # Pause clock to adjust spatial coordinates
        clear_screen()
        print("\n--- LENEMKETTE PAUSED: COORDINATE ADJUSTMENT ---")
        print(f"Current Coordinates: X={spatial_coords['x']}, Y={spatial_coords['y']}, Z={spatial_coords['z']}")
        
        while True:
            try:
                # Read user input for movement commands
                print("\nAdjust (A/D: X) | (W/S: Y) | (Q/E: Z) | (R: Resume) | (X: Exit)")
                
                # Check for input without waiting
                if sys.stdin in [sys.stdin]:
                    try:
                        char = sys.stdin.read(1)
                    except IOError:
                        char = ''

                    if char in 'aA': spatial_coords['x'] -= 10
                    elif char in 'dD': spatial_coords['x'] += 10
                    elif char in 'wW': spatial_coords['y'] += 10
                    elif char in 'sS': spatial_coords['y'] -= 10
                    elif char in 'qQ': spatial_coords['z'] -= 10
                    elif char in 'eE': spatial_coords['z'] += 10
                    elif char in 'rR': break
                    elif char in 'xX': raise SystemExit
                    
                    if char:
                        clear_screen()
                        print("\n--- LENEMKETTE PAUSED: COORDINATE ADJUSTMENT ---")
                        print(f"New Coordinates: X={spatial_coords['x']}, Y={spatial_coords['y']}, Z={spatial_coords['z']}")
                        
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                break # Exit the adjustment loop and the main program
            except EOFError:
                break # Handle EOF during input
    
    except SystemExit:
        pass # Clean exit

    finally:
        # Restore terminal settings
        try:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except Exception:
            pass
        clear_screen()
        print("Lenemkette terminated. All systems offline.")

if __name__ == "__main__":
    # Check for necessary libraries (tty/termios for non-blocking input on Unix-like systems)
    if os.name == 'nt' and (sys.version_info.major == 3 and sys.version_info.minor < 7):
        # On Windows, non-blocking input is complex. Simplifying for core function.
        print("Note: Advanced terminal controls (non-blocking input) may be limited on this OS.")
    
    run_lenemkette()

