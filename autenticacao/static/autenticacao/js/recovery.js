document.addEventListener("DOMContentLoaded", function () {
    const recoveryForm = document.getElementById("recovery-form");
    const otpModal = document.getElementById("otpModal");
    const otpForm = document.getElementById("otp-form");
    const otpInputs = document.querySelectorAll(".otp-input");
    const resendBtn = document.getElementById("resend-btn");
    const timerSpan = document.getElementById("timer");
    const otpError = document.getElementById("otp-error");

    // Envio do formulário de recuperação
    recoveryForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const email = document.querySelector("input[name='email']").value.trim();
        if (!email) {
            alert("Por favor, insira um e-mail válido.");
            return;
        }

        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        fetch("/auth/password-recovery/", {
            method: "POST",
            headers: {
              "X-CSRFToken": csrfToken,
              "X-Requested-With": "XMLHttpRequest", 
              "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `email=${encodeURIComponent(email)}`,
          })
          .then(response => {
            if (!response.ok) {
              throw new Error("Erro ao processar requisição");
            }
            return response.json();
          })
          .then(data => {
            if (data.success) {
              otpModal.style.display = "block";
              startTimer();
            } else {
              alert("Erro: " + data.error);
            }
          })
          .catch(error => console.error("Erro:", error));
    });

    // Configurar inputs OTP
    otpInputs.forEach((input, index) => {
        input.addEventListener("input", function () {
            if (this.value.length === 1 && index < otpInputs.length - 1) {
                otpInputs[index + 1].focus();
            }
        });

        input.addEventListener("keydown", function (e) {
            if (e.key === "Backspace" && !this.value && index > 0) {
                otpInputs[index - 1].focus();
            }
        });
    });

    // Envio do formulário OTP
    otpForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const enteredOTP = Array.from(otpInputs)
            .map((input) => input.value.trim())
            .join("");

        if (enteredOTP.length !== 6 || isNaN(enteredOTP)) {
            otpError.textContent = "Por favor, insira um código OTP válido.";
            otpError.style.display = "block";
            return;
        }

        fetch("/auth/verificar-otp/", {
            method: "POST",
            headers: {
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ otp: enteredOTP }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Erro ao verificar OTP");
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                window.location.href = "/auth/reset-password/";
            } else {
                otpError.textContent = "Código incorreto. Por favor, tente novamente.";
                otpError.style.display = "block";
            }
        })
        .catch(error => console.error("Erro:", error));
    });

    // Função para iniciar o timer
    function startTimer() {
        let timeLeft = 60;
        resendBtn.disabled = true;

        const timer = setInterval(() => {
            timeLeft--;
            timerSpan.textContent = timeLeft;

            if (timeLeft <= 0) {
                clearInterval(timer);
                resendBtn.disabled = false;
                timerSpan.textContent = "60";
            }
        }, 1000);
    }


    resendBtn.addEventListener("click", function () {
        if (!this.disabled) {
            const emailInput = document.querySelector("input[name='email']").value.trim();
            if (!emailInput) {
                alert("Por favor, insira um e-mail válido.");
                return;
            }

            fetch("/auth/resend-otp/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ email: emailInput }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    startTimer();
                    otpError.style.display = "none";
                    otpInputs.forEach((input) => (input.value = ""));
                    otpInputs[0].focus();
                } else {
                    alert("Erro ao reenviar código!");
                }
            })
            .catch(error => console.error("Erro:", error));
        }
    });
});
