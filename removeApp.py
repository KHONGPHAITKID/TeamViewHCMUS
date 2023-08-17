import pygetwindow as gw
import winreg
import subprocess

def get_apps_in_taskbar():
    taskbar_apps = []

    windows = gw.getWindowsWithTitle('')
    for index, window in enumerate(windows):
        taskbar_apps.append((index, window.title))

    return taskbar_apps

def close_app_by_id(app_id):
    windows = gw.getWindowsWithTitle('')
    if app_id < len(windows):
        windows[app_id].close()
        print(f"Closed application with ID {app_id}")
    else:
        print(f"No application found with ID {app_id}")

def open_app_by_name(app_name):
    # Get a list of all open windows
    all_windows = gw.getWindows()

    # Search for a window with the specified app name
    for window in all_windows:
        if app_name.lower() in window.title.lower():
            window.activate()
            return True
    
    return False

def list_installed_applications():
    apps = []
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall") as key:
        for i in range(winreg.QueryInfoKey(key)[0]):
            subkey_name = winreg.EnumKey(key, i)
            with winreg.OpenKey(key, subkey_name) as subkey:
                try:
                    app_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    apps.append(app_name)
                except FileNotFoundError:
                    pass
    return apps

def open_application(app_name):
    try:
        subprocess.Popen([app_name], shell=True)
    except FileNotFoundError:
        print(f"Application '{app_name}' not found or could not be opened.")
    
if __name__ == "__main__":
    #Remove app and print
    taskbar_apps = get_apps_in_taskbar()

    if taskbar_apps:
        print("Applications in Taskbar:")
        for app_id, app_title in taskbar_apps:
            if len(app_title) > 0:
                print(f"ID: {app_id}, Title: {app_title}")

        app_to_close = int(input("Enter the ID of the application to close (or -1 to exit): "))
        if app_to_close == -1:
            print("Exiting.")
        else:
            close_app_by_id(app_to_close)
    else:
        print("No applications found in the taskbar.")

    app_name = input("Enter the name of the app to open: ")
    
    if open_app_by_name(app_name):
        print(f"Successfully opened '{app_name}'.")
    else:
        print(f"Could not find an app with the name '{app_name}'.")

    #Open app with name
    installed_apps = list_installed_applications()

    print("Installed Applications:")
    for app in installed_apps:
        print(app)

    app_to_open = input("Enter the name of the application to open: ")
    open_application(app_to_open)
