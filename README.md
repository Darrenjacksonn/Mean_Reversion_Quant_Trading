# Mean_Reversion_Quant_Trading
Mean Reversion Quant Trading is a quantitative trading strategy that utilises the mean reversion principle at its core. This strategy aims to capitalize on teh statistical tendency of stock prices to revert to their mean over time, facilitating profitable trading opportunities.

# Description
This prject is developed with the objective of creating a low-risk long-term trading stratgey that leverages mean reversion principles. Unlike the traditional passive buy-and-hold approach, this strategy seeks to deliver comparable returns with significantly lower risk by minimizing market exposure. The motivation behind this project stems from my profound interest in programming, mathematics, and financial markets. It showcases my competencies in these areas, demonstrating my skills in data acquisition, cleaning, processing, manipulation, and analysis.

# Features & Highlights
Current Strategy: In the current iteration the project employs a robust mean reversion strategy enhanced with sophisticated analytical techniques to trigger buy signals under optimal conditions. The algorithm integrates linear regression to account for the general trend of the security. This addition allows for a more nuanced interpretation of buy signals, adjusting for underlying trends to refine entry points. This greatly increases the the accuracy of trade signals by considering the directional momentum of stock prices.

# Future Improvements (Currently working on)

1. Will add analysis on the best 'scope' value. The scope is the amount of time the algorithm takes into account when calculating the mean and standard deviation
   
2. Instead of 1, may use the Augmented Dickey Fuller Test to ensure that a buy signal is only triggered when a stock is deemed to be behaving in a 'stationary' manner.

3. Utilize machine learning (particularly the scikit-learn module) to analyse the variables and determine their favourable values.


# Installation

Full details of installation requirements can be find in requirements.txt, but the primary libraries include:
- pandas
- numpy
- yfinance
- matplotlib
- scikit-learn
