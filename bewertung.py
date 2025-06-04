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