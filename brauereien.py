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