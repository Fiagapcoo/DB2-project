$(document).ready(function() {
    // Show modals based on data attributes
    if ($("#successModal").data("show") === true) {
        $("#successModal").modal('show');
    }

    if ($("#errorModal").data("show") === true) {
        $("#errorModal").modal('show');
    }

    // Event listener for the "Fazer Login" button in the success modal
    $("#closeModalBtn").click(function() {
        window.location.href = $(this).data("login-url");
    });

    // Event listener for the "Fechar" button in the error modal
    $(".close-button").click(function() {
        $("#errorModal").modal('hide');
    });

    // Form validation
    $("form").submit(function(event) {
        if (this.checkValidity()) {
            // Form is valid; allow it to submit
        } else {
            event.preventDefault();
            this.reportValidity();
        }
    });
});
