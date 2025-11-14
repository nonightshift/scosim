"""
Shell Module
Implements an interactive shell with bash-like history
"""

import sys
import readline
import atexit
import os
from vfs import VirtualFileSystem
from commands.filesystem import execute_cd, execute_pwd, execute_mkdir, execute_ls
from commands.info import execute_date, execute_who, execute_w, execute_whoami, execute_uptime, execute_df, execute_ps, execute_uname
from commands.file_ops import execute_cat
from commands.tar_ops import execute_tar
from commands.system import execute_clear, execute_help, execute_alias


class Shell:
    """Interactive shell with bash-like history"""

    def __init__(self, username, vfs=None):
        self.username = username
        self.vfs = vfs if vfs else VirtualFileSystem()
        self.aliases = {}
        self.history_file = os.path.expanduser('~/.scosim_history')
        self.history_max_size = 1000

        # Initialize readline for history support
        self._setup_history()

    def _setup_history(self):
        """Setup readline history with bash-like behavior"""
        # Configure readline
        readline.set_history_length(self.history_max_size)

        # Load history from file if it exists
        if os.path.exists(self.history_file):
            try:
                readline.read_history_file(self.history_file)
            except:
                pass

        # Register save history on exit
        atexit.register(self._save_history)

    def _save_history(self):
        """Save command history to file"""
        try:
            readline.write_history_file(self.history_file)
        except:
            pass

    def print_instant(self, text):
        """Print text instantly"""
        print(text)

    def execute_command(self, command):
        """Execute Unix commands"""
        # Add to history (readline handles this automatically when using input())

        parts = command.strip().split()
        if not parts:
            return True

        # Check for aliases
        cmd = parts[0].lower()
        if cmd in self.aliases:
            # Replace command with alias expansion
            alias_expansion = self.aliases[cmd]
            # Combine alias expansion with remaining arguments
            command = alias_expansion + " " + " ".join(parts[1:]) if len(parts) > 1 else alias_expansion
            parts = command.strip().split()
            cmd = parts[0].lower()

        args = parts[1:] if len(parts) > 1 else []

        # Directory navigation commands
        if cmd == "cd":
            execute_cd(self.vfs, args, self.print_instant)

        elif cmd == "pwd":
            execute_pwd(self.vfs, args, self.print_instant)

        elif cmd == "mkdir":
            execute_mkdir(self.vfs, args, self.print_instant)

        elif cmd == "ls":
            execute_ls(self.vfs, args, self.print_instant)

        # System info commands
        elif cmd == "date":
            execute_date(self.vfs, args, self.print_instant)

        elif cmd == "who":
            execute_who(self.username, args, self.print_instant)

        elif cmd == "w":
            execute_w(self.username, args, self.print_instant)

        elif cmd == "whoami":
            execute_whoami(self.username, args, self.print_instant)

        elif cmd == "uptime":
            execute_uptime(self.vfs, args, self.print_instant)

        elif cmd == "df":
            execute_df(self.vfs, args, self.print_instant)

        elif cmd == "ps":
            execute_ps(self.username, args, self.print_instant)

        elif cmd == "uname":
            execute_uname(self.vfs, args, self.print_instant)

        # File operations
        elif cmd == "cat":
            execute_cat(self.vfs, args, self.print_instant)

        elif cmd == "tar":
            execute_tar(self.vfs, args, self.print_instant)

        # System commands
        elif cmd == "clear":
            execute_clear(self.vfs, args, self.print_instant)

        elif cmd == "help":
            execute_help(self.vfs, args, self.print_instant)

        elif cmd == "alias":
            execute_alias(self.aliases, args, self.print_instant)

        elif cmd == "history":
            self._show_history(args)

        elif cmd == "logout" or cmd == "exit" or cmd == "quit":
            return False

        else:
            self.print_instant(f"{cmd}: not found")

        return True

    def _show_history(self, args):
        """Show command history"""
        # Get number of history entries to show
        num_entries = readline.get_current_history_length()

        if args and args[0].isdigit():
            # Show last N entries
            show_count = int(args[0])
            start_index = max(1, num_entries - show_count + 1)
        else:
            # Show all history
            start_index = 1

        # Print history with line numbers
        for i in range(start_index, num_entries + 1):
            entry = readline.get_history_item(i)
            if entry:
                print(f" {i:4d}  {entry}")

    def run(self):
        """Run the interactive shell"""
        while True:
            try:
                # Unix root prompt
                if self.username == "root":
                    prompt = "# "
                else:
                    prompt = "$ "

                command = input(prompt)

                if not self.execute_command(command):
                    break

            except KeyboardInterrupt:
                print("\n")
                confirm = input("Do you really want to logout? (y/n): ")
                if confirm.lower() in ['y', 'yes']:
                    break
            except EOFError:
                break

        return True
