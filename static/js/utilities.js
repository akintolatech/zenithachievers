
// Website Loader:
// Check for resources against bandit to display the webpage

// Function to check image load status
function checkImagesLoaded() {

    const images = document.getElementsByTagNameNS("img");
    console.log(`images contain ${images.length}`)
    let loadedCount = 0;

    // Check each image's load status
    images.forEach((img) => {
        if (img.complete) {
            loadedCount++;
        } else {
            img.onload = () => {
                loadedCount++;
                updateLoaderStatus(loadedCount, images.length);
            };
        }
    });

    updateLoaderStatus(loadedCount, images.length);
}

// Update loader visibility based on loading progress
function updateLoaderStatus(loadedCount, totalCount) {

    const loader = document.getElementById('loader');
    const loadedPercentage = (loadedCount / totalCount) * 100;

    const mainElement = document.getElementById("main");
    mainElement.display = "none";

    if (loadedPercentage >= 80) {
        loader.style.display = 'none'; // Hide loader when 80% of images are loaded
    } else {
        loader.style.display = 'flex'; // Show loader if less than 80% are loaded
    }
}

// // Run the function to check image loading status when the page is loaded
window.onload = checkImagesLoaded;



//Price Formatter
// Get all elements with the "formatted-price" class
const priceElements = document.querySelectorAll('.formatted-price');

// Loop through each element and format the price with commas
priceElements.forEach(element => {
    // Parse the integer value and format it with commas
    const price = parseInt(element.textContent, 10);
    const formattedPrice = price.toLocaleString();
    // Update the element's content with the formatted price
    element.textContent = formattedPrice;
});

console.log("utilities module activated.....");