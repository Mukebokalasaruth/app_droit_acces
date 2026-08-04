const selectPromotion = document.getElementById("idPromotion");
const form = document.getElementById("promotionForm");
const studentsBody = document.getElementById("studentsBody");
const message = document.getElementById("message");

async function chargerPromotions() {
    try {
        const response = await fetch("http://127.0.0.1:5000/comptable/promotions");
        const data = await response.json();
        selectPromotion.innerHTML = '<option value="">Selectionner une promotion</option>';
        if (data.success) {
            data.data.forEach((promotion) => {
                const option = document.createElement("option");
                option.value = promotion.id;
                option.textContent = promotion.nom;
                selectPromotion.appendChild(option);
            });
        }
    } catch (error) {
        selectPromotion.innerHTML = '<option value="">Erreur de chargement</option>';
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    studentsBody.innerHTML = '<tr><td class="px-5 py-8 text-center text-slate-500" colspan="3">Chargement...</td></tr>';
    try {
        const response = await fetch(`http://127.0.0.1:5000/surveillant/verifier-par-promotion/${selectPromotion.value}`);
        const data = await response.json();

        if (!data.success) {
            studentsBody.innerHTML = `<tr><td class="px-5 py-8 text-center text-red-700" colspan="3">${data.message}</td></tr>`;
            return;
        }

        if (data.data.length === 0) {
            studentsBody.innerHTML = '<tr><td class="px-5 py-8 text-center text-slate-500" colspan="3">Aucun etudiant valide dans cette promotion.</td></tr>';
            return;
        }

        studentsBody.innerHTML = data.data.map((etudiant) => `
            <tr>
                <td class="px-5 py-4"><p class="font-bold">${etudiant.prenom} ${etudiant.nom}</p><p class="text-slate-500">${etudiant.postnom || ""}</p></td>
                <td class="px-5 py-4 font-semibold">${etudiant.matricule}</td>
                <td class="px-5 py-4"><span class="rounded-full bg-emerald-100 px-3 py-1 text-xs font-bold text-emerald-800">Autorise</span></td>
            </tr>
        `).join("");
        message.textContent = "";
    } catch (error) {
        studentsBody.innerHTML = '<tr><td class="px-5 py-8 text-center text-red-700" colspan="3">Impossible de contacter le serveur.</td></tr>';
    }
});

document.addEventListener("DOMContentLoaded", chargerPromotions);
