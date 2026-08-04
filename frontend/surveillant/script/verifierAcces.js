const form = document.getElementById("verifyForm");
const resultCard = document.getElementById("resultCard");

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const matricule = document.getElementById("matricule").value.trim();
    resultCard.innerHTML = "Verification en cours...";

    try {
        const response = await fetch(`http://127.0.0.1:5000/surveillant/verifier-droit-acces/${matricule}`);
        const data = await response.json();

        if (!data.success) {
            resultCard.innerHTML = `<p class="font-semibold text-red-700">${data.message}</p>`;
            return;
        }

        const allowed = data.data.autorisation === true;
        resultCard.className = `mt-8 rounded-lg border p-6 ${allowed ? "border-emerald-200 bg-emerald-50" : "border-red-200 bg-red-50"}`;
        resultCard.innerHTML = `
            <div class="flex flex-wrap items-start justify-between gap-4">
                <div>
                    <p class="text-sm font-semibold uppercase tracking-[.18em] text-slate-500">${data.data.matricule}</p>
                    <h2 class="mt-2 text-2xl font-bold">${data.data.prenom} ${data.data.nom} ${data.data.postnom || ""}</h2>
                    <p class="mt-2 text-slate-700">Statut: <strong>${data.data.validite}</strong></p>
                    ${data.data.motifRejet ? `<p class="mt-3 text-sm text-red-800">Motif: ${data.data.motifRejet}</p>` : ""}
                    ${data.data.messageEntree ? `<p class="mt-3 text-sm font-semibold ${allowed ? "text-emerald-700" : "text-red-700"}">${data.data.messageEntree}</p>` : ""}
                </div>
                <span class="rounded-full px-4 py-2 text-sm font-bold ${allowed ? "bg-emerald-600 text-white" : "bg-red-600 text-white"}">${allowed ? "Autorise" : "Non autorise"}</span>
            </div>
        `;
    } catch (error) {
        resultCard.innerHTML = '<p class="font-semibold text-red-700">Impossible de contacter le serveur.</p>';
    }
});
