class Unter {
    constructor() {
        this.socket = io('127.0.0.1:3000');
    }
}

class Provider extends Unter {
    constructor() {
        super();
        this.socket.emit('identify', 'provider');
        navigator.geolocation.watchPosition(this.updateLocation.bind(this));
    }

    updateLocation(location) {
        console.log(location);
        this.socket.emit('updateLocation', location);
    }

    available(data) {
        this.socket.emit('available', data);
    };
}

class Client extends Unter {
    constructor() {
        super();
        this.socket.emit('identify', 'client');
    }

    request() {
        navigator.geolocation.getCurrentPosition(location => {
            console.log(location);
            this.socket.emit('request', location);
        });
    };
}
