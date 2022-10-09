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


df = pd.read_csv('cycling_activities.csv')

# show all the columns of df
pd.set_option("display.max_columns", None)

st.title('Welcome to my Garmin Data Vizualization app')



# converting columns into useful formats
df['Date'] = pd.to_datetime(df['Date']).dt.date
df['Time'] = pd.to_timedelta(df['Time'])
df['Moving_Time'] = pd.to_timedelta(df['Moving_Time'])
df['Elapsed_Time'] = pd.to_timedelta(df['Elapsed_Time'])
df['Year'] = pd.to_datetime(df['Date']).dt.year



total_distance = int(df['Distance'].sum())
total_ascent = int(df['Total_Ascent'].sum())
total_time = df['Moving_Time'].sum()
days = str(total_time)[:2]
hours = str(total_time)[8:10]
total_hours = int(days)*24 + int(hours)
longest_ride = df['Distance'].max()


col1, col2, col3, col4 = st.columns(4)
col1.metric('Total distance ridden', str(total_distance) +' km')
col2.metric('Total meters climbed', str(total_ascent) +' m')
col3.metric('Total time', str(total_hours) + ' hours')
col4.metric('Longest ride', str(longest_ride) + ' km')


# Goal for the current year
df2022 = df[df['Year'] == 2022]

total_km_year = int(df2022['Distance'].sum())

goal = 4000
current = total_km_year
percent = int(current*100/goal)

fig, ax = plt.subplots(figsize=(6, 6))
data = [100-percent, percent]
wedgeprops = {'width':0.4, 'edgecolor':'black', 'lw':1}
patches, _ = ax.pie(data, wedgeprops=wedgeprops, startangle=90, colors=['#8b8f8f', '#3662c2'])
patches[1].set_zorder(1)
patches[0].set_edgecolor('#8b8f8f')
# plt.title('Goal for 2022', fontsize=24, loc='center', font='Sans Serif')
plt.text(0, 0, f"{data[1]}%", ha='center', va='center', fontsize=36, font='Sans Serif')
# plt.show()

col1, col2 = st.columns([4, 2])

col1.image('title-photo.jpg', width=300, use_column_width=True, output_format="auto")
col2.markdown('''<h1 style='text-align: center; color: #3662c2'>
                Road to 4K in 2022</h1>
                ''', unsafe_allow_html=True
                )
col2.pyplot(fig)
col2.markdown(f'''<h4 style='text-align: center; color: #3662c2'>
                {current} km ridden - {goal-current} km still remains</h4>
                ''', unsafe_allow_html=True
                )




