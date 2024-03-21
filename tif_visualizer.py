import streamlit as st
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
import numpy as np
import pydeck as pdk


# Function to convert raster data to RGB for visualization
# def read_tif_as_rgb(tif_path):
#     with rasterio.open(tif_path) as src:
#         # Read the raster data
#         band = src.read(1)

#         # Normalize the band for RGB visualization
#         band_norm = (band - np.min(band)) / (np.max(band) - np.min(band))
#         rgb = np.dstack((band_norm, band_norm, band_norm))  # Create a 3D array for RGB

#         # Return the normalized data along with the bounds for mapping
#         return rgb, src.bounds


# Function to get bounds from the raster file
def get_bounds(tif_path):
    with rasterio.open(tif_path) as src:
        return src.bounds



# Set up the title of the app
st.title('Burned Areas in Brazil Forests Visualization')

# Set up the sidebar
st.sidebar.title("Settings")

# Set the years range
years = range(2003, 2023)  # 2003 to 2022

# Create a slider for selecting the year
selected_year = st.sidebar.slider('Select a year', min(years), max(years), step=1)

# Construct the path to the TIF file for the selected year
tif_path = f'burned_areas/barea{selected_year}_bra.tif'  # Modify this line accordingly

# Display the TIF file as a map
try:
    # Read the data as RGB and get the bounds
    bounds = get_bounds(tif_path)

    # Set up Pydeck layer for showing the raster
    raster_layer = pdk.Layer(
        "BitmapLayer",
        data=None,
        image=tif_path,
        opacity=0.8,
        bounds=[bounds.left, bounds.bottom, bounds.right, bounds.top]
    )

    # Set the initial view state
    view_state = pdk.ViewState(
        latitude=(bounds.top + bounds.bottom) / 2,
        longitude=(bounds.left + bounds.right) / 2,
        zoom=5
    )

    r = pdk.Deck(
            layers=[raster_layer],
            initial_view_state=view_state,
            map_style='mapbox://styles/mapbox/satellite-v9',
        )

    # Show the map
    st.pydeck_chart(r)

except FileNotFoundError:
    st.error(f'File for the year {selected_year} not found.')
