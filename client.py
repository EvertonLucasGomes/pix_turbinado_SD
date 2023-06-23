import socket
import threading
import json

# Variaveis de conexão do servidor DNS
HostDNS = 'localhost'
PortDNS = 53

# Definindo os protocolos de comunicação
dnsProtocol = {"tipo": "1", "dominio": "bancoBemAmigos.com.br"}
loadBalancerProtocol = {"tipo": "2", }

#conectando com o servidor DNS 
socket_dns = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_dns.connect((HostDNS, PortDNS))

#obtendo dominio do load balancer
socket_dns.sendall(json.dumps(dnsProtocol).encode())

#recebendo o ip e a porta do servidor_dns
mensagem_dns = json.loads(socket_dns.recv(1024).decode())

socket_dns.close()

if len(mensagem_dns) == 2:
    HostLoadBalancer, PortLoadBalancer = mensagem_dns
    print(HostLoadBalancer, PortLoadBalancer)
    
else:
    print(mensagem_dns)