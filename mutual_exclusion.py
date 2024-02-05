import threading
import time
import random
import datetime
import socket

HOST = ''  # Endereco IP do Servidor
PORT = 5000  # Porta que o Servidor esta
conexao = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (HOST, PORT)
conexao.bind(orig)


# Arquivo compartilhado
RESOURCE_FILE = './shared.txt'

# Simulação de 4 dispositivos
devices = [
    {'id': 1, 'hostname': 'Dispositivo1'},
    {'id': 2, 'hostname': 'Dispositivo2'},
    {'id': 3, 'hostname': 'Dispositivo3'},
    {'id': 4, 'hostname': 'Dispositivo4'},
]

# Inicializando
leader = None

def elect_leader():
   # Eleger um novo líder entre os dispositivos.
    global leader
    leader = random.choice(devices)
    print(f"Novo lider eleito: {leader['hostname']}")

def access_resource(device):
   # Simular o acesso ao recurso compartilhado por um dispositivo.
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(RESOURCE_FILE, 'a') as file:
        file.write(f"{device['hostname']} acessado em {timestamp}\n")

def device_behaviour(device):
    # Simular o comportamento de um dispositivo no sistema distribuído. 
    while True:
        time.sleep(random.randint(1, 10))  # Sleep aleatório para simular solicitações de acesso aleatório

        if device == leader:
            # Simular falha do líder
            if random.random() < 0.1:  # 10% de chance de falha
                print(f"Lider {device['hostname']} falhou.")
                elect_leader()
                continue

       # Simula solicitação de acesso ao recurso compartilhado
        print(f"{device['hostname']} está solicitando acesso ao recurso compartilhado.")
        if leader:
            access_resource(device)
            print(f"{device['hostname']} accessed the shared resource.")

# Inicializando algoritmo de eleicao
elect_leader()

# Inicia comportamentos de dispositivos em threads separadas
for device in devices:
    threading.Thread(target=device_behaviour, args=(device,)).start()
