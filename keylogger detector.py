import psutil
import win32gui
import win32process

SUSPICIOUS_KEYWORDS = ["keylog", "logger", "keyboard", "hook", "spy"]

def detect_keylogger():
    print("🔍 Scanning for suspicious processes...")
    suspicious_processes = []

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            pid = proc.info['pid']
            name = proc.info['name'].lower()

            # Rule 1: Check for suspicious names
            if any(keyword in name for keyword in SUSPICIOUS_KEYWORDS):
                suspicious_processes.append((pid, name))

            # Rule 2: Check if process has hidden/invisible window
            def callback(hwnd, pid_list):
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if found_pid == pid and win32gui.IsWindowVisible(hwnd) == 0:
                    pid_list.append((pid, name))
            win32gui.EnumWindows(callback, suspicious_processes)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if suspicious_processes:
        print("⚠️ Suspicious Processes Detected:")
        for pid, name in suspicious_processes:
            print(f"PID {pid} - {name}")
    else:
        print("✅ No keylogger detected.")

if __name__ == "__main__":
    detect_keylogger()
