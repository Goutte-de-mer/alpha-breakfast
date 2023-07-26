// Get the select element
const dateSelect = document.getElementById("date-select");

// JSON string of dates_and_remaining_places variable from Flask
const remainingPlacesData = `{{ dates_and_remaining_places | tojson | safe }}`;

// Convert the JSON string to a JavaScript object
const remainingPlacesObj = JSON.parse(remainingPlacesData);

// Function to update the remaining places
function updateRemainingPlaces() {
  // Get the selected date from the select element
  const selectedDate = dateSelect.value;

  // Split the selected date into day, month, and year components
  const [day, month, year] = selectedDate.split("-");

  // Get the remaining places for the selected date from the JavaScript object
  const remainingPlaces = remainingPlacesObj[selectedDate];

  // Update the content in the 'remaining-places-info' element with the desired format
  document.getElementById(
    "remaining-places-info"
  ).textContent = `Remaining places for ${day}-${month}-${year}: ${remainingPlaces}`;
}

// Call the function to update the remaining places when the user changes the date selection
dateSelect.addEventListener("change", updateRemainingPlaces);

// Call the function initially to display the remaining places for the default selected date
updateRemainingPlaces();
