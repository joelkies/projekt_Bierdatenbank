from datenbankverbindung import verbinde_db

#Alle Biere mit Brauerei anzeigen
def hole_alle_biere():
    conn = verbinde_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT bier.id, bier.name, bierstil.bezeichnung AS stil,
               bier.alkoholgehalt, bier.preis,
               IFNULL(brauerei.name, 'Unbekannt') AS brauerei_name,
               ROUND(AVG(bewertung.sterne), 1) AS durchschnitt
        FROM bier
        JOIN brauerei ON bier.brauerei_id = brauerei.id
        LEFT JOIN bierstil ON bier.bierstil_id = bierstil.id
        LEFT JOIN bewertung ON bier.id = bewertung.bier_id
        GROUP BY bier.id, bier.name, bierstil.bezeichnung, bier.alkoholgehalt,
                 bier.preis, brauerei.name
        ORDER BY bier.name
    """)
    daten = cursor.fetchall()
    conn.close()
    return daten

#zeigt biere in gästebereich an
def hole_alle_biere_fuer_gaeste():
    conn = verbinde_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            bier.id,
            bier.name,
            bierstil.bezeichnung,
            bier.alkoholgehalt,
            bier.preis,
            brauerei.name,
            ort.Ort,
            ROUND(AVG(bewertung.sterne), 1) AS durchschnitt
        FROM bier
        JOIN brauerei ON bier.brauerei_id = brauerei.id
        LEFT JOIN ort ON brauerei.ort_id = ort.ID_Ort
        LEFT JOIN bierstil ON bierstil.id = bier.bierstil_id
        LEFT JOIN bewertung ON bier.id = bewertung.bier_id
        GROUP BY bier.id, bier.name, bierstil.bezeichnung, bier.alkoholgehalt, bier.preis, brauerei.name, ort.Ort
    """)
    daten = cursor.fetchall()
    conn.close()
    return daten

#fügt neues bier in datenbank hinzu
def bier_hinzufuegen(name, alkohol, preis, brauerei_id, bierstil_id):
    conn = verbinde_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO bier (name, alkoholgehalt, preis, brauerei_id, bierstil_id) VALUES (%s, %s, %s, %s, %s)",
        (name, alkohol, preis, brauerei_id, bierstil_id)
    )
    conn.commit()
    conn.close()

#Bier löschen
def bier_loeschen(bier_id):
    conn = verbinde_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bier WHERE id = %s", (bier_id,))
    conn.commit()
    conn.close()

#Dropdownmenü
def hole_brauereien_dropdown():
    conn = verbinde_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM brauerei ORDER BY name")
    daten = cursor.fetchall()
    conn.close()
    return daten

#Biersuchfunktion
def suche_biere(begriff):
    conn = verbinde_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            bier.id, 
            bier.name, 
            bierstil.bezeichnung AS stil,
            bier.alkoholgehalt, 
            bier.preis, 
            IFNULL(brauerei.name, 'Unbekannt') AS brauerei_name,
            ROUND(AVG(bewertung.sterne), 1) AS durchschnitt
        FROM bier
        LEFT JOIN brauerei ON bier.brauerei_id = brauerei.id
        LEFT JOIN ort o ON brauerei.ort_id = o.ID_Ort
        LEFT JOIN bierstil ON bier.bierstil_id = bierstil.id
        LEFT JOIN bewertung ON bier.id = bewertung.bier_id
        WHERE bier.name LIKE %s
           OR bierstil.bezeichnung LIKE %s
           OR brauerei.name LIKE %s
           OR o.Ort LIKE %s
        GROUP BY bier.id, bier.name, bierstil.bezeichnung, bier.alkoholgehalt, bier.preis, brauerei.name
        ORDER BY bier.name
    """, (f"%{begriff}%", f"%{begriff}%", f"%{begriff}%", f"%{begriff}%"))
    daten = cursor.fetchall()
    conn.close()
    return daten

#Best bewertete biere
def hole_top_biere(limit=5):
    conn = verbinde_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            bier.name, 
            bierstil.bezeichnung AS stil,
            bier.alkoholgehalt,
            bier.preis,
            IFNULL(brauerei.name, 'Unbekannt') AS brauerei_name,
            ort.Ort,
            ROUND(AVG(bewertung.sterne), 2) AS durchschnitt
        FROM bier
        LEFT JOIN brauerei ON bier.brauerei_id = brauerei.id
        LEFT JOIN ort ON brauerei.ort_id = ort.ID_Ort
        LEFT JOIN bierstil ON bier.bierstil_id = bierstil.id
        LEFT JOIN bewertung ON bier.id = bewertung.bier_id
        GROUP BY bier.id
        HAVING durchschnitt IS NOT NULL
        ORDER BY durchschnitt DESC
        LIMIT %s
    """, (limit,))
    daten = cursor.fetchall()
    conn.close()
    return daten

#Biersuche mit erweiterten filter
def suche_biere_erweitert(suchbegriff="", max_alkohol=None, max_preis=None):
    conn = verbinde_db()
    cursor = conn.cursor()

    sql = """
        SELECT bier.id, bier.name, bierstil.bezeichnung AS stil,
               bier.alkoholgehalt, bier.preis,
               IFNULL(brauerei.name, 'Unbekannt') AS brauerei_name,
               o.Ort,
               ROUND(AVG(bewertung.sterne), 1) AS durchschnitt
        FROM bier
        JOIN brauerei ON bier.brauerei_id = brauerei.id
        LEFT JOIN ort o ON brauerei.ort_id = o.ID_Ort
        LEFT JOIN bierstil ON bier.bierstil_id = bierstil.id
        LEFT JOIN bewertung ON bier.id = bewertung.bier_id
        WHERE (bier.name LIKE %s OR bierstil.bezeichnung LIKE %s OR brauerei.name LIKE %s)
    """

    werte = [f"%{suchbegriff}%", f"%{suchbegriff}%", f"%{suchbegriff}%"]

    if max_alkohol is not None:
        sql += " AND bier.alkoholgehalt <= %s"
        werte.append(max_alkohol)

    if max_preis is not None:
        sql += " AND bier.preis <= %s"
        werte.append(max_preis)

    sql += """
        GROUP BY bier.id, bier.name, bierstil.bezeichnung,
                 bier.alkoholgehalt, bier.preis, brauerei.name, o.Ort
        ORDER BY bier.name
    """

    cursor.execute(sql, tuple(werte))
    daten = cursor.fetchall()
    conn.close()
    return daten