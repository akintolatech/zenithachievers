// Mobile menu toggle
console.log("Toggle function activated!");
const mobileMenu = document.querySelector(".ham-nav");
const sidebar = document.querySelector(".sidebar-item");

mobileMenu.addEventListener("click", () => {
  sidebar.classList.toggle("active");
});
