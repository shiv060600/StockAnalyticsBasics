import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
from apis.get_current_price import get_current_price
from apis.put_price import get_put_price
from apis.call_price import get_call_price

st.markdown("<h1 style = 'text-align : center;'> Put Call Parity </h1>",unsafe_allow_html=True)


st.sidebar.header("Options Parameters")
option_type = st.sidebar.radio("Option Type", ["Call", "Put"])

today = datetime.datetime.now().date()
expiry_date = st.sidebar.date_input("Expiration Date", (datetime.datetime.now().date()+datetime.timedelta(days = 1)))

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
    price_range = np.linspace(0.5 * S, 1.5 * S, 20)
    payoffs = []

    if option_type == "Call":
        initial_premium = get_call_price(S, K, sigma, T, r)
    else:
        initial_premium = get_put_price(S, K, sigma, T, r)
    
    for price in price_range:
        # Calculate option payoff at expiration
        if option_type == "Call":
            payoff = (max(price - K,0) - initial_premium)
        else:
            payoff = (max(K - price, 0) - initial_premium)
                
            
        payoffs.append(payoff)
    

    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=price_range, 
        y=payoffs, 
        mode='lines', 
        name='Option Price Now',
        line=dict(color='red', width=2)
    ))
    
    fig.add_vline(
        x = K,line_color = 'white',line_width = 2,line_dash = "dash"
    )

    fig.add_hline(
        y=0, line_color="grey", line_width=2 , line_dash =  "dash"
        )
    
    fig.update_layout(
        title=f"{option_type} Option Analysis",
        xaxis_title="Underlying Price",
        yaxis_title="P/L",
        legend_title="",
        hovermode="x unified"
    )
    
    return fig

if option_type == "Put":
    S = st.sidebar.number_input("Underlying Asset Price", value=90.0)
else:
    S = st.sidebar.number_input("Underlying Asset Price", value=120.0)

K = st.sidebar.number_input("Strike Price", value=100.0)

sigma = st.sidebar.slider("Volatility", min_value = 0.0, max_value = 1.0, step= 0.05, value=0.2)

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










