#!/bin/bash

# --- Configuration and Globals ---
APP_NAME="LoA OS 9ehd (Shell)"
VERSION="7 (Simulated Processes)"
PROMPT_CHAR="λ"
VFS_SAVE_FILE="loa_vfs_state.json"
ENV_SAVE_FILE="loa_env_state.json"
PROC_SAVE_FILE="loa_proc_state.json"

# Gemini API Configuration
API_KEY="" # Placeholder for API Key
GEMINI_MODEL="gemini-2.5-flash-preview-05-20"
API_URL_BASE="https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent"

# Terminal Color Codes
# Use tput for wider compatibility, falling back to ANSI
C_HEADER=$(tput setaf 5 2>/dev/null || echo '\033[95m')
C_OKBLUE=$(tput setaf 4 2>/dev/null || echo '\033[94m')
C_OKCYAN=$(tput setaf 6 2>/dev/null || echo '\033[96m')
C_OKGREEN=$(tput setaf 2 2>/dev/null || echo '\033[92m')
C_WARNING=$(tput setaf 3 2>/dev/null || echo '\033[93m')
C_FAIL=$(tput setaf 1 2>/dev/null || echo '\033[91m')
C_ENDC=$(tput sgr0 2>/dev/null || echo '\033[0m')
C_BOLD=$(tput bold 2>/dev/null || echo '\033[1m')
C_UNDERLINE=$(tput smul 2>/dev/null || echo '\033[4m')

# External Tools Aliases (executed via 'eval')
declare -A TOOL_ALIASES
TOOL_ALIASES=( 
    ["sh_git"]="git" 
    ["cmake-debian"]="cmake" 
    ["py"]="python3"
    ["python"]="python3"
    ["node"]="node"
    ["gcc"]="gcc"
)

# Current VFS state variables
VFS_PATH="/home/user"
NEXT_PID=100

# --- Core Persistence Functions (Requires jq) ---

# Loads JSON state from a file, initializes if not found
_load_state() {
    local file_path=$1
    local default_content=$2
    if [[ -f "$file_path" ]]; then
        cat "$file_path"
    else
        echo "$default_content"
        echo "$default_content" > "$file_path"
        echo "${C_WARNING}Creating new state file: $file_path.${C_ENDC}" >&2
    fi
}

# Writes JSON data to a file
_save_state() {
    local file_path=$1
    local json_data=$2
    echo "$json_data" > "$file_path"
}

# --- VFS Utility Functions (Complex jq handling) ---

# Converts relative/redundant paths to a clean absolute path
_resolve_path() {
    local path_str=$1
    # If path is relative, prepend current VFS_PATH
    if [[ "$path_str" != /* ]]; then
        path_str="$VFS_PATH/$path_str"
    fi
    
    # Use python to resolve paths robustly (os.path.normpath is reliable)
    # If python is not available, fall back to a simple bash norm
    if command -v python3 &> /dev/null; then
        python3 -c "import os; print(os.path.normpath('$path_str'))"
    else
        # Fallback Bash path normalization (basic)
        local result=""
        local IFS='/'
        read -ra parts <<< "$path_str"
        for part in "${parts[@]}"; do
            if [[ "$part" == "." || "$part" == "" ]]; then
                continue
            elif [[ "$part" == ".." ]]; then
                if [[ "$result" != "" ]]; then
                    result="${result%/*}"
                fi
            else
                result="$result/$part"
            fi
        done
        echo "${result:-/}"
    fi
}

# Converts a POSIX path (/a/b/c) to a jq-friendly path (.contents.a.contents.b.contents.c)
_path_to_jq() {
    local path=$(_resolve_path "$1")
    if [[ "$path" == "/" ]]; then
        echo ""
        return
    fi
    # Strip leading / and replace / with .contents."name"
    path="${path#/}"
    # Replace slashes with .contents. and wrap parts in quotes
    echo ".contents.\"${path//\//\".contents.\""}\""
}

# Reads a VFS node from the VFS state file
_get_node() {
    local path=$1
    local jq_path=$(_path_to_jq "$path")
    
    local vfs_json=$(cat "$VFS_SAVE_FILE")
    local node
    
    if [[ "$path" == "/" ]]; then
        node=$(echo "$vfs_json" | jq -r '.')
    else
        node=$(echo "$vfs_json" | jq -r "$jq_path")
    fi
    
    # jq returns "null" if not found
    if [[ "$node" == "null" ]]; then
        echo ""
    else
        echo "$node"
    fi
}

# --- Initialization and Main Loop ---

loa_init() {
    # 1. Load VFS
    local default_vfs='{
        "/": {"type": "dir", "contents": {
            "home": {"type": "dir", "contents": {
                "user": {"type": "dir", "contents": {}}
            }},
            "bin": {"type": "dir", "contents": {}},
            "etc": {"type": "dir", "contents": {}}
        }}
    }'
    _load_state "$VFS_SAVE_FILE" "$default_vfs" > /dev/null
    
    # 2. Load ENV
    local default_env='{"USER":"loa_user", "HOME":"/home/user", "HOSTNAME":"loa-os-v7", "VERSION":"7"}'
    ENV_JSON=$(_load_state "$ENV_SAVE_FILE" "$default_env")
    VFS_PATH=$(echo "$ENV_JSON" | jq -r '.CURRENT_PATH // "/home/user"')
    
    # 3. Load Processes
    local default_proc='{"processes": {}, "next_pid": 100}'
    PROC_JSON=$(_load_state "$PROC_SAVE_FILE" "$default_proc")
    NEXT_PID=$(echo "$PROC_JSON" | jq -r '.next_pid // 100')
    
    # Create default files if VFS is brand new
    if ! _get_node "/home/user/readme.txt"; then
        cmd_edit "/home/user/readme.txt" "Welcome to LoA OS! Version $VERSION." > /dev/null
        cmd_edit "/home/user/long_task.py" "# Simulated long-running script\nprint('Starting task...')\nimport time; time.sleep(10)\nprint('Task complete.')" > /dev/null
    fi
}

loa_save_state() {
    # 1. Save ENV (update CURRENT_PATH)
    ENV_JSON=$(cat "$ENV_SAVE_FILE" | jq --arg path "$VFS_PATH" '.CURRENT_PATH = $path')
    _save_state "$ENV_SAVE_FILE" "$ENV_JSON"
    
    # 2. Save Processes
    PROC_JSON=$(cat "$PROC_SAVE_FILE" | jq --argjson pid "$NEXT_PID" '.next_pid = $pid')
    _save_state "$PROC_SAVE_FILE" "$PROC_JSON"
    
    # VFS is saved immediately on modification
}

_display_header() {
    clear
    echo "${C_HEADER}============================================================${C_ENDC}"
    echo "${C_BOLD}*** ${APP_NAME} | VFS & Multi-Environment Shell Emulator ***${C_ENDC}"
    echo "Version ${VERSION}. Type '${C_OKCYAN}help${C_ENDC}' for command list or '${C_FAIL}exit${C_ENDC}' to quit."
    echo "${C_WARNING}State is persistent in JSON files (requires jq).${C_ENDC}"
    echo "${C_HEADER}============================================================${C_ENDC}"
}

# --- VFS Command Implementation ---

cmd_edit() {
    local path_str=$1
    local content_str=$2
    
    local full_path=$(_resolve_path "$path_str")
    local name=$(basename "$full_path")
    local parent_path=$(dirname "$full_path")
    local jq_parent_path=$(_path_to_jq "$parent_path")

    # The jq command inserts/updates the file node under the parent's contents
    local vfs_json=$(cat "$VFS_SAVE_FILE")
    local new_vfs_json
    
    # Check if parent exists
    if ! _get_node "$parent_path" | grep -q '"type": "dir"'; then
        echo "${C_FAIL}Error: Parent directory '$parent_path' does not exist.${C_ENDC}"
        return 1
    fi
    
    # Use a single jq operation to set the new file node
    new_vfs_json=$(echo "$vfs_json" | jq --arg name "$name" --arg content "$content_str" \
        "$jq_parent_path.contents.\($name) = {\"type\": \"file\", \"content\": \$content}"
    )

    if [[ "$new_vfs_json" != "$vfs_json" ]]; then
        _save_state "$VFS_SAVE_FILE" "$new_vfs_json"
        echo "${C_OKGREEN}VFS file '$path_str' created/updated successfully.${C_ENDC}"
    else
        echo "${C_FAIL}Error: Could not edit file at path: $path_str.${C_ENDC}"
    fi
}

cmd_cat() {
    local path_str=$1
    if [[ -z "$path_str" ]]; then
        echo "${C_FAIL}Usage: cat <filename>${C_ENDC}"
        return 1
    fi

    local node=$(_get_node "$path_str")
    
    if [[ -z "$node" ]]; then
        echo "${C_FAIL}Error: VFS item '$path_str' not found.${C_ENDC}"
        return 1
    fi
    
    local type=$(echo "$node" | jq -r '.type')
    if [[ "$type" == "dir" ]]; then
        echo "${C_FAIL}Error: Cannot 'cat' a directory.${C_ENDC}"
        return 1
    fi

    local content=$(echo "$node" | jq -r '.content')
    
    echo "${C_OKCYAN}--- VFS File: $path_str ---${C_ENDC}"
    echo "$content"
    echo "${C_OKCYAN}--------------------------${C_ENDC}"
}

cmd_ls() {
    local path_to_list=$(_resolve_path "${1:-$VFS_PATH}")
    local jq_path=$(_path_to_jq "$path_to_list")
    
    local vfs_json=$(cat "$VFS_SAVE_FILE")
    local dir_contents
    
    if [[ "$path_to_list" == "/" ]]; then
        # For root, we look directly at /.contents
        dir_contents=$(echo "$vfs_json" | jq -r '."/"?.contents | keys[]')
    else
        # For sub-directories, we use the generated jq path
        dir_contents=$(echo "$vfs_json" | jq -r "$jq_path.contents | keys[]")
    fi

    if [[ -z "$dir_contents" ]]; then
        echo "${C_WARNING}Directory is empty or path not found: $path_to_list.${C_ENDC}"
        return
    fi
    
    echo "${C_UNDERLINE}Contents of VFS $path_to_list:${C_ENDC}"
    
    # Iterate over items and check their type for coloring
    while IFS= read -r item_name; do
        local item_path="$path_to_list/$item_name"
        local item_node=$(_get_node "$item_path")
        local item_type=$(echo "$item_node" | jq -r '.type')
        
        if [[ "$item_type" == "dir" ]]; then
            echo "${C_OKBLUE}${item_name}/${C_ENDC}"
        elif [[ "$item_type" == "file" ]]; then
            echo "${C_OKGREEN}${item_name}${C_ENDC}"
        fi
    done <<< "$dir_contents" | sort
    
    echo "${C_HEADER}------------------------------------------------------------${C_ENDC}"
}

cmd_cd() {
    local target_path=$1
    if [[ -z "$target_path" ]]; then
        target_path=$(echo "$ENV_JSON" | jq -r '.HOME // "/home/user"')
    fi
    
    local resolved_path=$(_resolve_path "$target_path")
    local node=$(_get_node "$resolved_path")

    if [[ -z "$node" ]]; then
        echo "${C_FAIL}Error: VFS directory not found: $target_path${C_ENDC}"
        return 1
    fi
    
    local type=$(echo "$node" | jq -r '.type')
    if [[ "$type" == "dir" ]]; then
        VFS_PATH="$resolved_path"
        echo "${C_OKGREEN}VFS directory changed to: ${C_OKBLUE}$VFS_PATH${C_ENDC}"
    else
        echo "${C_FAIL}Error: Not a directory: $target_path${C_ENDC}"
        return 1
    fi
}

cmd_mkdir() {
    local dirname=$1
    if [[ -z "$dirname" ]]; then
        echo "${C_FAIL}Usage: mkdir <directory_name>${C_ENDC}"
        return 1
    fi

    local full_path=$(_resolve_path "$dirname")
    local name=$(basename "$full_path")
    local parent_path=$(dirname "$full_path")
    local jq_parent_path=$(_path_to_jq "$parent_path")

    if [[ -n "$(_get_node "$full_path")" ]]; then
        echo "${C_WARNING}Warning: VFS item '$dirname' already exists.${C_ENDC}"
        return
    fi
    
    # Insert new dir node
    local vfs_json=$(cat "$VFS_SAVE_FILE")
    local new_vfs_json
    
    new_vfs_json=$(echo "$vfs_json" | jq --arg name "$name" \
        "$jq_parent_path.contents.\($name) = {\"type\": \"dir\", \"contents\": {}}"
    )

    if [[ "$new_vfs_json" != "$vfs_json" ]]; then
        _save_state "$VFS_SAVE_FILE" "$new_vfs_json"
        echo "${C_OKGREEN}Directory '$dirname' created in VFS.${C_ENDC}"
    else
        echo "${C_FAIL}Error: Cannot create directory in the parent path.${C_ENDC}"
    fi
}

cmd_rm() {
    local target_name=$1
    if [[ -z "$target_name" ]]; then
        echo "${C_FAIL}Usage: rm <filename_or_dirname>${C_ENDC}"
        return 1
    fi
    
    local full_path=$(_resolve_path "$target_name")
    local name=$(basename "$full_path")
    local parent_path=$(dirname "$full_path")
    local jq_parent_path=$(_path_to_jq "$parent_path")
    
    local node=$(_get_node "$full_path")
    if [[ -z "$node" ]]; then
        echo "${C_FAIL}Error: VFS item '$target_name' not found.${C_ENDC}"
        return 1
    fi

    local type=$(echo "$node" | jq -r '.type')
    
    if [[ "$type" == "dir" ]]; then
        local contents=$(echo "$node" | jq '.contents | length')
        if [[ "$contents" -gt 0 ]]; then
            echo "${C_FAIL}Error: Directory '$target_name' is not empty. Cannot remove.${C_ENDC}"
            return 1
        fi
    fi

    # Remove the node using jq
    local vfs_json=$(cat "$VFS_SAVE_FILE")
    local new_vfs_json
    
    new_vfs_json=$(echo "$vfs_json" | jq "del($jq_parent_path.contents.\"$name\")")
    
    if [[ "$new_vfs_json" != "$vfs_json" ]]; then
        _save_state "$VFS_SAVE_FILE" "$new_vfs_json"
        echo "${C_OKGREEN}VFS $type '$target_name' removed.${C_ENDC}"
    else
        echo "${C_FAIL}Error: Could not remove '$target_name'.${C_ENDC}"
    fi
}

cmd_find() {
    local pattern=$1
    if [[ -z "$pattern" ]]; then
        echo "${C_FAIL}Usage: find <name_pattern>${C_ENDC}"
        return 1
    fi
    
    echo "${C_WARNING}Searching VFS for items matching '$pattern' (requires fnmatch in bash)...${C_ENDC}"

    # Use recursive descent in jq to find all items and paths, then grep/fnmatch
    local vfs_json=$(cat "$VFS_SAVE_FILE")
    local paths_and_types
    
    # Generate an array of path and type objects: [{"path": "/home/user/file", "type": "file"}, ...]
    paths_and_types=$(echo "$vfs_json" | jq -r '
        paths as $p | 
        (.[$p[0]] | select(. != null and .type)) as $n | 
        # Check if we are at a "contents" level; if so, skip, otherwise process
        if $p[-1] != "contents" and $n.type then 
            # Construct the POSIX path
            ( $p | map(select(. != "contents")) | join("/") | "/" + . ) as $path |
            # Output the path and type
            "\"type\":\"" + $n.type + "\", \"path\":\"" + $path + "\", \"name\":\"" + $p[-1] + "\"" 
        else 
            empty 
        end
    ' | sed 's/\/[^"]*$//' | sort -u) # Cleanup and deduplicate

    local found_count=0
    
    echo "${paths_and_types}" | while IFS= read -r line; do
        local path=$(echo "$line" | grep -o '"path":"[^"]*"' | cut -d':' -f2 | tr -d '"')
        local name=$(basename "$path")
        local type=$(echo "$line" | grep -o '"type":"[^"]*"' | cut -d':' -f2 | tr -d '"')

        # Use bash globbing/fnmatch simulation
        if [[ "$name" == $pattern ]]; then
            if [[ "$type" == "dir" ]]; then
                echo "${C_OKBLUE}${path}/${C_ENDC}"
            elif [[ "$type" == "file" ]]; then
                echo "${C_OKGREEN}${path}${C_ENDC}"
            fi
            found_count=$((found_count + 1))
        fi
    done
    
    # Note: Cannot reliably get $found_count outside the loop in simple shell pipes.
    # We trust the output speaks for itself.
    
    echo "${C_HEADER}------------------------------------------------------------${C_ENDC}"
}

# --- Process Management Implementation (NEW in V7) ---

cmd_run_bg() {
    if [[ $# -eq 0 ]]; then
        echo "${C_FAIL}Usage: run-bg <command_and_args>${C_ENDC}"
        return 1
    fi

    local command_str="$*"
    local current_time=$(date +%s)
    local user=$(echo "$ENV_JSON" | jq -r '.USER // "loa_user"')

    local proc_json=$(cat "$PROC_SAVE_FILE")
    local new_proc_json

    # Get current process list, append new process, and update NEXT_PID
    new_proc_json=$(echo "$proc_json" | jq \
        --arg cmd "$command_str" \
        --arg time "$current_time" \
        --arg user "$user" \
        --argjson pid "$NEXT_PID" \
        '{
            "next_pid": ($pid + 1),
            "processes": (.processes + { 
                ($pid | tostring): {
                    "pid": $pid, 
                    "user": $user, 
                    "command": $cmd, 
                    "status": "Running", 
                    "start_time": ($time | tonumber)
                }
            })
        }'
    )

    _save_state "$PROC_SAVE_FILE" "$new_proc_json"
    PROC_JSON="$new_proc_json" # Update in-memory cache
    NEXT_PID=$(echo "$PROC_JSON" | jq -r '.next_pid')

    echo "${C_OKGREEN}Process launched in background: PID $((NEXT_PID - 1))${C_ENDC}"
    echo "${C_WARNING}Use 'ps' to view and 'kill $((NEXT_PID - 1))' to terminate the simulated process.${C_ENDC}"
}

cmd_ps() {
    local proc_json=$(cat "$PROC_SAVE_FILE")
    local processes=$(echo "$proc_json" | jq -r '.processes | to_entries | .[] | .value | {pid, user, command, status, start_time}')

    if [[ -z "$processes" ]]; then
        echo "${C_WARNING}No background processes currently running.${C_ENDC}"
        echo "${C_HEADER}------------------------------------------------------------${C_ENDC}"
        return
    fi
    
    echo "${C_UNDERLINE}Simulated Process Status:${C_ENDC}"
    echo "${C_BOLD}PID  USER       STATUS     RUNTIME    COMMAND${C_ENDC}"
    
    local current_time=$(date +%s)
    
    # Iterate over processes using jq and calculate runtime
    echo "$proc_json" | jq -r '.processes | to_entries[] | 
        "\(.value.pid) \(.value.user) \(.value.command) \(.value.start_time) \(.value.status)"' | while read pid user command start_time status; do
        
        local runtime_seconds=$((current_time - start_time))
        local runtime_str=$(printf "%02d:%02d" $((runtime_seconds / 60)) $((runtime_seconds % 60)))
        
        printf "%-5s %-10s %s%-10s%s %-10s %s%s%s\n" \
            "$pid" \
            "$user" \
            "$C_OKGREEN" \
            "$status" \
            "$C_ENDC" \
            "$runtime_str" \
            "$C_OKCYAN" \
            "$command" \
            "$C_ENDC"

    done | sort -n

    echo "${C_HEADER}------------------------------------------------------------${C_ENDC}"
}

cmd_kill() {
    local pid_to_kill=$1
    if [[ -z "$pid_to_kill" || "$pid_to_kill" != [0-9]* ]]; then
        echo "${C_FAIL}Usage: kill <PID>. PID must be a number.${C_ENDC}"
        return 1
    fi

    local proc_json=$(cat "$PROC_SAVE_FILE")
    
    if echo "$proc_json" | jq -e ".processes.\"$pid_to_kill\"" &> /dev/null; then
        local new_proc_json=$(echo "$proc_json" | jq "del(.processes.\"$pid_to_kill\")")
        _save_state "$PROC_SAVE_FILE" "$new_proc_json"
        PROC_JSON="$new_proc_json"
        echo "${C_OKGREEN}Successfully terminated simulated process with PID $pid_to_kill.${C_ENDC}"
    else
        echo "${C_FAIL}Error: Process with PID $pid_to_kill not found.${C_ENDC}"
    fi
}

# --- Environment & Misc Commands ---

cmd_setvar() {
    local arg=$1
    if [[ -z "$arg" || "$arg" != *"="* ]]; then
        echo "${C_FAIL}Usage: setvar KEY=VALUE${C_ENDC}"
        return 1
    fi

    local key=$(echo "$arg" | cut -d'=' -f1 | tr '[:lower:]' '[:upper:]')
    local value=$(echo "$arg" | cut -d'=' -f2-)
    
    local new_env_json=$(cat "$ENV_SAVE_FILE" | jq --arg key "$key" --arg value "$value" '.[$key] = $value')
    _save_state "$ENV_SAVE_FILE" "$new_env_json"
    ENV_JSON="$new_env_json" # Update cache
    echo "${C_OKGREEN}Set environment variable ${key}=${value} (will persist)${C_ENDC}"
}

cmd_env() {
    echo "${C_UNDERLINE}LoA OS Environment Variables (VFS):${C_ENDC}"
    echo "$ENV_JSON" | jq -r 'to_entries | map("\(.key)=\(.value)") | .[]' | sort | while IFS= read -r line; do
        echo "${C_OKCYAN}$line${C_ENDC}"
    done
    echo "${C_HEADER}------------------------------------------------------------${C_ENDC}"
}

cmd_whoami() {
    echo "$ENV_JSON" | jq -r '.USER // "unknown_user"' | echo "${C_OKGREEN}$(cat)${C_ENDC}"
}

cmd_hostname() {
    echo "$ENV_JSON" | jq -r '.HOSTNAME // "localhost"' | echo "${C_OKGREEN}$(cat)${C_ENDC}"
}

cmd_help() {
    echo "${C_UNDERLINE}Available Environments & Aliases ($VERSION):${C_ENDC}"
    echo "  - ${C_OKGREEN}gcc, py, node, sh_git, cmake-debian${C_ENDC}: Execute VFS files with host tools."
    echo "${C_UNDERLINE}Process Management (V7):${C_ENDC}"
    echo "  - ${C_OKCYAN}run-bg <cmd>${C_ENDC}: Simulate running a command/file in the background."
    echo "  - ${C_OKCYAN}ps${C_ENDC}             : List all running simulated background processes."
    echo "  - ${C_OKCYAN}kill <PID>${C_ENDC}     : Terminate a simulated background process."
    echo "${C_UNDERLINE}System Introspection & Network:${C_ENDC}"
    echo "  - ${C_OKCYAN}fetch-web <query>${C_ENDC}: Grounded web search using Gemini API (requires curl)."
    echo "  - ${C_OKCYAN}setvar KEY=VALUE${C_ENDC}: Set persistent VFS environment variables."
    echo "${C_UNDERLINE}VFS File System Commands (
