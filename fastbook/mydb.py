import sqlite3

def is_first_visit() :
    con = sqlite3.connect("cookie.sqlite")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f'SELECT * FROM cookie')
    result = cur.fetchall()
    con.close()
    if len(result) != 0 :
        return False

    return True


def clear_cookie():
    con = sqlite3.connect("cookie.sqlite")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f'delete from cookie')
    # cur.execute(f'update sqlite_sequence SET seq = 0 where name = "cookie"')
    con.commit()
    con.close()


def save_cookie(domain, cookie) :
    con = sqlite3.connect("cookie.sqlite")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    for key, value in cookie.items() :
        cur.execute(f'delete from cookie where key="{key}" and domain="{domain}"')
        cur.execute(f'insert into cookie (key, domain, value) values ("{key}", "{domain}", "{value}")')
    con.commit()
    con.close()


def get_cookie(domain, key) :
    con = sqlite3.connect("cookie.sqlite")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f'select value from cookie where domain="{domain}" and key="{key}"')
    one = cur.fetchone()
    if one != None and one['value'] != '' :
        con.close()
        return one['value']

    cur.execute(f'select value from cookie where key="{key}"')
    one = cur.fetchone()
    if one != None and one['value'] != '' :
        con.close()
        return one['value']

    return ''


is_first_visit = is_first_visit()
