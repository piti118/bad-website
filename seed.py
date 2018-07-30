import sqlite3

with sqlite3.connect('badwebsites.db') as conn:
    c = conn.cursor()

    c.execute('''
      DROP TABLE IF EXISTS users;
    ''')

    c.execute('''
      CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username text NOT NULL,
        password text NOT NULL 
      )
    ''')

    c.execute('''
      INSERT INTO users (username, password) 
      VALUES
      ('admin', 'password'),
      ('user', '12345678')
    ''')

    c.execute('''
      DROP TABLE IF EXISTS votes;
    ''')

    c.execute('''
      CREATE TABLE votes (
        name text PRIMARY KEY,
        vote INTEGER DEFAULT 0
      )
    ''')

    c.execute('''
      INSERT INTO votes (name)
      VALUES
      ('Pepsi'),
      ('Coke')
    ''')


    c.execute('''
      CREATE TABLE wall (
        id INTEGER PRIMARY KEY,
        msg INTEGER DEFAULT 0
      )
    ''')

    c.execute('''
      INSERT INTO wall (msg)
      VALUES
      ('First POST!!!!')
    ''')

    conn.commit()

    print("DONE")



