import sqlite3
import hashlib
import time

class dbC():
    
    def __init__(self):
        self.conn = sqlite3.connect('test.db')
        self.cur = self.conn.cursor()
    
    def commit(self):
        self.conn.commit()

    def reg(self, user):
        t = (user['name'], hashlib.sha256(user['password'].encode("utf_8")).hexdigest())
        self.cur.execute('''INSERT INTO users (username, passwords) VALUES (?,?)''', t)
        self.commit()

    def login(self, user):
        t = (user['name'], hashlib.sha256(user['password'].encode("utf_8")).hexdigest())
        self.cur.execute('SELECT * FROM users WHERE username=? AND passwords=?', t)
        t = self.cur.fetchone()
        if t:
            cookie = str(time.time()) + str(t[0]) + user['password']
            return hashlib.sha256(cookie.encode("utf_8")).hexdigest()
        else:
            return False
        
