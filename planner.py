import os #Importiert OS-Bibliothek für das Arbeiten mit Dateisystemen
import json
from datetime import datetime

PLANNER_FILE = "planner.json"


def load_entries(): # Lädt daten der JSON-File
    if not os.path.exists(PLANNER_FILE):
        return [] # Falls keine file existiert, wird leere liste zurückgegeben
    with open(PLANNER_FILE, "r") as f:
        return json.load(f)
    
def save_entries(start, end, callback = None):
    entries = load_entries()
    
    entry = {
        "von": start,  
        "bis": end
        }
    
    entries.append(entry) # Erweiter liste um neuen eintrag
    
    entries.sort(key=lambda entry:entry["von"]) # Sortiert daten Chronologisch anhand "von"
    
    
    # speichern der Liste zurück in die Datei
    with open(PLANNER_FILE, "w") as f:
        json.dump(entries, f, indent=2)

    if callback:
        callback()


        
def show_planner_entries():
    for entry in load_entries():
        entry.get("von")
        print(
            f"Von: {entry['von']} Bis: {entry['bis']}") #"Abändern mit tk-inter tabelle für visualisierung"
    