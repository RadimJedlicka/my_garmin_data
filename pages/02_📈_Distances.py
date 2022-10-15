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
df['Month'] = pd.to_datetime(df['Date']).dt.month


list_of_years = df['Year'].drop_duplicates().values.tolist()
years_string = [str(year) for year in list_of_years]
years_string


df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
df['Month_num'] = pd.to_datetime(df['Date']).dt.month

selection = df[['Year', 'Month', 'Month_num', 'Distance']]
selection.set_index('Year', inplace=True)
# selection

selection_grouped = selection.groupby(
    ['Month_num', 'Month','Year']
).agg({'Distance': 'sum'})

selection_grouped.reset_index(inplace=True)
# selection_grouped

year2022 = selection_grouped['Year'] == 2022
year2021 = selection_grouped['Year'] == 2021
year2020 = selection_grouped['Year'] == 2020
year2019 = selection_grouped['Year'] == 2019

df_super = selection_grouped[
    year2022 | 
    year2021 | 
    year2020 | 
    year2019
]
df_super

df_final = selection.groupby(
    [
        'Year', 
        'Month', 
        'Month_num'
    ]
).agg({'Distance': 'sum'})

df_final.sort_values(['Month_num', 'Year'], inplace=True)

df_final.to_csv('df_final.csv')
df_final2 = pd.read_csv('df_final.csv')
df_final2

country = st.sidebar.multiselect(
    label='Select year',
    options=years_string,
    default=['2022'])

# brush = alt.selection(type='single', encodings=['x'])
selection = alt.selection_multi(fields=country, bind='legend')

base_chart = alt.Chart(df_final2).mark_bar().encode(
        x=alt.X('Month_num:N'),
        y=alt.Y('sum(Distance):Q', scale=alt.Scale(zero=False)),
        color='Year:N',
        # column='Year:O'
        # column = alt.Column('Month:N', spacing = 1)
        # opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
    # ).add_selection(
    #     selection
    ).properties(
    width=900,
    height=600
    )
# alt.layer(base_chart).facet(
#     column='Year'
# )
st.altair_chart(base_chart, use_container_width=False)


base_chart = alt.Chart(df_super).mark_bar().encode(
        x=alt.X('Month:N', sort = 'y'),
        y=alt.Y('sum(Distance):Q', scale=alt.Scale(zero=False)),
        color='Year:N',
        column='Year:O'
        # column = alt.Column('Month:N', spacing = 1)
        # opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
    # ).add_selection(
    #     selection
    )
# alt.layer(base_chart).facet(
#     column='Year'
# )
st.altair_chart(base_chart, use_container_width=False)
