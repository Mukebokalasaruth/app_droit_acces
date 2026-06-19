const form = document.getElementById("loginForm");
const message = document.getElementById("message");

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const login = document.getElementById("login").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://localhost:5000/comptable/login",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        login: login,
                        password: password
                    })
                }
            );

        const data = await response.json();

        if (data.success) {
            console.log(data.data)
            message.innerText = "Connexion réussie";

            // sauvegarder utilisateur
            localStorage.setItem("comptable", JSON.stringify(data.data));

            // redirection 
            window.location.href =
                "acceuil.html";

        } else {

            message.innerText =
                data.message;
        }

    } catch (error) {

        console.error(error);

        message.innerText =
            "Erreur serveur";
    }
});