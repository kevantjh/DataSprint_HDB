import streamlit as st
import numpy as np
import pandas as pd
import joblib

# Load our trained model
hdb_model = joblib.load('random_forest.pkl')

st.title("HDB Resale Price Prediction📊")

# Create variables for towns to be used for selection
towns = ['ANG MO KIO','BEDOK', 'BISHAN', 'BUKIT BATOK',
        'BUKIT MERAH', 'BUKIT PANJANG', 'BUKIT TIMAH',
        'CENTRAL AREA', 'CHOA CHU KANG', 'CLEMENTI',
        'GEYLANG', 'HOUGANG', 'JURONG EAST', 'JURONG WEST',
        'KALLANG/WHAMPOA', 'MARINE PARADE', 'PASIR RIS',
        'PUNGGOL', 'QUEENSTOWN', 'SEMBAWANG', 'SENGKANG',
        'SERANGOON', 'TAMPINES', 'TOA PAYOH', 'WOODLANDS',
        'YISHUN']

#Each selectbox represents one variable for user input
town = st.selectbox(
    "Insert the town of the HDB unit",
    index=None,
    placeholder="Select a town...",
    options=towns
)

floor_area_sqft = st.number_input(
    "Insert the size (in sqft) of the HDB unit",
    value=None, 
    placeholder="Type a number..."
)

age_sold = st.number_input(
    "Insert the current age of the HDB unit", 
    value=None,
    step=1,
    format="%d",
    placeholder="Type a number..."
)

mid = st.number_input(
    "Insert the storey of the HDB unit", 
    value=None,
    step=1,
    format="%d",
    placeholder="Type a number..."
)

hawker_nearest_distance = st.number_input(
    "Insert the distance (in metres) to the nearest hawker",
    value=None,
    placeholder="Type a number..."
)

mrt_nearest_distance = st.number_input(
    "Insert the distance (in metres) to the nearest MRT station",
    value=None,
    placeholder="Type a number..."
)

tranc_year = st.number_input(
    "Insert the transaction year of the HDB unit",
    value=None,
    step=1,
    format="%d",
    placeholder="E.g. 2015"
)

# Run the prediction model when user clicks "Predict Resale Price" button
if st.button("Predict Resale Price"):
    if None in (town, floor_area_sqft, age_sold, mid, hawker_nearest_distance, mrt_nearest_distance, tranc_year):
        st.warning("Please fill in all fields.")
    else:
        towns_model = ['BEDOK', 'BISHAN', 'BUKIT BATOK',
        'BUKIT MERAH', 'BUKIT PANJANG', 'BUKIT TIMAH',
        'CENTRAL AREA', 'CHOA CHU KANG', 'CLEMENTI',
        'GEYLANG', 'HOUGANG', 'JURONG EAST', 'JURONG WEST',
        'KALLANG/WHAMPOA', 'MARINE PARADE', 'PASIR RIS',
        'PUNGGOL', 'QUEENSTOWN', 'SEMBAWANG', 'SENGKANG',
        'SERANGOON', 'TAMPINES', 'TOA PAYOH', 'WOODLANDS',
        'YISHUN']
        #Initialize all towns into one-hot encoded format (except AMK which is dropped in the model)
        town_encoded = {f"town_{t}": 0 for t in towns_model}

        if town != 'ANG MO KIO':
            town_encoded[f"town_{town}"] = 1
        
        #Convert inputed data into dataframe and run the prediction model
        
        input_data = {
            'floor_area_sqft': floor_area_sqft,
            'age_sold': age_sold,
            'mid': mid,
            'hawker_nearest_distance': hawker_nearest_distance,
            'mrt_nearest_distance': mrt_nearest_distance,
            'tranc_year': tranc_year,
            **town_encoded
        }    

        input_df = pd.DataFrame([input_data])

        prediction = hdb_model.predict(input_df)[0]
        st.success(f"Predicted Resale Price: ${prediction:,.2f}")