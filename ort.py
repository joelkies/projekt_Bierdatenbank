from datenbankverbindung import verbinde_db

def hole_orte_dropdown():
    conn = verbinde_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ID_Ort, Ort, PLZ FROM ort ORDER BY Ort")
    daten = cursor.fetchall()
    conn.close()
    return daten