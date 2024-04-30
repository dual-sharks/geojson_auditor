import folium
from folium.plugins import Draw

def create_map(geojson_dict, df, nav_index):
    """
    Create an interactive map centered on the GeoJSON's centroid coordinates.

    Parameters:
    geojson_dict (dict): The dictionary representation of the GeoJSON data.

    Returns:
    folium.Map: A folium map object with all layers and controls added.
    """
    m = folium.Map(location=[df.loc[nav_index, 'centroid_latitude'], df.loc[nav_index, 'centroid_longitude']], zoom_start=13)
    folium.TileLayer('OpenStreetMap').add_to(m)
    folium.TileLayer(
        tiles='https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/{z}/{x}/{y}?access_token=pk.eyJ1Ijoiam9jb3B1ZmZzIiwiYSI6ImNsdjFncHdwdDA2eXcya25ub3dhOWw0aWEifQ.Ryosfu85kSVO8P408f1l-g',
        attr='Mapbox attribution',
        name='Mapbox Satellite'
    ).add_to(m)
    geojson_layer = folium.GeoJson(geojson_dict, name='GeoJSON')
    geojson_layer.add_to(m)
    m.fit_bounds(geojson_layer.get_bounds())
    folium.LayerControl().add_to(m)
    return m