# Etapa base
FROM node:18-slim

# Diretório de trabalho
WORKDIR /app

# Copia apenas os arquivos necessários para instalar dependências
COPY package.json package-lock.json ./

# Instala as dependências
RUN npm install

# Copia o restante do código
COPY tsconfig.json next.config.ts jest.config.js next-env.d.ts ./
COPY public ./public
COPY src /app/src

# Exponha a porta padrão do Next.js
EXPOSE 3000

# Comando para iniciar o servidor em produção
CMD ["npm", "run", "dev"]
