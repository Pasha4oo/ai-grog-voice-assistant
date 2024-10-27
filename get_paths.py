import os
import win32com.client

def resolve_shortcut(shortcut_path):
    if shortcut_path.lower().endswith((".lnk", ".url")):
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(shortcut_path)
        target_path = os.path.abspath(shortcut.TargetPath)
        _, extension = os.path.splitext(target_path)
        
        if extension.lower() == ".exe" and os.path.basename(target_path).lower() not in ("unins000.exe", "uninstall.exe", "setup.exe"):
            return target_path
    return None

def get_programs_from_start_menu():
    start_menu_path = os.path.join(os.environ['ProgramData'], 'Microsoft', 'Windows', 'Start Menu', 'Programs')
    desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')

    programs = []

    for root, dirs, files in os.walk(start_menu_path):
        for file in files:
            program_path = os.path.join(root, file)
            programs.append(program_path)

    for root, dirs, files in os.walk(desktop_path):
        for file in files:
            program_path = os.path.join(root, file)
            programs.append(program_path)

    return programs