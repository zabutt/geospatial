import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium

def load_data(file):
    return pd.read_csv(file)

def show_map(df):
    st.map(df, use_container_width=True)

def main():
    st.title("Geospatial Data Visualization")

    # Sidebar
    st.sidebar.header("Options")
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

    # Main content
    if uploaded_file is not None:
        df = load_data(uploaded_file)

        # Convert latitude and longitude columns to numeric
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

        show_map(df)

if __name__ == "__main__":
    main()

