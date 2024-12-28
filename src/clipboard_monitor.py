import win32clipboard
import win32con
import win32gui
import threading
import time
import threading
import sys

class ClipboardMonitor:
    def __init__(self, callback):
        self.hwnd = None
        self.next_clipboard_viewer = None
        self.is_running = False
        self.thread = None
        self.class_atom = None
        self.callback = callback

    def start_thread(self):
        try:
            wc = win32gui.WNDCLASS()
            wc.lpfnWndProc = self.wnd_proc
            wc.hInstance = win32gui.GetModuleHandle(None)
            wc.lpszClassName = "EraClipboardMonitor"
            
            try:
                win32gui.UnregisterClass(wc.lpszClassName, wc.hInstance)
            except:
                pass
                
            self.class_atom = win32gui.RegisterClass(wc)

            self.hwnd = win32gui.CreateWindow(self.class_atom, "EraClipboardMonitor", 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None)
            if not self.hwnd:
                raise Exception("Failed to create window.")
            
            win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, win32con.WS_EX_TOOLWINDOW)
            win32gui.ShowWindow(self.hwnd, win32con.SW_HIDE)

            self.next_clipboard_viewer = win32clipboard.SetClipboardViewer(self.hwnd)
            if not self.next_clipboard_viewer:
                print("Warning: No next clipboard viewer.")
            
            self.is_running = True
            print("Clipboard monitor started.")

            while self.is_running:
                win32gui.PumpWaitingMessages()
                time.sleep(0.1)

            sys.exit(0)
        except Exception as e:
            print(f"Error in start_thread: {e}")
    
    def start(self):
        if self.thread and self.thread.is_alive():
            return
        self.is_running = True
        self.thread = threading.Thread(target=self.start_thread)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.is_running = False
        if self.hwnd:
            try:
                win32clipboard.ChangeClipboardChain(self.hwnd, self.next_clipboard_viewer)
                win32gui.SendMessage(self.hwnd, win32con.WM_DESTROY, 0, 0)
            except Exception as e:
                print(f"Error during cleanup: {e}")
            self.hwnd = None
        
        if self.class_atom:
            try:
                win32gui.UnregisterClass("EraClipboardMonitor", win32gui.GetModuleHandle(None))
                self.class_atom = None
            except Exception as e:
                print(f"Error unregistering class: {e}")
        
        if self.thread:
            self.thread.join(timeout=1.0)
            self.thread = None
        
        print("Clipboard monitor stopped.")
    
    def wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_DRAWCLIPBOARD:
            time.sleep(0.2) # Delay to let the clipboard data be ready
            self.on_clipboard_change()
            if self.next_clipboard_viewer:
                win32gui.SendMessage(self.next_clipboard_viewer, msg, wparam, lparam)
        elif msg == win32con.WM_CHANGECBCHAIN:
            if wparam == self.next_clipboard_viewer:
                self.next_clipboard_viewer = lparam
            elif self.next_clipboard_viewer:
                win32gui.SendMessage(self.next_clipboard_viewer, msg, wparam, lparam)
        elif msg in (win32con.WM_CLOSE,win32con.WM_DESTROY):
            win32gui.PostQuitMessage(0)
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)
    
    def on_clipboard_change(self):
        try:
            win32clipboard.OpenClipboard()
            if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
                data = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
                if self.callback:
                    self.callback(data)
            win32clipboard.CloseClipboard()
        except Exception as e:
            raise e