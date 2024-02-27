import sys
sys.path.append('../../..')
from stock_info.stock_info import StockInfo
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

'''
The class below is an extension to the StockInfo class, which adds the following method:
1. a method that allows you to calculate the buy and hold returns of a stock.
2. a method that acts as a strategy template, which you can call to evaluate your stratgey against a buy and hold position

The input parameters are:
period = Which is of the usual format [start_date, end_date, amount_invested]
scope = This determines how far after the start_date that the security is bought and then held. This is important as if a stratgey triggers buy
signals on historical data, it will need a certain amount of data before it begins making decisions. This 'scope' ensures that the buy and hold 
method below and the strategy that it is being compared to begin trading on the same day, hence can be compared accurately.

It plots the stock price trajectory if required (graph = True)

It prints the final investment amount and the percentage increase

It returns the final investement amount and the list of all invesment amounts throughout the period as a list
'''

class StrategyComparison(StockInfo):

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
            'strat_returns' : Your strategies returns (float) , 
            'strat_array_returns' : Your stratgeies returns at each data point (List) , 
            'time_in_market' : The time spent in the market (int)
        }

        Then return this function in your custom method
    '''
    
    def strategy_template(self, results: dict, scope, period = None, graph = True, analysis = True):
        period = self.default_period(period)
        segment = self.data.loc[period[0] : period[1]]
        
        bah_investment = self.buy_and_hold(period, scope = scope, graph = False, plotting = True, analysis = False)

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

        if analysis:
            print('Initial Investment:',period[2],'\nBuy and Hold Returns:',bah_returns, f"  Percentage Increase:  {bah_perc_returns} %" ,'\nStrategy Returns:',strat_returns,f"      Percentage Increase:  {strat_perc_returns} %",f" Risk-Adjusted Returns: {strat_risk_adj_returns} %")
        
        return [bah_returns, bah_perc_returns, strat_returns, strat_perc_returns, strat_risk_adj_returns]
    