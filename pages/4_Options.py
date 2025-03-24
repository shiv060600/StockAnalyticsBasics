import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
from apis.get_current_price import get_current_price
from apis.put_price import get_put_price
from apis.call_price import get_call_price

st.markdown("<h1 style = 'text-align : center;'> Put Call Parity </h1>",unsafe_allow_html=True)

use_real_data = st.sidebar.toggle("Use Realtime Stock Data",value= False)

st.sidebar.header("Options Parameters")
option_type = st.sidebar.radio("Option Type", ["Call", "Put"])

today = datetime.datetime.now().date()
expiry_date = st.sidebar.date_input("Expiration Date")

@st.cache_data
def get_current_price_data(ticker):
    return get_current_price(ticker)

if expiry_date < today:
    st.error("You cannot go back in time! Pick another date.")

# Add option theory explanations based on selected option type
if option_type == "Call":
    st.markdown("""
    ## Call Option Basics
    
    A call option gives the holder the right (but not obligation) to buy an underlying asset at a specified strike price on or before expiration.
    

    $$ Call Payoff = \max(S_T - K, 0) $$
    
    **Option Premium Formula (Black-Scholes):** $$ C = S_0 \cdot N(d_1) - K \cdot e^{-rT} \cdot N(d_2) $$
    
    Where:
    - $S_T$ is the price of the underlying asset at expiration
    - $S_0$ is the current price of the underlying asset
    - $K$ is the strike price
    - $N(d)$ is the cumulative distribution function of standard normal distribution
    - $r$ is the risk-free interest rate
    - $T$ is the time to expiration in years
    """)
elif option_type == "Put":
    st.markdown("""
    ## Put Option Basics
    
    A put option gives the holder the right (but not obligation) to sell an underlying asset at a specified strike price on or before expiration.
    
    **Put Option Payoff:**
    $$ Put Payoff = \max(K - S_T, 0) $$
    
    **Option Premium Formula (Black-Scholes):** $$ P = K \cdot e^{-rT} \cdot N(-d_2) - S_0 \cdot N(-d_1) $$
    
    Where:
    - $S_T$ is the price of the underlying asset at expiration
    - $S_0$ is the current price of the underlying asset
    - $K$ is the strike price
    - $N(d)$ is the cumulative distribution function of standard normal distribution
    - $r$ is the risk-free interest rate
    - $T$ is the time to expiration in years
    """)

T = (expiry_date - today).days / 365.0

def plot_option_payoff_price(S, K, r, sigma, T, option_type):
    price_range = np.linspace(max(0.7 * S, 1), 1.3 * S, 100)
    payoffs = []
    prices = []
    
    for price in price_range:
        if option_type == "Call":
            payoff = np.maximum(price - K, 0)
            option_price = get_call_price(price, K, T, r, sigma)
        else:
            payoff = np.maximum(K - price, 0)
            option_price = get_put_price(price, K, T, r, sigma)
        
        payoffs.append(payoff)
        prices.append(option_price)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=price_range, 
        y=payoffs, 
        mode='lines', 
        name='Payoff at Expiration',
        line=dict(color='blue', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=price_range, 
        y=prices, 
        mode='lines', 
        name='Option Price Now',
        line=dict(color='red', width=2)
    ))
    
    fig.add_shape(
        type="line", line=dict(dash="dash", color="gray"),
        x0=K, y0=0, x1=K, y1=max(max(payoffs), max(prices)) * 1.1
    )
    
    fig.update_layout(
        title=f"{option_type} Option Analysis",
        xaxis_title="Underlying Price",
        yaxis_title="Value",
        legend_title="",
        hovermode="x unified"
    )
    
    return fig

if not use_real_data:
    K = st.sidebar.number_input("Strike Price", value=100.0)
    sigma = st.sidebar.slider("Volatility", min_value = 0.0, max_value = 1.0, step= 0.05, value=0.2)
    S = st.sidebar.number_input("Underlying Asset Price", value=100.0)
    r = st.sidebar.slider("Interest Rate", min_value = 0.01, max_value= 0.1, step=0.01, value=0.05)
    
    if S > 0 and K > 0 and T > 0:
        if option_type == "Call":
            option_value = get_call_price(S, K, T, r, sigma)
            st.write(f"Call option price: ${option_value:.2f}")
        else:
            option_value = get_put_price(S, K, T, r, sigma)
            st.write(f"Put option price: ${option_value:.2f}")
        
        fig = plot_option_payoff_price(S, K, r, sigma, T, option_type)
        st.plotly_chart(fig, use_container_width=True)
else:
    ticker = st.sidebar.text_input("Enter Ticker","AAPL")
    current_prices = get_current_price_data(ticker)
    current_price_float = round(current_prices['Close'],3)
    K = st.sidebar.number_input("Strike Price", value=current_price_float)
    
    # For real data we still need volatility and risk-free rate
    sigma = st.sidebar.slider("Implied Volatility", min_value=0.0, max_value=1.0, step=0.05, value=0.2)
    r = st.sidebar.slider("Risk-Free Rate", min_value=0.01, max_value=0.1, step=0.01, value=0.05)
    
    if K > 0 and T > 0:
        if option_type == "Call":
            option_value = get_call_price(current_price_float, K, T, r, sigma)
            st.write(f"Call option price: ${option_value:.2f}")
            st.write(f"Current price is ${current_price_float}")
        else:
            option_value = get_put_price(current_price_float, K, T, r, sigma)
            st.write(f"Put option price: ${option_value:.2f}")
            st.write(f"Current price is ${current_price_float}")
        
        fig = plot_option_payoff_price(current_price_float, K, r, sigma, T, option_type)
        st.plotly_chart(fig, use_container_width=True)









