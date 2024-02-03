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
        folium.TileLayer("stamenterrain").add_to(folium_map)
    elif map_style == "Stamen Toner":
        folium.TileLayer("stamentoner").add_to(folium_map)
    elif map_style == "Stamen Watercolor":
        folium.TileLayer("stamenwatercolor").add_to(folium_map)
    elif map_style == "CartoDB Positron":
        folium.TileLayer("cartodbpositron").add_to(folium_map)

    folium.LayerControl().add_to(folium_map)
