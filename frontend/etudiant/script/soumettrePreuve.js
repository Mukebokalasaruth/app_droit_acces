const form = document.getElementById("form");
const message = document.getElementById("message");
form.addEventListener("submit",
    async (e) => {
        e.preventDefault();

        try {

            const etudiant = JSON.parse(localStorage.getItem("etudiant"));
            if (!etudiant) {
                message.innerText = "Etudiant non connecté";
                return;
            }
            const fichier = document.getElementById("file").files[0];
            if (!fichier) {

                message.innerText = "Sélectionnez un fichier";
                return;
            }
            const formData = new FormData();

            formData.append("file", fichier);

            formData.append("idEtudiant", etudiant.id);
            const response =await fetch("http://127.0.0.1:5000/etudiant/upload-preuve",
                    {
                        method: "POST",
                        body: formData
                    }
                );

            const data = await response.json();
            console.log(data);

            if (data.success) {

                message.innerText =
                    data.message;

                form.reset();

            } else {

                message.innerText =
                    data.message;
            }

        } catch (error) {

            console.error(error);

            message.innerText =
                error.message;
        }
    }
);