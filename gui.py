import tkinter as tk
from tkinter import ttk, messagebox
import random
import logik

def zeige_rangliste(root):
    daten = logik.lade_ergebnisse()
    rang_fenster = tk.Toplevel(root)
    rang_fenster.title("Rangliste")
    rang_fenster.geometry("500x400")
    label = ttk.Label(rang_fenster, text="Rangliste", font=("Arial", 14, "bold"))
    label.pack(pady=10)
    if daten:
        for platz, eintrag in enumerate(daten, 1):
            eintrag_label = ttk.Label(
                rang_fenster,
                text=f"{platz}. {eintrag.get('name', 'Unbekannt')}: {eintrag.get('punkte', 0)} Punkte",
                font=("Arial", 12)
            )
            eintrag_label.pack(anchor="w", padx=30)
    else:
        leer_label = ttk.Label(rang_fenster, text="Noch keine Ergebnisse vorhanden.", font=("Arial", 12))
        leer_label.pack(pady=20)

def quiz_seite(root, ausgewaehlte_kategorien, ausgewaehlte_schwierigkeiten, spieler_name=None):
    fragen = logik.gefilterte_fragen(ausgewaehlte_kategorien, ausgewaehlte_schwierigkeiten)
    random.shuffle(fragen)
    aktuelle_frage = {"index": 0, "richtig": 0, "falsch": 0}

    def zeige_frage():
        for widget in root.winfo_children():
            widget.pack_forget()
        idx = aktuelle_frage["index"]
        if idx >= len(fragen):
            end_label = ttk.Label(
                root,
                text=f"Quiz beendet!\nRichtig: {aktuelle_frage['richtig']} | Falsch: {aktuelle_frage['falsch']}",
                font=("Arial", 16), anchor="center", justify="center"
            )
            end_label.pack(expand=True, pady=30)

            def quiz_neu_starten():
                aktuelle_frage["index"] = 0
                aktuelle_frage["richtig"] = 0
                aktuelle_frage["falsch"] = 0
                random.shuffle(fragen)
                zeige_frage()

            def ergebnis_speichern():
                logik.ergebnis_speichern(spieler_name, aktuelle_frage["richtig"])

            ttk.Button(root, text="Erneut Versuchen", command=quiz_neu_starten).pack(pady=5)
            ttk.Button(root, text="Neues Quiz", command=lambda: einstellungen_seite(root, [], spieler_name)).pack(pady=5)
            ttk.Button(root, text="Ergebnis Speichern", command=ergebnis_speichern).pack(pady=5)
            ttk.Button(root, text="Zum Hauptmenü", command=lambda: hauptfenster(root)).pack(pady=5)
            ttk.Button(root, text="Beenden", command=root.destroy).pack(pady=5)
            return

        frage = fragen[idx]
        ttk.Label(root, text=f"Frage {idx+1} von {len(fragen)}", font=("Arial", 12)).pack(pady=10)
        ttk.Label(root, text=frage["Frage"], font=("Arial", 14), wraplength=500).pack(pady=10)
        feedback_label = ttk.Label(root, text="", font=("Arial", 12))
        feedback_label.pack(pady=10)

        def antwort_geklickt(auswahl):
            for btn in antwort_buttons:
                btn.state(["disabled"])
            if auswahl == frage["RichtigeAntwort"]:
                aktuelle_frage["richtig"] += 1
                feedback_label.config(text="Richtig!", foreground="green")
            else:
                aktuelle_frage["falsch"] += 1
                richtige_antwort = frage["Antworten"][frage["RichtigeAntwort"]-1]
                feedback_label.config(text=f"Falsch! Richtige Antwort: {richtige_antwort}", foreground="red")
            next_btn.pack(pady=10)

        antwort_buttons = []
        for idx_a, antwort in enumerate(frage["Antworten"], 1):
            btn = ttk.Button(root, text=antwort, width=40, command=lambda a=idx_a: antwort_geklickt(a))
            btn.pack(pady=5)
            antwort_buttons.append(btn)

        def naechste_frage():
            next_btn.pack_forget()
            aktuelle_frage["index"] += 1
            zeige_frage()

        next_btn = ttk.Button(root, text="Nächste Frage", command=naechste_frage)
        # Wird erst nach Antwort angezeigt

    if len(fragen) == 0:
        for widget in root.winfo_children():
            widget.pack_forget()
        ttk.Label(root, text="Keine Fragen für diese Auswahl gefunden.", font=("Arial", 14)).pack(pady=30)
        return

    zeige_frage()

def einstellungen_seite(root, start_widgets, spieler_name=None):
    for widget in root.winfo_children():
        widget.pack_forget()
    label = ttk.Label(root, text="Wähle eine Kategorie", font=("Arial", 16))
    label.pack(pady=10)

    kategorien = ["PowerShell", "Virtualisierung", "VM-Konzepte", "Automatisierung"]
    var_dict = {}
    cb_frame = ttk.Frame(root)
    cb_frame.pack(pady=5)
    for idx, kategorie in enumerate(kategorien):
        var = tk.BooleanVar()
        cb = ttk.Checkbutton(cb_frame, text=kategorie, variable=var)
        cb.grid(row=0, column=idx, padx=5)
        var_dict[kategorie] = var

    def alle_auswaehlen():
        if all(var.get() for var in var_dict.values()):
            for var in var_dict.values():
                var.set(False)
        else:
            for var in var_dict.values():
                var.set(True)

    alle_button = ttk.Button(root, text="Alle Kategorien auswählen", command=alle_auswaehlen)
    alle_button.pack(pady=5)

    label2 = ttk.Label(root, text="Wähle einen Schwierigkeitsgrad", font=("Arial", 14))
    label2.pack(pady=10)

    schwierigkeiten = ["Anfänger", "Fortgeschritten"]
    schwierigkeit_vars = {}
    schwierigkeit_frame = ttk.Frame(root)
    schwierigkeit_frame.pack(pady=5)
    for idx, schwierig in enumerate(schwierigkeiten):
        var = tk.BooleanVar()
        cb = ttk.Checkbutton(schwierigkeit_frame, text=schwierig, variable=var)
        cb.grid(row=0, column=idx, padx=5)
        schwierigkeit_vars[schwierig] = var

    def alle_schwierigkeiten_auswaehlen():
        if all(var.get() for var in schwierigkeit_vars.values()):
            for var in schwierigkeit_vars.values():
                var.set(False)
        else:
            for var in schwierigkeit_vars.values():
                var.set(True)

    alle_schwierigkeiten_button = ttk.Button(root, text="Alle Schwierigkeitsgrade auswählen", command=alle_schwierigkeiten_auswaehlen)
    alle_schwierigkeiten_button.pack(pady=5)

    def quiz_starten():
        ausgewaehlte_kategorien = [k for k, v in var_dict.items() if v.get()]
        ausgewaehlte_schwierigkeiten = [s for s, v in schwierigkeit_vars.items() if v.get()]
        if not ausgewaehlte_kategorien or not ausgewaehlte_schwierigkeiten:
            messagebox.showwarning("Auswahl fehlt", "Bitte wähle mindestens eine Kategorie und einen Schwierigkeitsgrad aus!")
            return
        quiz_seite(root, ausgewaehlte_kategorien, ausgewaehlte_schwierigkeiten, spieler_name)

    quiz_start_button = ttk.Button(
        root,
        text="Quiz starten",
        command=quiz_starten
    )
    quiz_start_button.pack(pady=15)

    back_button = ttk.Button(
        root,
        text="Zurück",
        command=lambda: spieler_seite(root, start_widgets)
    )
    back_button.pack(pady=10)

    hauptmenue_button = ttk.Button(
        root,
        text="Zum Hauptmenü",
        command=lambda: hauptfenster(root)
    )
    hauptmenue_button.pack(pady=10)

def spieler_seite(root, start_widgets):
    for widget in root.winfo_children():
        widget.pack_forget()
    spieler_label = ttk.Label(root, text="Wie lautet dein Name?", font=("Arial", 14))
    spieler_label.pack(pady=10)
    name_var = tk.StringVar()
    name_entry = ttk.Entry(root, textvariable=name_var, font=("Arial", 12))
    name_entry.pack(pady=10)
    weiter_button = ttk.Button(
        root,
        text="Weiter",
        command=lambda: einstellungen_seite(root, start_widgets, name_var.get())
    )
    weiter_button.pack(pady=10)
    back_button = ttk.Button(
        root,
        text="Zurück",
        command=lambda: hauptfenster(root)
    )
    back_button.pack(pady=10)

def hauptfenster(root):
    for widget in root.winfo_children():
        widget.pack_forget()
    label = ttk.Label(root, text="Willkommen zum Modul 3 Quiz!", font=("Arial", 16))
    start_button = ttk.Button(root, text="Start")
    rang_button = ttk.Button(root, text="Rangliste", command=lambda: zeige_rangliste(root))
    beenden_button = ttk.Button(root, text="Beenden", command=root.destroy)
    label.pack(pady=30)
    start_button.pack(pady=10)
    rang_button.pack(pady=10)
    beenden_button.pack(pady=10)
    start_widgets = [label, start_button, rang_button, beenden_button]
    start_button.config(command=lambda: spieler_seite(root, start_widgets))