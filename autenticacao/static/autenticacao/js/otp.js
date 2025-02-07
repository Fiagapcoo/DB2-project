document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("recovery-form");
    const inputs = document.querySelectorAll(".otp-input");
  
    // Foco automático nos inputs
    inputs.forEach((input, index) => {
      input.addEventListener("input", () => {
        if (input.value.length === 1 && index < inputs.length - 1) {
          inputs[index + 1].focus();
        }
      });
  
      input.addEventListener("keydown", (e) => {
        if(e.key === "Backspace" && !input.value && index > 0){
          inputs[index - 1].focus();
        }
      });
    });
  
    // Submit via fetch
    form.addEventListener("submit", function(e) {
      e.preventDefault();
  
      const otpCode = Array.from(inputs).map(input => input.value).join("");
  
      // Aqui vais buscar o email ao input hidden
      const emailInput = document.querySelector('input[name="email"]');
      const userEmail = emailInput.value;
  
      // CSRF
      const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  
      fetch("/auth/send_otp/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({ otp: otpCode, email: userEmail })
      })
      .then(response => {
        if (!response.ok) {
          throw new Error("Erro ao validar código.");
        }
        return response.json();
      })
      .then(data => {
        if (data.success) {
          alert("OTP validado com sucesso!");
          
           window.location.href = "/auth/reset-password/?email=" + encodeURIComponent(userEmail);
        } else {
          alert(data.message || "Código inválido ou expirado!");
        }
      })
      .catch(err => {
        console.error(err);
        alert("Ocorreu um erro ao validar o código. Tente novamente.");
      });
    });
  });
  