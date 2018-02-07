'''
Collection of Windows-specific I/O functions
'''

import msvcrt
import time
import ctypes
import weakref

SW_RESTORE = 9
SPIF_SENDCHANGE = 2
SPI_GETFOREGROUNDLOCKTIMEOUT = 0x2000
SPI_SETFOREGROUNDLOCKTIMEOUT = 0x2001


hwnd_map = weakref.WeakKeyDictionary()

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

def flush_io_buffer():
    while msvcrt.kbhit():
        print(msvcrt.getch().decode('utf8'), end='')

def close_active_window():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    ctypes.windll.user32.PostMessageA(hwnd, winconstants.WM_CLOSE, 0, 0)

def maximize_active_window():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    ctypes.windll.user32.ShowWindow(hwnd, 3)

class WindowImplementation:

    def __init__(self, hwnd):
        self.hwnd = hwnd

    @property
    def title(self):
        length = GetWindowTextLength(self.hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(self.hwnd, buff, length + 1)
        return buff.value

    def minimize(self):
        ctypes.windll.user32.ShowWindow(self.hwnd, 6)

    def focus(self):
        IsIconic = ctypes.windll.user32.IsIconic
        ShowWindow = ctypes.windll.user32.ShowWindow
        GetForegroundWindow = ctypes.windll.user32.GetForegroundWindow
        GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
        BringWindowToTop = ctypes.windll.user32.BringWindowToTop
        AttachThreadInput = ctypes.windll.user32.AttachThreadInput
        SetForegroundWindow = ctypes.windll.user32.SetForegroundWindow
        SystemParametersInfo = ctypes.windll.user32.SystemParametersInfoA
        
        if IsIconic(self.hwnd):
            ShowWindow(self.hwnd, SW_RESTORE)
        if GetForegroundWindow() == self.hwnd:
            return True
        ForegroundThreadID = GetWindowThreadProcessId(GetForegroundWindow(), None)
        ThisThreadID = GetWindowThreadProcessId(self.hwnd, None)
        if AttachThreadInput(ThisThreadID, ForegroundThreadID, True):
            BringWindowToTop(self.hwnd)
            SetForegroundWindow(self.hwnd)
            AttachThreadInput(ThisThreadID, ForegroundThreadID, False)
            if GetForegroundWindow() == self.hwnd:
                return True
        timeout = ctypes.c_int()
        zero = ctypes.c_int(0)
        SystemParametersInfo(winconstants.SPI_GETFOREGROUNDLOCKTIMEOUT, 0, ctypes.byref(timeout), 0)
        (winconstants.SPI_SETFOREGROUNDLOCKTIMEOUT, 0, ctypes.byref(zero), winconstants.SPIF_SENDCHANGE)
        BringWindowToTop(self.hwnd)
        SetForegroundWindow(self.hwnd)
        SystemParametersInfo(winconstants.SPI_SETFOREGROUNDLOCKTIMEOUT, 0, ctypes.byref(timeout), winconstants.SPIF_SENDCHANGE); 
        if GetForegroundWindow() == self.hwnd:
            return True
        return False


def get_all_windows():
    windows = []

    def window_enum_callback(hwnd, _):
        if IsWindowVisible(hwnd) and get_window_title(hwnd):
            window = create_application_window(hwnd)
            windows.append(window)
        return True

    EnumWindows(EnumWindowsProc(window_enum_callback), 0)
    return windows

def get_foreground_window():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    return create_application_window(hwnd)

def create_application_window(hwnd):
    from pywindow.appwindow import ApplicationWindow
    impl = WindowImplementation(hwnd)
    return ApplicationWindow(impl)