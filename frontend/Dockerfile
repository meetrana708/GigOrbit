FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package.json ./
RUN npm install --legacy-peer-deps --silent

# Copy application code
COPY public ./public
COPY src ./src

EXPOSE 3000

CMD ["npm", "start"]