import tkinter as tk
from tkinter import messagebox
import socket
import cv2
import pyautogui
from time import time
import numpy as np
import os
from threading import Thread
from PIL import Image
import io

# "127.0.0.1"
host = "127.0.0.1"
port = 65431
timeout = 3
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
isConnected = False

def Quit():
    print("Program Close!")
    isConnected = False
    client_socket.close()
    root.quit()

def connect(user_input):
    global isConnected
    try:
        client_socket.settimeout(timeout)
        client_socket.connect((host, port))
        isConnected = True
        print("Connection successful.")
        messagebox.showinfo("Success", "Connection successful!")
    except socket.timeout:
        print("Connection timed out!")
        messagebox.showinfo("Error", "Connection timed out!")
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        print(f"Connection failed: {e}")
        messagebox.showinfo("Error", "Connection failed!")

def send_command(command):
    if (isConnected == False):
        messagebox.showinfo("Error", "Connection failed!")
        return
    client_socket.sendall(command.encode())
    print(command)
    parts = command.split()
    if parts[0] == "SendKeyStroke":
        Handle_send_keystroke()
    elif parts[0] == "TakeScreenShot":
        Handle_take_screenshot()
    elif parts[0] == "AppRunningChecking":
        Handle_app_running_check()
    elif parts[0] == "ProcessRunningChecking":
        Handle_process_running_check()
    elif parts[0] == "ShutDownComputer":
        Handle_shutdown_computer()
    elif parts[0] == "FixRegistry":
        Handle_fix_registry()

def submit_button_click(event=None):
    user_input = InputTextbox.get()
    print("User input:", user_input)
    connect(user_input)
    InputTextbox.delete(0, tk.END)


# def FixRegistry():
#     send_command("FixRegistry")
#     print("Fixing Registry...")

def Handle_send_keystroke():
    pass

def Handle_take_screenshot():
    file = open("received_image.png", "wb")
    isBreak = False;
    while True:
        if (isBreak):
            break
        image_chunk = client_socket.recv(2048)
        # print(f"{len(image_chunk)} writing..")
        if (len(image_chunk) < 2048):
            isBreak = True
        if (len(image_chunk) == 0):
            break
        file.write(image_chunk)
    file.close()
    print("picture received")

def Handle_app_running_check():
    pass

def Handle_process_running_check():
    pass

def Handle_shutdown_computer():
    pass

def Handle_fix_registry():
    pass




# Building the Client UI
root = tk.Tk()
root.geometry("650x550")
root.resizable(False, False)

InputMessage = tk.StringVar()
InputMessage.set("")

InputTextbox = tk.Entry(root, width=50, textvariable=InputMessage)
InputTextbox.place(x=35, y=80)
InputTextbox.bind("<Return>", submit_button_click)

SubmitButton = tk.Button(root, text="Connect", width=10, command=submit_button_click)
SubmitButton.place(x=500, y = 75)

ProcessRunningButton = tk.Button(
    root,
    text="Process\nrunning",
    width=10,
    height=16,
    font=("Helvetica", 14, "bold"),
    relief=tk.RAISED,
    bd=3,
    command=lambda: send_command("ProcessRunning"),
    highlightthickness=2,
)
ProcessRunningButton.place(x=35, y=120)

AppRunningButton = tk.Button(
    root,
    text="App running",
    width=20,
    height=4,
    font=("Helvetica", 14, "bold"),
    relief=tk.RAISED,
    bd=3,
    command=lambda: send_command("AppRunning"),
    highlightthickness=2,
)
AppRunningButton.place(x=185, y=120)

KeyStrokeButton = tk.Button(
    root,
    text="Keystroke",
    width=12,
    height=11,
    font=("Helvetica", 14, "bold"),
    relief=tk.RAISED,
    bd=3,
    command=lambda: send_command("SendKeyStroke"),
    highlightthickness=2,
)
KeyStrokeButton.place(x=450, y=120)

ShutDownButton = tk.Button(
    root,
    text="Shut down",
    width=8,
    height=5,
    font=("Helvetica", 15, "bold"),
    relief=tk.RAISED,
    bd=3,
    command=lambda: send_command("ShutDown"),
    highlightthickness=2,
)
ShutDownButton.place(x=185, y=241)

ScreenShotButton = tk.Button(
    root,
    text="ScreenShot",
    width=10,
    height=5,
    font=("Helvetica", 15, "bold"),
    relief=tk.RAISED,
    bd=3,
    command=lambda: send_command("TakeScreenShot"),
    highlightthickness=2,
)
ScreenShotButton.place(x=304, y=241)

FixRegistryButton = tk.Button(
    root,
    text="Fixing Registry",
    width=26,
    height=3,
    font=("Helvetica", 15, "bold"),
    relief=tk.RAISED,
    bd=3,
    command=lambda: send_command("FixRegistry"),
    highlightthickness=2,
)
FixRegistryButton.place(x=185, y=399)

QuitButton = tk.Button(
    root,
    text="Quit",
    width=6,
    height=3,
    font=("Helvetica", 15, "bold"),
    relief=tk.RAISED,
    bd=3,
    command=Quit,
    highlightthickness=2,
)
QuitButton.place(x=522, y=399)

# Example usage
if __name__ == "__main__":
    root.mainloop()

    
# Function:
# def TakeScreenShot():
#     send_command("TakeScreenShot")
#     filename = "pic1.png"
#     # screenshot = pyautogui.screenshot()
#     # screenshot.save(filename)
#     print("Taken picture...")

# def ShutDown(countdown_seconds=10):
#     send_command("ShutDown")
#     print("ShuttingDown")
    # print(f"Initiating system shutdown in {countdown_seconds} seconds...")

    # # Create a countdown window
    # root = tk.Tk()
    # root.title("Shutdown Countdown")
    # root.geometry("300x100")
    
    # label = tk.Label(root, text="System will shut down in", font=("Helvetica", 14))
    # label.pack(pady=20)

    # time_left = countdown_seconds
    # label_time = tk.Label(root, text=str(time_left), font=("Helvetica", 30))
    # label_time.pack()

    # def update_time():
    #     nonlocal time_left
    #     label_time.config(text=str(time_left))
    #     if time_left > 0:
    #         time_left -= 1
    #         root.after(1000, update_time)
    #     else:
    #         root.destroy()
    #         print("Shutting down the system...")
    #         os.system("sudo shutdown -h now")

    # root.after(1000, update_time)
    # root.mainloop()