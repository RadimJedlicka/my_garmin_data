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

st.title('My garmin data')


# longest rides
longest_rides = df[['Date', 'Title', 'Distance']
                  ].sort_values('Distance', ascending=False).reset_index().head(10).round(2)

longest_rides.index += 1

longest_rides


df['Date_dt'] = pd.to_datetime(df['Date']).dt.year
km_per_year = df[
    ['Date_dt', 'Distance']
    ].groupby(df['Date_dt']
    ).agg({'Date_dt': 'mean', 'Distance': 'sum'})

st.header('Kilometers per year')

kmpr = alt.Chart(km_per_year).mark_bar().encode(
    x='Date_dt:O',
    y='Distance:Q',
    tooltip=['Distance', 'Date_dt']
).interactive()

st.altair_chart(kmpr, use_container_width=True)

# longest rides
longest_rides = df[['Date', 'Title', 'Distance']
                  ].sort_values('Distance', ascending=False).reset_index().head(10).round(2)

longest_rides.index += 1

longest_rides


df['Date_dt'] = pd.to_datetime(df['Date']).dt.year
km_per_year = df[
    ['Date_dt', 'Distance']
    ].groupby(df['Date_dt']
    ).agg({'Date_dt': 'mean', 'Distance': 'sum'})

st.header('Kilometers per year')

kmpr = alt.Chart(km_per_year).mark_bar().encode(
    x='Date_dt:O',
    y='Distance:Q',
    tooltip=['Distance', 'Date_dt']
).interactive()

st.altair_chart(kmpr, use_container_width=True)