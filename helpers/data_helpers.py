import pandas as pd

def count_unvalidated_geojsons(df):
    """
    Count the number of unvalidated GeoJSON entries in a DataFrame.

    The function checks the 'status' column in the DataFrame for missing values (NaN),
    which indicate that the GeoJSON has not yet been validated.

    Parameters:
    df (pd.DataFrame): The DataFrame containing GeoJSON entries with a 'status' column.

    Returns:
    int: The number of unvalidated GeoJSON entries.
    """
    return len(df[df['status'].isna()])


def find_next_unvalidated_index(df, start_index):
    """
    Find the index of the next unvalidated GeoJSON entry in the DataFrame, starting from a specified index.

    This function iterates through the DataFrame from 'start_index', checking each row to see if the 'status'
    field is NaN or not filled out, which indicates that the entry is unvalidated. The process skips entries
    that are already validated.

    Parameters:
    df (pd.DataFrame): The DataFrame containing GeoJSON entries.
    start_index (int): The index from which to start checking for unvalidated entries.

    Returns:
    int: The index of the next unvalidated GeoJSON entry. If all entries from 'start_index' onwards are validated,
         returns the length of the DataFrame.
    """
    while start_index < len(df) and pd.notna(df.loc[start_index, 'status']) and df.loc[start_index, 'status'].strip() != '':
        print(f"Skipping index {start_index} with status '{df.loc[start_index, 'status']}'")
        start_index += 1
    print(f"Next unvalidated index: {start_index}")
    return start_index

