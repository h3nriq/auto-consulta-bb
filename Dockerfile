# Use a imagem oficial do Python como base
FROM python:3.8-slim

# Instalação de utilitários necessários e libs para o Chrome
RUN apt-get update && apt-get install -y wget gnupg2 unzip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instala o Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos do projeto para o contêiner
COPY . .

# Instala as dependências do Python a partir do arquivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Comando para executar o bot
CMD ["python", "bot.py"]
