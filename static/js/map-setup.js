// Map initialization and drawing functionalities
var latestDrawnGeoJSON = null;

function setupMap() {
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
    //L.control.layers(baseMaps).addTo(map);

    map.on(L.Draw.Event.CREATED, function (event) {
        var layer = event.layer;
        drawnItems.addLayer(layer);
        latestDrawnGeoJSON = layer.toGeoJSON();
        console.log("Drawn GeoJSON stored:", JSON.stringify(latestDrawnGeoJSON));
    });
}
