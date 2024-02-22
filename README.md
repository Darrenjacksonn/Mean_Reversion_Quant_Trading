# Mean_Reversion Quant Trading
Mean Reversion Quant Trading is a quantitative trading strategy that utilises the mean reversion principal to trade stock assets profitably.

# Description
The purpose of this project is to formulate a low-risk long-term trading stratgey that utilizes mean reversion principals at its core. It is designed to be a favourable alternative to a passive buy and hold position, offering similar returns versus greatly reduced risk in the form of a reduction in time spent in the market. The main reason for choosing a project like this is I have a deep passion for programming, mathematics and a keen interest in financial markets. As a result, this project aims to highlight my comptenecies in these fields, as well as my ability to gather, clean, process, manipulate and analyse data.

# Features & Highlights
In the current iteration the project uses a very standard stratgey that triggers a buy signal when the stocks trading price falls below two standard devations of the running mean.

# Future Improvements (Currently working on)

1. Will add regression to the stratgey, accounting for the general trend of the security to better interpret a profitable buy trigger

2. Will add analysis on the best 'scope' value. The scope is the amount of time the algorithm takes into account when calculating the mean and standard deviation
   
3. Instead of 1, may use the Augmented Dickey Fuller Test to ensure that a buy signal is only triggered when a stock is deemed to be behaving in a 'stationary' manner.

4. Utilize machine learning (particularly the scikit-learn module) to analyse the variables and determine their favourable values.

# Technology Used

Full details of installation requirements can be find in requirements.txt, but the main libraries used were:
pandas, numpy, yfinance and matplotlib
