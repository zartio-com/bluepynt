export class SocketHandler {
  constructor() {
    this.callbacks = {};

    this._api_host = location.host;
    this._api_base = location.pathname.split('/').slice(0, -1).join('/');

    let existingSession = window.name;
    if (existingSession) {
        existingSession = "?clientId=" + existingSession;
    }

    this._ws = new WebSocket(`ws${window.location.protocol === "https:" ? "s" : ""}://${this._api_host}${this._api_base}/ws${existingSession}`);
    this._ws.onmessage = (event) => {
        const json = JSON.parse(event.data);
        this.handle(json.event, json.data);
    }
  }

  on(event, callback) {
    this.callbacks[event] = callback;
  }

  send(event, data) {
    this._ws.send(JSON.stringify({event, data}));
  }

  handle(event, data) {
    if (this.callbacks[event]) {
      this.callbacks[event](data);
    }
  }
}