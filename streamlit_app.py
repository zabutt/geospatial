import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

def load_data(file):
    try:
        df = pd.read_csv(file)
        # Check if required columns are present
        if set(["Latitude", "Longitude", "Location"]).issubset(df.columns):
            return df
        else:
            raise ValueError("Invalid CSV file. Please ensure it contains 'Latitude', 'Longitude', and 'Location' columns.")
    except pd.errors.EmptyDataError:
        raise ValueError("Empty CSV file. Please upload a file with valid data.")
    except pd.errors.ParserError:
        raise ValueError("Unable to parse the CSV file. Please check the file format and try again.")

def main():
    st.title("Geospatial Data Visualization App")

    # Upload CSV file with location data
    file = st.file_uploader("Upload a CSV file with location data", type=["csv"])

    if file is not None:
        try:
            # Load data
            df = load_data(file)

            # Display raw data
            st.subheader("Raw Data:")
            st.write(df)

            # Create a folium map
            map_center = [df['Latitude'].mean(), df['Longitude'].mean()]
            my_map = folium.Map(location=map_center, zoom_start=12)

            # Plot markers on the map
            for index, row in df.iterrows():
                folium.Marker([row['Latitude'], row['Longitude']], popup=row['Location']).add_to(my_map)

            # Display the map
            st.subheader("Geospatial Visualization:")
            folium_static(my_map)

        except ValueError as ve:
            st.error(str(ve))

if __name__ == "__main__":
    main()
