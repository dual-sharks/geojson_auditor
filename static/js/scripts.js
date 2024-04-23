console.log('scripts.js is loaded successfully');

document.addEventListener('DOMContentLoaded', function() {
    var submitButton = document.getElementById('submit-data');
    if (submitButton) {
        submitButton.addEventListener('click', function(event) {
            var geojsonData = drawnItems.toGeoJSON();
            console.log("GeoJSON being sent:", JSON.stringify(geojsonData));  // Debug output

            fetch('/submit_geojson', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(geojsonData)
            })
            .then(response => response.json())
            .then(data => console.log("Server response:", data))
            .catch(error => console.error('Error:', error));
        });
    } else {
        console.error("Submit button not found");
    }
});

document.addEventListener('DOMContentLoaded', function() {
     var map = L.map('map-container').setView([51.505, -0.09], 13);
    
     var drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);
    var drawControl = new L.Control.Draw({
        edit: { featureGroup: drawnItems },
        draw: {
            polygon: true,
            polyline: false,
            rectangle: false,
            circle: false,
            marker: true
        }
    });
    map.addControl(drawControl);

    map.on(L.Draw.Event.CREATED, function (event) {
        var layer = event.layer;
        drawnItems.addLayer(layer);
        sendDataToServer(layer.toGeoJSON());
    });
});

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