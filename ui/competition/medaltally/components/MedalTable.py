import streamlit as st
import pandas as pd
from competition.medaltally.api import MedalTableOperation
from country.api import CountryOperation, GameOperation
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode


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

        medalTable = pd.merge(left=medalTable, right=nocTable,
                              left_on='country_noc', right_on='noc', how='left')
        medalTable = pd.merge(left=medalTable, right=olympicEditionTable,
                              left_on='edition_id', right_on='edition_id', how='left')
        medalTable = medalTable.drop(columns=['noc'])

        col1, col2, col3 = st.columns(3)
        with col1:
            editionSelect = st.selectbox(
                "Select Edition:",
                ["All", *olympicEditionTable['edition'].tolist()],
                key="medal_table_edition"
            )
        with col2:
            countrySelect = st.selectbox(
                "Select Country:", ["All", *nocTable['country'].tolist()],
                key="medal_table_country"
            )
        with col3:
            orderSelect = st.selectbox(
                "Order :",
                ["Total Medals", "Gold", "Alphabetical"],
                key="medal_table_order"
            )

        # TODO: Add sports and gender selection

        if editionSelect != "All":
            medalTable = medalTable[medalTable['edition'] == editionSelect]
        if countrySelect != "All":
            medalTable = medalTable[medalTable['country'] == countrySelect]
        if "Total Medals":
            medalTable = medalTable.sort_values(by='total', ascending=False)
        elif "Gold":
            medalTable = medalTable.sort_values(by='gold', ascending=False)
        elif "Alphabetical":
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

        medalTable = medalTable.head(5)

        gb = GridOptionsBuilder.from_dataframe(medalTable)
        gb.configure_default_column(
            resizable=True, filterable=True, sortable=True, editable=True)
        gb.configure_column("Country", width=100, lockPosition=True)
        gb.configure_column("Olympic Edition", width=150, lockPosition=True)
        gb.configure_column("Gold", width=100)
        gb.configure_column("Silver", width=100)
        gb.configure_column("Bronze", width=100)
        gb.configure_column("Total Medals", width=150)
        gb.configure_columns()
        gridOptions = gb.build()

        # Display the DataFrame using AgGrid
        displayTable = AgGrid(
            medalTable,
            gridOptions=gridOptions,
            allow_unsafe_jscode=True,
            fit_columns_on_grid_load=True,
            height=500,
            width='100%',
            theme='material',
            update_mode=GridUpdateMode.MODEL_CHANGED,
            data_return_mode=DataReturnMode.AS_INPUT)

        print("reloaded")

        df = displayTable['data']
        df2 = displayTable['selected_rows']
        print(df)
        print(df2)
        # st.data_editor(medalTable, hide_index=True, column_order=[
        #                'Olympic Edition', 'Country', 'Gold', 'Silver', 'Bronze', 'Total Medals'])
