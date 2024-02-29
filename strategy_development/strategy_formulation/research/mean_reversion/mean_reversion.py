import sys
sys.path.append('../')

from comparisons.buy_and_hold import StrategyComparison
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt


# Classic Mean Reversion Stratgey

class MeanReversion(StrategyComparison):

    def mean_reversion(self, period, scope = 30, graph = True, analysis = True):
        period = self.default_period(period)
        segment = self.data.loc[period[0] : period[1]]
        
        bah_investment = self.buy_and_hold(period, scope = scope, graph = False, plotting = True, analysis = False)
        
        investment = period[2]
        strat_investment = [ investment ]
        position = False
        length_in_market = 0

        # Loop over every data point once there is enough data to analyse previous data
        for i in range(scope, len(segment)):
            if position:
                length_in_market += 1
                perc_change = segment.iloc[i] / segment.iloc[i - 1]
                investment *= perc_change.iloc[0] # Increase investment if we are in the market
                strat_investment.append(investment) 
                # If we go above 2std above the mean, sell
                if segment.iloc[i].iloc[0] > segment.iloc[i - scope : i].mean().iloc[0] + 2 * np.sqrt(segment.iloc[i - scope : i].var().iloc[0]):
                    position = False
            else:
                strat_investment.append(0) # If we're not in the market, append 0 to investment amount
                
            if not position and segment.iloc[i].iloc[0] < segment.iloc[i - scope : i].mean().iloc[0] - 2 * np.sqrt(segment.iloc[i - scope : i].var().iloc[0]):
                position = True # if we are not in the market and the price is below 2std below the mean -> buy

        perc_in_market = length_in_market / (len(segment) - scope)
        if perc_in_market:
            risk_adj_returns = ( (investment / period[2] - 1) * 100 ) / perc_in_market
        else:
            risk_adj_returns = 0

        if graph:
            plt.figure()
            plt.plot(strat_investment, label = 'Mean Reversion Stratgey Returns')
            plt.plot(bah_investment, label = 'Buy and Hold Returns', alpha = 0.4)
            plt.title(f"Mean Reversion Strategy versus Buy and Hold Strategy for {self.ticker}")
            plt.xlabel('Time')
            plt.ylabel('Investment Value')
            plt.legend()
            plt.show()

        def round_2_dp(x):
            return round(x,2)

        bah_returns = round_2_dp(bah_investment[-1])
        bah_perc_returns = round_2_dp((bah_investment[-1] / period[2] - 1) * 100)
        strat_returns = round_2_dp(investment)
        strat_perc_returns = round_2_dp((investment / period[2] - 1) * 100)
        strat_risk_adj_returns = round_2_dp(risk_adj_returns)

        if analysis:
            print('Initial Investment:',period[2],'\nBuy and Hold Returns:',bah_returns, f"  percentage_increase:  {bah_perc_returns} %" ,'\nStrategy Returns:',strat_returns,f"      percentage_increase:  {strat_perc_returns} %",f" Risk-Adjusted Returns: {strat_risk_adj_returns} %")
        
        return [bah_returns, bah_perc_returns, strat_returns, strat_perc_returns, strat_risk_adj_returns]