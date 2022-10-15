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
st.title('Just a link to my Google Sheets')
st.subheader('Data are automatically refreshed if I change them in original sheet. So cool :-)')

link = '[How many push-ups I do?](https://docs.google.com/spreadsheets/d/e/2PACX-1vSrWEH5plL1gmWoqyd2L81iqdCVlU2iVI37XtlJrr03ih9dk1SEE0CvNTuJcTk3ODJj_7kW6_ASi8BB/pubhtml?gid=2131450823&single=true)'
st.markdown(link, unsafe_allow_html=True)


