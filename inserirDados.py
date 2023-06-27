import sqlite3
from random import randint

# Connect to the database
conn = sqlite3.connect('bank_database.db')
cursor = conn.cursor()

# Generate sample data for 'usuario' table
usuarios = [
    ('2526', '1234'),
    ('2527', '1234'),
    ('2528', '1234')
]

cursor.executemany('INSERT INTO usuario (login, senha) VALUES (?, ?)', usuarios)

# Generate sample data for 'conta' table
contas = [
    (1, '2526', 1000.0),
    (2, '2527', 2500.0),
    (3, '2528', 1500.0)
]

cursor.executemany('INSERT INTO conta (id_usuario, numero, saldo) VALUES (?, ?, ?)', contas)

# Commit the changes and close the connection
conn.commit()
conn.close()