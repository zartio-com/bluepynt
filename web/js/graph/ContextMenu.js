
export class ContextMenu
{
    /** @type {Editor} */
    #editor;

    /** @type {HTMLElement} */
    #element;

    /** @type {Graph} */
    #graphContext = null;

    /** @type {{x: number, y: number}} */
    #graphPosition = { x: 0, y: 0 };

    /**
     *
     * @param editor
     */
    constructor(editor) {
        this.#editor = editor;
        this.#element = document.getElementById("context-menu");

        this.#setupEvents();
    }

    /**
     *
     * @param {Graph} graphContext
     * @param {number} x
     * @param {number} y
     * @param {{x: number, y: number}} graphPosition
     */
    showAt(graphContext, x, y, graphPosition) {
        this.#updateNodeData();
        this.#graphPosition = graphPosition;
        this.#graphContext = graphContext;
        this.#element.style.left = x + "px";
        this.#element.style.top = y + "px";
        this.#element.style.display = "block";
    }

    hide() {
        this.#element.style.display = "none";
    }

    get element() {
        return this.#element;
    }

    #updateNodeData() {
        this.#element.innerHTML = "";
        this.#editor.nodeData.forEach((nodeData) => {
            let item = document.createElement("div");
            item.classList.add("context-menu-item");
            item.innerHTML = nodeData.name;
            item.addEventListener("click", () => {
                if (this.#graphContext === null) {
                    return;
                }

                this.#graphContext.addNode(nodeData, this.#graphPosition.x, this.#graphPosition.y);
                this.hide();
            });

            this.#element.appendChild(item);
        });
    }

    #setupEvents() {
        document.addEventListener("click", () => {
            this.hide();
        });
    }
}