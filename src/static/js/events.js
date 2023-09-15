$(document).ready(function () {
  // Gestionnaire de clic sur le bouton "Modifier"
  $(".event .edit").on("click", function () {
    let listItem = $(this).closest("li");
    let eventDetails = listItem.find(".event-details");
    let menuBtn = listItem.find(".menu-btn");

    // Masquer les détails de l'événement et afficher le formulaire de modification
    eventDetails.hide();
    showEditForm(listItem);

    // Cacher le bouton "Modifier"
    $(this).hide();
    menuBtn.hide();
  });

  // Fonction pour afficher le formulaire de modification
  function showEditForm(listItem) {
    let eventId = listItem.find(".editable-field").data("event-id");

    // Récupérer les valeurs actuelles de l'événement depuis le modèle Flask
    $.ajax({
      type: "GET",
      url: `/get-event/${eventId}`, // Définissez une route Flask pour récupérer les détails de l'événement
      success: function (response) {
        if (response.success) {
          let eventDetails = response.event;

          let editForm = `<form class="edit-form" data-event-id="${eventId}">
          <div class="input-group">
            <label for="date">Date : </label>
            <input type="date" name="date" value="${eventDetails.date}">
          </div>

          <div class="input-group">
            <label for="capacity">Capacité : </label>
            <input type="text" name="capacity" value="${eventDetails.capacity}">
          </div>

          <div class="input-group">
            <label for="start-time">Début : </label>
            <input type="text" name="start-time" value="${eventDetails.start_time}">
          </div>`;

          // Vérifier si la durée n'est pas nulle ou vide
          if (eventDetails.duration !== null && eventDetails.duration !== "") {
            editForm += `
            <div class="input-group">
              <label for="duration">Durée : </label>
              <input type="text" name="duration" value="${eventDetails.duration}">
            </div>`;
          } else {
            editForm += `
            <div class="input-group">
              <label for="duration">Durée : </label>
              <input type="text" name="duration" value="">
            </div>`;
          }

          editForm += `<div class="form-btns">
          <button class="confirm" type="button"><i class="fa-solid fa-check"></i> Valider</button>
          <button class="cancel" type="button"><i class="fa-solid fa-xmark"></i> Annuler</button></div>
          </form>`;

          listItem.append(editForm);

          // Gestionnaire de clic sur le bouton "Valider"
          listItem.find(".confirm").on("click", function () {
            saveChanges(listItem);
          });

          // Gestionnaire de clic sur le bouton "Annuler"
          listItem.find(".cancel").on("click", function () {
            cancelChanges(listItem);
          });
        } else {
          alert("Événement non trouvé");
        }
      },
      error: function (xhr, status, error) {
        alert(
          "Erreur lors de la récupération des détails de l'événement. Veuillez réessayer."
        );
      },
    });
  }

  // Fonction pour annuler les modifications
  function cancelChanges(listItem) {
    // Masquer le formulaire de modification et afficher les détails de l'événement
    listItem.find(".edit-form").remove();
    listItem.find(".event-details").show();

    // Afficher à nouveau le bouton "Modifier"
    listItem.find(".edit").show();
    listItem.find(".menu-btn").show();
  }

  // Fonction pour enregistrer les modifications
  function saveChanges(listItem) {
    let eventId = listItem.find(".edit-form").data("event-id");
    let editFields = listItem.find(".edit-form input");

    // Récupérer les nouvelles valeurs des champs éditables
    let newData = {};
    editFields.each(function () {
      let fieldName = $(this).attr("name");
      let newValue = $(this).val();

      newData[fieldName] = newValue;
    });

    // Envoyer les modifications à votre serveur (via une requête AJAX)
    $.ajax({
      type: "POST",
      url: "/update-event",
      contentType: "application/json",
      data: JSON.stringify({
        event_id: eventId,
        new_data: newData,
      }),
      success: function (response) {
        if (response.success) {
          alert("Mise à jour réussie");
        } else {
          alert("Échec de la mise à jour de l'événement");
        }

        // Actualiser la page ou effectuer d'autres actions en fonction de votre besoin
        window.location.reload();
      },
      error: function (xhr, status, error) {
        alert(
          "Erreur lors de la mise à jour de l'événement. Veuillez réessayer."
        );
      },
    });

    // Masquer le formulaire de modification et afficher les détails de l'événement
    listItem.find(".edit-form").remove();
    listItem.find(".event-details").show();

    // Afficher à nouveau le bouton "Modifier"
    listItem.find(".edit").show();
    listItem.find(".menu-btn").show();
  }
});
