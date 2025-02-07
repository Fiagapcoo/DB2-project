document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("reset-form");

  form.addEventListener("submit", function(e) {
    e.preventDefault();
    const formData = new FormData(form);

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const params = new URLSearchParams(window.location.search);
    const userEmail = params.get("email") || "";
    const userSegredo = params.get("segredo") || "";  // Lê o segredo da URL

    // Inclui email e segredo na query string do fetch
    fetch(`/auth/reset-password/?email=${encodeURIComponent(userEmail)}&segredo=${encodeURIComponent(userSegredo)}`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken
      },
      body: formData
    })
    .then(response => {
      return response.json().then(data => ({
        status: response.status,
        body: data
      }));
    })
    .then(({ status, body }) => {
      if (status >= 200 && status < 300) {
        alert(body.message || "Password alterada com sucesso!");
        window.location.href = "/auth";
      } else {
        alert(body.error || "Ocorreu um erro ao alterar a password.");
      }
    })
    .catch(err => {
      console.error("Erro inesperado:", err);
      alert("Erro inesperado ao tentar redefinir a senha.");
    });
  });
});