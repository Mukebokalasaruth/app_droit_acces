const prenom = document.getElementById("prenom")

const donnee = JSON.parse(localStorage.getItem("etudiant"))
prenom.innerText = donnee ? donnee.prenom : "Etudiant"
