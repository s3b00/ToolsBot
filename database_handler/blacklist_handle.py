import sqlite3

conn = sqlite3.connect("mydb.db") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

def blacklist_add(userid, groupid):
    cursor.execute(f"""INSERT INTO blacklist 
        VALUES ('{userid}', '{groupid}')
    """)
    conn.commit()

def blacklist_remove(userid: str, groupid: str):
    cursor.execute(f"""DELETE FROM blacklist
        WHERE user_id='{userid}' AND groupid='{groupid}'
    """)
    conn.commit()

def blacklist_get():
    cursor.execute(f"""SELECT * FROM blacklist """)
    return cursor.fetchall()

def isInBlackList(userid: str, groupid: str):
    blacklist = blacklist_get()
    for record in blacklist:
        if (str(record[0]) == str(userid) and str(record[1]) == str(groupid)):
            return True
    return False