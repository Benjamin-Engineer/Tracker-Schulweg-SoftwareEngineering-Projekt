from datetime import datetime
from dateifunktionen import gps_json_write #Custom Import. Kann kaputtgehen wenn die Routendatei umbenannt wird


daten = ["50.74271683333333 7.0670345",
"2025-05-21 20:04:28+00.00",
"50.74271683333333 7.0670345",
"2025-05-21 20:04:29+00.00",
"59.7427125 7.067018333333333",
"2025-05-21 20:04:30+00.00",
"50.7427095 7.667001",
"2025-05-21 20:04:31+00.00",
"50.74271066666667 7.0669935",
"2025-05-21 20:04:32+00.00",
"50.74270766666667 7.066976833333333",
"2025-05-21 20:04:33+00.00"]

def gps_test(daten):
    i = 0
    for lines in daten:
        print(i, lines)
        i+=1


# Gibt die Liste der Daten über print() aus
gps_test(daten)


# Überordner der Routendatei
# Wenn der Ordner nicht existiert, wird er erstellt
parent_folder = "2001-01-01"
# Fügt die Koordinaten "50.74271683333333 7.0670345" unter der aktuellen Systemzeit zur Route in der Datei 11-11-11.json hinzu
# Wenn es die Datei 11-11-11.json nicht gibt, wird eine erstellt
gps_json_write(
    daten[0],
    datetime.now().isoformat(),
    "11-11-11.json",
    folder=parent_folder
)