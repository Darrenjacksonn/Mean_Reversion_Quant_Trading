import sys
sys.path.append('../')
try: # When doing analysis is strategy_analysis folder
    from strategy_formulation.research.stock_info.stock_info import StockInfo
except:
    pass
try: # When tunning this script directly
    from research.stock_info.stock_info import StockInfo
except:
    pass
import numpy as np
import yfinance as yf
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt



# Function computes a Linear Regression line to fit the data based on the previous 'scope' data points. It outputs True
# if the current price is n below the Linear Regression line
        
def tilted_mean(data, scope, n, check = 'buy'):
    actual_prices = data[-scope:]
    data_points = np.arange(scope).reshape(-1,1)
    model = LinearRegression().fit(data_points, actual_prices)
    predicted_prices = model.predict(data_points)
    current_predicted_price = model.predict([[scope - 1]])[0][0] # What you would expect the current price to be based off of trends
    residuals = actual_prices - predicted_prices
    stddev = residuals.std().iloc[0]
    #print(type(stddev),type(current_predicted_price),type(n),type(data.iloc[-1]))
    if check == 'buy':
        return data.iloc[-1].iloc[0] < (current_predicted_price - n * stddev)

    else:
        return data.iloc[-1].iloc[0] > (current_predicted_price + n * stddev)
    



class MeanReversion(StockInfo):

    def tilted_mean_reversion(self, period, scope = 30, buy_range = 2, sell_range = 2, graph = True, analysis = True):
        period = self.default_period(period)
        segment = self.data.loc[period[0] : period[1]]

        
        '''
            The Strategies Logic
        '''

        
        investment = period[2]
        strat_investment = [ 0 ]
        position = False
        time_in_market = 0
        trades, winning_trades = 0, 0

        # Loop over every data point once there is enough data to analyse previous data
        for i in range(scope, len(segment)):
            if position:
                time_in_market += 1
                perc_change = segment.iloc[i] / segment.iloc[i - 1]
                investment *= perc_change.iloc[0] # Increase investment if we are in the market
                strat_investment.append(investment) 
                # If we go above n std above the linear model line => sell
                if tilted_mean(segment.iloc[i - scope : i], scope = scope, n = sell_range, check = 'sell'):
                    position = False
                    if segment.iloc[i].iloc[0] > starting_point:
                        winning_trades += 1
            else:
                strat_investment.append(0) # If we're not in the market, append 0 to investment amount
                
            if not position and tilted_mean(segment.iloc[i - scope : i], scope = scope, n = buy_range, check = 'buy'):
                trades += 1
                starting_point = segment.iloc[i].iloc[0]
                position = True # if we are not in the market and the price is below 2std below the mean -> buy



        results = {
            'strat_returns' : investment,
            'strat_array_returns' : strat_investment,
            'time_in_market' : time_in_market,
            'no_of_trades' : trades,
            'no_of_winning_trades' : winning_trades
        }

        return self.strategy_template(results, period = period, scope = scope, graph = graph, analysis = analysis)