# Etapa base
FROM node:18-slim

# Diretório de trabalho
WORKDIR /app

# Copia apenas os arquivos necessários para instalar dependências
COPY package.json package-lock.json ./

# Instala as dependências
RUN npm install

# Copia o restante do código (após instalar dependências para melhor cache)
COPY tsconfig.json next.config.ts jest.config.js next-env.d.ts .env ./
COPY public ./public
COPY src ./src


# Comando para iniciar o servidor de desenvolvimento
CMD ["npm", "run", "dev"]
