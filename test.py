import pickle
import os, sys
import pandas as pd

path = '/home/himanshu/Projects/ML_Proj/PropertyApp/final_model_data'

df = pd.read_csv(path + '/latlong.csv')

l1 = set(df.sector.unique())

with open(path + '/latlong.pkl', 'wb') as file:
    pickle.dump(df, file)
    
