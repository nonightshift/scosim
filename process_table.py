"""
Process Table Simulation Module
Implements a simulated Unix process table with ps and kill command support
"""

import json
import os
from datetime import datetime, timedelta
from system_time import now


class Process:
    """Represents a single process in the process table"""

    def __init__(self, pid, ppid, uid, command, tty="?", stime=None, cputime="0:00", status="running"):
        self.pid = pid
        self.ppid = ppid
        self.uid = uid
        self.command = command
        self.tty = tty
        self.stime = stime if stime else now().strftime("%H:%M")
        self.cputime = cputime
        self.status = status  # running, sleeping, zombie, stopped
        self.c = 0  # CPU usage percentage

    def to_dict(self):
        """Convert process to dictionary representation"""
        return {
            "pid": self.pid,
            "ppid": self.ppid,
            "uid": self.uid,
            "command": self.command,
            "tty": self.tty,
            "stime": self.stime,
            "cputime": self.cputime,
            "status": self.status,
            "c": self.c
        }

    @classmethod
    def from_dict(cls, data):
        """Create process from dictionary representation"""
        proc = cls(
            pid=data.get("pid", 1),
            ppid=data.get("ppid", 0),
            uid=data.get("uid", "root"),
            command=data.get("command", ""),
            tty=data.get("tty", "?"),
            stime=data.get("stime"),
            cputime=data.get("cputime", "0:00"),
            status=data.get("status", "running")
        )
        proc.c = data.get("c", 0)
        return proc


class ProcessTable:
    """Simulated Unix process table"""

    def __init__(self, config_path="processes.json"):
        self.processes = {}  # pid -> Process
        self.config_path = config_path
        self.next_pid = 1000

        # Load initial process table from config
        self._load_from_config()

    def _load_from_config(self):
        """Load process table from JSON configuration"""
        if not os.path.exists(self.config_path):
            # Create default process table
            self._create_default_processes()
            return

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # Load processes
            for proc_data in config.get("processes", []):
                proc = Process.from_dict(proc_data)
                self.processes[proc.pid] = proc
                # Track highest PID for generating new PIDs
                if proc.pid >= self.next_pid:
                    self.next_pid = proc.pid + 1

        except Exception as e:
            print(f"Error loading process table: {e}")
            self._create_default_processes()

    def _create_default_processes(self):
        """Create a default set of system processes"""
        # System init process
        self.add_process(Process(1, 0, "root", "/etc/init", "?", "Nov 01", "0:03"))
        self.add_process(Process(23, 1, "root", "/etc/cron", "?", "Nov 01", "0:00"))
        self.add_process(Process(45, 1, "root", "/etc/syslogd", "?", "Nov 01", "0:12"))
        self.add_process(Process(156, 1, "root", "/usr/lib/sendmail", "?", "Nov 02", "1:23"))
        self.add_process(Process(234, 1, "root", "/usr/sbin/inetd", "?", "Nov 03", "0:45"))

    def add_process(self, process):
        """Add a process to the table"""
        self.processes[process.pid] = process

    def remove_process(self, pid):
        """Remove a process from the table"""
        if pid in self.processes:
            del self.processes[pid]
            return True
        return False

    def get_process(self, pid):
        """Get a process by PID"""
        return self.processes.get(pid)

    def get_all_processes(self):
        """Get all processes"""
        return list(self.processes.values())

    def get_processes_by_user(self, uid):
        """Get all processes for a specific user"""
        return [p for p in self.processes.values() if p.uid == uid]

    def get_processes_by_command(self, command_pattern):
        """Get processes matching a command pattern"""
        return [p for p in self.processes.values() if command_pattern in p.command]

    def kill_process(self, pid, signal=15):
        """
        Simulate killing a process
        Returns: (success, message)
        """
        if pid not in self.processes:
            return False, f"kill: {pid}: No such process"

        proc = self.processes[pid]

        # Don't allow killing init (PID 1)
        if pid == 1:
            return False, f"kill: {pid}: Operation not permitted"

        # Check if it's a critical system process
        critical_processes = [23, 45, 156, 234]  # cron, syslogd, sendmail, inetd
        if pid in critical_processes:
            # For simulation, we can kill but show a warning
            pass

        # Signal 9 (SIGKILL) removes immediately
        # Signal 15 (SIGTERM) is default
        if signal == 9:
            self.remove_process(pid)
            return True, f"Process {pid} ({proc.command}) killed with signal 9"
        else:
            # Simulate graceful termination - remove process
            self.remove_process(pid)
            return True, f"Process {pid} ({proc.command}) terminated"

    def spawn_process(self, uid, command, ppid=1, tty="?"):
        """
        Spawn a new process
        Returns: Process object
        """
        pid = self.next_pid
        self.next_pid += 1

        proc = Process(
            pid=pid,
            ppid=ppid,
            uid=uid,
            command=command,
            tty=tty,
            stime=now().strftime("%H:%M"),
            cputime="0:00"
        )

        self.add_process(proc)
        return proc

    def format_ps_output(self, full_listing=False, filter_user=None):
        """
        Format process table for ps command output

        Args:
            full_listing: If True, show full listing with all columns (ps -ef style)
            filter_user: If provided, only show processes for this user

        Returns:
            List of formatted output lines
        """
        output = []

        # Get processes to display
        if filter_user:
            procs = self.get_processes_by_user(filter_user)
        else:
            procs = self.get_all_processes()

        # Sort by PID
        procs = sorted(procs, key=lambda p: p.pid)

        if full_listing:
            # Full listing format (ps -ef)
            output.append("  UID   PID  PPID  C    STIME TTY      TIME COMMAND")
            for proc in procs:
                line = f"  {proc.uid:<8}{proc.pid:>5}{proc.ppid:>6}{proc.c:>3} {proc.stime:>8} {proc.tty:<8} {proc.cputime:>4} {proc.command}"
                output.append(line)
        else:
            # Simple listing format (ps)
            output.append("  PID TTY      TIME COMMAND")
            for proc in procs:
                # Extract command name (basename)
                cmd_name = proc.command.split('/')[-1].split()[0]
                line = f" {proc.pid:>4} {proc.tty:<8} {proc.cputime:>4} {cmd_name}"
                output.append(line)

        return output

    def save_to_config(self):
        """Save current process table to configuration file"""
        config = {
            "processes": [p.to_dict() for p in self.processes.values()]
        }

        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving process table: {e}")
            return False
