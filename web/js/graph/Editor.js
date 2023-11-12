import { ContextMenu } from "./ContextMenu.js";
import { ApiService } from "../ApiService.js";
import { NodeData } from "../api/NodeData.js";

export class Editor
{
    /** @type {ApiService} */
    #apiService;

    /** @type {ContextMenu} */
    #contextMenu;

    /** @type {NodeData[]} */
    #nodeData = [];

    constructor() {
        this.#apiService = new ApiService();
        this.#initializeNodeData();

        this.#contextMenu = new ContextMenu(this);
    }

    /**
     *
     * @returns {ContextMenu}
     */
    get contextMenu() {
        return this.#contextMenu;
    }

    /**
     *
     * @returns {ApiService}
     */
    get apiService() {
        return this.#apiService;
    }

    /**
     *
     * @returns {NodeData[]}
     */
    get nodeData() {
        return this.#nodeData;
    }

    async #initializeNodeData() {
        const nodeData = await this.#apiService.getNodes();
        this.#nodeData = nodeData.map((node) => {
            return new NodeData(node);
        });
    }
}