
import os
import webbrowser
import subprocess
import pyautogui
import time
import platform

def open_notepad():
    """Opens the Notepad application."""
    try:
        subprocess.Popen(["notepad.exe"])
        return "Notepad opened."
    except Exception as e:
        return f"Failed to open Notepad: {e}"

def open_calculator():
    """Opens the Calculator."""
    try:
        subprocess.Popen("calc.exe")
        return "Calculator opened."
    except Exception as e:
        return f"Failed to open Calculator: {e}"

def google_search(query):
    """Searches Google for the given query."""
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Searched Google for {query}."

def type_text(text):
    """Types the specified text on the keyboard."""
    try:
        # Give user a moment to focus the field
        # time.sleep(1) 
        pyautogui.write(text, interval=0.05)
        return "Text typed."
    except Exception as e:
        return f"Typing failed: {e}"

def volume_control(action):
    """Controls volume: 'up', 'down', 'mute'."""
    try:
        if action == "up":
            pyautogui.press("volumeup")
            return "Volume increased."
        elif action == "down":
            pyautogui.press("volumedown")
            return "Volume decreased."
        elif action == "mute":
            pyautogui.press("volumemute")
            return "Volume muted/unmuted."
    except Exception as e:
        return f"Volume control failed: {e}"

def press_key(key):
    """Presses a specific key (e.g., 'enter', 'tab', 'esc', 'backspace')."""
    try:
        pyautogui.press(key)
        return f"Key '{key}' pressed."
    except Exception as e:
        return f"Failed to press key: {e}"

def hotkey(keys):
    """Performs a hotkey combination (e.g., 'ctrl+s', 'alt+f4'). Separated by '+'."""
    try:
        key_list = keys.split('+')
        # Unwrap list for pyautgui
        pyautogui.hotkey(*key_list)
        return f"Hotkey '{keys}' performed."
    except Exception as e:
        return f"Failed to perform hotkey: {e}"

def scroll(amount):
    """Scrolls the screen up (positive) or down (negative). Amount usually +/- 100 to 500."""
    try:
        pyautogui.scroll(int(amount))
        return f"Scrolled {'up' if int(amount) > 0 else 'down'} by {abs(int(amount))}."
    except Exception as e:
        return f"Scroll failed: {e}"

def mouse_click(button="left"):
    """Clicks the mouse. button can be 'left' or 'right'."""
    try:
        pyautogui.click(button=button)
        return f"{button.capitalize()} clicked."
    except Exception as e:
        return f"Click failed: {e}"

def mouse_move(direction, pixels=100):
    """Moves mouse 'up', 'down', 'left', 'right' by a number of pixels."""
    try:
        x, y = 0, 0
        if direction == "up": y = -int(pixels)
        elif direction == "down": y = int(pixels)
        elif direction == "left": x = -int(pixels)
        elif direction == "right": x = int(pixels)
        
        pyautogui.move(x, y)
        return f"Moved mouse {direction} by {pixels} pixels."
    except Exception as e:
        return f"Move failed: {e}"

def get_system_info():
    """Returns basic system info."""
    return f"System: {platform.system()} {platform.release()}"

# Dictionary of available tools for the LLM to inspect (if doing manually)
# But we will pass these functions directly to Gemini's tool config.
tools_list = [open_notepad, open_calculator, google_search, type_text, volume_control, get_system_info, press_key, hotkey, scroll, mouse_click, mouse_move]
