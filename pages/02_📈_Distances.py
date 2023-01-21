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
df['Month'] = pd.to_datetime(df['Date']).dt.month


list_of_years = df['Year'].drop_duplicates().values.tolist()
years_string = [str(year) for year in list_of_years]


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

# ######################## ###################################################
# STREAMLIT PAGE STRUCTURE 
# ######################## ###################################################
st.title('Distances')

select_year = st.multiselect(
    label='Select year',
    options=years_string,
    default='2023')

string_query = ''
for year in select_year:
    base = 'Year == '
    if not string_query:
        string_query = base + year + ' | '
    if string_query:
        string_query += base + year + ' | '


df_month_stack = selection_grouped.query(string_query[:-2])
# df_month_stack

select = alt.selection_multi(fields=['Year'], bind='legend')

base_chart = alt.Chart(
    df_month_stack
    ).mark_bar(
    ).encode(
        x=alt.X(
            'Month_num:N',
            axis=alt.Axis(
                title='Months by their order (1: January - 12: December)')),
        y=alt.Y(
            'sum(Distance):Q',
            axis=alt.Axis(
                title='Cummulated sum of kilometers ridden each month')),
        
        tooltip=['Distance', 'Month', 'Year'],
        color='Year:N',
        order=alt.Order('Year', sort='ascending')
    ).properties(
        width=900,
        height=600
    ).add_selection(
        select
    ).interactive()
# alt.layer(base_chart).facet(
#     column='Year'
# )
st.altair_chart(base_chart, use_container_width=False)








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
# df_final2

base_chart = alt.Chart(df_month_stack).mark_bar().encode(
        x=alt.X('Month_num:N', sort = 'y'),
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


