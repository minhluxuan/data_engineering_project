import streamlit as st
import pandas as pd
from competition.medaltally.api import MedalTableOperation
from country.api import CountryOperation, GameOperation
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder


class BestOlympics:
    def __init__(self):
        pass

    @staticmethod
    def display():
        st.title("Best Olympics for each country")

        nocTable = pd.DataFrame(CountryOperation.search().json())

        medalTable = MedalTableOperation.search()

        olympicEditionTable = pd.DataFrame(GameOperation.search().json())
        olympicEditionTable = olympicEditionTable[['edition_id', 'edition']]

        medalTable = pd.merge(medalTable, nocTable,
                              left_on='country_noc', right_on='noc', how='left')
        medalTable = pd.merge(medalTable, olympicEditionTable,
                              left_on='edition_id', right_on='edition_id', how='left')
        medalTable = medalTable.drop(columns=['noc'])

        # Identify the best Olympic edition for each country
        best_olympics = medalTable.loc[medalTable.groupby(
            'country')['total'].idxmax()]

        # Create a bar chart
        fig = px.bar(best_olympics, x='country', y='total', color='edition',
                     title='Best Olympic Edition for Each Country (Total Medals)',
                     labels={'total': 'Total Medals', 'country': 'Country', 'edition': 'Olympic Edition'})

        st.plotly_chart(fig, use_container_width=True)
