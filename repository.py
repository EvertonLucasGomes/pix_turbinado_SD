import sqlite3

class Db:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def get_user_by_id(self, user_id):
        self.cursor.execute("SELECT * FROM usuario WHERE id=?", (user_id,))
        user = self.cursor.fetchone()
        return user

    def get_account_by_user_id(self, user_id):
        self.cursor.execute("SELECT * FROM conta WHERE id_usuario=?", (user_id,))
        account = self.cursor.fetchone()
        return account

    def user_exists(self, user_id):
        self.cursor.execute("SELECT COUNT(*) FROM usuario WHERE id=?", (user_id,))
        count = self.cursor.fetchone()[0]
        return count > 0

    def credit_account(self, user_id, amount):
        self.cursor.execute("UPDATE conta SET saldo = saldo + ? WHERE id_usuario=?", (amount, user_id))
        self.conn.commit()

    def debit_account(self, user_id, amount):
        self.cursor.execute("UPDATE conta SET saldo = saldo - ? WHERE id_usuario=?", (amount, user_id))
        self.conn.commit()

    def autenticar_usuario(self, login, senha):
        self.cursor.execute("SELECT * FROM usuario WHERE login=? AND senha=?", (login, senha))
        user = self.cursor.fetchone()

        self.conn.close()

        return True if user else False
        
    def verificar_conta_existe(self, numero_conta):
        self.cursor.execute("SELECT * FROM conta WHERE numero=?", (numero_conta,))
        conta = self.cursor.fetchone()
        
        return True if conta else False
        
    def close(self):
        self.conn.close()