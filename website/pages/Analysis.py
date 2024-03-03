import streamlit as st
import pandas as pd
import os, pickle
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.set_page_config(page_title='Plotting Demo')

st.title('Analytics')

file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'final_model_data/')

with open(file_path + 'map_df.pkl', 'rb') as file:
    new_df = pickle.load(file)
    
#st.dataframe(new_df)

group_df = new_df[['sector','price','price_per_sqft','built_up_area','latitude','longitude']].groupby('sector').\
    mean()[['price','price_per_sqft','built_up_area','latitude','longitude']]
    
st.header('Geo Map')
fig = px.scatter_mapbox(group_df, lat = 'latitude', lon = 'longitude', color = 'price_per_sqft',
                        size = 'built_up_area', color_continuous_scale=px.colors.cyclical.IceFire,
                        zoom = 10, mapbox_style='open-street-map', text = group_df.index,
                        hover_name=group_df.index, width=1200, height=700)

st.plotly_chart(fig, use_container_width=True)

with open(file_path + 'wordcloud.pkl', 'rb') as file:
    wordcloud_df = pickle.load(file)

st.header('Sector WordCloud')    
sector = st.selectbox('Sector', wordcloud_df['sector_y'])

feature = wordcloud_df[wordcloud_df['sector_y'] == sector]['features']

feature_text = ' '.join(feature)

plt.rcParams['font.family'] = 'Arial'

wordcloud = WordCloud(width=800, height=800,
                      background_color='white',
                      stopwords=set(['s']),
                      min_font_size=10).generate(feature_text)

plt.figure(figsize=(8,8), facecolor=None)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.tight_layout(pad = 0)
plt.show()

st.pyplot(plt)

st.header('Area Vs Price')

property_type = st.selectbox('Select Property Type',['flat', 'house'])
sector = st.selectbox('Select Sector', new_df['sector'].unique(), key='scatter')
min_bua = new_df['built_up_area'].min()
max_bua = new_df['built_up_area'].max()
built_up_area = st.slider(label = 'Select Build Up Area', min_value = min_bua, max_value = max_bua, value=(min_bua, max_bua))

try:
    if st.button('Show', key = 'scatter_button'):
        rec_df = new_df[new_df['property_type'] == property_type]
        rec_df = rec_df[(rec_df['built_up_area'] >= built_up_area[0]) & (rec_df['built_up_area'] <= built_up_area[1])]
        rec_df = rec_df[rec_df['sector'] == sector]
        fig1 = px.scatter(rec_df, x = 'built_up_area', y='price', color = 'bedroom')
        st.plotly_chart(fig1, use_container_width=True)
except Exception as e:
    temp_df = pd.DataFrame(columns = new_df.columns.to_list())
    fig_temp = px.scatter(temp_df, x = 'built_up_area', y='price', color = 'bedroom')
    st.plotly_chart(fig_temp, use_container_width=True)
    

st.header('BHK Property Available')

sector_pie = st.selectbox('Select Sector', new_df['sector'].unique(), key='pie_selectbox')

if st.button('Show', key='pie_button'):
    fig2 = px.pie(title=f'BHK Property Available in {sector_pie}', names='bedroom', data_frame=new_df)
    st.plotly_chart(fig2, use_container_width=True)
    
