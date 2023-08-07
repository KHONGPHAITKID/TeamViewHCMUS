import cv2
import pyautogui
from time import time
import numpy as np

def send_keystroke():
    key = input("Enter the keystroke to send: ")
    print(f"Sending Keystroke: {key}")

def take_screenshot():
    filename = "pic1.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    print("Taken picture...")

def screenRecord():
    screen_width, screen_height = pyautogui.size()
    mon = (0, 0, screen_width, screen_height)

    while 1:
        begin_time = time()
        screenshot = pyautogui.screenshot(region=mon)
        img_bgr = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        cv2.imshow('test', img_bgr)
        print('This frame takes {} seconds.'.format(time() - begin_time))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

def Running():
    print("Running...")
    pass

def process():
    print("Processing...")
    pass

def ShutDown():
    print("Initiating system shutdown...")
    os.system("shutdown /s /t 0")

def FixRegistry():
    print("Fixing Registry...")
    pass