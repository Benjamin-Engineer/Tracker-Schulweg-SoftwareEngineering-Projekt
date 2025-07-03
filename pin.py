import os #Importiert OS-Bibliothek für das Arbeiten mit Dateisystemen

PIN_FILE = "pin.txt"

def default_pin(): # Setzt die Standard PIN zu 
    if not os.path.exists(PIN_FILE):
        with open(PIN_FILE, "w") as f:
            f.write("000000") # Legt standard pin auf "000000"

def get_pin(): # Lädt die PIN aus der Datei
    with open(PIN_FILE, "r") as f:
        f_contents = f.read().strip()
        return f_contents

def check_pin(entered_pin): # Vergleicht eingegebene PIN mit gespeicherter PIN
    default_pin()
    return entered_pin == get_pin()

def set_pin(new_pin): # Setzt neue PIN über das eingabe fenster
    with open(PIN_FILE, "w") as f:
        f.write(new_pin)

def change_pin(alte_pin, new_pin, confirm_pin): # Ändert die PIN
    default_pin()
    if check_pin(alte_pin):
        if new_pin == confirm_pin: 
            if new_pin.isdigit() or len(new_pin) < 6:
                set_pin(new_pin) #speichern der neuen pin und überschreiben der alten
                print("PIN wurde erfolgreich geändert.")
                return True
            else: # Kriterien wurden nicht erfüllt
                print("PIN erfüllt nicht die Kriterien")
                return False
        else: # confirm_pin != new_pin
            print("Pin stimmt nicht überein")
            return False
    else: # falsche PIN zum überprüfen eingegeben.
        print("PIN ist falsch")
        return False

#change_pin(input("ALte PIN: "), input("Neue Pin: "), input("Confirm PIN: "))