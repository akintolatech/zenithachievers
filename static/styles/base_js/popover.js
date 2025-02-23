  // Pop over 
  function togglePopOver(){

    let popOverItem = document.querySelector(".popover-item");
    let popOverBtn = document.querySelector(".popOverBtn");

    // Toggle popover using css scripting
    if (popOverBtn.className === "popOverBtn") {
        //popOverItem.style.transition = "all 500ms ease";
        popOverItem.style.display = "block";
        popOverBtn.className += " open"
        popOverBtn.style.transform = "rotate(45deg)";
    } else {
        popOverBtn.className = "popOverBtn"
        popOverBtn.style.transform = "rotate(0deg)";
        popOverItem.style.display = "none";
    }
    
}

let popOverBtn = document.querySelector(".popOverBtn");

popOverBtn.addEventListener("click", togglePopOver);
