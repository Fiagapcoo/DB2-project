async function loadCountries() {
    const response = await fetch('https://restcountries.com/v3.1/all'); // Requisição para a API de países
    const countries = await response.json(); // Converte a resposta para JSON

    const select = document.getElementById('country'); // Referência ao campo select
    countries.forEach(country => {
        const option = document.createElement('option'); // Cria um novo elemento <option>
        option.value = country.cca2; // Define o valor como o código do país
        option.textContent = country.name.common; // Define o nome do país como texto da opção
        select.appendChild(option); // Adiciona a opção ao select
    });
}

// Chama a função quando a página for carregada
window.onload = loadCountries;