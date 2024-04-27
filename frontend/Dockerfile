

FROM node:21-alpine3.19

WORKDIR /mlchk

COPY yarn.lock package.json ./

RUN yarn install

COPY . .

EXPOSE 8000

CMD ["yarn", "dev", "--host", "0.0.0.0", "--port", "8000"]