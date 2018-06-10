from context import pywindow
import time

def debug():
    windows = pywindow.all_windows()
    print(windows)
    # for w in windows:
    #     print(w.title)
    time.sleep(3)
    w = pywindow.foreground_window()
    print(w.coords)
    print(w.right)
    time.sleep(5)
    # w.close()
    w.maximize()

if __name__ == '__main__':
    debug()