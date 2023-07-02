import repository

def verificar_usuario_autenticado(mensagem):
    return True if mensagem['autenticado'] == 1 else False

def verificar_dados_mensagem():
    pass

def verificar_contas_existentes(mensagem):
    db = repository.Db("bank_database.db")
    protocolo = mensagem["mensagem"].split("|")
    
    user_origem = protocolo[0].lstrip("0")
    
    user_destino = 0
    if mensagem['funcao']==3:
        user_destino = mensagem[1].lstrip("0")
    
    conta_origem_existente = db.verificar_conta_existe(user_origem)
    conta_destino_existente = True if user_destino == 0 else db.verificar_conta_existe(user_destino)
    
    return conta_destino_existente and conta_origem_existente
    

def verificar_tipo_mensagem(mensagem):
    return True if mensagem["funcao"] in [1,3,5,7] else False

def executar_verificações(mensagem):
    if mensagem["funcao"] == 7:
        return verificar_contas_existentes(mensagem)
    else:
        return verificar_usuario_autenticado(mensagem) and verificar_contas_existentes(mensagem) and verificar_tipo_mensagem(mensagem)