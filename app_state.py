import pandas as pd

class AppState:
    def __init__(self, df):
        self.nav_index = 0
        self.is_initialized = False
        self.df = df

    def initialize(self):
        if not self.is_initialized:
            self.nav_index = self.find_next_unvalidated_index()
            self.is_initialized = True
        # Check if all entries are validated
        if self.nav_index >= len(self.df):
            return False, "All GeoJSONs have been validated."
        return True, None
    
    def find_next_unvalidated_index(self):
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
        start_index = self.nav_index
        while start_index < len(self.df) and pd.notna(self.df.loc[start_index, 'status']) and self.df.loc[start_index, 'status'].strip() != '':
            print(f"Skipping index {start_index} with status '{self.df.loc[start_index, 'status']}'")
            start_index += 1
        print(f"Next unvalidated index: {start_index}")
        return start_index

    def count_unvalidated_geojsons(self):
        """
        Count the number of unvalidated GeoJSON entries in a DataFrame.

        The function checks the 'status' column in the DataFrame for missing values (NaN),
        which indicate that the GeoJSON has not yet been validated.

        Parameters:
        df (pd.DataFrame): The DataFrame containing GeoJSON entries with a 'status' column.

        Returns:
        int: The number of unvalidated GeoJSON entries.
        """
        return len(self.df[self.df['status'].isna()])
