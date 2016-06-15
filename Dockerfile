FROM node

RUN mkdir /app
WORKDIR /app

# We launch npm install only if the requirements have changed
COPY package.json package.json
RUN npm install

COPY . .

CMD ["npm", "start"]