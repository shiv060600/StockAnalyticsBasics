import numpy as np
from scipy.stats import norm

def get_put_price(S,K,sigma,T,r):
    PVK = K*np.exp(-1*r*T)
    d1 = (np.log(S/K)+(r + (sigma*sigma/2)*T))/(sigma * np.sqrt(T))
    d2 = d1 - (sigma * np.sqrt(T))
    P = PVK * norm.cdf(-1 * d2) - S * norm.cdf(-1*d1)
    return P

if __name__ == "__main__":
    S = 100
    K = 100
    simga = 0.2 
    T = 1
    r = 0.05
    res = get_put_price(S,K,simga,T,r)
    print(res)


