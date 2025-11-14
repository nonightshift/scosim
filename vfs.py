"""
Virtual Filesystem Module
Implements a virtual filesystem for the SCO UNIX simulator
"""

from datetime import datetime


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
