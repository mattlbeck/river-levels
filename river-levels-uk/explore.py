import streamlit as st
from pathlib import Path
import pandas as pd
import altair as alt

dataset = st.selectbox("Select datasest", Path("data").glob("*.csv"))

df = pd.read_csv(dataset, parse_dates=["date"])
st.dataframe(df)

chart = alt.Chart(df).mark_line().encode(
    x="date", 
    y="avg_level"
).properties(width=800, height=400).interactive()

st.altair_chart(chart)