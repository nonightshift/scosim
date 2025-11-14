"""
File Operations Commands Module
Implements file reading and manipulation commands
"""


def execute_cat(vfs, args, print_func):
    """Execute cat command - concatenate and print files"""
    if args:
        if args[0] == "/etc/motd":
            print_func("\nSCO UNIX System V/386 Release 3.2")
            print_func("Copyright (C) 1976-1995 The Santa Cruz Operation, Inc.")
            print_func("\nWelcome to SCO UNIX!")
            print_func("For technical support, contact your system administrator.")
        elif args[0] == ".profile":
            print_func("# .profile for root")
            print_func("PATH=/bin:/usr/bin:/etc:/usr/sbin")
            print_func("export PATH")
            print_func("PS1='# '")
            print_func("TERM=vt100")
            print_func("export TERM")
        else:
            print_func(f"cat: cannot open {args[0]}: No such file or directory")
    else:
        print_func("Usage: cat filename")
