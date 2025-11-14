#!/usr/bin/env python3
"""
SCO UNIX System V/386 Modem Login Simulator
Simulates a classic modem login to a SCO UNIX System from the 1990s era
"""

import sys
import time
import random
import getpass
from datetime import datetime
import io
import tarfile

class VNode:
    """Virtual filesystem node (file or directory)"""
    def __init__(self, name, is_dir=False, parent=None, permissions="rwxr-xr-x", owner="root", group="sys"):
        self.name = name
        self.is_dir = is_dir
        self.parent = parent
        self.children = {} if is_dir else None
        self.content = "" if not is_dir else None
        self.permissions = permissions
        self.owner = owner
        self.group = group
        self.size = 0
        self.mtime = datetime.now()

    def get_full_path(self):
        """Get the full path of this node"""
        if self.parent is None:
            return "/"
        path_parts = []
        node = self
        while node.parent is not None:
            path_parts.insert(0, node.name)
            node = node.parent
        return "/" + "/".join(path_parts) if path_parts else "/"

    def add_child(self, child):
        """Add a child node to this directory"""
        if self.is_dir:
            self.children[child.name] = child
            child.parent = self

    def remove_child(self, name):
        """Remove a child node from this directory"""
        if self.is_dir and name in self.children:
            del self.children[name]

class VirtualFileSystem:
    """Virtual filesystem implementation"""
    def __init__(self):
        # Create root directory
        self.root = VNode("/", is_dir=True, parent=None)
        self.current_dir = self.root
        self._initialize_standard_structure()

    def _initialize_standard_structure(self):
        """Initialize standard SCO Unix directory structure"""
        # Standard Unix directories
        standard_dirs = [
            ("bin", "rwxr-xr-x"),
            ("etc", "rwxr-xr-x"),
            ("home", "rwxr-xr-x"),
            ("usr", "rwxr-xr-x"),
            ("tmp", "rwxrwxrwx"),
            ("var", "rwxr-xr-x"),
            ("dev", "rwxr-xr-x"),
            ("lib", "rwxr-xr-x"),
            ("sbin", "rwxr-xr-x"),
            ("boot", "rwxr-xr-x"),
            ("mnt", "rwxr-xr-x"),
            ("opt", "rwxr-xr-x"),
        ]

        for dirname, perms in standard_dirs:
            node = VNode(dirname, is_dir=True, permissions=perms)
            self.root.add_child(node)

        # Create /home/dxmail structure
        home_dir = self.root.children["home"]
        dxmail_dir = VNode("dxmail", is_dir=True, permissions="rwxr-xr-x")
        home_dir.add_child(dxmail_dir)

        dxmail_subdirs = [
            "bin",
            "etc",
            "lib",
        ]

        for subdir in dxmail_subdirs:
            node = VNode(subdir, is_dir=True, permissions="rwxr-xr-x")
            dxmail_dir.add_child(node)

        # Create /home/dxmail/lib/queue structure
        lib_dir = dxmail_dir.children["lib"]
        queue_dir = VNode("queue", is_dir=True, permissions="rwxr-xr-x")
        lib_dir.add_child(queue_dir)

        trash_dir = VNode("trash", is_dir=True, permissions="rwxr-xr-x")
        queue_dir.add_child(trash_dir)

        # Create /home/hacky
        hacky_dir = VNode("hacky", is_dir=True, permissions="rwxr-xr-x")
        home_dir.add_child(hacky_dir)

        # Create some standard files
        profile = VNode(".profile", is_dir=False, permissions="rw-r--r--")
        profile.content = """# .profile for root
PATH=/bin:/usr/bin:/etc:/usr/sbin
export PATH
PS1='# '
TERM=vt100
export TERM
"""
        profile.size = len(profile.content)
        self.root.add_child(profile)

        history = VNode(".history", is_dir=False, permissions="rw-------")
        history.content = ""
        history.size = 0
        self.root.add_child(history)

    def resolve_path(self, path):
        """Resolve a path to a VNode"""
        if not path:
            return self.current_dir

        # Handle absolute paths
        if path.startswith("/"):
            current = self.root
            path = path[1:]  # Remove leading slash
        else:
            current = self.current_dir

        # Handle empty path (just "/")
        if not path:
            return current

        # Split path and navigate
        parts = path.split("/")
        for part in parts:
            if not part or part == ".":
                continue
            elif part == "..":
                if current.parent:
                    current = current.parent
            else:
                if not current.is_dir:
                    return None
                if part not in current.children:
                    return None
                current = current.children[part]

        return current

    def mkdir(self, path):
        """Create a directory"""
        # Get parent directory and directory name
        if "/" in path:
            parent_path = path.rsplit("/", 1)[0]
            dirname = path.rsplit("/", 1)[1]
            parent = self.resolve_path(parent_path) if parent_path else self.current_dir
        else:
            dirname = path
            parent = self.current_dir

        if parent is None or not parent.is_dir:
            return False, "mkdir: cannot create directory: No such file or directory"

        if dirname in parent.children:
            return False, f"mkdir: cannot create directory '{dirname}': File exists"

        new_dir = VNode(dirname, is_dir=True)
        parent.add_child(new_dir)
        return True, None

    def chdir(self, path):
        """Change current directory"""
        if not path:
            # No argument, go to home (which is root for root user)
            self.current_dir = self.root
            return True, None

        target = self.resolve_path(path)
        if target is None:
            return False, f"{path}: No such file or directory"
        if not target.is_dir:
            return False, f"{path}: Not a directory"

        self.current_dir = target
        return True, None

    def list_dir(self, path=None, long_format=False):
        """List directory contents"""
        if path:
            target = self.resolve_path(path)
        else:
            target = self.current_dir

        if target is None:
            return None, f"ls: cannot access {path}: No such file or directory"

        if not target.is_dir:
            # If it's a file, just show the file
            if long_format:
                return [self._format_long_entry(target)], None
            else:
                return [target.name], None

        entries = []
        for name, node in sorted(target.children.items()):
            if long_format:
                entries.append(self._format_long_entry(node))
            else:
                entries.append(name)

        return entries, None

    def _format_long_entry(self, node):
        """Format a directory entry in long format"""
        # Type
        type_char = "d" if node.is_dir else "-"

        # Permissions
        perms = node.permissions

        # Number of links (simplified)
        links = len(node.children) + 2 if node.is_dir else 1

        # Owner and group
        owner = node.owner.ljust(8)
        group = node.group.ljust(8)

        # Size
        size = str(node.size).rjust(8)

        # Time
        mtime = node.mtime.strftime("%b %d %H:%M")

        # Name
        name = node.name

        return f"{type_char}{perms}  {links:2} {owner} {group} {size} {mtime} {name}"

class ModemSimulator:
    def __init__(self):
        self.connected = False
        self.logged_in = False
        self.username = None

        # Default users for demo (in production passwords should be hashed)
        self.users = {
            "root": "root",
            "sysadmin": "admin123",
            "user": "password",
            "guest": "guest"
        }

        # Virtual filesystem
        self.vfs = VirtualFileSystem()

        # Alias storage
        self.aliases = {}

    def slow_print(self, text, delay=0.05):
        """Prints text character by character for authentic retro effect"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def print_instant(self, text):
        """Prints text instantly"""
        print(text)

    def simulate_modem_dial(self):
        """Simulates the modem dial-in process"""
        self.print_instant("\n" + "="*60)
        self.print_instant("     MODEM COMMUNICATIONS SIMULATOR v2.4")
        self.print_instant("     Copyright (C) 1995-1998")
        self.print_instant("="*60 + "\n")

        time.sleep(0.5)
        self.slow_print("Initializing modem...", 0.03)
        time.sleep(0.3)

        # AT commands
        at_commands = [
            ("AT", "OK"),
            ("ATZ", "OK"),
            ("ATE1", "OK"),
            ("ATM1", "OK"),
            ("ATX4", "OK"),
            ("ATDT 555-1234", "")
        ]

        for cmd, response in at_commands:
            self.slow_print(f"{cmd}", 0.02)
            time.sleep(0.2)
            if response:
                self.slow_print(response, 0.02)
            time.sleep(0.3)

        # Simulate dialing sounds
        self.print_instant("")
        self.slow_print("Dialing...", 0.04)
        time.sleep(0.5)

        dial_sounds = ["BEEP", "BEEP", "BEEP", "BEEP", "BEEP", "BEEP", "BEEP"]
        for sound in dial_sounds:
            sys.stdout.write(sound + " ")
            sys.stdout.flush()
            time.sleep(0.15)
        print("\n")

        time.sleep(0.5)
        self.slow_print("Connecting...", 0.04)
        time.sleep(0.8)

        # Modem handshake sounds as text
        handshake = [
            "RRRRR.....",
            "KSSSSSHHHHhhhh....",
            "BEEEEeeeeee....",
            "WRRRRrrrrrr....",
            "CHHHhhhhh...."
        ]

        for sound in handshake:
            self.slow_print(sound, 0.02)
            time.sleep(0.3)

        time.sleep(0.5)
        self.print_instant("")
        self.slow_print("CONNECT 14400/V.32bis", 0.03)
        self.connected = True
        time.sleep(0.5)

    def show_login_screen(self):
        """Displays the login screen"""
        self.print_instant("\n" + "="*60)
        self.print_instant("")
        self.print_instant("     ███████╗ ██████╗ ██████╗     ██╗   ██╗███╗   ██╗██╗██╗  ██╗")
        self.print_instant("     ██╔════╝██╔════╝██╔═══██╗    ██║   ██║████╗  ██║██║╚██╗██╔╝")
        self.print_instant("     ███████╗██║     ██║   ██║    ██║   ██║██╔██╗ ██║██║ ╚███╔╝ ")
        self.print_instant("     ╚════██║██║     ██║   ██║    ██║   ██║██║╚██╗██║██║ ██╔██╗ ")
        self.print_instant("     ███████║╚██████╗╚██████╔╝    ╚██████╔╝██║ ╚████║██║██╔╝ ██╗")
        self.print_instant("     ╚══════╝ ╚═════╝ ╚═════╝      ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝")
        self.print_instant("")
        self.print_instant("     SCO UNIX System V/386 Release 3.2")
        self.print_instant("     Copyright (C) 1976-1995 The Santa Cruz Operation, Inc.")
        self.print_instant("="*60)
        self.print_instant(f"\nSystem time: {datetime.now().strftime('%b %d %H:%M:%S %Y')}")
        self.print_instant("Last successful connection: Nov 13 14:32:18 2025")
        self.print_instant("\n" + "-"*60)

    def login(self):
        """Performs the login process"""
        max_attempts = 3
        attempts = 0

        while attempts < max_attempts and not self.logged_in:
            print("\n")
            username = input("login: ")
            password = getpass.getpass("Password: ")

            # Simulate processing time
            sys.stdout.write("Authenticating")
            for _ in range(3):
                time.sleep(0.3)
                sys.stdout.write(".")
                sys.stdout.flush()
            print()
            time.sleep(0.5)

            if username in self.users and self.users[username] == password:
                self.logged_in = True
                self.username = username
                self.slow_print(f"\n*** Login successful for {username} ***", 0.03)
                time.sleep(0.5)
                return True
            else:
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    self.slow_print(f"\nLogin incorrect", 0.03)
                    self.slow_print(f"Remaining attempts: {remaining}", 0.03)
                    time.sleep(0.5)

        if not self.logged_in:
            self.slow_print("\n*** Too many login failures ***", 0.03)
            self.slow_print("Disconnecting...", 0.03)
            time.sleep(1)
            self.disconnect()
            return False

    def show_welcome_message(self):
        """Displays welcome message after login"""
        self.print_instant("\n" + "="*60)
        self.print_instant("  SCO UNIX System V/386 Release 3.2")
        self.print_instant("="*60)
        self.print_instant(f"\nLast login: {datetime.now().strftime('%a %b %d %H:%M:%S')} on tty1a")
        self.print_instant(f"Terminal: vt100")
        self.print_instant(f"\nYou have mail.")
        self.print_instant("\n" + "-"*60)
        self.print_instant("SCO UNIX System V/386 Release 3.2 (scohost)")
        self.print_instant("-"*60 + "\n")

    def execute_command(self, command):
        """Executes Unix commands"""
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
            if args:
                success, error = self.vfs.chdir(args[0])
                if not success:
                    self.print_instant(f"cd: {error}")
            else:
                # cd without arguments goes to root for root user
                self.vfs.chdir("/")

        elif cmd == "pwd":
            self.print_instant(self.vfs.current_dir.get_full_path())

        elif cmd == "mkdir":
            if not args:
                self.print_instant("Usage: mkdir directory")
            else:
                for dirname in args:
                    success, error = self.vfs.mkdir(dirname)
                    if not success:
                        self.print_instant(error)

        elif cmd == "ls":
            # Parse ls options
            long_format = "-l" in args
            # Remove options from args to get paths
            paths = [arg for arg in args if not arg.startswith("-")]

            if not paths:
                paths = [None]  # Current directory

            for path in paths:
                entries, error = self.vfs.list_dir(path, long_format)
                if error:
                    self.print_instant(error)
                else:
                    if long_format:
                        # Calculate total blocks (simplified)
                        total = len(entries) * 4
                        self.print_instant(f"total {total}")
                        for entry in entries:
                            self.print_instant(entry)
                    else:
                        # Print entries in columns (tab-separated)
                        self.print_instant("\t".join(entries))

        elif cmd == "date":
            self.print_instant(datetime.now().strftime('%a %b %d %H:%M:%S %Z %Y'))

        elif cmd == "who":
            self.print_instant(f"{self.username:<12} tty1a        {datetime.now().strftime('%b %d %H:%M')}")
            self.print_instant(f"operator     tty2         {datetime.now().strftime('%b %d')} 09:15")
            self.print_instant(f"admin        tty3         {datetime.now().strftime('%b %d')} 14:22")

        elif cmd == "w" or cmd == "whoami":
            if cmd == "whoami":
                self.print_instant(self.username)
            else:
                current_time = datetime.now().strftime('%H:%M:%S')
                self.print_instant(f" {current_time}  up 23 days,  4:32,  3 users")
                self.print_instant(f"User     tty       login@  idle   what")
                self.print_instant(f"{self.username:<8} tty1a     {datetime.now().strftime('%H:%M')}    0     -sh")
                self.print_instant(f"operator tty2      09:15    1:45  /usr/bin/vi")
                self.print_instant(f"admin    tty3      14:22    0:12  /bin/sh")

        elif cmd == "uptime":
            self.print_instant(f" {datetime.now().strftime('%H:%M:%S')}  up 23 days,  4:32,  3 users,  load average: 0.15, 0.21, 0.18")

        elif cmd == "df":
            self.print_instant("Filesystem            kbytes    used   avail capacity  Mounted on")
            self.print_instant("/dev/root              51200   28672   22528    56%    /")
            self.print_instant("/dev/u                256000  189440   66560    74%    /u")
            self.print_instant("/dev/swap              65536   12288   53248    19%    swap")

        elif cmd == "ps":
            if "-ef" in args or "-aux" in args:
                self.print_instant("  UID   PID  PPID  C    STIME TTY      TIME COMMAND")
                self.print_instant("  root     1     0  0 Nov 01  ?        0:03 /etc/init")
                self.print_instant("  root    23     1  0 Nov 01  ?        0:00 /etc/cron")
                self.print_instant("  root    45     1  0 Nov 01  ?        0:12 /etc/syslogd")
                self.print_instant(f"  {self.username:<8}{random.randint(100,999)}     1  0 {datetime.now().strftime('%H:%M')}  tty1a    0:00 -sh")
                self.print_instant("  root   156     1  0 Nov 02  ?        1:23 /usr/lib/sendmail")
                self.print_instant("  root   234     1  0 Nov 03  ?        0:45 /usr/sbin/inetd")
            else:
                self.print_instant("  PID TTY      TIME COMMAND")
                self.print_instant(f" {random.randint(100,999)} tty1a    0:00 sh")
                self.print_instant(f" {random.randint(100,999)} tty1a    0:00 ps")

        elif cmd == "uname":
            if "-a" in args:
                self.print_instant("SCO_SV scohost 3.2 2 i386")
            else:
                self.print_instant("SCO_SV")

        elif cmd == "cat":
            if args:
                if args[0] == "/etc/motd":
                    self.print_instant("\nSCO UNIX System V/386 Release 3.2")
                    self.print_instant("Copyright (C) 1976-1995 The Santa Cruz Operation, Inc.")
                    self.print_instant("\nWelcome to SCO UNIX!")
                    self.print_instant("For technical support, contact your system administrator.")
                elif args[0] == ".profile":
                    self.print_instant("# .profile for root")
                    self.print_instant("PATH=/bin:/usr/bin:/etc:/usr/sbin")
                    self.print_instant("export PATH")
                    self.print_instant("PS1='# '")
                    self.print_instant("TERM=vt100")
                    self.print_instant("export TERM")
                else:
                    self.print_instant(f"cat: cannot open {args[0]}: No such file or directory")
            else:
                self.print_instant("Usage: cat filename")

        elif cmd == "clear":
            # Simple clear using many blank lines
            print("\n" * 50)

        elif cmd == "help":
            self.print_instant("\nAvailable UNIX commands:")
            self.print_instant("-" * 60)
            self.print_instant("  ls [-l] [path]  - list directory contents")
            self.print_instant("  cd [path]       - change directory")
            self.print_instant("  pwd             - print working directory")
            self.print_instant("  mkdir <dir>     - create directory")
            self.print_instant("  alias [name[=value]] - define or display aliases")
            self.print_instant("  tar cvf <file> <dir> - create tar archive")
            self.print_instant("  tar xvf <file>  - extract tar archive")
            self.print_instant("  date            - print system date and time")
            self.print_instant("  who             - display logged in users")
            self.print_instant("  w               - display users and their activities")
            self.print_instant("  whoami          - print effective user name")
            self.print_instant("  uptime          - display system uptime")
            self.print_instant("  df              - report filesystem disk space usage")
            self.print_instant("  ps [-ef]        - report process status")
            self.print_instant("  uname [-a]      - print system information")
            self.print_instant("  cat <file>      - concatenate and print files")
            self.print_instant("  clear           - clear the terminal screen")
            self.print_instant("  exit, logout    - log out of the system")
            self.print_instant("-" * 60)

        elif cmd == "alias":
            if not args:
                # Display all aliases
                if not self.aliases:
                    # No output if no aliases defined (standard Unix behavior)
                    pass
                else:
                    for name, value in sorted(self.aliases.items()):
                        self.print_instant(f"{name}='{value}'")
            else:
                # Parse alias definition
                alias_def = " ".join(args)
                if "=" in alias_def:
                    # Define new alias
                    name, value = alias_def.split("=", 1)
                    # Remove quotes if present
                    value = value.strip("'\"")
                    self.aliases[name] = value
                else:
                    # Display specific alias
                    if alias_def in self.aliases:
                        self.print_instant(f"{alias_def}='{self.aliases[alias_def]}'")
                    else:
                        self.print_instant(f"alias: {alias_def}: not found")

        elif cmd == "tar":
            if len(args) < 2:
                self.print_instant("Usage: tar [cvf|xvf] file [directory]")
            else:
                options = args[0]
                tarfile_name = args[1]

                if options == "cvf":
                    # Create tar archive
                    if len(args) < 3:
                        self.print_instant("tar: missing directory argument")
                    else:
                        dir_path = args[2]
                        target = self.vfs.resolve_path(dir_path)
                        if target is None:
                            self.print_instant(f"tar: {dir_path}: No such file or directory")
                        elif not target.is_dir:
                            self.print_instant(f"tar: {dir_path}: Not a directory")
                        else:
                            # Create tar archive in memory
                            tar_content = self._create_tar(target)
                            # Store as virtual file
                            tar_node = VNode(tarfile_name, is_dir=False)
                            tar_node.content = tar_content
                            tar_node.size = len(tar_content)
                            self.vfs.current_dir.add_child(tar_node)
                            # Print verbose output
                            self._print_tar_contents(target, "a")

                elif options == "xvf":
                    # Extract tar archive
                    tar_node = self.vfs.resolve_path(tarfile_name)
                    if tar_node is None:
                        self.print_instant(f"tar: {tarfile_name}: No such file or directory")
                    elif tar_node.is_dir:
                        self.print_instant(f"tar: {tarfile_name}: Is a directory")
                    else:
                        # Extract tar archive
                        if tar_node.content:
                            self._extract_tar(tar_node.content)
                        else:
                            self.print_instant(f"tar: {tarfile_name}: Empty archive")

                else:
                    self.print_instant(f"tar: invalid option -- '{options}'")
                    self.print_instant("Usage: tar [cvf|xvf] file [directory]")

        elif cmd == "logout" or cmd == "exit" or cmd == "quit":
            return False

        else:
            self.print_instant(f"{cmd}: not found")

        return True

    def _create_tar(self, root_node):
        """Create a tar archive from a virtual directory tree"""
        tar_buffer = io.BytesIO()
        with tarfile.open(fileobj=tar_buffer, mode='w') as tar:
            self._add_to_tar(tar, root_node, root_node.name)
        return tar_buffer.getvalue()

    def _add_to_tar(self, tar, node, arcname):
        """Recursively add nodes to tar archive"""
        info = tarfile.TarInfo(name=arcname)
        info.mtime = int(node.mtime.timestamp())
        info.uid = 0
        info.gid = 0
        info.uname = node.owner
        info.gname = node.group

        if node.is_dir:
            info.type = tarfile.DIRTYPE
            info.mode = 0o755
            tar.addfile(info)
            # Add children
            for child_name, child_node in node.children.items():
                child_arcname = f"{arcname}/{child_name}"
                self._add_to_tar(tar, child_node, child_arcname)
        else:
            info.type = tarfile.REGTYPE
            info.mode = 0o644
            info.size = len(node.content) if node.content else 0
            content_bytes = node.content.encode('utf-8') if node.content else b''
            tar.addfile(info, io.BytesIO(content_bytes))

    def _print_tar_contents(self, node, prefix="a", path=""):
        """Print tar archive contents in verbose mode"""
        current_path = f"{path}/{node.name}" if path else node.name
        self.print_instant(f"{prefix} {current_path}")

        if node.is_dir:
            for child_name, child_node in sorted(node.children.items()):
                self._print_tar_contents(child_node, prefix, current_path)

    def _extract_tar(self, tar_content):
        """Extract a tar archive to the virtual filesystem"""
        tar_buffer = io.BytesIO(tar_content)
        try:
            with tarfile.open(fileobj=tar_buffer, mode='r') as tar:
                for member in tar.getmembers():
                    # Print extraction (verbose mode)
                    self.print_instant(f"x {member.name}")

                    # Skip if it's the root of the archive
                    if not member.name or member.name == '.':
                        continue

                    # Parse path
                    path_parts = member.name.split('/')

                    # Navigate to parent directory
                    parent = self.vfs.current_dir
                    for part in path_parts[:-1]:
                        if part not in parent.children:
                            # Create intermediate directory
                            new_dir = VNode(part, is_dir=True)
                            parent.add_child(new_dir)
                            parent = new_dir
                        else:
                            parent = parent.children[part]

                    # Create the file or directory
                    name = path_parts[-1]
                    if member.isdir():
                        if name not in parent.children:
                            new_dir = VNode(name, is_dir=True)
                            parent.add_child(new_dir)
                    else:
                        # Extract file content
                        file_content = tar.extractfile(member)
                        content = file_content.read().decode('utf-8') if file_content else ""

                        new_file = VNode(name, is_dir=False)
                        new_file.content = content
                        new_file.size = len(content)
                        parent.add_child(new_file)

        except Exception as e:
            self.print_instant(f"tar: Error extracting archive: {e}")

    def interactive_shell(self):
        """Interactive shell after successful login"""
        self.show_welcome_message()

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

        self.logout()

    def logout(self):
        """Logout process"""
        self.print_instant("\n" + "="*60)
        self.slow_print("Closing session...", 0.03)
        time.sleep(0.5)
        self.slow_print(f"Goodbye, {self.username}!", 0.03)
        self.slow_print(f"Connect time: {random.randint(5, 45)} minutes", 0.03)
        time.sleep(0.5)
        self.disconnect()

    def disconnect(self):
        """Disconnects the modem connection"""
        self.slow_print("\nDisconnecting...", 0.03)
        time.sleep(0.5)
        self.slow_print("+++ATH0", 0.03)
        time.sleep(0.3)
        self.slow_print("NO CARRIER", 0.03)
        time.sleep(0.3)
        self.print_instant("\n" + "="*60)
        self.print_instant("  Connection closed")
        self.print_instant("="*60 + "\n")
        self.connected = False
        self.logged_in = False

    def run(self):
        """Main program"""
        try:
            # Simulate modem dial-in
            self.simulate_modem_dial()

            # Display login screen
            self.show_login_screen()

            # Perform login
            if self.login():
                # Start interactive shell
                self.interactive_shell()

        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user.")
            if self.connected:
                self.disconnect()
        except Exception as e:
            print(f"\nError: {e}")
            if self.connected:
                self.disconnect()

def main():
    """Main entry point"""
    print("\nStarting SCO UNIX Modem Simulator...")
    print("(Press Ctrl+C to abort)\n")
    time.sleep(1)

    simulator = ModemSimulator()
    simulator.run()

    print("\nThank you for using the SCO UNIX Simulator!")
    print("Demo credentials: root/root, sysadmin/admin123, user/password, guest/guest\n")

if __name__ == "__main__":
    main()
