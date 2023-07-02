import socket
import threading
import json
import edge_helpers

# Variaveis de conexão
Host = 'localhost'
Port = 57000

host_servidor = 'localhost'
port_servidor = 59000

# Criação e configuração do socket
socket_edge = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_edge.bind((Host, Port))
socket_edge.listen()

def processo_login(mensagem, socket_servidor, socket_balancer):
    #enviando mensagem para o servidor 
    socket_servidor.sendall(json.dumps(mensagem).encode())
            
    mensagem_servidor = socket_servidor.recv(62).decode()
    socket_balancer.sendall(mensagem_servidor.encode())

def processo_request(mensagem, socket_servidor ,soclet_balancer):
    #enviar request
    socket_servidor.sendall(json.dumps(mensagem).encode())
    #recebe grant
    resposta_grant = socket_servidor.recv(62).decode()
    #envia grant para cliente
    soclet_balancer.sendall(resposta_grant.encode())
    #recebe operation do cliente
    mensagem_operation = soclet_balancer.recv(62).decode()
    #envia operation
    socket_servidor.sendall(mensagem_operation.encode())
    #recebe resposta
    resposta_operation = socket_servidor.recv(62).decode()
    #envia resposta para cliente
    soclet_balancer.sendall(resposta_operation.encode())
    #recebe release do cliente
    mensagem_release = soclet_balancer.recv(62).decode()
    #envia release
    socket_servidor.sendall(mensagem_release.encode())

def threaded_recebimento_do_balancer(socket_balancer):
    while True:
        mensagem = socket_balancer.recv(62).decode()
        mensagem = json.loads(mensagem)
        
        if edge_helpers.executar_verificações(mensagem):
            socket_servidor= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_servidor.connect((host_servidor, port_servidor))
            
            if mensagem["funcao"] == 7:
                processo_login(mensagem, socket_servidor, socket_balancer)
            elif mensagem["funcao"] == 1:
                processo_request(mensagem, socket_servidor, socket_balancer)
            
if __name__ == "__main__":
    print('Servidor edge 1 iniciado.')
    while True:
        # Espera por conexões de clientes
        socket_cliente, endereco_cliente = socket_edge.accept()
        print(f'{endereco_cliente[0]}:{endereco_cliente[1]} conectou.')

        # Cria uma nova thread para lidar com o cliente
        thread_cliente = threading.Thread(target=threaded_recebimento_do_balancer, args=([socket_cliente]))
        thread_cliente.start()