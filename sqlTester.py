import sqlite3conn=sqlite3.connect('tester.db')curs=conn.cursor()#curs.execute('''INSERT INTO hits values(date('now'),time('now'),'troller 3');''')conn.commit()for row in curs.execute('SELECT * FROM hits'):    print rowconn.close()