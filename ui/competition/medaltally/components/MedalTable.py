import streamlit as st
import pandas as pd
from competition.medaltally.api import MedalTableOperation
from country.api import CountryOperation, GameOperation
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode


class MedalTable:
    def __init__(self):
        pass

    def medalTableToDisplay(self):
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

        medalTable = medalTable[[
            'Olympic Edition', 'Country', 'Gold', 'Silver', 'Bronze', 'Total Medals', 'id', 'edition_id', 'country_noc']]
        return medalTable
        pass

        # if st.button("Save Changes"):
        #     displayTable.columns_state
        #     print(displayTable.columns_state)
        # MedalTable().updateGridTable(medalTableCopy, recordUpdateDF)
        # st.success("Changes saved successfully!")

    def gridTable(self, df):
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(applyColumnDefOrder=True,
                                    resizable=True, filterable=True, sortable=True)
        gb.configure_column("Olympic Edition", width=150)
        gb.configure_column("Country", width=100)
        gb.configure_column("Gold", width=100, editable=True)
        gb.configure_column("Silver", width=100, editable=True)
        gb.configure_column("Bronze", width=100, editable=True)
        gb.configure_column("Total Medals", width=150)
        gb.configure_column("id", hide=True)
        gb.configure_column("edition_id", hide=True)
        gb.configure_column("country_noc", hide=True)

        gb.configure_selection(
            selection_mode="multiple", use_checkbox=True, header_checkbox=True)

        gridOptions = gb.build()

        # Display the DataFrame using AgGrid

        displayTable = AgGrid(
            df,
            # editable=True
            gridOptions=gridOptions,
            fit_columns_on_grid_load=True,
            height=500,
            width='100%',
            theme='material',
            # reload_data=True,
            # update_mode=GridUpdateMode.NO_UPDATE,
            data_return_mode=DataReturnMode.AS_INPUT)

        return displayTable

    def updateGridTable(self, original_df, new_df):

        changes = new_df.compare(original_df)

        for index, row in changes.iterrows():
            print("index :")
            print(index)
            # Extract the original and new values
            original_row = original_df.iloc[index]
            print("original :")
            print(original_row)
            new_row = new_df.iloc[index]
            print("new :")
            print(new_row)
            new_row_dict = new_row.to_dict()
            updated_row = {
                'edition_id': int(original_row['edition_id']),
                'country_noc': original_row['country_noc'],
                'country': new_row_dict['Country'],
                'gold': new_row_dict['Gold'],
                'silver': new_row_dict['Silver'],
                'bronze': new_row_dict['Bronze'],
                'total': new_row_dict['Total Medals']
            }
            # Update the database with the new values
            MedalTableOperation.update(
                int(original_row['id']), updated_row)

    @staticmethod
    def display():
        st.title("Medal Table")

        medalTable = MedalTable().medalTableToDisplay()

        medalTable = medalTable.head(5)
        medalTable = medalTable.reset_index(drop=True)
        medalTableCopy = medalTable.copy()

        displayTable = MedalTable().gridTable(medalTable)

        recordUpdateDF = displayTable['data'].reset_index(drop=True)
        recordSelectedDF = displayTable['selected_data']

        st.button("Update", on_click=MedalTable.updateGridTable,
                  args=[medalTable, recordUpdateDF])
