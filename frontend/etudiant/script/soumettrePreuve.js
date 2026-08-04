const form = document.getElementById("form");
const message = document.getElementById("message");

function setMessage(text, type = "info") {
    message.innerText = text;
    const colors = { info: "text-slate-600", success: "text-emerald-700", error: "text-red-700" };
    message.className = `mt-5 min-h-6 text-sm font-semibold ${colors[type]}`;
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    try {
        const etudiant = JSON.parse(localStorage.getItem("etudiant"));
        if (!etudiant) {
            setMessage("Etudiant non connecte", "error");
            return;
        }

        const fichier = document.getElementById("file").files[0];
        if (!fichier) {
            setMessage("Selectionnez un fichier", "error");
            return;
        }

        const formData = new FormData();
        formData.append("file", fichier);
        formData.append("idEtudiant", etudiant.id);

        const response = await fetch("http://127.0.0.1:5000/etudiant/upload-preuve", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        if (data.success) {
            setMessage(data.message, "success");
            form.reset();
        } else {
            setMessage(data.message, "error");
        }
    } catch (error) {
        setMessage(error.message, "error");
    }
});
