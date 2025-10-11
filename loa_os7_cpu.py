import json
import os
import subprocess
from typing import Dict, Any, List, Optional
import time
import requests # Required for the fetch-web command simulation
import fnmatch # For wildcard matching in 'find'

# --- Configuration and Persistence ---
APP_NAME = "LoA OS 9ehd (Python)"
VERSION = "7 (Simulated Processes)"
PROMPT_CHAR = "λ"
VFS_SAVE_FILE = "loa_vfs_state.json"
ENV_SAVE_FILE = "loa_env_state.json"
PROC_SAVE_FILE = "loa_proc_state.json" # New file for process persistence

# Gemini API Configuration Placeholder
# The API key is left empty as per the guidelines, relying on the canvas environment.
API_KEY = "" 
GEMINI_MODEL = "gemini-2.5-flash-preview-05-20"
API_URL_TEMPLATE = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={API_KEY}"

# --- Terminal Color Codes (ANSI) ---
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

# --- LoA OS Core Class ---

class LoAOS:
    """
    Core class managing the Virtual File System (VFS), environment variables, 
    and command execution for the simulated OS environment, now including
    simulated process management.
    """
    def __init__(self):
        self.vfs: Dict[str, Any] = {}
        self.env: Dict[str, str] = {}
        self.processes: Dict[int, Dict[str, Any]] = {} # PID -> Process details
        self._next_pid_counter = 100 
        self.current_path: str = "/home/user"
        self.history: List[str] = []
        self.tool_aliases: Dict[str, str] = {
            "sh_git": "git", 
            "cmake-debian": "cmake", 
            "py": "python3"
        }
        self.is_running = True
        
        self._initialize_state()

    # --- Persistence and Initialization ---

    def _load_state(self, filename: str, default_val: Any = None) -> Any:
        """Loads state from a JSON file."""
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    return json.load(f)
            except (IOError, json.JSONDecodeError) as e:
                print(f"{Colors.FAIL}Warning: Could not load {filename}. Error: {e}{Colors.ENDC}")
        return default_val if default_val is not None else {}

    def _save_state(self, data: Any, filename: str):
        """Saves state to a JSON file."""
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"{Colors.FAIL}Error: Could not save {filename}. Error: {e}{Colors.ENDC}")

    def _initialize_state(self):
        """Sets up default VFS, environment, and processes or loads persistence."""
        
        # 1. Load VFS
        loaded_vfs = self._load_state(VFS_SAVE_FILE)
        if loaded_vfs:
            self.vfs = loaded_vfs
            print(f"{Colors.OKGREEN}VFS loaded from {VFS_SAVE_FILE}.{Colors.ENDC}")
        else:
            self.vfs = {
                '/': {'type': 'dir', 'contents': {
                    'home': {'type': 'dir', 'contents': {}},
                    'bin': {'type': 'dir', 'contents': {}},
                    'etc': {'type': 'dir', 'contents': {}}
                }}
            }
            self._get_dir_node('/home')['contents']['user'] = {'type': 'dir', 'contents': {}}
            self._create_vfs_file("/home/user/readme.txt", f"Welcome to {APP_NAME} {VERSION}!")
            self._create_vfs_file("/home/user/long_task.py", "# Simulated long-running script\nimport time\nprint('Starting long task...')\ntime.sleep(60)\nprint('Task complete.')")
            print(f"{Colors.WARNING}Creating new VFS file: {VFS_SAVE_FILE}.{Colors.ENDC}")
        
        # 2. Load ENV
        self.env = self._load_state(ENV_SAVE_FILE)
        if not self.env:
            self.env = {
                "USER": "loa_user",
                "HOME": "/home/user",
                "HOSTNAME": "loa-os-v7",
                "VERSION": VERSION
            }
            print(f"{Colors.WARNING}Creating new ENV file: {ENV_SAVE_FILE}.{Colors.ENDC}")
        
        # 3. Load Processes and PID counter
        loaded_proc = self._load_state(PROC_SAVE_FILE, default_val={'processes': {}, 'next_pid': 100})
        self.processes = {int(k):v for k,v in loaded_proc.get('processes', {}).items()}
        self._next_pid_counter = loaded_proc.get('next_pid', 100)
        
        # 4. Load/Set Current Path
        self.current_path = self.env.get("CURRENT_PATH", "/home/user")
        
    def save_all_state(self):
        """Saves VFS, ENV, and Process state."""
        self.env["CURRENT_PATH"] = self.current_path
        self._save_state(self.vfs, VFS_SAVE_FILE)
        self._save_state(self.env, ENV_SAVE_FILE)
        
        # Save process state
        proc_state = {
            'processes': self.processes,
            'next_pid': self._next_pid_counter
        }
        self._save_state(proc_state, PROC_SAVE_FILE)

    # --- VFS Utilities ---

    def _resolve_path(self, path_str: str) -> str:
        """Converts relative paths to absolute, resolving '..', '.'."""
        if path_str.startswith('/'):
            target_path = path_str
        else:
            target_path = os.path.join(self.current_path, path_str)

        target_path = os.path.normpath(target_path)
        
        if target_path == '.':
            target_path = '/' if self.current_path == '/' else self.current_path
        elif not target_path.startswith('/'):
             target_path = '/' + target_path
             
        return target_path

    def _get_node(self, path: str) -> Optional[Dict[str, Any]]:
        """Traverses the VFS dictionary to find a node."""
        path = self._resolve_path(path).strip('/')
        if path == "":
            return self.vfs.get('/')
        
        current_node = self.vfs.get('/')
        if not current_node: return None

        components = path.split('/')
        
        for comp in components:
            if comp in current_node.get('contents', {}):
                current_node = current_node['contents'][comp]
            else:
                return None
        return current_node

    def _get_dir_node(self, path: str) -> Optional[Dict[str, Any]]:
        """Returns a VFS node if it exists and is a directory."""
        node = self._get_node(path)
        if node and node.get('type') == 'dir':
            return node
        return None

    def _get_parent_and_name(self, path: str) -> Optional[tuple[Dict[str, Any], str]]:
        """Returns the parent directory node and the name of the target item."""
        path = self._resolve_path(path)
        parent_path = os.path.dirname(path)
        name = os.path.basename(path)
        
        if parent_path == '/':
            parent_node = self.vfs.get('/')
        else:
            parent_node = self._get_dir_node(parent_path)
        
        if parent_node and parent_node.get('type') == 'dir' and name:
            return parent_node, name
        return None

    def _create_vfs_file(self, path: str, content: str):
        """Helper to create or overwrite a file."""
        result = self._get_parent_and_name(path)
        if result:
            parent_node, name = result
            parent_node['contents'][name] = {'type': 'file', 'content': content}
            return True
        return False
        
    # --- VFS Commands (Retained from A5) ---

    def cmd_cd(self, args: List[str]):
        """Change directory (cd)."""
        target_path = args[0] if args else self.env.get("HOME", "/home/user")
        resolved_path = self._resolve_path(target_path)
        target_node = self._get_dir_node(resolved_path)

        if target_node:
            self.current_path = resolved_path
            print(f"{Colors.OKGREEN}VFS directory changed to: {Colors.OKBLUE}{self.current_path}{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}Error: VFS directory not found or is a file: {target_path}{Colors.ENDC}")

    def cmd_ls(self, args: List[str]):
        """List directory contents (ls)."""
        path_to_list = self.current_path
        if args:
            path_to_list = self._resolve_path(args[0])

        target_node = self._get_dir_node(path_to_list)

        if target_node:
            print(f"{Colors.UNDERLINE}Contents of VFS {path_to_list}:{Colors.ENDC}")
            contents = target_node.get('contents', {})
            items = sorted(contents.items())
            
            for name, node in items:
                if node.get('type') == 'dir':
                    print(f"{Colors.OKBLUE}{name}/{Colors.ENDC}")
                elif node.get('type') == 'file':
                    print(f"{Colors.OKGREEN}{name}{Colors.ENDC}")
            print(f"{Colors.HEADER}------------------------------------------------------------{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}Error: Cannot list contents. Not a directory or does not exist.{Colors.ENDC}")

    def cmd_mkdir(self, args: List[str]):
        """Make directory (mkdir)."""
        if not args:
            print(f"{Colors.FAIL}Usage: mkdir <directory_name>{Colors.ENDC}")
            return

        dirname = args[0]
        full_path = self._resolve_path(os.path.join(self.current_path, dirname))

        if self._get_node(full_path):
            print(f"{Colors.WARNING}Warning: VFS item '{dirname}' already exists.{Colors.ENDC}")
            return
        
        result = self._get_parent_and_name(full_path)
        if result:
            parent_node, name = result
            parent_node['contents'][name] = {'type': 'dir', 'contents': {}}
            print(f"{Colors.OKGREEN}Directory '{dirname}' created in VFS.{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}Error: Cannot create directory in the parent path.{Colors.ENDC}")
            
    def cmd_rm(self, args: List[str]):
        """Remove file or directory (rm)."""
        if not args:
            print(f"{Colors.FAIL}Usage: rm <filename_or_dirname>{Colors.ENDC}")
            return
        
        target_name = args[0]
        full_path = self._resolve_path(os.path.join(self.current_path, target_name))

        result = self._get_parent_and_name(full_path)
        if not result:
            print(f"{Colors.FAIL}Error: VFS item '{target_name}' not found or is root.{Colors.ENDC}")
            return
        
        parent_node, name = result
        target_node = parent_node['contents'].get(name)

        if not target_node:
            print(f"{Colors.FAIL}Error: VFS item '{target_name}' not found.{Colors.ENDC}")
            return

        if target_node.get('type') == 'dir':
            if target_node['contents']:
                print(f"{Colors.FAIL}Error: Directory '{target_name}' is not empty. Cannot remove.{Colors.ENDC}")
                return
            else:
                del parent_node['contents'][name]
                print(f"{Colors.OKGREEN}VFS directory '{target_name}' removed.{Colors.ENDC}")
        elif target_node.get('type') == 'file':
            del parent_node['contents'][name]
            print(f"{Colors.OKGREEN}VFS file '{target_name}' removed.{Colors.ENDC}")
        else:
             print(f"{Colors.FAIL}Error: Unknown item type for '{target_name}'.{Colors.ENDC}")

    def cmd_cat(self, args: List[str]):
        """Display contents of a VFS file (cat)."""
        if not args:
            print(f"{Colors.FAIL}Usage: cat <filename>{Colors.ENDC}")
            return
        
        filename = args[0]
        full_path = self._resolve_path(os.path.join(self.current_path, filename))
        target_node = self._get_node(full_path)
        
        if not target_node:
            print(f"{Colors.FAIL}Error: VFS item '{filename}' not found.{Colors.ENDC}")
            return
            
        if target_node.get('type') == 'dir':
            print(f"{Colors.FAIL}Error: Cannot 'cat' a directory.{Colors.ENDC}")
            return
        
        print(f"{Colors.OKCYAN}--- VFS File: {filename} ---{Colors.ENDC}")
        print(target_node.get('content', ''))
        print(f"{Colors.OKCYAN}--------------------------{Colors.ENDC}")

    def cmd_edit(self, args: List[str]):
        """Saves a string of text directly into a VFS file."""
        if len(args) < 2:
            print(f"{Colors.FAIL}Usage: edit <filename> <content_string>{Colors.ENDC}")
            print(f"{Colors.WARNING}Note: Use single quotes to encapsulate multi-word content.{Colors.ENDC}")
            return

        filename = args[0]
        content = " ".join(args[1:])
        full_path = self._resolve_path(os.path.join(self.current_path, filename))

        if self._create_vfs_file(full_path, content):
            print(f"{Colors.OKGREEN}VFS file '{filename}' created/updated successfully.{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}Error: Could not edit file at path: {full_path}{Colors.ENDC}")
            
    def _vfs_walk(self, node: Dict[str, Any], current_path: str, pattern: str, results: List[str]):
        """Recursively walks the VFS to find nodes matching a pattern."""
        if 'contents' in node:
            for name, child_node in node['contents'].items():
                full_path = os.path.join(current_path, name)
                
                if fnmatch.fnmatch(name, pattern):
                    if child_node['type'] == 'dir':
                        results.append(f"{Colors.OKBLUE}{full_path}/{Colors.ENDC}")
                    else:
                        results.append(f"{Colors.OKGREEN}{full_path}{Colors.ENDC}")
                
                if child_node['type'] == 'dir':
                    self._vfs_walk(child_node, full_path, pattern, results)


    def cmd_find(self, args: List[str]):
        """Recursively searches the VFS for files/directories matching a name pattern."""
        if not args:
            print(f"{Colors.FAIL}Usage: find <name_pattern> (e.g., find *.py or find user){Colors.ENDC}")
            return
        
        pattern = args[0]
        
        print(f"{Colors.WARNING}Searching VFS for items matching '{pattern}'...{Colors.ENDC}")
        
        results: List[str] = []
        self._vfs_walk(self.vfs.get('/'), "/", pattern, results)
        
        if results:
            for result in sorted(results):
                print(result)
        else:
            print(f"{Colors.WARNING}No VFS items found matching '{pattern}'.{Colors.ENDC}")
        print(f"{Colors.HEADER}------------------------------------------------------------{Colors.ENDC}")


    # --- Process Management Commands (NEW in V7) ---

    def cmd_run_bg(self, args: List[str]):
        """Simulates running a VFS file or command in the background."""
        if not args:
            print(f"{Colors.FAIL}Usage: run-bg <command_and_args>{Colors.ENDC}")
            return

        pid = self._next_pid_counter
        self._next_pid_counter += 1
        
        command_str = " ".join(args)
        
        # Check if the command is an internal command alias for a VFS file (e.g., 'py long_task.py')
        # This is a simulation: the command won't *actually* run, but we track it.
        
        self.processes[pid] = {
            'pid': pid,
            'user': self.env.get('USER', 'loa_user'),
            'command': command_str,
            'status': 'Running',
            'start_time': time.time()
        }
        
        print(f"{Colors.OKGREEN}Process launched in background: PID {pid}{Colors.ENDC}")
        print(f"{Colors.WARNING}Use 'ps' to view and 'kill {pid}' to terminate the simulated process.{Colors.ENDC}")

    def cmd_ps(self, args: List[str]):
        """Lists currently running simulated processes."""
        print(f"{Colors.UNDERLINE}Simulated Process Status:{Colors.ENDC}")
        
        if not self.processes:
            print(f"{Colors.WARNING}No background processes currently running.{Colors.ENDC}")
            print(f"{Colors.HEADER}------------------------------------------------------------{Colors.ENDC}")
            return

        # Header
        print(f"{Colors.BOLD}{'PID':<5} {'USER':<10} {'STATUS':<10} {'RUNTIME':<10} {'COMMAND'}{Colors.ENDC}")
        
        for pid, proc in sorted(self.processes.items()):
            runtime_seconds = int(time.time() - proc['start_time'])
            runtime_str = f"{runtime_seconds // 60:02d}:{runtime_seconds % 60:02d}"
            
            print(
                f"{proc['pid']:<5} "
                f"{proc['user']:<10} "
                f"{Colors.OKGREEN}{proc['status']:<10}{Colors.ENDC} "
                f"{runtime_str:<10} "
                f"{Colors.OKCYAN}{proc['command']}{Colors.ENDC}"
            )
        print(f"{Colors.HEADER}------------------------------------------------------------{Colors.ENDC}")

    def cmd_kill(self, args: List[str]):
        """Terminates a simulated process by PID."""
        if not args:
            print(f"{Colors.FAIL}Usage: kill <PID>{Colors.ENDC}")
            return
            
        try:
            pid_to_kill = int(args[0])
        except ValueError:
            print(f"{Colors.FAIL}Error: PID must be a number.{Colors.ENDC}")
            return
            
        if pid_to_kill in self.processes:
            del self.processes[pid_to_kill]
            print(f"{Colors.OKGREEN}Successfully terminated simulated process with PID {pid_to_kill}.{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}Error: Process with PID {pid_to_kill} not found.{Colors.ENDC}")

    # --- Environment Commands (Retained from A5) ---

    def cmd_setvar(self, args: List[str]):
        """Sets a persistent environment variable (setvar KEY=VALUE)."""
        if not args or "=" not in args[0]:
            print(f"{Colors.FAIL}Usage: setvar KEY=VALUE{Colors.ENDC}")
            return

        key_value = args[0].split('=', 1)
        key = key_value[0].upper()
        value = key_value[1]
        
        self.env[key] = value
        print(f"{Colors.OKGREEN}Set environment variable {key}={value} (will persist){Colors.ENDC}")


    def cmd_env(self, args: List[str]):
        """Lists all persistent VFS-based environment variables."""
        print(f"{Colors.UNDERLINE}LoA OS Environment Variables (VFS):{Colors.ENDC}")
        for key, value in sorted(self.env.items()):
            print(f"{Colors.OKCYAN}{key}={value}{Colors.ENDC}")
        print(f"{Colors.HEADER}------------------------------------------------------------{Colors.ENDC}")

    def cmd_whoami(self, args: List[str]):
        """Displays the current VFS user."""
        print(f"{Colors.OKGREEN}{self.env.get('USER', 'unknown_user')}{Colors.ENDC}")

    def cmd_hostname(self, args: List[str]):
        """Displays the VFS hostname."""
        print(f"{Colors.OKGREEN}{self.env.get('HOSTNAME', 'localhost')}{Colors.ENDC}")
        
    # --- Network/API Command (Retained from A5) ---

    def cmd_fetch_web(self, args: List[str]):
        """Fetches grounded text from the Gemini API (simulated network access)."""
        if not args:
            print(f"{Colors.FAIL}Usage: fetch-web <query for Google Search/Gemini>{Colors.ENDC}")
            return
            
        user_query = " ".join(args)
        
        print(f"{Colors.WARNING}Sending grounded query to LoA Nexus (Gemini API)...{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Query: {user_query}{Colors.ENDC}")
        
        system_prompt = "You are a concise, helpful research assistant in an experimental OS environment. Provide the answer in a single paragraph, and do not use greetings or sign-offs."
        
        payload = {
            "contents": [{"parts": [{"text": user_query}]}],
            "tools": [{"google_search": {} }],
            "systemInstruction": {"parts": [{"text": system_prompt}]}
        }
        
        headers = {'Content-Type': 'application/json'}
        
        try:
            for attempt in range(3):
                time.sleep(2**attempt if attempt > 0 else 0) 
                
                response = requests.post(API_URL_TEMPLATE, headers=headers, json=payload, timeout=20)
                response.raise_for_status()
                
                result = response.json()
                candidate = result.get('candidates', [{}])[0]
                text = candidate.get('content', {}).get('parts', [{}])[0].get('text', 'API response was empty.')
                
                sources = []
                grounding_metadata = candidate.get('groundingMetadata')
                if grounding_metadata and grounding_metadata.get('groundingAttributions'):
                    sources = [
                        f"{s.get('web', {}).get('title')} ({s.get('web', {}).get('uri')})"
                        for s in grounding_metadata['groundingAttributions']
                    ]

                print(f"\n{Colors.OKGREEN}--- Web Search Results ---{Colors.ENDC}")
                print(text)
                
                if sources:
                    print(f"\n{Colors.WARNING}Sources Used:{Colors.ENDC}")
                    for src in sources:
                        print(f"  - {src}")
                print(f"{Colors.OKGREEN}--------------------------{Colors.ENDC}")
                return

            print(f"{Colors.FAIL}Error: API failed after multiple retries. Check connectivity or API key status.{Colors.ENDC}")
            
        except requests.exceptions.RequestException as e:
            print(f"{Colors.FAIL}Network Error: Could not connect to the API endpoint. ({e}){Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}An unexpected error occurred during API processing: {e}{Colors.ENDC}")


    # --- External Tool Execution (Retained from A5) ---

    def _execute_external_tool(self, command: str, args: List[str], tool_name: str, vfs_file: Optional[str] = None):
        """Handles running host system commands."""
        
        full_command = [command] + args
        print(f"{Colors.WARNING}Running external tool ({tool_name}): {' '.join(full_command)}{Colors.ENDC}")
        
        temp_file = None
        if vfs_file:
            full_path = self._resolve_path(os.path.join(self.current_path, vfs_file))
            node = self._get_node(full_path)
            
            if not node or node.get('type') != 'file':
                print(f"{Colors.FAIL}Error: VFS file '{vfs_file}' not found or is not a file.{Colors.ENDC}")
                return
            
            temp_file = f"/tmp/loa_os_exec_{os.getpid()}_{os.path.basename(vfs_file)}"
            with open(temp_file, 'w') as f:
                f.write(node['content'])
            
            try:
                index = full_command.index(vfs_file)
                full_command[index] = temp_file
            except ValueError:
                full_command.append(temp_file)

        try:
            result = subprocess.run(
                full_command, 
                capture_output=True, 
                text=True, 
                check=False
            )
            
            if result.stdout:
                print(f"{Colors.OKCYAN}--- Output ({tool_name}) ---{Colors.ENDC}")
                print(result.stdout.strip())
                print(f"{Colors.OKCYAN}--- End Output ---{Colors.ENDC}")

            if result.stderr:
                print(f"{Colors.FAIL}--- Error ({tool_name}) ---{Colors.ENDC}")
                print(result.stderr.strip())
                print(f"{Colors.FAIL}--- End Error ---{Colors.ENDC}")

            if result.returncode == 0:
                print(f"{Colors.OKGREEN}Command completed successfully.{Colors.ENDC}")
            else:
                 print(f"{Colors.FAIL}Command failed with exit code {result.returncode}.{Colors.ENDC}")

        except FileNotFoundError:
            print(f"{Colors.FAIL}Error: Host command '{command}' not found. Check system PATH.{Colors.ENDC}")
        finally:
            if temp_file and os.path.exists(temp_file):
                os.remove(temp_file)

    def _determine_external_tool(self, command: str, args: List[str]):
        """Routes commands to external tools based on aliases and file extensions."""
        
        file_arg = next((a for a in args if '.' in a and not a.startswith('-')), None)
        
        if file_arg:
            if file_arg.endswith('.py') or command in ["python", "py"]:
                self._execute_external_tool("python3", args, "Python", file_arg)
                return
            elif file_arg.endswith('.c') or command in ["gcc", "g++"]:
                print(f"{Colors.HEADER}--- Copyright LoA Corp. SLPOE_ in c. ---{Colors.ENDC}")
                self._execute_external_tool("gcc", args, "GCC", file_arg)
                return
            elif file_arg.endswith('.js') or command in ["node", "npm"]:
                self._execute_external_tool("node", args, "Node.js", file_arg)
                return
        
        if command in self.tool_aliases:
            host_cmd = self.tool_aliases[command]
            self._execute_external_tool(host_cmd, args, command)
            return

        self._execute_external_tool(command, args, command)


    # --- Command Router and Main Loop ---
    
    def _display_header(self):
        """Clears screen and displays header."""
        os.system('clear || cls') 
        print(f"{Colors.HEADER}============================================================{Colors.ENDC}")
        print(f"{Colors.BOLD}*** {APP_NAME} | VFS & Multi-Environment Shell Emulator ***{Colors.ENDC}")
        print(f"Version {VERSION}. Type '{Colors.OKCYAN}help{Colors.ENDC}' for command list or '{Colors.FAIL}exit{Colors.ENDC}' to quit.")
        print(f"{Colors.WARNING}State is persistent in {VFS_SAVE_FILE}, {ENV_SAVE_FILE}, and {PROC_SAVE_FILE}.{Colors.ENDC}")
        print(f"{Colors.HEADER}============================================================{Colors.ENDC}")
        
    def cmd_help(self, args: List[str]):
        """Displays help information."""
        print(f"{Colors.UNDERLINE}Available Environments & Aliases ({VERSION}):{Colors.ENDC}")
        print(f"  - {Colors.OKGREEN}gcc, py, node, npm{Colors.ENDC}: Execute VFS files with host tools.")
        print(f"  - {Colors.OKGREEN}sh_git, cmake-debian{Colors.ENDC} : Standard tool routing (Aliased).")
        print(f"{Colors.UNDERLINE}Process Management (NEW in V7):{Colors.ENDC}")
        print(f"  - {Colors.OKCYAN}run-bg <cmd>{Colors.ENDC}: Simulate running a command/file in the background.")
        print(f"  - {Colors.OKCYAN}ps{Colors.ENDC}             : List all running simulated background processes.")
        print(f"  - {Colors.OKCYAN}kill <PID>{Colors.ENDC}     : Terminate a simulated background process.")
        print(f"{Colors.UNDERLINE}System Introspection & Network:{Colors.ENDC}")
        print(f"  - {Colors.OKCYAN}whoami, hostname, env{Colors.ENDC}: Display system details and variables.")
        print(f"  - {Colors.OKCYAN}fetch-web <query>{Colors.ENDC}: Grounded web search using Gemini API.")
        print(f"  - {Colors.OKCYAN}setvar KEY=VALUE{Colors.ENDC}: Set persistent VFS environment variables.")
        print(f"{Colors.UNDERLINE}VFS File System Commands (V7):{Colors.ENDC}")
        print(f"  - {Colors.OKCYAN}ls, cd, mkdir, rm, cat, edit, find{Colors.ENDC}: VFS management.")
        print(f"  - {Colors.OKCYAN}history, clear, exit{Colors.ENDC}: Standard shell commands.")
        print(f"{Colors.HEADER}------------------------------------------------------------{Colors.ENDC}")

    def run(self):
        """The main interactive shell loop."""
        self._display_header()
        
        internal_commands = {
            "exit": lambda x: setattr(self, 'is_running', False),
            "clear": lambda x: self._display_header(),
            "history": lambda x: [print(f"{i+1}: {cmd}") for i, cmd in enumerate(self.history)],
            "help": self.cmd_help,
            
            # VFS & Env
            "cd": self.cmd_cd,
            "ls": self.cmd_ls,
            "mkdir": self.cmd_mkdir,
            "rm": self.cmd_rm,
            "cat": self.cmd_cat,
            "edit": self.cmd_edit,
            "find": self.cmd_find,
            "setvar": self.cmd_setvar,
            "env": self.cmd_env,
            "whoami": self.cmd_whoami,
            "hostname": self.cmd_hostname,
            
            # Process Management (NEW)
            "run-bg": self.cmd_run_bg,
            "ps": self.cmd_ps,
            "kill": self.cmd_kill,
            
            # API
            "fetch-web": self.cmd_fetch_web
        }
        
        while self.is_running:
            try:
                prompt = (
                    f"{Colors.OKGREEN}{self.env.get('USER', 'user')}{Colors.ENDC}"
                    f"@{Colors.OKBLUE}{self.current_path}{Colors.ENDC} {PROMPT_CHAR} "
                )
                
                raw_input = input(prompt).strip()
                
                if not raw_input:
                    continue
                
                self.history.append(raw_input)
                
                parts = raw_input.split()
                command = parts[0].lower()
                args = parts[1:]
                
                if command in internal_commands:
                    internal_commands[command](args)
                else:
                    self._determine_external_tool(command, args)

            except EOFError:
                print("\nExiting...")
                self.is_running = False
            except Exception as e:
                print(f"{Colors.FAIL}OS Error: An internal error occurred: {e}{Colors.ENDC}")
        
        # Cleanup
        self.save_all_state()
        print(f"{Colors.WARNING}Exiting {APP_NAME}. State saved. Goodbye!{Colors.ENDC}")

if __name__ == '__main__':
    try:
        loa_os = LoAOS()
        loa_os.run()
    except ImportError as e:
        if 'requests' in str(e):
            print(f"{Colors.FAIL}CRITICAL ERROR: The 'requests' library is required for 'fetch-web'. Please install it: pip install requests{Colors.ENDC}")
        else:
            raise

