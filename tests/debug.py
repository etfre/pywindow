from context import pywindow

def debug():
    windows = pywindow.get_all_windows()
    for w in windows:
        print(w.title)
    print(pywindow.get_foreground_window().minimize())

if __name__ == '__main__':
    debug()