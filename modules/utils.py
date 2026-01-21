import os
import sys

def format_time(ms):
    if ms < 0:
        ms = 0
    seconds = ms // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}" 

def resource_path(*paths):
    # When running as .exe
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        # Always resolve from the project root, not modules/
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))

    return os.path.join(base_path, *paths)
