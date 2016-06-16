let app = require('express')();
let http = require('http').Server(app);
let io = require('socket.io')(http);

class Client {
    constructor(id, socket) {
        this.id = id;
        this.socket = socket;
    }
}

class Provider {
    constructor(id, socket) {
        this.id = id;
        this.socket = socket;
    }
}

class Dispatcher {
    constructor() {
        this.clients = [];
        this.providers = [];
    }

    newClient(socket) {
        let client = new Client(this.clients.length, socket);
        this.clients.push(client);
        socket.on('request', request => {
            console.log(`Client ${client.id} requested "${request}"`);
        });
    }

    newProvider(socket) {
        let provider = new Provider(this.providers.length, socket);
        this.providers.push(provider);
        socket.on('available', () => {
            console.log(`Provider ${provider.id} is available`);
        });
    }
}

let dispatcher = new Dispatcher();

io.on('connection', function (socket) {
    socket.on('identify', role => {
        switch (role.toLowerCase()) {
            case 'client':
                dispatcher.newClient(socket);
                break;
            case 'provider':
                dispatcher.newProvider(socket);
                break;
            default:
                throw new Error('Role does not exist');
        }
    });
});

http.listen(3000, function () {
    console.log('Listening on *:3000');
});