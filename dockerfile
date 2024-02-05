FROM ubuntu:latest

# Atualizar pacotes
RUN apt-get update && \
    apt-get install -y iputils-ping

# Instalar Python
RUN apt-get install -y python3

# Copiar arquivos
COPY . /app

# Definir um diretório
WORKDIR /app

# Comando para iniciar script
CMD ["python3", "main.py"] 
