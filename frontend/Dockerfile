FROM node:21-alpine

WORKDIR ./
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
ENV PORT=8000
ENV REACT_APP_SERVER_URL=http://0.0.0.0:8000
ENV HOST=0.0.0.0
EXPOSE 8000
CMD ["npm", "start"]