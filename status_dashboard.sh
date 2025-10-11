#!/bin/bash

# =================================================================
# Unix Status Dashboard Script
# Author: Gemini
# Description: Displays real-time status for Wi-Fi, Bluetooth, Battery,
#              Date/Time, Calendar, and Network Location in the terminal.
# Designed for macOS/BSD-like systems, with notes for Linux users.
# =================================================================

# --- Configuration ---
REFRESH_RATE=3 # Seconds between updates
WIFI_INTERFACE="en0" # Change to 'wlan0' or similar for Linux

# --- ANSI Color Codes ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# --- Utility Functions ---

# Function to get Wi-Fi status (macOS-specific)
get_wifi_status() {
    # Check if networksetup (macOS tool) exists
    if command -v networksetup &> /dev/null; then
        SSID=$(/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | awk '/ SSID:/ {print $2}')
        POWER=$(networksetup -getairportpower "$WIFI_INTERFACE" | awk '{print $NF}')

        if [[ "$POWER" == "On" && -n "$SSID" ]]; then
            echo -e "${GREEN}Status: Connected${NC} | SSID: $SSID"
        elif [[ "$POWER" == "On" ]]; then
            echo -e "${YELLOW}Status: Enabled${NC} | Not Connected"
        else
            echo -e "${RED}Status: Off${NC}"
        fi
    else
        # Placeholder for Linux (requires 'nmcli' or 'iwctl'/'ip a')
        echo -e "${MAGENTA}Wi-Fi Status: Use 'nmcli' or 'ip a' on Linux.${NC}"
    fi
}

# Function to get Bluetooth status (macOS-specific)
get_bluetooth_status() {
    # Check if system_profiler (macOS tool) exists
    if command -v system_profiler &> /dev/null; then
        STATUS=$(system_profiler SPBluetoothDataType 2>/dev/null | awk '/  State:/{print $2}')
        if [[ "$STATUS" == "On" ]]; then
            echo -e "${GREEN}Status: Enabled${NC}"
        elif [[ "$STATUS" == "Off" ]]; then
            echo -e "${RED}Status: Disabled${NC}"
        else
            echo -e "${YELLOW}Status: Unknown${NC}"
        fi
    else
        # Placeholder for Linux (requires 'bluetoothctl' or 'hcitool')
        echo -e "${MAGENTA}Bluetooth Status: Use 'bluetoothctl' on Linux.${NC}"
    fi
}

# Function to get Battery status (macOS-specific)
get_battery_status() {
    # Check if pmset (macOS tool) exists
    if command -v pmset &> /dev/null; then
        BATTERY_INFO=$(pmset -g batt | grep -E "(\d+%)|charged")
        PERCENT=$(echo "$BATTERY_INFO" | awk -F'\t' '{print $NF}' | grep -oE '[0-9]+%')
        STATE=$(echo "$BATTERY_INFO" | grep -oE "charging|charged|discharging")

        if [[ "$PERCENT" == *% ]]; then
            if [[ "$STATE" == "charging" ]]; then
                ICON="⚡"
                COLOR=$YELLOW
            elif [[ "$STATE" == "charged" ]]; then
                ICON="✅"
                COLOR=$GREEN
            elif [[ "$STATE" == "discharging" ]]; then
                ICON="🔋"
                # Set color based on level
                LEVEL_NUM=$(echo "$PERCENT" | tr -d '%')
                if [ "$LEVEL_NUM" -le 20 ]; then
                    COLOR=$RED
                else
                    COLOR=$GREEN
                fi
            else
                ICON="?"
                COLOR=$YELLOW
            fi
            echo -e "${COLOR}$ICON Level: $PERCENT | State: $STATE${NC}"
        else
            echo -e "${BLUE}Desktop/AC Power${NC}"
        fi
    else
        # Placeholder for Linux (requires 'upower' or /sys/class/power_supply)
        echo -e "${MAGENTA}Battery Status: Use 'upower' or check /sys/class/power_supply on Linux.${NC}"
    fi
}

# Function to get Location (IP-based Geolocation)
get_location() {
    # Using an external service is the simplest way to get city/region from the terminal.
    LOCATION=$(curl -s "ipinfo.io/city" 2>/dev/null)
    IP=$(curl -s "ipinfo.io/ip" 2>/dev/null)

    if [ -n "$LOCATION" ]; then
        echo -e "IP: $IP | ${CYAN}City: $LOCATION${NC}"
    else
        echo -e "${RED}Could not fetch location (Network error)${NC}"
    fi
}

# Function to draw the main screen
draw_dashboard() {
    clear
    
    echo -e "${BLUE}=======================================================${NC}"
    echo -e "${BLUE}|               ${YELLOW}UNIX SYSTEM STATUS DASHBOARD${NC}              |${NC}"
    echo -e "${BLUE}=======================================================${NC}"

    # --- Section 1: System Time & Date ---
    echo -e "\n${CYAN}--- Date & Time ---${NC}"
    echo -e "$(date "+%A, %B %d, %Y | %H:%M:%S")"
    
    # --- Section 2: Device Status ---
    echo -e "\n${CYAN}--- Device Status ---${NC}"
    echo -e "Wi-Fi: $(get_wifi_status)"
    echo -e "Bluetooth: $(get_bluetooth_status)"
    echo -e "Battery: $(get_battery_status)"

    # --- Section 3: Network & Location ---
    echo -e "\n${CYAN}--- Network Location ---${NC}"
    echo -e "Location: $(get_location)"

    # --- Section 4: Calendar ---
    echo -e "\n${CYAN}--- Calendar (Current Month) ---${NC}"
    echo -e "${MAGENTA}"
    # Use cal, and ensure it's centered or left-aligned nicely
    cal -h # -h removes the highlighting of the current day
    echo -e "${NC}"

    # --- Footer ---
    echo -e "${BLUE}=======================================================${NC}"
    echo -e "Last updated: $(date "+%H:%M:%S") | Refreshing in $REFRESH_RATE seconds. (Press Ctrl+C to exit)"
}

# --- Main Loop ---
main() {
    trap exit SIGINT # Trap Ctrl+C (SIGINT) to allow clean exit

    while true; do
        draw_dashboard
        sleep $REFRESH_RATE
    done
}

# Execute the main function
main

