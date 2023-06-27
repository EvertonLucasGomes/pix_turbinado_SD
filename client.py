import socket
import threading
import json
import time

# Variaveis de conexão do servidor DNS
HostDNS = 'localhost'
PortDNS = 53

# Definindo os protocolos de comunicação
dnsProtocol = {"tipo": "1", "dominio": "bancoBemAmigos.com.br"}

#Seção do usuario
protocolo_de_envio = {"autenticado": 0,"funcao": 0 ,"mensagem": ""}

#conectando com o servidor DNS 
socket_dns = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_dns.connect((HostDNS, PortDNS))

#obtendo dominio do load balancer
socket_dns.sendall(json.dumps(dnsProtocol).encode())

#recebendo o ip e a porta do servidor_dns
mensagem_dns = json.loads(socket_dns.recv(1024).decode())

socket_dns.close()

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
        
    mensagem_servidor = socket_balancer.recv(51).decode()
    print(mensagem_servidor)
    
    socket_balancer.close()
    
    
        
    # time.sleep(2)
    
    # mensagem = "teste2"
    # socket_balancer.sendall(mensagem.encode())
    
    # socket_balancer.close()
    
else:
    print(mensagem_dns)