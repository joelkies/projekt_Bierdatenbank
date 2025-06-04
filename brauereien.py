from datenbankverbindung import verbinde_db  

#Gibt brauereien zurück
def hole_alle_brauereien():
    conn = verbinde_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            b.id, b.name, b.straße, b.hausnr,
            o.PLZ, o.Ort, b.website, b.gruendungsjahr
        FROM brauerei b
        JOIN ort o ON b.ort_id = o.ID_Ort
        ORDER BY b.name
    """)
    brauereien = cursor.fetchall()
    conn.close()
    return brauereien

#Brauereien hinzufügen
def brauerei_hinzufuegen(name, ort, plz, adresse, website, jahr):
    conn = verbinde_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO brauerei (name, ort, plz, adresse, website, gruendungsjahr) VALUES (%s, %s, %s, %s, %s, %s)",
        (name, ort, plz, adresse, website, jahr)
    )
    conn.commit()
    conn.close()

#Brauereien löschen
def brauerei_loeschen(brauerei_id):
    conn = verbinde_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM brauerei WHERE id = %s", (brauerei_id,))
    conn.commit()
    conn.close()