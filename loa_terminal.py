import sys
import os
import time

# Platform-specific functions for getting a single character without waiting for Enter
try:
    # Unix-like systems (Linux, macOS)
    import tty
    import termios

    def getch():
        """Gets a single character from standard input on Unix-like systems."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

except ImportError:
    # Windows
    import msvcrt
    def getch():
        """Gets a single character from standard input on Windows."""
        return msvcrt.getch().decode()

# ANSI color codes for styling the terminal output
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    # Text colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

class LoaTerminal:
    """
    A class representing the LOA Terminal Emulator.
    It manages the file system, commands, and the main application loop.
    """
    def __init__(self):
        self.current_path = '/home/guest'
        self.fs = self._initialize_fs()
        self.commands = self._initialize_commands()

    def _initialize_fs(self):
        """Sets up the virtual file system as a dictionary."""
        return {
            '/': {'type': 'dir', 'children': ['home', 'bin', 'etc']},
            '/home': {'type': 'dir', 'children': ['guest']},
            '/home/guest': {'type': 'dir', 'children': ['documents', 'welcome.txt']},
            '/home/guest/documents': {'type': 'dir', 'children': ['project-alpha.txt']},
            '/home/guest/documents/project-alpha.txt': {'type': 'file', 'content': 'Project Alpha: Inception Report.\nStatus: TOP SECRET.'},
            '/home/guest/welcome.txt': {'type': 'file', 'content': 'Welcome to the LOA Operating System!\nType "help" to see a list of available commands.'},
            '/bin': {'type': 'dir', 'children': ['tahkmahnelle', 'sysmon']},
            '/bin/tahkmahnelle': {'type': 'file', 'content': 'File Manager Executable'},
            '/bin/sysmon': {'type': 'file', 'content': 'System Monitor'},
            '/etc': {'type': 'dir', 'children': ['config.sys']},
            '/etc/config.sys': {'type': 'file', 'content': 'KERNEL=loa.core\nSHELL=tahk.sh'}
        }

    def _initialize_commands(self):
        """Maps command strings to their corresponding methods."""
        return {
            'help': self._cmd_help,
            'ls': self._cmd_ls,
            'cd': self._cmd_cd,
            'pwd': self._cmd_pwd,
            'cat': self._cmd_cat,
            'echo': self._cmd_echo,
            'clear': self._cmd_clear,
            'tahkmahnelle': self._run_tahkmahnelle,
            'exit': self._cmd_exit,
            'quit': self._cmd_exit,
        }
        
    def _resolve_path(self, path):
        """Converts a relative or complex path to a simplified, absolute path."""
        if path.startswith('/'):
            # Absolute path
            new_path_parts = []
        else:
            # Relative path
            new_path_parts = self.current_path.strip('/').split('/') if self.current_path != '/' else []

        for part in path.split('/'):
            if not part or part == '.':
                continue
            if part == '..':
                if new_path_parts:
                    new_path_parts.pop()
            else:
                new_path_parts.append(part)
        
        return '/' + '/'.join(new_path_parts)

    def _get_prompt(self):
        """Builds the colored command prompt string."""
        path_display = self.current_path.replace('/home/guest', '~')
        return (
            f"{Colors.GREEN}guest@loa{Colors.RESET}:"
            f"{Colors.MAGENTA}{path_display}{Colors.RESET}$ "
        )

    # --- Command Implementations ---

    def _cmd_help(self, args):
        """Prints the list of available commands."""
        print(f"""
LOA OS Command List:
  {Colors.CYAN}help{Colors.RESET}          - Shows this list
  {Colors.CYAN}ls [path]{Colors.RESET}     - Lists directory contents
  {Colors.CYAN}cd [path]{Colors.RESET}     - Changes the current directory
  {Colors.CYAN}pwd{Colors.RESET}           - Prints the current working directory
  {Colors.CYAN}cat [file]{Colors.RESET}    - Displays file content
  {Colors.CYAN}echo [text]{Colors.RESET}   - Prints text to the terminal
  {Colors.CYAN}clear{Colors.RESET}         - Clears the terminal screen
  {Colors.CYAN}tahkmahnelle{Colors.RESET}  - Starts the interactive file manager
  {Colors.CYAN}exit / quit{Colors.RESET} - Exits the LOA terminal
        """)

    def _cmd_ls(self, args):
        """Lists contents of a directory."""
        target_path = self._resolve_path(args[0]) if args else self.current_path
        node = self.fs.get(target_path)
        if node and node['type'] == 'dir':
            output = []
            for child in node['children']:
                child_path = os.path.join(target_path, child)
                child_node = self.fs.get(child_path, {})
                if child_node.get('type') == 'dir':
                    output.append(f"{Colors.CYAN}{child}{Colors.RESET}")
                else:
                    output.append(f"{Colors.WHITE}{child}{Colors.RESET}")
            print("  ".join(output))
        else:
            print(f"{Colors.RED}ls: cannot access '{args[0] if args else '.'}': No such file or directory{Colors.RESET}")

    def _cmd_cd(self, args):
        """Changes the current working directory."""
        target_path = args[0] if args else '/home/guest'
        new_path = self._resolve_path(target_path)
        if new_path in self.fs and self.fs[new_path]['type'] == 'dir':
            self.current_path = new_path
        else:
            print(f"{Colors.RED}cd: no such file or directory: {target_path}{Colors.RESET}")
            
    def _cmd_pwd(self, args):
        """Prints the current working directory."""
        print(self.current_path)

    def _cmd_cat(self, args):
        """Prints the content of a file."""
        if not args:
            print(f"{Colors.RED}cat: missing operand{Colors.RESET}")
            return
        target_path = self._resolve_path(args[0])
        node = self.fs.get(target_path)
        if node and node['type'] == 'file':
            print(node['content'])
        elif node and node['type'] == 'dir':
            print(f"{Colors.RED}cat: {args[0]}: Is a directory{Colors.RESET}")
        else:
            print(f"{Colors.RED}cat: {args[0]}: No such file or directory{Colors.RESET}")

    def _cmd_echo(self, args):
        """Prints the provided arguments back to the terminal."""
        print(' '.join(args))

    def _cmd_clear(self, args=None):
        """Clears the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def _cmd_exit(self, args):
        """Exits the terminal emulator."""
        print("Shutting down LOA OS...")
        sys.exit(0)

    # --- Tahkmahnelle File Manager ---

    def _run_tahkmahnelle(self, args=None):
        """Runs the interactive file manager UI."""
        selected_index = 0
        
        while True:
            # 1. Get current directory items
            current_node = self.fs[self.current_path]
            items = []
            if self.current_path != '/':
                items.append({'name': '..', 'type': 'dir'})
            for child_name in current_node['children']:
                child_path = os.path.join(self.current_path, child_name)
                items.append({'name': child_name, 'type': self.fs[child_path]['type']})

            # 2. Render the UI
            self._cmd_clear()
            print(f"{Colors.BOLD}{Colors.YELLOW}tahkmahnelle File Manager{Colors.RESET}")
            print(f"Location: {self.current_path}")
            print("-" * 40)
            for i, item in enumerate(items):
                is_selected = (i == selected_index)
                prefix = "> " if is_selected else "  "
                color = Colors.CYAN if item['type'] == 'dir' else Colors.WHITE
                suffix = "/" if item['type'] == 'dir' else ""
                
                # Apply selection highlight
                if is_selected:
                    print(f"{Colors.BG_CYAN}{Colors.BLACK}{prefix}{item['name']}{suffix}{Colors.RESET}")
                else:
                    print(f"{color}{prefix}{item['name']}{suffix}{Colors.RESET}")
            print("-" * 40)
            print("Use 'w'/'s' or Arrow Keys to navigate. 'Enter' to select. 'q' to quit.")

            # 3. Handle user input
            key = getch()
            
            # Handle multi-byte arrow key sequences from Unix terminals
            if key == '\x1b': # Escape character, likely an arrow key
                if getch() == '[':
                    arrow = getch()
                    if arrow == 'A': key = 'w' # Up Arrow
                    if arrow == 'B': key = 's' # Down Arrow
            
            if key in ('w', 'k'): # Up
                selected_index = max(0, selected_index - 1)
            elif key in ('s', 'j'): # Down
                selected_index = min(len(items) - 1, selected_index + 1)
            elif key in ('q', 'Q'): # Quit
                break
            elif key == '\r' or key == '\n': # Enter
                selected_item = items[selected_index]
                if selected_item['type'] == 'dir':
                    self._cmd_cd([selected_item['name']])
                    selected_index = 0 # Reset selection in new directory
                else: # It's a file, cat it and exit tahkmahnelle
                    self._cmd_clear()
                    print(f"tahkmahnelle> cat {selected_item['name']}")
                    self._cmd_cat([selected_item['name']])
                    input("\nPress Enter to continue...")
                    break
        self._cmd_clear()

    # --- Main Application Loop ---

    def run(self):
        """Starts and runs the main terminal loop."""
        self._cmd_clear()
        print(f"""{Colors.YELLOW}
 LLLLLLLLLLL          OOOOOOOOO          AAAAAAAAA
 L:::::::::L        OO:::::::::OO       A:::::::::A
 L:::::::::L      OO:::::::::::::OO    A::::::::::A
 LL:::::::LL     O:::::::OOO:::::::O  A:::::A A:::::A
   L:::::L       O::::::O   O::::::O A:::::A   A:::::A
   L:::::L       O:::::O     O:::::OA:::::A     A:::::A
   L:::::L       O:::::O     O:::::OA:::::AAAAAAAAA:::::A
   L:::::L       O:::::O     O:::::OA:::::::::::::::::A
   L:::::L       O:::::O     O:::::OA:::::AAAAAAAAA:::::A
   L:::::L       O:::::O     O:::::OA:::::A     A:::::A
   L:::::L       O::::::O   O::::::OA:::::A     A:::::A
 LL:::::::LLLLLL O:::::::OOO:::::::OA:::::A     A:::::A
 L:::::::::::::L  OO:::::::::::::OO A:::::A       A:::::A
 L:::::::::::::L    OO:::::::::OO  A:::::A       A:::::A
 LLLLLLLLLLLLLLL      OOOOOOOOO   AAAAAAA       AAAAAAA
        {Colors.RESET}""")
        print("Welcome to LOA OS. System loaded successfully.")
        print('Type "help" for a list of commands.')

        while True:
            try:
                prompt = self._get_prompt()
                user_input = input(prompt)
                if not user_input:
                    continue
                
                parts = user_input.strip().split()
                command_name = parts[0]
                args = parts[1:]
                
                command = self.commands.get(command_name)
                if command:
                    command(args)
                else:
                    print(f"{Colors.RED}{command_name}: command not found{Colors.RESET}")
            
            except (KeyboardInterrupt, EOFError):
                print("\nShutting down LOA OS...")
                break

if __name__ == "__main__":
    terminal = LoaTerminal()
    terminal.run()


