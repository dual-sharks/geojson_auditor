# DATA HANDLING LOGIC

import pandas as pd
import json
from helpers.data_helpers import  gather_info
import folium
from flask import render_template
from map_services import create_map
from app_state import AppState

df = pd.read_csv('data/geojsons.csv', low_memory=False)
app_state = AppState(df)


def load_geojson_details(app_state):
    """
    Load and display the details of the current GeoJSON entry based on the navigation index.
    This function manages the flow of checking initialization, creating maps, and gathering information.
    
    Returns:
    render_template: Renders the 'index.html' template with the interactive map, GeoJSON information,
                     and a count of unvalidated GeoJSONs. If all entries are validated, it renders
                     a message indicating completion.
    """
    initialized, message = app_state.initialize()
    if not initialized:
        return render_template('index.html', map=None, info={}, message=message)

    geojson_dict = json.loads(df.loc[app_state.nav_index, 'polygon'])
    m = create_map(geojson_dict, df = app_state.df, nav_index=app_state.nav_index)
    info = gather_info(df = app_state.df, nav_index=app_state.nav_index)
    unvalidated_count = app_state.count_unvalidated_geojsons()

    return render_template('index.html', map=m._repr_html_(), info=info, message=None, unvalidated_count=unvalidated_count)

def update_geojson(coordinates):
    polygon = f'{{"type": "Polygon", "coordinates": {coordinates}}}'
    app_state.df.loc[app_state.nav_index, 'polygon'] = polygon
    process_previous_next(direction='next')
    app_state.df.to_csv('data/geojsons.csv', index=False)

#TODO: add comments
def update_validation_status(validation_result, df):
    df.loc[app_state.nav_index, 'status'] = validation_result
    process_previous_next(direction='next')
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
    if direction == 'previous' and app_state.nav_index > 0:
        app_state.nav_index -= 1
    elif direction == 'next' and app_state.nav_index < len(df) - 1:
        app_state.nav_index += 1

