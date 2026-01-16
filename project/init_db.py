import sqlite3

conn = sqlite3.connect("mapping.db")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS mapping(id TEXT, website TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS imageslog(filename TEXT, website TEXT)")

data = [
    ("605004", "pondicherry.com"),
    ("605106", "cuddalore.com"),
    ("627003", "tirunelveli.com"),
]

for d in data:
    cur.execute("INSERT INTO mapping VALUES (?,?)", d)

conn.commit()
conn.close()

print("DB ready!")
