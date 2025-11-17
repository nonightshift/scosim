"""
System Time Module
Provides simulated system time for the SCO UNIX simulator
"""

from datetime import datetime


class SystemTime:
    """Manages simulated system time for historical simulation"""

    def __init__(self):
        # System starts at December 11, 1995, 01:45:00
        self._system_time = datetime(1995, 12, 11, 1, 45, 0)
        self._start_time = self._system_time

    def now(self):
        """Return the current simulated system time"""
        return self._system_time

    def set_time(self, dt):
        """Set the system time to a specific datetime"""
        self._system_time = dt

    def advance(self, seconds=0, minutes=0, hours=0, days=0):
        """Advance the system time by the specified amount"""
        from datetime import timedelta
        delta = timedelta(days=days, seconds=seconds, minutes=minutes, hours=hours)
        self._system_time += delta

    def get_start_time(self):
        """Get the time when the system started"""
        return self._start_time


# Global system time instance
_system_time = SystemTime()


def now():
    """Get the current simulated system time (replacement for datetime.now())"""
    return _system_time.now()


def get_system_time():
    """Get the SystemTime instance"""
    return _system_time


def create_historical_datetime(year, month, day, hour=0, minute=0, second=0):
    """Create a datetime for historical file timestamps (must be before system start)"""
    dt = datetime(year, month, day, hour, minute, second)
    if dt >= _system_time.now():
        raise ValueError(f"Historical datetime {dt} must be before system start time {_system_time.now()}")
    return dt
