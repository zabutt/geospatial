import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Sample CSV files with geospatial data
file_options = {
    "Option 1": "data/option1.csv",
    "Option 2": "data/option2.csv",
    "Option 3": "data/option3.csv",
}

def load_data(file):
    try:
        df = pd.read_csv(file)
        if set(["Latitude", "Longitude", "Location"]).issubset(df.columns):
            return df
        else:
            raise ValueError(f"Invalid CSV file '{file}'. Please ensure it contains 'Latitude', 'Longitude', and 'Location' columns.")
    except pd.errors.EmptyDataError:
        raise ValueError(f"Empty CSV file '{file}'. Please upload a file with valid data.")
    except pd.errors.ParserError:
        raise ValueError(f"Unable to parse the CSV file '{file}'. Please check the file format and try again.")

def main():
    st.title("Geospatial Data Visualization App")

    # Option to select predefined CSV files
    selected_option = st.selectbox("Select a predefined CSV file:", list(file_options.keys()))

    if selected_option == "Upload Your Own":
        # Upload CSV file with location data
        file = st.file_uploader("Upload a CSV file with location data", type=["csv"])

        if file is not None:
            try:
                df = load_data(file)

                st.subheader("Raw Data:")
                st.write(df)

                map_center = [df['Latitude'].mean(), df['Longitude'].mean()]
                my_map = folium.Map(location=map_center, zoom_start=12)

                for index, row in df.iterrows():
                    folium.Marker([row['Latitude'], row['Longitude']], popup=row['Location']).add_to(my_map)

                st.subheader("Geospatial Visualization:")
                folium_static(my_map)

            except ValueError as ve:
                st.error(str(ve))
    else:
        # Load predefined CSV file
        selected_file = file_options[selected_option]
        try:
            df = load_data(selected_file)

            st.subheader("Raw Data:")
            st.write(df)

            map_center = [df['Latitude'].mean(), df['Longitude'].mean()]
            my_map = folium.Map(location=map_center, zoom_start=12)

            for index, row in df.iterrows():
                folium.Marker([row['Latitude'], row['Longitude']], popup=row['Location']).add_to(my_map)

            st.subheader("Geospatial Visualization:")
            folium_static(my_map)

        except ValueError as ve:
            st.error(str(ve))

if __name__ == "__main__":
    main()
