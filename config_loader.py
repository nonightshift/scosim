"""
Configuration Loader Module
Loads configuration from config.json
"""

import json
import os

# Default configuration values
DEFAULT_CONFIG = {
    "command_delays": {
        "tar": {"delay": 0.02},
        "rm": {"delay": 0.1}
    }
}

_config = None


def load_config():
    """Load configuration from config.json"""
    global _config
    if _config is not None:
        return _config

    config_path = os.path.join(os.path.dirname(__file__), 'config.json')

    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                _config = json.load(f)
        else:
            _config = DEFAULT_CONFIG
    except Exception as e:
        print(f"Warning: Error loading config.json: {e}")
        print("Using default configuration values.")
        _config = DEFAULT_CONFIG

    return _config


def get_command_delay(command):
    """Get the delay value for a specific command"""
    config = load_config()
    try:
        return config["command_delays"][command]["delay"]
    except KeyError:
        # Return default values if not found
        return DEFAULT_CONFIG["command_delays"].get(command, {}).get("delay", 0.0)
