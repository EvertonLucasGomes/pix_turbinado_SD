import socket
import threading
import json

# Variaveis de conexão
Host = 'localhost'
Port = 53

# Criação e configuração do socket
socket_consumidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_consumidor.bind((Host, Port))
socket_consumidor.listen()

#banco do servidor DNS
links = {"bancoBemAmigos.com.br": ("localhost", "56000")}

def threaded_recebimento_dados_cliente(socket):
    mensagem = socket.recv(1024).decode()
    mensagem = json.loads(mensagem)
    
    if mensagem["tipo"] == "1":
        if mensagem["dominio"] in links:
            socket.sendall(json.dumps(links[mensagem["dominio"]]).encode())
        else:
            socket.sendall(json.dumps("dominio nao encontrado").encode())
    
    socket.close()

if __name__ == "__main__":
    print('Servidor DNS iniciado.')
    while True:
        # Espera por conexões de clientes
        socket_cliente, endereco_cliente = socket_consumidor.accept()
        print(f'{endereco_cliente[0]}:{endereco_cliente[1]} conectou.')

        # Cria uma nova thread para lidar com o cliente
        thread_cliente = threading.Thread(target=threaded_recebimento_dados_cliente, args=([socket_cliente]))
        thread_cliente.start()
