import sqlite3

conn = sqlite3.connect("mapping.db")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS mapping(id TEXT, website TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS imageslog(filename TEXT, website TEXT)")

cur.execute("INSERT INTO mapping VALUES('605004','pondicherry.com')")
cur.execute("INSERT INTO mapping VALUES('605106','cuddalore.com')")
cur.execute("INSERT INTO mapping VALUES('627003','tirunelveli.com')")

conn.commit()
conn.close()
