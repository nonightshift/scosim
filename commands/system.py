"""
System Commands Module
Implements system utility commands
"""


def execute_clear(vfs, args, print_func):
    """Execute clear command - clear the terminal screen"""
    # Simple clear using many blank lines
    print("\n" * 50)


def execute_help(vfs, args, print_func):
    """Execute help command - show available commands"""
    print_func("\nAvailable UNIX commands:")
    print_func("-" * 60)
    print_func("  ls [-l] [path]  - list directory contents")
    print_func("  cd [path]       - change directory")
    print_func("  pwd             - print working directory")
    print_func("  mkdir <dir>     - create directory")
    print_func("  alias [name[=value]] - define or display aliases")
    print_func("  tar cvf <file> <dir> - create tar archive")
    print_func("  tar xvf <file>  - extract tar archive")
    print_func("  date            - print system date and time")
    print_func("  who             - display logged in users")
    print_func("  w               - display users and their activities")
    print_func("  whoami          - print effective user name")
    print_func("  uptime          - display system uptime")
    print_func("  df              - report filesystem disk space usage")
    print_func("  ps [-ef]        - report process status")
    print_func("  uname [-a]      - print system information")
    print_func("  cat <file>      - concatenate and print files")
    print_func("  clear           - clear the terminal screen")
    print_func("  history         - show command history")
    print_func("  exit, logout    - log out of the system")
    print_func("-" * 60)


def execute_alias(aliases, args, print_func):
    """Execute alias command - define or display aliases"""
    if not args:
        # Display all aliases
        if not aliases:
            # No output if no aliases defined (standard Unix behavior)
            pass
        else:
            for name, value in sorted(aliases.items()):
                print_func(f"{name}='{value}'")
    else:
        # Parse alias definition
        alias_def = " ".join(args)
        if "=" in alias_def:
            # Define new alias
            name, value = alias_def.split("=", 1)
            # Remove quotes if present
            value = value.strip("'\"")
            aliases[name] = value
        else:
            # Display specific alias
            if alias_def in aliases:
                print_func(f"{alias_def}='{aliases[alias_def]}'")
            else:
                print_func(f"alias: {alias_def}: not found")
