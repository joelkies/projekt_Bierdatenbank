import tkinter as tk
from tkinter import ttk, messagebox

# Funktionen aus anderen Dateien Importieren
from login import login, registrieren
from nutzer import hole_alle_nutzer, nutzer_loeschen, rolle_aendern, nutzer_suchen, nutzer_hinzufuegen
from brauereien import hole_alle_brauereien, brauerei_hinzufuegen, brauerei_loeschen
from biere import hole_alle_biere, bier_hinzufuegen, bier_loeschen, hole_brauereien_dropdown, suche_biere

#Hauptfenster der App
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.nutzer_id = None  
        self.title("Bierdatenbank")
        self.geometry("900x600")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        # Alle Seiten der App (Frames)
        for F in (
            LoginSeite, AdminMenue, GastMenue,
            NutzerVerwaltung, NutzerHinzufuegen, NutzerBearbeiten, NutzerSuchen,
            BrauereienVerwaltung, BrauereiHinzufuegen,
            BiereVerwaltung, BierHinzufuegen  # 👈 das ist neu!
        ):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginSeite)

    def show_frame(self, seite):
        frame = self.frames[seite]
        frame.tkraise()

# Login-Seite mit Eingabe von Nutzername und Passwort
class LoginSeite(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Benutzername").pack()
        self.e_user = tk.Entry(self)
        self.e_user.pack()

        tk.Label(self, text="Passwort").pack()
        self.e_pw = tk.Entry(self, show="*")
        self.e_pw.pack()

        tk.Button(self, text="Login", command=self.login).pack(pady=5)
        tk.Button(self, text="Registrieren", command=self.registrieren).pack()

    def login(self):
        # Login-Logik
        benutzer = self.e_user.get()
        pw = self.e_pw.get()
        nutzer_info = login(benutzer, pw)  # ruft Login-Funktion auf

        if not nutzer_info:
            return  # kein Zugriff bei falschen Daten

        nutzer_id, rolle = nutzer_info
        self.controller.nutzer_id = nutzer_id  # 👈 

        if rolle == 1:
            self.controller.show_frame(AdminMenue)
        elif rolle == 2:
            self.controller.show_frame(GastMenue)
    # Popup für neue Registrierung
    def registrieren(self):
        reg_win = tk.Toplevel(self)
        reg_win.title("Registrieren")
        reg_win.geometry("400x300")

        tk.Label(reg_win, text="Benutzername").pack()
        e_name = tk.Entry(reg_win)
        e_name.pack()

        tk.Label(reg_win, text="Passwort").pack()
        e_pw = tk.Entry(reg_win, show="*")
        e_pw.pack()

        def speichern():
            registrieren(e_name.get(), e_pw.get())
            reg_win.destroy()

        tk.Button(reg_win, text="Registrieren", command=speichern).pack(pady=10)

# Admin-Menü nach erfolgreichem Admin-Login

class AdminMenue(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Admin-Menü", font=("Arial", 16)).pack(pady=10)
        # Navigation zu verschiedenen Verwaltungsbereichen
        tk.Button(self, text="Nutzer verwalten", command=lambda: controller.show_frame(NutzerVerwaltung)).pack(pady=5)
        tk.Button(self, text="Brauereien verwalten", command=lambda: controller.show_frame(BrauereienVerwaltung)).pack(pady=5)
        tk.Button(self, text="Biere verwalten", command=lambda: controller.show_frame(BiereVerwaltung)).pack(pady=5)
        tk.Button(self, text="Logout", command=lambda: controller.show_frame(LoginSeite)).pack(pady=20)

# Nutzerverwaltung zeigt Tabelle aller Nutzer und bietet Zugriff auf Unterfunktionen

class NutzerVerwaltung(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Nutzerverwaltung", font=("Arial", 16)).pack(pady=10)

        # Treeview (Tabelle)
        spalten = ("ID", "Benutzername", "Rolle")
        self.tree = ttk.Treeview(self, columns=spalten, show="headings")
        for spalte in spalten:
            self.tree.heading(spalte, text=spalte)
            self.tree.column(spalte, anchor="center", width=120)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Aktions-Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="🔍 Suchen", command=lambda: controller.show_frame(NutzerSuchen)).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="➕ Hinzufügen", command=lambda: controller.show_frame(NutzerHinzufuegen)).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="🔁 Bearbeiten/Löschen", command=lambda: controller.show_frame(NutzerBearbeiten)).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="↩ Zurück", command=lambda: controller.show_frame(AdminMenue)).grid(row=0, column=3, padx=5)



        self.lade_inhalt()
    # Lädt Nutzerdaten aus der Datenbank
    def lade_inhalt(self, suchbegriff=""):
        self.tree.delete(*self.tree.get_children())
        daten = nutzer_suchen(suchbegriff)
        for id, name, rolle in daten:
            rolle_text = "Admin" if rolle == 1 else "Gast"
            self.tree.insert("", "end", values=(id, name, rolle_text))

    def clear_maske(self):
        for widget in self.maske_frame.winfo_children():
            widget.destroy()

# Ansicht für Admins zur Verwaltung aller Brauereien
class BrauereienVerwaltung(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Brauereiverwaltung", font=("Arial", 16)).pack(pady=10)

        # Tabelle
        spalten = ("ID", "Name", "Straße", "Hausnr", "PLZ", "Ort", "Website", "Gründungsjahr")
        self.tree = ttk.Treeview(self, columns=spalten, show="headings")

        for spalte in spalten:
            self.tree.heading(spalte, text=spalte)
            self.tree.column(spalte, anchor="center", width=120)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbar nicht vergessen
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Buttonleiste
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="🔍 Suchen", command=self.maske_suche).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="➕ Hinzufügen", command=lambda: controller.show_frame(BrauereiHinzufuegen)).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="🗑 Löschen", command=self.maske_loeschen).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="↩ Zurück", command=lambda: controller.show_frame(AdminMenue)).grid(row=0, column=3, padx=5)

        # Eingabemaske
        self.maske_frame = tk.Frame(self)
        self.maske_frame.pack(pady=10, fill="x")

        self.lade_inhalt()

    # Holt alle Brauereien aus DB und füllt die Tabelle
    def lade_inhalt(self, suchbegriff=""):
        self.tree.delete(*self.tree.get_children())
        daten = hole_alle_brauereien()

        print("DEBUG Daten:", daten)  # ← Zeigt dir, was zurückkommt

        for row in daten:
            self.tree.insert("", "end", values=row)

    # Löscht alle Elemente im unteren Eingabebereich
    def clear_maske(self):
        for widget in self.maske_frame.winfo_children():
            widget.destroy()

    # Zeigt Eingabefeld zum Suchen nach Name
    def maske_suche(self):
        self.clear_maske()
        tk.Label(self.maske_frame, text="Suchbegriff (Name):").pack()
        entry = tk.Entry(self.maske_frame)
        entry.pack()

        def suchen():
            self.lade_inhalt(entry.get())

        tk.Button(self.maske_frame, text="Suchen", command=suchen).pack(pady=5)

    # Zeigt Eingabe zum Löschen einer Brauerei nach ID
    def maske_loeschen(self):
        self.clear_maske()
        tk.Label(self.maske_frame, text="Brauerei-ID zum Löschen:").pack()
        entry = tk.Entry(self.maske_frame)
        entry.pack()

        def loeschen():
            bid = entry.get()
            if bid.isdigit():
                brauerei_loeschen(int(bid))
                messagebox.showinfo("Erfolg", "Brauerei gelöscht.")
                self.lade_inhalt()
                self.clear_maske()
            else:
                messagebox.showerror("Fehler", "Gültige ID eingeben!")

        tk.Button(self.maske_frame, text="Löschen", command=loeschen).pack(pady=5)

# Admin-Ansicht zur Verwaltung aller Biere
class BiereVerwaltung(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Bierverwaltung", font=("Arial", 16)).pack(pady=10)

        # Tabelle
        spalten = ("ID", "Name", "Stil", "Alkohol", "Preis", "Brauerei", "Ø Bewertung")
        self.tree = ttk.Treeview(self, columns=spalten, show="headings")
        for spalte in spalten:
            self.tree.heading(spalte, text=spalte)
            self.tree.column(spalte, anchor="center", width=100)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="🔍 Suchen", command=self.maske_suche).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="➕ Hinzufügen", command=lambda: controller.show_frame(BierHinzufuegen)).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="🗑 Löschen", command=self.maske_loeschen).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="↩ Zurück", command=lambda: controller.show_frame(AdminMenue)).grid(row=0, column=3, padx=5)

        # Eingabebereich
        self.maske_frame = tk.Frame(self)
        self.maske_frame.pack(pady=10, fill="x")

        self.lade_inhalt()

    # Holt Biere aus DB und zeigt sie an (optional mit Suchfilter)
    def lade_inhalt(self, suchbegriff=""):
        self.tree.delete(*self.tree.get_children())
        daten = suche_biere(suchbegriff) if suchbegriff else hole_alle_biere()
        for row in daten:
            self.tree.insert("", "end", values=[str(x) if x is not None else "-" for x in row])

    # Entfernt Inhalt aus der Eingabemaske
    def clear_maske(self):
        for widget in self.maske_frame.winfo_children():
            widget.destroy()

    # Zeigt Suchfeld für Biernamen
    def maske_suche(self):
        self.clear_maske()
        tk.Label(self.maske_frame, text="Suchbegriff (Name):").pack()
        entry = tk.Entry(self.maske_frame)
        entry.pack()

        def suchen():
            self.lade_inhalt(entry.get())

        tk.Button(self.maske_frame, text="Suchen", command=suchen).pack(pady=5)

    # BierHinzufuegen-Frame
    def maske_hinzufuegen(self):
        self.clear_maske()
        felder = ["Name", "Stil", "Alkoholgehalt (%)", "Preis (€)"]
        entries = []

        for feld in felder:
            tk.Label(self.maske_frame, text=feld).pack()
            e = tk.Entry(self.maske_frame)
            e.pack()
            entries.append(e)

        tk.Label(self.maske_frame, text="Brauerei wählen:").pack()
        brauereien = hole_brauereien_dropdown()
        dropdown = ttk.Combobox(self.maske_frame, values=[f"{id} - {name}" for id, name in brauereien])
        dropdown.pack()

        def speichern():
            name, stil, alk, preis = [e.get() for e in entries]
            auswahl = dropdown.get()
            if not name or not auswahl:
                messagebox.showerror("Fehler", "Name und Brauerei müssen gewählt sein.")
                return
            brauerei_id = int(auswahl.split(" - ")[0])
            bier_hinzufuegen(name, stil, alk, preis, brauerei_id)
            messagebox.showinfo("Erfolg", "Bier hinzugefügt.")
            self.lade_inhalt()
            self.clear_maske()

        tk.Button(self.maske_frame, text="Hinzufügen", command=speichern).pack(pady=5)

    # Zeigt Feld zum Löschen eines Bieres per ID
    def maske_loeschen(self):
        self.clear_maske()
        tk.Label(self.maske_frame, text="Bier-ID zum Löschen:").pack()
        entry = tk.Entry(self.maske_frame)
        entry.pack()

        def loeschen():
            bid = entry.get()
            if bid.isdigit():
                bier_loeschen(int(bid))
                messagebox.showinfo("Erfolg", "Bier gelöscht.")
                self.lade_inhalt()
                self.clear_maske()
            else:
                messagebox.showerror("Fehler", "Gültige ID eingeben!")

        tk.Button(self.maske_frame, text="Löschen", command=loeschen).pack(pady=5)

# Formular zum Hinzufügen eines neuen Biers (Adminbereich)
class BierHinzufuegen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="➕ Bier hinzufügen", font=("Arial", 16)).pack(pady=10)

        
        labels = ["Name", "Alkoholgehalt (%)", "Preis (€)"]
        self.entries = []

        for label in labels:
            tk.Label(self, text=label).pack()
            e = tk.Entry(self)
            e.pack()
            self.entries.append(e)

        # Brauerei-Auswahl (Dropdown)
        tk.Label(self, text="Brauerei wählen:").pack()
        from biere import hole_brauereien_dropdown
        self.brauereien = hole_brauereien_dropdown()
        self.dropdown = ttk.Combobox(self, values=[f"{id} - {name}" for id, name in self.brauereien])
        self.dropdown.pack()
        # Bierstil-Auswahl (Dropdown)
        tk.Label(self, text="Bierstil wählen:").pack()
        from bierstil import hole_bierstile_dropdown  
        self.bierstile = hole_bierstile_dropdown()
        self.dropdown_stil = ttk.Combobox(self, values=[f"{id} - {bez}" for id, bez in self.bierstile])
        self.dropdown_stil.pack()

        
        tk.Button(self, text="Hinzufügen", command=self.speichern).pack(pady=5)
        tk.Button(self, text="↩ Zurück", command=self.zurueck).pack()

    # Liest alle Eingaben aus, validiert sie und speichert das neue Bier
    def speichern(self):
        from biere import bier_hinzufuegen

        name, alk, preis = [e.get() for e in self.entries]

        # Brauerei aus Dropdown lesen
        auswahl = self.dropdown.get()
        if not name or not auswahl:
            tk.messagebox.showerror("Fehler", "Name und Brauerei müssen angegeben sein.")
            return
        brauerei_id = int(auswahl.split(" - ")[0])

        # Bierstil aus zweitem Dropdown lesen
        auswahl_stil = self.dropdown_stil.get()
        if not auswahl_stil:
            tk.messagebox.showerror("Fehler", "Bitte Bierstil auswählen.")
            return
        bierstil_id = int(auswahl_stil.split(" - ")[0])

        # Jetzt Bier speichern
        bier_hinzufuegen(name, alk, preis, brauerei_id, bierstil_id)

        tk.messagebox.showinfo("Erfolg", "Bier wurde hinzugefügt.")
        self.controller.frames[BiereVerwaltung].lade_inhalt()
        self.controller.show_frame(BiereVerwaltung)

    # Zurück zur Bier-Verwaltung
    def zurueck(self):
        self.controller.show_frame(BiereVerwaltung)


# Formular zum Hinzufügen einer neuen Brauerei (Adminbereich)
class BrauereiHinzufuegen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="➕ Brauerei hinzufügen", font=("Arial", 16)).pack(pady=10)

        labels = ["Name", "Straße", "Hausnummer", "Ort-ID", "Website", "Gründungsjahr"]
        self.entries = []

        for label in labels:
            tk.Label(self, text=label).pack()
            entry = tk.Entry(self)
            entry.pack()
            self.entries.append(entry)

        tk.Button(self, text="Speichern", command=self.speichern).pack(pady=5)
        tk.Button(self, text="↩ Zurück", command=self.zurueck).pack()

    # Speichert die eingegebenen Brauerei-Daten in der Datenbank
    def speichern(self):
        from brauereien import brauerei_hinzufuegen
        daten = [e.get() for e in self.entries]
        if daten[0]:
            brauerei_hinzufuegen(*daten)
            tk.messagebox.showinfo("Erfolg", "Brauerei wurde hinzugefügt!")
            self.controller.frames[BrauereienVerwaltung].lade_inhalt()
            self.controller.show_frame(BrauereienVerwaltung)
        else:
            tk.messagebox.showerror("Fehler", "Name darf nicht leer sein.")

    # Zurück zur Brauereien-Verwaltung
    def zurueck(self):
        self.controller.show_frame(BrauereienVerwaltung)

# Formular zum Erstellen eines neuen Benutzers (nur für Admins)
class NutzerHinzufuegen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="➕ Nutzer hinzufügen", font=("Arial", 16)).pack(pady=10)

        # Eingabefelder
        tk.Label(self, text="Benutzername:").pack()
        self.e_name = tk.Entry(self)
        self.e_name.pack()

        tk.Label(self, text="Passwort:").pack()
        self.e_pw = tk.Entry(self, show="*")
        self.e_pw.pack()

        tk.Label(self, text="Rolle (1 = Admin, 2 = Gast):").pack()
        self.e_rolle = tk.Entry(self)
        self.e_rolle.pack()

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Speichern", command=self.speichern).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="↩ Zurück", command=self.zurueck_und_aktualisieren).grid(row=0, column=1, padx=5)
    
    # Speichert den neuen Nutzer, wenn Eingaben gültig
    def speichern(self):
        name = self.e_name.get()
        pw = self.e_pw.get()
        rolle = self.e_rolle.get()

        if name and pw and rolle in ["1", "2"]:
            erfolg = nutzer_hinzufuegen(name, pw, int(rolle))
            if erfolg:
                messagebox.showinfo("Erfolg", "Nutzer erfolgreich hinzugefügt.")
                self.e_name.delete(0, tk.END)
                self.e_pw.delete(0, tk.END)
                self.e_rolle.delete(0, tk.END)
            else:
                messagebox.showerror("Fehler", "Benutzername existiert bereits.")

    # Zurück zur Nutzerverwaltung + Liste neu laden
    def zurueck_und_aktualisieren(self):
        self.controller.frames[NutzerVerwaltung].lade_inhalt()
        self.controller.show_frame(NutzerVerwaltung)

# Seite für Admins zum Bearbeiten oder Löschen von Nutzern
class NutzerBearbeiten(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="🔁 Nutzer bearbeiten / löschen", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Nutzer-ID:").pack()
        self.e_id = tk.Entry(self)
        self.e_id.pack()

        tk.Label(self, text="Neue Rolle (1 = Admin, 2 = Gast):").pack()
        self.e_rolle = tk.Entry(self)
        self.e_rolle.pack()

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Rolle ändern", command=self.rolle_aendern).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Nutzer löschen", command=self.loeschen).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="↩ Zurück", command=self.zurueck_und_aktualisieren).grid(row=0, column=2, padx=5)

    # Ändert die Rolle des Nutzers (Admin/Gast)
    def rolle_aendern(self):
        nid = self.e_id.get()
        rolle = self.e_rolle.get()
        if nid.isdigit() and rolle in ["1", "2"]:
            rolle_aendern(int(nid), int(rolle))
            messagebox.showinfo("Erfolg", "Rolle geändert.")
            self.e_id.delete(0, tk.END)
            self.e_rolle.delete(0, tk.END)
        else:
            messagebox.showerror("Fehler", "Ungültige Eingaben.")

    # Löscht den Nutzer mit angegebener ID
    def loeschen(self):
        nid = self.e_id.get()
        if nid.isdigit():
            nutzer_loeschen(int(nid))
            messagebox.showinfo("Erfolg", "Nutzer gelöscht.")
            self.e_id.delete(0, tk.END)
            self.e_rolle.delete(0, tk.END)
        else:
            messagebox.showerror("Fehler", "Ungültige ID.")

    # Zurück zur Nutzerverwaltung + Aktualisierung der Liste
    def zurueck_und_aktualisieren(self):
        self.controller.frames[NutzerVerwaltung].lade_inhalt()
        self.controller.show_frame(NutzerVerwaltung)

