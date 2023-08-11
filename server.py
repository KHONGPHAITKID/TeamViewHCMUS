import socket
import pyautogui
from PIL import ImageGrab
import io
import os
import tkinter as tk

HOST = "127.0.0.1"
PORT = 65431

def send_keystroke(key):
    # Add your implementation to send keystroke command here
    print(f"Sending keystroke: {key}")

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

def app_running_check(app_name):
    print(f"Checking if {app_name} is running...")

def process_running_check(process_name):
    print(f"Checking if {process_name} is running...")

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

def fix_registry():
    print("Fixing the registry...")
    

def handle_command(client_socket, command):
    parts = command.split()
    if parts[0] == "SendKeyStroke":
        send_keystroke(parts[0])
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

if __name__ == "__main__":
    start_server()

# if command == "ProcessRunning":
#     # process_output = subprocess.check_output(["tasklist"])
#     # connection.sendall(process_output)
#     print("ProcessRunning!")
# elif command == "AppRunning":
#     # app_output = subprocess.check_output(["your_command_to_check_app_running"])
#     # connection.sendall(app_output)
#     print("AppRunning!")
# elif command == "SendKeyStroke":
#     print("KeyStroke!")
# elif command == "ShutDown":
#     print("ShutDown!")
# elif command == "TakeScreenShot":
#     print("TakeScreenShot!")
# elif command == "FixRegistry":
#     print("FixRegistry!")