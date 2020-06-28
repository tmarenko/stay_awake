import time
import pyautogui
from datetime import datetime
from pynput import keyboard, mouse
from threading import Thread


pyautogui.FAILSAFE = False
MAX_NON_ACTIVE_TIME = 600  # in seconds
LAST_ACTIVITY_TIME = time.time()
LAST_MOUSE_POSITION = mouse.Controller().position


def activity_listener(*args):
    global LAST_ACTIVITY_TIME, LAST_MOUSE_POSITION
    LAST_ACTIVITY_TIME = time.time()
    if len(args) >= 2:
        LAST_MOUSE_POSITION = args[0], args[1]


def make_activity_thread():
    global LAST_ACTIVITY_TIME, LAST_MOUSE_POSITION
    while True:
        current_time = time.time()
        if current_time - LAST_ACTIVITY_TIME > MAX_NON_ACTIVE_TIME:
            print("Reached max non-activity time.")
            LAST_ACTIVITY_TIME = current_time
            restore_position = LAST_MOUSE_POSITION
            pyautogui.moveTo(0, 0)
            pyautogui.moveTo(*restore_position)
            pyautogui.press("ctrl")
            print(f"Movement made at {datetime.now().time()}")
        time.sleep(1)


keyboard_listener = keyboard.Listener(on_press=activity_listener)
mouse_listener = mouse.Listener(on_move=activity_listener, on_click=activity_listener, on_scroll=activity_listener)

activity_thread = Thread(target=make_activity_thread)

keyboard_listener.start() and mouse_listener.start()
activity_thread.start() and activity_thread.join()
