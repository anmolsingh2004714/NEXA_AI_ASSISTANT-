import os

def shutdown_pc(delay: int = 5):
    os.system(f"shutdown /s /t {delay}")
    return f"Shutting down in {delay} seconds"

def cancel_shutdown():
    os.system("shutdown /a")
    return "Shutdown cancelled"

def restart_pc(delay: int = 5):
    os.system(f"shutdown /r /t {delay}")
    return f"Restarting in {delay} seconds"