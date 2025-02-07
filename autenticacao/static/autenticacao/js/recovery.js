document.addEventListener("DOMContentLoaded", function () {
    const recoveryForm = document.getElementById("recovery-form");
  
    recoveryForm.addEventListener("submit", function (e) {
      e.preventDefault(); // Impede o envio normal do form
  
      // Ler o email inserido
      const emailInput = recoveryForm.querySelector('input[name="email"]');
      const email = emailInput.value.trim();
  
      // CSRF token, gerado pelo {% csrf_token %} dentro do <form>
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  
      // Faz POST via fetch
      fetch("/auth/password_recovery/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({ email: email })
      })
      .then(response => {
        if (!response.ok) {
         throw new Error("Erro ao enviar pedido de recuperação.");
        }
        return response.json();
      })
      .then(data => {
        if (data.success) {
    
        window.location.href = "/auth/send_otp/?email=" + encodeURIComponent(email);
        } else {
      
          alert(data.message || "Falha ao recuperar a palavra-passe.");
        }
      })
      .catch(error => {
        console.error(error);
        alert("Ocorreu um erro. Tenta novamente mais tarde.");
      });
    });
  });
  