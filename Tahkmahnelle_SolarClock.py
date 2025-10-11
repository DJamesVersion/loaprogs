import time
import datetime
import math
import os

# --- Tahkmahnelle Time System Constants ---

# Ratios defining the subdivisions of the T-Day (Tahkmahnelle Day)
T_SECONDS_PER_MINUTE = 9
T_MINUTES_PER_HOUR = 7
T_HOURS_PER_DAY = 8
T_DAYS_PER_WEEK = 5
T_WEEKS_PER_MONTH = 9
T_MONTHS_PER_AGE = 3
T_TICKS_PER_SECOND = 1000 # Used for high-precision display and calculation

# Real-world conversion constants
REAL_SECONDS_PER_DAY = 86400

# Total T-Seconds in one T-Day (504 T-Seconds)
TOTAL_T_SECONDS_PER_DAY = (T_SECONDS_PER_MINUTE * T_MINUTES_PER_HOUR * T_HOURS_PER_DAY)

# The duration of one T-Second in real-world seconds
REAL_SECONDS_PER_T_SECOND = REAL_SECONDS_PER_DAY / TOTAL_T_SECONDS_PER_DAY

# --- Age and Year Configuration ---

# The 4 Ages cycle through the year, tied to Equinox/Solstice events.
TAHKMAHNELLE_AGES = {
    'A': 'The Age of Genesis (Spring Equinox)',
    'B': 'The Age of Zenith (Summer Solstice)',
    'C': 'The Age of Precedent (Autumn Equinox)',
    'D': 'The Age of Transition (Winter Solstice)'
}

# Approximate month/day start points for the 4 ages in the Northern Hemisphere (used for simplicity)
AGE_START_DATES = [
    (3, 20, 'A'),   # Spring Equinox (Mar 20) -> Age A
    (6, 21, 'B'),   # Summer Solstice (Jun 21) -> Age B
    (9, 22, 'C'),   # Autumn Equinox (Sep 22) -> Age C
    (12, 21, 'D')   # Winter Solstice (Dec 21) -> Age D
]

# Year offset: Set the current real-world year to be displayed as T-Year 5849.
# We calculate the difference between the target year (5849) and a reference year (e.g., 2024)
YEAR_OFFSET = 5849 - datetime.datetime.now().year


def clear_screen():
    """Clears the console screen for continuous running time display."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_current_t_age(now):
    """
    Determines the current Tahkmahnelle Age and Year based on the real-world date.
    """
    current_year = now.year
    age_starts = []
    
    # Check Age starts in the current and previous year to find the most recent one
    for y in [current_year, current_year - 1]:
        for month, day, age_key in AGE_START_DATES:
            age_starts.append((datetime.datetime(y, month, day), age_key))
        
    age_starts.sort(key=lambda x: x[0])
    
    current_age = None
    age_start_date = None

    # Find the most recent age start date before or on the current time
    for start_date, age_key in reversed(age_starts):
        if start_date <= now:
            current_age = TAHKMAHNELLE_AGES[age_key]
            age_start_date = start_date
            break
            
    # Calculate T-Year based on offset
    t_year = now.year + YEAR_OFFSET
            
    return current_age, age_start_date, t_year


def get_tahkmahnelle_time(now):
    """
    Calculates the Tahkmahnelle time units based on the real-world timestamp.
    """
    
    # 1. Age (A), Age Start Date, and T-Year
    current_age_name, age_start_date, t_year = get_current_t_age(now)
    
    # Calculate time elapsed since the start of the current Age
    time_in_age = now - age_start_date
    real_days_in_age = time_in_age.total_seconds() / REAL_SECONDS_PER_DAY
    
    # --- Month, Week, Day Calculation (Based on whole day units) ---
    
    days_in_month = T_WEEKS_PER_MONTH * T_DAYS_PER_WEEK
    
    # T-Month (Mo): 0-indexed within the T_MONTHS_PER_AGE cycle
    t_month_index = math.floor(real_days_in_age / days_in_month) % T_MONTHS_PER_AGE
    t_month_display = t_month_index + 1 # 1-indexed for display
    
    # Days elapsed since the start of the current T-Month (in real days)
    days_since_month_start = real_days_in_age % days_in_month
    
    # T-Week (W): 0-indexed within T_WEEKS_PER_MONTH
    t_week_index = math.floor(days_since_month_start / T_DAYS_PER_WEEK) % T_WEEKS_PER_MONTH
    t_week_display = t_week_index + 1 # 1-indexed for display
    
    # Days elapsed since the start of the current T-Week (in real days)
    days_since_week_start = days_since_month_start % T_DAYS_PER_WEEK
    
    # T-Day (D): 0-indexed within T_DAYS_PER_WEEK
    t_day_index = math.floor(days_since_week_start) % T_DAYS_PER_WEEK
    t_day_display = t_day_index + 1 # 1-indexed for display
    
    # --- Hour, Minute, Second, Tick Calculation (Based on time within the day) ---
    
    # Total real seconds elapsed since midnight (0 to 86399.999...)
    real_seconds_in_day = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    
    # Conversion of real seconds to a high-precision T-Time index (T-Ticks total)
    # T-Index ranges from 0 to (TOTAL_T_SECONDS_PER_DAY * T_TICKS_PER_SECOND)
    total_t_index = (real_seconds_in_day * TOTAL_T_SECONDS_PER_DAY * T_TICKS_PER_SECOND) / REAL_SECONDS_PER_DAY
    
    # Total T-Ticks per T-Second (1000)
    TOTAL_TICKS_PER_SECOND = T_TICKS_PER_SECOND 
    
    # 5. T-Hours (H)
    t_hour_divisor = T_MINUTES_PER_HOUR * T_SECONDS_PER_MINUTE * TOTAL_TICKS_PER_SECOND
    t_hour = math.floor(total_t_index / t_hour_divisor) % T_HOURS_PER_DAY
    
    # Remaining index after hours
    remaining_index = total_t_index % t_hour_divisor

    # 6. T-Minutes (M)
    t_minute_divisor = T_SECONDS_PER_MINUTE * TOTAL_TICKS_PER_SECOND
    t_minute = math.floor(remaining_index / t_minute_divisor) % T_MINUTES_PER_HOUR
    
    # Remaining index after minutes
    remaining_index = remaining_index % t_minute_divisor
    
    # 7. T-Seconds (S)
    t_second_divisor = TOTAL_TICKS_PER_SECOND
    t_second = math.floor(remaining_index / t_second_divisor) % T_SECONDS_PER_MINUTE
    
    # 8. T-Ticks (T)
    t_tick = math.floor(remaining_index % t_second_divisor)
    
    return {
        'T-Tick': t_tick,
        'T-Second': t_second,
        'T-Minute': t_minute,
        'T-Hour': t_hour,
        'T-Day': t_day_display,
        'T-Week': t_week_display,
        'T-Month': t_month_display,
        'T-Age': current_age_name,
        'T-Year': t_year
    }


def run_clock():
    """Runs the main display loop."""
    
    print("Initializing Tahkmahnelle Solar Clock (Year 5849)...")
    time.sleep(1) 
    
    # Set the sleep interval to 46 milliseconds (0.046 seconds)
    UPDATE_INTERVAL = 0.046 
    
    try:
        while True:
            now = datetime.datetime.now()
            t_time = get_tahkmahnelle_time(now)
            
            # --- Display Logic ---
            clear_screen()
            print("=" * 90)
            print("         Tahkmahnelle Solar Clock: Lands of Ages Time Index (Year 5849)")
            print("=" * 90)
            print(f"Current Real Time (RT): {now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} (Updates every {UPDATE_INTERVAL*1000}ms)")
            print("-" * 90)
            
            # W - ticks, seconds, minutes, hours, days, weeks, months, ages, year
            # Concise output including T-Ticks and T-Year
            concise_output = (
                f"W - T:{t_time['T-Tick']:03d}, S:{t_time['T-Second']:01d}, M:{t_time['T-Minute']:01d}, H:{t_time['T-Hour']:01d}, "
                f"D:{t_time['T-Day']:01d}/{T_DAYS_PER_WEEK}, W:{t_time['T-Week']:01d}/{T_WEEKS_PER_MONTH}, "
                f"Mo:{t_time['T-Month']:01d}/{T_MONTHS_PER_AGE}"
            )
            
            print(f"Tahkmahnelle45time Index: {concise_output}")
            print("-" * 90)
            print(f"Current Age: {t_time['T-Age']}")
            print(f"Tahkmahnelle Year: {t_time['T-Year']}")
            print("=" * 90)
            print("Press Ctrl+C to stop the clock.")
            
            # Control the update speed
            time.sleep(UPDATE_INTERVAL) 
            
    except KeyboardInterrupt:
        clear_screen()
        print("\nTahkmahnelle Solar Clock stopped by user.")


if __name__ == "__main__":
    run_clock()

