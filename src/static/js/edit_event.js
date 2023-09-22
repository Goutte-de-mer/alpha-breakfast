// =========== VARIABLES ===========

const select_status = document.querySelectorAll(".status");
const options = [
  { value: "ouvert", text: "Ouvrir" },
  { value: "ferme", text: "Fermer" },
  { value: "annule", text: "Annuler" },
];
let dropdownMenuButtons = $(".menu-btn");
const confirmationMessage = $("#confirmation-message");
const contentBody = $(".content-body");
const header = $(".header-admin");
// =========== FONCTIONS ===========

// ....BODY MARGIN....
function updateContentBodyMargin() {
  const headerWidth = header.width();
  contentBody.css("margin-left", headerWidth);
}

// ....SELECT STATUS....

// Peuple le select du statut
function populateSelect() {
  select_status.forEach((select) => {
    options.forEach((option) => {
      const currentStatus = select.querySelector(".current-status").value;
      if (option.value !== currentStatus) {
        const optionElement = document.createElement("option");
        optionElement.value = option.value;
        optionElement.textContent = option.text;
        select.appendChild(optionElement);
      }
    });
  });
}

// Fonction pour gérer le changement d'état
function handleStatusChange() {
  let listItem = $(this).closest(".event");
  let eventId = listItem.find(".status").data("event-id");
  let editFields = listItem.find(".status");

  // Appelez la fonction saveChanges avec les nouvelles données
  saveChanges(listItem, eventId, editFields);
}

// ....MODIFICATION D'UN EVENEMENT....

// Fonction pour gérer le clic sur le bouton "Modifier"
function handleEditButtonClick() {
  let listItem = $(this).closest("li");
  let eventDetails = listItem.find(".event-details");
  let menuBtn = listItem.find(".menu-btn");

  // Masquer les détails de l'événement et afficher le formulaire de modification
  eventDetails.hide();
  showEditForm(listItem);

  // Cacher le bouton "Modifier" et le bouton "Menu"
  $(this).hide();
  menuBtn.hide();
}

// Fonction pour afficher le formulaire de modification
function showEditForm(listItem) {
  let eventId = listItem.find(".editable-field").data("event-id");

  // Récupérer les valeurs actuelles de l'événement depuis le modèle Flask
  fetchEventDetails(eventId)
    .then((eventDetails) => {
      if (eventDetails) {
        const editForm = createEditForm(eventId, eventDetails);
        listItem.append(editForm);

        // Gestionnaire de clic sur le bouton "Valider"
        listItem.find(".confirm").on("click", function () {
          let eventId = listItem.find(".edit-form").data("event-id");
          let editFields = listItem.find(".edit-form input");
          saveChanges(listItem, eventId, editFields);
        });

        // Gestionnaire de clic sur le bouton "Annuler"
        listItem.find(".cancel").on("click", function () {
          cancelChanges(listItem);
        });
      } else {
        alert("Événement non trouvé");
      }
    })
    .catch((error) => {
      alert(
        "Erreur lors de la récupération des détails de l'événement. Veuillez réessayer."
      );
    });
}

// Fonction pour récupérer les détails de l'événement depuis le serveur
function fetchEventDetails(eventId) {
  return new Promise((resolve, reject) => {
    $.ajax({
      type: "GET",
      url: `/get-event/${eventId}`,
      success: function (response) {
        if (response.success) {
          resolve(response.event);
        } else {
          resolve(null);
        }
      },
      error: function (xhr, status, error) {
        reject(error);
      },
    });
  });
}

// Fonction pour créer le formulaire de modification
function createEditForm(eventId, eventDetails) {
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
      <label for="start_time">Début : </label>
      <input type="text" name="start_time" value="${eventDetails.start_time}">
    </div>`;

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
    <button class="confirm transition" type="button"><i class="fa-solid fa-check transition"></i> Valider</button>
    <button class="cancel transition" type="button"><i class="fa-solid fa-xmark transition"></i> Annuler</button></div>
    </form>`;

  return editForm;
}

// Fonction pour enregistrer les modifications
function saveChanges(listItem, eventId, editFields) {
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

// Fonction pour annuler les modifications
function cancelChanges(listItem) {
  // Masquer le formulaire de modification et afficher les détails de l'événement
  listItem.find(".edit-form").remove();
  listItem.find(".event-details").show();

  // Afficher à nouveau le bouton "Modifier"
  listItem.find(".edit").show();
  listItem.find(".menu-btn").show();
}

// ....GESTION DROPDOWN MENU....

// Fonction pour ouvrir le menu déroulant
function openDropdownMenu(button) {
  const menuId = button.attr("data-menu-id");
  const dropdownMenu = $("#" + menuId);

  positionDropdownMenu(button[0], dropdownMenu);

  dropdownMenu.toggleClass("show-menu");

  // Ajoute un écouteur de clic sur le document uniquement lorsque le menu est ouvert
  $(document).on("click", closeMenuOutside);

  // Fonction pour fermer le menu lorsqu'un clic est détecté en dehors du menu
  function closeMenuOutside(event) {
    // Vérifie si le clic est en dehors du menu et du bouton
    if (
      !dropdownMenu.is(event.target) &&
      !button.is(event.target) &&
      dropdownMenu.has(event.target).length === 0 &&
      button.has(event.target).length === 0
    ) {
      dropdownMenu.removeClass("show-menu");
      $(document).off("click", closeMenuOutside);
    }
  }
}

// Fonction pour gérer le clic sur les boutons de menu
function handleDropdownButtonClick(e) {
  e.preventDefault();

  openDropdownMenu($(this));

  const menuId = $(this).attr("data-menu-id");
  const dropdownMenu = $("#" + menuId);

  const deleteButton = dropdownMenu.find(".delete-button");

  deleteButton.on("click", handleDeleteButtonClick);
}

// Fonction pour positionner le dropdown menu par rapport au bouton
function positionDropdownMenu(button, dropdownMenu) {
  // Récupère la position du bouton "menu-btn"
  const buttonRect = button.getBoundingClientRect();

  dropdownMenu.css({
    top: buttonRect.top + window.scrollY - 85 + "px",
    left: buttonRect.left + window.scrollX - 610 + "px",
  });
}

function handleDeleteButtonClick(event) {
  event.preventDefault();
  let confirmMessage =
    "Cette action supprimera définitivement l'événement de la base de données. Êtes-vous sûr de vouloir continuer ?";
  const eventId = $(this).attr("data-event-id");

  const confirmation = window.confirm(confirmMessage);

  if (confirmation) {
    fetch(`/delete-event/${eventId}`, {
      method: "DELETE",
    })
      .then((response) => response.json())
      .then((data) => {
        confirmationMessage.css("display", "flex");
        // Masquez le message de confirmation après quelques secondes (par exemple, 3 secondes)
        setTimeout(() => {
          confirmationMessage.css("display", "none");
          window.location.reload();
        }, 2000);
      })
      .catch((error) => {
        console.error("Erreur lors de la suppression de l'événement : ", error);
      });
  }
}

// =========== GESTIONNAIRES D'EVENEMENTS ===========

// Gestionnaire de changement d'état (.status)
$(".status").on("change", handleStatusChange);

// Gestionnaire de clic sur le bouton "Modifier" (.event .edit)
$(".event .edit").on("click", handleEditButtonClick);

// Gestionnaire de clic sur le bouton menu
dropdownMenuButtons.on("click", handleDropdownButtonClick);

// Soumission du formulaire
$("#create-event-form").submit(function (event) {
  event.preventDefault();
  $.ajax({
    type: "POST",
    url: "/create-event",
    data: $(this).serialize(),
    success: function (response) {
      // If the reservation is successful, redirect to another page
      if (response.success) {
        confirmationMessage.css("display", "flex");
        // Masquez le message de confirmation après quelques secondes (par exemple, 3 secondes)
        setTimeout(() => {
          confirmationMessage.css("display", "none");
          window.location.reload();
        }, 2000);
      } else {
        // If the reservation fails, show an alert with the error message
        alert(response.message);
        window.location.reload();
      }
    },
    error: function (xhr, status, error) {
      // If the request fails, show a generic error message
      showAlert("Une erreur s'est produite lors de la réservation.");
    },
  });
});

// Quand redimenssion de la fenêtre, définit margin de content
$(window).on("resize", updateContentBodyMargin);

populateSelect();
updateContentBodyMargin();
