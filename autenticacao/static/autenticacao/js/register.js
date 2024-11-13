document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const successModal = document.getElementById("successModal");
    const closeModalBtn = document.getElementById("closeModalBtn");

    // Function to redirect to login page when closing the modal
    function redirectToLogin() {
        window.location.href = "{% url 'login' %}"; // Redirect to login page
    }

    // Form submit event
    form.addEventListener("submit", function(event) {
        // Remove or comment out the next line to allow form submission
        // event.preventDefault(); // Prevent immediate form submission

        // Check if all fields are valid according to patterns
        if (form.checkValidity()) {
            // Form is valid; allow it to submit
            // Optionally, you can display a loading indicator here
        } else {
            event.preventDefault(); // Prevent submission if form is invalid
            form.reportValidity(); // Show validation errors
        }
    });

    // Event to redirect when clicking the "Fazer Login" button
    closeModalBtn.addEventListener("click", redirectToLogin);
});
