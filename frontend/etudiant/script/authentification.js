const form = document.getElementById("loginForm");
const message = document.getElementById("message");

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const matricule = document.getElementById("matricule").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://localhost:5000/etudiant/login",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        matricule: matricule,
                        password: password
                    })
                }
            );

        const data = await response.json();

        if (data.success) {
            console.log(data.data)
            message.innerText = "Connexion réussie";

            // sauvegarder utilisateur
            localStorage.setItem("etudiant", JSON.stringify(data.data));

            // redirection 
            window.location.href =
                "acceuil.html";

        } else {

            message.innerText = data.message;
        }

    } catch (error) {

        console.error(error);

        message.innerText = "Erreur serveur";
    }
});