# Use uma imagem oficial do Python como base
FROM python:3.12-slim

# Impede que o Python gere arquivos .pyc e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho
WORKDIR /app

# Instala as dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends 
    build-essential 
    libpq-dev 
    && rm -rf /var/lib/apt/lists/*

# Instala as dependências do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do projeto
COPY . .

# Expõe a porta 8000
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
