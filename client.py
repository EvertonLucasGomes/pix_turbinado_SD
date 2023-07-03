import socket
import threading
import json
import time
import repository

# Variaveis de conexão do servidor DNS
HostDNS = 'localhost'
PortDNS = 53

# Definindo os protocolos de comunicação
dnsProtocol = {"tipo": "1", "dominio": "bancoBemAmigos.com.br"}

#Seção do usuario
protocolo_de_envio = {"autenticado": 0,"funcao": 0 ,"mensagem": ""}

db = repository.Db("bank_database.db")

contas = []

#conectando com o servidor DNS 
socket_dns = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_dns.connect((HostDNS, PortDNS))

#obtendo dominio do load balancer
socket_dns.sendall(json.dumps(dnsProtocol).encode())

#recebendo o ip e a porta do servidor_dns
mensagem_dns = json.loads(socket_dns.recv(1024).decode())

socket_dns.close()

def thread_realizar_pix():
    for i in range(5):
        socket_balancer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_balancer.connect((host_load_balancer, int(port_load_balancer)))
    
        #enviar request
        mensagem_request = f"{login.zfill(4)}|0000|00000"
        protocolo_de_envio["funcao"] = 1
        protocolo_de_envio["mensagem"] = mensagem_request
        socket_balancer.sendall(json.dumps(protocolo_de_envio).encode())
        #recebe grant
        resposta_grant = socket_balancer.recv(62).decode()
        resposta_grant = json.loads(resposta_grant)
        print("GRANT RECEBIDO ")
        print(resposta_grant)
        #envia deposito
        mensagem_operation = f"{login.zfill(4)}|0000|00000"
        protocolo_de_envio["funcao"] = 3
        protocolo_de_envio["mensagem"] = mensagem_operation
        socket_balancer.sendall(json.dumps(protocolo_de_envio).encode())
        #recebe resposta
        resposta_operation = socket_balancer.recv(62).decode()
        resposta_operation = json.loads(resposta_operation)
        print("RESPOSTA DA OPERAÇÃO ")
        print(resposta_operation)
        #envia release
        mensagem_release = f"{login.zfill(4)}|0000000000"
        protocolo_de_envio["funcao"] = 5
        protocolo_de_envio["mensagem"] = mensagem_release
        socket_balancer.sendall(json.dumps(protocolo_de_envio).encode())
        
        socket_balancer.close()
        
def thread_interface():
    while True:
        print("Bem vindo ao Banco Bem Amigos")
        print("1 - ver saldo")
        print("2 - ver extrato")
        input_usuario = input("Digite a opção desejada: ")
        
        if input_usuario == "1":
            pass
        elif input_usuario == "2":
            pass

if len(mensagem_dns) == 2:
    host_load_balancer, port_load_balancer = mensagem_dns
    print(host_load_balancer, port_load_balancer)
    
    login = input("Digite seu login: ")
    senha = input("Digite sua senha: ")
    
    protocolo_de_envio["funcao"] = 7
    protocolo_de_envio["mensagem"] = f"{login}|{senha.zfill(10)}"

    #conexao com o servidor balancer
    socket_balancer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_balancer.connect((host_load_balancer, int(port_load_balancer)))
        
    mensagem = json.dumps(protocolo_de_envio)    
        
    #enviando mensagem para o servidor edge
    socket_balancer.sendall(mensagem.encode())
        
    resposta_login = socket_balancer.recv(62).decode()
    protocolo_de_envio = json.loads(resposta_login)
    
    socket_balancer.close()
    
    if protocolo_de_envio["autenticado"] == 1:
        
        contas = db.retornar_contas_removendo_conta_origem(login)
        
        print(contas)
        
        thread_pix = threading.Thread(target=thread_realizar_pix)
        thread_pix.start()
        
        interface = threading.Thread(target=thread_interface)
        interface.start()
        

        
    # time.sleep(2)
    
    # mensagem = "teste2"
    # socket_balancer.sendall(mensagem.encode())
    
    # socket_balancer.close()
    
else:
    print(mensagem_dns)