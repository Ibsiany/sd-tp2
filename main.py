import random
import datetime
import socket
from ping3 import ping

RESOURCE_FILE = './shared.txt'
access_resource_verify = False
leader = {'ID': '', 'IP': ''}
HOST = 'localhost'  # Endereco IP do Servidor
PORT = 5000  # Porta que o Servidor esta
conexao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)

fila = []
array = []

def get_active_ips(): 
    devicesIds = []
    devices = []
    
    for ip_machine in range(2, 6):
        ip = f"172.20.0.{ip_machine}"
        if ping(ip) != False:
            devicesIds.append(ip_machine)
            devices.append({"ID": ip_machine, "IP": ip})
        
    return devices,devicesIds

# devices = [
#     {'ID': '10', 'IP': '186.25.0.2'},
#     {'ID': '20', 'IP': '186.25.0.3'},
#     {'ID': '30', 'IP': '186.25.0.4'},
#     {'ID': '40', 'IP': '186.25.0.5'},
# ]

# Find with 'ID'
def find_device(id,devices):
    for device in devices:
        if device['ID'] == id:
            return device

def ring_election(device, index, devices):
    global leader 
    global array 
    
    try:
        if device["ID"] not in array and len(devices) >= index:
            array.append(device["ID"])
            ring_election(devices[index+1],index+1)
        else:
            id = max(array)
            leader = find_device(id,devices)
            array = []
            print(f"Novo lider eleito: {leader}")
    except Exception as e:
        return ring_election(devices[index-1],len(devices)-1,devices)

def remove_item_queue(item, array):
    try:
        array.remove(item)
    except Exception as e:
        return e

def access_resource(maquina):
    access_resource_verify = True
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(RESOURCE_FILE, 'a') as file:
        file.write(f"ID: {maquina['ID']}, IP: {maquina['IP']} acessado em {timestamp}\n")
        
    remove_item_queue(maquina, fila)
    access_resource_verify = False

def solicitar_acesso_recurso(maquina):
    if(access_resource_verify == False):
        access_resource(maquina)
    else:
        fila.append(maquina)

def mutual_exclusion(access_resource_random):
    if(((access_resource_random["ID"] == leader["ID"]) or (len(fila) == 0)) and access_resource_verify == False):
        access_resource(access_resource_random)
    elif (access_resource_random["ID"]  == leader["ID"]  and access_resource_verify == True):
        fila.append(access_resource_random)
    else:
        solicitar_acesso_recurso(access_resource_random)

def init():
    # print("ola")
    
    # defineId()
    
    # print(devices)
    
    while True:
        devices,devicesIds = get_active_ips()
        
        if(devices == []):
            print('Nenhum dispositivo encontrado')
            continue
        else:
            if(leader in  devices and leader["ID"] == max(devicesIds)):
                print(f'Lider atual: {leader}')
                continue
            else:
                print('Eleger lider: ')
                ring_election(devices[0],0,devices)

            access_resource_random = random.choice(devices)
            
            mutual_exclusion(access_resource_random)
        
init()
