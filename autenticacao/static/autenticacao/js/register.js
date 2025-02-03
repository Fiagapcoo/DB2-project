document.addEventListener("DOMContentLoaded", function() {
    const togglePassword = document.querySelector(".toggle-password");
    const passwordInput = document.getElementById("password");
    const eyeIcon = togglePassword.querySelector("i");

    togglePassword.addEventListener("click", function() {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            eyeIcon.classList.remove("fa-eye-slash");
            eyeIcon.classList.add("fa-eye");
        } else {
            passwordInput.type = "password";
            eyeIcon.classList.remove("fa-eye");
            eyeIcon.classList.add("fa-eye-slash");
        }
    });

    // Lógica para exibir os modais corretamente
    const successModal = document.getElementById("successModal");
    const errorModal = document.getElementById("errorModal");
    const closeErrorModalBtn = document.getElementById("closeErrorModalBtn");

    // Pegamos os atributos do body
    const success = document.body.getAttribute("data-success") === "true";
    const error = document.body.getAttribute("data-error") === "true";

    if (success && !error) {
        successModal.style.display = "block";
    }

    if (error && !success) {
        errorModal.style.display = "block";
    }

    // Fechar modal de erro ao clicar no botão
    if (closeErrorModalBtn) {
        closeErrorModalBtn.addEventListener("click", function() {
            errorModal.style.display = "none";
        });
    }
});
