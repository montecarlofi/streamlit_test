import pandas as pd
#from hashlib import new
from random import random
import streamlit as st
import numpy as np
import math
#from numpy.random import default_rng

st.write("Monte Carlo . fi")

chart_data = pd.DataFrame()

S = st.slider('Initial Stock Price: ', 0, 100, 50, 5)
mu = st.slider('Drift %: ', 0, 30, 0, 1)
sigma = st.slider('Volatility %: ', 0, 30, 15, 1)
T = st.slider('T (mos): ', 0, 100, 50, 10)
n = st.slider('Simulations: ', 0, 100, 50, 10) 


def get_historical_data(market):
    # market choice and where and how to pull data from it is not yet implemented
    # so making it randomly for now
    dataset = []
    for n in range(0,5):
        random_number = random()
        dataset.append(random_number)
    return dataset

def get_random_series(average_rate, volatility, n, periods): # periods would typically be trading days per year, but could also be months.
    if average_rate == "":
        average_rate = 1
    rate_per_period = np.e**(np.log(average_rate)/periods)
    series = []
    largest = 1 # Should it be ""?
    smallest = 1
    for i in range(0, n):
        random_number = random()
        # Rescale according to volatility: New value = 1 +/- volatility. E.g., 1 + 0.15.
        movement = 1 + (((random_number * 2) - 1) * volatility)
        # Re-calculate to natural rate over periods.
        movement = np.e**(np.log(movement)/periods) + (rate_per_period - 1)
        movement = math.ceil(movement*10000)/10000 # rounds up to nearest .0000
        if movement>largest:
            largest=movement
        if movement<smallest:
            smallest=movement
        series.append(movement)
    return series, largest, smallest


def resample(some_dataset, n):
    resampled = []
    for a in range(0, n):
        randomly_selected_value = np.random.choice(some_dataset)
        resampled.append(randomly_selected_value)
    return resampled

def geometric_series(rates_of_movements, start_value):
    value = start_value
    series = []
    for i in rates_of_movements:
        value = value * rates_of_movements[int(i)]
        series.append(value)
    return series


### User variables ###
volatility = 0.3
rate = 1.07
periods_per_rate = 252 # E.g., trading days per yearly rate.
size_of_each_resample = 252 # How many days do I want for my sample?
years = 4


### Script ###
size_of_history = 252*50
history, largest, smallest = get_random_series(rate, volatility, size_of_history, periods_per_rate)
#history = get_historical_data("Nor_Stock_Market") # market choice not yet implemented
#print("History ", history, "\n")
#print("Largest: ", largest, "\nSmallest: ", smallest, "\n")

chart = []
start_value = 1
resampled = resample(history, size_of_each_resample)
#print("Resampled ", resampled)
geo = geometric_series(resampled, start_value)
chart.append(geo)
highest_index = len(geo) - 1
last_value = geo[highest_index]
for i in range(1, years):
    resampled = resample(history, size_of_each_resample)
    row = geometric_series(resampled, last_value)
    highest_index = len(geo) - 1
    last_value = row[highest_index]
    #chart[i] = geo
    chart.append(row)

#print("Chart \n ", chart[1])

#figure, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, sharex=True)
#figure, (ax1, axall, axRndDist) = plt.subplots(3, constrained_layout = True)
#plt.xticks(np.arange(0, len(x), 10))

#ax1.set_title("Year 1")
x1_index = []
x1_index.extend(range(0,len(chart[0])))
for i in range(0, len(chart)):
    #ax1.plot(x1_index, chart[i])
    pass

#axall.set_title("All {} years".format(years))
paths_combined = []
for i in range(0, len(chart)):
    temp_series = chart[i]
    for k in range(0, len(temp_series)):
        paths_combined.append(temp_series[int(k)])
# Works:
#paths_combined = []
#for i in range(0, len(chart)):
#    paths_combined.extend(chart[int(i)])
x_index = []
x_index.extend(range(0,len(paths_combined)))
#axall.plot(x_index, paths_combined, 'r')


#chart_data[str(i)] = chart[0]
st.line_chart(chart)
