import pyautogui
import time

def youtube_play_pause():
    pyautogui.press('k')  # YouTube shortcut: Play/Pause
    return "Toggled play/pause"

def youtube_skip_ad():
    """Skips ad if skip button is available (simulates clicking skip)"""
    # YouTube ad skip button click ka exact position screen pe alag hota hai,
    # isliye keyboard shortcut zyada reliable hai agar available ho
    pyautogui.press('tab')  # focus move
    pyautogui.press('enter')  # try click on skip button
    return "Attempted to skip ad"

def youtube_next_video():
    pyautogui.hotkey('shift', 'n')  # YouTube shortcut: Next video (playlist mein)
    return "Playing next video"

def youtube_fullscreen():
    pyautogui.press('f')
    return "Toggled fullscreen"

def youtube_mute():
    pyautogui.press('m')
    return "Toggled mute"