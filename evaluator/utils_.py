import psutil
import base64
import win32gui
from win32 import win32process

import pygetwindow as gw 

def get_window_hwnd(pid):
    windows = gw.getWindowsWithTitle("")  
    for window in windows:
        hwnd = window._hWnd
        thread_id, process_id = win32process.GetWindowThreadProcessId(hwnd)
        if process_id == pid:
            return hwnd
    return -1

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    

def get_window_rect(pid):
    hwnd = get_window_hwnd(pid)
    if hwnd == -1:
        return -1
    else:
        rect = win32gui.GetWindowRect(hwnd)
        return rect

def get_python_pid():
    pid = []
    procs = psutil.process_iter()
    for proc in procs:
        if 'python' in proc.name().lower():
            pid.append(proc.pid)
    return pid