

import json
import os

def lade_fragen(dateipfad="fragen.json"):
    with open(dateipfad, "r", encoding="utf-8") as f:
        return json.load(f)

def gefilterte_fragen(kategorien, schwierigkeiten):
    fragen = lade_fragen()
    return [
        f for f in fragen
        if f["Kategorie"] in kategorien and f["Schwierigkeitsgrad"] in schwierigkeiten
    ]

def lade_ergebnisse(dateipfad="ergebnisse.json"):
    if os.path.exists(dateipfad):
        try:
            with open(dateipfad, "r", encoding="utf-8") as f:
                daten = json.load(f)
        except Exception:
            daten = []
    else:
        daten = []
    daten.sort(key=lambda x: x.get("punkte", 0), reverse=True)
    return daten

def ergebnis_speichern(name, punkte, dateipfad="ergebnisse.json"):
    daten = lade_ergebnisse(dateipfad)
    daten.append({"name": name if name else "Unbekannt", "punkte": punkte})
    with open(dateipfad, "w", encoding="utf-8") as f:
        json.dump(daten, f, ensure_ascii=False, indent=2)