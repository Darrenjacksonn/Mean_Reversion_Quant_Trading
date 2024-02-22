import yfinance as yf
import pandas as pd
import matplotlib as plt
import numpy as np
from statsmodels.tsa.stattools import adfuller

import requests as rq
from bs4 import BeautifulSoup as bs

'''
StockInfo() is used to gather the 'Adj Close' stock price of stocks from yahoo finance using yfinance.
Each instance is the information of a single stock. It takes parameters are:
ticker = ticker symbol of stock
start = start date of information retrieval
end = end date of information retrieval
interval = frequency of data points
Valid values for interval include:
1m, 2m, 5m, 15m, 30m, 60m, 90m, 1d, 5d, 1wk, 1mo, 3mo


This methods of this class allow you to conduct mathematical computations on the stock info, 
as well as plot some key graphs. Each method has a description above it.
'''



class StockInfo():
    
    # By default (no values for start or end) this class stores all the available data as a pandas DataFrame.
    
    def __init__(self, ticker: str, start = None, end = None, interval = '1d') -> pd.DataFrame:
        
        # Includes custom exception handling so future methods do not break if stock info is not available for a set of given parameters
        try:
            adj_close_prices = yf.download(ticker, start = start, end = end, interval = interval)['Adj Close'].to_frame()

            if adj_close_prices.empty:
                raise ValueError(f"No Data foound for ticker {ticker} in the given date range")
            
            self.data = adj_close_prices.rename(columns = {'Adj Close' : f"{ticker}"})
            self.ticker = ticker
        
        except ValueError as ve:
            print(ve)
            self.data = pd.DataFrame()
            self.ticker = ticker
        
        except Exception as e:
            print(f"An unexpected error occurres: {e}")
            self.data = pd.DataFrame()
            self.ticker = ticker
    
    
    # For all methods we will assume that period is a list with the following layout:
    # period = [start_date, end_date, investment_amount]
    

    # This method is called upon to initiate the entire dataset if no period is specified
    def default_period(self, period):
        if not period:
            period = [self.data.index[0], self.data.index[-1], 100]
        return period
    # I may change period to be a dictionary: period = { 'start' : start... } in the future as it would most likely improve readability below


    '''
        For Displaying info about the Stock Prices and performing analysis on the stock data
    '''


    def display_data(self, period = None):
        period = self.default_period(period)
        return self.data.loc[period[0] : period[1]]

    def plot_stock_price(self, period = None):
        period, segment = self.default_period(period), self.display_data(period)
        segment.plot()
    
    '''
        THESE METHODS ARE STATISITCAL MEASURES OF prices
    '''
    
    def variance(self, period = None): 
        period = self.default_period(period)
        segment = self.data.loc[period[0] : period[1]]
        return segment.var()
    
    def std(self, period = None):
        return np.sqrt(self.variance(period))
    
    def mean(self, period = None):
        period = self.default_period(period)
        segment = self.data.loc[period[0] : period[1]]
        return segment.mean()






    '''
        THESE METHODS HELP YOU WORK WITH RETURNS 
    '''
    
    # 'returns' function outputs the returns of the stock in a given interval
    def df_returns(self, period = None) -> pd.DataFrame:
        period = self.default_period(period)
        segment = self.data.loc[period[0] : period[1]]
        return segment.div(segment.iloc[0]).mul(period[2])

    def returns(self, period = None) -> float:
        return_df = self.df_returns(period)
        return return_df.iloc[-1]

    def profit(self, period = None) -> float:
        return_df = self.df_returns(period)
        return return_df.iloc[-1] - return_df.iloc[0]

    def perc_returns(self, period = None) -> float:
        return_df = self.df_returns(period)
        return (return_df.iloc[-1] - return_df.iloc[0]) / return_df.iloc[0] * 100

    def plot_returns(self, period = None):
        return_df = self.df_returns(period)
        return_df.plot()
    

    '''
        THESE METHODS ARE STATISITCAL MEASURES OF RETURNS
    '''
    

    def variance_of_returns(self, period = None): # Finds the variance of the Adj Close values
        period = self.default_period(period)
        segment = self.data.loc[period[0] : period[1]]
        return segment.pct_change().mul(period[2]).dropna().var()

    def std_of_returns(self, period = None):
        return np.sqrt(self.variance_of_returns(period))
    
    def mean_of_returns(self, period = None):
        period = self.default_period(period)
        segment = self.data.loc[period[0] : period[1]]
        return segment.pct_change().mul(period[2]).dropna().mean()





    '''
        Augmented Dickey-Fuller Test
    '''

    # def adf_test(self, period = None, graph = False):
    #     period = self.default_period(period)
    #     segment = self.data.loc[period[0] : period[1]]
    #     arr = segment.iloc[:,0] # Converts 1D Pandas DataFrame to series
    #     result = adfuller(arr)
    #     if graph:
    #         self.plot_stock_price(period)
    #     return f" ADF Statistic: {result[0]} \np-value: {result[1]}"





# This function finds S&P500 stock tickers in order of market cap

def sap500_tickers(index_1, index_2):

    url = 'https://stockanalysis.com/list/sp-500-stocks/'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    table_entries = soup.find_all('td')
    tickers = []
    for td in table_entries:
        a_tags = td.find('a')
        if a_tags:
            tickers.append(a_tags.text)
    return tickers[index_1 : index_2]