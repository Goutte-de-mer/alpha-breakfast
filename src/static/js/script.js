function updateRemainingPlaces(selectedDate) {
  // Requête AJAX pour récupérer les places restantes
  $.ajax({
    url: "/",
    method: "POST",
    data: { "date-select": selectedDate },
    success: function (response) {
      $("#remaining-places-info").text(
        "Places restantes : " + response.remainingPlaces
      );
    },
    error: function () {
      $("#remaining-places-info").text(
        "Un problème a eu lieu lors de la récupération des places"
      );
    },
  });
}

$("#date-select").change(function () {
  let selectedDate = $(this).val();
  updateRemainingPlaces(selectedDate);
});

$(document).ready(function () {
  // ============= RÉCUPÈRE LE NOMBRE DE PLACES RESTANTES
  let selectedDate = $("#date-select").val();
  updateRemainingPlaces(selectedDate);

  // ============= AJOUTER UNE PERSONNE AU FORMULAIRE
  let personCount = 1;

  $(".add-person-btn").click(function () {
    personCount++;
    const newPerson = `
        <div class="person">
            <h2>Personne n°${personCount}</h2>

            <div class="identity">
                <div class="name">
                  <label for="name-input-${personCount}">Prénom :</label>
                  <input type="text" id="name-input-${personCount}" name="name" required />
                </div>
                <div class="lastname">
                  <label for="lastname-input-${personCount}">Nom :</label>
                  <input type="text" id="lastname-input-${personCount}" name="lastname" required />
                </div>
              </div>
              <div class="email">
                <label for="email-input-${personCount}">Email :</label>
                <input type="email" id="email-input-${personCount}" name="email-input" required>
              </div>
        </div>
        `;

    const $newPerson = $(newPerson);
    $newPerson.css("opacity", "0");

    $(".people").append($newPerson);

    // Trigger a reflow to apply the CSS transition
    $newPerson[0].offsetHeight;

    // Remove the opacity property to trigger the fade-in effect
    $newPerson.css("opacity", "1");
  });

  // ============= ALERTE/CONFIRMATION SOUMISSION FORMULAIRE
  // Fonction pour afficher l'alerte avec le message
  function showAlert(message) {
    alert(message);
  }

  // Fonction pour soumettre le formulaire et gérer la réponse
  $(document).ready(function () {
    $("#registration-form").submit(function (event) {
      event.preventDefault();
      $.ajax({
        type: "POST",
        url: "/submit",
        data: $(this).serialize(),
        success: function (response) {
          // If the reservation is successful, redirect to another page
          if (response.success) {
            window.location.href = "/success"; // Replace "/success" with the desired URL for successful reservations
          } else {
            // If the reservation fails, show an alert with the error message
            showAlert(response.message);
          }
        },
        error: function (xhr, status, error) {
          // If the request fails, show a generic error message
          showAlert("Une erreur s'est produite lors de la réservation.");
        },
      });
    });
  });
});
