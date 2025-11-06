FROM python:3.12-slim

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc libpq-dev pkg-config default-libmysqlclient-dev poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências Python primeiro (para cache)
COPY core /app/core

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia código da aplicação
COPY src /app/src

# Copia entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
WORKDIR /app/src

ENTRYPOINT ["/entrypoint.sh"]
