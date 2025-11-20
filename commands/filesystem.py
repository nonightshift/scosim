"""
Filesystem Commands Module
Implements directory navigation and listing commands
"""

import time
from argparse_unix import parse_unix_args


def execute_cd(vfs, args, print_func):
    """Execute cd command - change directory"""
    if args:
        success, error = vfs.chdir(args[0])
        if not success:
            print_func(f"cd: {error}")
    else:
        # cd without arguments goes to root for root user
        vfs.chdir("/")


def execute_pwd(vfs, args, print_func):
    """Execute pwd command - print working directory"""
    print_func(vfs.current_dir.get_full_path())


def execute_mkdir(vfs, args, print_func):
    """Execute mkdir command - create directory"""
    if not args:
        print_func("Usage: mkdir directory")
    else:
        for dirname in args:
            success, error = vfs.mkdir(dirname)
            if not success:
                print_func(error)


def execute_ls(vfs, args, print_func):
    """Execute ls command - list directory contents"""
    # Parse arguments using unified parser
    parsed = parse_unix_args(args)

    # Check for options
    long_format = parsed.has_flag('l')
    show_hidden = parsed.has_flag('a')
    sort_by_time = parsed.has_flag('t')
    reverse_sort = parsed.has_flag('r')

    # Get paths
    paths = parsed.get_positionals()
    if not paths:
        paths = [None]  # Current directory

    for path in paths:
        entries, error = vfs.list_dir(path, long_format, show_hidden, sort_by_time, reverse_sort)
        if error:
            print_func(error)
        else:
            if long_format:
                # Calculate total blocks (simplified)
                total = len(entries) * 4
                print_func(f"total {total}")
                for entry in entries:
                    print_func(entry)
            else:
                # Print entries in columns (tab-separated)
                if entries:
                    print_func("\t".join(entries))


def execute_rm(vfs, args, print_func):
    """Execute rm command - remove files or directories"""
    if not args:
        print_func("Usage: rm [-r] file ...")
        return

    # Parse arguments using unified parser
    parsed = parse_unix_args(args)

    # Check for options (handles -rf, -fr, -r, -f all correctly)
    recursive = parsed.has_flag('r')
    force = parsed.has_flag('f')

    # Get file paths
    paths = parsed.get_positionals()

    if not paths:
        print_func("rm: missing operand")
        return

    # Expand glob patterns for each path
    expanded_paths = []
    for path in paths:
        matched = vfs.glob_match(path)
        if matched:
            expanded_paths.extend(matched)
        else:
            # No matches found - add original path (will produce error unless -f is used)
            expanded_paths.append(path)

    # If no files matched any pattern and not using force, show error
    if not expanded_paths and not force:
        print_func("rm: no matches found")
        return

    # Remove each matched file
    for path in expanded_paths:
        # Check if trying to delete /unix kernel
        target = vfs.resolve_path(path)
        if target is not None:
            full_path = target.get_full_path()
            if full_path == "/unix":
                print_func("Out of memory.")
                # Still proceed with deletion despite error message

        success, error = vfs.remove(path, recursive, force)
        if not success and not force:
            print_func(error)

        # Add delay to simulate real file deletion (approximately 100ms per file)
        time.sleep(0.1)
