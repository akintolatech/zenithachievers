


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