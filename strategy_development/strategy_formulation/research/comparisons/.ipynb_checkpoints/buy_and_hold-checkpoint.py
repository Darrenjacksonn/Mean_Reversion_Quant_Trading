import sys
sys.path.append('../../data_exploration')

from stock_info import StockInfo
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

'''
The class below is an extension to the StockInfo class, which adds a method that allows you to calculate the buy and hold returns of a stock.

The input parameters are:
period = Which is of the usual format [start_date, end_date, amount_invested]
scope = This determines how far after the start_date that the security is bought and then held. This is important as if a stratgey triggers buy
signals on historical data, it will need a certain amount of data before it begins making decisions. This 'scope' ensures that the buy and hold 
method below and the strategy that it is being compared to begin trading on the same day, hence can be compared accurately.

It plots the stock price trajectory if required (graph = True)

It prints the final investment amount and the percentage increase

It returns the final investement amount and the list of all invesment amounts throughout the period as a list
'''

class Strategy_Comparison(StockInfo):

    def buy_and_hold(self, period, scope = 30, graph = True):
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

        print('Buy and Hold Returns:',round(bah_investment[-1], 2), f"  percentage_increase:  {(bah_investment[-1] / period[2] - 1) * 100:.2f} %")
        return [round(bah_investment[-1], 2), bah_investment]