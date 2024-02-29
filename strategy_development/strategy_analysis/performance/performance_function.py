import sys
sys.path.append('../../')
from strategy_formulation.strategy.tilted_mean_reversion_strategy import MeanReversion
from strategy_formulation.research.stock_info.stock_info import sap500_tickers
import numpy as np
import yfinance as yf
import pandas as pd



# Define a function that allows you to analyse the startegy performance while adjusting certain parameters

# The output will be a pandas DataFrame containing the data

'''
The input parameters will be
1. scope 
2. buy_range
3. sell_range

'''

periods = [ 
    ['1984-01-02', '1994-01-01', 100], 
    ['1994-01-02', '2004-01-01', 100], 
    ['2004-01-02', '2014-01-01', 100], 
    ['2014-01-02', '2024-01-01', 100],
]

tickers_range = [0,50]

relevant_metrics = ['B&H % increase','Strat risk-adj % increase', 'No. of trades', 'Win / Loss Ratio']

def performance_analysis(periods, tickers_range, relevant_metrics, scope = 30, buy_range = 2, sell_range = 2):

    # Get list of tickers for stock data
    tickers = sap500_tickers(tickers_range[0], tickers_range[1])
    # Gather tickers stock info
    dict_of_tickers = {ticker : MeanReversion(ticker) for ticker in tickers}
    # Filter out tickers with empty stock data
    dict_of_tickers = {k : v for k, v in dict_of_tickers.items() if not v.data.empty}




    output_data = {(key, metric) : [] for key in dict_of_tickers for metric in relevant_metrics}
    index_labels = [f"{start} to {end}" for start, end, _ in periods]

    for key in dict_of_tickers:
        for period in periods:
            result = dict_of_tickers[key].tilted_mean_reversion(period, scope = scope, buy_range = buy_range, sell_range = sell_range, graph = False, analysis = False)
            for metric in relevant_metrics:
                output_data[(key, metric)].append(result[metric])
    output_df = pd.DataFrame(output_data)
    output_df.index = index_labels

    return output_df