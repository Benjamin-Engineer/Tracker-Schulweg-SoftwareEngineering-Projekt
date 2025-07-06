import datetime
from planner import load_entries
from gps import tracker

is_recording = False
now = datetime.datetime.now().time()


def toggle_status(callback = None): # Button Funktion zum ändern des aufzeichen von Aktiv -> Inaktiv -> Aktiv ...
    global is_recording
    
    is_recording = not is_recording # Ändert den Status der variable is_recording zwischen "True" und "False"
    
    while is_recording:
        tracker()
    
    if callback:
        callback()
    
def automatic_start_stop():
    plan = load_entries()
    for eintrag in plan:
        von = datetime.datetime.strptime(eintrag["von"], "%H:%M").time() # Wandelt 'von' einträge des Planers in datetime um
        bis = datetime.datetime.strptime(eintrag["bis"], "%H:%M").time() # Wandelt 'bis' einträge des Planers in datetime um   
        
        if von <= now <= bis: # Überprüft ob der Zeitpunkt 'now' zwischen 'von' und 'bis' liegt
            if not is_recording: 
                toggle_status() #Start
        else:
            if is_recording:
                toggle_status() #Stop
