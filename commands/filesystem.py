"""
Filesystem Commands Module
Implements directory navigation and listing commands
"""


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
    # Parse ls options
    long_format = "-l" in args
    # Remove options from args to get paths
    paths = [arg for arg in args if not arg.startswith("-")]

    if not paths:
        paths = [None]  # Current directory

    for path in paths:
        entries, error = vfs.list_dir(path, long_format)
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
                print_func("\t".join(entries))


def execute_rm(vfs, args, print_func):
    """Execute rm command - remove files or directories"""
    if not args:
        print_func("Usage: rm [-r] file ...")
        return

    # Parse options
    recursive = "-r" in args or "-rf" in args or "-fr" in args
    force = "-f" in args or "-rf" in args or "-fr" in args

    # Get file paths (filter out options)
    paths = [arg for arg in args if not arg.startswith("-")]

    if not paths:
        print_func("rm: missing operand")
        return

    for path in paths:
        success, error = vfs.remove(path, recursive, force)
        if not success and not force:
            print_func(error)
