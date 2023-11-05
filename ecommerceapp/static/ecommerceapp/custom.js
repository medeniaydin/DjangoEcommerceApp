<script>
    document.addEventListener("DOMContentLoaded", function() {
        var descriptionInput = document.getElementById("product_description");
    
        descriptionInput.addEventListener("input", function() {
            var maxChars = 250;
            var currentChars = this.value.length;
    
            if (currentChars > maxChars) {
                this.setCustomValidity("Ürün açıklaması 250 karakterden fazla olamaz.");
            } else {
                this.setCustomValidity("");
            }
        });
    });
 </script>