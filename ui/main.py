import streamlit as st
import pandas as pd
import country.main as country
from competition.medaltally.main import MedalTable, DataInsight

st.sidebar.title("Menu")

menu_options = ['Competition', 'Homepage', 'Country', 'Athlete']

selected_options = st.sidebar.radio('Choose one', menu_options)

if selected_options == 'Competition':
    MedalTable.display()

if selected_options == 'Homepage':
    pass

if selected_options == 'Country':
    country.main()


if selected_options == 'Athlete':
    pass
