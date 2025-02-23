// Mobile menu toggle
console.log("Toggle function activated!");
const mobileMenu = document.querySelector(".ham-nav");
const sidebar = document.querySelector(".sidebar-item");

mobileMenu.addEventListener("click", () => {
  sidebar.classList.toggle("active");
});
// console.log("Toggle function activated!")
// const mobileMenu = document.querySelector('.ham-nav');
// const sidebar = document.querySelector('.sidebar-item');

// mobileMenu.addEventListener('click', () => {

//   // sidebar.style.display = sidebar.style.display === 'flex' ? 'none' : 'flex';

//   sidebar.style.height = sidebar.style.height === '150px' ? '100%' : '150px';
// });