import sqlite3

class Db:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def autenticar_usuario(self, login, senha):
        self.cursor.execute("SELECT * FROM usuario WHERE login=? AND senha=?", (login, senha))
        user = self.cursor.fetchone()

        self.conn.close()

        return True if user else False
        
    def verificar_conta_existe(self, numero_conta):
        self.cursor.execute("SELECT * FROM conta WHERE numero=?", (numero_conta,))
        conta = self.cursor.fetchone()
        
        return True if conta else False
    
    def retornar_contas_removendo_conta_origem(self, numero_conta_origem):
        self.cursor.execute("SELECT numero FROM conta WHERE numero!=?", (numero_conta_origem,))
        contas = self.cursor.fetchall()
        contas = [contas[0] for contas in contas]
        
        return contas
        
    def close(self):
        self.conn.close()