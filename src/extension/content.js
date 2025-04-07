// Check if the popup is already open
if (!document.getElementById("sliding-popup-container")) {
    // Create container div
    let container = document.createElement("div");
    container.id = "sliding-popup-container";

    // Fetch and insert popup.html content
    fetch(chrome.runtime.getURL("popup.html"))
        .then(response => response.text())
        .then(html => {
            container.innerHTML = html;
            document.body.appendChild(container);

            // Slide in effect
            setTimeout(() => {
                container.style.right = "0";
            }, 100);

            // Set iframe src AFTER popup.html is added
            let iframe = document.getElementById("iframe");
            if (iframe) {
                iframe.src = chrome.runtime.getURL("tree.html");
            }

            // Add close functionality
            document.getElementById("close-btn").addEventListener("click", () => {
                container.style.right = "-100vw"; // Slide out
                setTimeout(() => container.remove(), 300);
            });
        });
}
