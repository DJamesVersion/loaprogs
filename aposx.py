#!/usr/bin/env python3
# APOSX Virtual Computer Emulator • LoA Corporation Experimental Shell

import os
import time
from pathlib import Path
from datetime import datetime

# --------------------------
# Ritual Boot Sequence
# --------------------------

def boot_sequence():
    print("\033[2J\033[H", end="")  # Clear screen
    print("LoA Corporation BIOS v7.1")
    time.sleep(0.5)
    print("Initializing doctrine vault...")
    time.sleep(0.5)
    print("Synchronizing ceremonial clock... [T-Solar 13:7]")
    time.sleep(0.5)
    print("Glyph co-processor detected [v2.4]")
    time.sleep(0.5)
    print("Memory check: 65536 KB OK")
    time.sleep(0.5)
    print("Boot device: NVMe Codex [LoA-APOSX]")
    time.sleep(0.5)
    print("Launching APOSX environment...\n")
    time.sleep(1)

# --------------------------
# Filesystem Sandbox
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

    def cd(self, path):
        target = self.abspath(path)
        if target.exists() and target.is_dir():
            self.cwd = target
            return ""
        return f"Directory not found: {path}"

    def mkdir(self, path):
        p = self.abspath(path)
        try:
            p.mkdir(parents=True, exist_ok=False)
            return f"Directory created: {p}"
        except FileExistsError:
            return f"Already exists: {p}"
        except Exception as e:
            return f"Error: {e}"

    def ls(self):
        try:
            return "\n".join(f"{e.name}/" if e.is_dir() else e.name for e in self.cwd.iterdir())
        except Exception as e:
            return f"Error: {e}"

    def write(self, path, content):
        p = self.abspath(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"Wrote to {p}"

    def read(self, path):
        p = self.abspath(path)
        if not p.exists():
            return f"File not found: {path}"
        return p.read_text(encoding="utf-8", errors="replace")

# --------------------------
# APOSX Shell Environment
# --------------------------

class APOSXShell:
    def __init__(self):
        self.sb = Sandbox()
        self.env = {}
        self.running = True

    def prompt(self):
        return f"loa@aposx:{self.sb.cwd}$ "

    def run(self, line):
        parts = line.strip().split()
        if not parts:
            return ""
        cmd, *args = parts

        match cmd:
            case "exit":
                self.running = False
                return "Shutting down APOSX..."
            case "ls":
                return self.sb.ls()
            case "cd":
                return self.sb.cd(args[0] if args else ".")
            case "mkdir" | "mk":
                return self.sb.mkdir(args[0]) if args else "Usage: mkdir <dir>"
            case "cat":
                return self.sb.read(args[0]) if args else "Usage: cat <file>"
            case "echo":
                return " ".join(args)
            case "sh":
                return self.run_script(args[0]) if args else "Usage: sh <script.sh>"
            case "cmake":
                return self.simulate_cmake(args)
            case "git":
                return self.simulate_git(args)
            case "npm":
                return self.simulate_npm(args)
            case "help":
                return self.help_text()
            case _:
                return f"Unknown command: {cmd}"

    def run_script(self, filename):
        path = self.sb.abspath(filename)
        if not path.exists():
            return f"Script not found: {filename}"
        lines = path.read_text(encoding="utf-8").splitlines()
        output = []
        for line in lines:
            result = self.run(line)
            if result:
                output.append(result)
        return "\n".join(output)

    def simulate_cmake(self, args):
        return "[CMake] Ritual configuration complete. Codex bindings aligned."

    def simulate_git(self, args):
        if not args:
            return "[Git] Usage: git <command>"
        subcmd = args[0]
        match subcmd:
            case "init":
                return "[Git] Initialized empty ceremonial repository."
            case "status":
                return "[Git] No commits yet. Doctrine clean."
            case "clone":
                return "[Git] Cloning glyph repository... (simulated)"
            case _:
                return f"[Git] Unknown subcommand: {subcmd}"

    def simulate_npm(self, args):
        if not args:
            return "[npm] Usage: npm <command>"
        subcmd = args[0]
        match subcmd:
            case "init":
                return "[npm] Initialized package.json for ritual scripts."
            case "install":
                return "[npm] Installing ceremonial modules... (simulated)"
            case "run":
                return "[npm] Executing glyph overlay... (simulated)"
            case _:
                return f"[npm] Unknown subcommand: {subcmd}"

    def help_text(self):
        return "\n".join([
            "APOSX Shell Commands:",
            "  ls                - list directory contents",
            "  cd <dir>          - change directory",
            "  mkdir <dir>       - create directory",
            "  mk <dir>          - alias for mkdir",
            "  cat <file>        - view file contents",
            "  echo <text>       - print text",
            "  sh <script.sh>    - run shell script",
            "  cmake             - simulate CMake ritual",
            "  git <cmd>         - simulate Git commands",
            "  npm <cmd>         - simulate npm commands",
            "  help              - show this help",
            "  exit              - shut down APOSX",
        ])

    def loop(self):
        print("Welcome to APOSX • LoA Corporation Experimental Shell")
        while self.running:
            try:
                line = input(self.prompt())
            except EOFError:
                break
            out = self.run(line)
            if out:
                print(out)

# --------------------------
# Entry Point
# --------------------------

if __name__ == "__main__":
    boot_sequence()
    shell = APOSXShell()
    shell.loop()
