import streamlit as st

# Note: Place 'HDB Resale Price Prediction.py' and 'Map Data.py' into a 'pages' folder (one layer below the folder for the Home.py)
# Run streamlit through Home.py as a landing page
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to HDB Resale Units App! 👋")

st.sidebar.success("Select an application above.")

st.markdown(
    """
    Please select the application you want to use:
    1. HDB Resale Price Prediction📊
        - Predict HDB Resale Unit price using: 
            - Floor area (sqft),
            - Age of the unit, 
            - Storey,
            - Distance to nearest hawker,
            - Distance to nearest MRT Station,
            - Transaction Year,
            - Town
    
    2. Map Data🌍
        - For agent reference of past HDB resale unit transactions
"""
)