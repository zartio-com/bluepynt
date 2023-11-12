export class ApiService {
  constructor() {
    this._api_host = location.host;
    this._api_base = location.pathname.split('/').slice(0, -1).join('/');
  }

  apiURL(route) {
    return this._api_base + route;
  }

  async fetchApi(route, options) {
    return (await fetch(this.apiURL(route), options)).json()
  }

  async getNodes() {
    return await this.fetchApi('/api/nodes');
  }

  /** @param {Graph} graph */
  async executeGraph(graph) {
    const json = graph.toJson();
    const response = await this.fetchApi('/api/execute', {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        "graphs": [json]
      }),
    });
  }
}