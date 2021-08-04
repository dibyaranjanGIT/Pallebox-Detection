import sqlite3

def create_db():
    con=sqlite3.connect(database=r'userdatabase.db')
    cur= con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS user(uid text,name text,email text,pass text,utype text)")
    con.commit()

create_db()