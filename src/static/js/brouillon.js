// Function to fetch data from the Flask backend
function fetchData() {
  return fetch("/data")
    .then((response) => response.json())
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

// Function to convert Unix timestamp to human-readable date format
function formatDate(timestamp) {
  const date = new Date(timestamp * 1000); // Convert Unix timestamp to milliseconds
  const day = date.getDate().toString().padStart(2, "0"); // Ensure day is two digits
  const month = (date.getMonth() + 1).toString().padStart(2, "0"); // Ensure month is two digits
  const year = date.getFullYear();
  return `${day}-${month}-${year}`;
}

// Function to update the remaining places
function updateRemainingPlaces() {
  const selectedDateTimestamp = parseInt(dateSelect.value);
  const remainingPlaces = remainingPlacesObj[selectedDateTimestamp];
  //const selectedDate = formatDate(selectedDateTimestamp);
  const remainingPlacesInfo = document.getElementById("remaining-places-info");
  const noPlacesMessage =
    "Plus de places disponibles, veuillez sélectionner une autre date";
  const placesMessage = `${remainingPlaces} place(s) restante(s) pour cette date`;

  remainingPlacesInfo.textContent =
    remainingPlaces === "0" ? noPlacesMessage : placesMessage;

  remainingPlacesInfo.classList.toggle(
    "no-places-available",
    remainingPlaces === "0"
  );
  remainingPlacesInfo.classList.toggle(
    "places-available",
    remainingPlaces !== "0"
  );
}

// Get the select element
const dateSelect = document.getElementById("date-select");

// Fetch the data from the Flask backend
fetchData().then((data) => {
  // Convert the received JSON data to JavaScript object
  remainingPlacesObj = data;

  // Clear existing options in the select dropdown
  dateSelect.innerHTML = "";

  // Add options to the select element
  const uniqueTimestamps = Object.keys(remainingPlacesObj).sort(
    (a, b) => a - b
  );
  uniqueTimestamps.forEach((timestamp) => {
    const option = new Option(formatDate(timestamp), timestamp);
    dateSelect.appendChild(option);
  });

  // Call the function initially to display the remaining places for the default selected date
  updateRemainingPlaces();

  // Call the function to update the remaining places when the user changes the date selection
  dateSelect.addEventListener("change", updateRemainingPlaces);
});
