import pandas as pd



def gather_info(df, nav_index):
    """
    Gather and structure the information about the current GeoJSON entry for display.

    Returns:
    dict: A dictionary containing information about the current GeoJSON entry.
    """
    return {
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