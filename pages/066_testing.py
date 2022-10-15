import streamlit as st
import altair as alt

from vega_datasets import data

source = data.barley()
source

chart = (
    alt.Chart(source)
    .mark_bar()
    .encode(x="year:O", y="sum(yield):Q", color="year:N", column="site:N")
)

st.write(chart)