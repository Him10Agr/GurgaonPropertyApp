import streamlit as st
import pickle, sys, os
import pandas as pd
import numpy as np

st.set_page_config(page_title='Viz Demo')

file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'final_model_data')

with open(f'{file_path}/pipeline.pkl', 'rb') as file:
    pipeline = pickle.load(file)
    
with open(f'{file_path}/df.pkl', 'rb') as file:
    df = pickle.load(file)

#st.dataframe(df)

st.header('Enter Your Inputs')

#property type
property_type = st.selectbox('Property Type', sorted(df['property_type'].unique().tolist()))

#sectors
sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))

#bedroom
bedroom = float(st.selectbox('Number of Bedroom', sorted(df['bedroom'].unique().tolist())))

#bathroom
bathroom = float(st.selectbox('Number of Bathroom', sorted(df['bathroom'].unique().tolist())))

#balcony
balcony = st.selectbox('Number of Balconies', sorted(df['balcony'].unique().tolist()))

#property_age
property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))

#built_up_area
built_up_area = float(st.number_input('Built Up Area'))

#servant room
servantroom = float(st.selectbox('Number of Servant Room', sorted(df['servant room'].unique().tolist())))

#store room
storeroom = float(st.selectbox('Number of Store Room', sorted(df['store room'].unique().tolist())))

#furnishing_type
furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))

#luxury_score
luxury_score = st.selectbox('Luxury Type', sorted(df['luxury_score'].unique().tolist()))

#floorNum
floorNum = st.selectbox('Floor type', sorted(df['floorNum'].unique().tolist()))

if st.button('Predict'):
    
    #form a dataframe
    data = [[property_type, sector, bedroom, bathroom, balcony, 
             floorNum, property_age, built_up_area, servantroom, storeroom, 
             furnishing_type, luxury_score]]
    columns = df.columns.to_list()
    
    one_df = pd.DataFrame(data = data, columns = columns)
    
    #st.dataframe(one_df)
    
    #pedict
    
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low_price = base_price - 0.3
    high_price = base_price + 0.3
    
    st.text('''The price of the flat is expected to be between ₹ {} Cr. and ₹ {} Cr.'''\
        .format(round(low_price, 2), round(high_price, 2)))
    #display