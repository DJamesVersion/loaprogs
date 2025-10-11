# solar_clock.py
#
# A Python script for a conceptual solar clock.
#
# To run this script, you first need to install the 'astral' library:
# pip install astral
#
# Then, execute the script from your terminal:
# python solar_clock.py
#
# The clock will start running and updating in place. Press Ctrl+C to stop.

import time
from datetime import datetime, timezone
import sys

try:
    # astral is used to get precise dates for solstices and equinoxes
    from astral.sun import equinoxes_and_solstices
except ImportError:
    print("Error: The 'astral' library is required.")
    print("Please install it using: pip install astral")
    sys.exit(1)

# --- Define the custom time system based on the prompt ---
# These constants define the structure of the custom time system.
WICKS_PER_MINUTE = 9
MINUTES_PER_HOUR = 7
HOURS_PER_DAY = 8
DAYS_PER_WEEK = 5
WEEKS_PER_MONTH = 9
MONTHS_PER_AGE = 3

# --- Pre-calculate total "wicks" for each period for efficiency ---
# This avoids recalculating these values in every loop.
WICKS_PER_HOUR = WICKS_PER_MINUTE * MINUTES_PER_HOUR
WICKS_PER_DAY = WICKS_PER_HOUR * HOURS_PER_DAY
WICKS_PER_WEEK = WICKS_PER_DAY * DAYS_PER_WEEK
WICKS_PER_MONTH = WICKS_PER_WEEK * WEEKS_PER_MONTH
WICKS_PER_AGE = WICKS_PER_MONTH * MONTHS_PER_AGE


def get_celestial_events(year):
    """
    Gets the UTC datetimes for the equinoxes and solstices of a given year.
    The events are returned in chronological order.
    """
    # The astral library provides the four key moments of the solar year.
    events = equinoxes_and_solstices(year)
    return sorted(events, key=lambda x: x.timestamp())


def find_current_age(now, events_this_year, events_next_year):
    """
    Determines the current age (season), its number, start time, and end time.
    Handles the transition between years seamlessly.
    """
    all_events = events_this_year + [events_next_year[0]]

    # Case 1: Before the first event of the year (Vernal Equinox).
    # This means we are in the 'Winter' age that began in the previous year.
    if now < all_events[0]:
        events_last_year = get_celestial_events(now.year - 1)
        start_event = events_last_year[3]  # Previous year's Winter Solstice
        end_event = all_events[0]          # This year's Vernal Equinox
        age_name = "Winter"
        age_number = 4
    # Case 2: Between Vernal Equinox and Summer Solstice.
    elif all_events[0] <= now < all_events[1]:
        age_name = "Spring"
        age_number = 1
        start_event = all_events[0]
        end_event = all_events[1]
    # Case 3: Between Summer Solstice and Autumnal Equinox.
    elif all_events[1] <= now < all_events[2]:
        age_name = "Summer"
        age_number = 2
        start_event = all_events[1]
        end_event = all_events[2]
    # Case 4: Between Autumnal Equinox and Winter Solstice.
    elif all_events[2] <= now < all_events[3]:
        age_name = "Autumn"
        age_number = 3
        start_event = all_events[2]
        end_event = all_events[3]
    # Case 5: After the Winter Solstice.
    else:
        age_name = "Winter"
        age_number = 4
        start_event = all_events[3]
        end_event = all_events[4]  # The Vernal Equinox of the next year.

    return age_name, age_number, start_event, end_event


def main():
    """Main function to run the solar clock."""
    print("Initializing Solar Clock...")
    last_year_checked = -1
    events_this_year = None
    events_next_year = None

    try:
        while True:
            now = datetime.now(timezone.utc)

            # To save resources, only fetch the celestial events when the year changes.
            if now.year != last_year_checked:
                print(f"Calibrating for the year {now.year}...")
                last_year_checked = now.year
                events_this_year = get_celestial_events(now.year)
                events_next_year = get_celestial_events(now.year + 1)

            # Determine the current age and its start/end boundaries.
            age_name, age_num, age_start, age_end = find_current_age(now, events_this_year, events_next_year)

            # Calculate the total duration of the current age in real-world seconds.
            total_age_duration_sec = (age_end - age_start).total_seconds()
            # Calculate how many real-world seconds have passed in this age.
            elapsed_sec_in_age = (now - age_start).total_seconds()

            # Find what fraction of the age has been completed.
            age_proportion = elapsed_sec_in_age / total_age_duration_sec

            # Convert the proportion of the age passed into the total number of "wicks" passed.
            total_wicks = int(age_proportion * WICKS_PER_AGE)

            # Deconstruct the total wicks into the custom time units using division and modulo.
            remaining_wicks = total_wicks
            
            # Note: Months, Weeks, and Days are 1-based (start from 1).
            months = (remaining_wicks // WICKS_PER_MONTH) + 1
            remaining_wicks %= WICKS_PER_MONTH
            
            weeks = (remaining_wicks // WICKS_PER_WEEK) + 1
            remaining_wicks %= WICKS_PER_WEEK
            
            days = (remaining_wicks // WICKS_PER_DAY) + 1
            remaining_wicks %= WICKS_PER_DAY
            
            # Note: Hours, Minutes, and Wicks are 0-based (start from 0).
            hours = remaining_wicks // WICKS_PER_HOUR
            remaining_wicks %= WICKS_PER_HOUR
            
            minutes = remaining_wicks // WICKS_PER_MINUTE
            wicks = remaining_wicks % WICKS_PER_MINUTE
            
            # --- Format and display the output ---
            # Format: AgeNumber.Month.Week.Day.Hour.Minute.Wick
            time_str = f"{age_num}.{months}.{weeks}.{days}.{hours}.{minutes}.{wicks}"
            
            # Use carriage return '\r' to print on the same line, creating an updating effect.
            # Use sys.stdout.flush() to ensure the output is shown immediately.
            display_string = f"\r{age_name} Age | Time: {time_str:<20}" # Padding for clean overwriting
            sys.stdout.write(display_string)
            sys.stdout.flush()

            # Sleep for a fraction of a second to create a running clock effect.
            time.sleep(1/9)

    except KeyboardInterrupt:
        print("\nSolar clock stopped.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")


if __name__ == "__main__":
    main()

