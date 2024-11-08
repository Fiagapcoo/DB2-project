document.addEventListener('DOMContentLoaded', function() {
    const recoveryForm = document.getElementById('recovery-form');
    const otpModal = document.getElementById('otpModal');
    const otpForm = document.getElementById('otp-form');
    const otpInputs = document.querySelectorAll('.otp-input');
    const resendBtn = document.getElementById('resend-btn');
    const timerSpan = document.getElementById('timer');
    const otpError = document.getElementById('otp-error');

    // Código OTP estático para teste
    const STATIC_OTP = "123456";
    
    // Manipular envio do formulário de recuperação
    recoveryForm.addEventListener('submit', function(e) {
        e.preventDefault();
        otpModal.style.display = 'block';
        startTimer();
    });

    // Configurar inputs OTP
    otpInputs.forEach((input, index) => {
        input.addEventListener('input', function() {
            if (this.value.length === 1) {
                if (index < otpInputs.length - 1) {
                    otpInputs[index + 1].focus();
                }
            }
        });

        input.addEventListener('keydown', function(e) {
            if (e.key === 'Backspace' && !this.value) {
                if (index > 0) {
                    otpInputs[index - 1].focus();
                }
            }
        });
    });

    // Manipular envio do formulário OTP
    otpForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const enteredOTP = Array.from(otpInputs)
            .map(input => input.value)
            .join('');

        if (enteredOTP === STATIC_OTP) {
            window.location.href = '/auth/reset-password/';
        } else {
            otpError.textContent = 'Código incorreto. Por favor, tente novamente.';
            otpError.style.display = 'block';
        }
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
                timerSpan.textContent = '60';
            }
        }, 1000);
    }

    // Manipular reenvio de código
    resendBtn.addEventListener('click', function() {
        if (!this.disabled) {
            // Aqui você pode adicionar a lógica para reenviar o código
            startTimer();
            otpError.style.display = 'none';
            Array.from(otpInputs).forEach(input => input.value = '');
            otpInputs[0].focus();
        }
    });
});