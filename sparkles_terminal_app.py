#!/usr/bin/env python3
# sparkles_terminal_app.py — SPARKLES DOS Emulator as full-screen terminal app (curses)
# Usage: python3 sparkles_terminal_app.py

import curses, os, sys, time, traceback, shutil, importlib.util
from pathlib import Path
from datetime import datetime
import uuid

# ---------------------------
# Configuration
# ---------------------------
SANDBOX = Path.cwd() / "C_DRIVE"
PLUGINS_DIR = SANDBOX / "PLUGINS"
BOOT_ID = str(uuid.uuid4())[:8]

# Ensure directories
SANDBOX.mkdir(exist_ok=True)
PLUGINS_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------
# APOSX ritual features
# ---------------------------
PHONEME_MAP = {
    "T":"ʈ","KH":"χ","M":"m","N":"n","L":"ɬ","R":"ʁ","A":"ɑ","E":"ɛ","U":"u",
    "Z":"z","TH":"θ","SH":"ʃ","Y":"j","O":"o"
}

PLANETS = {
    "VEYUUN":{"role":"Judicial Core","orbit":"3rd","moons":2},
    "KHARUUN":{"role":"Military Forge","orbit":"5th","moons":0},
    "ZHAELLE":{"role":"Spiritual Nexus","orbit":"1st","moons":3},
    "THARUUN":{"role":"Codex Archive","orbit":"4th","moons":1},
    "ELYUUN":{"role":"Agricultural Sphere","orbit":"2nd","moons":1},
    "SHAQEL":{"role":"Outer Watch","orbit":"6th","moons":4}
}

def phonology(tokens):
    parts = tokens.replace('-', ' ').split()
    return " ".join(PHONEME_MAP.get(p.upper(), f"[{p}]") for p in parts)

def ceremonial_calendar():
    now = datetime.utcnow()
    cycle = (now.year - 3000) % 13
    phase = now.month % 7
    return f"Cycle {cycle}, Phase {phase}, Solar Day {now.day}"

def ritual_clock():
    t = time.localtime()
    return f"Ritual Hour {(t.tm_hour + 3) % 24:02}:{t.tm_min:02}"

def solar(planet):
    p = PLANETS.get(planet.upper())
    if not p:
        return f"Planet {planet} not found."
    return f"{planet.upper()}: {p['role']}, Orbit {p['orbit']}, Moons: {p['moons']}"

def military(unit, fmt="T"):
    if fmt.upper().startswith("C"):
        return (f"[CEREMONIAL MANDATE]\nUnit: {unit}\nRitual Alignment: Phase 3\nGlyph Seal: T-KH-MN-L\n"
                f"Sanctioned by: High Codex Authority")
    return (f"[TACTICAL ORDER]\nUnit: {unit}\nObjective: Secure orbital perimeter\nProtocol: Skyward Doctrine\nSeal: T-KH-MN-L")

# ---------------------------
# DOS-style sandbox helpers
# ---------------------------
def to_sandbox_path(dos_path: str) -> Path:
    p = dos_path.replace("\\", "/")
    if ":" in p:
        _, rest = p.split(":",1)
        p = rest
    if p.startswith("/"):
        p = p[1:]
    return (SANDBOX / p).resolve()

def list_dir(path: Path):
    try:
        items = []
        for entry in sorted(path.iterdir()):
            stat = entry.stat()
            if entry.is_dir():
                items.append(f"{entry.name:<20} <DIR>     {datetime.fromtimestamp(stat.st_mtime).strftime('%m/%d/%Y %I:%M%p')}")
            else:
                items.append(f"{entry.name:<20} {stat.st_size:9d} {datetime.fromtimestamp(stat.st_mtime).strftime('%m/%d/%Y %I:%M%p')}")
        return "\n".join(items)
    except Exception as e:
        return f"Error listing directory: {e}"

# ---------------------------
# Plugin loader
# ---------------------------
loaded_plugins = {}

def load_plugins(register_fn):
    loaded_plugins.clear()
    if not PLUGINS_DIR.exists():
        return
    for fp in sorted(PLUGINS_DIR.glob("*.py")):
        name = fp.stem
        try:
            spec = importlib.util.spec_from_file_location(f"plugs.{name}", fp)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "register") and callable(mod.register):
                mod.register(register_fn)
            loaded_plugins[name] = fp
        except Exception as e:
            # keep going, error will be shown in UI output
            loaded_plugins[name] = f"ERROR: {e}"

# ---------------------------
# Command registry
# ---------------------------
COMMANDS = {}

def register_command(name, fn, help_text=""):
    COMMANDS[name.upper()] = {"fn": fn, "help": help_text}

# Core command implementations
def cmd_help(args):
    lines = []
    for k in sorted(COMMANDS.keys()):
        lines.append(f"{k:<12} - {COMMANDS[k].get('help','')}")
    return "\n".join(lines)

def cmd_dir(args):
    path = SANDBOX if not args else to_sandbox_path(args[0])
    if not path.exists(): return f"File not found: {args[0]}"
    return list_dir(path)

def cmd_cd(args):
    global CUR_DIR
    if not args:
        CUR_DIR = SANDBOX
        return ""
    target = to_sandbox_path(args[0])
    if target.exists() and target.is_dir():
        CUR_DIR = target
        return ""
    return f"Directory not found: {args[0]}"

def cmd_md(args):
    if not args: return "Usage: MD <directory>"
    target = to_sandbox_path(args[0])
    try:
        target.mkdir(parents=True, exist_ok=False)
        return f"Directory created: {target.relative_to(SANDBOX)}"
    except FileExistsError:
        return "Directory already exists."
    except Exception as e:
        return f"Error: {e}"

def cmd_rd(args):
    if not args: return "Usage: RD <directory>"
    target = to_sandbox_path(args[0])
    try:
        target.rmdir()
        return f"Directory removed: {target.relative_to(SANDBOX)}"
    except Exception as e:
        return f"Error: {e}"

def cmd_type(args):
    if not args: return "Usage: TYPE <file>"
    fp = to_sandbox_path(args[0])
    if not fp.exists(): return "File not found."
    try:
        return fp.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"Error: {e}"

def cmd_copy(args):
    if len(args) < 2: return "Usage: COPY <src> <dst>"
    src = to_sandbox_path(args[0]); dst = to_sandbox_path(args[1])
    try:
        if src.is_dir():
            return "COPY does not support directories"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        return f"Copied to {dst.relative_to(SANDBOX)}"
    except Exception as e:
        return f"Error: {e}"

def cmd_del(args):
    if not args: return "Usage: DEL <file>"
    fp = to_sandbox_path(args[0])
    try:
        fp.unlink()
        return f"Deleted {args[0]}"
    except Exception as e:
        return f"Error: {e}"

def cmd_ren(args):
    if len(args) < 2: return "Usage: REN <oldname> <newname>"
    old = to_sandbox_path(args[0]); new = to_sandbox_path(args[1])
    try:
        old.rename(new)
        return f"Renamed to {new.relative_to(SANDBOX)}"
    except Exception as e:
        return f"Error: {e}"

def cmd_cls(args):
    # UI handles screen clearing; return special token
    return "__CLS__"

def cmd_echo(args):
    return " ".join(args)

def cmd_exit(args):
    return "__EXIT__"

# APOSX integrations
def cmd_phon(args): return phonology(" ".join(args)) if args else "Usage: PHON <tokens>"

def cmd_calendar(args): return ceremonial_calendar()

def cmd_clock(args): return ritual_clock()

def cmd_solar(args): 
    if not args: return "Usage: SOLAR <planet>"
    return solar(args[0])

def cmd_military(args):
    if not args: return "Usage: MILITARY <unit> [C]"
    unit = args[0]
    fmt = args[1] if len(args) > 1 else "T"
    return military(unit, fmt)

def cmd_loadplugs(args):
    load_plugins(register_command)
    return f"Loaded plugins: {', '.join(sorted(loaded_plugins.keys())) or 'none'}"

def cmd_plugins(args):
    return "\n".join(sorted(loaded_plugins.keys())) if loaded_plugins else "No plugins"

# Register core commands
register_command("DIR", cmd_dir, "List directory")
register_command("CD", cmd_cd, "Change directory")
register_command("MD", cmd_md, "Make directory")
register_command("RD", cmd_rd, "Remove directory")
register_command("TYPE", cmd_type, "Show file")
register_command("COPY", cmd_copy, "Copy file")
register_command("DEL", cmd_del, "Delete file")
register_command("REN", cmd_ren, "Rename file")
register_command("CLS", cmd_cls, "Clear screen")
register_command("ECHO", cmd_echo, "Echo text")
register_command("EXIT", cmd_exit, "Exit shell")
register_command("HELP", lambda a: cmd_help(a), "Show help")
register_command("PHON", cmd_phon, "Phonology generator")
register_command("CALENDAR", lambda a: cmd_calendar(a), "Ceremonial calendar")
register_command("CLOCK", lambda a: cmd_clock(a), "Ritual clock")
register_command("SOLAR", cmd_solar, "Solar chart")
register_command("MILITARY", cmd_military, "Military doc")
register_command("LOADPLUGS", cmd_loadplugs, "Load plugins from C_DRIVE/PLUGINS")
register_command("PLUGINS", cmd_plugins, "List loaded plugins")

# ---------------------------
# REPL and curses UI
# ---------------------------
CUR_DIR = SANDBOX
HISTORY = []

PROMPTDRV = "C:\\"

def format_prompt():
    rel = "\\" + str(CUR_DIR.relative_to(SANDBOX)).replace("/", "\\")
    if rel == "\\.": rel = "\\"
    return f"{PROMPTDRV}{rel}> "

def parse_command_line(line):
    if not line.strip():
        return None, []
    parts = []
    cur = ""
    inq = False
    for ch in line.strip():
        if ch == '"':
            inq = not inq
            continue
        if ch.isspace() and not inq:
            if cur: parts.append(cur); cur=""
        else:
            cur += ch
    if cur: parts.append(cur)
    cmd = parts[0].upper()
    args = parts[1:]
    return cmd, args

def execute_command(cmd, args):
    entry = COMMANDS.get(cmd)
    if not entry:
        return f"Bad command or file name: {cmd}"
    try:
        return entry["fn"](args)
    except Exception as e:
        return f"Error executing {cmd}: {e}"

def draw_header(stdscr):
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(0, 0, f" SPARKLES DOS Emulator — APOSX Integrated  BootID {BOOT_ID} ".ljust(curses.COLS - 1))
    stdscr.attroff(curses.color_pair(2))

def main_curses(stdscr):
    curses.curs_set(1)
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(3, curses.COLOR_GREEN, -1)

    # initial boot messages
    stdscr.clear()
    draw_header(stdscr)
    stdscr.addstr(2, 2, "Mounting C_DRIVE ...")
    stdscr.refresh()
    time.sleep(0.2)
    stdscr.addstr(3, 2, "Calibrating ritual clock ...")
    stdscr.refresh()
    time.sleep(0.2)
    load_plugins(register_command)
    stdscr.addstr(4, 2, f"Loaded plugins: {', '.join(sorted(loaded_plugins.keys())) or 'none'}")
    stdscr.addstr(6, 0, "-" * (curses.COLS - 1))
    stdscr.refresh()
    time.sleep(0.2)

    # main interactive area
    maxy, maxx = stdscr.getmaxyx()
    output_win = curses.newwin(maxy - 6, maxx, 7, 0)
    output_win.scrollok(True)
    input_win = curses.newwin(1, maxx, maxy - 2, 0)
    input_win.keypad(True)

    prompt = format_prompt()
    input_buf = ""
    cursor = 0

    def append_output(text):
        for line in str(text).splitlines():
            output_win.addstr(line + "\n")
        output_win.refresh()

    append_output("Type HELP for commands. Press Ctrl-C to exit.")

    while True:
        try:
            prompt = format_prompt()
            input_win.clear()
            input_win.addstr(0, 0, prompt, curses.color_pair(1))
            input_win.addstr(0, len(prompt), input_buf)
            input_win.move(0, len(prompt) + cursor)
            input_win.refresh()
            ch = input_win.getch()
            if ch in (curses.KEY_BACKSPACE, 127):
                if cursor > 0:
                    input_buf = input_buf[:cursor-1] + input_buf[cursor:]
                    cursor -= 1
            elif ch in (curses.KEY_DC,):
                if cursor < len(input_buf):
                    input_buf = input_buf[:cursor] + input_buf[cursor+1:]
            elif ch in (curses.KEY_LEFT,):
                if cursor > 0: cursor -= 1
            elif ch in (curses.KEY_RIGHT,):
                if cursor < len(input_buf): cursor += 1
            elif ch in (curses.KEY_END,):
                cursor = len(input_buf)
            elif ch in (curses.KEY_HOME,):
                cursor = 0
            elif ch in (curses.KEY_UP,):
                if HISTORY:
                    input_buf = HISTORY[-1]
                    cursor = len(input_buf)
            elif ch in (curses.KEY_ENTER, 10, 13):
                line = input_buf.strip()
                append_output(prompt + line)
                input_buf = ""
                cursor = 0
                if not line:
                    continue
                HISTORY.append(line)
                cmd, args = parse_command_line(line)
                if not cmd:
                    continue
                res = execute_command(cmd, args)
                if res == "__CLS__":
                    output_win.clear()
                    output_win.refresh()
                elif res == "__EXIT__":
                    append_output("Exiting SPARKLES... Goodbye.")
                    time.sleep(0.2)
                    break
                else:
                    append_output(res)
            elif ch >= 32 and ch < 256:
                input_buf = input_buf[:cursor] + chr(ch) + input_buf[cursor:]
                cursor += 1
            # else ignore control chars
        except KeyboardInterrupt:
            break
        except Exception:
            append_output("Unhandled error:")
            append_output(traceback.format_exc())
            break

# ---------------------------
# Entrypoint
# ---------------------------
def main():
    try:
        curses.wrapper(main_curses)
    except Exception as e:
        print("Fatal error:", e)
        traceback.print_exc()

if __name__ == "__main__":
    main()
