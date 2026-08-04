const selectPromotion = document.getElementById("idPromotion");
const message = document.getElementById("message");
const filterForm = document.getElementById("filterForm");
const preuvesBody = document.getElementById("preuvesBody");

function setMessage(text, type = "info") {
    message.textContent = text;
    const colors = { info: "text-slate-600", success: "text-emerald-700", error: "text-red-700" };
    message.className = `mt-5 min-h-6 text-sm font-semibold ${colors[type]}`;
}

function statutBadge(statut, motifRejet) {
    if (statut === true) return '<span class="rounded-full bg-emerald-100 px-3 py-1 text-xs font-bold text-emerald-800">Valide</span>';
    if (statut === false && motifRejet) return '<span class="rounded-full bg-red-100 px-3 py-1 text-xs font-bold text-red-800">Rejete</span>';
    return '<span class="rounded-full bg-amber-100 px-3 py-1 text-xs font-bold text-amber-800">En attente</span>';
}

function preuveUrl(chemin) {
    if (!chemin) return "#";
    return `http://127.0.0.1:5000/${chemin.replaceAll("\\", "/")}`;
}

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

async function chargerPreuves(idPromotion) {
    preuvesBody.innerHTML = '<tr><td class="px-5 py-8 text-center text-slate-500" colspan="6">Chargement des preuves...</td></tr>';

    try {
        const response = await fetch(`http://127.0.0.1:5000/comptable/preuves-promotion/${idPromotion}`);
        const data = await response.json();

        if (!data.success) {
            preuvesBody.innerHTML = `<tr><td class="px-5 py-8 text-center text-red-700" colspan="6">${data.message}</td></tr>`;
            return;
        }

        if (data.data.length === 0) {
            preuvesBody.innerHTML = '<tr><td class="px-5 py-8 text-center text-slate-500" colspan="6">Aucune preuve trouvee pour cette promotion.</td></tr>';
            return;
        }

        preuvesBody.innerHTML = data.data.map((preuve) => `
            <tr class="align-top">
                <td class="px-5 py-4">
                    <p class="font-bold">${preuve.prenom} ${preuve.nom}</p>
                    <p class="text-slate-500">${preuve.postnom || ""}</p>
                </td>
                <td class="px-5 py-4 font-semibold">${preuve.matricule}</td>
                <td class="px-5 py-4 text-slate-600">${preuve.dateSoumission || "-"}</td>
                <td class="px-5 py-4">${statutBadge(preuve.statutValidation, preuve.motifRejet)}</td>
                <td class="px-5 py-4"><a class="font-semibold text-brand hover:text-teal-900" href="${preuveUrl(preuve.cheminCapture)}" target="_blank" rel="noreferrer">Voir</a></td>
                <td class="px-5 py-4">
                    <div class="flex flex-wrap gap-2">
                        <button class="rounded-lg bg-emerald-600 px-3 py-2 text-xs font-bold text-white hover:bg-emerald-700" data-action="approve" data-id="${preuve.idPreuve}" type="button">Approuver</button>
                        <button class="rounded-lg bg-red-600 px-3 py-2 text-xs font-bold text-white hover:bg-red-700" data-action="reject" data-id="${preuve.idPreuve}" type="button">Rejeter</button>
                    </div>
                </td>
            </tr>
        `).join("");
    } catch (error) {
        preuvesBody.innerHTML = '<tr><td class="px-5 py-8 text-center text-red-700" colspan="6">Impossible de contacter le serveur.</td></tr>';
    }
}

async function changerStatut(idPreuve, action) {
    const isReject = action === "reject";
    let options = { method: "PUT" };

    if (isReject) {
        const motifRejet = prompt("Motif du rejet");
        if (!motifRejet) return;
        options = {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ motifRejet })
        };
    }

    const endpoint = isReject ? "rejeter-paiement" : "approuver-paiement";
    try {
        const response = await fetch(`http://127.0.0.1:5000/comptable/${endpoint}/${idPreuve}`, options);
        const data = await response.json();
        if (data.success) {
            setMessage(data.message, "success");
            await chargerPreuves(selectPromotion.value);
        } else {
            setMessage(data.message, "error");
        }
    } catch (error) {
        setMessage("Impossible de mettre a jour le statut.", "error");
    }
}

filterForm.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!selectPromotion.value) {
        setMessage("Selectionnez une promotion.", "error");
        return;
    }
    setMessage("");
    chargerPreuves(selectPromotion.value);
});

preuvesBody.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-action]");
    if (!button) return;
    changerStatut(button.dataset.id, button.dataset.action);
});

document.addEventListener("DOMContentLoaded", chargerPromotions);
