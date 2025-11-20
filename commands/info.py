"""
System Information Commands Module
Implements commands that display system information
"""

from system_time import now
from argparse_unix import parse_unix_args
from process_table import ProcessTable
import random

# Global process table instance
_process_table = None


def get_process_table():
    """Get or create the global process table instance"""
    global _process_table
    if _process_table is None:
        _process_table = ProcessTable()
    return _process_table


def execute_date(vfs, args, print_func):
    """Execute date command - print system date and time"""
    print_func(now().strftime('%a %b %d %H:%M:%S %Z %Y'))


def execute_who(username, args, print_func):
    """Execute who command - display logged in users"""
    print_func(f"{username:<12} tty1a        {now().strftime('%b %d %H:%M')}")
    print_func(f"operator     tty2         Dec 10 23:15")
    print_func(f"admin        tty3         Dec 11 00:22")


def execute_w(username, args, print_func):
    """Execute w command - display users and their activities"""
    current_time = now().strftime('%H:%M:%S')
    print_func(f" {current_time}  up 23 days,  4:32,  3 users")
    print_func(f"User     tty       login@  idle   what")
    print_func(f"{username:<8} tty1a     {now().strftime('%H:%M')}    0     -sh")
    print_func(f"operator tty2      23:15    2:30  /usr/bin/vi")
    print_func(f"admin    tty3      00:22    1:23  /bin/sh")


def execute_whoami(username, args, print_func):
    """Execute whoami command - print effective user name"""
    print_func(username)


def execute_uptime(vfs, args, print_func):
    """Execute uptime command - display system uptime"""
    print_func(f" {now().strftime('%H:%M:%S')}  up 23 days,  4:32,  3 users,  load average: 0.15, 0.21, 0.18")


def execute_df(vfs, args, print_func):
    """Execute df command - report filesystem disk space usage"""
    print_func("Filesystem            kbytes    used   avail capacity  Mounted on")
    print_func("/dev/root              51200   28672   22528    56%    /")
    print_func("/dev/u                256000  189440   66560    74%    /u")
    print_func("tmpfs                  16384    1024   15360     7%    /tmp")
    print_func("/dev/swap              65536   12288   53248    19%    swap")


def execute_ps(username, args, print_func):
    """Execute ps command - report process status"""
    # Get process table
    ptable = get_process_table()

    # Parse arguments using unified parser
    parsed = parse_unix_args(args)

    # Check for full listing options (handles -ef, -e -f, -aux, -a -u -x)
    full_listing = (parsed.has_flag('e') and parsed.has_flag('f')) or \
                   (parsed.has_flag('a') and parsed.has_flag('u') and parsed.has_flag('x'))

    # Add current shell and ps process for this user
    shell_pid = random.randint(800, 899)
    ps_pid = random.randint(900, 999)

    # Temporarily add shell and ps processes
    shell_proc_exists = ptable.get_process(shell_pid) is None
    ps_proc_exists = ptable.get_process(ps_pid) is None

    if shell_proc_exists:
        from process_table import Process
        shell_proc = Process(shell_pid, 1, username, "-sh", "tty1a", now().strftime('%H:%M'), "0:00")
        ptable.add_process(shell_proc)

    if ps_proc_exists:
        from process_table import Process
        ps_proc = Process(ps_pid, shell_pid, username, "ps " + " ".join(args), "tty1a", now().strftime('%H:%M'), "0:00")
        ptable.add_process(ps_proc)

    # Get formatted output from process table
    output_lines = ptable.format_ps_output(full_listing=full_listing, filter_user=None if full_listing else username)

    # Print all lines
    for line in output_lines:
        print_func(line)

    # Clean up temporary processes
    if shell_proc_exists:
        ptable.remove_process(shell_pid)
    if ps_proc_exists:
        ptable.remove_process(ps_pid)


def execute_uname(vfs, args, print_func):
    """Execute uname command - print system information"""
    # Parse arguments using unified parser
    parsed = parse_unix_args(args)

    if parsed.has_flag('a'):
        print_func("SCO_SV scohost 3.2 2 i386")
    else:
        print_func("SCO_SV")
