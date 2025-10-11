import datetime
import time
import json
import uuid

# --- Mission Constants ---
TOTAL_MISSION_DAYS = 1330

KEY_ARTIFACTS = [
    'ps-686657',
    'nss-23-7417411',
    'nasm-1894977',
    'aamb-11022429',
    'ps*-2853',
    'boinc-109090',
    'itu-1200527740'
]

# --- Application State (Simulating Database/Shared State) ---
# In a real-world Python application (like a Flask or Django backend), 
# this data would be stored persistently in a database like Firestore.
app_state = {
    'user_id': str(uuid.uuid4()),
    'role': 'Scientist',
    'mission_status': {
        'start_date': None,  # Will store a datetime object
        'is_active': False
    },
    'evidence_log': [] # List of dictionaries for submitted evidence
}

# --- Core Mission Logic ---

def set_user_role(role_choice):
    """Sets the user's role for evidence submission."""
    roles = {'1': 'Scientist', '2': 'Mission Control'}
    role = roles.get(role_choice)
    if role:
        app_state['role'] = role
        print(f"\n[SYSTEM] Role set to: {role}")
    else:
        print("[ERROR] Invalid choice. Role remains: Scientist")

def start_mission():
    """Initiates the 1330-day round-trip countdown."""
    if app_state['mission_status']['is_active']:
        print("\n[ALERT] Mission already underway!")
        return

    # Using datetime.datetime.now() to mark the start time
    app_state['mission_status']['start_date'] = datetime.datetime.now()
    app_state['mission_status']['is_active'] = True
    print("\n[MISSION CONTROL] Countdown initiated!")
    print(f"Mission Start Time: {app_state['mission_status']['start_date'].strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target Round-Trip Duration: {TOTAL_MISSION_DAYS} days.")

def get_mission_time():
    """Calculates elapsed time and days remaining."""
    start_date = app_state['mission_status']['start_date']
    if not start_date:
        return 0, TOTAL_MISSION_DAYS, 0.0

    time_elapsed = datetime.datetime.now() - start_date
    days_elapsed = time_elapsed.total_seconds() / (60 * 60 * 24)
    days_remaining = max(0, TOTAL_MISSION_DAYS - days_elapsed)
    
    progress = min(100.0, (days_elapsed / TOTAL_MISSION_DAYS) * 100)
    
    return round(days_elapsed), round(days_remaining), progress

def submit_evidence():
    """Collects and logs new evidence from the user."""
    days_elapsed, _, _ = get_mission_time()

    print("\n--- Evidence Log Submission ---")
    title = input("Enter Title/Hypothesis Summary: ").strip()
    content = input("Enter Detailed Inspection Data: ").strip()

    if not title or not content:
        print("[ERROR] Title and content cannot be empty. Evidence submission canceled.")
        return

    new_evidence = {
        'id': str(uuid.uuid4()),
        'title': title,
        'content': content,
        'submitted_by': app_state['user_id'],
        'role': app_state['role'],
        'day_logged': days_elapsed,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    app_state['evidence_log'].append(new_evidence)
    print(f"\n[SUCCESS] Evidence logged on Day {days_elapsed} by {app_state['role']}.")

# --- Display Functions ---

def display_artifacts():
    """Prints the list of critical waypoint identifiers."""
    print("\n--- FOSSE & LYOT CRATER WAYPOINT IDENTIFIERS ---")
    for i, artifact in enumerate(KEY_ARTIFACTS):
        print(f"  [{i+1}] {artifact}")
    print("-" * 50)

def display_status():
    """Prints the current mission progress and user info."""
    days_elapsed, days_remaining, progress = get_mission_time()
    
    print("\n" + "=" * 50)
    print("        MARS ROUND-TRIP ARTIFACT MANAGER")
    print("=" * 50)
    print(f"| User ID: {app_state['user_id']}")
    print(f"| User Role: {app_state['role']}")
    print("-" * 50)

    if app_state['mission_status']['is_active']:
        if days_remaining > 0:
            print(f"| STATUS: MISSION ACTIVE")
            print(f"| Rendezvous Target: Fosse & Lyot Crater")
            print(f"| Days Elapsed: {days_elapsed} (Progress: {progress:.2f}%)")
            print(f"| Days Remaining: {days_remaining} / {TOTAL_MISSION_DAYS}")
        else:
            print(f"| STATUS: MISSION COMPLETE!")
            print(f"| SUCCESS: Round-trip completed in {days_elapsed} days.")
    else:
        print("| STATUS: MISSION PENDING")
        print(f"| Duration: {TOTAL_MISSION_DAYS} days (round-trip)")
    print("=" * 50)

def display_evidence():
    """Prints the chronological log of all submitted evidence."""
    if not app_state['evidence_log']:
        print("\n[LOG] Evidence board is empty. Start inspecting!")
        return

    print("\n--- EVIDENCE INSPECTION BOARD (Latest First) ---")
    # Sort by day logged (in reverse order for latest first)
    sorted_log = sorted(app_state['evidence_log'], key=lambda x: x['day_logged'], reverse=True)
    
    for item in sorted_log:
        print(f"\n[ID: {item['id'][:8]}] DAY {int(item['day_logged'])}")
        print(f"  -> Title: {item['title']}")
        print(f"  -> Content: {item['content']}")
        print(f"  -> Submitted by: {item['role']} ({item['submitted_by'][:8]}...) at {item['timestamp']}")
    print("-" * 50)


# --- Main CLI Loop ---

def main_menu():
    """Displays the interactive menu."""
    display_status()
    print("\n[ACTION MENU]")
    print("1. Start 1330-Day Mission Countdown")
    print("2. Change User Role (Current: " + app_state['role'] + ")")
    print("3. Log New Evidence")
    print("4. View All Evidence Log")
    print("5. View Key Artifact Identifiers")
    print("6. Exit")
    
    choice = input("Enter choice (1-6): ").strip()
    return choice

def run_manager():
    """The main application entry point."""
    print("Initializing Martian Waypoint Manager...")
    
    while True:
        choice = main_menu()
        
        if choice == '1':
            start_mission()
        
        elif choice == '2':
            print("\n[ROLE SELECTION]")
            role_choice = input("Select Role (1=Scientist, 2=Mission Control): ").strip()
            set_user_role(role_choice)
            
        elif choice == '3':
            if app_state['mission_status']['is_active']:
                submit_evidence()
            else:
                print("\n[ALERT] Mission must be started before logging evidence. Select option 1.")
        
        elif choice == '4':
            display_evidence()

        elif choice == '5':
            display_artifacts()

        elif choice == '6':
            print("\n[SYSTEM] Manager shutting down. Safe journey!")
            break
        
        else:
            print("\n[ERROR] Invalid choice. Please select a number from 1 to 6.")
        
        # Pause for better readability in the CLI
        if choice != '6':
            input("\nPress Enter to continue...")
            # Simulate a small passage of time for countdown visualization
            if app_state['mission_status']['is_active']:
                time.sleep(0.01)

if __name__ == '__main__':
    run_manager()

