from context import pywindow
import time

def debug():
    windows = pywindow.get_all_windows()
    for w in windows:
        print(w.title)
    w = pywindow.get_foreground_window()
    w.minimize()
    time.sleep(3)
    w.focus()

if __name__ == '__main__':
    debug()