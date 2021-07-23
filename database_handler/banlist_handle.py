import sqlite3

conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()

def banlist_add(groupid, userid):
    cursor.execute(f"""INSERT INTO banlist 
        VALUES ('{groupid}', '{userid}')
    """)
    conn.commit()

def banlist_remove(groupid: str, userid: str):
    cursor.execute(f"""DELETE FROM banlist
        WHERE user_id='{userid}' AND groupid='{groupid}'
    """)
    conn.commit()

def banlist_get():
    cursor.execute(f"""SELECT * FROM banlist """)
    return cursor.fetchall()

def isInBanlist(groupid: str, userid: str):
    banlist = banlist_get()
    for record in banlist:
        if (str(record[0]) == str(groupid) and str(record[1]) == str(userid)):
            return True
    return False