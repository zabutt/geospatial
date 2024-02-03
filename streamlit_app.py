import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium

# Function to load data from CSV file
def load_data(file):
    df = pd.read_csv(file)
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
    return df

# Function to display the map
def show_map(df):
    st.subheader("Geospatial Data Visualization")
    st.map(df)

# Main function
def main():
    st.title("Geospatial Data Visualization App")

    # Upload CSV file or choose from provided options
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file:
        # Load data from the uploaded file
        df = load_data(uploaded_file)

        if not df.empty:
            # Display the map with the uploaded data
            show_map(df)
        else:
            st.warning("The uploaded file is empty or does not contain valid geospatial data.")

if __name__ == "__main__":
    main()
