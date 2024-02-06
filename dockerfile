FROM ubuntu:latest

# Atualizar pacotes
RUN apt-get update && \
    apt-get install -y iputils-ping

RUN apt-get update && apt-get install -y python3

# Copiar arquivos
COPY . /app

# Definir um diretório
WORKDIR /app

# Comando para iniciar script
CMD ["python3", "main.py"] 

## teste

FROM python:3.7

WORKDIR /app

COPY . /app

RUN pip install ping3

CMD ["python", "./main.py"]
