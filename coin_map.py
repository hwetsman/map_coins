

# from pyproj import Transformer
# from pyproj import CRS
# from pyproj import Proj
# import pyproj
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
import math


def Get_Lat_Long(x, y, israel_lat_fudge, isreal_long_fudge):
    lat, long = transformer.transform(x, y)
    lat = lat + israel_lat_fudge
    long = long + israel_long_fudge
    return lat, long


# set streamlit options
st.set_page_config(layout="wide")
col1, col2 = st.columns(2)


# create coiner dict

# get site data
site_df = pd.read_csv('site_data.csv')


# create sidebar instructions
st.sidebar.write('Instructions for using this site:')
instructions = """\nFrom this sidebar, choose the level of zoom, the era to map, and whether or not you would like to include undated mikvot."""
st.sidebar.write(instructions)
tile = st.sidebar.selectbox('Choose a map tile', ['OpenStreetMap', 'Stamen Terrain', 'Stamen Toner', 'Stamen Watercolor', 'Cartodb Positron',
                                                  'Cartodb dark_matter'], index=4)
zlevel = st.sidebar.slider('Choose level of zoom', min_value=0, max_value=10, value=3)


# set map
m = folium.Map(location=[31.77555556, 35.23527778], zoom_start=zlevel,
               tiles=tile)


# trim df to user choices

#map sites
for i, r in site_df.iterrows():
    lat = site_df.loc[i, 'Lat']
    long = site_df.loc[i, 'Long']
    name = site_df.loc[i, 'Name']
    marker = folium.CircleMarker(
        location=[lat, long], popup=name, tooltip=f'{name} \nLat:{lat} \nLong:{long}', color='red', radius=1).add_to(m)
# add Western Wall
marker = folium.CircleMarker(location=[31.7767, 35.2345],
                             tooltip='western wall', color='blue', radius=1).add_to(m)


# # Convert ITM coordinates(x, y) to latitude and longitude(lat, long)
# x = 185000
# y = 97500
# lat, long = transformer.transform(x, y)
#
# print("Latitude: ", lat)
# print("Longitude: ", long)


# marker = folium.CircleMarker(
#     location=[lat+israel_lat_fudge, long+israel_long_fudge], color='green', radius=5).add_to(m)
# m.save(outfile=f'{e}_{a}_map.html')
# display map
with col1:
    st_data = st_folium(m)
