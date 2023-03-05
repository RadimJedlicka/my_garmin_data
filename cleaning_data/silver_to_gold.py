import pandas as pd
import numpy as np

# show all the columns of df
pd.set_option("display.max_columns", None)

df = pd.read_csv('Activities_silver.csv')

# Cleaning table from unsued columns
df = df.drop(columns=[
    'Favorite',
    'Avg Stride Length', 
    'Avg Vertical Ratio',
    'Avg Vertical Oscillation', 
    'Avg Ground Contact Time',
    'Grit', 
    'Flow',
    'Avg. Swolf',
    'Avg Stroke Rate', 
    'Total Reps', 
    'Dive Time',
    'Surface Interval', 
    'Decompression', 
    'Best Lap Time', 
    'Number of Laps',
    'Max Temp',
    ]
)

# replacing bulshit values to zeros
df = df.replace(['--'],'0')
df['Total Strokes'] = df['Total Strokes'].fillna(0)
df.head()

# converting columns into useful formats
df['Date'] = pd.to_datetime(df['Date'])
df['Distance'] = df['Distance'].str.replace(',', '.', regex=True).astype('float').round(2)
df['Calories'] = df['Calories'].str.replace('.', '', regex=True).astype('float')
df['Avg HR'] = df['Avg HR'].astype('int')
df['Max HR'] = df['Max HR'].astype('int')
df['Aerobic TE'] = df['Aerobic TE'].str.replace(',', '.').astype('float')
df['Avg Speed'] = df['Avg Speed'].str.replace(',', '.').astype('float')
df['Max Speed'] = df['Max Speed'].str.replace(',', '.').astype('float')
df['Total Ascent'] = df['Total Ascent'].str.replace('.', '', regex=True).astype('int')
df['Total Descent'] = df['Total Descent'].str.replace('.', '', regex=True).astype('int')
df['Avg Bike Cadence'] = df['Avg Bike Cadence'].astype('int')
df['Max Bike Cadence'] = df['Max Bike Cadence'].astype('int')
df['Normalized Power® (NP®)'] = df['Normalized Power® (NP®)'].astype('int')
df['Training Stress Score®'] = df['Training Stress Score®'].str.replace(',', '.').astype('float')
df['Max Avg Power (20 min)'] = df['Max Avg Power (20 min)'].str.replace(',', '.').astype('int')
df['Avg Power'] = df['Avg Power'].str.replace(',', '.').astype('int')
df['Max Power'] = df['Max Power'].str.replace(',', '.').astype('int')
df['Total Strokes'] = df['Total Strokes'].astype('int')
df['Min Temp'] = df['Min Temp'].str.replace(',', '.').astype('float')
df['Min Elevation'] = df['Min Elevation'].str.replace('.', '', regex=True).astype('int')
df['Max Elevation'] = df['Max Elevation'].str.replace('.', '', regex=True).astype('int')
df['Time'] = pd.to_timedelta(df['Time'])
df['Moving Time'] = pd.to_timedelta(df['Moving Time'])
df['Elapsed Time'] = pd.to_timedelta(df['Elapsed Time'])

# rename columns
df.rename(
    columns={
        'Activity Type': 'Activity_Type',
        'Avg HR': 'Avg_HR',
        'Max HR': 'Max_HR',
        'Aerobic TE': 'Aerobic_TE',
        'Avg Speed': 'Avg_Speed',
        'Max Speed': 'Max_Speed',
        'Total Ascent': 'Total_Ascent',
        'Total Descent': 'Total_Descent',
        'Avg Bike Cadence': 'Avg_Cadence',
        'Max Bike Cadence': 'Max_Cadence',
        'Normalized Power® (NP®)': 'Normalized_Power',
        'Training Stress Score®': 'Training_Stress_Score',
        'Max Avg Power (20 min)': 'Max_Avg_Power(20min)',
        'Avg Power': 'Avg_Power',
        'Max Power': 'Max_Power',
        'Total Strokes': 'Total_Strokes',
        'Min Temp': 'Min_Temp',
        'Moving Time': 'Moving_Time',
        'Elapsed Time': 'Elapsed_Time',
        'Min Elevation': 'Min_Elevation',
        'Max Elevation': 'Max_Elevation'
    }, inplace=True
)

# create new column with name of bike used
# create a list of our conditions
conditions = [
    (df['Activity_Type'] == 'Road Cycling'),
    (df['Activity_Type'] == 'Gravel/Unpaved Cycling'),
    (df['Activity_Type'] == 'Mountain Biking'),
    (df['Activity_Type'] == 'Indoor Cycling'),
    (df['Activity_Type'] == 'Virtual Cycling'),
    (df['Activity_Type'] == 'eBiking'),
    (df['Activity_Type'] == 'Cycling')
    
]
# create a list of the values we want to assign for each condition
values = ['Roubaix', 'Bergamont', 'Rockhopper', 'Tacx', 'Tacx', 'Elops','unknown']
# create a new column and use np.select to assign values to it using our lists as arguments
df['Bike'] = np.select(conditions, values)

# shorten name of Gravel Cycling activity
df = df.replace('Gravel/Unpaved Cycling', 'Gravel Cycling')

df.to_csv('Activities_golden.csv')

print('Data transformation done. Enjoy :-)')