"""
Shell Module
Implements an interactive shell with bash-like history
"""

import sys
import readline
import atexit
import os
import json
import importlib
from vfs import VirtualFileSystem


class Shell:
    """Interactive shell with bash-like history"""

    def __init__(self, username, vfs=None, commands_config_path="commands.json"):
        self.username = username
        self.vfs = vfs if vfs else VirtualFileSystem()
        self.aliases = {}
        self.history_file = os.path.expanduser('~/.scosim_history')
        self.history_max_size = 1000
        self.commands = {}
        self.commands_config_path = commands_config_path
        self.history = []  # Command history list for web terminal

        # Load dynamic commands
        self._load_commands()

        # Initialize readline for history support
        self._setup_history()

    def _load_commands(self):
        """Load commands dynamically from commands.json"""
        try:
            if not os.path.exists(self.commands_config_path):
                print(f"Warning: {self.commands_config_path} not found, using default command set")
                self._load_default_commands()
                return

            with open(self.commands_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            for cmd_config in config.get("commands", []):
                name = cmd_config.get("name")
                module_path = cmd_config.get("module")
                function_name = cmd_config.get("function")

                if not all([name, module_path, function_name]):
                    print(f"Warning: Invalid command configuration for {name}")
                    continue

                try:
                    # Dynamically import the module and get the function
                    module = importlib.import_module(module_path)
                    func = getattr(module, function_name)
                    self.commands[name] = func
                except (ImportError, AttributeError) as e:
                    print(f"Warning: Could not load command '{name}': {e}")

        except Exception as e:
            print(f"Error loading commands.json: {e}")
            print("Falling back to default commands...")
            self._load_default_commands()

    def _load_default_commands(self):
        """Load default commands as fallback"""
        try:
            from commands.filesystem import execute_cd, execute_pwd, execute_mkdir, execute_ls, execute_rm
            from commands.info import execute_date, execute_who, execute_w, execute_whoami, execute_uptime, execute_df, execute_ps, execute_uname
            from commands.file_ops import execute_cat
            from commands.tar_ops import execute_tar
            from commands.system import execute_clear, execute_help, execute_alias

            self.commands = {
                "cd": execute_cd,
                "pwd": execute_pwd,
                "mkdir": execute_mkdir,
                "ls": execute_ls,
                "rm": execute_rm,
                "cat": execute_cat,
                "tar": execute_tar,
                "date": execute_date,
                "who": execute_who,
                "w": execute_w,
                "whoami": execute_whoami,
                "uptime": execute_uptime,
                "df": execute_df,
                "ps": execute_ps,
                "uname": execute_uname,
                "clear": execute_clear,
                "help": execute_help,
                "alias": execute_alias,
            }
        except ImportError as e:
            print(f"Error loading default commands: {e}")

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

    def get_prompt(self):
        """Get the shell prompt based on username"""
        if self.username == "root":
            return "# "
        else:
            return "$ "

    def execute_command(self, command, print_func=None):
        """Execute Unix commands"""
        # Use provided print_func or default to print_instant
        if print_func is None:
            print_func = self.print_instant

        # Check for output redirection
        redirect_output = None
        redirect_append = False

        if '>>' in command:
            # Append redirect
            parts = command.split('>>', 1)
            command = parts[0].strip()
            redirect_output = parts[1].strip()
            redirect_append = True
        elif '>' in command:
            # Overwrite redirect
            parts = command.split('>', 1)
            command = parts[0].strip()
            redirect_output = parts[1].strip()
            redirect_append = False

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

        # Handle special built-in commands
        if cmd in ["logout", "exit", "quit"]:
            return False
        elif cmd == "history":
            self._show_history(args, print_func)
            return True

        # Handle output redirection
        if redirect_output:
            # Capture output
            captured_output = []
            def capture_print(text):
                captured_output.append(text)

            # Execute command with output capture
            if cmd in self.commands:
                func = self.commands[cmd]
                if cmd in ["who", "w", "whoami", "ps", "kill"]:
                    func(self.username, args, capture_print)
                elif cmd == "alias":
                    func(self.aliases, args, capture_print)
                else:
                    func(self.vfs, args, capture_print)
            else:
                capture_print(f"{cmd}: not found")

            # Write captured output to file
            content = "\n".join(captured_output) + "\n" if captured_output else ""
            success, error = self.vfs.write_file(redirect_output, content, redirect_append)
            if not success:
                print_func(error)
        else:
            # Dynamic command dispatch
            if cmd in self.commands:
                func = self.commands[cmd]
                # Check if command needs username (like who, whoami, w, ps, kill)
                if cmd in ["who", "w", "whoami", "ps", "kill"]:
                    func(self.username, args, print_func)
                # Check if command needs aliases dict (like alias command)
                elif cmd == "alias":
                    func(self.aliases, args, print_func)
                else:
                    # Standard commands that need vfs
                    func(self.vfs, args, print_func)
            else:
                print_func(f"{cmd}: not found")

        # Check if /unix file exists, print "Out of memory" if not
        unix_file = self.vfs.resolve_path("/unix")
        if unix_file is None:
            print_func("Out of memory")

        return True

    def _show_history(self, args, print_func=None):
        """Show command history"""
        if print_func is None:
            print_func = self.print_instant

        # Use self.history if available (web terminal), otherwise use readline (CLI)
        if self.history:
            # Web terminal mode - use self.history list
            num_entries = len(self.history)

            if args and args[0].isdigit():
                # Show last N entries
                show_count = int(args[0])
                start_index = max(0, num_entries - show_count)
            else:
                # Show all history
                start_index = 0

            # Print history with line numbers (1-indexed for display)
            for i in range(start_index, num_entries):
                print_func(f" {i+1:4d}  {self.history[i]}")
        else:
            # CLI mode - use readline
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
                    print_func(f" {i:4d}  {entry}")

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
