import mariadb
import sys

# Verbindung zur Datenbank
def verbinde_db():
    try:
        conn = mariadb.connect(
            user = "team10",
            password = "QYHV8",
            host = "10.80.0.206",
            port = 3306,
            database = "team10"
        )
        print("Verbindung zur Datenbank hergestellt!")
        return conn
    except mariadb.Error as e:
        print(f"Error Verbindung nicht möglich: {e}")
        sys.exit(1)