import threading
import ipaddress
import random
import datetime
import socket

HOST = 'localhost'  # Endereco IP do Servidor
PORT = 5000  # Porta que o Servidor esta
conexao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)

devices = [
    'Dispositivo1',
    'Dispositivo2',
    'Dispositivo3',
    'Dispositivo4',
]

devicesAux = []
devicesIps = []

RESOURCE_FILE = './shared.txt'
leader = {'ID': '', 'IP': ''}
access_resource_verify = False
fila = []
     
# def infoMaquinas():
#     # nomeHost = conexao.gethostname()
#     # ipHost = conexao.gethostbyname(nomeHost)

#     network = ipaddress.IPv4Network(f"{dest}/24", strict=False)

#     for ip in network.hosts():
#        devicesIps.append(str(ip))
#        print(ip)

#     devicesAux.append(devicesIps)
#     print(devicesAux)

def removeItemQueue(item, array):
    try:
        array.remove(item)
    except Exception as e:
        return e
    
def elect_leader(maquinas):
    #  Eleger um novo líder entre os dispositivos.
     leader = random.choice(maquinas)
     print(f"Novo lider eleito: {leader}")
     
def defineId(devices):
    for i, ip in enumerate(devices):
                id_maquina = str(i+1)
                devicesAux.append({"ID": id_maquina, "IP": ip})
    print(devicesAux)
    
    return devicesAux
    

def access_resource(maquina):
    access_resource_verify = True
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(RESOURCE_FILE, 'a') as file:
        file.write(f"ID: {maquina['ID']}, IP: {maquina['IP']} acessado em {timestamp}\n")
        
    removeItemQueue(maquina, fila)
    access_resource_verify = False

def solicitar_acesso_recurso(maquina):
    if(access_resource_verify == False):
        access_resource(maquina)
    else:
        fila.append(maquina)

def init():
    infos = defineId(devices)
    elect_leader(infos)
    
    # while True:
    if(leader in  devicesAux):
        print('Leader')
        # continue
    else:
        print('Eleger lider')
        elect_leader(devicesAux)

    access_resource_random = random.choice(devicesAux)
    
    if(((access_resource_random["ID"] == leader["ID"]) or (len(fila) == 0)) and access_resource_verify == False):
        access_resource(access_resource_random)
    elif (access_resource_random["ID"]  == leader["ID"]  and access_resource_verify == True):
        fila.append(access_resource_random)
    else:
        solicitar_acesso_recurso(access_resource_random)
            
    # infoMaquinas()
    # access_resource_random = random.choice(devicesAux)
    # removeItemQueue(access_resource_random,devicesAux)
    
init()

# def device_behaviour(device):
#     # Simular o comportamento de um dispositivo no sistema distribuído. 
#     while True:
#         time.sleep(random.randint(1, 10))  # Sleep aleatório para simular solicitações de acesso aleatório

#         if device == leader:
#             # Simular falha do líder
#             if random.random() < 0.1:  # 10% de chance de falha
#                 print(f"Lider {device['hostname']} falhou.")
#                 elect_leader()
#                 continue

#        # Simula solicitação de acesso ao recurso compartilhado
#         print(f"{device['hostname']} está solicitando acesso ao recurso compartilhado.")
#         if leader:
#             access_resource(device)
#             print(f"{device['hostname']} acessou o recurso compartilhado.")

