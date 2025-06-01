is_recording = False

def toggle_status():
    global is_recording
    
    is_recording = not is_recording # Ändert den Status der variable is_recording zwischen "True" und "False"
    print(is_recording)
    
toggle_status()