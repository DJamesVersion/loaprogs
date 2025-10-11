#!/bin/bash
#
# solar_clock.sh
#
# A shell script implementation of the conceptual solar clock.
#
# This script requires 'bc' for floating-point math.
# It is calibrated with the celestial event dates for the year 2025.
#
# To run this script:
# 1. Save it as solar_clock.sh
# 2. Make it executable: chmod +x solar_clock.sh
# 3. Run it from your terminal: ./solar_clock.sh
#
# The clock will start running. Press Ctrl+C to stop.

# --- Define the custom time system ---
WICKS_PER_MINUTE=9
MINUTES_PER_HOUR=7
HOURS_PER_DAY=8
DAYS_PER_WEEK=5
WEEKS_PER_MONTH=9
MONTHS_PER_AGE=3

# --- Pre-calculate total "wicks" for each period ---
WICKS_PER_HOUR=$((WICKS_PER_MINUTE * MINUTES_PER_HOUR))
WICKS_PER_DAY=$((WICKS_PER_HOUR * HOURS_PER_DAY))
WICKS_PER_WEEK=$((WICKS_PER_DAY * DAYS_PER_WEEK))
WICKS_PER_MONTH=$((WICKS_PER_WEEK * WEEKS_PER_MONTH))
WICKS_PER_AGE=$((WICKS_PER_MONTH * MONTHS_PER_AGE))

# --- Celestial Event Timestamps for 2025/2026 (in UTC) ---
# To perform calculations, we convert the UTC dates of equinoxes and solstices
# into Unix timestamps (seconds since the epoch).

# For the age before the March 2025 Equinox
DEC_SOLSTICE_2024_TS=$(date -u -d "2024-12-21T09:20:00Z" "+%s")

# Events for 2025
MAR_EQUINOX_2025_TS=$(date -u -d "2025-03-20T09:01:00Z" "+%s")
JUN_SOLSTICE_2025_TS=$(date -u -d "2025-06-21T02:42:00Z" "+%s")
SEP_EQUINOX_2025_TS=$(date -u -d "2025-09-22T18:19:00Z" "+%s")
DEC_SOLSTICE_2025_TS=$(date -u -d "2025-12-21T14:03:00Z" "+%s")

# First event of 2026 to define the end of the last age of 2025
MAR_EQUINOX_2026_TS=$(date -u -d "2026-03-20T14:45:00Z" "+%s")


# Function to handle Ctrl+C for a clean exit
cleanup() {
    echo -e "\nSolar clock stopped."
    exit 0
}
trap cleanup INT

echo "Initializing Solar Clock for 2025..."
echo "Press Ctrl+C to stop."

# Main loop to continuously update the time
while true; do
    # Get the current time as a UTC Unix timestamp
    now_ts=$(date -u "+%s")

    # --- Determine the current age based on the current timestamp ---
    if (( now_ts < MAR_EQUINOX_2025_TS )); then
        age_name="Winter"
        age_num=4
        age_start_ts=$DEC_SOLSTICE_2024_TS
        age_end_ts=$MAR_EQUINOX_2025_TS
    elif (( now_ts >= MAR_EQUINOX_2025_TS && now_ts < JUN_SOLSTICE_2025_TS )); then
        age_name="Spring"
        age_num=1
        age_start_ts=$MAR_EQUINOX_2025_TS
        age_end_ts=$JUN_SOLSTICE_2025_TS
    elif (( now_ts >= JUN_SOLSTICE_2025_TS && now_ts < SEP_EQUINOX_2025_TS )); then
        age_name="Summer"
        age_num=2
        age_start_ts=$JUN_SOLSTICE_2025_TS
        age_end_ts=$SEP_EQUINOX_2025_TS
    elif (( now_ts >= SEP_EQUINOX_2025_TS && now_ts < DEC_SOLSTICE_2025_TS )); then
        age_name="Autumn"
        age_num=3
        age_start_ts=$SEP_EQUINOX_2025_TS
        age_end_ts=$DEC_SOLSTICE_2025_TS
    else # After the December Solstice
        age_name="Winter"
        age_num=4
        age_start_ts=$DEC_SOLSTICE_2025_TS
        age_end_ts=$MAR_EQUINOX_2026_TS
    fi

    # --- Calculate the custom time ---
    total_age_duration_sec=$((age_end_ts - age_start_ts))
    elapsed_sec_in_age=$((now_ts - age_start_ts))

    # Use 'bc -l' for floating-point division to get the proportion of the age completed
    age_proportion=$(echo "scale=15; $elapsed_sec_in_age / $total_age_duration_sec" | bc -l)

    # Calculate total wicks passed and truncate to an integer
    total_wicks=$(echo "$age_proportion * $WICKS_PER_AGE" | bc)
    total_wicks=${total_wicks%.*} # Remove decimal part

    # Deconstruct total wicks into our custom time units
    remaining_wicks=$total_wicks
    
    # Months, Weeks, Days are 1-based
    months=$(( (remaining_wicks / WICKS_PER_MONTH) + 1 ))
    remaining_wicks=$((remaining_wicks % WICKS_PER_MONTH))
    
    weeks=$(( (remaining_wicks / WICKS_PER_WEEK) + 1 ))
    remaining_wicks=$((remaining_wicks % WICKS_PER_WEEK))
    
    days=$(( (remaining_wicks / WICKS_PER_DAY) + 1 ))
    remaining_wicks=$((remaining_wicks % WICKS_PER_DAY))
    
    # Hours, Minutes, Wicks are 0-based
    hours=$((remaining_wicks / WICKS_PER_HOUR))
    remaining_wicks=$((remaining_wicks % WICKS_PER_HOUR))
    
    minutes=$((remaining_wicks / WICKS_PER_MINUTE))
    wicks=$((remaining_wicks % WICKS_PER_MINUTE))

    # Format the output string
    time_str="$age_num.$months.$weeks.$days.$hours.$minutes.$wicks"
    display_string="${age_name} Age | Time: ${time_str}"
    
    # Use printf with '\r' to print on the same line, creating the update effect
    # The padding with spaces at the end clears any leftover characters from previous prints
    printf "\r%-40s" "$display_string"

    # Sleep for a fraction of a second
    sleep 0.1
done

