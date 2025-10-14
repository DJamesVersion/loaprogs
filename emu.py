#!/usr/bin/env python3
# APOSX Virtual Computer with LoA Corporation splash and boot ritual

import os
import sys
import time
import shutil
from pathlib import Path
from datetime import datetime

# --------------------------
# UI helpers
# --------------------------

def clear():
    print("\033[2J\033[H", end="")

def center(text, width=None):
    width = width or shutil.get_terminal_size((80, 24)).columns
    pad = max(0, (width - len(text)) // 2)
    return " " * pad + text

def slow_print(lines, delay=0.03):
    for ln in lines:
        print(ln)
        time.sleep(delay)

def animate_line(text, duration=1.5, frames=12):
    width = shutil.get_terminal_size((80, 24)).columns
    for i in range(frames):
        clear()
        dots = "." * (i % 4)
        print(center(text + dots, width))
        time.sleep(duration / frames)

# --------------------------
# LoA branding (ASCII art)
# --------------------------

LOA_LOGO = r"""
      ▗▄▄▄▄▖
  ▗▄▄████████▄▄▖
 ▟█████▙▟▙▟██████▙
▐██▛  ▜██  ██▛  ▜██▌
▐██     ▐██▌     ██▌
 ▜██▄  ▗███▙  ▄██▛
   ▜████████████▛
      ▝▀████▀▘
"""

APOSX_WORDMARK = r"""
   █████  ██████  ██████  ███████ ██   ██
  ██   ██ ██   ██ ██   ██ ██      ██   ██
  ███████ ██████  ██████  █████   ███████
  ██   ██ ██      ██      ██           ██
  ██   ██ ██      ██      ███████      ██
"""

def draw_splash():
    clear()
    width = shutil.get_terminal_size((80, 24)).columns
    lines = []
    lines.append(center("LoA Corporation", width))
    lines.append(center("Ceremonial Boot Overlay v7.1", width))
    lines.append("")
    for ln in LOA_LOGO.splitlines():
        lines.append(center(ln, width))
    lines.append("")
    for ln in APOSX_WORDMARK.splitlines():
        lines.append(center(ln, width))
    lines.append("")
    lines.append(center("APOSX • Ascension Protocol OS eXperimental", width))
    lines.append(center("Initializing glyph lattice · syncing doctrine caches · calibrating ritual clocks", width))
    slow_print(lines, delay=0.02)
    animate_line("Booting APOSX", duration=1.8, frames=24)

# --------------------------
# BIOS / POST simulation
# --------------------------

def bios_post():
    clear()
    width = shutil.get_terminal_size((80, 24)).columns
    slow_print([
        center("LoA Corp. Phoenix-BIOS v3.9", width),
        center("Copyright (C) LoA Corporation", width),
        "",
        "Memory test: 65536 KB OK",
        "Glyph co-processor: Detected (v2.4)",
        "Ceremony clock: Synchronized (UTC+0 / T-Solar 13:7)",
        "Doctrine vault: Integrity VERIFIED",
        "PCIe Lattice: 4 lanes active",
        "NVMe Codex: Online",
        "",
        "Press F2 for Ritual Settings, F12 for Boot Menu",
    ], delay=0.02)
    time.sleep(0.6)
    slow_print(["Selecting Boot Device: NVMe Codex [LoA-APOSX]"], delay=0.04)
    time.sleep(0.4)

# --------------------------
# Filesystem sandbox
# --------------------------

class Sandbox:
    def __init__(self, root=None):
        self.root = Path(root).resolve() if root else None
        self.cwd = Path.cwd()

    def abspath(self, path):
        p = Path(path)
        if not p.is_absolute():
            p = self.cwd / p
        return p.resolve()

    def ls(self, detailed=False):
        try:
            entries = list(self.cwd.iterdir())
        except Exception as e:
            return f"Error: {e}"
        lines = []
        for e in entries:
            if detailed:
                stat = e.stat()
                dt = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                size = stat.st_size
                kind = "<DIR>" if e.is_dir() else "     "
                lines.append(f"{dt} {kind:5} {size:8} {e.name}")
            else:
                lines.append(e.name + ("/" if e.is_dir() else ""))
        return "\n".join(lines)

    def cd(self, path):
        target = self.abspath(path)
        if target.exists() and target.is_dir():
            self.cwd = target
            return ""
        return f"Path not found: {path}"

    def read(self, path):
        p = self.abspath(path)
        if not p.exists() or not p.is_file():
            return f"File not found: {path}"
        return p.read_text(encoding="utf-8", errors="replace")

    def write(self, path, content):
        p = self.abspath(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return ""

# --------------------------
# Operating systems
# --------------------------

class OperatingSystem:
    def __init__(self, sandbox):
        self.sb = sandbox

    def prompt(self):
        raise NotImplementedError

    def run(self, line):
        raise NotImplementedError

class DOS(OperatingSystem):
    def prompt(self):
        return f"C:{str(self.sb.cwd).replace('/', '\\')}> "

    def run(self, line):
        parts = line.strip().split()
        if not parts:
            return ""
        cmd, *args = parts
        cmd = cmd.lower()

        if cmd == "help":
            return "\n".join([
                "DIR, CD, TYPE, ECHO, EXIT",
            ])
        if cmd == "dir":
            return self.sb.ls()
        if cmd == "cd":
            return self.sb.cd(args[0] if args else ".")
        if cmd == "type":
            return self.sb.read(args[0]) if args else "Usage: TYPE <file>"
        if cmd == "echo":
            return " ".join(args)
        if cmd == "exit":
            return "__EXIT__"
        return f"Unknown DOS command: {cmd}"

class Unix(OperatingSystem):
    def prompt(self):
        return f"loa@aposx:{self.sb.cwd}$ "

    def run(self, line):
        parts = line.strip().split()
        if not parts:
            return ""
        cmd, *args = parts

        if cmd == "help":
            return "\n".join([
                "ls, cd, cat, echo, exit",
            ])
        if cmd == "ls":
            return self.sb.ls(detailed="-l" in args)
        if cmd == "cd":
            return self.sb.cd(args[0] if args else ".")
        if cmd == "cat":
            return self.sb.read(args[0]) if args else "Usage: cat <file>"
        if cmd == "echo":
            return " ".join(args)
        if cmd == "exit":
            return "__EXIT__"
        return f"Unknown Unix command: {cmd}"

# --------------------------
# APOSX Computer
# --------------------------

class Computer:
    def __init__(self, name="APOSX", mode="unix"):
        self.name = name
        self.sb = Sandbox()
        self.mode = mode
        self.os = Unix(self.sb) if mode == "unix" else DOS(self.sb)

    def boot(self):
        bios_post()
        draw_splash()
        clear()
        print(center(f"{self.name} OS Loader • LoA Corporation", shutil.get_terminal_size((80, 24)).columns))
        time.sleep(0.5)

    def switch(self, mode):
        self.mode = mode
        self.os = Unix(self.sb) if mode == "unix" else DOS(self.sb)
        return f"Mode switched to {mode.upper()}."

    def run_loop(self):
        while True:
            try:
                cmd = input(self.os.prompt())
            except EOFError:
                print("\nPowering down.")
                break
            out = self.os.run(cmd)
            if out == "__EXIT__":
                print("Powering down APOSX...")
                break
            if out:
                print(out)

# --------------------------
# Entry point
# --------------------------

if __name__ == "__main__":
    comp = Computer(name="APOSX", mode="unix")
    comp.boot()
    comp.run_loop()
