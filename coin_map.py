

import matplotlib.pyplot as plt
import matplotlib.colors
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


coiners=['John Hyrcanus I','Aristobulus I','Alexander Jannaeus','Matityahu Antigonus','Herod I',
'Herod Archelaus','Herod Antipas','Herod Philip','Herod Agrippa I','Herod Agrippa II',
'Coponius','Marcus Ambivulus','Valerius Gratus','Pontius Pilate','Antonius Felix',
'Porcius Festus','First Revolt','Second Revolt']
categories = ['Hasmonean','Herodian','Procurator','First Revolt','Second Revolt']


# set streamlit options
st.set_page_config(layout="wide")
col1, col2 = st.columns((1,5))
a2 = col2.empty()

# Create a colormap
cmap = plt.get_cmap("coolwarm")

# get site data
column_types = {'Name':'str','Lat':'float','Long':float,'Ref':'str'}
site_df = pd.read_csv('site_data.csv',dtype=column_types)

#get coin_data
column_types = {'Coiner':'str','Category':'str','Number':'int','Site':'str'}
coin_df = pd.read_csv('coin_data.csv',dtype=column_types)
total=coin_df.Number.sum()

# create sidebar instructions and trim coin_df
col1.write('Instructions for using this site:')
instructions = """\nFrom this sidebar, choose the level of zoom, selecting the coins to map, and whether to include uncertain issuers or not."""
col1.write(instructions)
tile = col1.selectbox('Choose a map tile', ['OpenStreetMap', 'Stamen Terrain', 'Stamen Toner', 'Stamen Watercolor', 'Cartodb Positron',
                                                  'Cartodb dark_matter'], index=4)
zlevel = col1.slider('Choose level of zoom', min_value=0, max_value=10, value=3)
select_level = col1.radio('Choose level of coin selection',['Coiner/Ruler','Category'])
if select_level =='Coiner/Ruler':
    coin_group = col1.selectbox('Choose which coins to view',coiners,key='coiners select')
    coin_df = coin_df[coin_df.Coiner==coin_group]
elif select_level == 'Category':
    coin_group = col1.selectbox('Choose which coins to view',categories, key='category select')
    coin_df = coin_df[coin_df.Category==coin_group]

m = folium.Map(location=[31.77555556, 35.23527778], zoom_start=zlevel,
               tiles=tile,width='100%')

#map sites
mapping_df = coin_df.groupby('Site')['Number'].sum().reset_index()
for i, r in mapping_df.iterrows():
    name = mapping_df.loc[i, 'Site']
    st.write(f'A{name}A')
    lat = float(site_df.loc[site_df.Name==name,'Lat'].values[0])
    long = float(site_df.loc[site_df.Name==name, 'Long'].values[0])
    number = mapping_df.loc[i,'Number']
    normalized_number = number/total
    rgba = cmap(normalized_number)
    color = matplotlib.colors.to_hex(rgba)
    marker = folium.CircleMarker(
        location=[lat, long],popup=name,tooltip=f'{name} \nLat:{lat} \nLong:{long}',
        color=color,fill=True,fill_color=color, radius=1).add_to(m)
# add Western Wall
marker = folium.CircleMarker(location=[31.7767, 35.2345],
                             tooltip='Jerusalem', color='black', radius=1).add_to(m)
# st.markdown("""
#     <style>
#     .leaflet-container {
#         width: 100% !important;
#     }
#     </style>
#     """, unsafe_allow_html=True)

with col2:
    st_data = st_folium(m)
