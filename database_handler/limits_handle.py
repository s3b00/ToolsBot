import sqlite3

conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()

def command_limits_add(groupid, limit):
    cursor.execute(f"""INSERT INTO command_limits 
        VALUES ('{groupid}', '{limit}')
    """)
    conn.commit()

def command_limits_update(groupid, limit):
    cursor.execute(f"""UPDATE command_limits 
        SET limit={limit}
        WHERE groupid={groupid}
    """)
    conn.commit()

def command_limits_remove(groupid: str, limit):
    cursor.execute(f"""DELETE FROM command_limits
        WHERE groupid='{groupid}' and limit='{limit}'
    """)
    conn.commit()

def command_limits_get():
    cursor.execute(f"""SELECT * FROM command_limits """)
    return cursor.fetchall()

def getLimit(groupid):
    cursor.execute(f"""SELECT * FROM command_limits WHERE groupid={groupid}""")
    return cursor.fetchone()

def isInCommand_limits(groupid: str):
    command_limits = command_limits_get()
    for record in command_limits:
        if (str(record[0]) == str(groupid)):
            return True
    return False