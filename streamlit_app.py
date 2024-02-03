import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium

def load_data(file):
    return pd.read_csv(file)

def show_map(df, lat_col, lon_col, use_clusters, map_style):
    st.header("Geospatial Data Visualization")
    
    if st.checkbox("Show Data", True):
        st.write(df)

    folium_map = folium.Map(location=[df[lat_col].mean(), df[lon_col].mean()], zoom_start=12, control_scale=True)

    if use_clusters:
        marker_cluster = folium.MarkerCluster().add_to(folium_map)
        for idx, row in df.iterrows():
            folium.Marker([row[lat_col], row[lon_col]]).add_to(marker_cluster)
    else:
        for idx, row in df.iterrows():
            folium.Marker([row[lat_col], row[lon_col]]).add_to(folium_map)

    folium_static(folium_map)

def main():
    st.title("Interactive Geospatial Data Visualization")

    # Sidebar
    st.sidebar.header("Options")
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = load_data(uploaded_file)

        # Check if required columns are present
        if 'latitude' not in df.columns or 'longitude' not in df.columns:
            st.error("The CSV file must have 'latitude' and 'longitude' columns.")
            st.stop()

        st.sidebar.subheader("Map Settings")
        lat_col = st.sidebar.selectbox("Select Latitude Column", df.columns)
        lon_col = st.sidebar.selectbox("Select Longitude Column", df.columns)

        use_clusters = st.sidebar.checkbox("Use Marker Clusters", True)
        map_styles = ["OpenStreetMap", "Stamen Terrain", "Stamen Toner", "Stamen Watercolor", "CartoDB Positron"]
        map_style = st.sidebar.selectbox("Select Map Style", map_styles)

        # Main content
        show_map(df, lat_col, lon_col, use_clusters, map_style)

if __name__ == "__main__":
    main()
