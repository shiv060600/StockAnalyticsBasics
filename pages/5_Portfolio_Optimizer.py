import streamlit as st
import numpy as np

st.markdown("<h1 style = 'text-align : center;'> Portfolio Oprimizer </h1>",unsafe_allow_html=True)

number_unique_stocks = st.number_input(label = 'Enter the number of Stocks you own')
