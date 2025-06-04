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