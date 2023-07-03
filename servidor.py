import socket
import threading
import json
import repository
import locker
import time

# Variaveis de conexão
Host = 'localhost'
Port = 59000

locker = threading.Lock()

# Criação e configuração do socket
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_servidor.bind((Host, Port))
socket_servidor.listen()

fila = []
clientes_conectados = []
logs = []

def realizar_autenticacao(mensagem, socket_edge, db):
    global logs
    login = mensagem['mensagem'].split('|')[0]
    senha = mensagem['mensagem'].split('|')[1].lstrip('0')
    
    protocolo = {"cliente": 0, "quantidade_de_atendimentos": 0}
    
    protocolo["cliente"] = login
    
    if db.autenticar_usuario(login, senha):
        mensagem['autenticado'] = 1
        mensagem['mensagem'] =  f"{login}|0000000000"
        clientes_conectados.append(protocolo)
    
    print(len(json.dumps(mensagem).encode()))   
    logs.append(mensagem)
    #retornando a mensagem para o cliente
    socket_edge.sendall(json.dumps(mensagem).encode())

def realizar_request(mensagem, socket_edge, db):
    global logs
    global clientes_conectados
    #recebe request
    print(mensagem)
    logs.append(mensagem)
    protocolo = mensagem
    usuario = protocolo['mensagem'].split('|')[0]
    
    time.sleep(2)

    #envia grant
    mensagem_grant = f"{usuario.zfill(4)}|0000000000"
    protocolo["funcao"] = 2
    protocolo["mensagem"] = mensagem_grant
    socket_edge.sendall(json.dumps(protocolo).encode())
    logs.append(protocolo)
    
    #recebe operation
    resposta_operation = socket_edge.recv(62).decode()
    protocolo = json.loads(resposta_operation)
    print("RECEBENDO OPERATION " )
    print(protocolo)
    logs.append(protocolo)
    
    #realiza operation
    mensagem_operation = protocolo['mensagem']
    mensagem_operation = mensagem_operation.split('|')
    conta_origem = mensagem_operation[0]
    conta_destino = mensagem_operation[1]
    valor = mensagem_operation[2]
    realizar_deposito(conta_origem, conta_destino, valor ,db)
    
    #envia respota
    resposta_operation = f"{usuario.zfill(4)}|0000000000"
    protocolo["funcao"] = 4
    protocolo["mensagem"] = resposta_operation
    socket_edge.sendall(json.dumps(protocolo).encode())
    
    #recebe release
    resposta_release = socket_edge.recv(62).decode()
    resposta_release = json.loads(resposta_release)
    print("RESPOSTA DO RELEASE ")
    print(resposta_release)
    logs.append(resposta_release)
    
    fila.remove("Cliente " + usuario)
    
    elemento = next((x for x in clientes_conectados if x["cliente"] == usuario), None)
    if elemento:
        elemento["quantidade_de_atendimentos"] += 1
    
def realizar_deposito(conta_origem, conta_destino, valor, db):
    global logs
    db = repository.Db("bank_database.db")
    if(db.executar_operacao_saque_transferencia(conta_origem, conta_destino, valor)):
        db.adicionar_trasancao_extrato(conta_origem, conta_destino, valor)
        logs.append(f"[INFO] Operação realizada com sucesso - {conta_origem} - {conta_destino} - {valor}")
        print("Operação realizada com sucesso")
    else:
        logs.append(f"[ERROR] Não foi possível realizar a operação, saldo insuficiente - {conta_origem} - {conta_destino} - {valor}")
        print("Não foi possível realizar a operação, saldo insuficiente")

def threaded_recebimento_do_edge(socket_edge):
    #instanciando o repositório
    db = repository.Db("bank_database.db")
    
    mensagem = socket_edge.recv(62).decode()
    mensagem = json.loads(mensagem)
    
    if mensagem['funcao'] == 7:
        realizar_autenticacao(mensagem, socket_edge, db)
        
    elif mensagem['funcao'] == 1:
        usuario = mensagem['mensagem'].split('|')[0]
        fila.append("Cliente " + usuario)
        #lock
        locker.acquire()
        realizar_request(mensagem, socket_edge, db)
        locker.release()
        #release
        
    socket_edge.close()

def thread_interface():
    global clientes_conectados
    global fila
    while True:
        print("Bem vindo ao Banco Bem Amigos")
        print("1 - Listar Operações dos usuarios")
        print("2 - Imprimir quantas vezes cada processo foi atendido")
        print("3 - Imprimir fila de pedidos atual")
        print("4 - Encerrar Execução")
        input_usuario = input("Digite a opção desejada: ")
        
        locker.acquire()
        if input_usuario == "1":
            print("Todas as operações:",logs)
        elif input_usuario == "2":
            print(clientes_conectados)
        elif input_usuario == "3":
            print(fila)
        elif input_usuario == "4":
            print("Encerrando execução")
            socket_servidor.close()
            break
        locker.release()

interface = threading.Thread(target=thread_interface)
interface.start()

if __name__ == "__main__":
    print('Servidor iniciado.')
    while True:
        # Espera por conexões de clientes
        socket_cliente, endereco_cliente = socket_servidor.accept()
        print(f'{endereco_cliente[0]}:{endereco_cliente[1]} conectou.')

        # Cria uma nova thread para lidar com o cliente
        thread_cliente = threading.Thread(target=threaded_recebimento_do_edge, args=([socket_cliente]))
        thread_cliente.start()
