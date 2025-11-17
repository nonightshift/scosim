"""
System Information Commands Module
Implements commands that display system information
"""

from system_time import now
import random


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
    if "-ef" in args or "-aux" in args:
        print_func("  UID   PID  PPID  C    STIME TTY      TIME COMMAND")
        print_func("  root     1     0  0 Nov 01  ?        0:03 /etc/init")
        print_func("  root    23     1  0 Nov 01  ?        0:00 /etc/cron")
        print_func("  root    45     1  0 Nov 01  ?        0:12 /etc/syslogd")
        print_func(f"  {username:<8}{random.randint(100,999)}     1  0 {now().strftime('%H:%M')}  tty1a    0:00 -sh")
        print_func("  root   156     1  0 Nov 02  ?        1:23 /usr/lib/sendmail")
        print_func("  root   234     1  0 Nov 03  ?        0:45 /usr/sbin/inetd")
    else:
        print_func("  PID TTY      TIME COMMAND")
        print_func(f" {random.randint(100,999)} tty1a    0:00 sh")
        print_func(f" {random.randint(100,999)} tty1a    0:00 ps")


def execute_uname(vfs, args, print_func):
    """Execute uname command - print system information"""
    if "-a" in args:
        print_func("SCO_SV scohost 3.2 2 i386")
    else:
        print_func("SCO_SV")
