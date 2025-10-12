import os
import time
import math
from datetime import datetime, timedelta

# --- ANSI COLOR CODES ---
class Color:
    HEADER = '\033[95m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    LORE = '\033[38;5;250m' # Light Gray
    SUN = '\033[38;5;208m'  # Orange/Yellow

# --- I. TAHKMAHNELLE TIME CONSTANTS & PHONOLOGY ---

# Phonology is used for cycle naming and lore reference
PHONOLOGY = {
    'a': 'ariatnah', 'b': 'batobwatchaeh', 'c': "c'illiatnah", 'd': 'diadowatchaeh', 'e': 'eecheechuwah',
    'f': "f'illianarre", 'g': 'gagoikenne', 'h': "h'uilliatachaeh", 'i': 'illianarre', 'j': 'ampejinne',
    'k': 'kajoinkenne', 'l': 'lenemketobontette', 'm': 'momaw', 'n': 'nona', 'o': 'oichenne', 'p': 'perfuvium',
    'q': 'quaristenne', 'r': 'roykenne', 's': 'stihuu', 'siataeh': 'siataeh', 't': 'tetnobautte', 
    'tahkmahnelle': 'tahkmahnelle', 'u': 'uilliatachaeh', 'v': 'vraelvrae', 'w': 'weetus', 
    'x': 'xiangxong', 'y': "y'uilliatachaeh", 'z': 'zazoykenne'
}

# Time Conversion Ratios
T_SECONDS_PER_MINUTE = 9
T_MINUTES_PER_HOUR = 7
T_HOURS_PER_DAY = 8  # 4 Day Hours, 4 Night Hours
T_DAYS_PER_WEEK = 5
T_WEEKS_PER_MONTH = 9
DAYS_IN_T_MONTH = T_WEEKS_PER_MONTH * T_DAYS_PER_WEEK  # 45 Earth days

T_SECONDS_PER_DAY = T_HOURS_PER_DAY * T_MINUTES_PER_HOUR * T_SECONDS_PER_MINUTE  # 504 T-Seconds
EARTH_SECONDS_PER_DAY = 86400
EARTH_SECONDS_PER_T_SECOND = EARTH_SECONDS_PER_DAY / T_SECONDS_PER_DAY # Approx. 171.428 seconds

# T-Day Names (based on indices 0-4)
T_DAY_NAMES = [
    PHONOLOGY['a'].upper(),  # 0
    PHONOLOGY['b'].upper(),  # 1
    PHONOLOGY['c'].upper(),  # 2
    PHONOLOGY['d'].upper(),  # 3
    PHONOLOGY['e'].upper()   # 4
]

# T-Year Reference (used for calendar alignment)
T_YEAR_REFERENCE = 2025 # The reference year for T-Day calculations

# --- II. HOLIDAYS AND RITUALS LORE ---

# Dictionary mapping T-Day of the T-Month (1-45) to a list of holidays/rituals
# Note: T-Days 1 to 45 are indexed 0 to 44
HOLIDAYS = {
    # Tahkmahnelle Planetary Days (T-Day 1, 10, 20)
    0: {"name": PHONOLOGY['v'] + " Day", "category": "Planetary", "lore": "A day of alignment and strategy, honoring the habitable worlds."}, 
    9: {"name": PHONOLOGY['t'] + " Day", "category": "Planetary", "lore": "A day for research and archiving, dedicated to the ancestral knowledge."},
    19: {"name": PHONOLOGY['s'] + " Day", "category": "Planetary", "lore": "A primary day of rest and cultural celebration on the main habitable moon."},
    
    # Jedi Festivals (T-Day 5, 15, 25, 35, 40)
    4: {"name": "Peace Day", "category": "Jedi Festivals", "lore": "A day of meditation and commitment to the Living Force."},
    14: {"name": "Eclipse Day", "category": "Jedi Festivals", "lore": "A rare day of profound introspection; silence and balance are mandated."},
    24: {"name": "Moon Day", "category": "Jedi Festivals", "lore": "Honoring the twin moons (Nona & Nano) and their influence on destiny."},
    34: {"name": "Solstice Day", "category": "Jedi Festivals", "lore": "The day to celebrate extremes and adaptability; marked by physical trials."},
    39: {"name": "Equinox Day", "category": "Jedi Festivals", "lore": "A day to achieve perfect harmony between light and darkness, structure and chaos."},

    # Martial Arts (T-Day 7, 17)
    6: {"name": "Samurai Bushido Ritual", "category": "Karate", "lore": "A ritual honoring discipline, honor, and loyalty; focus on form and precision."},
    16: {"name": "Ninja Kuji-Kiri Ceremony", "category": "Karate", "lore": "A secretive observance dedicated to stealth, infiltration, and mental resilience."},
    
    # Religious Observances (T-Day 12, 22)
    11: {"name": "Presbyterian Covenant Day", "category": "Religious", "lore": "A day dedicated to reaffirming spiritual agreements and community service."},
    21: {"name": "Yazidi Tawûsî Melek Feast", "category": "Religious", "lore": "A joyous feast celebrating the cycle of creation and renewal."},
}

# --- III. LORE INDEX (Static Explanations) ---

LORE_INDEX = f"""
{Color.HEADER}{Color.BOLD}=================================================================={Color.ENDC}
{Color.HEADER}{Color.BOLD}|                 TAHKMAHNELLE CHRONOSYSTEM EDICT                |{Color.ENDC}
{Color.HEADER}{Color.BOLD}=================================================================={Color.ENDC}
{Color.OKCYAN}The Tahkmahnelle Chronometer (Lenemkette) maps the complex 45-day cycle to Earth time.{Color.ENDC}

{Color.BOLD}A. TIME STRUCTURE (QUATERNARY METER){Color.ENDC}
-----------------------------------
- {Color.OKGREEN}T-Hours (8 per day):{Color.ENDC} The day is split into 8 hours (4 Day, 4 Night).
  - T-Minute: 7 T-Minutes per T-Hour.
  - T-Second: 9 T-Seconds per T-Minute.
  - T-Tick: 1000 T-Ticks per T-Second (for micro-precision).
- {Color.OKGREEN}T-Day (5 per week):{Color.ENDC} The cycle repeats every 5 days: 
  {', '.join(T_DAY_NAMES)}.
- {Color.OKGREEN}T-Week (9 per month):{Color.ENDC} There are 9 T-Weeks in every T-Month.
- {Color.OKGREEN}T-Month (45 Earth Days):{Color.ENDC} The core calendar cycle.

{Color.BOLD}B. DAY/NIGHT & LUNAR CYCLE{Color.ENDC}
-----------------------------------
- {Color.SUN}Day (ariatnah):{Color.ENDC} T-Hours 0 to 3. Period of activity, strategy, and resource gathering.
- {Color.HEADER}Night (siataeh):{Color.ENDC} T-Hours 4 to 7. Period of rest, deep thought, and archiving knowledge.
- {Color.WARNING}Lunar Cycle:{Color.ENDC} The habitable moon, Stihuu, has two satellites: Nona and Nano, tracked for astrological timing of deep space jumps.

{Color.BOLD}C. RITUALS AND HOLIDAYS INDEX (Mapped to T-Month Days 1-45){Color.ENDC}
--------------------------------------------------------------
{Color.BOLD}{Color.UNDERLINE}Planetary Cycle Lore:{Color.ENDC}
- {Color.FAIL}{HOLIDAYS[0]["name"]}: T-Day 1.{Color.ENDC} Focus on aggressive alignment and strategy.
- {Color.FAIL}{HOLIDAYS[9]["name"]}: T-Day 10.{Color.ENDC} Archiving and knowledge retrieval rituals.
- {Color.FAIL}{HOLIDAYS[19]["name"]}: T-Day 20.{Color.ENDC} System-wide cultural observation and rest.

{Color.BOLD}{Color.UNDERLINE}Jedi Festivals (Cosmic Alignment):{Color.ENDC}
- {Color.FAIL}{HOLIDAYS[4]["name"]}: T-Day 5.{Color.ENDC} Meditation on the Living Force.
- {Color.FAIL}{HOLIDAYS[14]["name"]}: T-Day 15.{Color.ENDC} Silent reflection during celestial phenomena.
- {Color.FAIL}{HOLIDAYS[24]["name"]}: T-Day 25.{Color.ENDC} Honoring the stability provided by Nona and Nano.
- {Color.FAIL}{HOLIDAYS[34]["name"]}: T-Day 35.{Color.ENDC} Physical endurance and extreme trial adaptation.
- {Color.FAIL}{HOLIDAYS[39]["name"]}: T-Day 40.{Color.ENDC} Seeking perfect balance and harmony.

{Color.BOLD}{Color.UNDERLINE}Earthly Faiths/Martial Disciplines:{Color.ENDC}
- {Color.FAIL}{HOLIDAYS[6]["name"]}: T-Day 7.{Color.ENDC} Samurai discipline and loyalty honor.
- {Color.FAIL}{HOLIDAYS[16]["name"]}: T-Day 17.{Color.ENDC} Ninja mental resilience and stealth techniques.
- {Color.FAIL}{HOLIDAYS[11]["name"]}: T-Day 12.{Color.ENDC} Presbyterian community service.
- {Color.FAIL}{HOLIDAYS[21]["name"]}: T-Day 22.{Color.ENDC} Yazidi celebration of renewal and creation.

{Color.HEADER}{Color.BOLD}=================================================================={Color.ENDC}
"""

# --- IV. T-TIME CALCULATION FUNCTIONS ---

def calculate_t_time(now):
    """Calculates all T-Time components from the current system time."""
    
    # 1. T-Time of Day
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    real_seconds_of_day = (now - midnight).total_seconds()
    
    # Convert real seconds to Tahkmahnelle seconds
    t_seconds_absolute = real_seconds_of_day / EARTH_SECONDS_PER_T_SECOND
    
    # H.M.S.
    t_hour = math.floor(t_seconds_absolute / (T_MINUTES_PER_HOUR * T_SECONDS_PER_MINUTE)) % T_HOURS_PER_DAY
    remaining_seconds = t_seconds_absolute % (T_MINUTES_PER_HOUR * T_SECONDS_PER_MINUTE)
    
    t_minute = math.floor(remaining_seconds / T_SECONDS_PER_MINUTE) % T_MINUTES_PER_HOUR
    t_second = math.floor(remaining_seconds % T_SECONDS_PER_MINUTE)
    
    # T-Tick (for the decimal part)
    t_tick_value = (remaining_seconds % T_SECONDS_PER_MINUTE) - t_second
    t_tick_display = math.floor(t_tick_value * 1000 / T_SECONDS_PER_MINUTE)
    
    # Day/Night Cycle
    day_night = PHONOLOGY['a'].upper() if t_hour < 4 else PHONOLOGY['siataeh'].upper()

    # 2. T-Calendar Metrics (relative to T-Month 45-day cycle)
    
    # Use a fixed reference date (Jan 1, T_YEAR_REFERENCE)
    reference_date = datetime(T_YEAR_REFERENCE, 1, 1)
    
    # Total days since reference date (with fraction for live update)
    total_days_since_reference = (now - reference_date).total_seconds() / EARTH_SECONDS_PER_DAY
    
    # T-Day index (0-44) with fraction for progress
    t_day_index_fractional = total_days_since_reference % DAYS_IN_T_MONTH
    t_day_index = math.floor(t_day_index_fractional)

    # T-Day Name (0-4)
    t_day_name = T_DAY_NAMES[t_day_index % T_DAYS_PER_WEEK]
    
    # T-Week Number (1-9)
    t_week = math.floor(t_day_index / T_DAYS_PER_WEEK) + 1
    
    return {
        "T_H": t_hour, "T_M": t_minute, "T_S": t_second, "T_TICK": t_tick_display,
        "Day_Night": day_night,
        "T_DayIndex": t_day_index,
        "T_DayName": t_day_name,
        "T_Week": t_week,
        "Month_Progress": (t_day_index_fractional / DAYS_IN_T_MONTH) * 100
    }

def get_active_holiday(t_day_index):
    """Checks if the current T-Day index corresponds to a known holiday."""
    return HOLIDAYS.get(t_day_index, None)

def draw_chronometer(td):
    """Renders the live chronometer status in the console."""
    
    # Clear screen (only needed for the live clock loop)
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    print(LORE_INDEX) # Print the static index

    print(f"\n{Color.WARNING}{Color.BOLD}================ LIVE CHRONOMETER STATUS ================{Color.ENDC}")

    # --- T-TIME & DAY/NIGHT ---
    time_color = Color.OKCYAN if td['Day_Night'] == PHONOLOGY['a'].upper() else Color.HEADER
    
    print(f"\n{Color.BOLD}CURRENT T-TIME:{Color.ENDC}")
    print(f"  {time_color}{td['T_H']}:{td['T_M']}:{td['T_S']}.{str(td['T_TICK']).zfill(3)}{Color.ENDC}")
    print(f"  Phase: {time_color}{td['Day_Night']} ({td['T_H']} T-Hour){Color.ENDC}")
    
    # --- T-CALENDAR ---
    print(f"\n{Color.BOLD}TAHKMAHNELLE CALENDAR:{Color.ENDC}")
    print(f"  {Color.OKGREEN}T-Day Name:{Color.ENDC} {td['T_DayName']}")
    print(f"  {Color.OKGREEN}T-Week:{Color.ENDC} {td['T_Week']} of {T_WEEKS_PER_MONTH}")
    print(f"  {Color.OKGREEN}T-Day Index:{Color.ENDC} {td['T_DayIndex'] + 1} of {DAYS_IN_T_MONTH}")
    
    # --- PROGRESS BAR ---
    progress = int(td['Month_Progress'])
    bar_length = 40
    filled = int(bar_length * progress / 100)
    bar = "█" * filled + "-" * (bar_length - filled)
    print(f"  {Color.OKCYAN}T-Month Progress:{Color.ENDC} [{bar}] {progress:.2f}%")

    # --- HOLIDAY STATUS ---
    active_holiday = get_active_holiday(td['T_DayIndex'])
    
    print(f"\n{Color.BOLD}RITUAL LORE STATUS:{Color.ENDC}")
    
    if active_holiday:
        print(f"  {Color.FAIL}{Color.BOLD}ACTIVE HOLIDAY!{Color.ENDC}")
        print(f"  {Color.FAIL}Event:{Color.ENDC} {active_holiday['name']} ({active_holiday['category']})")
        print(f"  {Color.LORE}Lore/Ritual:{Color.ENDC} {active_holiday['lore']}")
    else:
        print(f"  {Color.LORE}No major ritual active on this T-Day.{Color.ENDC}")

    print(f"\n{Color.WARNING}Press Ctrl+C to stop.{Color.ENDC}")


# --- V. MAIN EXECUTION LOOP ---

def main():
    """Runs the live chronometer."""
    
    # Print the index once cleanly before starting the loop
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
        
    print(LORE_INDEX)
    input(f"{Color.BOLD}Press ENTER to launch the live Tahkmahnelle Chronometer...{Color.ENDC}")

    try:
        while True:
            now = datetime.now()
            td = calculate_t_time(now)
            draw_chronometer(td)
            
            # The T-Tick is roughly 46ms. We'll refresh faster than that for smoothness.
            time.sleep(0.04) 

    except KeyboardInterrupt:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        print(f"{Color.BOLD}\nTahkmahnelle Chronometer Terminated.{Color.ENDC}")

if __name__ == "__main__":
    main()

