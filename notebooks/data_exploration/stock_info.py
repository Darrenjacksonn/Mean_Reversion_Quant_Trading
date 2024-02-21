import yfinance as yf
import pandas as pd
import matplotlib as plt
import numpy as np
from statsmodels.tsa.stattools import adfuller

'''
Going to define a custom class, each instance is the information on a single stock, will then define a seperate 
analysing class to compare stocks

This class StockInfo will contain all information about a stock between a certain period specified and will 
also be able to compute relevant mathematical computations on the stock info, as well as plot some key graphs.
'''



class StockInfo():
    '''
    This class gathers the 'Adj Close' prices of the stock with ticker = ticker
    
    When you initiate the function you have the option to select a start and end date, if none are inputted,
    all possible data will be selected. The data is stored in a pandas DataFrame.
    '''


    def __init__(self, ticker: str, start = None, end = None, interval = '1d') -> pd.DataFrame:
        adj_close_prices = yf.download(ticker, start = start, end = end, interval = interval)['Adj Close'].to_frame()
        
        self.data = adj_close_prices.rename(columns = {'Adj Close' : f"{ticker}"})
        self.ticker = ticker

    # period = [start, end, amount theoretically invested]

    def default_period(self, period):
        if not period:
            period = [self.data.index[0], self.data.index[-1], 1]
        return period



    '''
        For Displaying info about the Stock Prices
                                                    '''

    def display_data(self, period = None):
        period = self.default_period(period)
        return self.data.loc[period[0] : period[1]]

    def plot_stock_price(self, period = None):
        period, segment = self.default_period(period), self.display_data(period)
        segment.plot()






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
        return return_df.iloc[-1] - return_df.iloc[0]

    def perc_returns(self, period = None) -> float:
        return_df = self.df_returns(period)
        return (return_df.iloc[-1] - return_df.iloc[0]) / return_df.iloc[0] * 100

    def plot_returns(self, period = None):
        return_df = self.df_returns(period)
        return_df.plot()
    


    




    '''
        THESE METHODS HELP YOU WORK WITH VOLATILITY
                                                    '''

    def variance(self, period = None):
        period = self.default_period(period)
        segment = self.data.loc[period[0] : period[1]]
        return segment.pct_change().mul(100).dropna().var()

    def sigma(self, period = None):
        return np.sqrt(self.variance(period))


    '''
        Augmented Dickey-Fuller Test
                                    '''

    def adf_test(self, period = None, graph = False):
        period = self.default_period(period)
        segment = self.data.loc[period[0] : period[1]]
        arr = segment.iloc[:,0] # Converts 1D Pandas DataFrame to series
        result = adfuller(arr)
        if graph:
            self.plot_stock_price(period)
        return f" ADF Statistic: {result[0]} \np-value: {result[1]}"
        