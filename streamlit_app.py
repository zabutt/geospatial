import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import FastMarkerCluster

def load_data(file):
    df = pd.read_csv(file)
    return df

def show_map(df, lat_col, lon_col, use_clusters, map_style):
    st.header("Geospatial Data Visualization")

    if st.checkbox("Show Data", True):
        st.write(df)

    folium_map = folium.Map(location=[df[lat_col].mean(), df[lon_col].mean()], zoom_start=12, control_scale=True)

    if use_clusters:
        data = list(zip(df[lat_col], df[lon_col]))
        FastMarkerCluster(data).add_to(folium_map)
    else:
        for idx, row in df.iterrows():
            folium.Marker([row[lat_col], row[lon_col]]).add_to(folium_map)

    folium_static(folium_map, width=800, height=600)

    # Set the map style
    if map_style == "OpenStreetMap":
        folium.TileLayer("openstreetmap").add_to(folium_map)
    elif map_style == "Stamen Terrain":
        folium.TileLayer("stamenterrain", attr="Stamen Terrain").add_to(folium_map)
    elif map_style == "Stamen Toner":
        folium.TileLayer("stamentoner", attr="Stamen Toner").add_to(folium_map)
    elif map_style == "Stamen Watercolor":
        folium.TileLayer("stamenwatercolor", attr="Stamen Watercolor").add_to(folium_map)
    elif map_style == "CartoDB Positron":
        folium.TileLayer("cartodbpositron").add_to(folium_map)

    folium.LayerControl().add_to(folium_map)

def main():
    st.title("Geospatial Data Explorer")

    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            df = load_data(uploaded_file)

            if 'latitude' not in df.columns or 'longitude' not in df.columns:
                st.error("Please make sure your CSV file has columns named 'latitude' and 'longitude'.")
            else:
                st.success("File uploaded successfully!")

                st.sidebar.subheader("Map Settings")
                lat_col = st.sidebar.selectbox("Select Latitude Column", df.columns, key='lat')
                lon_col = st.sidebar.selectbox("Select Longitude Column", df.columns, key='lon')
                use_clusters = st.sidebar.checkbox("Use Marker Clusters", value=True)
                map_style = st.sidebar.selectbox("Select Map Style", ["OpenStreetMap", "Stamen Terrain", "Stamen Toner", "Stamen Watercolor", "CartoDB Positron"])

                show_map(df, lat_col, lon_col, use_clusters, map_style)

        except pd.errors.EmptyDataError:
            st.error("Uploaded file is empty. Please upload a valid CSV file.")

if __name__ == "__main__":
    main()

