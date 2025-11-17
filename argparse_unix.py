"""
Unix-style Argument Parser
Provides a unified parameter parser for classic Unix command behavior
"""


class UnixArgParser:
    """
    Parse Unix-style command arguments
    Supports:
    - Combined short options: -la, -rf
    - Separate short options: -l -a
    - Options with values: -n 10
    - Positional arguments
    """

    def __init__(self):
        self.flags = set()
        self.options = {}
        self.positionals = []

    def parse(self, args):
        """
        Parse argument list

        Args:
            args: List of argument strings

        Returns:
            Self for chaining
        """
        i = 0
        while i < len(args):
            arg = args[i]

            if arg.startswith('-') and len(arg) > 1 and arg != '--':
                # This is an option
                if arg.startswith('--'):
                    # Long option (not commonly used in classic Unix)
                    option_name = arg[2:]
                    if '=' in option_name:
                        key, value = option_name.split('=', 1)
                        self.options[key] = value
                    else:
                        self.flags.add(option_name)
                else:
                    # Short option(s)
                    option_chars = arg[1:]

                    # Check if this looks like a combined option (like -rf, -la, -aux)
                    # Process each character as a separate flag
                    for char in option_chars:
                        self.flags.add(char)
                i += 1
            elif arg == '--':
                # Everything after -- is positional
                self.positionals.extend(args[i+1:])
                break
            else:
                # Positional argument
                self.positionals.append(arg)
                i += 1

        return self

    def has_flag(self, *flags):
        """Check if any of the given flags are present"""
        for flag in flags:
            if flag in self.flags:
                return True
        return False

    def get_option(self, name, default=None):
        """Get value of an option"""
        return self.options.get(name, default)

    def get_positionals(self):
        """Get all positional arguments"""
        return self.positionals

    def has_any_flags(self, flag_set):
        """Check if any flags from the given set are present"""
        return bool(self.flags.intersection(flag_set))


def parse_unix_args(args):
    """
    Convenience function to parse Unix-style arguments

    Args:
        args: List of argument strings

    Returns:
        UnixArgParser instance with parsed arguments
    """
    parser = UnixArgParser()
    return parser.parse(args)
