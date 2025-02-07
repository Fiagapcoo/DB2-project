document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("reset-form");
  
    form.addEventListener("submit", function(e) {
      e.preventDefault();
      const formData = new FormData(form);
  
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      // Se precisas do email na URL
      const params = new URLSearchParams(window.location.search);
      const userEmail = params.get("email") || "";
  
      fetch(`/auth/reset-password/?email=${encodeURIComponent(userEmail)}`, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken // Não colocar "Content-Type": "application/json"
        },
        body: formData
      })
      .then(response => {
        if (!response.ok) throw new Error("Erro ao enviar form");
        return response.json();
      })
      .then(data => {
        if (data.success) {
          alert(data.message || "Password alterada com sucesso!");
          window.location.href = "/";
        } else {
          alert(data.error || "Ocorreu um erro ao alterar a password.");
        }
      })
      .catch(err => {
        console.error(err);
        alert("Erro inesperado.");
      });
    });
  });
  