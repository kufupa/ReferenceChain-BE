class Flashcard extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });

        const title = this.getAttribute("title") || "Title";
        const content = this.getAttribute("content") || "Content";
        const link = this.getAttribute("link") || "#";

        // Define the shadow DOM structure and styles
        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    width: 600px;
                    height: auto;
                    border-radius: 15px;
                    background-color: #fff;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    overflow: hidden;
                    transition: transform 0.3s ease;
                    margin: 20px;
                }

                :host(:hover) {
                    transform: scale(1.05);
                }

                /* Center the card on the screen */
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background-color: #f4f4f9;
                }

                .card-content {
                    display: block; /* Change to block for title above content */
                    padding: 20px;
                }

                #title {
                    font-size: 24px;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 10px;
                }

                #content {
                    font-size: 16px;
                    color: #666;
                    line-height: 1.5;
                    overflow-y: auto;
                    height: 100%;
                }

                #link {
                    display: inline-block;
                    margin-top: 15px;
                    font-size: 16px;
                    text-decoration: none;
                    color: #007BFF;
                }
            </style>

            <div class="card-content">
                <div id="title">${title}</div>
                <div id="content">${content}</div>
            </div>
        `;
    }

    static get observedAttributes() {
        return ["title", "content", "link"];
    }
    attributeChangedCallback(name, oldValue, newValue) {
        if (newValue !== null) {
            if ((name === "title") && this.shadowRoot.getElementById("title")) {
                this.shadowRoot.getElementById("title").textContent = newValue;
            }
            if ((name === "content") && this.shadowRoot.getElementById("content")) {
                this.shadowRoot.getElementById("content").textContent = newValue;
            }
            if ((name === "link") && this.shadowRoot.getElementById("link")) {
                this.shadowRoot.getElementById("link").href = newValue;
            }
        }
    }
}

// Define the custom element
customElements.define('flash-card', Flashcard);