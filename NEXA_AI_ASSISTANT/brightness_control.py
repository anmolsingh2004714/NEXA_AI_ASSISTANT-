import screen_brightness_control as sbc

def set_brightness(level: int):
    """level 0-100"""
    sbc.set_brightness(level)
    return f"Brightness set to {level}%"

def brightness_up(step: int = 10):
    current = sbc.get_brightness()[0]
    new_level = min(100, current + step)
    sbc.set_brightness(new_level)
    return f"Brightness increased to {new_level}%"

def brightness_down(step: int = 10):
    current = sbc.get_brightness()[0]
    new_level = max(0, current - step)
    sbc.set_brightness(new_level)
    return f"Brightness decreased to {new_level}%"