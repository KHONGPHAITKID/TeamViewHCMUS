import tkinter as tk
import tasks

def QuitFunction():
    print("Program Close!")
    root.quit()  # Close the program

def submit_button_click():
    user_input = input_textbox.get()
    print("User input:", user_input)
    input_textbox.delete(0, tk.END)

def on_enter_key(event):
    submit_button_click()

EnterFirstTime = False
root = tk.Tk()
root.geometry("650x550")

inputMessage = tk.StringVar()
inputMessage.set("")

input_textbox = tk.Entry(root, width=75, textvariable=inputMessage)
input_textbox.place(x=35, y=80)
input_textbox.bind("<Return>", on_enter_key)

SubmitButton = tk.Button(root, text="Submit", width=14, command=submit_button_click)
SubmitButton.place(x=500, y = 75)


ProcessRunningButton = tk.Button(
    root,
    text="Process\nrunning",
    width=10,
    height=16,
    font=("Helvetica", 14, "bold"),
    relief=tk.RAISED,
    bd=3,
    command=tasks.process,
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
    command=tasks.Running,
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
    command=tasks.send_keystroke,
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
    command=tasks.ShutDown,
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
    command=tasks.take_screenshot,
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
    command=tasks.Fixing,
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
    command=QuitFunction,
    highlightthickness=2,
)
QuitButton.place(x=522, y=399)

root.mainloop()