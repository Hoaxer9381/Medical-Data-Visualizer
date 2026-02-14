import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import the data set 
df = pd.read_csv("medical_examination.csv") 


# BMI Formula BMI = weight / (hight_in_meaters(square))
#Converting hight from CM to Meters hight_in_meters = hight / 100
#If BMI is graterthan 25 then it overweight as 1, Else overweight is 0
#overweight is an main cause of heart disease
df['BMI'] = df['weight'] / ((df['height'] / 100) ** 2)  
df['overweight'] = (df['BMI'] > 25).astype(int)

# Normalizing the Cholesteral and Glucouse 
# where scaling 1 --> 0 (healthy) and 2&3 --> 1 (unhealthy)
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)

def draw_cat_plot():
    # counts of healthy and unhealthy pepole 
    # pd.melt() it converts wide format to long format
    df_cat = pd.melt(
        df,
        id_vars=['cardio'],
        value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
    )

 # Groupby and counts 
 # counting the appearence of 'groupby values' by combinations
    df_cat = (
        df_cat
        .groupby(['cardio', 'variable', 'value'])
        .size()
        .reset_index(name='total')
    )

# Creating the categorical plot 
# comparing healthy vs unhealthy
    fig = sns.catplot(
        data=df_cat,
        x='variable',
        y='total',
        hue='value',
        col='cardio',
        kind='bar'
    ).fig
    return fig


def draw_heat_map():
    # Cleaning the Data
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    #Correlation matrix
    # correlation between all numeric columns
    corr = df_heat.corr()

    #Generate mask
    mask = np.triu(np.ones_like(corr, dtype=bool))

    #matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 10))

    #Ploting heatmap
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".1f",
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.5},
        ax=ax
    )

    return fig