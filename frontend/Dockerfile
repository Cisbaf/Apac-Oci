# Build stage
FROM node:18-slim AS builder
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install --frozen-lockfile

COPY tsconfig.json next.config.ts jest.config.js next-env.d.ts ./
COPY public ./public
COPY src ./src

RUN npm run build

# Production stage
FROM node:18-slim
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install --production --frozen-lockfile

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

EXPOSE 3000
CMD ["npm", "run", "start"]
