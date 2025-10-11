/*
 * solar_clock.c
 *
 * A C implementation of the conceptual solar clock.
 *
 * This program requires a C compiler (like GCC) and the standard C library.
 *
 * How to Compile and Run:
 * 1. Save this file as solar_clock.c
 * 2. Open your terminal and compile the program using GCC:
 * gcc solar_clock.c -o solar_clock -lm
 * (The '-lm' flag is important to link the math library for floor())
 *
 * 3. Run the compiled program:
 * ./solar_clock
 *
 * The clock will start running. Press Ctrl+C to stop.
 */

#include <stdio.h>
#include <time.h>
#include <unistd.h> // For usleep()
#include <math.h>   // For floor()
#include <signal.h> // For signal handling (Ctrl+C)
#include <stdlib.h> // For exit()

// --- Define the custom time system ---
const int WICKS_PER_MINUTE = 9;
const int MINUTES_PER_HOUR = 7;
const int HOURS_PER_DAY = 8;
const int DAYS_PER_WEEK = 5;
const int WEEKS_PER_MONTH = 9;
const int MONTHS_PER_AGE = 3;

// --- Pre-calculate total "wicks" for each period ---
const long WICKS_PER_HOUR = WICKS_PER_MINUTE * MINUTES_PER_HOUR;
const long WICKS_PER_DAY = WICKS_PER_HOUR * HOURS_PER_DAY;
const long WICKS_PER_WEEK = WICKS_PER_DAY * DAYS_PER_WEEK;
const long WICKS_PER_MONTH = WICKS_PER_WEEK * WEEKS_PER_MONTH;
const long WICKS_PER_AGE = WICKS_PER_MONTH * MONTHS_PER_AGE;


// Converts a date string (like "2025-03-20T09:01:00Z") to a time_t timestamp.
time_t get_utc_timestamp(const char* date_string) {
    struct tm tm = {0};
    // strptime parses the string into the tm struct
    strptime(date_string, "%Y-%m-%dT%H:%M:%SZ", &tm);
    // timegm converts the tm struct to a UTC timestamp
    return timegm(&tm);
}

// Function to handle Ctrl+C for a clean exit
void handle_sigint(int sig) {
    printf("\nSolar clock stopped.\n");
    exit(0);
}

int main() {
    // Register the signal handler for Ctrl+C
    signal(SIGINT, handle_sigint);

    // --- Celestial Event Timestamps for 2025/2026 (in UTC) ---
    // These are the key moments that define the "Ages".
    const time_t DEC_SOLSTICE_2024_TS = get_utc_timestamp("2024-12-21T09:20:00Z");
    const time_t MAR_EQUINOX_2025_TS = get_utc_timestamp("2025-03-20T09:01:00Z");
    const time_t JUN_SOLSTICE_2025_TS = get_utc_timestamp("2025-06-21T02:42:00Z");
    const time_t SEP_EQUINOX_2025_TS = get_utc_timestamp("2025-09-22T18:19:00Z");
    const time_t DEC_SOLSTICE_2025_TS = get_utc_timestamp("2025-12-21T14:03:00Z");
    const time_t MAR_EQUINOX_2026_TS = get_utc_timestamp("2026-03-20T14:45:00Z");

    printf("Initializing Solar Clock for 2025...\n");
    printf("Press Ctrl+C to stop.\n");

    // Main loop
    while (1) {
        time_t now_ts;
        time(&now_ts); // Get current time as a timestamp

        // Variables to hold the current age's properties
        const char* age_name;
        int age_num;
        time_t age_start_ts;
        time_t age_end_ts;

        // --- Determine the current age ---
        if (now_ts < MAR_EQUINOX_2025_TS) {
            age_name = "Winter";
            age_num = 4;
            age_start_ts = DEC_SOLSTICE_2024_TS;
            age_end_ts = MAR_EQUINOX_2025_TS;
        } else if (now_ts >= MAR_EQUINOX_2025_TS && now_ts < JUN_SOLSTICE_2025_TS) {
            age_name = "Spring";
            age_num = 1;
            age_start_ts = MAR_EQUINOX_2025_TS;
            age_end_ts = JUN_SOLSTICE_2025_TS;
        } else if (now_ts >= JUN_SOLSTICE_2025_TS && now_ts < SEP_EQUINOX_2025_TS) {
            age_name = "Summer";
            age_num = 2;
            age_start_ts = JUN_SOLSTICE_2025_TS;
            age_end_ts = SEP_EQUINOX_2025_TS;
        } else if (now_ts >= SEP_EQUINOX_2025_TS && now_ts < DEC_SOLSTICE_2025_TS) {
            age_name = "Autumn";
            age_num = 3;
            age_start_ts = SEP_EQUINOX_2025_TS;
            age_end_ts = DEC_SOLSTICE_2025_TS;
        } else {
            age_name = "Winter";
            age_num = 4;
            age_start_ts = DEC_SOLSTICE_2025_TS;
            age_end_ts = MAR_EQUINOX_2026_TS;
        }

        // --- Calculate the custom time ---
        double total_age_duration_sec = difftime(age_end_ts, age_start_ts);
        double elapsed_sec_in_age = difftime(now_ts, age_start_ts);
        
        double age_proportion = elapsed_sec_in_age / total_age_duration_sec;
        
        long total_wicks = (long)floor(age_proportion * WICKS_PER_AGE);
        
        long remaining_wicks = total_wicks;

        // Deconstruct total wicks into our custom time units
        int months = (remaining_wicks / WICKS_PER_MONTH) + 1;
        remaining_wicks %= WICKS_PER_MONTH;

        int weeks = (remaining_wicks / WICKS_PER_WEEK) + 1;
        remaining_wicks %= WICKS_PER_WEEK;

        int days = (remaining_wicks / WICKS_PER_DAY) + 1;
        remaining_wicks %= WICKS_PER_DAY;

        int hours = remaining_wicks / WICKS_PER_HOUR;
        remaining_wicks %= WICKS_PER_HOUR;

        int minutes = remaining_wicks / WICKS_PER_MINUTE;
        int wicks = remaining_wicks % WICKS_PER_MINUTE;

        // --- Format and display the output ---
        // Use carriage return '\r' to print on the same line.
        // The padding with spaces at the end clears any leftover characters.
        printf("\r%-10s Age | Time: %d.%d.%d.%d.%d.%d.%d      ", 
               age_name, age_num, months, weeks, days, hours, minutes, wicks);
        
        // Flush the output buffer to ensure the line is printed immediately.
        fflush(stdout);
        
        // Sleep for 100,000 microseconds (0.1 seconds)
        usleep(100000);
    }

    return 0;
}

