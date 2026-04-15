import streamlit as st
import pandas as pd
import folium
import requests
from streamlit_folium import st_folium

# --- STEP 1: FETCH LIVE DATA ---
@st.cache_data # This prevents reloading data every time you click a button
def get_ecobici_data():
    url = "https://api.citybik.es/v2/networks/ecobici"
    response = requests.get(url).json()
    stations = response['network']['stations']
    
    # Convert JSON to DataFrame
    df = pd.DataFrame(stations)
    # Extract lat/lon from the 'latitude' and 'longitude' keys in the API
    # The API returns 'name', 'latitude', 'longitude', 'free_bikes', etc.
    return df

try:
    df = get_ecobici_data()
except Exception as e:
    st.error(f"Could not connect to Ecobici API: {e}")
    df = pd.DataFrame() # Fallback

# --- STEP 2: ROW 1 (Title & Name) ---
st.title("🚲 Live Ecobici Network Map")
st.caption("Developed by [Your Name] | Data source: CityBikes API & CDMX Open Data")

# --- STEP 3: ROW 2 (Controls & Map) ---
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Station Search")
    # Search by station name instead of just ID for better UX
    station_names = sorted(df['name'].tolist())
    selected_name = st.selectbox("Select a station:", station_names)
    
    # Get details for the selected station
    selected_station = df[df['name'] == selected_name].iloc[0]
    
    st.metric("Bikes Available", selected_station['free_bikes'])
    st.metric("Empty Slots", selected_station['empty_slots'])

with col2:
    def create_map(current_station):
        # Center on CDMX
        m = folium.Map(
            location=[df['latitude'].mean(), df['longitude'].mean()], 
            zoom_start=13,
            tiles="cartodbpositron" # Cleaner map style
        )

        # Plot ALL stations as small circles to keep the map fast
        for _, row in df.iterrows():
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=3,
                color="red",
                fill=True,
                fill_color="red",
                tooltip=row['name']
            ).add_to(m)

        # Highlight the SELECTED station with the Blue Cloud Icon
        folium.Marker(
            location=[current_station['latitude'], current_station['longitude']],
            tooltip=f"SELECTED: {current_station['name']}",
            icon=folium.Icon(color="blue", icon="cloud"),
            z_index_offset=1000 # Make sure it stays on top
        ).add_to(m)
        
        return m

    # Render map
    if not df.empty:
        map_object = create_map(selected_station)
        st_folium(map_object, width=700, height=500)
