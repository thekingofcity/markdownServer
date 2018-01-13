import os
import sqlite3
import json
import hashlib
import time

class dbC():
    """
    Manipulate the database.
    """

    def __init__(self, dbLoaction):
        self.conn = sqlite3.connect(dbLoaction)
        self.cur = self.conn.cursor()

    def commit(self):
        """
        Deprecated
        """
        self.conn.commit()

    def reg(self, user):
        """
        User regsiter.
        1. Check whether email exist in database.
        2. INSERT into users.
        3. SELECT from users --> id.
        4. create UID from time, id and passwordHash.
        5. return cookie.

        Parameters:
            user - {'name': username, 'email': email, 'password': passwordHash}

        Returns:
            cookie for successful sign up.
            False for existing email address.
        """
        t = (user['email'], )
        self.cur.execute('SELECT * FROM users WHERE email=?', t)
        t = self.cur.fetchone()
        if t:
            self.conn.close()
            return False
        else:
            t = (user['name'], user['password'], user['email'])
            self.cur.execute('''INSERT INTO users
                (username, passwords, email) VALUES (?, ?, ?)''', t)
            self.commit()
            t = (user['name'], user['password'])
            self.cur.execute('SELECT * FROM users WHERE username=? AND passwords=?', t)
            t = self.cur.fetchone()
            cookie = str(time.time()) + str(t[0]) + user['password']
            cookie = hashlib.sha256(cookie.encode("utf_8")).hexdigest()
            t = (cookie, t[0])
            self.cur.execute('UPDATE users SET cookie=? WHERE id=?', t)
            self.commit()
            self.conn.close()
            return cookie

    def login(self, user):
        """
        User login.
        1. Check whether name and UID exist in database.
        2. SELECT from users --> id.
        3. create UID from time, id and passwordHash.
        4. return cookie.

        Parameters:
            user - {'name': username, 'password': passwordHash}

        Returns:
            cookie for successful login.
            False when UID doesn't match name.
        """
        t = (user['name'], user['password'])
        self.cur.execute('SELECT * FROM users WHERE username=? AND passwords=?', t)
        t = self.cur.fetchone()
        if t:
            cookie = str(time.time()) + str(t[0]) + user['password']
            cookie = hashlib.sha256(cookie.encode("utf_8")).hexdigest()
            t = (cookie, t[0])
            self.cur.execute('UPDATE users SET cookie=? WHERE id=?', t)
            self.commit()
            self.conn.close()
            return cookie
        else:
            self.conn.close()
            return False

    def getlist(self, userhash):
        """
        Get user notes list.
        1. Check whether name and UID exist in database.
        2. SELECT from users --> id.
        3. SELECT from texts --> all docname and docHash.
        4. return js.array string.

        Parameters:
            user - {'name': username, 'UID': UID}

        Returns:
            js.array string for query.
            False when UID doesn't match name.
        """
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
            if listFromDb:
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

    def delNotes(self, userhash, docHash):
        """
        Delete user notes according to the docHash.
        1. Check whether name and UID exist in database.
        2. SELECT from users --> id.
        3. DELETE from texts <-- id and docHash.
        4. delete file on disk

        Parameters:
            user - {'name': username, 'UID': UID}
            docHash - note hash not name

        Returns:
            True when UID matches name.
            False when UID doesn't match name.
        """
        t = (userhash['name'], userhash['UID'])
        self.cur.execute('SELECT * FROM users WHERE username=? AND cookie=?', t)
        t = self.cur.fetchone()
        if t:
            t = (t[0], docHash)
            self.cur.execute('DELETE FROM texts WHERE userID=? AND docHash=?', t)
            self.conn.commit()
            self.conn.close()
            os.remove('data\\' + docHash)
            return True
        else:
            self.conn.close()
            return False
        
    def dltext(self, userhash):
        """
        Send user notes according to the docHash. Downloadtext refers to client side.
        1. Check whether name and UID exist in database.
        2. SELECT from users --> id.
        3. SELECT from texts <-- whether id and docHash matches.
        4. read text and return

        Parameters:
            user - {'name': username, 'UID': UID, 'docHash': docHash}

        Returns:
            all_the_text when UID matches name.
            False when UID doesn't match name or id doesn't match docHash.
        """
        t = (userhash['name'], userhash['UID'])
        self.cur.execute('SELECT * FROM users WHERE username=? AND cookie=?', t)
        t = self.cur.fetchone()
        if t:
            t = (t[0], userhash['docHash'])
            self.cur.execute('SELECT * FROM texts WHERE userID=? AND docHash=?', t)
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
        else:
            self.conn.close()
            return False

    def ultext(self, userhash, data):
        """
        Save user notes according to the docHash. Uploadtext refers to client side.
        1. Check whether name and UID exist in database.
        2. SELECT from users --> id.
        3. SELECT from texts <-- whether id and docHash matches.
        4. write text and return

        Parameters:
            user - {'name': username, 'UID': UID}
            data - {'docHash': docHash, 'data': data}

        Returns:
            True when UID matches name and userID matches docHash.
            False vice versa.
        """
        t = (userhash['name'], userhash['UID'])
        self.cur.execute('SELECT * FROM users WHERE username=? AND cookie=?', t)
        t = self.cur.fetchone()
        if t:
            t = (t[0], data['docHash'])
            self.cur.execute('SELECT * FROM texts WHERE userID=? AND docHash=?', t)
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
        else:
            self.conn.close()
            return False

    def newtext(self, userhash, data):
        """
        WARNING: !!!check if there is a same name file under the folder!!!
        Save user notes without docHash.
        1. Check whether name and UID exist in database.
        2. SELECT from users --> id.
        3. create docHash from time, docName and passwordHash.
        4. write text and return docHash

        Parameters:
            user - {'name': username, 'UID': UID}
            data - {'docName': docName, 'data': data}

        Returns:
            docHash when UID matches name and write successfully.
            False when UID doesn't match name.
        """
        t = (userhash['name'], userhash['UID'])
        self.cur.execute('SELECT * FROM users WHERE username=? AND cookie=?', t)
        t = self.cur.fetchone()
        if t:
            docHash = str(time.time()) + data['docName'] + userhash['UID']
            docHash = hashlib.sha256(docHash.encode("utf_8")).hexdigest()
            t = (t[0], docHash, data['docName'])
            fileName = 'data\\' + docHash
            # check if there is a same name file under the folder
            file_object = open(fileName, 'w')
            try:
                file_object.write(data['data'])
            finally:
                file_object.close()
            self.cur.execute('''INSERT INTO texts (userID, docHash, docname) VALUES (?, ?, ?)''', t)
            self.commit()
            self.conn.close()
            return docHash
        else:
            self.conn.close()
            return False