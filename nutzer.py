from datenbankverbindung import verbinde_db
import bcrypt
import sqlite3
from tkinter import messagebox

#nutzer anzeigen
def hole_alle_nutzer():
    conn = verbinde_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, benutzername, rolle_id FROM nutzer ORDER BY id")
    nutzer = cursor.fetchall()

    conn.close()
    return nutzer

#nutzer löschen
def nutzer_loeschen(nutzer_id):
    conn = verbinde_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM nutzer WHERE id = %s", (nutzer_id,))
    conn.commit()
    conn.close()

#benutzerrolle ändern
def rolle_aendern(nutzer_id, neue_rolle):
    conn = verbinde_db()
    cursor = conn.cursor()

    cursor.execute("UPDATE nutzer SET rolle_id = %s WHERE id = %s", (neue_rolle, nutzer_id))
    conn.commit()
    conn.close()

#nutzer suchen
def nutzer_suchen(suchbegriff):
    conn = verbinde_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, benutzername, rolle_id FROM nutzer WHERE benutzername LIKE %s", (f"%{suchbegriff}%",))
    ergebnisse = cursor.fetchall()

    conn.close()
    return ergebnisse

#nutzer hinzufügen
def nutzer_hinzufuegen(benutzername, passwort, rolle_id):
    from tkinter import messagebox  # Import nicht vergessen!
    conn = verbinde_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM nutzer WHERE benutzername = %s", (benutzername,))
    if cursor.fetchone():
        conn.close()
        return False  

    pass_hash = bcrypt.hashpw(passwort.encode('utf-8'), bcrypt.gensalt())

    cursor.execute(
        "INSERT INTO nutzer (benutzername, passwort_hash, rolle_id) VALUES (%s, %s, %s)",
        (benutzername, pass_hash.decode(), rolle_id)
    )
    conn.commit()
    conn.close()
    return True 