import sqlite3

conn = sqlite3.connect('mydb.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY, name TEXT, salary INTEGER)')
c.execute('INSERT INTO employees (name, salary) VALUES (?, ?)', ('Alice', 50000))
c.execute('INSERT INTO employees (name, salary) VALUES (?, ?)', ('Bob', 60000))
conn.commit()
conn.close()
print('Sample database mydb.db created!') 