import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Garmin Data Visualization app", 
    page_icon=":bike:", 
    layout="wide", 
    initial_sidebar_state="auto",
    )

# ###################################### #####################################
# DATA PROCESSING, DATAFRAMES, VARIABLES 
# ###################################### #####################################
df = pd.read_csv('cycling_activities.csv')

# converting columns into useful formats
df['Date'] = pd.to_datetime(df['Date']).dt.date
df['Time'] = pd.to_timedelta(df['Time'])
df['Moving_Time'] = pd.to_timedelta(df['Moving_Time'])
df['Elapsed_Time'] = pd.to_timedelta(df['Elapsed_Time'])
df['Year'] = pd.to_datetime(df['Date']).dt.year

# ######################## ###################################################
# STREAMLIT PAGE STRUCTURE 
# ######################## ###################################################
st.markdown('''<h1 style='text-align: center; color: #3662c2'>
                Welcome to my Garmin Data Vizualization app</h1>
                ''', unsafe_allow_html=True
                )

total_distance = int(df['Distance'].sum())
prg_bz = int(total_distance/666)
total_ascent = int(df['Total_Ascent'].sum())
everest = int(total_ascent/8848)
total_time = df['Moving_Time'].sum()
days = str(total_time)[:2]
hours = str(total_time)[8:10]
total_hours = int(days)*24 + int(hours)
total_calories = int(df['Calories'].sum())
burger_count = int(total_calories/300)

col1, col2, col3, col4 = st.columns(4)
col1.metric(
    'Total distance ridden', 
    str(total_distance) +' km', 
    str(prg_bz) + ' x PRG-BZ distance',
    delta_color="inverse",
)
col2.metric(
    'Total meters climbed', 
    str(total_ascent) +' m',
    str(everest) + ' x Mount Everest',
)
col3.metric(
    'Total time', 
    str(total_hours) + ' hours',
    str(days) + ' days in the saddle'
)
col4.metric(
    'Longest ride', 
    str(total_calories) + ' kcal',
    'like ' + str(burger_count) + ' burgers eaten',
    delta_color="inverse"
)


# Goal for the current year
df2022 = df[df['Year'] == 2022]

total_km_year = int(df2022['Distance'].sum())

goal = 4000
current = total_km_year
percent = int(current*100/goal)

fig, ax = plt.subplots(figsize=(6, 6))
data = [100-percent, percent]
wedgeprops = {'width':0.4, 'edgecolor':'black', 'lw':1}
patches, _ = ax.pie(
    data, 
    wedgeprops=wedgeprops, 
    startangle=90, 
    colors=['#8b8f8f', '#3662c2'])
patches[1].set_zorder(1)
patches[0].set_edgecolor('#8b8f8f')
plt.text(
    0, 
    0, 
    f"{data[1]}%", 
    ha='center', 
    va='center', 
    fontsize=36, 
    font='Sans Serif')
# plt.show()

col1, col2 = st.columns([4, 2])

col1.image('title-photo.jpg', width=300, use_column_width=True)
col2.markdown('''<h2 style='text-align: center; color: #3662c2'>
                Road to 4K in 2022</h2>
                ''', unsafe_allow_html=True
                )
col2.pyplot(fig)
col2.markdown(f'''<h4 style='text-align: center; color: #3662c2'>
                {current} km ridden - {goal-current} km still remains</h4>
                ''', unsafe_allow_html=True
                )
