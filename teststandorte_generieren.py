import os

STANDORTE_FOLDER = "Standorte"

# Daten für die zu erstellenden Standortdateien
# Format: (Dateiname, [Zeile1, Zeile2, ...]).
standort_dateien_daten = [
    (
        "50.000000 7.000000.txt",
        [
            "50.000000 7.000000",
            "2023-10-27 12:00:00.000000"
        ]
    ),
    (
        "51.111111 8.111111.txt",
        [
            "51.111111 8.111111",
            "2023-10-27 10:00:00.000000"
        ]
    ),
    (
        "52.222222 9.222222.txt",
        [
            "Arbeit",
            "2023-10-26 09:00:00.000000"
        ]
    ),
    (
        "54.444444 11.444444.txt",
        [
            "Schule",
            "2023-10-25 07:00:00.000000"
        ]
    ),
    (
        "53.333333 10.333333.txt",
        [
            "Zuhause",
            "2023-10-24 18:00:00.000000"
        ]
    ),
    (
        "50.741705 7.065974.txt",
        [
            "Bushaltestelle",
            "2025-05-21 20:23:36+00.00"
        ]
    )
]

def erstelle_test_standortdateien():
    """
    Erstellt den Ordner STANDORTE_FOLDER (falls nicht vorhanden)
    und füllt ihn mit den oben definierten Test-Standortdateien.
    """
    try:
        if not os.path.exists(STANDORTE_FOLDER):
            os.makedirs(STANDORTE_FOLDER)
            print(f"Ordner '{STANDORTE_FOLDER}' wurde erstellt.")
        else:
            print(f"Ordner '{STANDORTE_FOLDER}' existiert bereits.")

        for dateiname, inhalt_zeilen in standort_dateien_daten:
            filepath = os.path.join(STANDORTE_FOLDER, dateiname)
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    for zeile in inhalt_zeilen:
                        f.write(zeile + "\n")
                print(f"Datei '{filepath}' wurde erfolgreich erstellt.")
            except IOError as e:
                print(f"Fehler beim Erstellen der Datei '{filepath}': {e}")

    except OSError as e:
        print(f"Fehler beim Erstellen des Ordners '{STANDORTE_FOLDER}': {e}")
    except Exception as e_general:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e_general}")

if __name__ == "__main__":
    erstelle_test_standortdateien()
    print("\nTest-Standortdateien wurden (versucht zu) erstellen.")
    print(f"Bitte überprüfen Sie den Inhalt des Ordners '{STANDORTE_FOLDER}'.")