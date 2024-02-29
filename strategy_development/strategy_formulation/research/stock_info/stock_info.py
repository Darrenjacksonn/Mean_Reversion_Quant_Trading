import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#from statsmodels.tsa.stattools import adfuller

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





    def buy_and_hold(self, period, scope = 30, graph = True, plotting = False, analysis = True):
        period = self.default_period(period)
        segment = self.data.loc[period[0] : period[1]]
        
        bah_investment = [ period[2] ]

        for i in range(scope, len(segment)):
            bah_perc_change = segment.iloc[i] / segment.iloc[i - 1]
            bah_investment.append(bah_investment[-1] * bah_perc_change.iloc[0])

        if graph:
            plt.figure()
            plt.plot(bah_investment, label = 'Buy and Hold Returns')
            plt.title(f"Buy and Hold Returns for stock {self.ticker}")
            plt.xlabel('Time')
            plt.ylabel('Investment Value')
            plt.show()

        if analysis:
            print('Buy and Hold Returns:',round(bah_investment[-1], 2), f"  percentage_increase:  {(bah_investment[-1] / period[2] - 1) * 100:.2f} %")
        if plotting:
            return bah_investment
        return round(bah_investment[-1], 2)
    



    '''
        In order to use the below function to test your custom strategy against a buy and hold position, you must:
        1. Create a new CustomStrategy class that inherits from this class
        2. Create a custom strategy method that produces a results dictionary with the follwowing setup:
        results = {
            'strat_returns'         : Your strategies returns (float) , 
            'strat_array_returns'   : Your stratgeies returns at each data point (List) , 
            'time_in_market'        : The time spent in the market (int),
            'no_of_trades'          : The quantity of trades (int),
            'no_of_winning_trades'  : The quantity of winning trades (int)
        }

        Then return this function in your custom method

    '''
    
    def strategy_template(self, results: dict, scope, period = None, graph = True, analysis = True):
        period = self.default_period(period)
        segment = self.data.loc[period[0] : period[1]]
        
        bah_investment = self.buy_and_hold(period, scope = scope, graph = False, plotting = True, analysis = False)

        w_l_ratio = 0
        # Works out the win / loss Ratio
        if results['no_of_trades'] - results['no_of_winning_trades']:
            w_l_ratio = results['no_of_winning_trades'] / (results['no_of_trades'] - results['no_of_winning_trades'] )
        
        
        # Works out the risk adjusted return

        perc_in_market = results['time_in_market'] / ( len(segment) - scope )
        if perc_in_market:
            risk_adj_returns = ( (results['strat_returns'] / period[2] - 1) * 100 ) / perc_in_market
        else:
            risk_adj_returns = 0
        

        # Plots the results if required
        
        if graph:
            plt.figure()
            plt.plot(results['strat_array_returns'], label = 'Stratgey Returns')
            plt.plot(bah_investment, label = 'Buy and Hold Returns', alpha = 0.4)
            plt.title(f"Strategy versus Buy and Hold for {self.ticker}")
            plt.xlabel('Time')
            plt.ylabel('Investment Value')
            plt.legend()
            plt.show()
        

        # Rounds all of our key results to 2 decimal places
            
        def round_2_dp(x):
            return round(x,2)

        bah_returns = round_2_dp(bah_investment[-1])
        bah_perc_returns = round_2_dp((bah_investment[-1] / period[2] - 1) * 100)

        strat_returns = round_2_dp(results['strat_returns'])
        strat_perc_returns = round_2_dp((results['strat_returns'] / period[2] - 1) * 100)
        strat_risk_adj_returns = round_2_dp(risk_adj_returns)
        
        trades = results['no_of_trades']
        w_l_ratio = round_2_dp(w_l_ratio)

        if analysis:
            print('Initial Investment:',period[2],'\nBuy and Hold Returns:',bah_returns, f"  Percentage Increase:  {bah_perc_returns} %" ,'\nStrategy Returns:',strat_returns,f"      Percentage Increase:  {strat_perc_returns} %",f" Risk-Adjusted Returns: {strat_risk_adj_returns} %",'\nNumber of Trades:',trades,'       Win / Loss Ratio:', w_l_ratio)
        
        return {
            'B&H increase'                  : bah_returns, 
            'B&H % increase'                : bah_perc_returns, 
            'Strat increase'                : strat_returns, 
            'Strat % increase'              : strat_perc_returns, 
            'Strat risk-adj % increase'     : strat_risk_adj_returns, 
            'No. of trades'                 : trades, 
            'Win / Loss Ratio'              : w_l_ratio,
        }






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