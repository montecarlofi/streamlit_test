import pandas as pd
import streamlit as st
from random import random
#from qfin.simulations import GeometricBrownianMotion
#from "https://github.com/RomanMichaelPaolucci/Q-Fin" import GeometricBrownianMotion

st.write("Monte Carlo . fi")

# df = pd.DataFrame({"one": [1, 2, 3], "two": [4, 5, 6], "three": [7, 8, 9]})
# st.write(df)

with st.echo(code_location='below'):
  chart_data = pd.DataFrame()
  
  S = st.slider('Initial Stock Price: ', 0, 100, 50, 5)
  mu = st.slider('Drift %: ', 0, 30, 0, 1)
  sigma = st.slider('Volatility %: ', 0, 30, 15, 1)
  T = st.slider('T (mos): ', 0, 100, 50, 10)
  n = st.slider('Simulations: ', 0, 100, 50, 10) 
  
  # 100 - initial underlying asset price
  # 0 - underlying asset drift (mu)
  # .3 - underlying asset volatility
  # 1/52 - time steps (dt)
  # 1 - time to maturity (annum)
  # gbm = GeometricBrownianMotion(100, 0, .3, 1/52, 1)
 
  for i in range(n):
    #chart_data[str(i)] = GeometricBrownianMotion(S, mu/100, sigma/100, 1/252, T/12).simulated_path
    #sample = np.random.normal(0, 0.1, 10)
    series = []
    for a in range(0,9):
      number = random()
      series.append(number)
    chart_data[str(i)] = series
    #[1.04, 1.07, 1.11]
    
  st.line_chart(chart_data)
