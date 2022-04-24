import sqlite3

conn = sqlite3.connect('logs.db')
cur = conn.cursor()
cur.execute('''
        CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_hora TEXT,
        nome TEXT,
        imc REAL,
        classificacao TEXT,
        ip TEXT,
        navegador TEXT
        );
        ''')
conn.commit()
cur.close()
conn.close()