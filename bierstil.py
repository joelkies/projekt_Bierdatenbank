from datenbankverbindung import verbinde_db

#bierstil dropdown
def hole_bierstile_dropdown():
    conn = verbinde_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, bezeichnung FROM bierstil ORDER BY bezeichnung")
    daten = cursor.fetchall()
    conn.close()
    return daten