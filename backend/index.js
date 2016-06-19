let app = require('express')();
let http = require('http').Server(app);
let io = require('socket.io')(http);

class Client {
    constructor(id, socket) {
        this.id = id;
        this.socket = socket;
        this.serviceWanted = false;
        this.position = null;
    }

    wants(position) {
        this.serviceWanted = true;
        this.position = position;
    }

    cancel() {
        this.serviceWanted = false;
    }
}

class Provider {
    constructor(id, socket) {
        this.id = id;
        this.socket = socket;
        this.position = null;
        this.available = false;
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
        socket.on('request', position => {
            console.log(`Client ${client.id} at "${position}"`);
            client.wants(position);
            this.dispatch(client);
        });
    }

    dispatch(client) {
        let availableProviders = this.providers.filter(provider => provider.available);
        console.log(`${availableProviders.length} providers are available`);
    }

    newProvider(socket) {
        let provider = new Provider(this.providers.length, socket);
        this.providers.push(provider);
        socket.on('updateLocation', location => {
            console.log(`Provider ${provider.id} is at ${location}`);
            provider.location = location;
        });
        socket.on('available', () => {
            console.log(`Provider ${provider.id} is available`);
            provider.available = true;
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