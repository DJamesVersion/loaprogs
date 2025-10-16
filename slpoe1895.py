# SLPOE 9EHD OS 18.9.5 - Unix-like Terminal Environment
# Update: Enhanced Data Integrity, Orbital Inclination Added, Advanced Analysis Features
# Core System Updated: T-SPIRAL Locus (Spiral Cycle 8.472)
# Use 'help' to see the available commands.

import sys
import os
import textwrap
import random
import math

# --- Configuration and Core Constants (Version 18.9.5) ---

SHELL_NAME = "SLPOE 9EHD"
VERSION = "18.9.5" # Version Bumped
PROMPT = "SLPOE-18.9.5:/" # Updated Prompt
CURRENT_SIM_TIME = 8472.0 # Arbitrary Spiral Cycle Time since Epoch

# T-System Color codes: 31=Red (Flare/M-Dwarf), 33=Yellow, 36=Cyan, 35=Magenta, 34=Blue, 37=Gray, 97=Bright White (stars)
# Tetnobautte Color codes: 93=Bright Yellow (Habitable), 90=Dark Gray (Uninhabitable)
T_MONTH_DAYS = 45 # Core Constant: 1 T-Month = 45 Earth Days.

# --- DATA STRUCTURES ---

# -------------------------------------------------------------
# 1. PHONOLOGY DATA (R-Sector Linguistic Data) - Retained
# -------------------------------------------------------------
PHONOLOGY_DATA = {
    "source": "Tahkmahnelle Linguistic Archives, R-Sector Dialect",
    "notes": "Phonemic inventory is highly constrained, favoring dental and velar articulation. The language is agglutinative.",
    "consonants": {
        "Plosives": ["/t/", "/d/", "/k/", "/g/", "/p/", "/b/"],
        "Fricatives": ["/s/", "/z/", "/h/", "/f/"],
        "Nasals": ["/m/", "/n/", "/ŋ/ (ng)"],
        "Approximants": ["/l/", "/r/", "/j/ (y)", "/w/"],
        "Ejective (Glottal)": ["/tʼ/ (t-prime)"] 
    },
    "vowels": {
        "Front": ["/i/ (high)", "/e/ (mid)"],
        "Central": ["/a/ (low)"],
        "Back": ["/u/ (high)", "/o/ (mid)"]
    },
    "phonotactics": {
        "Syllable Structure": "Highly restricted: (C)(S)V(C), where S is an approximant.",
        "Allowed Clusters": ["tr-", "kl-", "dw-", "st-"],
        "Forbidden Endings": "No complex clusters. Only Nasals (/n/, /m/) or Plosives (/t/, /k/) allowed in coda.",
        "Stress Rule": "Primary stress is always on the first syllable of the root."
    },
    "example_morphemes": {
        "Tahkmah": "Star/Home",
        "Nell": "Companion/Shadow",
        "Jal'in": "Water/Flow",
        "Tetn": "Time/Cycle"
    }
}


# -------------------------------------------------------------
# 2. TETNOBAUTTE CHRONOMETRIC SYSTEM (BCI Source) - Retained
# -------------------------------------------------------------
TETNOBAUTTE_DATA = {
    "description": "Chronometric Locus, derived from BCI data. Uses T-Months and Scaled Radii.",
    "source": "Bureau of Chronometric Integrity (BCI) / Tetnobautte Grand Archives",
    "planets": {
        "lenemketobontette": {"status": "UNINHABITABLE", "radii": 55, "rev_factor": 2.00, "color_code": "90"},
        "stihuu": {"status": "HABITABLE", "radii": 80, "rev_factor": 1.33, "color_code": "93"},
        "tetnobautte": {"status": "HABITABLE", "radii": 105, "rev_factor": 1.00, "color_code": "93", "anchor": True},
        "vraelvrae": {"status": "HABITABLE", "radii": 130, "rev_factor": 0.80, "color_code": "93"},
        "lenemketobontettestihuu": {"status": "UNINHABITABLE", "radii": 155, "rev_factor": 0.67, "color_code": "90"},
        "stihuutetnobautte": {"status": "UNINHABITABLE", "radii": 180, "rev_factor": 0.57, "color_code": "90"},
        "tetnobauttestihuu": {"status": "UNINHABITABLE", "radii": 205, "rev_factor": 0.50, "color_code": "90"},
        "TAHKMAHNELLE45": {"status": "HABITABLE", "radii": 230, "rev_factor": 0.44, "color_code": "93", "type": "DWARF"},
    },
    "star": {"name": "T-Chronos (K0V)", "info": "Single orange dwarf. Stable emissions.", "color_code": "97"},
    "chart": [
        "  [SCALED RADIUS]                    |",
        "  55: \033[90mO\033[0m (lenemketobontette) . . . . . . . . . . . . . . . . . . . . . . . . . . .",
        "  80: . . \033[93mO\033[0m (stihuu) . . . . . . . . . . . . . . . . . . . . . . . . . . .",
        " 105: . . . . \033[93mO\033[0m (tetnobautte) . . . . . . . . . . . . . . . . . . . . . . .",
        " 130: . . . . . . \033[93mO\033[0m (vraelvrae) . . . . . . . . . . . . . . . . . . . . . . .",
        " 155: . . . . . . . . \033[90mO\033[0m (lenemketobontettestihuu) . . . . . . . . . . . . . . . . . .",
        " 180: . . . . . . . . . . . \033[90mO\033[0m (stihuutetnobautte) . . . . . . . . . . . . . . . . . . .",
        " 205: . . . . . . . . . . . . . \033[90mO\033[0m (tetnobauttestihuu) . . . . . . . . . . . . . . . . .",
        " 230: . . . . . . . . . . . . . . . \033[93mO\033[0m (TAHKMAHNELLE45) . . . . . . . . . . . . . .",
        " --- Tetnobautte Locus (Chrono-Anchor at 105) ---"
    ]
}

# -------------------------------------------------------------
# 3. STANDARD TAHKMAHNELLE SYSTEMS (AU/Year Metrics) - T-SPIRAL Data Updated
# -------------------------------------------------------------
SYSTEM_DATA = {
    "T-PRIME": {
        "description": "Prime System, pre-binary capture. Single star Locus.",
        "planets": {
            "K'tharr-P": {"type": "Rocky", "temp": "High", "distance_au": 0.9, "period_yr": 0.6, "current_deg": 180, "inclination_deg": 3.1, "color_code": "31"},
            "Old Jal'in": {"type": "Oceanic", "temp": "Temperate", "distance_au": 2.1, "period_yr": 1.7, "current_deg": 45, "inclination_deg": 0.2, "color_code": "33"},
        },
        "star": {"name": "Tahkmah-Prime (G2V)", "info": "Single Star System.", "color_code": "97"},
        "chart": ["  (T-PRIME Chart Placeholder)"]
    },
    "T-45": {
        "description": "Mid-Phase System (45 Standard Years post-capture). Unstable Locus.",
        "planets": {
            "T-45 Vorex": {"type": "Desert", "temp": "Erratic", "distance_au": 5.5, "period_yr": 5.1, "current_deg": 270, "inclination_deg": 9.5, "color_code": "36"},
            "T-45 Xylos": {"type": "Ringed Gas", "temp": "Icy", "distance_au": 17.0, "period_yr": 48.0, "current_deg": 90, "inclination_deg": 1.9, "color_code": "34"},
        },
        "star": {"name": "Tahkmah/Nell Locus", "info": "Highly elliptical orbits.", "color_code": "97"},
        "chart": ["  (T-45 Chart Placeholder)"]
    },
    # --- T-SPIRAL DATA (Enhanced) ---
    "T-SPIRAL": { 
        "description": "Spiral Cycle 8.472 · Binary Core: Vrael & Stihuu. Focus on Chronarchic and Mnemonic Loci.",
        "planets": {
            "NAHARAIM MINOR": {"type": "Guild Bastion", "temp": "Temperate", "distance_au": 0.9, "period_yr": 0.93, "current_deg": 20, "inclination_deg": 1.1, "color_code": "33", "moons": ["Velk", "Thuun"]},
            "VRAELEN PRIME": {"type": "Capital World", "temp": "Warm", "distance_au": 1.4, "period_yr": 1.66, "current_deg": 100, "inclination_deg": 0.5, "color_code": "36", "moons": ["Cenra", "Mirell"]},
            "DUSKBONE": {"type": "Ceremonial World", "temp": "Cool", "distance_au": 2.2, "period_yr": 2.9, "current_deg": 180, "inclination_deg": 2.2, "color_code": "35", "moons": ["Stellune", "Orryx"]},
            "STIHUUN’S WAKE": {"type": "Flare Cluster", "temp": "Erratic", "distance_au": 3.1, "period_yr": 4.2, "current_deg": 270, "inclination_deg": 3.4, "color_code": "31", "moons": ["Sirr", "Vexil", "Thrae", "Omn", "Jull", "Korr", "Nenn"]},
            "ECHOREACH": {"type": "Archive World", "temp": "Icy", "distance_au": 4.5, "period_yr": 6.1, "current_deg": 330, "inclination_deg": 0.8, "color_code": "34", "moons": ["Ysil", "Brann"]},
            "KINLESS EXPANSE": {"type": "Contested Zone", "temp": "Cold", "distance_au": 6.3, "period_yr": 9.2, "current_deg": 50, "inclination_deg": 5.7, "color_code": "37", "moons": ["Xenith (rogue)"]},
            "SPIRALUM": {"type": "Temporal Observatory", "temp": "Frozen", "distance_au": 8.1, "period_yr": 12.5, "current_deg": 150, "inclination_deg": 1.3, "color_code": "37", "moons": ["Talvra", "Ephra"]},
            "MAJESTAS": {"type": "Gas Giant", "temp": "Cryogenic", "distance_au": 10.5, "period_yr": 19.5, "current_deg": 210, "inclination_deg": 4.8, "color_code": "34", "moons": ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]}, # New massive planet
        },
        "star": {"name": "Vrael (M5.5V) / Stihuu (M6V)", "info": "Binary Separation: 2.1–8.8 AU. Orbital Resonance: 26.5 years (Spiral Cycle).", "color_code": "31"},
        "events": {
            "Spiral Eclipse": {"type": "Ceremonial", "info": "Year 14.71 of Cycle", "color_code": "36"},
            "Accord Pulse": {"type": "Ceremonial", "info": "Every 8.83 years", "color_code": "36"},
            "Hollow Moon Eclipse": {"type": "Ceremonial", "info": "Year 26.5", "color_code": "36"}
        },
        "chart": ["  (T-SPIRAL Chart Placeholder)"]
    }
}
SYSTEM_DATA['TETNOBAUTTE'] = TETNOBAUTTE_DATA

MAJOR_OBJECTS = {} 
MINOR_OBJECTS = {}

CONSTELLATION_CHART = [
    "--- Galactic Overlay: Sector 7 ---",
    "                                   * (Algenib)",
    "        * (Zuben)                    | ",
    "    --*-- (Sadalt)                 * |",
    " * * /                             /  |",
    "  \\    / (The Hunter)             /   | (The Serpent)",
    "   \\  * *---*",
    "    *---* |  *",
    "     \\  | *",
    "      * *",
    "        |",
    "        *",
    "--- The Serpent Constellation is a navigational key for T-SPIRAL Locus ---"
]


# --- Core Simulation Class ---

class SLPOESimulator:
    """Simulates a Unix-like terminal environment for the Tahkmahnelle Multi-System (v18.9.5)."""

    def __init__(self):
        self.commands = {
            "help": self.cmd_help,
            "ls": self.cmd_list_objects,
            "slpoe": self.cmd_slpoe,
            "scan": self.cmd_scan,
            "trace": self.cmd_trace,
            "chrono": self.cmd_chrono_analysis,
            "phonology": self.cmd_phonology, 
            "chart": self.cmd_constellation_chart,
            "graph": self.cmd_orbital_graph,
            "history": self.cmd_history,
            "clear": self.cmd_clear,
            "exit": self.cmd_quit,
            "quit": self.cmd_quit,
        }
        self.running = True
        self.history = []
        
        # Calculate max distance across ALL planets for common scaling
        all_distances = [d['distance_au'] for sys_name, sys in SYSTEM_DATA.items() if sys_name != 'TETNOBAUTTE' for d in sys['planets'].values()]
        self.max_dist = max(all_distances) if all_distances else 1.0


    def run(self):
        """Main loop for the terminal simulation."""
        self.welcome_screen()
        while self.running:
            try:
                # Updated prompt display to match the new OS branding
                user_input = input(f"\n\033[92m{PROMPT}\033[0m$ ").strip() 
                if user_input:
                    self.process_command(user_input)
            except EOFError:
                print("\n")
                self.cmd_quit()
            except KeyboardInterrupt:
                print("\n^C detected. Use 'quit' or 'exit' to terminate safely.")

    def welcome_screen(self):
        """Displays the startup message and system banner."""
        self.cmd_clear([])
        print("\n" + "=" * 80)
        print(f"| {SHELL_NAME} OS {VERSION} - TAHKMAHNELLE MULTI-SYSTEM ANALYZER |".center(78))
        print("| Core System: \033[96mT-SPIRAL Locus (Spiral Cycle 8.472)\033[0m is now active. |".center(80))
        print(f"| Core Constant: 1 T-Month = {T_MONTH_DAYS} Earth Days                     |".center(80))
        print("=" * 80)
        print("Type 'help' for commands or 'ls' for the system manifest.")

    def process_command(self, user_input):
        """Parses user input and executes the appropriate command."""
        parts = user_input.split()
        command = parts[0].lower()
        args = parts[1:]

        if command in self.commands:
            try:
                self.commands[command](args)
                self.history.append(user_input)
            except Exception as e:
                print(f"\033[91mERROR\033[0m: Command '{command}' failed: {e}")
        else:
            print(f"\033[91mERROR\033[0m: Command not found: {command}. Type 'help' for assistance.")

    # --- Utility Methods ---
    def _calculate_tetnobautte_periods(self, rev_factor):
        """Calculates T-Month and Earth Day periods based on REV_FACTOR."""
        if rev_factor == 0:
            return None, None
        
        period_t_months = 1.0 / rev_factor
        period_earth_days = period_t_months * T_MONTH_DAYS
        return period_t_months, period_earth_days

    def _get_planet_by_name(self, target_name):
        """Searches all systems for a planet by name."""
        for sys_name, sys_data in SYSTEM_DATA.items():
            for name, data in sys_data['planets'].items():
                if name.lower() == target_name.lower():
                    return name, data, sys_name
        return None, None, None

    # --- Command Implementations ---

    def cmd_history(self, args):
        """Displays the command history of the current session."""
        print(f"\n--- SESSION COMMAND HISTORY ({len(self.history)} entries) ---\n")
        if not self.history:
            print("  No successful commands recorded yet.")
            return

        for i, cmd in enumerate(self.history):
            print(f"  {i+1:>3}. \033[94m{cmd}\033[0m")
        print("-" * 35 + "\n")

    def cmd_help(self, args):
        """Displays command usage information."""
        print(f"\nAVAILABLE COMMANDS ({SHELL_NAME} Terminal v{VERSION}):\n")
        commands_info = {
            "help": "Display this help screen.",
            "ls": "List all systems (T-PRIME, T-45, T-SPIRAL, TETNOBAUTTE) and T-SPIRAL events.",
            "slpoe [system]": "Run Orbital Emitter for a specific system (e.g., 'slpoe T-SPIRAL'). T-SPIRAL shows current orbital positions.",
            "scan [object]": "Retrieve detailed data on any system object, including **Orbital Inclination**.",
            "trace [planet]": "Simulate and predict orbital dynamics for a T-SPIRAL planet and perform **Harmonic Resonance Check**.",
            "chrono [planet]": "Analyze orbital periods and calculate **Scaled Orbital Velocity** for Tetnobautte bodies.",
            "phonology": "Display the Tahkmahnelle phonemic inventory and phonotactic rules (R-Sector).",
            "chart [sys/const]": "View System Locus or Galactic Constellation Chart.",
            "graph [metric]": "Comparative graph of T-systems metrics. Metrics: **distance**, **period**, **radii**, **inclination**.",
            "history": "Show successful command history.",
            "clear": "Clear the terminal screen.",
            "exit/quit": "Terminate the SLPOE session."
        }
        for cmd, desc in commands_info.items():
            print(f"  \033[94m{cmd:<15}\033[0m {desc}") 
        print()
        
    def cmd_phonology(self, args):
        """Displays the phonological rules and inventory of the Tahkmahnelle language."""
        print("\n--- TAHKMAHNELLE PHONOLOGY REPORT (R-SECTOR LINGUISTIC ARCHIVES) ---")
        print(f"  \033[96mSOURCE:\033[0m {PHONOLOGY_DATA['source']}")
        print(f"  \033[96mNOTES:\033[0m {PHONOLOGY_DATA['notes']}")
        
        # Consonants
        print("\n\033[93m[CONSONANT INVENTORY (IPA)]\033[0m")
        for category, sounds in PHONOLOGY_DATA['consonants'].items():
            print(f"  {category:<18}: {', '.join(sounds)}")
            
        # Vowels
        print("\n\033[93m[VOWEL INVENTORY (IPA)]\033[0m")
        for category, sounds in PHONOLOGY_DATA['vowels'].items():
            print(f"  {category:<18}: {', '.join(sounds)}")
            
        # Phonotactics
        print("\n\033[93m[PHONOTACTIC RULES]\033[0m")
        for rule, detail in PHONOLOGY_DATA['phonotactics'].items():
            print(f"  - \033[94m{rule}\033[0m: {detail}")
            
        # Examples
        print("\n\033[93m[EXAMPLE MORPHEMES]\033[0m")
        for morpheme, meaning in PHONOLOGY_DATA['example_morphemes'].items():
            print(f"  - {morpheme:<12}: {meaning}")

        print("-" * 60 + "\n")


    def cmd_list_objects(self, args):
        """Lists the defined systems and major assets/events."""
        print("\nTAHKMAHNELLE MULTI-SYSTEM MANIFEST:\n")
        
        # List Systems
        print("\033[93m[SYSTEM LENSES]\033[0m") 
        system_list = {
            "T-SPIRAL": "Current Binary System: Vrael/Stihuu (AU/Year)",
            "T-PRIME": "Historical Single Star (AU/Year)",
            "T-45": "Historical Unstable Phase (AU/Year)",
            "TETNOBAUTTE": "Chronometric Locus (Scaled/T-Month)"
        }
        for sys_name, desc in system_list.items():
            print(f"  - \033[96m{sys_name:<12}\033[0m: {desc}")
        
        # List T-SPIRAL Ceremonial Events
        spiral_events = SYSTEM_DATA.get("T-SPIRAL", {}).get("events", {})
        if spiral_events:
            print("\n\033[93m[T-SPIRAL CEREMONIAL EVENTS]\033[0m")
            print(f"  {'EVENT NAME':<20} {'TYPE':<12} {'CYCLE NOTE':<20}")
            print("  " + "-" * 52)
            for name, data in spiral_events.items():
                color = f"\033[{data['color_code']}m"
                print(f"  {color}{name:<20}\033[0m {data['type']:<12} {data['info']:<20}")
        
        print()

    def cmd_slpoe(self, args):
        """Runs the SLPOE for a specified system."""
        sys_name = (args[0] if args else "T-SPIRAL").upper() # Default to T-SPIRAL

        if sys_name not in SYSTEM_DATA:
            print(f"\033[91mERROR\033[0m: System '{sys_name}' not recognized. Use T-PRIME, T-45, T-SPIRAL, or TETNOBAUTTE.")
            return

        data = SYSTEM_DATA[sys_name]
        print(f"\n--- {SHELL_NAME} SYSTEM EMMISION DIAGRAM V.{VERSION}: {sys_name} ---")
        print(f"STAR(S): \033[91m{data['star']['name']}\033[0m")
        print(f"STATUS: {data['star']['info']}\n")

        if sys_name == 'T-SPIRAL':
            # NEW: Dynamic Orbital Position Chart for T-SPIRAL
            print("--- ORBITAL POSITION CHART (VIEWED FROM ABOVE ECCLIPTIC) ---")
            print("   (0°/360°) ---------------------------------------- (180°)")
            
            # Simple radial mapping based on current_deg
            chart_size = 70
            center = chart_size // 2
            
            grid = [[' ' for _ in range(chart_size)] for _ in range(chart_size)]

            # Place Star at center (simulated)
            grid[center][center] = '\033[91m*\033[0m'

            for name, p_data in data['planets'].items():
                deg = p_data['current_deg']
                dist = p_data['distance_au']
                color_code = f"\033[{p_data['color_code']}m"
                
                # Scale distance to grid (Arbitrary scaling factor)
                scaled_dist = int((dist / self.max_dist) * (center - 5)) 
                
                # Convert polar coordinates (deg, scaled_dist) to cartesian (x, y)
                rad = math.radians(deg)
                # Y is inverted in terminal row numbering
                x = int(center + scaled_dist * math.cos(rad))
                y = int(center + scaled_dist * math.sin(rad))
                
                # Boundary check
                if 0 <= y < chart_size and 0 <= x < chart_size:
                    # Place the planet (using first letter of name for density)
                    grid[y][x] = f"{color_code}{name[0].upper()}\033[0m"

            # Print the grid
            # Reduce print size for readability on smaller screens
            print_start = center - 15
            print_end = center + 15
            for row in grid[print_start:print_end]:
                print("  " + "".join(row[print_start:print_end]))
            
            print("   (90°) ------------------------------------------- (270°)")
            print("   \033[33mN\033[0m=Naharaim, \033[36mV\033[0m=Vraelen, \033[35mD\033[0m=Duskbone, \033[31mS\033[0m=Stihuun, \033[34mE\033[0m=Echoreach, \033[37mK\033[0m=Kinless, \033[37mR\033[0m=Spiralum, \033[34mM\033[0m=Majestas")

        elif sys_name == 'TETNOBAUTTE':
             for line in data['chart']:
                 print(line)
        else:
             # Simple placeholder for T-PRIME and T-45
            for line in data['chart']:
                print(f"\033[37m{line}\033[0m")


        print(f"\nSLPOE STATUS: Locus lock confirmed for {sys_name}.\n")
        
    def cmd_scan(self, args):
        """Retrieves detailed information on a specific object from any system."""
        if not args:
            print("\033[91mERROR\033[0m: Please specify an object or event to scan (e.g., 'scan Naharaim Minor' or 'scan Spiral Eclipse').")
            return

        target_name = " ".join(args)
        found_data = None
        system_origin = "N/A"
        key_name = target_name
        
        # 1. Search T-SPIRAL Events
        spiral_events = SYSTEM_DATA.get("T-SPIRAL", {}).get("events", {})
        for name, data in spiral_events.items():
            if name.lower() == target_name.lower():
                found_data = data
                system_origin = "T-SPIRAL EVENTS"
                key_name = name
                break
        
        # 2. Search all planetary data
        if not found_data:
            key_name, found_data, system_origin = self._get_planet_by_name(target_name)
        
        if not found_data:
            print(f"\033[91mERROR\033[0m: Object or Event '{target_name}' not found in any system manifest.")
            return

        data = found_data
        
        print(f"\n--- SCAN REPORT: {key_name.upper()} ({system_origin} LENS) ---")
        
        if system_origin == "T-SPIRAL EVENTS":
            # Event Data Display
            print(f"  \033[96mTYPE:\033[0m {data.get('type')}")
            print(f"  \033[96mCYCLE NOTE:\033[0m {data.get('info')}")
        
        elif system_origin == "TETNOBAUTTE":
            # Tetnobautte Data Display (Leveraging chrono data)
            rev_factor = data['rev_factor']
            period_t_months, period_earth_days = self._calculate_tetnobautte_periods(rev_factor)
            scaled_velocity = self._calculate_scaled_velocity(rev_factor, data['radii'])

            print(f"  \033[96mSTATUS:\033[0m {data['status']}")
            print(f"  \033[96mRADII (Scaled):\033[0m {data['radii']}")
            print(f"  \033[96mREV_FACTOR:\033[0m {rev_factor:.2f}")
            print(f"  \033[96mPERIOD (T-Months):\033[0m {period_t_months:.2f} T-Months")
            print(f"  \033[96mSCALED VELOCITY:\033[0m \033[92m{scaled_velocity:.3f}\033[0m units/cycle (New in v{VERSION})")
        
        else:
            # Standard T-System (including T-SPIRAL) Data Display
            print(f"  \033[96mPLANETARY ROLE:\033[0m {data.get('type', 'Planet')}")
            print(f"  \033[96mAVERAGE TEMP:\033[0m {data['temp']}")
            print(f"  \033[96mORBITAL DISTANCE:\033[0m {data.get('distance_au', 'N/A'):.2f} AU")
            print(f"  \033[96mORBITAL PERIOD:\033[0m {data.get('period_yr', 'N/A'):.2f} Standard Years")
            print(f"  \033[96mORBITAL INCLINATION:\033[0m \033[92m{data.get('inclination_deg', 'N/A'):.1f}°\033[0m (New in v{VERSION})")
            
            if 'moons' in data:
                 moon_list = ", ".join(data['moons'])
                 print(f"  \033[96mPRIMARY MOONS:\033[0m {moon_list}")
            
        print("-" * 35 + "\n")

    def _calculate_scaled_velocity(self, rev_factor, radii):
        """Calculates a simulated scaled orbital velocity for Tetnobautte."""
        # Derived formula for simulated comparison: V = C * REV / sqrt(R)
        if radii <= 0 or rev_factor <= 0: return 0.0
        return (rev_factor * 100) / math.sqrt(radii)

    def cmd_chrono_analysis(self, args):
        """
        Analyzes Tetnobautte Chronometric System data, including Scaled Orbital Velocity.
        Usage: chrono [planet]
        """
        if not args:
            print("\033[91mERROR\033[0m: Please specify a Tetnobautte system body (e.g., 'chrono tetnobautte').")
            print("Available Tetnobautte bodies: " + ", ".join(TETNOBAUTTE_DATA['planets'].keys()))
            return

        target_name = args[0]
        tetnobautte_planets = TETNOBAUTTE_DATA['planets']
        
        planet_data = {k: v for k, v in tetnobautte_planets.items() if k.lower() == target_name.lower()}

        if not planet_data:
            print(f"\033[91mERROR\033[0m: Body '{target_name}' not found in Tetnobautte system data.")
            return

        data = list(planet_data.values())[0]
        
        # --- BCI Chronometric Calculation ---
        rev_factor = data['rev_factor']
        period_t_months, period_earth_days = self._calculate_tetnobautte_periods(rev_factor)
        scaled_velocity = self._calculate_scaled_velocity(rev_factor, data['radii'])
        
        
        print(f"\n--- CHRONOMETRIC ANALYSIS: {target_name.upper()} (BCI Source) ---")
        print(f"  \033[96mSOURCE:\033[0m {TETNOBAUTTE_DATA['source']}")
        print(f"  \033[96mCore Constant:\033[0m 1 T-Month = {T_MONTH_DAYS} Earth Days")
        
        print("\n\033[93m[ORBITAL METRICS]\033[0m")
        print(f"  - Scaled Radii (R): {data['radii']}")
        print(f"  - Revolution Factor (REV_FACTOR): \033[92m{rev_factor:.2f}\033[0m (Relative to tetnobautte=1.00)")
        print(f"  - Orbital Period (T-Months): {period_t_months:.2f} T-Months")
        print(f"  - Orbital Period (Earth Days): {period_earth_days:.2f} Earth Days")
        print(f"  - \033[96mSCALED ORBITAL VELOCITY:\033[0m \033[92m{scaled_velocity:.3f}\033[0m units/cycle (New in v{VERSION})")
        
        print("\n\033[93m[HABITABILITY ASSESSMENT]\033[0m")
        status_color = "\033[92m" if data['status'] == "HABITABLE" else "\033[91m"
        print(f"  - STATUS: {status_color}{data['status']}\033[0m")

        print("\nNote: Use 'graph radii' to compare Tetnobautte system metrics.\n")


    def cmd_trace(self, args):
        """
        Simulates orbital tracing and conjunction prediction for a T-SPIRAL planet,
        including a Harmonic Resonance Check.
        """
        if not args:
            print("\033[91mERROR\033[0m: Please specify a T-SPIRAL planet to trace (e.g., 'trace Duskbone').")
            print("Available T-SPIRAL planets: " + ", ".join(SYSTEM_DATA['T-SPIRAL']['planets'].keys()))
            return

        target_name = " ".join(args)
        spiral_planets = SYSTEM_DATA['T-SPIRAL']['planets']
        
        planet_data = {k: v for k, v in spiral_planets.items() if k.lower() == target_name.lower()}

        if not planet_data:
            print(f"\033[91mERROR\033[0m: Planet '{target_name}' not found in T-SPIRAL planetary data. Use 'chrono' for Tetnobautte bodies.")
            return

        data = list(planet_data.values())[0]
        planet_key = list(planet_data.keys())[0]
        
        # --- Astrometry Calculation Simulation ---
        period_yr = data['period_yr']
        period_days = period_yr * 365.25 
        angular_speed = 360 / period_days 
        days_passed_since_epoch = CURRENT_SIM_TIME 
        current_deg = (angular_speed * days_passed_since_epoch) % 360 # Simulated position
        
        # Conjunction prediction uses random based on the long Spiral Cycle
        time_to_conjunction = random.uniform(5000, 26500) # Fictional time in days

        print(f"\n--- ASTROMETRIC TRACE REPORT: {planet_key.upper()} (T-SPIRAL LENS) ---")
        print(f"  \033[96mANALYSIS LENS:\033[0m T-SPIRAL v{VERSION} (Spiral Cycle 8.472)")
        print(f"  \033[96mPROJECTED POSITION:\033[0m {current_deg:.1f} degrees (Ecliptic Locus)")
        print(f"  \033[96mORBITAL INCLINATION:\033[0m {data['inclination_deg']:.1f}°")
        
        # NEW: Harmonic Resonance Check
        print("\n\033[93m[HARMONIC RESONANCE CHECK]\033[0m (New in v{VERSION})")
        
        # Use VRAELEN PRIME as the index point (1.66 yr)
        vrael_prime_period = SYSTEM_DATA['T-SPIRAL']['planets']['VRAELEN PRIME']['period_yr']
        resonance_ratio = vrael_prime_period / period_yr
        
        # Check for simple 1:X or X:1 resonance
        if abs(resonance_ratio - round(resonance_ratio)) < 0.01:
            status = f"\033[92mSTABLE ({1}:{(round(1/resonance_ratio))})\033[0m"
            note = "Strong commensurability with VRAELEN PRIME. Stable orbital mechanics."
        elif abs((1/resonance_ratio) - round(1/resonance_ratio)) < 0.01:
            status = f"\033[92mSTABLE ({round(resonance_ratio)}:{1})\033[0m"
            note = "Strong commensurability with VRAELEN PRIME. Stable orbital mechanics."
        else:
            status = "\033[93mNOMINAL\033[0m"
            note = "Nominal ratio. Potential for minor orbital drift over multiple cycles."

        print(f"  - Ratio to VRAELEN PRIME (1.66yr): 1 : {1/resonance_ratio:.2f}")
        print(f"  - Resonance Status: {status}")
        print(f"  - Assessment: {note}")
        
        print("\n\033[93m[CONJUNCTION PREDICTION]\033[0m")
        print(f"  Next Ceremonial Conjunction (Approximate): ~{time_to_conjunction:.0f} Standard Days")
        
        print("-" * 35 + "\n")


    def cmd_constellation_chart(self, args):
        """
        Displays a specific chart (system locus or galactic constellation).
        Usage: chart [T-PRIME|T-45|T-SPIRAL|TETNOBAUTTE|CONSTELLATION]
        """
        chart_target = (args[0] if args else "CONSTELLATION").upper()

        if chart_target == "CONSTELLATION":
            print("\n--- GALACTIC CONSTELLATION CHART: SECTOR 7 (Reference) ---\n")
            print("\033[96m")
            for line in CONSTELLATION_CHART:
                print(line)
            print("\033[0m\n")
        elif chart_target in SYSTEM_DATA:
            self.cmd_slpoe([chart_target])
        else:
            print(f"\033[91mERROR\033[0m: Chart target '{chart_target}' not recognized.")
            print("Available charts: T-PRIME, T-45, T-SPIRAL, TETNOBAUTTE, CONSTELLATION.")

    def cmd_orbital_graph(self, args):
        """
        Generates a comparative graph.
        Usage: graph [distance|period|radii|inclination]
        """
        valid_metrics = ["distance", "period", "radii", "inclination"]
        if not args or args[0].lower() not in valid_metrics:
            print(f"\033[91mERROR\033[0m: Please specify the metric. Available: {', '.join(valid_metrics)}.")
            return

        metric = args[0].lower()
        
        if metric == 'radii':
            self._graph_tetnobautte_radii()
        elif metric == 'inclination':
            self._graph_t_system_metrics(metric)
        else:
            self._graph_t_system_metrics(metric)

    def _graph_t_system_metrics(self, metric):
        """Helper to graph distance/period/inclination for AU/Year systems."""
        if metric == 'distance':
            metric_key = 'distance_au'
            metric_label = 'ORBITAL DISTANCE (AU)'
        elif metric == 'period':
            metric_key = 'period_yr'
            metric_label = 'ORBITAL PERIOD (Standard YR)'
        elif metric == 'inclination':
            metric_key = 'inclination_deg'
            metric_label = 'ORBITAL INCLINATION (Degrees)'
        else:
            return # Should not happen based on calling function

        print(f"\n--- COMPARATIVE PLANETARY GRAPH (Standard T-Systems): {metric_label} ---")
        print("Note: Tetnobautte system data is excluded due to incompatible metrics.\n")
        
        # Collect and flatten all AU/Year planetary data
        all_planets = []
        for sys_name, sys_data in SYSTEM_DATA.items():
            if sys_name == 'TETNOBAUTTE': continue
            for planet_name, p_data in sys_data['planets'].items():
                all_planets.append({
                    "name": f"{planet_name} ({sys_name})",
                    "value": p_data[metric_key],
                    "color_code": p_data['color_code']
                })

        if not all_planets:
            print("\033[93mWARNING\033[0m: No standard T-System data available for graphing.")
            return

        max_val = max(p['value'] for p in all_planets)
        SCALE = 50 / max_val # Max bar length 50 characters
        sorted_planets = sorted(all_planets, key=lambda x: x['value'])

        print(f"  {'PLANET (SYSTEM)':<25} | {metric_label} (Max: {max_val:.2f})")
        print("  " + "=" * 70)

        for planet in sorted_planets:
            value = planet['value']
            bar_len = max(1, int(value * SCALE)) # Ensure a minimum bar length of 1
            planet_color_fg = f"\033[{planet['color_code']}m"
            bar = f"\033[40m{planet_color_fg}█" + "█" * (bar_len-1) + "\033[0m" + "░" * (50 - bar_len)
            print(f"  {planet['name']:<25} | {bar} {value:.2f}")

        print("\nMaximum scale set by the largest object in the analyzed dataset.\n")


    def _graph_tetnobautte_radii(self):
        """Helper to graph scaled radii for the Tetnobautte system."""
        print("\n--- COMPARATIVE PLANETARY GRAPH (TETNOBAUTTE LENS): SCALED RADII ---")
        print(f"Reference: tetnobautte = 105 Scaled Radii\n")
        
        tetnobautte_planets = TETNOBAUTTE_DATA['planets']
        
        all_planets = []
        for planet_name, p_data in tetnobautte_planets.items():
            all_planets.append({
                "name": planet_name,
                "value": p_data['radii'],
                "color_code": p_data['color_code'],
                "status": p_data['status']
            })

        max_val = max(p['value'] for p in all_planets)
        SCALE = 50 / max_val
        sorted_planets = sorted(all_planets, key=lambda x: x['value'])

        print(f"  {'PLANET NAME':<25} | SCALED RADII (Max: {max_val})")
        print("  " + "=" * 70)

        for planet in sorted_planets:
            value = planet['value']
            bar_len = max(1, int(value * SCALE))
            planet_color_fg = f"\033[{planet['color_code']}m"
            
            # Use background color to highlight status (Green for Habitable, Gray for Uninhabitable)
            status_bg = "\033[42m" if planet['status'] == "HABITABLE" else "\033[40m" 
            
            bar = f"{status_bg}{planet_color_fg}█" + "█" * (bar_len-1) + "\033[0m" + "░" * (50 - bar_len)
            
            print(f"  {planet['name']:<25} | {bar} {value}")

        print("\nHabitable planets displayed with a green background for easy identification.\n")


    def cmd_clear(self, args):
        """Clears the terminal screen (approximation for cross-platform)."""
        os.system('cls' if os.name == 'nt' else 'clear')


    def cmd_quit(self, args=None):
        """Exits the simulation."""
        print("\nClosing Multi-Locus Connection...")
        print(f"{SHELL_NAME} OS {VERSION} session terminated. Data integrity confirmed.")
        print("Goodbye.\n")
        self.running = False


if __name__ == "__main__":
    emulator = SLPOESimulator()
    emulator.run()

