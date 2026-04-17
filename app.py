import random
import threading
import time

import pyautogui
from pynput import keyboard, mouse

IDLE_SECONDS = 30
POLL_INTERVAL = 0.5
SCROLL_DOWN = -6
SCROLL_UP = 4
CORNER_MARGIN = 50

_lock = threading.Lock()
_last_activity = time.monotonic()


def _mark_active():
    global _last_activity
    with _lock:
        _last_activity = time.monotonic()


def _on_mouse_move(_x, _y):
    _mark_active()


def _on_mouse_click(_x, _y, _button, _pressed):
    _mark_active()


def _on_mouse_scroll(_x, _y, _dx, _dy):
    _mark_active()


def _on_key_press(_key):
    _mark_active()


mouse.Listener(
    on_move=_on_mouse_move,
    on_click=_on_mouse_click,
    on_scroll=_on_mouse_scroll,
).start()

keyboard.Listener(on_press=_on_key_press).start()

while True:
    time.sleep(POLL_INTERVAL)
    with _lock:
        idle = time.monotonic() - _last_activity
    if idle < IDLE_SECONDS:
        continue
    w, h = pyautogui.size()
    pyautogui.moveTo(random.randint(CORNER_MARGIN, w - CORNER_MARGIN), random.randint(CORNER_MARGIN, h - CORNER_MARGIN))
    time.sleep(0.5)
    if random.random() < 0.5:
        pyautogui.scroll(SCROLL_DOWN)
    else:
        pyautogui.scroll(SCROLL_UP)
    _mark_active()
