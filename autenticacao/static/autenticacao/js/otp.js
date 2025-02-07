document.addEventListener("DOMContentLoaded", function () {
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
      if (e.key === "Backspace" && !input.value && index > 0) {
        inputs[index - 1].focus();
      }
    });
  });

  // Intercepta o submit do formulário para enviar via fetch
  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // Obtém o código OTP dos inputs (concatenando todos)
    const otpCode = Array.from(inputs)
      .map(input => input.value)
      .join("");

    // Obtém o email do input hidden
    const emailInput = document.querySelector('input[name="email"]');
    const userEmail = emailInput.value.trim();

    // Obtém o token CSRF
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    // Faz POST via fetch – note que não enviamos o "segredo" pois ele vem do backend
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
          // Redireciona para a página de reset de senha, passando email e segredo na query string
          window.location.href =
            "/auth/reset-password/?email=" +
            encodeURIComponent(userEmail) +
            "&segredo=" +
            encodeURIComponent(data.segredo);
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