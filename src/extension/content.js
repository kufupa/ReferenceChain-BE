// Create the newstitch button and add it to the page
const createNewtitchButton = () => {
    // Check if button already exists
    if (document.getElementById("newstitch-button")) return;
    
    // Create button
    const button = document.createElement("button");
    button.id = "newstitch-button";
    button.textContent = "Newstitch";
    
    // Add event listener
    button.addEventListener("click", openSlidingPopup);
    
    // Add to page
    document.body.appendChild(button);
};

// Function to open the sliding popup
const openSlidingPopup = () => {
    // Check if the popup is already open
    if (document.getElementById("sliding-popup-container")) return;
    
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
};

// Initialize button when the page loads
document.addEventListener("DOMContentLoaded", createNewtitchButton);

// Also try to add the button when the script loads (for pages already loaded)
createNewtitchButton();