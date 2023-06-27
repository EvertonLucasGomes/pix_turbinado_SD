import socket
import threading
import json
import repository

# Variaveis de conexão
Host = 'localhost'
Port = 59000

# Criação e configuração do socket
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_servidor.bind((Host, Port))
socket_servidor.listen()

def realizar_autenticacao(mensagem, socket_edge):
    #instanciando o repositório
    db = repository.Db("bank_database.db")
    
    login = mensagem['mensagem'].split('|')[0]
    senha = mensagem['mensagem'].split('|')[1].lstrip('0')
    
    if db.autenticar_usuario(login, senha):
        mensagem['autenticado'] = 1
        mensagem['mensagem'] =  f"{login}|0000000000"
    
    print(len(json.dumps(mensagem).encode()))    
    #retornando a mensagem para o cliente
    socket_edge.sendall(json.dumps(mensagem).encode())

def threaded_recebimento_do_balancer(socket_edge):
    mensagem = socket_edge.recv(62).decode()
    mensagem = json.loads(mensagem)
    
    if mensagem['funcao'] == 7:
        realizar_autenticacao(mensagem, socket_edge)
    
    #socket_edge.sendall("chegou".encode())
    
    # mensagem = socket_edge.recv(51).decode()
    # print (mensagem)
    socket_edge.close()

if __name__ == "__main__":
    print('Servidor iniciado.')
    while True:
        # Espera por conexões de clientes
        socket_cliente, endereco_cliente = socket_servidor.accept()
        print(f'{endereco_cliente[0]}:{endereco_cliente[1]} conectou.')

        # Cria uma nova thread para lidar com o cliente
        thread_cliente = threading.Thread(target=threaded_recebimento_do_balancer, args=([socket_cliente]))
        thread_cliente.start()
