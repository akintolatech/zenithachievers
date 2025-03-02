// Mobile menu toggle

$(document).ready(
  function(){

      $('.nav').click(

          function(){
              $('.pry-nav').toggleClass('open');

              // ham nav animation
              $('.bar1').toggleClass('active');
              $('.bar2').toggleClass('active');
              $('.bar3').toggleClass('active');
              $('.back-drop').show();
          }
          
      )

  }
)


console.log("Toggle function activated!");
const mobileMenu = document.querySelector(".ham-nav");
const sidebar = document.querySelector(".sidebar-item");

mobileMenu.addEventListener("click", () => {
  sidebar.classList.toggle("active");
});
