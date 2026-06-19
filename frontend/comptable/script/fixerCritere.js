const selectPromotion = document.getElementById("idPromotion");
const form = document.getElementById("critereForm");
const message = document.getElementById("message");

// CHARGER LES PROMOTIONS
async function chargerPromotions() {

    try {

        const response =
            await fetch("http://127.0.0.1:5000/comptable/promotions");

        const data = await response.json();

        selectPromotion.innerHTML = '<option value="">Sélectionner une promotion</option>';
        if (data.success) {

            data.data.forEach(
                (promotion) => {

                    const option = document.createElement("option");

                    option.value = promotion.id;

                    option.textContent = promotion.nom;

                    selectPromotion.appendChild(option);
                });}

    } catch (error) {

        console.error(
            error
        );

        selectPromotion.innerHTML = '<option value="">Erreur de chargement</option>';
    }}

    // ENREGISTRER CRITERE
// ==========================
form.addEventListener(
    "submit",
    async function (e) {

        e.preventDefault();

        const montant = document.getElementById("montant").value;
        const session = document.getElementById("session").value;
        const idPromotion = document.getElementById("idPromotion").value;

        try {

            const response =
                await fetch(
                    "http://127.0.0.1:5000/critere/critere-paiement",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            montant:
                                parseFloat(
                                    montant
                                ),

                            session:
                                session,

                            idPromotion:
                                parseInt(
                                    idPromotion
                                )
                        })
                    }
                );

            const data =
                await response.json();

            if (data.success) {

                message.innerText =
                    "Critère enregistré avec succès";

                form.reset();

            } else {

                message.innerText =
                    data.message;
            }

        } catch (error) {

            console.error(error);

            message.innerText =
                "Erreur lors de l'enregistrement";
        }
    }
);

// AU CHARGEMENT DE LA PAGE
document.addEventListener("DOMContentLoaded", chargerPromotions);