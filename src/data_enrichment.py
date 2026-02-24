import pandas as pd
from src.data_cleaning import clean_data

def add_coordinates(df, coords_path):
    """
    Merge neighborhood coordinates into main dataset.

    """

    coords = pd.read_csv(coords_path)

    df = df.merge(coords, on=["District", "Neighborhood"],how="left")

    return df
