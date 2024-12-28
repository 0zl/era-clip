import os
from ctypes import WINFUNCTYPE, WinDLL, Structure, c_long, byref, wintypes

user32 = WinDLL("user32")
user32.SetWindowPos.restype = wintypes.BOOL
user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.UINT]
WNDENUMPROC = WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
user32.EnumWindows.argtypes = [WNDENUMPROC, wintypes.LPARAM]

def get_hwnd_from_pid(pid: int) -> int | None:
    import ctypes
    result = None

    def callback(hwnd, _):
        nonlocal result
        lpdw_PID = ctypes.c_ulong()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(lpdw_PID))
        hwnd_PID = lpdw_PID.value

        if hwnd_PID == pid:
            result = hwnd
            return False
        return True

    cb_worker = WNDENUMPROC(callback)
    user32.EnumWindows(cb_worker, 0)
    return result

def set_always_top(value: bool):
    window = get_hwnd_from_pid(os.getpid())
    if window is None:
        return

    class RECT(Structure):
        _fields_ = [
            ('left', c_long),
            ('top', c_long),
            ('right', c_long),
            ('bottom', c_long),
        ]

        def width(self):  return self.right - self.left
        def height(self): return self.bottom - self.top

    rc = RECT()
    user32.GetWindowRect(window, byref(rc))
    value = -1 if value else -2
    user32.SetWindowPos(window, value, rc.left, rc.top, 0, 0, 0x0001)

def set_window_transparency(opacity: float):
    """Set window transparency. opacity should be between 0.0 and 1.0"""
    window = get_hwnd_from_pid(os.getpid())
    if window is None:
        return

    style = user32.GetWindowLongA(window, -20)  # GWL_EXSTYLE
    user32.SetWindowLongA(window, -20, style | 0x80000)
    user32.SetLayeredWindowAttributes(window, 0, int(255 * opacity), 0x02)  # LWA_ALPHA
