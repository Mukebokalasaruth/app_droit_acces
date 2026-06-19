const prenom = document.getElementById("prenom")

const donnee = JSON.parse(localStorage.getItem("comptable"))
prenom.innerText = donnee.prenom