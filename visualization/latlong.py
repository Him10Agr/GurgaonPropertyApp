import requests
from bs4 import BeautifulSoup
import pandas as pd
import os, sys, pickle, random, time

BASE_URL = "https://www.google.com/search?q="


def get_coordinates(sector):
    
    #HEADERS = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'}
    
    user_agent = random.choice(('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0',
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
                  ))
    
    HEADERS = {'User-Agent':f'{user_agent}'}
    search_term = f'sector {sector} gurgaon longitude & latitude'
    response = requests.get(BASE_URL + search_term, headers=HEADERS)
    time.sleep(2)
    print(response.status_code)
    if response.status_code == 200:
        
        soup = BeautifulSoup(response.content, 'html.parser')
        coordinates_div = soup.find("div", {"class" : "Z0LcW t2b5Cf"})
        if coordinates_div:
            return coordinates_div.text
    
    return None

file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'final_model_data/sectors.pkl')
with open(file_path, 'rb') as file:
    sectors = pickle.load(file)


df = pd.DataFrame(columns = ['Sector', 'Coordinates'])
for sector in sectors:
    number = sector.split('sector')[-1]
    coordinates = get_coordinates(number)
    temp_df = pd.DataFrame({'Sector':[f'{sector}'], 'Coordinates':[coordinates]})
    df = pd.concat([df, temp_df], ignore_index = True)
    df.reset_index()
    print(sector, coordinates)

file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'final_model_data/latlong.csv')
df.to_csv(file_path)

'''
file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'final_model_data/latlong.pkl')
with open(file_path, 'wb') as file:
    pickle.dump(df, file)
'''