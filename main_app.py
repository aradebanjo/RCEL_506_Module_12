import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. SETUP & DATA LOADING
# Replace this with: df = pd.read_csv("your_file.csv")
# Creating dummy data for demonstration
data = {
    'station_id': [1, 2, 3, 4, 5],
    'lat': [19.4326, 19.4214, 19.4361, 19.4180, 19.4270],
    'lon': [-99.1332, -99.1633, -99.1500, -99.1700, -99.1400]
}
df = pd.DataFrame(data)

# 2. ROW 1: Title and Caption
st.title("🚲 Ecobici Station Finder")
st.caption("Created by [Your Name Here]")

st.divider() # Optional visual separator

# 3. ROW 2: Logic and Layout
# We create two columns. The first number is the width ratio.
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Controls")
    # Dropdown menu to select station
    selected_id = st.selectbox(
        "Select a Station ID:",
        options=df['station_id'].unique()
    )
    
    st.write(f"Showing details for station **#{selected_id}**")

with col2:
    # We modify your function slightly to RETURN the map instead of just displaying it
    def bike_share_system_plot(station_number):
        # Center map on average coordinates
        m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=13)

        # Plot all stations (Red)
        for n in range(len(df)):
            folium.Marker(
                location=[df['lat'].iloc[n], df['lon'].iloc[n]],
                tooltip=f"Station {df['station_id'].iloc[n]}",
                icon=folium.Icon(color="red"),
            ).add_to(m)

        # Filter and highlight selected station (Blue)
        temp = df[df['station_id'] == station_number]
        if not temp.empty:
            folium.Marker(
                location=[temp['lat'].iloc[0], temp['lon'].iloc[0]],
                tooltip=f"Selected: {temp['station_id'].iloc[0]}",
                icon=folium.Icon(color="blue", icon="cloud"),
            ).add_to(m)
        
        return m

    # Call the function and display it in Streamlit
    my_map = bike_share_system_plot(selected_id)
    st_folium(my_map, width=700, height=500, returned_objects=[])
