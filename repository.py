import sqlite3
import random
import datetime
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
    
    def executar_operacao_saque_transferencia(self,conta_origem , conta_destino, valor):
        if(self.verificar_saldo_suficiente(conta_origem, valor)):
            self.cursor.execute("UPDATE conta SET saldo=saldo-? WHERE numero=?", (float(valor.lstrip("0")), conta_origem))
            self.cursor.execute("UPDATE conta SET saldo=saldo+? WHERE numero=?", (float(valor.lstrip("0")), conta_destino))
            self.conn.commit()
            return True
        else:
            return False

    def retornar_conta_aleatoria_removendo_conta_origem(self, numero_conta_origem):
        self.cursor.execute("SELECT numero FROM conta WHERE numero!=?", (numero_conta_origem,))
        contas = self.cursor.fetchall()
        contas = [contas[0] for contas in contas]
        
        conta_aleatoria = random.choice(contas)

        return conta_aleatoria
    
    def retornar_saldo(self, numero_conta):
        self.cursor.execute("SELECT saldo FROM conta WHERE numero=?", (numero_conta,))
        saldo = self.cursor.fetchone()
        
        return saldo[0]
    
    def verificar_saldo_suficiente(self, numero_conta, valor):
        saldo = self.retornar_saldo(numero_conta)
        
        if saldo >= float(valor.lstrip("0")):
            return True
        else:
            return False
    
    def adicionar_trasancao_extrato(self, conta_destino, conta_origem, valor):
        print("conta_transacao", conta_destino, conta_origem, valor )
        self.cursor.execute("INSERT INTO transacoes (id_usuario, valor,login_destino,data, hora) VALUES (?, ?, ?, ?, ?)", (conta_destino,valor,conta_origem , datetime.date.today().strftime("%d/%m/%Y"), datetime.datetime.now().strftime("%H:%M:%S")))
        self.conn.commit()

    def extrato_conta(self, numero_conta):
        self.cursor.execute("SELECT * FROM transacoes WHERE id_usuario=?", (numero_conta,))
        extrato = self.cursor.fetchall()
        
        return extrato

    def close(self):
        self.conn.close()