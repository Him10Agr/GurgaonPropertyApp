import numpy as np
import pandas as pd
import os, sys, re, json
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import subprocess

file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'clean_data/gurgaon_properties_temp.csv')

df = pd.read_csv(file_path)

#print(df.duplicated().sum())

# focus is on -> areaWithType, additionalRoom, agePossession, furnishDetails, features 

'''Feature Engineering: areaWithType'''

#print(df[['area','areaWithType']].sample(5))

# This function extracts the Super Built up area
def get_super_built_up_area(text):
    match = re.search(r'Super Built up area (\d+\.?\d*)', str(text))
    if match:
        return float(match.group(1))
    return None

# This function extracts the Built Up area or Carpet area
def get_area(text, area_type):
    match = re.search(area_type + r'\s*:\s*(\d+\.?\d*)', str(text))
    if match:
        return float(match.group(1))
    return None

# This function checks if the area is provided in sq.m. and converts it to sqft if needed
def convert_to_sqft(text, area_value):
    if area_value is None:
        return None
    match = re.search(r'{} \((\d+\.?\d*) sq.m.\)'.format(area_value), str(text))
    if match:
        sq_m_value = float(match.group(1))
        return sq_m_value * 10.7639  # conversion factor from sq.m. to sqft
    return area_value

# Function to extract plot area from 'areaWithType' column
def extract_plot_area(area_with_type):
    match = re.search(r'Plot area (\d+\.?\d*)', str(area_with_type))
    return float(match.group(1)) if match else None

def convert_scale(row):
    if np.isnan(row['area']) or np.isnan(row['built_up_area']):
        return row['built_up_area']
    else:
        if round(row['area']/row['built_up_area']) == 9.0:
            return row['built_up_area'] * 9
        elif round(row['area']/row['built_up_area']) == 11.0:
            return row['built_up_area'] * 10.7
        else:
            return row['built_up_area']

# Extract Super Built up area and convert to sqft if needed
df['super_built_up_area'] = df['areaWithType'].apply(get_super_built_up_area)
df['super_built_up_area'] = df.apply(lambda x: convert_to_sqft(x['areaWithType'], x['super_built_up_area']), axis=1)

# Extract Built Up area and convert to sqft if needed
df['built_up_area'] = df['areaWithType'].apply(lambda x: get_area(x, 'Built Up area'))
df['built_up_area'] = df.apply(lambda x: convert_to_sqft(x['areaWithType'], x['built_up_area']), axis=1)

# Extract Carpet area and convert to sqft if needed
df['carpet_area'] = df['areaWithType'].apply(lambda x: get_area(x, 'Carpet area'))
df['carpet_area'] = df.apply(lambda x: convert_to_sqft(x['areaWithType'], x['carpet_area']), axis=1)

#print(df[['price','property_type','area','areaWithType','super_built_up_area','built_up_area','carpet_area']].sample(5))
#print(df[~((df['super_built_up_area'].isnull()) | (df['built_up_area'].isnull()) | (df['carpet_area'].isnull()))][['price',\
#    'property_type','area','areaWithType','super_built_up_area','built_up_area','carpet_area']].shape)
#print(df[df['areaWithType'].str.contains('Plot')][['price','property_type','area','areaWithType','super_built_up_area','built_up_area','carpet_area']].head(5))
#print(df.isnull().sum())
all_nan_df = df[((df['super_built_up_area'].isnull()) & (df['built_up_area'].isnull()) & (df['carpet_area'].isnull()))][['price','property_type','area','areaWithType','super_built_up_area','built_up_area','carpet_area']]
#print(all_nan_df.head(5))
all_nan_index = df[((df['super_built_up_area'].isnull()) & (df['built_up_area'].isnull()) & (df['carpet_area'].isnull()))][['price','property_type','area','areaWithType','super_built_up_area','built_up_area','carpet_area']].index

all_nan_df['built_up_area'] = all_nan_df['areaWithType'].apply(extract_plot_area)

all_nan_df['built_up_area'] = all_nan_df.apply(convert_scale,axis=1)
df.update(all_nan_df)
#print(df.isnull().sum())

'''Feature Engineering: additionalRoom'''

#print(df['additionalRoom'].value_counts())

new_cols = ['servant room','study room','store room','pooja room','others']
for col in new_cols:
    df[col] = df['additionalRoom'].str.contains(col).astype(int)
#print(df[new_cols].sample(5))
    
'''Feature Engineering: agePossession'''

#print(df['agePossession'].value_counts())
#print(df['agePossession'].duplicated().sum())
#print(df['agePossession'].isnull().sum())

def categorize_age_possession(value):
    if pd.isna(value):
        return "Undefined"
    if "0 to 1 Year Old" in value or "Within 6 months" in value or "Within 3 months" in value:
        return "New Property"
    if "1 to 5 Year Old" in value:
        return "Relatively New"
    if "5 to 10 Year Old" in value:
        return "Moderately Old"
    if "10+ Year Old" in value:
        return "Old Property"
    if "Under Construction" in value or "By" in value:
        return "Under Construction"
    try:
        # For entries like 'May 2024'
        int(value.split(" ")[-1])
        return "Under Construction"
    except:
        return "Undefined"

df['agePossession'] = df['agePossession'].apply(categorize_age_possession)
#print(df['agePossession'].value_counts())


'''Feature Engineering: furnishDetails'''

#print(df['furnishDetails'].value_counts())
# Extract all unique furnishings from the furnishDetails column
all_furnishings = []
for detail in df['furnishDetails'].dropna():
    furnishings = detail.replace('[', '').replace(']', '').replace("'", "").split(', ')
    all_furnishings.extend(furnishings)
unique_furnishings = list(set(all_furnishings))

# Function to extract the count of a furnishing from the furnishDetails
def get_furnishing_count(details, furnishing):
    if isinstance(details, str):
        if f"No {furnishing}" in details:
            return 0
        pattern = re.compile(f"(\d+) {furnishing}")
        match = pattern.search(details)
        if match:
            return int(match.group(1))
        elif furnishing in details:
            return 1
    return 0

# Simplifying the furnishings list by removing "No" prefix and numbers
columns_to_include = [re.sub(r'No |\d+', '', furnishing).strip() for furnishing in unique_furnishings]
columns_to_include = list(set(columns_to_include))  # Get unique furnishings
columns_to_include = [furnishing for furnishing in columns_to_include if furnishing]  # Remove empty strings

# Creating new columns for each unique furnishing and populate with counts
for furnishing in columns_to_include:
    df[furnishing] = df['furnishDetails'].apply(lambda x: get_furnishing_count(x, furnishing))

# Creating the new dataframe with the required columns
furnishings_df = df[['furnishDetails'] + columns_to_include]

furnishings_df.drop(columns=['furnishDetails'],inplace=True)

scalar = StandardScaler()
scaled_data = scalar.fit_transform(furnishings_df)

wcss_reduced = []

for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(scaled_data)
    wcss_reduced.append(kmeans.inertia_)

furnishDetails_clusters_png_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'figures/furnishDetails_clusters.png')
plt.figure(figsize=(12, 8))
plt.plot(range(1,11), wcss_reduced, marker='o', linestyle='--')
plt.title('Elbow Method For Optimal Number of Clusters (Reduced Range)')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.grid(True)
plt.savefig(furnishDetails_clusters_png_path)


n_clusters = int(input('Give number of clusters: '))

kmeans = KMeans(n_clusters= n_clusters, random_state=42)
kmeans.fit(scaled_data)
cluster_assignments = kmeans.predict(scaled_data)

df = df.iloc[:,:-18]
df['furnishing_type'] = cluster_assignments

#print(df[['furnishDetails', 'furnishing_type']].sample(5))

'''Feature Engineering: features'''

#print(df['features'].sample(5))
#print(df['features'].isnull().sum()) ''' -> 631'''

file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/real_estate_data.csv')
app_df = pd.read_csv(file_path)
app_df['PropertyName'] = app_df['PropertyName'].str.lower()
temp_df = df[df['features'].isnull()]

x = temp_df.merge(app_df, left_on='society', right_on='PropertyName', how='left')['TopFacilities']
df.loc[temp_df.index, 'features'] = x.values
#print(df['features'].isnull().sum()) '''-> 478'''

import luxury_weights_json

file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'clean_data/luxury_weights.json')

with open(file_path, 'r') as file:
    luxury_weights = json.load(file)
    
#print(luxury_weights)
#print(type(eval(df['features'][0])))

'''def test(x, weights):
    score = 0
    x = x.strip(']').strip('[')
    for element in weights.keys():
        if re.search(str(element), x):
            score += weights[element]
    print(x)
    print({key: value for key, value in weights.items() if re.search(str(key), x)})
    print(score)
    sys.exit()
'''
def feature_score(row, weights):
    score = 0
    row = row.strip(']').strip('[')
    for element in weights.keys():
        if re.search(str(element), row):
            score += weights[element]
    
    return score

df['luxury_score'] = df['features'].apply(lambda x: feature_score(str(x), luxury_weights))

#print(df[['features','luxury_score']].sample(5))

# cols to drop -> nearbyLocations,furnishDetails, features,features_list, additionalRoom
df.drop(columns=['nearbyLocations','furnishDetails','features','additionalRoom'],inplace=True)


file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'clean_data/gurgaon_properties.csv')
df.to_csv(file_path, index=False)