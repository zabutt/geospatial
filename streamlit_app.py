import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap

def load_data(file):
    df = pd.read_csv(file)
    return df

def show_map_openstreetmap(df, lat_col, lon_col, use_clusters, use_heatmap):
    # Calculate center and bounds
    center = [df[lat_col].mean(), df[lon_col].mean()]
    bounds = [[df[lat_col].min(), df[lon_col].min()], [df[lat_col].max(), df[lon_col].max()]]

    # Create the folium map
    folium_map = folium.Map(location=center, zoom_start=12, control_scale=True)
    
    # Set the bounds
    folium_map.fit_bounds(bounds)

    if use_heatmap:
        heat_data = [[row[lat_col], row[lon_col]] for idx, row in df.iterrows()]
        HeatMap(heat_data).add_to(folium_map)
    elif use_clusters:
        data = list(zip(df[lat_col], df[lon_col]))
        folium.plugins.FastMarkerCluster(data).add_to(folium_map)
    else:
        for idx, row in df.iterrows():
            folium.Marker([row[lat_col], row[lon_col]]).add_to(folium_map)

    return folium_map

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
                use_heatmap = st.sidebar.checkbox("Use Heatmap", value=False)

                folium_map = show_map_openstreetmap(df, lat_col, lon_col, use_clusters, use_heatmap)

                if folium_map is not None:
                    folium_static(folium_map, width=800, height=600)

        except pd.errors.EmptyDataError:
            st.error("Uploaded file is empty. Please upload a valid CSV file.")

if __name__ == "__main__":
    main()
