import sqlite3

conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()

def chat_keys_add(groupid, key, value):
    cursor.execute(f"""INSERT INTO chat_keys 
        VALUES ('{groupid}', '{key}', '{value}')
    """)
    conn.commit()

def chat_keys_remove(groupid: str, key):
    cursor.execute(f"""DELETE FROM chat_keys
        WHERE groupid='{groupid}' and key='{key}'
    """)
    conn.commit()

def chat_keys_get():
    cursor.execute(f"""SELECT * FROM chat_keys """)
    return cursor.fetchall()

def getKey(groupid, key):
    cursor.execute(f"""SELECT * FROM chat_keys WHERE groupid={groupid} and key='{key}'""")
    return cursor.fetchone()

def isInChat_keys(groupid: str, key):
    chat_keys = chat_keys_get()
    for record in chat_keys:
        if (str(record[0]) == str(groupid) and str(record[1]) == str(key)):
            return True
    return False