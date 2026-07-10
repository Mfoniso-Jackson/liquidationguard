FROM node:22-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . ./

ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

CMD ["sh", "-c", "npm run start -- -p ${PORT:-3000}"]
