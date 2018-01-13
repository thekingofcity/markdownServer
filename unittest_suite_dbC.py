import unittest
import json
from unittest_dbC import test_dbC
from db_init import *

if __name__ == '__main__':
    db_init_main()
    file = os.listdir('data')
    for f in file:
        if((f != 'default') and (f != 'defaultA')):
            os.remove('data\\' + f)
    
    userhash = {"name": "", "UID": ""}
    dochash = {"docHashSecond": "", "fisrtDocHash": ""}
    with open('unittestConfuserhash', 'w') as f:
        json.dump(userhash, f)
    with open('unittestConfdochash', 'w') as f:
        json.dump(dochash, f)

    suite = unittest.TestSuite()

    tests = [test_dbC("test_reg"), test_dbC("test_login"),
        test_dbC("test_getlist_first"), test_dbC("test_newtext_first"),
        test_dbC("test_newtext_second"), test_dbC("test_ultext"),
        test_dbC("test_dltext"), test_dbC("test_getlist_second"),
        test_dbC("test_delNotes"), test_dbC("test_getlist_third"),
        ]
    suite.addTests(tests)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

    db_init_main()
    file = os.listdir('data')
    for f in file:
        if((f != 'default') and (f != 'defaultA')):
            os.remove('data\\' + f)
    file = os.listdir()
    for f in file:
        if((f == 'unittestConfuserhash') or (f == 'unittestConfdochash')):
            os.remove(f)
