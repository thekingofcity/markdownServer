import os
import sqlite3
import hashlib
from dbC import dbC

def db_init_main():
    if os.path.exists("test.db"):
        os.remove("test.db")
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE users 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, username varchar(255), passwords char(256), cookie char(256), email varchar(255))''')
    cur.execute('''INSERT INTO users VALUES (100000, 'admin', '5aa8765f576b6c12dc5c0d2548861ef965bb7b448ca6ae23d404dc52ce24c0df', '', 'aaa@gmail.com')''')
    cur.execute('''INSERT INTO users VALUES (100001, 'Wzl', 'a4bd71f9bcbc2922c31132bec4c2c1ad0fd0b6833b8d656a7541059de4cd1cc5', '', 'bbb@gmail.com')''')
    cur.execute('''CREATE TABLE texts 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, userID INTEGER, docHash char(256), docname varchar(255))''')
    cur.execute('''INSERT INTO texts VALUES (10000, 100000, 'default', 'defaultAdmin')''')
    cur.execute('''INSERT INTO texts VALUES (10001, 100000, 'defaultA', 'defaultAdminA')''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    db_init_main()
    # pw = "".encode("utf_8")
    # print(hashlib.sha256(pw).hexdigest())
