import streamlit as st
import pandas as pd
from competition.medaltally.api import MedalTableOperation
from country.api import CountryOperation, GameOperation
import altair as alt
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder


class MedalTable:
    def __init__(self):
        pass

    @staticmethod
    def display():
        st.title("Medal Table")

        nocTable = pd.DataFrame(CountryOperation.search().json())

        medalTable = MedalTableOperation.search()

        olympicEditionTable = pd.DataFrame(GameOperation.search().json())
        olympicEditionTable = olympicEditionTable[['edition_id', 'edition']]

        medalTable = pd.merge(medalTable, nocTable,
                              left_on='country_noc', right_on='noc', how='left')
        medalTable = pd.merge(medalTable, olympicEditionTable,
                              left_on='edition_id', right_on='edition_id', how='left')
        medalTable = medalTable.drop(columns=['noc'])

        col1, col2, col3 = st.columns(3)
        with col1:
            editionSelect = st.selectbox(
                "Select Edition:",
                ["All", *olympicEditionTable['edition'].tolist()]
            )
        with col2:
            countrySelect = st.selectbox(
                "Select Country:", ["All", *nocTable['country'].tolist()]
            )
        with col3:
            orderSelect = st.selectbox(
                "Order :",
                ["Total Medals", "Gold", "Alphabetical"]
            )

        # TODO: Add sports and gender selection

        if editionSelect != "All":
            medalTable = medalTable[medalTable['edition'] == editionSelect]
        if countrySelect != "All":
            medalTable = medalTable[medalTable['country'] == countrySelect]
        if orderSelect == "Total Medals":
            medalTable = medalTable.sort_values(by='total', ascending=False)
        elif orderSelect == "Gold":
            medalTable = medalTable.sort_values(by='gold', ascending=False)
        elif orderSelect == "Alphabetical":
            medalTable = medalTable.sort_values(by='country')

        medalTable = medalTable.rename(columns={
            'edition': 'Olympic Edition',
            'country': 'Country',
            'gold': 'Gold',
            'silver': 'Silver',
            'bronze': 'Bronze',
            'total': 'Total Medals'
        })
        medalTable.drop(
            columns=['edition_id', 'country_noc', 'id'], inplace=True)

        gb = GridOptionsBuilder.from_dataframe(medalTable)
        gb.configure_default_column(
            resizable=True, filterable=True, sortable=True)
        gb.configure_column("Olympic Edition", width=150)
        gb.configure_column("Country", width=100)
        gb.configure_column("Gold", width=100)
        gb.configure_column("Silver", width=100)
        gb.configure_column("Bronze", width=100)
        gb.configure_column("Total Medals", width=150)
        gridOptions = gb.build()

        # Display the DataFrame using AgGrid
        AgGrid(medalTable, gridOptions=gridOptions, height=500, width='100%')
        # st.data_editor(medalTable, hide_index=True, use_container_width=True, column_order=[
        #                'Olympic Edition', 'Country', 'Gold', 'Silver', 'Bronze', 'Total Medals'])


class DataInsight:
    def __init__(self):
        pass

    @staticmethod
    def display():
        st.title("Data Insight")
        st.write("This page will display data insights")

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
                     labels={'Total Medals': 'total', 'Country': 'country', 'Olympic Edition': 'edition'})

        st.plotly_chart(fig)
