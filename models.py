# DATA HANDLING LOGIC

import pandas as pd
import json
from helpers.data_helpers import count_unvalidated_geojsons, find_next_unvalidated_index
import folium
from flask import render_template

df = pd.read_csv('data/geojsons.csv', low_memory=False)

nav_index = 0 
is_initialized = False
current_index = find_next_unvalidated_index(df=df, start_index=0)

def load_geojson_details():
    """
    Load and display the details of the current GeoJSON entry based on the navigation index.

    This function checks if the application has been initialized and finds the next unvalidated
    GeoJSON entry if necessary. It then creates an interactive map using Folium centered on
    the centroid coordinates of the GeoJSON and adds various basemap options and a GeoJSON layer.
    The function also compiles an information dictionary about the current GeoJSON entry for display
    and counts the remaining unvalidated GeoJSONs.

    Globals:
    nav_index (int): The current index in the DataFrame for navigation.
    is_initialized (bool): A flag indicating whether the initial setup has been done.

    Returns:
    render_template: Renders the 'index.html' template with the interactive map, GeoJSON information,
                     and a count of unvalidated GeoJSONs. If all entries are validated, it renders
                     a message indicating completion.
    """
    global nav_index, is_initialized

    if not is_initialized:
        nav_index = find_next_unvalidated_index(df=df, start_index=nav_index)
        is_initialized = True

    if nav_index >= len(df):
        return render_template('index.html', map=None, info={}, message="All GeoJSONs have been validated.")

    geojson_str = df.loc[nav_index, 'polygon']
    geojson_dict = json.loads(geojson_str)

    # Create a Map with OpenStreetMap and Mapbox basemaps
    m = folium.Map(location=[df.loc[nav_index, 'centroid_latitude'], df.loc[nav_index, 'centroid_longitude']], zoom_start=13)

    # Add the OpenStreetMap basemap
    folium.TileLayer('OpenStreetMap').add_to(m)

    # Add the Mapbox satellite basemap
    folium.TileLayer(
        tiles='https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/{z}/{x}/{y}?access_token=YOUR_MAPBOX_ACCESS_TOKEN',
        attr='Mapbox attribution',
        name='Mapbox Satellite'
    ).add_to(m)

    # Add the GeoJSON layer
    geojson_layer = folium.GeoJson(geojson_dict, name='GeoJSON')
    geojson_layer.add_to(m)

    # Fit the map to the bounds of the GeoJSON layer
    bounds = geojson_layer.get_bounds()
    m.fit_bounds(bounds)

    # Add a layer control to switch between the basemaps
    folium.LayerControl().add_to(m)

    # Set up info dictionary
    info = {
        'Name': df.loc[nav_index, 'name'],
        'Sector': df.loc[nav_index, 'sector'],
        'Sub': df.loc[nav_index, 'sub'],
        'Category': df.loc[nav_index, 'category'],
        'Location ISO2 Code': df.loc[nav_index, 'location_iso2_code'],
        'Associated ISO2 Code': df.loc[nav_index, 'associated_iso2_code'],
        'Legacy Category': df.loc[nav_index, 'legacy_category'],
        'Legacy Behavior': df.loc[nav_index, 'legacy_behavior'],
        'Centroid Latitude': df.loc[nav_index, 'centroid_latitude'],
        'Centroid Longitude': df.loc[nav_index, 'centroid_longitude'],
        'Info Issue? (nan = none)': df.loc[nav_index, 'info_issue'],
        'Status (nan = none)': df.loc[nav_index, 'status'],
        'Bad Polygon (nan = none)': df.loc[nav_index, 'bad_polygon']
    }

    unvalidated_count = count_unvalidated_geojsons(df=df)

    return render_template('index.html', map=m._repr_html_(), info=info, message=None, unvalidated_count=unvalidated_count)


def update_validation_status(validation_result):
    global df
    # Logic to update CSV with new status
    df.to_csv('data/geojsons.csv', index=False)

def process_previous_next(direction):
    """
    Adjust the navigation index to either the previous or next GeoJSON entry in the DataFrame.

    This function updates the global navigation index (`nav_index`) based on the direction
    specified. If 'previous' is requested, the index is decremented, unless it is already at
    the first entry. If 'next' is requested, the index is incremented, unless it is already
    at the last entry of the DataFrame.

    Parameters:
    direction (str): The direction to move in the DataFrame; should be 'previous' or 'next'.

    Globals:
    nav_index (int): The current index in the DataFrame indicating the currently viewed GeoJSON.

    Returns:
    None: The function updates the global `nav_index` directly.
    """
    global nav_index
    if direction == 'previous' and nav_index > 0:
        nav_index -= 1
    elif direction == 'next' and nav_index < len(df) - 1:
        nav_index += 1

