import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

class StockAPI:

    def __init__(self):
        self.api_key = st.secrets["API_KEY"]
        self.url = "https://alpha-vantage.p.rapidapi.com/query"
        self.headers =  {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "alpha-vantage.p.rapidapi.com"
        }

    def symbol_search(self, company: str) -> dict:
        querystring = {
            "datatype":"json",
            "keywords": company ,
            "function":"SYMBOL_SEARCH"
        }
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        # create a blank dictionary
        data2 = {}
        # Apply for loop 
        for i in data["bestMatches"]:
            symbol = i["1. symbol"]
            data2[symbol] = [i["2. name"], i["4. region"], i["8. currency"]]
        # Return data2
        return data2
    
    def daily_data(self, symbol: str) -> pd.DataFrame:
        querystring = {
            "function":"TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize":"compact",
            "datatype":"json"
        }
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        df = pd.DataFrame(data["Time Series (Daily)"]).T
        # Convert the data to float
        df = df.astype(float)
        # Convert index to datetime
        df.index = pd.to_datetime(df.index)
        # Add name to index
        df.index.name = "Date"
        return df

    def plotly_chart(self, df: pd.DataFrame) -> go.Figure:
        fig = go.Figure(data = [
            go.Candlestick(
                x = df.index,
                open = df["1. open"],
                high = df["2. high"],
                low = df["3. low"],
                close = df["4. close"]
            )
        ])
        fig.update_layout(width = 1200, height= 800)
        return fig
