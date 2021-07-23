import sqlite3

conn = sqlite3.connect("mydb.db") 
cursor = conn.cursor()

def roullets_add(groupid, limit=6, target='mute'):
    cursor.execute(f"""INSERT INTO roullets 
        VALUES ('{groupid}', '{limit}', '{target}')
    """)
    conn.commit()

def roullets_remove(groupid: str):
    cursor.execute(f"""DELETE FROM roullets
        WHERE groupid='{groupid}'
    """)
    conn.commit()

def roullets_get():
    cursor.execute(f"""SELECT * FROM roullets """)
    return cursor.fetchall()

def roullets_get_game(groupid):
    cursor.execute(f"""SELECT * FROM roullets WHERE groupid={groupid} """)
    return cursor.fetchone()

def isInRoullets(groupid: str):
    roullets = roullets_get()
    for record in roullets:
        if (str(record[0]) == str(groupid)):
            return True
    return False



def roullets_games_get():
    cursor.execute(f"""SELECT * FROM roullets_games """)
    return cursor.fetchall()

def roullets_games_add(groupid, userid, bullet = 0):
    cursor.execute(f"""INSERT INTO roullets_games
        VALUES ('{groupid}', '{userid}', '{bullet}')
    """)
    conn.commit()

def roullets_games_remove(userid: str, groupid: str):
    cursor.execute(f"""DELETE FROM roullets_games
        WHERE groupid='{groupid}' or userid='{userid}'
    """)
    conn.commit()

def roullets_games_get_game(groupid):
    cursor.execute(f"""SELECT * FROM roullets_games WHERE groupid={groupid} """)
    return cursor.fetchall()

def isInRoulletsGames(groupid: str, userid: str):
    roullets = roullets_games_get()
    for record in roullets:
        if (str(record[0]) == str(groupid) and str(record[1]) == str(userid)):
            return True
    return False