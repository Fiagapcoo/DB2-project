document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const successModal = document.getElementById("successModal");
    const closeModalBtn = document.getElementById("closeModalBtn");

    // Função para abrir o modal de sucesso
    function openSuccessModal() {
        successModal.style.display = "flex";
    }

    // Função para redirecionar para a página de login ao fechar o modal
    function redirectToLogin() {
        successModal.style.display = "none";
        window.location.href = "{% url 'login' %}"; // Redireciona para a página de login
    }

    // Evento de envio do formulário
    form.addEventListener("submit", function(event) {
        event.preventDefault(); // Previne o envio imediato do formulário

        // Verifica se todos os campos estão válidos de acordo com os patterns
        if (form.checkValidity()) {
            openSuccessModal(); // Exibe o modal de sucesso
        } else {
            form.reportValidity(); // Mostra os erros de validação
        }
    });

    // Evento para redirecionar ao clicar no botão "Fazer Login"
    closeModalBtn.addEventListener("click", redirectToLogin);
});

document.querySelector('.toggle-password').addEventListener('click', function() {
    const passwordInput = document.querySelector('#password');
    const icon = this.querySelector('i');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    } else {
        passwordInput.type = 'password';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    }
});