import sqlite3

DB = None
CONN = None

ADMIN_USER="hackbright"
ADMIN_PASSWORD=5980025637247534551

def authenticate(username, password):
    connect_to_db()

    query = """SELECT id from users WHERE username=? AND password=?
            """
    DB.execute(query, (username, hash(password)))
    user_id = DB.fetchone()

    if user_id != None:
        return user_id

    else:
        return None

def get_user_by_name(username):
    connect_to_db()
    query = """SELECT id from users WHERE username=?
            """
    DB.execute(query, (username,))
    user_id = DB.fetchone()

    if user_id != None:
        return user_id

    else:
        return [None]


def get_wall_posts(userid):
    connect_to_db()
    query = """SELECT author_id, created_at, content
               FROM wall_posts
               WHERE owner_id = ?
            """
    result = DB.execute(query, (userid,))
    return result.fetchall()
    # if result != None:
    #     return result.fetchall()
    # else:
    #     return None

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("thewall.db")
    DB = CONN.cursor()
