import sqlite3

conn = sqlite3.connect("mapping.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS mapping")
cur.execute("DROP TABLE IF EXISTS imageslog")

cur.execute("CREATE TABLE mapping(id TEXT, website TEXT)")
cur.execute("CREATE TABLE imageslog(filename TEXT, website TEXT)")

cur.execute("INSERT INTO mapping VALUES('605004','pondicherry.com')")
cur.execute("INSERT INTO mapping VALUES('605106','cuddalore.com')")
cur.execute("INSERT INTO mapping VALUES('627003','tirunelveli.com')")

conn.commit()
conn.close()

print("DB created!")
