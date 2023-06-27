import socket
import threading
import json
import edge_helpers

# Variaveis de conexão
Host = 'localhost'
Port = 58000

host_servidor = 'localhost'
port_servidor = 59000

# Criação e configuração do socket
socket_edge = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_edge.bind((Host, Port))
socket_edge.listen()

def threaded_recebimento_do_balancer(socket_balancer):
    mensagem = socket_balancer.recv(62).decode()
    
    if edge_helpers.executar_verificações(mensagem):
        socket_servidor= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_servidor.connect((host_servidor, port_servidor))
        socket_servidor.sendall(mensagem.encode())
        
        mensagem_servidor = socket_servidor.recv(62).decode()
        socket_balancer.sendall(mensagem_servidor.encode())

        
        
        # mensagem = socket_balancer.recv(51).decode()
        # socket_servidor.sendall(mensagem.encode())
        
    socket_balancer.close()

if __name__ == "__main__":
    print('Servidor edge 2 iniciado.')
    while True:
        # Espera por conexões de clientes
        socket_cliente, endereco_cliente = socket_edge.accept()
        print(f'{endereco_cliente[0]}:{endereco_cliente[1]} conectou.')

        # Cria uma nova thread para lidar com o cliente
        thread_cliente = threading.Thread(target=threaded_recebimento_do_balancer, args=([socket_cliente]))
        thread_cliente.start()
