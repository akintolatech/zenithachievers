
document.addEventListener('DOMContentLoaded', function(){
    const imageInput = document.getElementById('image_input_id');
    const imagePreview = document.getElementById('image_preview_id');

    imageInput.addEventListener('change', function(){
        const file = imageInput.files[0];
        if(file){
            const reader = new FileReader();

            reader.onload = function(e){
                imagePreview.src = e.target.result;
                imagePreview.style.display = "block";
            }

            reader.readAsDataURL(file);
        }else{
                imagePreview.src = "";
                imagePreview.style.display = "none";
        }
    });

});