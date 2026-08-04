const form = document.getElementById("loginForm");
const message = document.getElementById("message");

function setMessage(text, type = "info") {
    message.innerText = text;
    const colors = { info: "text-slate-600", success: "text-emerald-700", error: "text-red-700" };
    message.className = `mt-5 min-h-6 text-sm font-semibold ${colors[type]}`;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const login = document.getElementById("login").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://127.0.0.1:5000/surveillant/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ login, password })
        });
        const data = await response.json();
        if (data.success) {
            localStorage.setItem("surveillant", JSON.stringify(data.data));
            setMessage("Connexion reussie", "success");
            window.location.href = "acceuil.html";
        } else {
            setMessage(data.message, "error");
        }
    } catch (error) {
        setMessage("Erreur serveur", "error");
    }
});
