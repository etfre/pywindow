from context import pywindow
import time

def debug():
    windows = pywindow.all_windows()
    print(windows)
    # for w in windows:
    #     print(w.title)
    time.sleep(3)
    w = pywindow.foreground_window()
    print('confused')
    time.sleep(30)
    w.maximize()
    # w.focus()

if __name__ == '__main__':
    debug()