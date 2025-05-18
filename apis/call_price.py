import numpy as np
from scipy.stats import norm

def get_call_price(S,K,sigma,T,r):
    d1 = (1/sigma*np.sqrt(T))*(np.log(S/K) +(r + (sigma * sigma / 2)*T))
    d2 = d1 - sigma*np.sqrt(T)
    PVK = K * np.exp(-1*r*T)
    C = S * norm.cdf(d1) - PVK * norm.cdf(d2)
    return C

