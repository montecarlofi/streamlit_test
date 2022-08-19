#from hashlib import new
import pandas as pd
import streamlit as st
from random import random
#import matplotlib.pyplot as plt
import numpy as np
import math
#from numpy.random import default_rng

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
        if volatility == 0:
            movement = rate_per_period # No volatility = no randomness.
        else:
            random_number = random()
            # Remap to 1.0 +/- volatility. E.g., a +50% movement on a +-30% volatility range becomes 1.15.
            movement = 1 + (((random_number * 2) - 1) * volatility)
            # Re-calculate to natural rate over periods.
            movement = np.e**(np.log(movement)/periods) + (rate_per_period - 1)

            # Remap 0.0-1.0 to 0.5-1.5
            #movement = 1 + ((random_number * 2) - 1)
            #movement = (np.e**(np.log(movement)/periods) * volatility) + (rate_per_period - 1)

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


### Initial setup ###
size_of_history = 252*50
#history, largest, smallest = get_random_series(rate, volatility, size_of_history, periods_per_rate)

st.title("R A N D O M . W A L K")

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: magenta;'>Random walk</h1>", unsafe_allow_html=True)


#with st.echo(code_location="below"):
simulated_paths = []
n_simulations = st.slider("Number of simulations", 1, 100, 3, 1)
volatility = st.slider("Volatility", 0, 30, 15, 1) / 100
trading_periods_per_year = st.slider("Trading days per year", 2, 252, 12, 1)
years = st.slider("Years of investing", 1, 60, 20, 1)
bias = st.slider("Yearly expected return rate", 0.90, 1.10, 1.07, 0.01)

size_of_history = trading_periods_per_year*50
history, largest, smallest = get_random_series(bias, volatility, size_of_history, trading_periods_per_year)

charted_years = []

for i in range(n_simulations):
    resampled = resample(history, trading_periods_per_year * years)
    geo_series = geometric_series(resampled, 1)
    simulated_paths.append(geo_series)

rearranged = pd.DataFrame()
for i in range(0, len(simulated_paths)):
    rearranged[i] = simulated_paths[int(i)]

st.line_chart(rearranged)
#st.dataframe(pd.DataFrame(resampled))
#st.dataframe(resampled)


# Count simulation paths that ended up below starting point.
count = 0
for i in range(0, len(simulated_paths)):
    last_value = simulated_paths[i][-1]
    #last_value = round(last_value, 4)
    if last_value < 1:
        count += 1
    #st.write(last_value)
message = "Lives in which you got wiped out: {}.".format(count)
st.write(message)
