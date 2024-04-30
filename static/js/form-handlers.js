// Handles form submissions and data interactions
function setupFormSubmission() {
    var submitButton = document.getElementById('submit-data');
    if (submitButton) {
        submitButton.addEventListener('click', function(event) {
            if (!latestDrawnGeoJSON) {
                console.error('No drawing data to submit.');
                return; 
            }
            sendDataToServer(latestDrawnGeoJSON);
        });
    } else {
        console.error("Submit button not found");
    }
}

function sendDataToServer(geoJsonData) {
    console.log(geoJsonData)
    fetch('/submit_geojson', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(geoJsonData)
    })
    .then(response => response.json())
    .then(data => console.log("Data submitted successfully", data))
    .catch(error => console.error('Failed to save drawing:', error));
}
