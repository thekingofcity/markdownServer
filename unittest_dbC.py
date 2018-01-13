import os
import json
import unittest
import hashlib

from dbC import dbC
from db_init import *

class test_dbC(unittest.TestCase):
    dbLoaction = "test.db"
    passwordHash = hashlib.sha256("ccc".encode("utf_8")).hexdigest()

    def setUp(self):
        self.userhash = {"name": "", "UID": ""}
        self.dochash = {"secondDocHash": "", "fisrtDocHash": ""}

        with open("unittestConfuserhash", "r") as f:
            json_userhash = json.load(f)
        self.userhash.update(json_userhash)
        for k,v in self.userhash.items():
            setattr(self, k, v)

        with open("unittestConfdochash", "r") as f:
            json_dochash = json.load(f)
        self.dochash.update(json_dochash)
        for k,v in self.dochash.items():
            setattr(self, k, v)
    
    def tearDown(self):

        with open('unittestConfuserhash', 'w') as f:
            json.dump(self.userhash, f)
        
        with open('unittestConfdochash', 'w') as f:
            json.dump(self.dochash, f)
        

    def test_reg(self):
        user = {'name': "ccc", 'email': "ccc@gmail.com", 'password': self.passwordHash}
        db = dbC(self.dbLoaction)
        self.UID = db.reg(user)
        self.assertNotEqual(self.UID, False)
        self.userhash = {'name': 'ccc', 'UID': self.UID}

    def test_login(self):
        user = {'name': "ccc", 'password': self.passwordHash}
        db = dbC(self.dbLoaction)
        self.UID = db.login(user)
        self.assertNotEqual(self.UID, False)
        self.userhash = {'name': 'ccc', 'UID': self.UID}

    def test_getlist_first(self):
        db = dbC(self.dbLoaction)
        ret = db.getlist(self.userhash)
        self.assertNotEqual(ret, False)

    def test_newtext_first(self):
        data = {'docName': 'first', 'data': 'This is the first file.'}
        db = dbC(self.dbLoaction)
        self.fisrtDocHash = db.newtext(self.userhash, data)
        self.dochash = {"secondDocHash": "", "fisrtDocHash": self.fisrtDocHash}
        self.assertNotEqual(self.fisrtDocHash, False)

    def test_newtext_second(self):
        data = {'docName': 'second', 'data': 'This is the second file.'}
        db = dbC(self.dbLoaction)
        self.secondDocHash = db.newtext(self.userhash, data)
        self.dochash["secondDocHash"] = self.secondDocHash
        self.assertNotEqual(self.secondDocHash, False)

    def test_ultext(self):
        data = {'docHash': self.dochash["secondDocHash"], 'data': 'This is the second file. Modified version.'}
        db = dbC(self.dbLoaction)
        self.assertTrue(db.ultext(self.userhash, data))

    def test_dltext(self):
        self.userhash["docHash"] = self.dochash["secondDocHash"]
        db = dbC(self.dbLoaction)
        self.assertEqual(db.dltext(self.userhash), 'This is the second file. Modified version.')

    def test_getlist_second(self):
        db = dbC(self.dbLoaction)
        ret = db.getlist(self.userhash)
        self.assertRegex(ret, 'first')
        self.assertRegex(ret, 'second')
        # self.fisrtDocHash = eval(ret)[1]['hash']

    def test_delNotes(self):
        db = dbC(self.dbLoaction)
        ret = db.delNotes(self.userhash, self.dochash["fisrtDocHash"])
        self.assertTrue(ret)

    def test_getlist_third(self):
        db = dbC(self.dbLoaction)
        ret = db.getlist(self.userhash)
        self.assertNotRegex(ret, 'first')
