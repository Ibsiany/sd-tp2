import threading
import ipaddress
import random
import datetime
import socket

RESOURCE_FILE = './shared.txt'
access_resource_verify = False
leader = {'ID': '', 'IP': ''}
HOST = 'localhost'  # Endereco IP do Servidor
PORT = 5000  # Porta que o Servidor esta
conexao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)

devices = [
    {'ID': '10', 'IP': '186.25.0.2'},
    {'ID': '20', 'IP': '186.25.0.3'},
    {'ID': '30', 'IP': '186.25.0.4'},
    {'ID': '40', 'IP': '186.25.0.5'},
]

# devices = []
devicesIps = []

fila = []
     
# def infoMaquinas():
#     # nomeHost = conexao.gethostname()
#     # ipHost = conexao.gethostbyname(nomeHost)

#     network = ipaddress.IPv4Network(f"{dest}/24", strict=False)

#     for ip in network.hosts():
#        devicesIps.append(str(ip))
#        print(ip)

#     devices.append(devicesIps)
#     print(devices)
# Define the list of dictionaries

# Find with 'ID'
def findDevice(id):
    for device in devices:
        if device['ID'] == id:
            return device

def ring_election(device, array, index):
    global leader 
    
    try:
        if device["ID"] not in array and len(devices) >= index:
            array.append(device["ID"])
            ring_election(devices[index+1],array,index+1)
        else:
            id = max(array)
            leader = findDevice(id)
            print(f"Novo lider eleito: {leader}")
    except Exception as e:
        return ring_election(devices[index-1],array,len(devices)-1)
     

def removeItemQueue(item, array):
    try:
        array.remove(item)
    except Exception as e:
        return e
    
# def defineId(devices):

#     staticIps = ['186.25.0.1', '186.25.0.2', '186.25.0.3', '186.25.0.4']

#     devices.clear()

#     for i, ip in enumerate(staticIps):
#                 id_maquina = random.randint(0,99)
#                 devices.append({"ID": id_maquina, "IP": ip})
#     return devices
    

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
    # defineId(devices)
    
    array = []
    
    while True:
        if(leader in  devices):
            print(f'Lider atual: {leader}')
            continue
        else:
            print('Eleger lider: ')
            ring_election(devices[0],array,0)

        access_resource_random = random.choice(devices)
        
        if(((access_resource_random["ID"] == leader["ID"]) or (len(fila) == 0)) and access_resource_verify == False):
            access_resource(access_resource_random)
        elif (access_resource_random["ID"]  == leader["ID"]  and access_resource_verify == True):
            fila.append(access_resource_random)
        else:
            solicitar_acesso_recurso(access_resource_random)
        
init()
