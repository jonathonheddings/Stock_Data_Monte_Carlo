import pandas as pd
import numpy as np
from pandas_datareader import data as wb
from scipy.stats import norm
import matplotlib as mpl
import matplotlib.pyplot as plt

# Function to create a Geometric Brownian Motion Monte Carlo
#          simulation to model potential future stock prices
#
def get_monte_carlo(ticker, startdate, enddate, years):  
    
    # Pull Stock data and Compute the logreturns
    stock_data = pd.DataFrame()
    stock_data[ticker] = wb.DataReader(ticker, data_source="yahoo", start=startdate, end=enddate)['Adj Close']
       
    log_returns = np.log(1 + stock_data.pct_change())   
    
    # Compute Statistics
    mean = log_returns.mean()
    var = log_returns.var()  
    stdev = log_returns.std()  
    drift = mean - (0.5 * var)
    
    # Initialize Simulation Variables
    intervals = 252 * years
    iterations = 10
    
    # Do the stats math Future Returns = drift + shock
    daily_returns = np.exp(drift.values + stdev.values * norm.ppf(np.random.rand(intervals, iterations)))
    
    S0 = stock_data.iloc[-1]
    
    # Set up future stock values array starting with the last value of the known prices
    price_list = np.zeros_like(daily_returns)
    price_list[0] = S0
    
    for t in range(1, intervals):
        price_list[t] = price_list[t-1] * daily_returns[t]
    
    # Plot Graph
    #plot_MonteCarlo(price_list)
    
    # Save Graph
    save_MonteCarlo(price_list)

# Function to save graph
def save_MonteCarlo(price_list):
    
    plt.style.use('Solarize_Light2')    
    plt.figure(figsize=(10,6))
    
    plt.title(" Geometric Brownian Motion Monte Carlo Price Simulation")
    plt.ylabel("Price of Stock ($)")
    plt.xlabel("Time (Trading Days)")
    
    plt.plot(price_list)
    plt.savefig("temp.png")
    plt.close()
    
# Function to plot graph
def plot_MonteCarlo(price_list):
    
    plt.style.use('Solarize_Light2')    
    plt.figure(figsize=(10,6))
    
    plt.title(" Geometric Brownian Motion Monte Carlo Price Simulation")
    plt.ylabel("Price of Stock ($)")
    plt.xlabel("Time (Trading Days)")
    
    plt.plot(price_list)
    plt.show()
    
get_monte_carlo("AMZN", '2007-1-1', '2020-1-1', 8)