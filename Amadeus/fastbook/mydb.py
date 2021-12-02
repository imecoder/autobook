import sqlite3

def is_first_visit() :
    con = sqlite3.connect("cookie.sqlite")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f'SELECT * FROM cookie')
    result = cur.fetchall()
    if len(result) != 0 :
        return False

    return True


def clear_cookie():
    con = sqlite3.connect("cookie.sqlite")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f'delete from cookie')
    cur.execute(f'update sqlite_sequence SET seq = 0 where name = "cookie"')

def insert_cookie(domain, key, value) :
    con = sqlite3.connect("cookie.sqlite")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f'')
    for row in cur:
        print(key + '=' + row['value'])


def get_cookie(domain, key) :
    con = sqlite3.connect("cookie.sqlite")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f'SELECT value FROM cookies where domain="{domain}" and key="{key}"')
    for row in cur:
        print(key + '=' + row['value'])


is_first_visit = is_first_visit()
