import streamlit as st
import pandas as pd
from competition.medaltally.api import MedalTableOperation
from country.api import CountryOperation, GameOperation
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder


class CountryTotalOvertime:
    def __init__(self):
        pass

    @staticmethod
    def display():
        st.title("Country Consistency Over Time")

        nocTable = pd.DataFrame(CountryOperation.search().json())

        medalTable = MedalTableOperation.search()

        olympicEditionTable = pd.DataFrame(GameOperation.search().json())
        olympicEditionTable = olympicEditionTable[['edition_id', 'edition']]

        medalTable = pd.merge(left=medalTable, right=nocTable,
                              left_on='country_noc', right_on='noc', how='left')
        medalTable = pd.merge(left=medalTable, right=olympicEditionTable,
                              left_on='edition_id', right_on='edition_id', how='left')
        medalTable.drop(columns=['country_noc'], inplace=True)

        nocTable = pd.merge(left=nocTable, right=medalTable[['noc']],
                            left_on='noc', right_on='noc', how='right')
        nocTable.drop_duplicates(subset='noc', inplace=True)

        medalTable['year'] = medalTable['edition'].str[:4]
        medalTable['year'] = pd.Categorical(medalTable['year'], ordered=True)

        #! Note about the observed parameter
        medalTableByYear = medalTable.groupby(
            ['year', 'noc'], observed=False)[['gold', 'silver', 'bronze', 'total']].sum().reset_index()
        medalTableByYear = pd.merge(
            left=medalTableByYear, right=nocTable, left_on='noc', right_on='noc', how='left')

        # st.write(nocTable.columns.tolist())
        countrySelect = st.selectbox(
            "Select Country:", ["Top three highest",
                                "All", *nocTable['country'].tolist()],
            key="country_total_overtime_country"
        )

        tableTodraw = medalTableByYear[medalTableByYear['country']
                                       == countrySelect]

        if countrySelect == "All":

            tableTodraw = medalTableByYear

        elif countrySelect == "Top three highest":

            topThreeHighestTotal = medalTableByYear.groupby(['noc'])['total'].sum(
            ).reset_index().sort_values(by='total', ascending=False).head(3)

            tableTodraw = medalTableByYear[medalTableByYear['noc'].isin(
                topThreeHighestTotal['noc'].tolist())]

        fig = px.line(tableTodraw, x='year', y='total', color='country',
                      title='Country Consistency Over Time (Total Medals)',
                      labels={'total': 'Total Medals', 'country': 'Country'})

        st.write(fig)
