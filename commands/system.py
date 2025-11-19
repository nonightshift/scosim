"""
System Commands Module
Implements system utility commands
"""

import json
import os


def execute_clear(vfs, args, print_func):
    """Execute clear command - clear the terminal screen"""
    # Simple clear using many blank lines
    print("\n" * 50)


def execute_help(vfs, args, print_func):
    """Execute help command - show available commands"""
    # Load commands from commands.json to generate dynamic help
    commands_file = "commands.json"

    print_func("\nAvailable UNIX commands:")
    print_func("-" * 60)

    try:
        if os.path.exists(commands_file):
            with open(commands_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # Display each command with its usage and description
            for cmd in config.get("commands", []):
                name = cmd.get("name", "")
                usage = cmd.get("usage", name)
                description = cmd.get("description", "")

                # Format: "  usage - description"
                print_func(f"  {usage:<20} - {description}")
        else:
            # Fallback to basic help if commands.json not found
            print_func("  Commands configuration file not found")

    except Exception as e:
        print_func(f"  Error loading help: {e}")

    # Add built-in commands not in commands.json
    print_func("  history              - show command history")
    print_func("  exit, logout         - log out of the system")
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


def execute_reset(vfs, args, print_func):
    """Execute reset command - restore filesystem to initial state"""
    success, error = vfs.reset()
    if success:
        print_func("System reset to initial state.")
    else:
        print_func(f"reset: {error}")
