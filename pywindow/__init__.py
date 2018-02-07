import os
import sys

if sys.platform == 'win32':
    import pywindow._windows as os_specific_implementation 
else:
    raise RuntimeError

def get_all_windows():
    return os_specific_implementation.get_all_windows()
def get_foreground_window():
    return os_specific_implementation.get_foreground_window()