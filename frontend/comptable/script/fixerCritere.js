const selectPromotion = document.getElementById("idPromotion");
const form = document.getElementById("critereForm");
const message = document.getElementById("message");

function setMessage(text, type = "info") {
    message.innerText = text;
    const colors = { info: "text-slate-600", success: "text-emerald-700", error: "text-red-700" };
    message.className = `mt-5 min-h-6 text-sm font-semibold ${colors[type]}`;
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

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const montant = document.getElementById("montant").value;
    const session = document.getElementById("session").value;
    const idPromotion = document.getElementById("idPromotion").value;

    try {
        const response = await fetch("http://127.0.0.1:5000/critere/critere-paiement", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                montant: parseFloat(montant),
                session,
                idPromotion: parseInt(idPromotion)
            })
        });

        const data = await response.json();
        if (data.success) {
            setMessage("Critere enregistre avec succes", "success");
            form.reset();
            await chargerPromotions();
        } else {
            setMessage(data.message, "error");
        }
    } catch (error) {
        setMessage("Erreur lors de l'enregistrement", "error");
    }
});

document.addEventListener("DOMContentLoaded", chargerPromotions);
