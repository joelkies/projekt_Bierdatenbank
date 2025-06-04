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
