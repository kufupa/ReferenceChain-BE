const API_BASE_URL = 'http://127.0.0.1:5000/api'; // Flask backend URL

async function initializeNodes() {
    try {
        await chrome.tabs.query({ active: true, currentWindow: true }, async function (tabs) {
            if (tabs.length > 0) {
                let initialUrl = tabs[0].url;
                const response = await fetch(`${API_BASE_URL}/nodes`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: initialUrl })
                });

                const result = await response.json();
                console.log("Initial node response:", result);

                // Fetch the nodes after initializing
                fetchNodes();
            } else {
                console.log("No active tab found.");
            }
        });
        
    } catch (error) {
        console.error("Error initializing nodes:", error);
    }
}

async function fetchNodes() {
    try {
        const response = await fetch(`${API_BASE_URL}/nodes`);
        const data = await response.json();
        if (data.nodes) {
            console.log(data);
            renderNodes(data.nodes);
        } else {
            console.error("Invalid data format:", data);
        }
    } catch (error) {
        console.error("Error fetching nodes:", error);
    }
}

async function postNodeClick(nodeUrl) {
    try {
        const response = await fetch(`${API_BASE_URL}/nodes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: nodeUrl })
        });

        const result = await response.json();
        console.log("POST result:", result);
        fetchNodes(); // Refresh nodes after posting
    } catch (error) {
        console.error("Error posting node click:", error);
    }
}

function renderNodes(nodes) {
    const container = document.getElementById("node-container");
    container.innerHTML = "";
    nodes.forEach((node) => {
        const div = document.createElement("div");
        div.classList.add("node");
        div.textContent = node.title;
        div.onclick = () => postNodeClick(node.url);
        container.appendChild(div);
    });
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Only initialize when the tree.html page is loaded
window.onload = async () => {
    initializeNodes();
    
    // Wait a few seconds before fetching nodes
    await sleep(2000);

    // Try to fetch nodes every 5 seconds
    setInterval(fetchNodes, 5000);
};