# import cv2
# import pyautogui
# from time import time
# import numpy as np
# import os
# import tkinter as tk

# def send_keystroke():
#     send_command("process_running")
#     print("Sending Keystroke: ")

# def take_screenshot():
#     filename = "pic1.png"
#     screenshot = pyautogui.screenshot()
#     screenshot.save(filename)
#     print("Taken picture...")

# def screenRecord():
#     screen_width, screen_height = pyautogui.size()
#     mon = (0, 0, screen_width, screen_height)

#     while 1:
#         begin_time = time()
#         screenshot = pyautogui.screenshot(region=mon)
#         img_bgr = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
#         cv2.imshow('test', img_bgr)
#         print('This frame takes {} seconds.'.format(time() - begin_time))
#         if cv2.waitKey(25) & 0xFF == ord('q'):
#             cv2.destroyAllWindows()
#             break

# def Running():
#     print("Running...")
#     pass

# def process():
#     print("Processing...")
#     pass

# def ShutDown(countdown_seconds=10):
#     print(f"Initiating system shutdown in {countdown_seconds} seconds...")

#     # Create a countdown window
#     root = tk.Tk()
#     root.title("Shutdown Countdown")
#     root.geometry("300x100")
    
#     label = tk.Label(root, text="System will shut down in", font=("Helvetica", 14))
#     label.pack(pady=20)

#     time_left = countdown_seconds
#     label_time = tk.Label(root, text=str(time_left), font=("Helvetica", 30))
#     label_time.pack()

#     def update_time():
#         nonlocal time_left
#         label_time.config(text=str(time_left))
#         if time_left > 0:
#             time_left -= 1
#             root.after(1000, update_time)
#         else:
#             root.destroy()
#             print("Shutting down the system...")
#             os.system("sudo shutdown -h now")

#     root.after(1000, update_time)
#     root.mainloop()

# def FixRegistry():
#     print("Fixing Registry...")
#     pass