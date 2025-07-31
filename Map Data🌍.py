import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import seaborn as sns

# Load HDB resale data
df = pd.read_csv("clean_train.csv")

# Setup default session states
if "filter_clicked" not in st.session_state:
    st.session_state.filter_clicked = False
if "applied_town" not in st.session_state:
    st.session_state.applied_town = df['town'].unique().tolist()
if "applied_years" not in st.session_state:
    st.session_state.applied_years = sorted(df['Tranc_Year'].unique())

# Sidebar headers and filters
st.sidebar.header("Map Data🌍")
towns = df['town'].unique()
years = sorted(df['Tranc_Year'].unique())

selected_town = st.sidebar.multiselect("Select Town", options=towns, default=None)
selected_years = st.sidebar.multiselect("Select Year(s)", options=years, default=None)

# Change session states once user clicks on "Filter Data"
if st.sidebar.button("Filter Data"):
    st.session_state.filter_clicked = True
    st.session_state.applied_town = selected_town
    st.session_state.applied_years = selected_years

if st.session_state.filter_clicked:
    # Filter data
    filtered_df = df[(df['town'].isin(st.session_state.applied_town)) & (df['Tranc_Year'].isin(st.session_state.applied_years))]

    # Assign colors for each year
    palette = sns.color_palette("hsv", len(selected_years)).as_hex()
    year_color_map = dict(zip(selected_years, palette))

    # Create base map for Singapore
    m = folium.Map(location=[1.3521, 103.8198], zoom_start=12)
    marker_cluster = MarkerCluster().add_to(m)

    # Plot points on map and use MarkerCluster to group points
    for _, row in filtered_df.iterrows():
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=5,
            color=year_color_map[row['Tranc_Year']],
            fill=True,
            fill_opacity=0.7,
            popup=(
                f"<b>Resale Price:</b> ${int(row['resale_price']):,}<br>"
                f"<b>Year:</b> {row['Tranc_Year']}<br>"
                f"<b>Full Flat Type:</b> {row['full_flat_type']}<br>"
                f"<b>Floor area (sqft):</b> {row['floor_area_sqft']}<br>"
                f"<b>Age of Unit when Sold:</b> {row['age_sold']}<br>"
            )
        ).add_to(marker_cluster)

    # Show map
    st.subheader(f"HDB Resale Prices in Singapore")
    st_folium(m, width=1000, height=600)

    # Show legend
    with st.expander("Show Legend"):
        for y in selected_years:
            st.markdown(f"<span style='color:{year_color_map[y]}'>&#9679;</span> {y}", unsafe_allow_html=True)

else:
    st.info("Select filters and click 'Filter Data' to view the map.")
