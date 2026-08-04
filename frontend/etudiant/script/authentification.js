const form = document.getElementById("loginForm");
const message = document.getElementById("message");

function setMessage(text, type = "info") {
    message.innerText = text;
    const colors = { info: "text-slate-600", success: "text-emerald-700", error: "text-red-700" };
    message.className = `mt-5 min-h-6 text-sm font-semibold ${colors[type]}`;
}

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const matricule = document.getElementById("matricule").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://localhost:5000/etudiant/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ matricule, password })
        });

        const data = await response.json();

        if (data.success) {
            setMessage("Connexion reussie", "success");
            localStorage.setItem("etudiant", JSON.stringify(data.data));
            window.location.href = "acceuil.html";
        } else {
            setMessage(data.message, "error");
        }
    } catch (error) {
        setMessage("Erreur serveur", "error");
    }
});
