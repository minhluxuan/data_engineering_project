import streamlit as st
import pandas as pd
from competition.medaltally.api import MedalTableOperation
from country.api import CountryOperation, GameOperation
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder
from .components.MedalTable import MedalTable
from .components.BestOfOlympics import BestOlympics
from .components.CountryTotalOvertime import CountryTotalOvertime


class Dashboard:
    def __init__(self):
        pass

    @staticmethod
    def display():
        MedalTable.display()
        # CountryTotalOvertime.display()
        # BestOlympics.display()


# Display the Dashboard
# Dashboard.display()
