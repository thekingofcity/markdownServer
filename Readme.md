# Simple python httpd

* [feature] CROS ajax and cookies

* [feature] support method OPTION

* [update] docs and unittest

# To-do

* [feature] Notes can be encrypted. Save and read encrypted data. 

Decrypt at client side. 

    CREATE TABLE texts (id INTEGER PRIMARY KEY AUTOINCREMENT, userID INTEGER, docHash char(256), docname varchar(255), isEncrypted BOOLEAN)

* [feature] Only VIP users can have notes more than one.

    CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username varchar(255), passwords char(256), cookie char(256), email varchar(255), isVIP BOOLEAN)