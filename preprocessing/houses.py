import numpy as np
import pandas as pd
import os, sys, re

def treat_price(x):
    if type(x) == float:
        return x
    else:
        if x[1] == 'Lac':
            return round(float(x[0])/100, 2)
        else:
            return round(float(x[0]), 2)

file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/independent-house.csv')
df = pd.read_csv(file_path)
print(f'DataFrame Shape: {df.shape}', end = '\n\n')
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
df['society'] = df['society'].str.replace('nan', 'independent')

print('Preprocessing column: price')
#print(df['price'].value_counts())
#print('Unique categories: {}\n\n'.format(df['price'].value_counts().shape))
print('''Dropping 'Price on Request' column \n\n''')
df = df[df['price'] != 'Price on Request']
df = df[df['price'] != 'price']
df = df[df['price'].notnull()]
df['price'] = df['price'].str.split(' ').apply(lambda x: treat_price(x))
#print(df['price'])

print('Preprocessing column: rate')
#print(df['area'].value_counts())
df['rate'] = df['rate'].str.split('/').str.get(0).str.replace('₹','').str.replace(',','').str.strip().astype('float')
print('Renaming column area -> price per sqft\n\n')
df.rename(columns={'rate':'price_per_sqft'}, inplace=True)

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

print('Preprocessing column: noOfFloor\n\n')
#print(df['additionalRoom'].value_counts())
#print(df['additionalRoom'].isnull().sum())
df['noOfFloor'] = df['noOfFloor'].str.split(' ').str.get(0)
df.rename(columns = {'noOfFloor':'floorNum'}, inplace=True)

print('Preprocessing column: facing\n\n')
#print(df['facing'].value_counts())
#print(df['facing'].isnull().sum())
df.fillna({'facing':'NA'}, inplace=True)
df['area'] = round((df['price']*10000000) / df['price_per_sqft'])

df.insert(loc=1, column='property_type', value = 'house')

file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'clean_data/houses_cleaned.csv')
df.to_csv(file_path, index=False)
