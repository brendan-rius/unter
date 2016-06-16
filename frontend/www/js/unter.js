class Unter {
    constructor() {
        this.socket = io('127.0.0.1:3000');
    }

    identify(role) {
        this.role = role.toLowerCase();
        this.socket.emit('identify', this.role);
    }

    request(data) {
        if (this.role !== 'client') {
            throw new Error("You must be a client to request something");
        }
        this.socket.emit('request', data);
    };

    available(data) {
        if (this.role !== 'provider') {
            throw new Error("You must be a provider to provide something");
        }
        this.socket.emit('available', data);
    };
}
