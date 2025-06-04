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