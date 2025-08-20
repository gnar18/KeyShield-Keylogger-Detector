import psutil
import win32gui
import win32process
import win32api
import win32con
import time

SUSPICIOUS_KEYWORDS = ["keylog", "logger", "keyboard", "hook", "spy", "stealth"]

def detect_keylogger():
    print("🔍 Scanning for suspicious processes...")
    suspicious_processes = []

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            pid = proc.info['pid']
            name = proc.info['name'].lower()

            # Rule 1: Suspicious names
            if any(keyword in name for keyword in SUSPICIOUS_KEYWORDS):
                suspicious_processes.append((pid, name, "Suspicious process name"))

            # Rule 2: Hidden window check
            def callback(hwnd, pid_list):
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if found_pid == pid and win32gui.IsWindowVisible(hwnd) == 0:
                    pid_list.append((pid, name, "Hidden window"))
            win32gui.EnumWindows(callback, suspicious_processes)

            # Rule 3: Network activity check
            conns = proc.connections(kind='inet')
            for conn in conns:
                if conn.status == "ESTABLISHED" and conn.raddr:
                    suspicious_processes.append((pid, name, f"Network activity → {conn.raddr}"))

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if suspicious_processes:
        print("⚠️ Suspicious Processes Detected:")
        for pid, name, reason in suspicious_processes:
            print(f"PID {pid} - {name} ({reason})")
    else:
        print("✅ No suspicious processes found.")


def decoy_keystroke_trap():
    """
    Sends fake keystrokes (decoy password).
    If a process is intercepting all keystrokes, it may log this.
    User should later check if this decoy appears in unexpected places (like logs).
    """
    print("\n🎭 Running decoy keystroke trap...")
    decoy_password = "FAKE_PASSWORD_123"
    for char in decoy_password:
        win32api.keybd_event(ord(char.upper()), 0, 0, 0)
        time.sleep(0.05)
        win32api.keybd_event(ord(char.upper()), 0, win32con.KEYEVENTF_KEYUP, 0)
    print("✅ Decoy keystrokes sent. If a hidden keylogger is running, it may log this fake password.")


if __name__ == "__main__":
    print("🛡️ Advanced Keylogger Detector")
    choice = input("Do you want to (S)can or (T)rap? ").strip().upper()

    if choice == "S":
        detect_keylogger()
    elif choice == "T":
        decoy_keystroke_trap()
    else:
        print("❌ Invalid choice. Use S or T.")

