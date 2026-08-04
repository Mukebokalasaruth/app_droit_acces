const etatCard = document.getElementById("etatCard");
const message = document.getElementById("message");
const printActions = document.getElementById("printActions");
const printAccessBtn = document.getElementById("printAccessBtn");
const rejectedProofs = document.getElementById("rejectedProofs");
const logoSrc = new URL("../../image/logo.jpeg", window.location.href).href;
let droitAcces = null;

function badgeClass(etat) {
    const etatNormalise = String(etat).toLowerCase();
    if (etatNormalise.startsWith("valid")) return "bg-emerald-100 text-emerald-800";
    if (etatNormalise.startsWith("rejet")) return "bg-red-100 text-red-800";
    return "bg-amber-100 text-amber-800";
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

async function chargerEtat() {
    const etudiant = JSON.parse(localStorage.getItem("etudiant"));
    if (!etudiant) {
        etatCard.innerHTML = '<p class="font-semibold text-red-700">Vous devez vous connecter comme etudiant.</p>';
        printActions.classList.add("hidden");
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/etudiant/etat-validation/${etudiant.id}`);
        const data = await response.json();

        if (!data.success) {
            etatCard.innerHTML = `<p class="font-semibold text-red-700">${data.message}</p>`;
            printActions.classList.add("hidden");
            return;
        }

        const etat = data.data.etat || "En attente";
        const motif = data.data.motifRejet ? `<p class="mt-4 rounded-lg bg-red-50 p-4 text-sm text-red-800"><strong>Motif du rejet:</strong> ${data.data.motifRejet}</p>` : "";
        const estValide = String(etat).toLowerCase().startsWith("valid");

        droitAcces = estValide ? {
            idPreuve: data.data.idPreuve,
            etat,
            nom: etudiant.nom || "",
            postnom: etudiant.postnom || "",
            prenom: etudiant.prenom || "",
            matricule: etudiant.matricule || "",
            dateImpression: new Date().toLocaleDateString("fr-FR")
        } : null;

        etatCard.innerHTML = `
            <div class="flex flex-wrap items-start justify-between gap-4">
                <div class="flex items-start gap-4">
                    ${estValide ? `<img class="h-14 w-14 rounded-lg bg-white object-contain p-1 ring-1 ring-slate-200" src="${logoSrc}" alt="Logo Droit d'acces">` : ""}
                    <div>
                    ${estValide ? '<p class="text-sm font-semibold uppercase tracking-[.18em] text-brand">Droit d\'acces aux examens</p>' : ""}
                    <p class="text-sm font-semibold uppercase tracking-[.18em] text-slate-500">Preuve #${data.data.idPreuve}</p>
                    <h2 class="mt-2 text-2xl font-bold">${etudiant.prenom} ${etudiant.nom || ""}</h2>
                    <p class="mt-1 text-slate-600">Matricule: ${etudiant.matricule}</p>
                    </div>
                </div>
                <span class="rounded-full px-4 py-2 text-sm font-bold ${badgeClass(etat)}">${etat}</span>
            </div>
            ${motif}
        `;

        printActions.classList.toggle("hidden", !estValide);
    } catch (error) {
        printActions.classList.add("hidden");
        message.textContent = "Impossible de contacter le serveur.";
        message.className = "mt-5 min-h-6 text-sm font-semibold text-red-700";
    }
}

function preuveUrl(chemin) {
    if (!chemin) return "#";
    return `http://127.0.0.1:5000/${chemin.replaceAll("\\", "/")}`;
}

async function chargerPreuvesRejetees() {
    const etudiant = JSON.parse(localStorage.getItem("etudiant"));
    if (!etudiant) {
        rejectedProofs.innerHTML = '<p class="font-semibold text-red-700">Vous devez vous connecter comme etudiant.</p>';
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/etudiant/preuves-rejetees/${etudiant.id}`);
        const data = await response.json();

        if (!data.success) {
            rejectedProofs.innerHTML = `<p class="font-semibold text-red-700">${escapeHtml(data.message)}</p>`;
            return;
        }

        if (!data.data.length) {
            rejectedProofs.innerHTML = '<p class="text-slate-600">Aucune preuve rejetee pour le moment.</p>';
            return;
        }

        rejectedProofs.innerHTML = `
            <div class="space-y-4">
                ${data.data.map((preuve) => `
                    <article class="rounded-lg border border-red-100 bg-white p-5">
                        <div class="flex flex-wrap items-start justify-between gap-3">
                            <div>
                                <p class="text-sm font-semibold uppercase tracking-[.16em] text-red-700">Preuve #${escapeHtml(preuve.idPreuve)}</p>
                                <p class="mt-1 text-sm text-slate-500">Soumise le ${escapeHtml(preuve.dateSoumission || "-")}</p>
                            </div>
                            <span class="rounded-full bg-red-100 px-3 py-1 text-xs font-bold text-red-800">Rejetee</span>
                        </div>
                        <p class="mt-4 rounded-lg bg-red-50 p-4 text-sm leading-6 text-red-800">
                            <strong>Motif du comptable:</strong> ${escapeHtml(preuve.motifRejet || "Aucun motif renseigne.")}
                        </p>
                        <a class="mt-4 inline-flex text-sm font-semibold text-brand hover:text-teal-900" href="${preuveUrl(preuve.capture)}" target="_blank" rel="noreferrer">
                            Voir la preuve envoyee
                        </a>
                    </article>
                `).join("")}
            </div>
        `;
    } catch (error) {
        rejectedProofs.innerHTML = '<p class="font-semibold text-red-700">Impossible de charger les preuves rejetees.</p>';
    }
}

function imprimerDroitAcces() {
    if (!droitAcces) return;

    const fullName = [droitAcces.prenom, droitAcces.nom, droitAcces.postnom]
        .filter(Boolean)
        .join(" ");
    const nomComplet = escapeHtml(fullName);
    const matricule = escapeHtml(droitAcces.matricule);
    const etat = escapeHtml(droitAcces.etat);
    const idPreuve = escapeHtml(droitAcces.idPreuve);
    const dateImpression = escapeHtml(droitAcces.dateImpression);

    const printWindow = window.open("", "_blank", "width=900,height=700");
    if (!printWindow) {
        message.textContent = "Autorisez les pop-ups pour imprimer le droit d'acces.";
        message.className = "mt-5 min-h-6 text-sm font-semibold text-red-700";
        return;
    }

    printWindow.document.write(`
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>Droit d'acces</title>
            <style>
                * { box-sizing: border-box; }
                body {
                    margin: 0;
                    background: #f5f7fb;
                    color: #172033;
                    font-family: Arial, sans-serif;
                }
                .page {
                    min-height: 100vh;
                    display: grid;
                    place-items: center;
                    padding: 32px;
                }
                .ticket {
                    width: 100%;
                    max-width: 760px;
                    border: 2px solid #0f766e;
                    border-radius: 12px;
                    background: #ffffff;
                    padding: 36px;
                }
                .header {
                    display: flex;
                    justify-content: space-between;
                    gap: 24px;
                    border-bottom: 1px solid #d9e2ec;
                    padding-bottom: 20px;
                }
                .logo {
                    width: 56px;
                    height: 56px;
                    border-radius: 10px;
                    background: #ffffff;
                    object-fit: contain;
                    padding: 4px;
                }
                .eyebrow {
                    margin: 0 0 8px;
                    color: #64748b;
                    font-size: 12px;
                    font-weight: 700;
                    letter-spacing: .16em;
                    text-transform: uppercase;
                }
                h1 {
                    margin: 0;
                    font-size: 30px;
                    line-height: 1.2;
                }
                .status {
                    align-self: start;
                    border-radius: 999px;
                    background: #d1fae5;
                    color: #065f46;
                    font-weight: 800;
                    padding: 10px 16px;
                    white-space: nowrap;
                }
                .content {
                    display: grid;
                    gap: 14px;
                    margin-top: 28px;
                }
                .row {
                    display: grid;
                    grid-template-columns: 190px 1fr;
                    gap: 18px;
                    border-bottom: 1px solid #edf2f7;
                    padding: 12px 0;
                }
                .label {
                    color: #64748b;
                    font-weight: 700;
                }
                .value {
                    font-weight: 800;
                }
                .note {
                    margin-top: 28px;
                    border-radius: 10px;
                    background: #f0fdfa;
                    color: #134e4a;
                    padding: 16px;
                    font-weight: 700;
                }
                .footer {
                    display: flex;
                    justify-content: space-between;
                    gap: 16px;
                    margin-top: 34px;
                    color: #64748b;
                    font-size: 13px;
                }
                @media print {
                    body { background: #ffffff; }
                    .page { min-height: auto; padding: 0; }
                    .ticket { border-radius: 0; box-shadow: none; }
                }
            </style>
        </head>
        <body>
            <main class="page">
                <section class="ticket">
                    <div class="header">
                        <div style="display:flex; gap:16px; align-items:center;">
                            <img class="logo" src="${logoSrc}" alt="Logo Droit d'acces">
                            <div>
                                <p class="eyebrow">Autorisation officielle</p>
                                <h1>Droit d'acces aux examens</h1>
                            </div>
                        </div>
                        <div class="status">${etat}</div>
                    </div>
                    <div class="content">
                        <div class="row"><div class="label">Etudiant</div><div class="value">${nomComplet}</div></div>
                        <div class="row"><div class="label">Matricule</div><div class="value">${matricule}</div></div>
                        <div class="row"><div class="label">Preuve de paiement</div><div class="value">#${idPreuve}</div></div>
                        <div class="row"><div class="label">Date d'impression</div><div class="value">${dateImpression}</div></div>
                    </div>
                    <p class="note">Cet etudiant est autorise a acceder aux examens.</p>
                    <div class="footer">
                        <span>Droit d'acces</span>
                        <span>Document genere depuis l'espace etudiant</span>
                    </div>
                </section>
            </main>
        </body>
        </html>
    `);
    printWindow.document.close();
    printWindow.focus();
    printWindow.print();
}

printAccessBtn.addEventListener("click", imprimerDroitAcces);
document.addEventListener("DOMContentLoaded", () => {
    chargerEtat();
    chargerPreuvesRejetees();
});
