from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

def set_volume(level: int):
    """level 0-100"""
    volume = get_volume_interface()
    volume.SetMasterVolumeLevelScalar(level / 100, None)
    return f"Volume set to {level}%"

def volume_up(step: int = 10):
    volume = get_volume_interface()
    current = volume.GetMasterVolumeLevelScalar() * 100
    new_level = min(100, current + step)
    volume.SetMasterVolumeLevelScalar(new_level / 100, None)
    return f"Volume increased to {int(new_level)}%"

def volume_down(step: int = 10):
    volume = get_volume_interface()
    current = volume.GetMasterVolumeLevelScalar() * 100
    new_level = max(0, current - step)
    volume.SetMasterVolumeLevelScalar(new_level / 100, None)
    return f"Volume decreased to {int(new_level)}%"