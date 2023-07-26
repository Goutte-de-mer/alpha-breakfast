// Fonction pour récupérer les dates disponibles depuis le backend
function fetchDates() {
  axios
    .get("/")
    .then((response) => {
      const dates = response.data.dates;
      const dateSelect = document.getElementById("date-select");
      // Ajouter les options pour chaque date disponible dans la liste déroulante
      dates.forEach((date) => {
        const option = document.createElement("option");
        option.value = date;
        option.text = date;
        dateSelect.appendChild(option);
      });
    })
    .catch((error) => {
      console.error("Erreur lors de la récupération des dates :", error);
    });
}

// Appeler la fonction pour récupérer les dates au chargement de la page
window.onload = fetchDates;
