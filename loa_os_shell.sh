#!/bin/sh
#
# LoA OS Command Shell Emulator V6.0.0 (SH Edition)
# Copyright LoA Corp. SLPOE_ in c.
#
# This shell script simulates an advanced operating system with a Virtual File System (VFS),
# environment variables, and external tool routing (python, gcc, node, etc.).
# Note: Complex features like in-memory code blocks (py-exec) and API calls (fetch-web) 
# have been simplified or replaced due to sh language limitations.

# --- Configuration and Environment ---
APP_NAME="LoA OS 9ehd (SH)"
VERSION="6.0.0 (SH/VFS Flat)"
PROMPT_CHAR="λ" 
VFS_SAVE_FILE="loa_vfs_state.txt"

# VFS data structure is flattened: [PATH]:[TYPE]:[CONTENT_BASE64]

# Global variables (must be exported for sub-shells, but managed via text for VFS)
# Using standard SH variables for in-session state
CURRENT_PATH="/home/user"
COMMAND_HISTORY=""
TEMP_FILE_COUNT=0

# Define aliases for the user's requested "virtual" commands
VIRTUAL_COMMANDS="sh_git=git cmake-debian=cmake py=python3"

# --- Terminal Color Codes (POSIX compliant) ---
# Check if TTY supports colors
if test -t 1; then
    HEADER='\033[95m'
    OKBLUE='\033[94m'
    OKCYAN='\033[96m'
    OKGREEN='\033[92m'
    WARNING='\033[93m'
    FAIL='\033[91m'
    ENDC='\033[0m'
    BOLD='\033[1m'
    UNDERLINE='\033[4m'
else
    # No colors if not a TTY
    HEADER="" OKBLUE="" OKCYAN="" OKGREEN="" WARNING="" FAIL="" ENDC="" BOLD="" UNDERLINE=""
fi

# --- VFS Persistence and Utility ---

_loa_base64_encode() {
    # Simple base64 encoding (depends on OS utility)
    echo "$1" | base64 2>/dev/null || echo "$1" | openssl base64
}

_loa_base64_decode() {
    # Simple base64 decoding
    echo "$1" | base64 -d 2>/dev/null || echo "$1" | openssl base64 -d
}

_loa_initialize_vfs() {
    # Initialize default environment variables
    # Note: These are SH variables, not VFS-stored ENV
    USER_VAR="loa_user"
    HOME_VAR="/home/user"

    if [ -f "$VFS_SAVE_FILE" ]; then
        echo "${OKGREEN}VFS loaded from $VFS_SAVE_FILE.${ENDC}"
    else
        echo "${WARNING}Creating new VFS file: $VFS_SAVE_FILE.${ENDC}"
        # Default VFS structure: /home/user, /bin, /etc
        echo "/home/user:dir:" > "$VFS_SAVE_FILE"
        echo "/bin:dir:" >> "$VFS_SAVE_FILE"
        echo "/etc:dir:" >> "$VFS_SAVE_FILE"
        
        # Add a default file (base64 encoded content)
        _loa_base64_encode "Welcome to LoA OS V6.0.0 (SH)! Use help for commands." > /tmp/loa_vfs_temp_content
        CONTENT=$(_loa_base64_encode "Welcome to LoA OS V6.0.0 (SH)! Use help for commands.")
        echo "/home/user/readme.txt:file:$CONTENT" >> "$VFS_SAVE_FILE"
        
        # Initialize default VFS-based environment variables
        echo "USER=$USER_VAR" >> "$VFS_SAVE_FILE"
        echo "HOME=$HOME_VAR" >> "$VFS_SAVE_FILE"
        echo "VERSION=$VERSION" >> "$VFS_SAVE_FILE"
    fi
}

_loa_get_vfs_item() {
    # Finds a line in the VFS file matching the path. 
    # Output: Full line (path:type:content_base64) or empty if not found.
    # $1: Full path to check (e.g., /home/user/file.txt)
    grep -E "^$1:|^$1=" "$VFS_SAVE_FILE" | head -n 1
}

_loa_update_vfs_item() {
    # Replaces or adds a line in the VFS file.
    # $1: Full path or variable name
    # $2: New line content (path:type:content_base64 or VAR=VALUE)
    
    # Use awk to find and replace the line, or append if not found
    # This AWK command is the most complex part, handling VFS file updates.
    awk -v path="$1" -v newline="$2" '
        BEGIN { found = 0 }
        # Check if the line starts with the path followed by : or =
        { 
            if ( $0 ~ ("^" path ":") || $0 ~ ("^" path "=") ) {
                print newline
                found = 1
            } else {
                print $0
            }
        } 
        END { 
            if (found == 0) {
                print newline
            } 
        }
    ' "$VFS_SAVE_FILE" > "$VFS_SAVE_FILE.tmp"
    mv "$VFS_SAVE_FILE.tmp" "$VFS_SAVE_FILE"
}

_loa_remove_vfs_item() {
    # Removes a line from the VFS file.
    # $1: Full path or variable name
    
    # Use grep to exclude the line
    grep -v -E "^$1:|^$1=" "$VFS_SAVE_FILE" > "$VFS_SAVE_FILE.tmp"
    mv "$VFS_SAVE_FILE.tmp" "$VFS_SAVE_FILE"
}

_loa_is_dir_empty() {
    # Checks if a VFS directory contains any items other than itself.
    # $1: Full path to directory (e.g., /home/user)
    # Output: 0 (empty), 1 (not empty)
    
    # Grep for any line that starts with the path followed by another path segment or VAR=
    if grep -E "^$1/[^:]+|^$1=" "$VFS_SAVE_FILE" >/dev/null; then
        return 1 # Not empty
    else
        return 0 # Empty
    fi
}

# --- Display and Utility ---

_loa_display_header() {
    # Clear screen and display header
    clear
    echo "${HEADER}============================================================${ENDC}"
    echo "${BOLD}*** $APP_NAME | VFS & Multi-Environment Shell Emulator ***${ENDC}"
    echo "Version $VERSION. Type '${OKCYAN}help${ENDC}' for command list or '${FAIL}exit${ENDC}' to quit."
    echo "${WARNING}VFS State is persistent in '$VFS_SAVE_FILE'.${ENDC}"
    echo "${HEADER}============================================================${ENDC}"
}

_loa_get_current_prompt() {
    # Generates the dynamic shell prompt (username@current_path λ)
    _loa_get_env_var USER_VAR
    _loa_get_env_var HOME_VAR # Not strictly needed but for safety
    
    echo "${OKGREEN}${USER_VAR:-user}${ENDC}@${OKBLUE}${CURRENT_PATH}${ENDC} ${PROMPT_CHAR} "
}

_loa_normalize_path() {
    # Normalizes a path string (e.g., '..' or '/etc')
    # $1: Path string
    # Output: Normalized path
    
    local path="$1"
    local normalized=""
    local current_segments=""
    
    if [ "${path}" = "." ]; then
        echo "$CURRENT_PATH"
        return
    elif [ "${path}" = ".." ]; then
        path="$(dirname "$CURRENT_PATH")"
    fi

    # Handle absolute path
    if echo "$path" | grep -E '^/' >/dev/null; then
        current_segments="/$(echo "$path" | sed 's|^/||')"
    else
        # Handle relative path
        current_segments="${CURRENT_PATH}/$path"
    fi
    
    # Use 'cd' logic in a subshell to resolve '..', '.', etc. 
    # Temporarily change directory to resolve relative paths against the host, then revert.
    # This is a hack to get path resolution without complex shell math.
    normalized=$(
        (
            cd /
            if [ -d "$current_segments" ]; then
                cd "$current_segments" 2>/dev/null
            elif [ -d "$CURRENT_PATH/$path" ]; then
                cd "$CURRENT_PATH/$path" 2>/dev/null
            fi
            # Now extract the path relative to the root '/'
            pwd -P
        ) 2>/dev/null
    )
    
    # Strip any potential leading slash if we're not at root, then re-add
    if [ -z "$normalized" ] || [ "$normalized" = "/" ]; then
        echo "/"
    else
        echo "$normalized"
    fi
}

# --- Environment Variable Functions (VFS based) ---

_loa_get_env_var() {
    # Retrieves an environment variable from the VFS state.
    # $1: Variable name (e.g., USER_VAR)
    # Sets the SH variable $1 to the value
    local line=$(_loa_get_vfs_item "$1")
    
    if [ -n "$line" ]; then
        # Extract value after the '='
        eval "$1=\"$(echo "$line" | cut -d'=' -f2-)\""
    else
        # Default to empty if not found
        eval "$1=\"\""
    fi
}

_loa_set_env_var() {
    # Sets an environment variable in the VFS state.
    # $1: Key, $2: Value
    _loa_update_vfs_item "$1" "$1=$2"
    _loa_get_env_var "$1" # Update the in-memory SH variable as well
}

# --- VFS Internal Commands ---

_loa_internal_cd() {
    # Changes the current working directory in the VFS.
    local path_str="${1:-$HOME_VAR}" # Default to HOME_VAR if no argument
    local new_path_raw=""
    local target_item=""
    
    # Resolve path using the internal "normalize" hack
    if [ "$path_str" = "/" ]; then
        new_path_raw="/"
    else
        new_path_raw=$(_loa_normalize_path "$path_str")
    fi
    
    # Check if the resolved path exists and is a directory
    target_item=$(_loa_get_vfs_item "$new_path_raw")

    # Check if target is not empty AND is a directory (line ends in :dir:)
    if [ -n "$target_item" ] && echo "$target_item" | grep -E ":dir:$" >/dev/null; then
        CURRENT_PATH="$new_path_raw"
        echo "${OKGREEN}VFS directory changed to: ${OKBLUE}${CURRENT_PATH}${ENDC}"
    elif [ -z "$target_item" ] && [ "$new_path_raw" = "/" ]; then
        # Allow root if it's not defined (it's implicit)
        CURRENT_PATH="/"
        echo "${OKGREEN}VFS directory changed to: ${OKBLUE}${CURRENT_PATH}${ENDC}"
    else
        echo "${FAIL}Error: VFS directory not found or is a file: $path_str${ENDC}"
    fi
}

_loa_internal_ls() {
    # Lists the contents of the current VFS directory.
    local current_path_prefix="${CURRENT_PATH}/"
    if [ "$CURRENT_PATH" = "/" ]; then
        current_path_prefix="/"
    fi

    echo "${UNDERLINE}Contents of VFS $CURRENT_PATH:${ENDC}"
    
    # Iterate through VFS entries
    local item=""
    local display_item=""
    
    # Use AWK to filter and extract unique entries under the current path
    awk -v prefix="$current_path_prefix" '
        BEGIN { split("", seen) }
        # Check if line starts with the current directory prefix
        $0 ~ ("^" prefix "[^:]+") {
            # Extract the item name (between the prefix and the next slash or colon)
            # This is complex string slicing based on the prefix length
            item = substr($0, length(prefix) + 1)
            
            # Find the position of the next separator (: or /)
            # If item contains a '/', it is a subdirectory entry, so only print the first part
            sep_pos_slash = index(item, "/")
            sep_pos_colon = index(item, ":")
            
            if (sep_pos_slash > 0 && (sep_pos_slash < sep_pos_colon || sep_pos_colon == 0)) {
                item = substr(item, 1, sep_pos_slash - 1)
                type = "dir"
            } else {
                item = substr(item, 1, sep_pos_colon - 1)
                type = "file" # or dir, we assume file if no slash, or rely on VFS line
            }
            
            if (item != "" && !(item in seen)) {
                seen[item] = 1
                # Check VFS line again to determine if it is explicitly a file or directory
                if ($0 ~ (":" item ":dir:$")) {
                    print item "/"
                } else if (type == "dir") {
                    print item "/"
                } else {
                    print item
                }
            }
        }
    ' "$VFS_SAVE_FILE" | sort | while read -r item; do
        if echo "$item" | grep -E '/$' >/dev/null; then
            # Directory
            echo "${OKBLUE}$item${ENDC}"
        else
            # File
            echo "${OKGREEN}$item${ENDC}"
        fi
    done
    
    echo "${HEADER}------------------------------------------------------------${ENDC}"
}

_loa_internal_mkdir() {
    # Creates a directory in the VFS.
    if [ -z "$1" ]; then
        echo "${FAIL}Usage: mkdir <directory_name>${ENDC}"
        return
    fi

    local dirname="$1"
    local full_path="${CURRENT_PATH}/$dirname"
    
    # Check if item already exists
    if [ -n "$(_loa_get_vfs_item "$full_path")" ]; then
        echo "${WARNING}Warning: VFS item '$dirname' already exists.${ENDC}"
        return
    fi
    
    # Add new directory entry
    _loa_update_vfs_item "$full_path" "$full_path:dir:"
    echo "${OKGREEN}Directory '$dirname' created in VFS.${ENDC}"
}

_loa_internal_rm() {
    # Removes a file or empty directory from the VFS.
    if [ -z "$1" ]; then
        echo "${FAIL}Usage: rm <filename_or_dirname>${ENDC}"
        return
    fi
    
    local target_name="$1"
    local full_path="${CURRENT_PATH}/$target_name"
    local target_item=$(_loa_get_vfs_item "$full_path")

    if [ -z "$target_item" ]; then
        echo "${FAIL}Error: VFS item '$target_name' not found.${ENDC}"
        return
    fi

    # Check if directory is not empty before removal
    if echo "$target_item" | grep -E ":dir:$" >/dev/null; then
        if _loa_is_dir_empty "$full_path"; then
            _loa_remove_vfs_item "$full_path"
            echo "${OKGREEN}VFS directory '$target_name' removed.${ENDC}"
        else
            echo "${FAIL}Error: Directory '$target_name' is not empty. Cannot remove.${ENDC}"
        fi
    else
        # Remove file entry
        _loa_remove_vfs_item "$full_path"
        echo "${OKGREEN}VFS file '$target_name' removed.${ENDC}"
    fi
}

_loa_internal_edit() {
    # Simple, temp file-based text editor for VFS files.
    if [ -z "$1" ]; then
        echo "${FAIL}Error: 'edit' requires a VFS filename. Usage: edit <filename>${ENDC}"
        return
    fi
    
    local filename="$1"
    local full_path="${CURRENT_PATH}/$filename"
    local target_item=$(_loa_get_vfs_item "$full_path")
    local content=""
    
    # Use a temporary file on the host for editing
    local temp_edit_file="/tmp/loa_os_edit_$$_$filename.tmp"
    
    if [ -n "$target_item" ]; then
        if echo "$target_item" | grep -E ":dir:$" >/dev/null; then
            echo "${FAIL}Error: Cannot edit a directory.${ENDC}"
            return
        fi
        
        # Load existing content from VFS entry (third field, base64 decoded)
        content=$(echo "$target_item" | cut -d':' -f3- | _loa_base64_decode)
        echo "$content" > "$temp_edit_file"
        echo "${WARNING}Loading existing VFS file: ${OKBLUE}${filename}${ENDC}"
    else
        # New file
        touch "$temp_edit_file"
        echo "${WARNING}Creating new VFS file: ${OKBLUE}${filename}${ENDC}"
    fi

    echo "${HEADER}*** LoA Editor ($filename) ***${ENDC}"
    echo "Using host 'nano' or 'vi'. Save and close the file to import changes to VFS."
    echo "${HEADER}----------------------------------${ENDC}"

    # Use a common host editor (vi is most universally available in POSIX, but nano is friendlier)
    # Fall back to vi if nano isn't found
    if command -v nano >/dev/null; then
        nano "$temp_edit_file"
    elif command -v vi >/dev/null; then
        vi "$temp_edit_file"
    else
        echo "${FAIL}Error: Neither nano nor vi found. Cannot edit file.${ENDC}"
        rm -f "$temp_edit_file"
        return
    fi
    
    # Read edited content and base64 encode it for VFS storage
    NEW_CONTENT=$(_loa_base64_encode "$(cat "$temp_edit_file")")
    
    # Update VFS entry
    _loa_update_vfs_item "$full_path" "$full_path:file:$NEW_CONTENT"
    
    echo "${OKGREEN}VFS file '$filename' saved successfully from host temp file.${ENDC}"
    rm -f "$temp_edit_file"
}

# --- Environment Variable Commands ---

_loa_internal_setvar() {
    # Sets an environment variable (key=value) in the VFS state.
    if [ -z "$1" ] || echo "$1" | grep -v -E '=' >/dev/null; then
        echo "${FAIL}Usage: setvar KEY=VALUE${ENDC}"
        return
    fi

    local key=$(echo "$1" | cut -d'=' -f1 | tr '[:lower:]' '[:upper:]')
    local value=$(echo "$1" | cut -d'=' -f2-)
    
    _loa_set_env_var "$key" "$value"
    echo "${OKGREEN}Set environment variable $key=$value${ENDC}"
}

_loa_internal_env() {
    # Lists all VFS-based environment variables.
    echo "${UNDERLINE}LoA OS Environment Variables (VFS):${ENDC}"
    # Filter lines that are environment variables (contain '=')
    grep -E '=' "$VFS_SAVE_FILE" | sort | while read -r line; do
        echo "${OKCYAN}$line${ENDC}"
    done
    echo "${HEADER}------------------------------------------------------------${ENDC}"
}

# --- Networking Simulation ---

_loa_internal_ping_sim() {
    # Replaces fetch-web with a networking simulation command.
    echo "${OKCYAN}Pinging LoA Corp. Mainframe (Simulated Network Latency)...${ENDC}"
    local delay=2
    sleep "$delay"
    
    echo "${OKGREEN}PING_SIM $1 (LoA_Corp_Network) 56(84) bytes of data.${ENDC}"
    
    # Random response simulation
    local response_time=$(($RANDOM % 50 + 10))
    echo "64 bytes from 10.0.0.1: icmp_seq=1 ttl=64 time=${response_time}.${RANDOM} ms"
    
    response_time=$(($RANDOM % 50 + 10))
    echo "64 bytes from 10.0.0.1: icmp_seq=2 ttl=64 time=${response_time}.${RANDOM} ms"
    
    response_time=$(($RANDOM % 50 + 10))
    echo "64 bytes from 10.0.0.1: icmp_seq=3 ttl=64 time=${response_time}.${RANDOM} ms"
    
    echo "${WARNING}--- $1 ping statistics ---${ENDC}"
    echo "3 packets transmitted, 3 received, 0% packet loss, time 2000ms"
}

# --- External Tool Executors ---

_loa_execute_external_command() {
    # Executes a command via the host system's shell.
    # $1: Full command string
    # $2: Command name for display
    local full_command_str="$1"
    local command_name="$2"
    
    echo "${WARNING}Running command in host shell: '$full_command_str'${ENDC}"

    # Use a temp file for output capture since sh piping is simpler
    local output_file="/tmp/loa_os_stdout_$$"
    local error_file="/tmp/loa_os_stderr_$$"
    
    # Execute the command, capture output/error, and get return code
    eval "$full_command_str" > "$output_file" 2> "$error_file"
    local return_code=$?

    if [ -s "$output_file" ]; then
        echo "${OKCYAN}--- Output ($command_name) ---${ENDC}"
        cat "$output_file"
        echo "${OKCYAN}--- End Output ---${ENDC}"
    fi

    if [ -s "$error_file" ] && [ "$return_code" -ne 0 ]; then
        echo "${FAIL}--- Error ($command_name) ---${ENDC}"
        cat "$error_file"
        echo "${FAIL}--- End Error ---${ENDC}"
    fi
    
    if [ "$return_code" -eq 0 ]; then
         echo "${OKGREEN}Command completed successfully.${ENDC}"
    fi
    
    rm -f "$output_file" "$error_file"
}

_loa_execute_tool_with_vfs_file() {
    # Writes VFS file content to a temp file, runs the command, and cleans up.
    # $1: Full command list (space separated, including the filename placeholder)
    # $2: Command name
    # $3: VFS filename
    
    local full_command_list="$1"
    local command_name="$2"
    local filename="$3"
    local full_path="${CURRENT_PATH}/$filename"
    local target_item=$(_loa_get_vfs_item "$full_path")

    if [ -z "$target_item" ] || echo "$target_item" | grep -E ":dir:$" >/dev/null; then
        echo "${FAIL}Error: VFS file '$filename' not found or is a directory.${ENDC}"
        return
    fi
        
    local file_content=$(echo "$target_item" | cut -d':' -f3- | _loa_base64_decode)
    
    local temp_exec_file="/tmp/loa_os_exec_$$_$filename"
    echo "$file_content" > "$temp_exec_file"
    
    # Replace the VFS filename with the temporary host path in the command
    local exec_command=$(echo "$full_command_list" | sed "s/$filename/$temp_exec_file/g")

    _loa_execute_external_command "$exec_command" "$command_name"
    
    rm -f "$temp_exec_file"
}

_loa_execute_exe() {
    # Simulates execution of a compiled program (expects a.out in host CWD).
    local target_name="${1:-a.out}"
    echo "${WARNING}Attempting to execute VFS program '$target_name' (Host CWD)...${ENDC}"
    _loa_execute_external_command "./$target_name" "EXE"
}

# --- Command Routing ---

_loa_handle_internal_command() {
    # $1: command, $2...: args
    local command="$1"
    shift
    local args="$@"

    case "$command" in
        exit)
            echo "${WARNING}Exiting $APP_NAME. Goodbye!${ENDC}"
            exit 0
            ;;
        cd)
            _loa_internal_cd "$1"
            ;;
        ls)
            _loa_internal_ls
            ;;
        mkdir)
            _loa_internal_mkdir "$1"
            ;;
        rm)
            _loa_internal_rm "$1"
            ;;
        edit)
            _loa_internal_edit "$1"
            ;;
        exe)
            _loa_execute_exe "$1"
            ;;
        setvar)
            _loa_internal_setvar "$1"
            ;;
        env)
            _loa_internal_env
            ;;
        ping-sim)
            _loa_internal_ping_sim "$1"
            ;;
        clear)
            _loa_display_header
            ;;
        history)
            echo "${UNDERLINE}Command History:${ENDC}"
            echo "$COMMAND_HISTORY" | awk '{print NR ": " $0}'
            echo "${HEADER}------------------------------------------------------------${ENDC}"
            ;;
        help)
            echo "${UNDERLINE}Available Environments & Aliases (V6.0.0 SH):${ENDC}"
            echo "  - ${OKGREEN}gcc, exe${ENDC}       : C/C++ Compile/Execute (prints LoA Copyright)."
            echo "  - ${OKGREEN}py, node, npm${ENDC}: Python/Node.js/NPM (VFS file content is used)."
            echo "  - ${OKGREEN}sh_git, cmake-debian${ENDC} : Standard tool routing."
            echo "${UNDERLINE}Advanced System Features:${ENDC}"
            echo "  - ${OKCYAN}ping-sim <host>${ENDC}: Network simulation (replaces fetch-web)."
            echo "  - ${OKCYAN}setvar KEY=VALUE${ENDC}: Set persistent VFS environment variables."
            echo "  - ${OKCYAN}env${ENDC}            : List all environment variables."
            echo "${UNDERLINE}VFS File System Commands:${ENDC}"
            echo "  - ${OKCYAN}ls, cd, mkdir, rm, edit{ENDC}: VFS directory and file management."
            echo "${HEADER}------------------------------------------------------------${ENDC}"
            ;;
        *)
            # Not an internal command, return 1 to signal external routing
            return 1
            ;;
    esac
    return 0
}

_loa_determine_and_execute_command() {
    local raw_input="$1"
    
    # 1. Resolve environment variables (simple substitution)
    local resolved_input=$(echo "$raw_input" | sed "s/\$USER_VAR/$USER_VAR/g")
    
    # Split command and arguments
    local command=$(echo "$resolved_input" | awk '{print tolower($1)}')
    local args=$(echo "$resolved_input" | cut -d' ' -f2-)

    # 2. Internal Command Check
    if _loa_handle_internal_command "$command" "$args"; then
        return
    fi
    
    # 3. External Command Determination (VFS file-based or direct external)
    
    local file_arg=$(echo "$args" | awk '/\.(c|py|js)$/{print $1; exit}')
    local full_command_list="$resolved_input"
    local command_name=""

    # C Compilation Routing (includes Copyright requirement)
    if [ "$command" = 'gcc' ] || [ -n "$file_arg" ] && [ "$(echo "$file_arg" | grep '\.c$')" ]; then
        echo "${HEADER}--- Copyright LoA Corp. SLPOE_ in c. ---${ENDC}"
        command_name="GCC"
        
        if [ -n "$file_arg" ]; then
            _loa_execute_tool_with_vfs_file "$full_command_list" "$command_name" "$file_arg"
        else
            _loa_execute_external_command "$full_command_list" "$command_name"
        fi
        return
    fi

    # Python/Node Routing
    if [ -n "$file_arg" ]; then
        if [ "$(echo "$file_arg" | grep '\.py$')" ] || [ "$command" = 'python' ] || [ "$command" = 'py' ]; then
            _loa_execute_tool_with_vfs_file "$full_command_list" "Python" "$file_arg"
        elif [ "$(echo "$file_arg" | grep '\.js$')" ] || [ "$command" = 'node' ] || [ "$command" = 'npm' ]; then
            _loa_execute_tool_with_vfs_file "$full_command_list" "Node.js" "$file_arg"
        fi
        return
    fi
    
    # Virtual command aliases routing (sh_git, cmake-debian, npm)
    local virtual_cmd=$(echo "$VIRTUAL_COMMANDS" | grep -w "$command" | cut -d'=' -f2)
    if [ -n "$virtual_cmd" ]; then
        _loa_execute_external_command "$virtual_cmd $args" "$command"
        return
    fi
    
    # Default: Treat as a standard system command 
    _loa_execute_external_command "$full_command_list" "$command"
}

# --- Main Shell Loop ---

_loa_run_shell() {
    _loa_initialize_vfs
    _loa_display_header

    # Load environment variables into SH session variables
    _loa_get_env_var USER_VAR

    while true; do
        printf "%s" "$(_loa_get_current_prompt)"
        
        # Read user input (requires sh/bash compatibility for 'read -r')
        if ! read -r raw_input; then
            echo # Handle EOF (Ctrl+D)
            _loa_handle_internal_command "exit"
        fi

        raw_input=$(echo "$raw_input" | sed 's/^[ \t]*//;s/[ \t]*$//') # Trim whitespace
        
        if [ -z "$raw_input" ]; then
            continue
        fi
        
        # Simple history logging (memory only)
        COMMAND_HISTORY="${COMMAND_HISTORY}\n$raw_input"

        _loa_determine_and_execute_command "$raw_input"
    done
}

# Execute the shell
_loa_run_shell

# End of script

