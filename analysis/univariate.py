import numpy as np
import pandas as pd
import os, json, sys
import matplotlib.pyplot as plt
import seaborn as sns


file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'clean_data/gurgaon_properties.csv')

df = pd.read_csv(file_path)
df.drop_duplicates(inplace=True)
#print(df.sample(5))

'''property_type'''
#print(df['property_type'].value_counts())
#print(df['property_type'].isnull().sum())
temp_df = df['property_type'].value_counts().to_frame()
plt.bar(temp_df.index.values, height=temp_df['count'])
img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'figures/property_type_univariate.png')
plt.savefig(img_path)
plt.close()

'''society'''
#print(df['society'].value_counts().shape) #(674,) highest -> 'independent' - 481, second high -> 75
#print(df['society'].isnull().sum()) #1
temp_df = df[df['society'] != 'independent']['society'].value_counts().head(10).to_frame()
plt.bar(range(len(temp_df.index.values)), height=temp_df['count'])
plt.xticks(range(len(temp_df.index.values)), temp_df.index.values, rotation = 90)
plt.title('Top 10 society excluding independent category')
img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'figures/society_univariate.png')
plt.tight_layout()
plt.savefig(img_path)
plt.close()

'''sector'''
#print(df['sector'].value_counts()) #(115,) 
#print(df['sector'].isnull().sum())
temp_df = df['sector'].value_counts().head(10).to_frame()
plt.bar(range(len(temp_df.index.values)), height=temp_df['count'])
plt.xticks(range(len(temp_df.index.values)), temp_df.index.values, rotation = 90)
plt.title('Top 10 sectors')
img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'figures/sector_univariate.png')
plt.tight_layout()
plt.savefig(img_path)
plt.close()

'''price -> output column'''
#print(df['price'].describe())
'''
count    3661.000000
mean        2.533300
std         2.980298
min         0.070000
25%         0.950000
50%         1.520000
75%         2.750000
max        31.500000
'''
#print(df['price'].isnull().sum()) #0
kurtosis = df['price'].kurt()
skewness = df['price'].skew()
#print(f'Kurtosis = {kurtosis} \nSkewness = {skewness}')
quantiles = df['price'].quantile([0.01, 0.05, 0.95, 0.99])
#print(f'Quantiles = \n{quantiles}')
q1 = df['price'].quantile(0.25)
q3 = df['price'].quantile(0.75)
#print(f'Q1 = {q1}\nQ3 = {q3}')
IQR = q3 - q1
lower_bound = q1 - 1.5 * IQR
upper_bound = q3 + 1.5 * IQR
#print(f'IQR = {IQR}\nUpper Bound = {upper_bound}\nLower Bound = {lower_bound}')
#outliers = df[(df['price'] > upper_bound) | (df['price'] < lower_bound)]['price']
#print(outliers.describe())

'''
Kurtosis = 14.937920682529791 
Skewness = 3.279691369881952
Quantiles = 
    0.01     0.25
    0.05     0.37
    0.95     8.50
    0.99    15.26

Q1 = 0.95
Q3 = 2.75
IQR = 1.8
Upper Bound = 5.45
Lower Bound = -1.7500000000000002
Outliers = 
    count    425.000000
    mean       9.235624
    std        4.065259
    min        5.460000
    25%        6.460000
    50%        8.000000
    75%       10.750000
    max       31.500000
'''
sns.histplot(df['price'], kde=True, bins=50)
img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'figures/price_kde_original.png')
plt.tight_layout()
plt.title('Original')
plt.savefig(img_path)
plt.close()
sns.histplot(np.log1p(df['price']), kde=True, bins=50)
img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'figures/price_kde_logtransformed.png')
plt.tight_layout()
plt.title('Log Transformed')
plt.savefig(img_path)
plt.close()
sns.boxplot(x = df['price'])
plt.grid()
img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'figures/price_boxplot_original.png')
plt.tight_layout()
plt.title('Original')
plt.savefig(img_path)
plt.close()
sns.boxplot(x = np.log1p(df['price']))
plt.grid()
img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'figures/price_boxplot_logtransformed.png')
plt.tight_layout()
plt.title('Log Transformed')
plt.savefig(img_path)
plt.close()

'''price_per_sqft'''
#print(df['price_per_sqft'].value_counts())
#print(df['price_per_sqft'].isnull().sum())
#print(df['price_per_sqft'].describe())
'''
count      3661.000000
mean      13891.070473
std       23207.097578
min           4.000000
25%        6818.000000
50%        9020.000000
75%       13878.000000
max      600000.000000
'''

#print(df['price_per_sqft'].isnull().sum()) #0
kurtosis = df['price_per_sqft'].kurt()
skewness = df['price_per_sqft'].skew()
#print(f'Kurtosis = {kurtosis} \nSkewness = {skewness}')
quantiles = df['price_per_sqft'].quantile([0.01, 0.05, 0.95, 0.99])
#print(f'Quantiles = \n{quantiles}')
q1 = df['price_per_sqft'].quantile(0.25)
q3 = df['price_per_sqft'].quantile(0.75)
#print(f'Q1 = {q1}\nQ3 = {q3}')
IQR = q3 - q1
lower_bound = q1 - 1.5 * IQR
upper_bound = q3 + 1.5 * IQR
#print(f'IQR = {IQR}\nUpper Bound = {upper_bound}\nLower Bound = {lower_bound}')
outliers = df[(df['price_per_sqft'] > upper_bound) | (df['price_per_sqft'] < lower_bound)]['price_per_sqft']
#print(outliers.describe())

'''
Kurtosis = 186.97639714598265 
Skewness = 11.438656008287285
Quantiles = 
    0.01     3299.4
    0.05     4716.0
    0.95    33333.0
    0.99    85026.8
Name: price_per_sqft, dtype: float64
Q1 = 6818.0
Q3 = 13878.0
IQR = 7060.0
Upper Bound = 24468.0
Lower Bound = -3772.0
Outliers = 
    count       354.000000
    mean      52592.612994
    std       61150.458507
    min       24489.000000
    25%       28208.250000
    50%       33368.500000
    75%       41982.250000
    max      600000.000000
'''
sns.histplot(df['price_per_sqft'], kde=True, bins=50)
img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'figures/price_per_sqft_kde_original.png')
plt.tight_layout()
plt.title('Original')
plt.savefig(img_path)
plt.close()
sns.histplot(np.log1p(df['price_per_sqft']), kde=True, bins=50)
img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'figures/price_per_sqft_kde_logtransformed.png')
plt.tight_layout()
plt.title('Log Transformed')
plt.savefig(img_path)
plt.close()
sns.boxplot(x = df['price_per_sqft'])
plt.grid()
img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'figures/price_per_sqft_boxplot_original.png')
plt.tight_layout()
plt.title('Original')
plt.savefig(img_path)
plt.close()
sns.boxplot(x = np.log1p(df['price_per_sqft']))
plt.grid()
img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'figures/price_per_sqft_boxplot_logtransformed.png')
plt.tight_layout()
plt.title('Log Transformed')
plt.savefig(img_path)
plt.close()


'''bedroom / bathroom / balcony'''

for column in ['bedroom','bathroom','balcony']:
    #print(df[column].value_counts())
    #print(f'Null values in {column} = ', df[column].isnull().sum())
    temp_df = df[column].value_counts().head(10).to_frame()
    plt.pie(temp_df['count'], labels=temp_df.index.values, autopct='%0.2f%%', normalize=True)
    plt.title(f'{column}')
    img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'figures/{column}_univariate.png')
    plt.tight_layout()
    plt.savefig(img_path)
    plt.close()
'''
bedroom
3     1496
2      941
4      659
5      200
1      124
6       73
9       40
8       30
7       28
12      27
10      20
16      11
13       4
19       2
18       2
21       1
11       1
20       1
14       1
Name: count, dtype: int64
Null values in bedroom =  0
bedroom
3     1496
2      941
4      659
5      200
1      124
6       73
9       40
8       30
7       28
12      27
10      20
16      11
13       4
19       2
18       2
21       1
11       1
20       1
14       1
Name: count, dtype: int64
Null values in bathroom =  0
bedroom
3     1496
2      941
4      659
5      200
1      124
6       73
9       40
8       30
7       28
12      27
10      20
16      11
13       4
19       2
18       2
21       1
11       1
20       1
14       1
Name: count, dtype: int64
Null values in balcony =  0
'''

'''floorNum'''
#print(df['floorNum'].value_counts())
#print(df['floorNum'].isnull().sum()) #19
#print(df['floorNum'].describe())
'''
count    3641.000000
mean        6.815161
std         6.019533
min         0.000000
25%         2.000000
50%         5.000000
75%        10.000000
max        51.000000
'''
temp_df = df['floorNum'].value_counts().to_frame()
plt.bar(range(len(temp_df.index.values)), height=temp_df['count'])
plt.xticks(range(len(temp_df.index.values)), temp_df.index.values, rotation = 90)
plt.title('floorNum')
img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'figures/floorNum_univariate.png')
plt.tight_layout()
plt.savefig(img_path)
plt.close()
sns.boxplot(x = df['floorNum'])
plt.grid()
img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'figures/floorNum_boxplot.png')
plt.tight_layout()
plt.title('floorNum')
plt.savefig(img_path)
plt.close()


['property_type', 'society', 'sector', 'price', 'price_per_sqft', 'area',
       'areaWithType', 'bedroom', 'bathroom', 'balcony', 'floorNum', 'facing',
       'agePossession', 'super_built_up_area', 'built_up_area', 'carpet_area',
       'servant room', 'study room', 'store room', 'pooja room', 'others',
       'furnishing_type', 'luxury_score']


'''facing / agePossession'''

for column in ['facing','agePossession']:
    #print(df[column].value_counts())
    #print(f'Null values in {column} = ', df[column].isnull().sum())
    temp_df = df[column].value_counts().to_frame()
    plt.pie(temp_df['count'], labels=temp_df.index.values, autopct='%0.2f%%', normalize=True)
    plt.title(f'{column}')
    img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'figures/{column}_univariate.png')
    plt.tight_layout()
    plt.savefig(img_path)
    plt.close()
    
'''super_built_up_area / built_up_area / carpet_area'''

for column in ['super_built_up_area', 'built_up_area', 'carpet_area']:
    #print(df[column].value_counts())
    #print(df[column].isnull().sum())
    #print(df[column].describe())
    sns.histplot(df[column], kde=True, bins=50)
    img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'figures/{column}_univariate.png')
    plt.tight_layout()
    plt.title(f'{column}')
    plt.savefig(img_path)
    plt.close()
    sns.boxplot(x = df[column])
    plt.grid()
    img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'figures/{column}_boxplot.png')
    plt.tight_layout()
    plt.title(f'{column}')
    plt.savefig(img_path)
    plt.close()
    
'''
super_built_up_area
1950.0    37
1650.0    37
2000.0    25
1578.0    25
1640.0    22
          ..
1495.0     1
5514.0     1
2193.0     1
1475.0     1
2520.0     1
Name: count, Length: 593, dtype: int64
1785
count     1875.000000
mean      1925.237627
std        764.172177
min         89.000000
25%       1479.500000
50%       1828.000000
75%       2215.000000
max      10000.000000
Name: super_built_up_area, dtype: float64
built_up_area
1800.0    41
3240.0    37
1900.0    34
1350.0    33
2700.0    32
          ..
5490.0     1
8067.8     1
1785.0     1
1145.0     1
90.0       1
Name: count, Length: 641, dtype: int64
1986
count      1674.000000
mean       2386.198942
std       18026.926801
min           2.000000
25%        1110.500000
50%        1650.000000
75%        2400.000000
max      737147.000000
Name: built_up_area, dtype: float64
carpet_area
1400.000000    42
1800.000000    35
1600.000000    35
1200.000000    31
1500.000000    29
               ..
15.000000       1
1535.000000     1
573.500592      1
1220.000000     1
683.830000      1
Name: count, Length: 731, dtype: int64
1791
count      1869.000000
mean       2532.585274
std       22817.977990
min          15.000000
25%         845.000000
50%        1300.000000
75%        1790.000000
max      607936.000000
Name: carpet_area, dtype: float64
'''

plt.figure(figsize=(20, 12))
for idx, room in enumerate(['servant room', 'study room', 'store room', 'pooja room', 'others'], 1):
    temp_df = df[room].value_counts().to_frame()
    ax = plt.subplot(2, 3, idx)
    ax.pie(temp_df['count'], labels=temp_df.index.values, autopct='%1.1f%%', normalize=True)
    plt.title(f'{room}')
plt.tight_layout()
img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'figures/additionalrooms_pie.png')
plt.savefig(img_path)
plt.close()

'''furnishing_type'''

#print(df['furnishing_type'].value_counts())
#print(df['furnishing_type'].isnull().sum())
temp_df = df['furnishing_type'].value_counts().to_frame()
plt.pie(temp_df['count'], labels=temp_df.index.values, autopct='%0.2f%%', normalize=True)
plt.title('furnishing_type')
img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'figures/furnishing_type_univariate.png')
plt.tight_layout()
plt.savefig(img_path)
plt.close()

'''
furnishing_type
0    2426
2    1033
1     201
Name: count, dtype: int64
'''

'''luxury_score'''
#print(df['luxury_score'].describe())
#print(df['luxury_score'].isnull().sum()) #0
sns.histplot(df['luxury_score'], kde=True, bins=50)
img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'figures/luxury_score_univariate.png')
plt.tight_layout()
plt.title('luxury_score')
plt.savefig(img_path)
plt.close()
sns.boxplot(x = df['luxury_score'])
plt.grid()
img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'figures/luxury_score_boxplot.png')
plt.tight_layout()
plt.title('luxury_score')
plt.savefig(img_path)
plt.close()

'''
count    3660.000000
mean       78.654918
std        58.975704
min         0.000000
25%        36.000000
50%        64.000000
75%       120.000000
max       192.000000
Name: luxury_score, dtype: float64

'''