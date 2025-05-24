# Tracker-Schulweg-SoftwareEngineering-Projekt
Repository für das Projekt im Modul Grundlagen des Software Engineering über ein Tracker für den Schulweg von Schülern

pin.py 
    Erstellt eine standard pin für das Sicherheitsverfahren über default_pin()
    Zieht sich die vorhandene PIN aus der pin.txt datei über get_pin()
    Vergeleicht eingegebene PIN mit vorhandener pin, über check_pin(), diese ruft get_pin() auf
    Setzt einen neuen PIN in der pin.txt Datei und überschreibt den alten, mit set_pin() hierfür wird die Variable new_pin benötigt
    Ändert die Alte pin mit einer neuen pin ab über change_pin()
        hierfür wird eine Abfrage des Alten PIN's über check_pin() getätigt, sobald dieser korrekt ist wird die eingabe eines Neuen pins mit dessen Confirmation ermöglicht. Stimmen beide überein und die Kriterien für den PIN sind erfüllt (nur Nummern und mindestens 6 zeichen), wird die PIN über set_pin() gespeichert und die Alte überschrieben.