import sqlite3
import json
import hashlib
import time

class dbC():
    
    def __init__(self):
        self.conn = sqlite3.connect('test.db')
        self.cur = self.conn.cursor()
    
    def commit(self):
        self.conn.commit()
        # self.conn.close()

    def reg(self, user):
        t = (user['name'], hashlib.sha256(user['password'].encode("utf_8")).hexdigest())
        self.cur.execute('''INSERT INTO users (username, passwords) VALUES (?,?)''', t)
        self.commit()

    def login(self, user):
        t = (user['name'], user['password'])
        self.cur.execute('SELECT * FROM users WHERE username=? AND passwords=?', t)
        t = self.cur.fetchone()
        if t:
            cookie = str(time.time()) + str(t[0]) + user['password']
            cookie = hashlib.sha256(cookie.encode("utf_8")).hexdigest()
            t = (cookie, t[0])
            self.cur.execute('UPDATE users SET cookie=? WHERE id=?', t)
            self.commit()
            return cookie
        else:
            return False

    def getlist(self, userhash):
        t = (userhash['name'], userhash['UID'])
        self.cur.execute('SELECT * FROM users WHERE username=? AND cookie=?', t)
        t = self.cur.fetchone()
        if t:
            t = (t[0], )
            self.cur.execute('SELECT * FROM texts WHERE userID=?', t)
            listFromDb = self.cur.fetchall()
            self.conn.close()
            list_ = {}
            ret = "["
            if len(listFromDb) > 0:
                for i in listFromDb:
                    list_["name"] = i[3]
                    list_["hash"] = i[2]
                    ret = ret + json.dumps(list_) + ","
                ret = ret[0:len(ret)-1] + "]"
            else:
                ret = ret + "]"
            return ret
        else:
            self.conn.close()
            return False
        
    def dltext(self, userhash):
        t = (userhash['name'], userhash['UID'])
        self.cur.execute('SELECT * FROM users WHERE username=? AND cookie=?', t)
        t = self.cur.fetchone()
        self.conn.close()
        if t:
            file_object = open('data\\' + userhash['docHash'])
            try:
                all_the_text = file_object.read()
            finally:
                file_object.close()
            return all_the_text
        else:
            return False

    def ultext(self, userhash, data):
        t = (userhash['name'], userhash['UID'])
        self.cur.execute('SELECT * FROM users WHERE username=? AND cookie=?', t)
        t = self.cur.fetchone()
        self.conn.close()
        if t:
            file_object = open('data\\' + data['docHash'], 'w')
            try:
                file_object.write(data['data'])
            finally:
                file_object.close()
            return True
        else:
            return False

    def newtext(self, userhash, data):
        t = (userhash['name'], userhash['UID'])
        self.cur.execute('SELECT * FROM users WHERE username=? AND cookie=?', t)
        t = self.cur.fetchone()
        if t:
            docHash = str(time.time()) + data['docName'] + userhash['UID']
            docHash = hashlib.sha256(docHash.encode("utf_8")).hexdigest()
            t = (t[0], docHash, data['docName'])
            fileName = 'data\\' + docHash
            # check if there is a same name file under the folder
            print(fileName)
            file_object = open(fileName, 'w')
            try:
                file_object.write(data['data'])
            finally:
                file_object.close()
            self.cur.execute('''INSERT INTO texts (userID, texthash, textname) VALUES (?, ?, ?)''', t)
            self.commit()
            self.conn.close()
            return docHash
        else:
            self.conn.close()
            return False