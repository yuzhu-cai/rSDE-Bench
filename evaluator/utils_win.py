import psutil
import base64
# import Quartz

# def get_window_hwnd(pid):
#     """
#     Get the window ID of a window by its process ID.
    
#     Parameters:
#     pid (int): The process ID of the window's owner.

#     Returns:
#     int: The window ID if found, otherwise -1.
#     """
#     # Get a list of all windows
#     options = Quartz.kCGWindowListOptionOnScreenOnly
#     window_list = Quartz.CGWindowListCopyWindowInfo(options, Quartz.kCGNullWindowID)

#     # Iterate over each window in the list
#     for window in window_list:
#         # Check if the window's process ID matches the given process ID
#         if window['kCGWindowOwnerPID'] == pid:
#             # Return the window ID if a match is found
#             return window['kCGWindowNumber']
    
#     # Return -1 if no matching window is found
#     return -1

# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode('utf-8')
    

# def get_window_rect(window_id):
#     """
#     Get the bounding rectangle of a window by its window ID.

#     Parameters:
#     window_id (int): The window ID of the target window.

#     Returns:
#     tuple: A tuple (x, y, width, height) representing the window's bounding rectangle,
#            or None if the window is not found.
#     """
#     # Get a list of all windows
#     options = Quartz.kCGWindowListOptionOnScreenOnly
#     window_list = Quartz.CGWindowListCopyWindowInfo(options, Quartz.kCGNullWindowID)
#     # import ipdb; ipdb.set_trace()
#     # Iterate over each window in the list
#     for window in window_list:
#         # Check if the window's ID matches the given window ID
#         if window['kCGWindowOwnerPID'] == window_id:
#             # Get the window's bounds
#             bounds = window['kCGWindowBounds']
#             x = bounds['X']
#             y = bounds['Y']
#             width = bounds['Width']
#             height = bounds['Height']
#             return (int(x), int(y), int(x+width), int(y+height))

#     # Return None if no matching window is found
#     return -1

def parse_data(data):
    result = {}
    
    # Process header
    header = data[0].strip().split('\t\t')
    tasks_header = header[0].strip()
    basic_header = header[1].strip()
    advanced_header = header[2].strip()
    
    for line in data[1:]:
        line = line.strip()
        if line:
            parts = line.replace('\t\t', '\t').split('\t')
            task = parts[0].strip()
            basic = parts[1].strip()
            advanced = parts[2].strip()
            result[task] = {
                basic_header: basic,
                advanced_header: advanced
            }
    
    return result

def get_python_pid():
    pid = []
    procs = psutil.process_iter()
    for proc in procs:
        if 'python' in proc.name().lower():
            pid.append(proc.pid)
    return pid