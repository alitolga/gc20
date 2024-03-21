import streamlit as st
import geopandas as gpd
import pydeck as pdk
import os
import tempfile

# Function to save uploaded files to temporary directory and return shapefile path
def save_uploaded_files(uploaded_files):
    temp_dir = tempfile.mkdtemp()
    for uploaded_file in uploaded_files:
        with open(os.path.join(temp_dir, uploaded_file.name), 'wb') as f:
            f.write(uploaded_file.getbuffer())
    # Return the path of the .shp file
    for file_name in os.listdir(temp_dir):
        if file_name.endswith('.shp'):
            return os.path.join(temp_dir, file_name)

# Set up the title of the app
st.title('State Highways of Brazil Visualization')

# Create file uploader
uploaded_files = st.file_uploader('Upload shapefile components (.shp, .shx, .dbf, and any other required files)',
                                  type=['shp', 'shx', 'dbf', 'prj', 'cpg'],
                                  accept_multiple_files=True)

if uploaded_files:
    shapefile_path = save_uploaded_files(uploaded_files)
    if shapefile_path:
        # Load the shapefile
        gdf = gpd.read_file(shapefile_path)

        # Convert GeoDataFrame to Pydeck-compatible format
        gdf['lon'] = gdf.geometry.centroid.x
        gdf['lat'] = gdf.geometry.centroid.y

        # Create Pydeck map
        layer = pdk.Layer(
            'GeoJsonLayer',
            data=gdf,
            get_fill_color=[180, 0, 200, 140],  # Set the fill color, can be adjusted
            pickable=True,
        )

        view_state = pdk.ViewState(
            latitude=gdf['lat'].mean(),
            longitude=gdf['lon'].mean(),
            zoom=5,  # Initial zoom level
        )

        r = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            map_style='mapbox://styles/mapbox/light-v9',
        )

        # Show the map
        st.pydeck_chart(r)

        # Display the raw data (optional)
        if st.checkbox('Show raw data'):
            st.write(gdf)