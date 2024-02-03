import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium

def load_data(file):
    try:
        df = pd.read_csv(file)
        return df
    except pd.errors.EmptyDataError:
        st.error("Error: The uploaded file is empty. Please choose a valid CSV file.")
        st.stop()
    except pd.errors.ParserError:
        st.error("Error: Unable to parse the CSV file. Make sure it follows the correct format.")
        st.stop()

def show_map(df):
    st.map(df, use_container_width=True)

def main():
    st.title("Geospatial Data Visualization")
    st.markdown("Upload a csv file containing langitude and latitude")
    # Sidebar
    st.sidebar.header("Options")
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

    # Main content
    if uploaded_file is not None:
        df = load_data(uploaded_file)

        # Ensure required columns are present
        required_columns = {'latitude', 'longitude'}
        if not required_columns.issubset(df.columns):
            st.error(f"Error: The CSV file must have columns {', '.join(required_columns)}.")
            st.stop()

        # Convert latitude and longitude columns to numeric
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

        show_map(df)

if __name__ == "__main__":
    main()
