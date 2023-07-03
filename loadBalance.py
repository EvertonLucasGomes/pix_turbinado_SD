import socket
import threading
import json

# Variaveis de conexão do servidor Load Balancer
host = 'localhost'
port = 56000

# Variaveis de conexão dos servidores Edge Computing
host_edge_computing_server_1 = 'localhost'
port_edge_computing_server_1 = 57000

host_edge_computing_server_2 = 'localhost'
port_edge_computing_server_2 = 58000

# Criação e configuração do socket do servidor Load Balancer
socket_balancer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_balancer.bind((host, port))
socket_balancer.listen()

def processo_login(mensagem, socket_edge, socket_cliente):
    #enviando mensagem para o servidor edge
    socket_edge.sendall(json.dumps(mensagem).encode())
    
    mensagem_servidor = socket_edge.recv(62).decode()
    socket_cliente.sendall(mensagem_servidor.encode())

def processo_request(mensagem, socket_edge, soclet_cliente):
    #enviar request
    socket_edge.sendall(json.dumps(mensagem).encode())
    #recebe grant
    resposta_grant = socket_edge.recv(62).decode()
    #envia grant para cliente
    soclet_cliente.sendall(resposta_grant.encode())
    #recebe operation do cliente
    mensagem_operation = soclet_cliente.recv(62).decode()
    #envia operation
    socket_edge.sendall(mensagem_operation.encode())
    #recebe resposta
    resposta_operation = socket_edge.recv(62).decode()
    #envia resposta para cliente
    soclet_cliente.sendall(resposta_operation.encode())
    #recebe release do cliente
    mensagem_release = soclet_cliente.recv(62).decode()
    #envia release
    socket_edge.sendall(mensagem_release.encode())

def threaded_direcionar_cliente(socket_cliente, sever):
    while True:
        mensagem = socket_cliente.recv(64).decode()
        
        if mensagem:
            #obtendo edge direcionado
            host_edge = host_edge_computing_server_1 if sever == 0 else host_edge_computing_server_2
            port_edge = port_edge_computing_server_1 if sever == 0 else port_edge_computing_server_2
            
            #conexao com o servidor edge
            socket_edge_computing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_edge_computing.connect((host_edge, port_edge))
            
            mensagem = json.loads(mensagem)
            
            if mensagem["funcao"] == 7:
                processo_login(mensagem, socket_edge_computing, socket_cliente)
            elif mensagem["funcao"] == 1:
                processo_request(mensagem, socket_edge_computing, socket_cliente)
                
var = 0

if __name__ == "__main__":
    print('Load balancer iniciado.')
    while True:
        # Espera por conexões de clientes
        socket_cliente, endereco_cliente = socket_balancer.accept()
        print(f'{endereco_cliente[0]}:{endereco_cliente[1]} conectou.')

        # Cria uma nova thread para lidar com o cliente
        thread_cliente = threading.Thread(target=threaded_direcionar_cliente, args=(socket_cliente, var))
        thread_cliente.start()
        
        var = 0 if var == 1 else 1