#pip install mysql-connector-python

import mysql.connector
from datetime import datetime
import time  # Importáljuk a time modult az időzítéshez

def insert_log_to_database():
    # Kapcsolódás az adatbázishoz
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )
    cursor = cnx.cursor()

    # Log fájl beolvasás
    with open("../camera/log.txt", "r") as log_file:
        lines = log_file.readlines()

    # Log fájlra alkalmazott beszúrás adatbázisba
    for line in lines:
        if line.startswith("ID:"):
            parts = line.split('\t')
            direction = parts[0]
            timestamp = parts[1]

            # Log adatok beszúrása az adatbázisba
            query = "INSERT INTO pythoninsertdatatomysql (direction, timestamp) VALUES (%s, %s)"
            data = (direction, timestamp)

            cursor.execute(query, data)

    # Változások kommitálása
    cnx.commit()

    # Kurzor és kapcsolat bezárása
    cursor.close()
    cnx.close()

# Időzített futtatás - például minden 1 perc
while True:
    insert_log_to_database()
    time.sleep(10)
