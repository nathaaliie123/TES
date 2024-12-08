import streamlit as st
import pydeck as pdk
import pandas as pd

# Expanded city connection data 
data = {
    "West Java": [
        ("Bandung", "Bogor"),
        ("Bandung", "Cirebon"),
        ("Bandung", "Bekasi"),
        ("Bogor", "Cirebon"),
        ("Bogor", "Sukabumi"),
        ("Sukabumi", "Garut"),
        ("Garut", "Tasikmalaya"),
        ("Tasikmalaya", "Ciamis"),
        ("Cirebon", "Indramayu"),
        ("Bandung", "Sumedang"),
    ],
    "Central Java": [
        ("Semarang", "Surakarta"),
        ("Semarang", "Purwokerto"),
        ("Surakarta", "Purwokerto"),
        ("Purwokerto", "Magelang"),
        ("Magelang", "Kudus"),
        ("Kudus", "Semarang"),
        ("Semarang", "Tegal"),
        ("Tegal", "Pekalongan"),
        ("Pekalongan", "Cilacap"),
        ("Cilacap", "Purwokerto"),
    ],
    "East Java": [
        ("Surabaya", "Malang"),
        ("Surabaya", "Jember"),
        ("Malang", "Banyuwangi"),
        ("Jember", "Banyuwangi"),
        ("Surabaya", "Probolinggo"),
        ("Probolinggo", "Malang"),
        ("Malang", "Kediri"),
        ("Kediri", "Madiun"),
        ("Madiun", "Blitar"),
        ("Blitar", "Surabaya"),
    ],
}

# Expanded coordinates for cities
city_coords = {
    "Bandung": [107.6191, -6.9175],
    "Bogor": [106.8060, -6.5950],
    "Cirebon": [108.5523, -6.7322],
    "Sukabumi": [106.9274, -6.9225],
    "Garut": [107.9046, -7.2111],
    "Tasikmalaya": [108.2207, -7.3506],
    "Ciamis": [108.3556, -7.3250],
    "Indramayu": [108.3248, -6.3265],
    "Sumedang": [107.9190, -6.8588],
    "Semarang": [110.4391, -6.9666],
    "Surakarta": [110.8279, -7.5563],
    "Purwokerto": [109.2349, -7.4215],
    "Magelang": [110.2177, -7.4706],
    "Kudus": [110.8629, -6.8049],
    "Tegal": [109.1256, -6.8693],
    "Pekalongan": [109.6753, -6.8895],
    "Cilacap": [109.0021, -7.7406],
    "Surabaya": [112.7398, -7.2504],
    "Malang": [112.6304, -7.9787],
    "Jember": [113.7038, -8.1845],
    "Banyuwangi": [114.3697, -8.2192],
    "Probolinggo": [113.2221, -7.7543],
    "Kediri": [112.0155, -7.8487],
    "Madiun": [111.5231, -7.6318],
    "Blitar": [112.1783, -8.0953],
}

st.title("City Connections Map in Java Province, Indonesia")

# Province selection
province = st.selectbox("Select a province", options=list(data.keys()))

# Prepare data for visualization
if province in data:
    connections = data[province]
    connection_df = pd.DataFrame(connections, columns=["City1", "City2"])
    
    # Create a DataFrame for lines
    lines = []
    for city1, city2 in connections:
        if city1 in city_coords and city2 in city_coords:
            lines.append({
                "start_lat": city_coords[city1][1],
                "start_lon": city_coords[city1][0],
                "end_lat": city_coords[city2][1],
                "end_lon": city_coords[city2][0],
            })
    lines_df = pd.DataFrame(lines)
    
    # Create a Pydeck Layer for 2D lines
    line_layer = pdk.Layer(
        "LineLayer",
        data=lines_df,
        get_source_position=["start_lon", "start_lat"],
        get_target_position=["end_lon", "end_lat"],
        get_width=2,
        get_color=[255, 0, 0],  # Red lines for connections
    )
    
    # Create a map centered on the first city in the province
    first_city_coords = city_coords[connections[0][0]]
    view_state = pdk.ViewState(
        longitude=first_city_coords[0],
        latitude=first_city_coords[1],
        zoom=7,
        pitch=0,
    )
    
    # Colorful map style
    st.pydeck_chart(pdk.Deck(
        initial_view_state=view_state,
        layers=[line_layer],
        map_style="mapbox://styles/mapbox/streets-v11",  # Colorful map style
    ))
else:
    st.write("No data available for the selected province.")
