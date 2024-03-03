import numpy as np
import pandas as pd
import sys, os, re

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def treat_price(x):
    if type(x) == float:
        return x
    else:
        if x[1] == 'Lac':
            return round(float(x[0])/100, 2)
        else:
            return round(float(x[0]), 2)

file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/flats.csv')

df = pd.read_csv(file_path)

print(f'DataFrame Info: \n{df.info()}', end = '\n\n')
print(f'Duplicates check: {df.duplicated().sum()}', end = '\n\n')
df = df.drop_duplicates()
print(f'Duplicate Columns: \n{df.isnull().sum()}', end = '\n\n')

print('Droping unrequired columns -> link, property_id\n\n')
df.drop(columns = ['link', 'property_id'],inplace=True)

print('Preprocessing column: society')
#print('Unique categories: {}\n\n'.format(df['society'].value_counts().shape))
df['society'] = df['society'].apply(lambda name: re.sub(r'\d+(\.\d+)?\s?★','',str(name)).strip()).str.lower()
print('Unique categories: {}\n\n'.format(df['society'].value_counts().shape))

print('Preprocessing column: price')
#print(df['price'].value_counts())
#print('Unique categories: {}\n\n'.format(df['price'].value_counts().shape))
print('''Dropping 'Price on Request' column \n\n''')
df = df[df['price'] != 'Price on Request']
df = df[df['price'] != 'price']
df = df[df['price'].notnull()]
df['price'] = df['price'].str.split(' ').apply(lambda x: treat_price(x))
#print(df['price'])

print('Preprocessing column: area')
#print(df['area'].value_counts())
df['area'] = df['area'].str.split('/').str.get(0).str.replace('₹','').str.replace(',','').str.strip().astype('float')
print('Renaming column area -> price per sqft\n\n')
df.rename(columns={'area':'price_per_sqft'}, inplace=True)

print('Preprocessing column: bedRoom, bathroom, balcony')
#print(df['bedRoom'].value_counts())
#print(df['bedRoom'].isnull().sum())
print('Renaming column bedRoom -> bedroom\n\n')
df.rename(columns={'bedRoom':'bedroom'}, inplace=True)
df = df[df['bedroom'].notnull()]
df['bedroom'] = df['bedroom'].str.split(' ').str.get(0).astype('int')
df = df[df['bathroom'].notnull()]
df['bathroom'] = df['bathroom'].str.split(' ').str.get(0).astype('int')
df = df[df['balcony'].notnull()]
df['balcony'] = df['balcony'].str.split(' ').str.get(0).str.replace('No','0')

print('Preprocessing column: additionalRoom\n\n')
#print(df['additionalRoom'].value_counts())
#print(df['additionalRoom'].isnull().sum())
df.fillna({'additionalRoom':'not available'}, inplace=True)
df['additionalRoom'] = df['additionalRoom'].str.lower()

print('Preprocessing column: floorNum\n\n')
#print(df['floorNum'].value_counts())
#print(df['floorNum'].isnull().sum())
df['floorNum'] = df['floorNum'].str.split(' ').str.get(0).replace('Ground', '0').\
    str.replace('Basement', '-1').str.replace('Lower', '0').str.extract(r'(\d+)')
    

print('Preprocessing column: facing\n\n')
#print(df['facing'].value_counts())
#print(df['facing'].isnull().sum())
df.fillna({'facing':'NA'}, inplace=True)
df.insert(loc=4, column='area', value=round((df['price']*10000000) / df['price_per_sqft']))

df.insert(loc=1, column='property_type', value = 'flat')

print(f'DataFrame Shape: {df.shape}', end = '\n\n')

print('Writing data in clean_data directory')
file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'clean_data/flats_cleaned.csv')
df.to_csv(file_path, index=False)
