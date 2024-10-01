import streamlit as st
import pandas as pd
import country.main as country
import competition.main as competition

st.sidebar.title("Menu")

menu_options = ['Homepage', 'Country', 'Competition', 'Athlete']

selected_options = st.sidebar.radio('Choose one', menu_options)

if selected_options == 'Homepage':
    pass

if selected_options == 'Country':
    country.main()

if selected_options == 'Competition':
    competition.main()

if selected_options == 'Athlete':
    pass
