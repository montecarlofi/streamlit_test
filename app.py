import pandas as pd
import streamlit as st
from qfin.simulations import GeometricBrownianMotion
#from "https://github.com/RomanMichaelPaolucci/Q-Fin" import GeometricBrownianMotion

st.write("My First Streamlit Web App")

df = pd.DataFrame({"one": [1, 2, 3], "two": [4, 5, 6], "three": [7, 8, 9]})
st.write(df)
