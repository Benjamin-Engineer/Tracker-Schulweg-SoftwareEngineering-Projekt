import os #Importiert OS-Bibliothek für das Arbeiten mit Dateisystemen

PIN_FILE = "pin.txt"

def default_pin(): # Setzt die Standard PIN zu 
    if not os.path.exists(PIN_FILE):
        with open(PIN_FILE, "w") as f:
            f.write("000000") # Legt standard pin auf "000000"
            
def get_pin(): # Lädt die PIN aus der Datei
    with open(PIN_FILE, "r") as f:
        f_contents = f.read()
        return f_contents
        
def check_pin(): # Vergleicht eingegebene PIN mit gespeicherter PIN
    entered_pin = input("PIN: ")
    print(entered_pin)
    print(get_pin())
    return entered_pin == get_pin()

def set_pin(new_pin): # Setzt neue PIN über das eingabe fenster
    with open(PIN_FILE, "w") as f:
        f.write(new_pin)
        
def change_pin(): # Ändert die PIN
    if not check_pin():
        print("Falsche PIN")
        return

    
    new_pin = input("Neue PIN: ");
    confirm = input("Bestätigen: ");
    
    if new_pin != confirm:
        print("Pin stimmt nicht überein")
        return
    if not new_pin.isdigit() or len(new_pin) < 6:
        print("PIN erfüllt nicht die Kriterien")
        return
    set_pin(new_pin)
    print("Ihre PIN wurde erfolgreich geändert.")
    
#default_pin()
#change_pin()
#get_pin()
#check_pin()