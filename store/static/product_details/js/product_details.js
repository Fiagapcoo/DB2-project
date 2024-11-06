// Função para incrementar o valor
function increment() {
    const counterInput = document.getElementById("counter-value");
    let value = parseInt(counterInput.value);
    value++;
    counterInput.value = value;
}

// Função para decrementar o valor
function decrement() {
    const counterInput = document.getElementById("counter-value");
    let value = parseInt(counterInput.value);
    if (value > 1) { // Evita valores menores que 1
        value--;
    }
    counterInput.value = value;
}

// Verifica se o valor inserido manualmente é válido
document.getElementById("counter-value").addEventListener("input", function() {
    let value = parseInt(this.value);
    if (isNaN(value) || value < 1) {
        this.value = 1; // Define o valor mínimo como 1
    }
});
