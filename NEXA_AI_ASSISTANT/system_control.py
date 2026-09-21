import os
import subprocess
import psutil
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
from livekit.agents import function_tool


# ============ VOLUME ============
def _get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

@function_tool()
async def set_volume(level: int) -> str:
    """Set system volume to a specific level (0-100)."""
    volume = _get_volume_interface()
    volume.SetMasterVolumeLevelScalar(max(0, min(100, level)) / 100, None)
    return f"Volume set to {level}%"

@function_tool()
async def volume_up(step: int = 10) -> str:
    """Increase system volume by a step (default 10%)."""
    volume = _get_volume_interface()
    current = volume.GetMasterVolumeLevelScalar() * 100
    new_level = min(100, current + step)
    volume.SetMasterVolumeLevelScalar(new_level / 100, None)
    return f"Volume increased to {int(new_level)}%"

@function_tool()
async def volume_down(step: int = 10) -> str:
    """Decrease system volume by a step (default 10%)."""
    volume = _get_volume_interface()
    current = volume.GetMasterVolumeLevelScalar() * 100
    new_level = max(0, current - step)
    volume.SetMasterVolumeLevelScalar(new_level / 100, None)
    return f"Volume decreased to {int(new_level)}%"

@function_tool()
async def mute_volume() -> str:
    """Mute or unmute system volume."""
    volume = _get_volume_interface()
    current_mute = volume.GetMute()
    volume.SetMute(not current_mute, None)
    return "Muted" if not current_mute else "Unmuted"


# ============ BRIGHTNESS ============
@function_tool()
async def set_brightness(level: int) -> str:
    """Set screen brightness to a specific level (0-100)."""
    sbc.set_brightness(max(0, min(100, level)))
    return f"Brightness set to {level}%"

@function_tool()
async def brightness_up(step: int = 10) -> str:
    """Increase screen brightness by a step (default 10%)."""
    current = sbc.get_brightness()[0]
    new_level = min(100, current + step)
    sbc.set_brightness(new_level)
    return f"Brightness increased to {new_level}%"

@function_tool()
async def brightness_down(step: int = 10) -> str:
    """Decrease screen brightness by a step (default 10%)."""
    current = sbc.get_brightness()[0]
    new_level = max(0, current - step)
    sbc.set_brightness(new_level)
    return f"Brightness decreased to {new_level}%"


# ============ MEDIA CONTROL (YouTube/Spotify/any media player) ============
@function_tool()
async def media_play_pause() -> str:
    """Play or pause currently playing media (YouTube, Spotify, etc)."""
    pyautogui.press('playpause')
    return "Toggled play/pause"

@function_tool()
async def media_next_track() -> str:
    """Skip to next track/video."""
    pyautogui.press('nexttrack')
    return "Skipped to next track"

@function_tool()
async def media_previous_track() -> str:
    """Go to previous track/video."""
    pyautogui.press('prevtrack')
    return "Went to previous track"

@function_tool()
async def youtube_skip_ad() -> str:
    """Attempt to skip a YouTube ad (works when ad skip button is focused)."""
    pyautogui.press('tab')
    pyautogui.press('enter')
    return "Attempted to skip ad"


# ============ POWER CONTROL ============
@function_tool()
async def shutdown_pc(delay: int = 10) -> str:
    """Shut down the laptop after a delay in seconds (default 10)."""
    os.system(f"shutdown /s /t {delay}")
    return f"Shutting down in {delay} seconds"

@function_tool()
async def cancel_shutdown() -> str:
    """Cancel a pending shutdown or restart."""
    os.system("shutdown /a")
    return "Shutdown/restart cancelled"

@function_tool()
async def restart_pc(delay: int = 10) -> str:
    """Restart the laptop after a delay in seconds (default 10)."""
    os.system(f"shutdown /r /t {delay}")
    return f"Restarting in {delay} seconds"

@function_tool()
async def sleep_pc() -> str:
    """Put the laptop to sleep."""
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    return "Going to sleep"

@function_tool()
async def lock_pc() -> str:
    """Lock the laptop screen."""
    os.system("rundll32.exe user32.dll,LockWorkStation")
    return "Screen locked"


# ============ SYSTEM INFO ============
@function_tool()
async def get_battery_status() -> str:
    """Get current battery percentage and charging status."""
    battery = psutil.sensors_battery()
    if battery is None:
        return "No battery detected (desktop PC?)"
    plugged = "charging" if battery.power_plugged else "not charging"
    return f"Battery at {battery.percent}%, {plugged}"

@function_tool()
async def get_cpu_ram_usage() -> str:
    """Get current CPU and RAM usage percentage."""
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    return f"CPU usage: {cpu}%, RAM usage: {ram}%"

@function_tool()
async def get_disk_space() -> str:
    """Get free and total disk space on C drive."""
    disk = psutil.disk_usage('C:\\')
    free_gb = disk.free / (1024**3)
    total_gb = disk.total / (1024**3)
    return f"Disk space: {free_gb:.1f} GB free out of {total_gb:.1f} GB total"


# ============ WIFI ============
@function_tool()
async def wifi_toggle_on() -> str:
    """Turn WiFi on."""
    subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "enabled"], shell=True)
    return "WiFi turned on"

@function_tool()
async def wifi_toggle_off() -> str:
    """Turn WiFi off."""
    subprocess.run(["netsh", "interface", "set", "interface", "Wi-Fi", "disabled"], shell=True)
    return "WiFi turned off"