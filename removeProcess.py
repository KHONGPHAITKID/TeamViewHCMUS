import socket
import psutil
import subprocess
import winreg

def terminate_process(process_name):
    isFlag = False
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if process.info['name'] == process_name:
            try:
                isFlag = True
                psutil.Process(process.info['pid']).terminate()
            except psutil.NoSuchProcess:
                return f"Process {process_name} not found"
            except psutil.AccessDenied:
                return f"Access denied to terminate {process_name}"
    if isFlag == False:
        print('No proccess with that name.')
    else:
        print('Process killed.')

def terminate_processwithID(process_ID):
    isFlag = False
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if process.info['pid'] == process_ID:
            try:
                isFlag = True
                psutil.Process(process.info['pid']).terminate()
            except psutil.NoSuchProcess:
                return f"Process {process_ID} not found"
            except psutil.AccessDenied:
                return f"Access denied to terminate {process_ID}"
    if isFlag == False:
        print('No proccess with that name.')
    else:
        print('Process killed.')

def printProcess():
    for process in psutil.process_iter(attrs=['pid','name']):
        print(f"Name: {process.info['name']}, ID: {process.info['pid']}")

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

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 65431))
    server.listen(1)
    client_socket, client_address = server.accept()
    process_name = client_socket.recv(1024).decode()
    response = terminate_process(process_name)
    client_socket.send(response.encode())

if __name__ == "__main__":
    #Remove process and print
    printProcess()
    terminate_process("chrome.exe")
    terminate_processwithID(23252)

    #Open process with name
    installed_apps = list_installed_applications()
    process_to_open = input("Enter the name of the process to open: ")
    open_application(process_to_open)