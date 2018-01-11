import sqlite3

def main():
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    for row in cur.execute('SELECT * FROM users'):
        print(row)
    conn.close()

if __name__ == '__main__':
    main()