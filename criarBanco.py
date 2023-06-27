import sqlite3

# Connect to the database
conn = sqlite3.connect('bank_database.db')
cursor = conn.cursor()

# Create the 'usuario' table
cursor.execute('''
    CREATE TABLE usuario (
        id INTEGER PRIMARY KEY,
        login TEXT,
        senha TEXT
    )
''')

# Create the 'conta' table
cursor.execute('''
    CREATE TABLE conta (
        id_usuario INTEGER,
        numero TEXT,
        saldo REAL,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id)
    )
''')

# Create the 'transacoes' table
cursor.execute('''
    CREATE TABLE transacoes (
        id_transacao INTEGER PRIMARY KEY,
        id_usuario INTEGER,
        valor REAL,
        login_destino TEXT,
        data TEXT,
        hora TEXT,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id)
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()