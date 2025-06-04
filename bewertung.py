from datenbankverbindung import verbinde_db
from datetime import datetime

#eine Bewertung hinzufügen
def bewertung_hinzufuegen(bier_id, nutzer_id, sterne, kommentar):
    conn = verbinde_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO bewertung (bier_id, nutzer_id, sterne, kommentar) VALUES (%s, %s, %s, %s)",
        (bier_id, nutzer_id, sterne, kommentar)
    )
    conn.commit()
    conn.close()

#Bewertungen ändern
def aktualisiere_bewertung(bier_id, nutzer_id, sterne, kommentar):
    conn = verbinde_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE bewertung
        SET sterne = %s, kommentar = %s
        WHERE bier_id = %s AND nutzer_id = %s
    """, (sterne, kommentar, bier_id, nutzer_id))
    conn.commit()
    conn.close()

#Bewertung anzeigen
def hole_bewertungen_fuer_bier(bier_id):
    conn = verbinde_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nutzer.benutzername, sterne, kommentar, erstellt_am, nutzer.id
        FROM bewertung
        JOIN nutzer ON bewertung.nutzer_id = nutzer.id
        WHERE bier_id = %s
        ORDER BY erstellt_am DESC
    """, (bier_id,))
    daten = cursor.fetchall()
    conn.close()
    return daten
