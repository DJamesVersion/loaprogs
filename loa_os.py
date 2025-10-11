import os
import sys
import time
import random
from typing import Dict, List, Any, Callable

# --- ANSI Color Configuration ---
# These codes work best on Linux/macOS terminals. They may display as plain text on some Windows setups.
GREEN = '\033[92m'
BRIGHT_GREEN = '\033[92;1m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

# --- Global Configuration and State ---

VERSION = "3.0.0 (Build 20251010)"
APP_NAME = "LoA Operating System"

# File system structure: Keys are drive letters (e.g., "C:", "D:").
# Each drive is a dictionary object with 'type', 'label', and 'contents'.
FILESYSTEM: Dict[str, Any] = {
    "C:": {
        "type": "DIR",
        "label": "LOA_MAIN",
        "contents": {
            "SYSTEM": {"type": "DIR", "contents": {}},
            "PROGRAMS": {"type": "DIR", "contents": {}},
            "README.TXT": {"type": "FILE", "size": 1200, "date": "04/10/2025", "content": "Welcome to LoA OS! Type HELP for commands. Try: CD PROGRAMS, DIR, or LOA.EXE."},
            "COMMAND.COM": {"type": "FILE", "size": 32134, "date": "01/01/1994", "content": "System Kernel"},
            "LOA.EXE": {"type": "EXE", "size": 512, "date": "04/10/2025", "content": "BUILTIN_LOA"},
        }
    }
}

# State variables
CURRENT_PATH: List[str] = ["C:"]
PROMPT: str = f"{GREEN}C:\\>{RESET}"

# --- Utility Functions ---

def clear_screen():
    """Clears the console screen using system-specific commands."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def print_slowly(text: str, delay: float = 0.005):
    """Prints text character by character for a retro typewriter effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def update_prompt():
    """Updates the global PROMPT variable based on the current path."""
    global PROMPT
    PROMPT = f"{BRIGHT_GREEN}{'\\'.join(CURRENT_PATH)}>{RESET} "

def get_current_directory() -> Dict[str, Any] | None:
    """Returns the 'contents' dictionary object of the current directory."""
    
    if not CURRENT_PATH:
        return None

    # Start from the drive root
    if CURRENT_PATH[0] not in FILESYSTEM:
        return None
        
    current_item = FILESYSTEM[CURRENT_PATH[0]]
    
    # Traverse subdirectories
    for segment in CURRENT_PATH[1:]:
        if current_item['type'] == 'DIR' and segment in current_item['contents']:
            current_item = current_item['contents'][segment]
        else:
            return None # Invalid path segment
            
    # Return the contents of the final directory item
    return current_item['contents']

def resolve_path(path_str: str) -> List[str] | None:
    """Resolves a relative or absolute path string to a list of segments."""
    segments = path_str.upper().replace("/", "\\").split("\\")
    segments = [s for s in segments if s]

    if not segments:
        return list(CURRENT_PATH)

    # Check for drive letter change
    is_absolute = False
    if len(segments[0]) == 2 and segments[0].endswith(":") and segments[0] in FILESYSTEM:
        resolved_path = [segments[0]]
        segments = segments[1:]
        is_absolute = True
    elif CURRENT_PATH:
        resolved_path = list(CURRENT_PATH)
    else:
        # Should not happen if C: is initialized
        return None

    # Process segments
    for segment in segments:
        if segment == '.':
            continue
        elif segment == '..':
            if len(resolved_path) > 1: # Cannot go above the drive root
                resolved_path.pop()
        else:
            if is_absolute:
                # If absolute path, reset path and start from current drive root
                resolved_path.append(segment)
            else:
                # Relative path navigation
                resolved_path.append(segment)
                
    # Basic validation: ensure the resolved path starts with a valid drive
    if not resolved_path or resolved_path[0] not in FILESYSTEM:
        return None
        
    return resolved_path

# --- Built-in Program Logic ---

def _builtin_loa_program():
    """The special, custom program execution."""
    print_slowly(f"\n{YELLOW}***** Running LOA.EXE *****{RESET}", 0.01)
    print_slowly("> Initiating Aspiration Protocol...", 0.02)
    print_slowly("> Verifying Core Beliefs...", 0.03)
    print_slowly("> Processing Input...", 0.03)
    
    print(f"\n    {CYAN}Success is not final, failure is not fatal:{RESET}")
    print(f"    {CYAN}it is the courage to continue that counts.{RESET}")
    print("    - W. Churchill")
    
    print_slowly("\n> Mission Complete.", 0.02)
    print_slowly(f"{YELLOW}***** Program Terminated *****{RESET}\n", 0.01)

def execute_program(command: str, args: List[str]) -> bool:
    """Simulates running an EXE file or a simple user-created program."""
    current_dir_contents = get_current_directory()
    if not current_dir_contents:
        return False
        
    target_name = command.upper()
    
    # Search for the executable in the current directory
    if target_name in current_dir_contents:
        item = current_dir_contents[target_name]
        
        # 1. Built-in EXE program
        if item['type'] == 'EXE' and item['content'] == 'BUILTIN_LOA':
            _builtin_loa_program()
            return True

        # 2. Simple LoA Scripting (Any FILE starting with RUN:)
        if item['type'] == 'FILE' and item['content'].strip().upper().startswith("RUN:"):
            print(f"\n{CYAN}Executing LoA Script: {target_name}...{RESET}")
            script_lines = item['content'].strip()[4:].strip().split('\n')
            
            for line in script_lines:
                if not line.strip(): continue # Skip empty lines
                print(f"[{target_name}] > {line}")
                # Simple recursive execution for script commands
                process_command(line)
                time.sleep(0.1) 
            
            print(f"{CYAN}Execution of {target_name} complete.{RESET}")
            return True
        
    return False # Not an executable

# --- Command Handlers ---

def cmd_ver(_: List[str]):
    """Displays the LoA OS version."""
    print(f"{APP_NAME} [Version {VERSION}]")

def cmd_cls(_: List[str]):
    """Clears the console screen."""
    clear_screen()

def cmd_exit(_: List[str]):
    """Exits the emulator."""
    print_slowly("Shutting down LoA OS. Goodbye!", 0.03)
    sys.exit(0)

def cmd_help(_: List[str]):
    """Displays a list of available commands."""
    help_text = f"""
{BRIGHT_GREEN}Available LoA OS Commands:{RESET}

CLS     - Clears the screen.
DIR     - Displays a list of files and subdirectories.
CD      - Changes the current directory or drive (e.g., CD .., CD D:).
MOUNT   - Mounts a new virtual drive (Usage: MOUNT <drive_letter>: <label>).
ECHO    - Displays messages.
EDIT    - Creates or modifies a text file (Usage: EDIT <filename>).
VER     - Displays the LoA OS version.
ABOUT   - Displays information about the system's purpose.
<FILE>  - Execute an EXE or simple LoA Script file.
HELP    - Displays this list of commands.
EXIT    - Terminates the LoA OS session.
"""
    print(help_text)

def cmd_dir(_: List[str]):
    """Displays the contents of the current directory."""
    current_path_str = '\\'.join(CURRENT_PATH)
    current_dir_contents = get_current_directory()
    
    if not current_dir_contents:
        print(f"{RED}Error: Path not found: {current_path_str}{RESET}")
        return

    drive_letter = CURRENT_PATH[0]
    drive_info = FILESYSTEM.get(drive_letter, {})
    drive_label = drive_info.get("label", "NO NAME")
    
    output = f"""
 Volume in drive {drive_letter} is {drive_label}
 Volume Serial Number is LOA-1994

 Directory of {current_path_str}\\

"""
    file_count = 0
    total_bytes = 0
    
    # Sort keys for cleaner output
    sorted_keys = sorted(current_dir_contents.keys())
    
    for name in sorted_keys:
        item = current_dir_contents[name]
        item_date = item.get("date", time.strftime("%m/%d/%Y"))
        
        if item["type"] == "DIR":
            output += f" {item_date.ljust(10)}  {'12:00p'.ljust(7)}  {CYAN}<DIR>{RESET}          {name}\n"
        else:
            size_str = str(item.get('size', 0)).rjust(10)
            total_bytes += item.get('size', 0)
            file_count += 1
            output += f" {item_date.ljust(10)}  {'12:00p'.ljust(7)} {size_str} {name}\n"

    # Simulated free space
    free_bytes = 33_554_432 
    
    output += f"""
         {str(file_count).rjust(3)} File(s)   {str(total_bytes).rjust(14)} bytes
         {str(len(current_dir_contents) - file_count).rjust(3)} Dir(s)  {str(free_bytes).rjust(14)} bytes free
"""
    print(output)

def cmd_cd(args: List[str]):
    """Changes the current directory or drive."""
    global CURRENT_PATH
    
    if not args:
        print(f"Current Directory: {'\\'.join(CURRENT_PATH)}\\")
        return
        
    path_str = args[0]
    target_segments = resolve_path(path_str)
    
    if not target_segments:
        print(f"{RED}Invalid path or drive specification: {path_str}{RESET}")
        return
        
    # Check if the target is just a drive letter (e.g., D:)
    if len(target_segments) == 1 and target_segments[0] in FILESYSTEM:
        CURRENT_PATH = target_segments # Change to the root of the new drive
        update_prompt()
        return

    # Full path validation
    current_dir = FILESYSTEM
    is_valid = True
    temp_item = FILESYSTEM.get(target_segments[0])
    
    if not temp_item:
        is_valid = False
    
    if is_valid:
        temp_dir_contents = temp_item['contents']
        for segment in target_segments[1:]:
            if segment not in temp_dir_contents:
                is_valid = False
                break
            
            next_item = temp_dir_contents[segment]
            
            if next_item['type'] != 'DIR':
                is_valid = False
                break
                
            temp_dir_contents = next_item['contents'] # Move deeper
            
    if is_valid:
        CURRENT_PATH = target_segments
        update_prompt()
    else:
        print(f"{RED}The system cannot find the path specified: {path_str}{RESET}")
        
def cmd_mount(args: List[str]):
    """Mounts a new virtual drive."""
    if len(args) < 1:
        print("Usage: MOUNT <drive_letter>: [label]")
        print("\nMounted Drives:")
        for drive in FILESYSTEM:
            print(f"  {drive}  ({FILESYSTEM[drive].get('label', 'NO NAME')})")
        return

    drive_spec = args[0].upper()
    drive_letter = drive_spec.strip(':')
    drive_label = " ".join(args[1:]) if len(args) > 1 else "VIRTUAL_DISK"

    if len(drive_letter) != 1 or not drive_letter.isalpha():
        print(f"{RED}Error: Invalid drive letter format. Must be a single letter followed by a colon (e.g., D:).{RESET}")
        return
    
    if drive_spec in FILESYSTEM:
        print(f"{RED}Error: Drive {drive_spec} is already mounted.{RESET}")
        return

    # Check for reserved letters (e.g., B: is often floppy, but we allow mounting anything not C)
    if drive_letter in 'C':
        print(f"{RED}Error: Drive {drive_spec} is reserved or already in use.{RESET}")
        return

    FILESYSTEM[drive_spec] = {
        "type": "DIR",
        "label": drive_label,
        "contents": {
            "DATA": {"type": "DIR", "contents": {}},
            f"{drive_letter}_INFO.TXT": {"type": "FILE", "size": 50, "date": time.strftime("%m/%d/%Y"), "content": f"Drive {drive_spec} is mounted."}
        }
    }
    
    print(f"{GREEN}Drive {drive_spec} mounted successfully with label '{drive_label}'.{RESET}")


def cmd_echo(args: List[str]):
    """Displays text passed as arguments."""
    if not args:
        print(f"{BRIGHT_GREEN}ECHO is ON.{RESET}")
    else:
        print(" ".join(args))

def cmd_edit(args: List[str]):
    """Creates or modifies a text file."""
    if not args:
        print("Usage: EDIT <filename>")
        return

    filename = args[0].upper()
    current_dir_contents = get_current_directory()

    if not current_dir_contents:
        print(f"{RED}Error: Could not access current directory.{RESET}")
        return

    if filename in current_dir_contents and current_dir_contents[filename]['type'] == 'DIR':
        print(f"{RED}Cannot edit a directory: {filename}{RESET}")
        return
    
    # Existing content or new content
    initial_content = current_dir_contents[filename]['content'] if filename in current_dir_contents else ""
    
    print(f"\n{YELLOW}--- LoA OS Simple Editor --- (Type 'SAVE' on a new line to finish){RESET}")
    print("------------------------------------------------------------------")
    print(initial_content)
    print("------------------------------------------------------------------")
    
    # Use a list to build up the new content line by line
    new_content_lines = initial_content.split('\n') if initial_content else []
    print("\nStart typing below. New content will be appended. Use 'SAVE' to finish.")

    while True:
        try:
            line = input(" > ") # Enhanced editor prompt
            if line.upper() == 'SAVE':
                break
            new_content_lines.append(line)
        except EOFError:
            print(f"\n{RED}Aborted without saving.{RESET}")
            return
        except KeyboardInterrupt:
            print(f"\n{RED}Aborted without saving.{RESET}")
            return

    # Join lines and save the file
    content_to_save = "\n".join(new_content_lines)
    
    # Determine if it's a regular file or an EXE/script based on content prefix
    item_type = 'FILE'
    if content_to_save.strip().upper().startswith("RUN:"):
        item_type = 'FILE' # Keep it as FILE, execution logic handles RUN: prefix
    
    # Update/create the file in the FS
    current_dir_contents[filename] = {
        "type": item_type,
        "size": len(content_to_save),
        "date": time.strftime("%m/%d/%Y"),
        "content": content_to_save
    }
    
    print(f"\n{GREEN}File '{filename}' saved. Size: {len(content_to_save)} bytes.{RESET}")

def cmd_about(_: List[str]):
    """Displays information about the emulator."""
    print(f"""
{CYAN}======================================================{RESET}
  {BRIGHT_GREEN}{APP_NAME} (CLI Simulation){RESET}
{CYAN}======================================================{RESET}
  This is a console application simulating a retro
  DOS-like environment with support for multiple
  drives and simple scripting.

  LoA stands for "{BRIGHT_GREEN}The Operating System of Aspiration{RESET}".
""")

COMMAND_HANDLERS: Dict[str, Callable[[List[str]], None]] = {
    "VER": cmd_ver,
    "CLS": cmd_cls,
    "HELP": cmd_help,
    "DIR": cmd_dir,
    "CD": cmd_cd,
    "MOUNT": cmd_mount,
    "ECHO": cmd_echo,
    "EDIT": cmd_edit,
    "ABOUT": cmd_about,
    "EXIT": cmd_exit
}

# --- Main Logic ---

def boot_sequence():
    """Displays the initial boot screen and messages."""
    clear_screen()
    
    boot_messages = [
        f"\n  {BRIGHT_GREEN}.  LoA OS - The Operating System of Aspiration  .{RESET}",
        f"  ................................................{RESET}\n",
        f"Copyright (C) 2025 LoA Corporation. All Rights Reserved.",
        f"LoA OS Version {VERSION}\n",
        f"Memory Check: 640 KB Base Memory {GREEN}OK.{RESET}",
        f"Extended Memory: 32768 KB {GREEN}OK.{RESET}",
        f"Searching for drives... Drive C: found.",
        f"Loading COMMAND.COM... {GREEN}Done.{RESET}\n",
        f"Type HELP for a list of available commands."
    ]

    for message in boot_messages:
        print_slowly(message, 0.002)
        time.sleep(0.1)
    
    update_prompt() # Initialize the prompt

def process_command(user_input: str):
    """Parses and executes a single command string."""
    parts = user_input.split()
    if not parts:
        return
        
    command = parts[0].upper()
    args = parts[1:]
    
    # 1. Check built-in commands
    handler = COMMAND_HANDLERS.get(command)
    
    if handler:
        handler(args)
    else:
        # 2. Check for program execution
        if not execute_program(command, args):
            print(f"{RED}Bad command or file name: {command}{RESET}")

def command_loop():
    """The main loop that takes user input and executes commands."""
    
    try:
        while True:
            # Print the prompt (which is updated globally)
            user_input = input(PROMPT).strip()
            
            if not user_input:
                continue

            # Process the command
            process_command(user_input)
                
    except EOFError:
        cmd_exit(None)
    except KeyboardInterrupt:
        print("\n\nSession interrupted.")
        cmd_exit(None)
    except Exception as e:
        print(f"{RED}An unexpected critical error occurred: {e}{RESET}")
        time.sleep(1)
        
if __name__ == "__main__":
    boot_sequence()
    command_loop()

