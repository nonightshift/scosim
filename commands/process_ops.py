"""
Process Operations Commands Module
Implements commands for process management (kill, etc.)
"""

from argparse_unix import parse_unix_args
from commands.info import get_process_table


def execute_kill(username, args, print_func):
    """Execute kill command - send signal to a process"""
    # Get process table
    ptable = get_process_table()

    if not args:
        print_func("usage: kill [ -sig ] pid ...")
        print_func("       kill -l")
        return

    # Parse arguments
    parsed = parse_unix_args(args)

    # Check for -l flag (list signals)
    if parsed.has_flag('l'):
        print_func("HUP INT QUIT ILL TRAP ABRT EMT FPE KILL BUS SEGV SYS")
        print_func("PIPE ALRM TERM USR1 USR2 CHLD PWR WINCH URG POLL STOP")
        print_func("TSTP CONT TTIN TTOU VTALRM PROF XCPU XFSZ WAITING LWP")
        return

    # Extract signal number (default is 15 - SIGTERM)
    signal = 15
    pids = []

    for arg in args:
        if arg.startswith('-') and len(arg) > 1 and arg[1:].isdigit():
            # Signal specified as -9, -15, etc.
            signal = int(arg[1:])
        elif arg.isdigit():
            # PID
            pids.append(int(arg))

    if not pids:
        print_func("kill: no process ID specified")
        return

    # Check permissions - non-root users can only kill their own processes
    for pid in pids:
        proc = ptable.get_process(pid)

        if proc is None:
            print_func(f"kill: {pid}: No such process")
            continue

        # Permission check
        if username != "root" and proc.uid != username:
            print_func(f"kill: {pid}: Operation not permitted")
            continue

        # Attempt to kill the process
        success, message = ptable.kill_process(pid, signal)

        # Only print message if there was an error
        # (Unix kill is normally silent on success)
        if not success:
            print_func(message)
