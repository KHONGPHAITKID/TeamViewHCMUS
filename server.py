import socket
import pyautogui
from PIL import ImageGrab
import io

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

def app_running_check(app_name):
    print(f"Checking if {app_name} is running...")

def process_running_check(process_name):
    print(f"Checking if {process_name} is running...")

def shutdown_computer():
    print("Shutting down the computer...")

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
        shutdown_computer()
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