import streamlit as st
import pandas as pd
import pickle, os, sys

st.set_page_config(page_title='Recommend Real Estate Properties')

def recommend_properties(property_name):
    
    cosine_sim = (cosine_sim_facilities + cosine_sim_loc + cosine_sim_price) / 3
    #index with id of property name
    idx = location_df.index.get_loc(property_name)
    
    #similarity score with the property
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    #sort the properties based on similarity score
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse=True)
    
    #Scores of 5 most similar properties
    sim_scores = sim_scores[1:6]
    
    #corresponding property indices
    property_indices = [i[0] for i in sim_scores]
    
    recommendation_df = pd.DataFrame({
        'Property Name': location_df.index[property_indices].tolist(),
        'Similarity Score': sim_scores
        
    })
    
    return recommendation_df

file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'final_model_data/')

with open(file_path + 'recommend_loc.pkl', 'rb') as file:
    location_df = pickle.load(file)
    
with open(file_path + 'cosine_sim_facilities.pkl', 'rb') as file:
    cosine_sim_facilities = pickle.load(file)
    
with open(file_path + 'cosine_sim_price.pkl', 'rb') as file:
    cosine_sim_price = pickle.load(file)
    
with open(file_path + 'cosine_sim_loc.pkl', 'rb') as file:
    cosine_sim_loc = pickle.load(file)
    
if 'store' not in st.session_state:
    st.session_state.store = False
 
#st.dataframe(location_df)

st.header('Select Location and Radius')

location = st.selectbox('Location', location_df.columns.to_list())

distance = st.number_input('Radius in Km')

if 'store' not in st.session_state:
    st.session_state.store = False

if st.button('Search', key = 'location') or st.session_state.store:
    
    st.session_state.store = True
    result = location_df[location_df[location] <= distance * 1000][location].sort_values().to_dict()
    
    appartment = []
    distances = []
    for key, value in result.items():
        appartment.append(key)
        distances.append(str(round(value / 1000)) + ' Kms')
        st.text(f'{key} - {round(value / 1000)} Km')


    st.header('Recommend Appartments')
    appartment = st.selectbox('Select an Appartment', sorted(location_df.index.to_list()))

    if st.button('Recommend'):
        st.dataframe(recommend_properties(appartment)['Property Name'])
    
