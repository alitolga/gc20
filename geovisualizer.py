import streamlit as st
import geopandas as gpd
import pydeck as pdk
import pandas as pd
from shapely.geometry import Point
import geemap
import ee

ee.Authenticate()
ee.Initialize(project='atd-gc')

# Set up the title of the app
st.title('Geographical Data Visualizer')
brazil_shapefile = geemap.shp_to_ee('brazil/Brazil.shp')


Map = geemap.Map()

landcover = ee.Image('MODIS/006/MCD12Q1/2004_01_01').select('LC_Type1')

igbpLandCoverVis = {
    'min': 1.0,
    'max': 17.0,
    'palette': [
        '05450a',
        '086a10',
        '54a708',
        '78d203',
        '009900',
        'c6b044',
        'dcd159',
        'dade48',
        'fbff13',
        'b6ff05',
        '27ff87',
        'c24f44',
        'a5a5a5',
        'ff6d4c',
        '69fff8',
        'f9ffa4',
        '1c0dff',
    ],
}
brazil_lc = landcover.clip(brazil_shapefile)
Map.setCenter(-55, -10, 4)
Map.addLayer(brazil_lc, igbpLandCoverVis, 'MODIS Land Cover')

Map.to_streamlit(height=700)




# Create a file uploader for the user to upload GeoJSON or CSV files
uploaded_file = st.file_uploader('Upload a geographical data file (GeoJSON or CSV)', type=['geojson', 'csv'])

if uploaded_file is not None:
    # Check the file extension to process accordingly
    file_extension = uploaded_file.name.split('.')[-1]

    if file_extension.lower() == 'geojson':
        # Read the GeoJSON file
        gdf = gpd.read_file(uploaded_file)
    elif file_extension.lower() == 'csv':
        # Read the CSV into a pandas DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Allow the user to input the latitude and longitude columns if a CSV is uploaded
        lat_col = 'latitude'
        lon_col = 'longitude'

        # Check if the specified columns exist in the DataFrame
        if lat_col in df.columns and lon_col in df.columns:
            # Create a GeoDataFrame from the DataFrame
            gdf = gpd.GeoDataFrame(df, geometry=[Point(xy) for xy in zip(df[lon_col], df[lat_col])])
            gdf.set_crs(epsg=4326, inplace=True)  # Set the coordinate reference system to WGS84 (lat/lon)
        else:
            st.error("Specified columns for latitude or longitude do not exist in the uploaded CSV.")
            gdf = None


        # # Allow the user to input the latitude and longitude columns if a CSV is uploaded
        # lat_col = st.text_input('Latitude Column Name', 'latitude')
        # lon_col = st.text_input('Longitude Column Name', 'longitude')

        # # Read the CSV file
        # gdf = gpd.read_file(uploaded_file, GEOM_POSSIBLE_NAMES=[lon_col, lat_col], KEEP_GEOM_COLUMNS="NO")

    # Convert GeoDataFrame to Pydeck-friendly format
    gdf['lon'] = gdf.geometry.x
    gdf['lat'] = gdf.geometry.y
    data = gdf[['lon', 'lat']]

    # Set up the Pydeck map
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=data['lat'].mean(),
            longitude=data['lon'].mean(),
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=data,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
            ),
        ],
    ))

    # Display the raw data
    st.write(gdf)

    st.subheader('Map of all pickups')
    st.map(data)

else:
    st.write("Please upload a file to get started.")
