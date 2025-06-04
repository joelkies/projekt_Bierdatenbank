import bcrypt
from datenbankverbindung import verbinde_db
from tkinter import messagebox
import tkinter as tk

#Nutzer Registrieren
def registrieren(benutzername,passwort):
    conn = verbinde_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM nutzer Where benutzername = %s", (benutzername,))
    if cursor.fetchone():
        conn.close()
        messagebox.showerror("Fehler, Benutzername existiert schon!")
        return False
    
    pass_hash = bcrypt.hashpw(passwort.encode('utf-8'), bcrypt.gensalt())

    cursor.execute(
        "INSERT INTO nutzer (benutzername, passwort_hash, rolle_id) VALUES (%s, %s, %s)",
        (benutzername, pass_hash, 2)
        
    )
    conn.commit()
    conn.close()

    messagebox.showinfo("Erfolg", "Registrierung war erfolgreich!")
    return True

#Nutzer Login
def login(benutzername, passwort):
    conn = verbinde_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, passwort_hash, rolle_id FROM nutzer WHERE benutzername = %s", (benutzername,))
    ergebnis = cursor.fetchone()
    conn.close()

    if not ergebnis:
        messagebox.showerror("Fehler", "Benutzername nicht gefunden.")
        return None

    nutzer_id, gespeicherter_hash, rolle_id = ergebnis

    if bcrypt.checkpw(passwort.encode('utf-8'), gespeicherter_hash.encode('utf-8')):
        return nutzer_id, rolle_id
    else:
        messagebox.showerror("Fehler", "Falsches Passwort.")
        return None