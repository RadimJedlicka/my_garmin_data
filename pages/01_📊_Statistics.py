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

# show all the columns of df
pd.set_option("display.max_columns", None)

# converting columns into useful formats
df['Date'] = pd.to_datetime(df['Date']).dt.date
df['Time'] = pd.to_timedelta(df['Time'])
df['Moving_Time'] = pd.to_timedelta(df['Moving_Time'])
df['Elapsed_Time'] = pd.to_timedelta(df['Elapsed_Time'])
df['Year'] = pd.to_datetime(df['Date']).dt.year

# longest rides
longest_rides = df[['Date', 'Title', 'Distance']
                  ].sort_values('Distance', ascending=False
                  ).reset_index().head(10).round(2)
longest_rides.index += 1

# Kilometers ridden per year
df['Year'] = pd.to_datetime(df['Date']).dt.year
km_per_year = df[
    ['Year', 'Distance']
    ].groupby(df['Year']
    ).agg({'Year': 'mean', 'Distance': 'sum'}
    )
km_per_year.iloc[::-1].drop('Year', axis=1)
kmpr = alt.Chart(km_per_year).mark_bar(color='darkblue').encode(
    x='Year:O',
    y='Distance:Q',
    tooltip=['Distance', 'Year']
).configure_axis(
    grid=False
).properties(
    width=600,
    height=450
).interactive()

# Bike usage
bike_usage = df[
    ['Bike', 'Distance']].assign(amount_of_rides=1
    ).groupby(df['Bike']
    ).agg({'amount_of_rides': 'sum', 'Distance': 'sum'})

bike_usage.to_csv('bike_usage.csv')
usage = pd.read_csv('bike_usage.csv')

usage = alt.Chart(usage).mark_bar(color='darkgreen').encode(
    alt.X('Bike:N', sort='y'),
    alt.Y('Distance:Q'),
    tooltip=['Distance', 'Bike:O']
).configure_axis(
    grid=False
).properties(
    width=600,
    height=500
).interactive()

# Activity types
activity_type = df[
    ['Activity_Type', 'Distance']].assign(amount_of_rides=1
    ).groupby(df['Activity_Type']
    ).agg({'amount_of_rides': 'sum', 'Distance': 'sum'})

activity_type.to_csv('activity_types.csv')
activities = pd.read_csv('activity_types.csv')

fig = alt.Chart(activities).mark_bar(color='darkred').encode(
    alt.X('Activity_Type:N', axis=alt.Axis(title='Type of activities'), sort='-y'),
    alt.Y('Distance:Q'),
    tooltip=['Distance', 'Activity_Type']
).configure_axis(
    grid=False
).properties(
    width=600,
    height=520
).interactive()

# ######################## ###################################################
# STREAMLIT PAGE STRUCTURE 
# ######################## ###################################################
st.title('My garmin data')

col1, col2 = st.columns(2)


col1.header('TOP 10 of my longest rides')
col1.dataframe(longest_rides)

col2.header('Kilometers per year')
col2.altair_chart(kmpr, use_container_width=False)


col1, col2 = st.columns(2)

col1.header('How much I use each bike')
col1.altair_chart(usage, use_container_width=False)

col2.header('Types of activities')
col2.altair_chart(fig, use_container_width=False)


