import os
import subprocess
import sys

# --- Configuration and Environment ---
APP_NAME = "LoA OS 9ehd"
VERSION = "1.0.0"
PROMPT_CHAR = "λ" # Lambda character for an advanced prompt

# Define aliases for the user's requested "virtual" commands
VIRTUAL_COMMANDS = {
    "sh_git": "git",
    "cmake-debian": "cmake",
    "py": "python3" # Shorter alias for python
}

# Terminal color codes (optional, but makes it look better)
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def display_header():
    """Prints a stylized welcome message for the shell."""
    print(Colors.HEADER + "=" * 60 + Colors.ENDC)
    print(f"{Colors.BOLD}*** {APP_NAME} | Advanced Multi-Environment Shell Emulator ***{Colors.ENDC}")
    print(f"Version {VERSION}. Type '{Colors.OKCYAN}help{Colors.ENDC}' for command list or '{Colors.FAIL}exit{Colors.ENDC}' to quit.")
    print(Colors.HEADER + "=" * 60 + Colors.ENDC)

def get_current_prompt(username="user"):
    """Generates the dynamic shell prompt (username@current_path λ)"""
    # Get current working directory, shorten if necessary
    cwd = os.getcwd()
    home = os.path.expanduser("~")
    display_cwd = cwd.replace(home, "~", 1)

    return f"{Colors.OKGREEN}{username}{Colors.ENDC}@{Colors.OKBLUE}{display_cwd}{Colors.ENDC} {PROMPT_CHAR} "

def handle_internal_command(command, args):
    """Handles commands built directly into the Python script (cd, exit, help, clear)."""
    if command == "exit":
        print(f"{Colors.WARNING}Exiting {APP_NAME}. Goodbye!{Colors.ENDC}")
        sys.exit(0)

    elif command == "cd":
        # 'cd' must be handled internally using os.chdir
        target_dir = args[0] if args else os.path.expanduser("~")
        try:
            os.chdir(target_dir)
            # Print new directory path (optional, but helpful)
            print(f"Changed directory to: {Colors.OKBLUE}{os.getcwd()}{Colors.ENDC}")
        except FileNotFoundError:
            print(f"{Colors.FAIL}Error: Directory not found: {target_dir}{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}Error changing directory: {e}{Colors.ENDC}")
        return True

    elif command == "help":
        print(f"\n{Colors.UNDERLINE}Available Environments and Aliases:{Colors.ENDC}")
        print(f"  - {Colors.OKGREEN}python/py{Colors.ENDC}      : Execute Python code or scripts (runs 'python3' or 'python').")
        print(f"  - {Colors.OKGREEN}gcc{Colors.ENDC}            : Compile C/C++ code.")
        print(f"  - {Colors.OKGREEN}npm{Colors.ENDC}            : Node Package Manager (if installed on host).")
        print(f"  - {Colors.OKGREEN}sh_git{Colors.ENDC}         : Alias for standard {Colors.OKCYAN}git{Colors.ENDC} commands.")
        print(f"  - {Colors.OKGREEN}cmake-debian{Colors.ENDC}   : Alias for standard {Colors.OKCYAN}cmake{Colors.ENDC} commands.")
        print(f"\n{Colors.UNDERLINE}Internal Commands:{Colors.ENDC}")
        print(f"  - {Colors.OKCYAN}cd [path]{Colors.ENDC}      : Change directory.")
        print(f"  - {Colors.OKCYAN}exit{Colors.ENDC}           : Quit the shell.")
        print(f"  - {Colors.OKCYAN}clear{Colors.ENDC}          : Clears the terminal screen.")
        print(f"  - {Colors.OKCYAN}help{Colors.ENDC}           : Displays this message.")
        print(f"\n{Colors.UNDERLINE}Standard Shell Commands:{Colors.ENDC}")
        print("  - Any other command (ls, dir, mkdir, nano, touch, etc.) is passed directly to the host system.")
        print("  - Note: File extension checks (like '.c' or '.py') will automatically route to the appropriate tool.")
        print("-" * 60 + "\n")
        return True

    elif command == "clear":
        # Clears the terminal screen (works on most systems)
        os.system('cls' if os.name == 'nt' else 'clear')
        display_header()
        return True

    return False

def execute_external_command(full_command, command_name, original_input):
    """Executes a command via the host system's shell using subprocess."""
    print(f"{Colors.WARNING}Running command in host shell: '{' '.join(full_command)}'{Colors.ENDC}")
    
    try:
        # Use subprocess.run to execute the command.
        # shell=True allows execution of complex commands like 'ls -l | grep file'
        process = subprocess.run(
            full_command,
            shell=True,
            check=False, # Don't raise an exception for non-zero exit codes (like failing a test)
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if process.stdout:
            print(f"{Colors.OKCYAN}--- Output ---{Colors.ENDC}")
            print(process.stdout.strip())
            print(f"{Colors.OKCYAN}--- End Output ---{Colors.ENDC}")

        if process.stderr and process.returncode != 0:
            print(f"{Colors.FAIL}--- Error ({command_name}) ---{Colors.ENDC}")
            print(process.stderr.strip())
            print(f"{Colors.FAIL}--- End Error ---{Colors.ENDC}")
        
        # Specific success message for compilation/execution
        if process.returncode == 0:
             print(f"{Colors.OKGREEN}Command completed successfully.{Colors.ENDC}")

    except FileNotFoundError:
        print(f"{Colors.FAIL}Error: Command '{command_name}' not found. Ensure the required environment/tool is installed on your host system (e.g., 'git', 'npm', 'gcc').{Colors.ENDC}")
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Command interrupted by user.{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}An unexpected execution error occurred: {e}{Colors.ENDC}")

def run_shell():
    """The main loop of the LoA OS shell emulator."""
    display_header()

    while True:
        try:
            # Get user input
            raw_input = input(get_current_prompt()).strip()
            if not raw_input:
                continue

            # Split input into command and arguments
            parts = raw_input.split()
            command = parts[0].lower()
            args = parts[1:]

            # 1. Handle Internal Commands (cd, exit, help, clear)
            if handle_internal_command(command, args):
                continue

            # 2. Determine and execute the external command
            
            # Check for file extension routing (C, Python)
            if any(arg.endswith('.c') for arg in args) or command == 'gcc':
                # Route to C compiler (defaulting to gcc)
                target_command = ['gcc'] + args
                command_name = "GCC"
            elif any(arg.endswith('.py') for arg in args) or command in ('python', 'python3', 'py'):
                # Route to Python interpreter
                # We need to prepend the interpreter command itself
                target_command = ['python3'] + args if os.name != 'nt' else ['python'] + args
                command_name = "Python"
            
            # Check for virtual command aliases
            elif command in VIRTUAL_COMMANDS:
                target_cmd_name = VIRTUAL_COMMANDS[command]
                target_command = [target_cmd_name] + args
                command_name = target_cmd_name.upper()

            # Check for specific external commands (npm)
            elif command == 'npm':
                target_command = [command] + args
                command_name = "NPM"

            # 3. Default: Treat as a standard system command (ls, dir, nano, etc.)
            else:
                target_command = [command] + args
                command_name = command.upper()
            
            # Execute the determined command
            execute_external_command(target_command, command_name, raw_input)

        except EOFError:
            # Handle Ctrl+D
            print(f"\n{Colors.WARNING}Exiting {APP_NAME}. Goodbye!{Colors.ENDC}")
            break
        except KeyboardInterrupt:
            # Handle Ctrl+C
            print(f"\n{Colors.WARNING}Session interrupted. Type '{Colors.FAIL}exit{Colors.ENDC}' to quit.{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}A fatal error occurred: {e}{Colors.ENDC}")
            break

if __name__ == "__main__":
    run_shell()

