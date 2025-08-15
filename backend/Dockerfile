FROM python:3.12-slim

# Define diretório de trabalho na imagem final
WORKDIR /app

# Instala dependências de runtime necessárias para mysqlclient funcionar
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev pkg-config default-libmysqlclient-dev poppler-utils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copia código da aplicação
COPY core /app/core
COPY src /app/src

# Copia dependências e instala com pip (sem cache, como usuário root)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN python manage.py collectstatic --noinput

# Expõe a porta usada pela aplicação (Django ou FastAPI)
EXPOSE 8000

# Comando padrão para iniciar a aplicação
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]
