import warnings
import numpy as np

from typing import Optional

from scipy.stats import norm
from deribit_arb_app.enums.enum_option_type import EnumOptionType

    ##################################################
    # Service Implements Black Scholes Merton Pricer #
    ##################################################

class ServicePricerBlackScholes():
    """
    Base Formulae:

    The Black-Scholes formulas for call and put options pricing are determined 
    using d1 and d2, which are intermediaries capturing aspects of the option's 
    moneyness, time to expiration, risk-free rate, and volatility. The Vega of 
    an option represents the rate of change of the option's price with respect 
    to changes in the underlying asset's volatility, and it's instrumental in 
    adjusting our volatility guess in the Newton-Raphson iteration.

    Newton-Raphson Iteration:

    Initial Guess: 
    Your method starts with an initial volatility guess, sigma, denoted by h.

    Iteration Mechanism: 
    You then employ an iterative loop for a maximum of 200 cycles 
    (MAX_ITERATIONS). In each cycle:
    - Depending on the option type (call or put), the option price is calculated 
    using the current volatility guess.
    - The difference between this calculated option price and the actual market 
    price (target_value) is determined.
    - The Vega of the option at the current volatility guess is also computed.
    - The difference between the calculated option price and market price is 
    then divided by this Vega value to give an adjustment to the volatility 
    guess.
    - The adjustment is added to the current guess to yield the next guess for 
    implied volatility.

    Convergence Criteria: 
    The iterations proceed until the difference between the calculated option 
    price and the market price is smaller than a set precision (PRECISION = 
    1.0e-10) or the maximum number of iterations is reached.
    """

    N = norm.cdf


    def bs_put(self, S, K, T, r, vol):
        d1 = round((np.log(S/K)+(r+0.5*vol*vol)*T)/(vol*np.sqrt(T)),8)
        d2 = round((d1-vol*np.sqrt(T)),5)
        return round((np.exp(-r*T)*K*norm.cdf(-d2)-S*norm.cdf(-d1)),8)
    
    
    def bs_call(self, S, K, T, r, vol):
        d1 = round((np.log(S/K)+(r+0.5*vol*vol)*T)/(vol*np.sqrt(T)),8)
        d2 = round((d1-vol*np.sqrt(T)),8)
        return round((S*norm.cdf(d1)-np.exp(-r*T)*K*norm.cdf(d2)),8)


    def bs_vega(self, S, K, T, r, sigma):
        d1 = round((np.log(S/K)+(r+0.5*sigma*sigma)*T)/(sigma*np.sqrt(T)),8)
        return round((S*norm.pdf(d1)*np.sqrt(T)),8)


    def find_vol(self, target_value, S, K, T, r, h,option_type, *args) -> Optional[float]:
        MAX_ITERATIONS = 200
        PRECISION = 1.0e-10
        sigma = h
        try:
            for i in range(0, MAX_ITERATIONS):
                if option_type == EnumOptionType.CALL.value:
                    price = self.bs_call(S, K, T, r, sigma)
                else:
                    price = self.bs_put(S, K, T, r, sigma)
                vega = self.bs_vega(S, K, T, r, sigma)
                diff = target_value - price  # our root
                if (abs(diff) < PRECISION):
                    return sigma
                if vega == 0:
                    return np.nan
                sigma = sigma + diff/vega # f(x) / f'(x)
        except Exception as e:
            return np.nan
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        return sigma # value wasn't found, return best guess so far