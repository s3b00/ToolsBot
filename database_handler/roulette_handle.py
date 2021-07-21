import sqlite3

conn = sqlite3.connect("mydb.db") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
