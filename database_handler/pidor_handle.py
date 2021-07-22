import sqlite3

conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()

def pidor_games_members_add(groupid):
    cursor.execute(f"""INSERT INTO pidor_games_member 
        VALUES ('{groupid}', '0')
    """)
    conn.commit()

def pidor_games_members_remove(groupid: str):
    cursor.execute(f"""DELETE FROM pidor_games_member
        WHERE groupid='{groupid}'
    """)
    conn.commit()

def pidor_games_members_get():
    cursor.execute(f"""SELECT * FROM pidor_games_member """)
    return cursor.fetchall()

def pidors_games_members_get_group(groupid):
    cursor.execute(f"""SELECT * FROM pidor_games_member WHERE groupid={groupid}""")
    return cursor.fetchone()

def isInPidor_games_members(groupid: str):
    pidor_games_members = pidor_games_members_get()
    for record in pidor_games_members:
        if (str(record[0]) == str(groupid)):
            return True
    return False



def pidor_games_add(groupid, date, winner):
    cursor.execute(f"""INSERT INTO pidor_games 
        VALUES ('{groupid}', '{date}', '{winner}')
    """)
    conn.commit()

def pidor_games_remove(groupid: str):
    cursor.execute(f"""DELETE FROM pidor_games
        WHERE groupid='{groupid}'
    """)
    conn.commit()

def pidor_games_get():
    cursor.execute(f"""SELECT * FROM pidor_games """)
    return cursor.fetchall()

def pidors_games_get_group(groupid):
    cursor.execute(f"""SELECT * FROM pidor_games WHERE groupid={groupid}""")
    return cursor.fetchall()

def isInPidor_games_today(groupid: str, day: str):
    pidor_games = pidor_games_get()
    for record in pidor_games:
        if (str(record[0]) == str(groupid) and str(record[1]) == str(day)):
            return True
    return False



def pidors_add(groupid, userid):
    cursor.execute(f"""INSERT INTO pidors
        VALUES ('{groupid}', '{userid}')
    """)
    conn.commit()

def pidors_remove(groupid: str, userid: str):
    cursor.execute(f"""DELETE FROM pidors
        WHERE groupid='{groupid}' or userid='{userid}'
    """)
    conn.commit()

def pidors_get():
    cursor.execute(f"""SELECT * FROM pidors """)
    return cursor.fetchall()

def pidors_get_group(groupid):
    cursor.execute(f"""SELECT * FROM pidors WHERE groupid={groupid}""")
    return cursor.fetchall()

def pidors_get_user_group(userid, groupid):
    cursor.execute(f"""SELECT * FROM pidors WHERE groupid={groupid} and userid='{userid}'""")
    return cursor.fetchall()