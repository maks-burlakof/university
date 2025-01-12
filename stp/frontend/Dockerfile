FROM node:20-alpine AS build

ENV WORKDIR=/app

WORKDIR ${WORKDIR}

COPY package*.json ${WORKDIR}/
RUN npm install

COPY . ${WORKDIR}/

EXPOSE 3000

CMD ["npm", "start"]
