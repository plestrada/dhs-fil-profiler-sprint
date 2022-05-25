import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
import geopandas as gpd
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv("data/PH-HRIR-merged.csv")
my_page = st.sidebar.radio('Page Navigation', ['page 1', 'page 2', 'page 3', 'page 4', 'page 5'])

if my_page == 'page 1':
    st.title("Data")
    st.header("2017 Philippines Standard DHS Dataset")
    if st.checkbox('Show data', value = True):
        st.subheader('Data')
        data_load_state = st.text('Loading data...')
        st.write(df.head(20))
        data_load_state.markdown('Loading data...**done!**')
    
elif my_page == 'page 2':
    option = st.sidebar.selectbox('Which region do you want to see?', df['HV024'].unique())

    'You selected: ', option

    province_level = df[df['HV024'] == option].groupby("SPROV").size()

    st.header(f"Bar chart of {option}")

    fig = plt.figure(figsize=(8,6)) 

    plt.barh(province_level.index, province_level.values) 

    plt.title("Number of Eligible Women Interviewed by Province", fontsize=16)
    plt.xlabel("Number of Women", fontsize=12)
    plt.ylabel("Province", fontsize=12)

    st.pyplot(fig)
    
elif my_page == 'page 3':
    st.title("Geospatial Analysis: Folium")
    shapefile = gpd.read_file('data/geo/Provinces/Provinces.shp')
    shapefile["x"] = shapefile.geometry.centroid.x
    shapefile["y"] = shapefile.geometry.centroid.y
    map_center = [14.583197, 121.051538]

    mymap = folium.Map(location=map_center, height=700, width=1000, tiles="OpenStreetMap", zoom_start=14)
    option_reg = st.sidebar.selectbox(
        'Which region',
        shapefile["REGION"].unique())
    
    'You selected: ', option_reg
    
    reg = option_reg
    df_reg = shapefile[shapefile["REGION"]==reg]

    for i in np.arange(len(df_reg)):
        lat = df_reg["y"].values[i]
        lon = df_reg["x"].values[i]
        name = df_reg["PROVINCE"].values[i]
        folium.Marker([lat, lon], popup=name).add_to(mymap)
    folium_static(mymap)
    
elif my_page == 'page 4':
    st.title("Geospatioal Analysis: st.map()")
    shapefile = gpd.read_file('data/Provinces/Provinces.shp')
    shapefile["lat"] = shapefile.geometry.centroid.x
    shapefile["lon"] = shapefile.geometry.centroid.y
    st.map(shapefile)
    
elif my_page == 'page 5':
    st.title("Geospatial Analysis: Geopandas")
    merged_data = gpd.read_file("data/geo/map-clean.shp")
   
    variable = 'ave_age_1birth'
    vmin, vmax = merged_data[variable].min(), merged_data[variable].max()
    fig, ax = plt.subplots(1, figsize=(15, 10))
    merged_data.plot(column=variable, cmap='Oranges', linewidth=0.8, ax=ax, edgecolor='0.8', vmin=vmin, vmax=vmax)
    plt.xlim(115,130)
    plt.ylim(0,25)
    sm = plt.cm.ScalarMappable(cmap='Oranges', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    cbar = fig.colorbar(sm)
    st.pyplot(fig)