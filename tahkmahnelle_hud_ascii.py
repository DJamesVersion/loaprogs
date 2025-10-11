import time
import random
import sys

# --- Setup and Global Constants ---
HUD_WIDTH = 80  # Define a consistent width for the HUD
REFRESH_RATE = 1.0  # Seconds between screen updates

LORE_UPDATES = [
    "LOG: Deep Regolith Scan complete. Temple of Mars location confirmed, 98% probability.",
    "ALERT: Subterranean pressure spike detected near Lebus Lineage root section (Section C).",
    "STATUS: Elara Wilson's original Navigational Path integrity report validated (100%).",
    "REPORT: Crystal Moss harvest efficiency boosted by 15% following Sora Lebus algorithm update.",
    "NOTICE: External system broadcast detected from Jupiter Quadrant. Analysis pending...",
    "DATA: Tahkmahnelle-Tree Biometric Health Index: Optimum (99.98%).",
]

# Simple ANSI color codes (may not work on all terminals, but adds flair)
# Using standard codes: \033[36m = Cyan, \033[33m = Yellow, \033[32m = Green, \033[0m = Reset
COLOR_CYAN = "\033[36m"
COLOR_YELLOW = "\033[33m"
COLOR_GREEN = "\033[32m"
COLOR_RED = "\033[31m"
COLOR_RESET = "\033[0m"

# --- Fictional Data Generation Functions ---

def get_random_finance_data():
    """Generates simulated financial data for stocks and credits."""
    return {
        "TechStocks_Wilson": round(random.uniform(95.0, 105.0), 2),
        "BioCredits_Lebus": round(random.uniform(1.2, 2.5), 2),
        "Science_R&D_Credit": random.randint(500, 950),
        "Total_Commonwealth_Treasury": random.randint(1_000_000, 5_000_000),
    }

def get_random_weather_data():
    """Generates simulated weather and environmental data for Tahkmahnelle45."""
    weather_states = ["Clear, Low Dust", "Regolith Storm Advisory", "Icy Micro-Meteor Shower", "Stable Atmosphere", "Thermal Anomaly Detected"]
    temp = random.randint(-180, -100)
    humidity = random.randint(5, 15)
    wind = random.randint(0, 50)
    
    return {
        "Atmosphere": random.choice(weather_states),
        "Temperature": f"{temp}°C (Stable)",
        "Ionosphere Wind Speed": f"{wind} km/h",
        "Humidity": f"{humidity}%",
    }

def get_random_tech_data():
    """Generates simulated technological attributes and advances."""
    return {
        "Tractor Beam Efficiency": random.randint(85, 100),
        "Arboreal Network Latency": round(random.uniform(0.01, 0.09), 3),
        "AI Co-Processor Load": random.randint(10, 70),
        "Life Extension Rate": round(random.uniform(0.8, 1.1), 2),
    }

# --- Formatting Helpers ---

def clear_screen():
    """Clears the terminal screen."""
    # Works for Windows ('cls') and Unix-like systems ('clear')
    if sys.platform.startswith('win'):
        import os
        os.system('cls')
    else:
        sys.stdout.write('\033[H\033[J')
        sys.stdout.flush()

def draw_separator(char='=', width=HUD_WIDTH, color=COLOR_CYAN):
    """Prints a full-width separator line."""
    print(f"{color}{char * width}{COLOR_RESET}")

def print_section_header(title, width=HUD_WIDTH, color=COLOR_YELLOW):
    """Prints a styled section header."""
    padding = (width - len(title) - 4) // 2
    print(f"{color}|{' ' * padding}{title}{' ' * (width - len(title) - 2 - padding)}|{COLOR_RESET}")
    draw_separator('-', width, color)

def format_bar(value, max_val, length=30, fill_char='#'):
    """Creates a simple ASCII progress bar."""
    ratio = value / max_val
    filled = int(ratio * length)
    empty = length - filled
    return f"[{fill_char * filled}{'-' * empty}] {value:.2f}/{max_val:.2f}"

# --- HUD Components ---

def print_header(current_time):
    """Prints the HUD header, time, and status."""
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    
    title = f"{COLOR_CYAN}ROYAL TAHKMAHNELLE COMMONWEALTH TERMINAL{COLOR_RESET}"
    time_status = f"{COLOR_YELLOW}System Time: {current_time_str}{COLOR_RESET} // {COLOR_GREEN}Tahkmahnelle45 Status: OPERATIONAL{COLOR_RESET}"
    
    draw_separator('=', HUD_WIDTH, COLOR_CYAN)
    
    # Center the title
    title_pad = (HUD_WIDTH - len(title) + len(COLOR_CYAN) + len(COLOR_RESET)) // 2
    print(f"{' ' * title_pad}{title}{' ' * title_pad}")
    
    # Left align time/status
    print(time_status.center(HUD_WIDTH + len(COLOR_YELLOW) + len(COLOR_GREEN) + len(COLOR_RESET)))
    
    draw_separator('=', HUD_WIDTH, COLOR_CYAN)

def print_finance_section(finance_data):
    """Displays monetary values, stocks, and credit in sciences."""
    draw_separator()
    print_section_header("FINANCIAL & CREDIT FLOW (Dynasty Valuations)")

    # 1. Stocks vs Credit Bars (Max values assumed for scaling)
    MAX_STOCK = 105.0
    MAX_CREDIT = 2.5
    MAX_SCIENCE = 1000

    stock_bar = format_bar(finance_data["TechStocks_Wilson"], MAX_STOCK, fill_char='#')
    credit_bar = format_bar(finance_data["BioCredits_Lebus"], MAX_CREDIT, fill_char='$')

    print(f"{COLOR_CYAN}| TechStocks (Wilson): {finance_data['TechStocks_Wilson']:<8.2f} {stock_bar.ljust(HUD_WIDTH - 25)} {COLOR_RESET}")
    print(f"{COLOR_MAGENTA}| BioCredits (Lebus):  {finance_data['BioCredits_Lebus']:<8.2f} {credit_bar.ljust(HUD_WIDTH - 25)} {COLOR_RESET}")
    print(f"|")

    # 2. Science Funding Gauge
    science_bar = format_bar(finance_data["Science_R&D_Credit"], MAX_SCIENCE, length=60, fill_char='*')
    print(f"{COLOR_GREEN}| Science R&D Funding (Cr): {science_bar.ljust(HUD_WIDTH - 25)} {COLOR_RESET}")
    print(f"|")

    # 3. Treasury
    treasury_str = f"| Total Commonwealth Treasury: {finance_data['Total_Commonwealth_Treasury']:,} Units"
    print(f"{COLOR_YELLOW}{treasury_str.ljust(HUD_WIDTH)}{COLOR_RESET}")
    draw_separator()

def print_weather_and_tech_section(weather_data, tech_data):
    """Displays environmental and technological attributes."""
    
    # Split the width for side-by-side presentation
    half_width = (HUD_WIDTH // 2) - 1
    
    # Headers
    print_section_header("ENVIRONMENTAL & TECHNOLOGICAL ADVANCES")

    # Combined Table Setup
    weather_lines = []
    for key, value in weather_data.items():
        weather_lines.append(f"{COLOR_YELLOW}{key:<25}: {COLOR_RESET}{value}")
        
    tech_lines = []
    for key, value in tech_data.items():
        rating_color = COLOR_GREEN if (isinstance(value, int) and value > 90) or (isinstance(value, float) and value > 1.0) else COLOR_RESET
        
        if "Efficiency" in key or "Load" in key:
            value_str = f"{value}%"
        elif "Latency" in key:
            value_str = f"{value}ms"
        else:
            value_str = str(value)

        tech_lines.append(f"{COLOR_CYAN}{key:<25}: {rating_color}{value_str}{COLOR_RESET}")

    max_lines = max(len(weather_lines), len(tech_lines))
    
    for i in range(max_lines):
        weather_part = weather_lines[i] if i < len(weather_lines) else f"{' ' * (half_width)}"
        tech_part = tech_lines[i] if i < len(tech_lines) else f"{' ' * (half_width - 1)}"

        # Combine and print
        print(f"| {weather_part:<{half_width}} | {tech_part:<{half_width - 1}} |")

    draw_separator()

def print_lore_feed():
    """Prints the Tahkmahnelle-Tree status and a rolling lore update."""
    draw_separator()
    print_section_header("THE GREAT TREE'S CONDUIT (Mission Data Feed)")

    # Simulate a rolling lore update
    update = random.choice(LORE_UPDATES)
    update_color = COLOR_RED if "ALERT" in update else COLOR_RESET
    
    # Tree Status Table
    print(f"| {COLOR_GREEN}Root Integrity:{COLOR_RESET} 100.0% | {COLOR_YELLOW}Data Flow:{COLOR_RESET} Nominal")
    print(f"| {COLOR_RED}Mission Target:{COLOR_RESET} Temple of Mars (Regolith Traversal)")
    draw_separator('-')
    
    # Lore Update
    update_line = f"| {update_color}>> {update}{COLOR_RESET}"
    print(update_line.ljust(HUD_WIDTH + len(COLOR_RED) + len(COLOR_RESET) + 1))
    
    draw_separator()

# --- Main Application Loop ---

def run_hud():
    """Initializes the HUD and runs the update loop."""
    
    print("Initializing Tahkmahnelle Data Streams...")
    time.sleep(2) 

    while True:
        try:
            clear_screen()
            
            current_time = time.localtime()
            finance_data = get_random_finance_data()
            weather_data = get_random_weather_data()
            tech_data = get_random_tech_data()
            
            print_header(current_time)
            print_finance_section(finance_data)
            print_weather_and_tech_section(weather_data, tech_data)
            print_lore_feed()

            time.sleep(REFRESH_RATE)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"System Error: {e}")
            time.sleep(5)
            
    print("\nTahkmahnelle HUD Offline. System Terminated.")


if __name__ == "__main__":
    run_hud()

