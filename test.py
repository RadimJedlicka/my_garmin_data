import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import pymysql

import plotly.graph_objects as go
import plotly.express as px
import altair as alt



# ##################
# Funkce
# ##################
def dict_to_sql(dict):
  base = 'SELECT '

  # dimensions
  for column in dict['columns']:
    base = base + column + ','

  # measures
  base = base + dict['measures']

  # from
  base = base + ' FROM ' + dict['table']

  # where
  base = base + ' WHERE 1=1'
  for filter in dict['filters']:
    base = base + ' AND ' + filter

  # group by
  base = base + ' GROUP BY '
  for column in dict['columns']:
    base = base + column + ','

  return base[:-1]


def to_filter(filter_name, filter_values):
    base = filter_name + ' IN ('

    for values in filter_values:
        base = base + "'" + values + "',"
    base = base[:-1] + ")"
    return base

# ##################
# Data
# ##################

engine = create_engine("mysql+pymysql://data-student:u9AB6hWGsNkNcRDm@data.engeto.com:3306/data_academy_04_2022")

# ##################
# VIZUALICE
# ##################
st.set_page_config(layout="wide")
st.title('Moje prvni appka')

page = st.sidebar.radio('Select page', ['Mapa','Thomson','Covid'])

if page == 'Mapa':
    st.header('Mapa pouzivani sdilenych kol v Edinburgu')

    col1, col2 = st.columns(2)

    from_hour_morning = col1.slider('Rano od', min_value=5, max_value=12, value=5)
    to_hour_morning = col1.slider('Rano do', min_value=5, max_value=12, value=9)
    col1.write('Pocatecni stanice rano mezi {} a {}'.format(from_hour_morning,
                                                              to_hour_morning))
    query_morning = """SELECT
                           start_station_latitude as lat,
                           start_station_longitude as lon
                        FROM edinburgh_bikes
                        WHERE hour(started_at) BETWEEN {} AND {}
                        LIMIT 100000
                    """.format(from_hour_morning,to_hour_morning)
    df_bikes_morning   = pd.read_sql(sql=query_morning, con=engine)
    col1.map(df_bikes_morning)

    from_hour_afternoon = col2.slider('Vecer od', min_value=12, max_value=23, value=15)
    to_hour_afternoon = col2.slider('Vecer do', min_value=12, max_value=23, value=19)
    col2.write('Pocatecni stanice odpoledne mezi {} a {}'.format(from_hour_afternoon,
                                                                 to_hour_afternoon))
    query_afternoon = """SELECT
                       start_station_latitude as lat,
                       start_station_longitude as lon
                    FROM edinburgh_bikes
                    WHERE hour(started_at) BETWEEN {} AND {}
                    LIMIT 100000
                """.format(from_hour_afternoon, to_hour_afternoon)
    df_bikes_afternoon = pd.read_sql(sql=query_afternoon, con=engine)
    col2.map(df_bikes_afternoon)

if page == 'Thomson':
    st.write('Thomson sampling')


if page == 'Covid':

    query_countries = 'SELECT DISTINCT country as country FROM covid19_basic_differences'
    df_countries = pd.read_sql(sql=query_countries, con=engine)
    list_of_countries = df_countries['country'].values.tolist()
    list_of_countries

    country = st.sidebar.multiselect(
     'Pick up country',
        list_of_countries,
        ['Czechia'])

    filter_country = to_filter('country',country)
    filter_country

    sql_dict = {'table':'covid19_basic_differences',
                'columns':['date','country'],
                'measures':'sum(confirmed) as confirmed',
                'filters':[filter_country]}

    query_for_covid = dict_to_sql(sql_dict)
    df_covid = pd.read_sql(sql=query_for_covid, con=engine)
    df_covid

    st.write('Covid data analysis')
    col1, col2 = st.columns(2)
    col1.write(df_covid)


    brush = alt.selection(type='interval', encodings=['x'])
    selection = alt.selection_multi(fields=['country'], bind='legend')

    base_chart = alt.Chart(df_covid).mark_line().encode(
            x='date',
            y=alt.Y('confirmed', scale=alt.Scale(zero=False)),
            color='country',
            opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
        ).add_selection(
            selection
        )
    col2.altair_chart(base_chart, use_container_width=True)
