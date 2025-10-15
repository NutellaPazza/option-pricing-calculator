"""
Greeks calculations for option pricing.
Implements first and second order sensitivities.
"""

import numpy as np
from scipy.stats import norm
from typing import Dict


class GreeksCalculator:
    """
    Calculator for option Greeks (sensitivities).
    
    Greeks measure the sensitivity of option prices to various parameters:
    - Delta: Sensitivity to underlying price
    - Gamma: Sensitivity of delta to underlying price
    - Theta: Sensitivity to time decay
    - Vega: Sensitivity to volatility
    - Rho: Sensitivity to interest rate
    """
    
    @staticmethod
    def calculate_all_greeks(
        spot: float,
        strike: float,
        time_to_maturity: float,
        risk_free_rate: float,
        volatility: float,
        option_type: str
    ) -> Dict[str, float]:
        """
        Calculate all Greeks for an option.
        
        Returns:
            Dict containing Delta, Gamma, Theta, Vega, and Rho
        """
        calc = GreeksCalculator()
        
        return {
            'Delta': calc.delta(
                spot, strike, time_to_maturity, 
                risk_free_rate, volatility, option_type
            ),
            'Gamma': calc.gamma(
                spot, strike, time_to_maturity, 
                risk_free_rate, volatility
            ),
            'Theta': calc.theta(
                spot, strike, time_to_maturity, 
                risk_free_rate, volatility, option_type
            ),
            'Vega': calc.vega(
                spot, strike, time_to_maturity, 
                risk_free_rate, volatility
            ),
            'Rho': calc.rho(
                spot, strike, time_to_maturity, 
                risk_free_rate, volatility, option_type
            )
        }
    
    def delta(
        self,
        spot: float,
        strike: float,
        time_to_maturity: float,
        risk_free_rate: float,
        volatility: float,
        option_type: str
    ) -> float:
        """
        Calculate Delta: ∂V/∂S
        Measures the rate of change of option value with respect to spot price.
        
        Call Delta: N(d1)
        Put Delta: N(d1) - 1
        
        Range: [0, 1] for calls, [-1, 0] for puts
        """
        d1 = self._calculate_d1(
            spot, strike, time_to_maturity, risk_free_rate, volatility
        )
        
        if option_type.lower() == 'call':
            return float(norm.cdf(d1))
        else:  # put
            return float(norm.cdf(d1) - 1)
    
    def gamma(
        self,
        spot: float,
        strike: float,
        time_to_maturity: float,
        risk_free_rate: float,
        volatility: float
    ) -> float:
        """
        Calculate Gamma: ∂²V/∂S²
        Measures the rate of change of delta with respect to spot price.
        
        Formula: φ(d1) / (S * σ * √T)
        where φ is the standard normal PDF
        
        Gamma is the same for calls and puts.
        Always positive.
        """
        d1 = self._calculate_d1(
            spot, strike, time_to_maturity, risk_free_rate, volatility
        )
        
        return (
            norm.pdf(d1) / 
            (spot * volatility * np.sqrt(time_to_maturity))
        )
    
    def theta(
        self,
        spot: float,
        strike: float,
        time_to_maturity: float,
        risk_free_rate: float,
        volatility: float,
        option_type: str
    ) -> float:
        """
        Calculate Theta: ∂V/∂t
        Measures the rate of change of option value with respect to time.
        Typically expressed as the change per day (divide by 365).
        
        Usually negative for long positions (time decay).
        """
        d1 = self._calculate_d1(
            spot, strike, time_to_maturity, risk_free_rate, volatility
        )
        d2 = d1 - volatility * np.sqrt(time_to_maturity)
        
        # Common term
        term1 = -(spot * norm.pdf(d1) * volatility) / (2 * np.sqrt(time_to_maturity))
        
        if option_type.lower() == 'call':
            term2 = risk_free_rate * strike * np.exp(-risk_free_rate * time_to_maturity) * norm.cdf(d2)
            theta = term1 - term2
        else:  # put
            term2 = risk_free_rate * strike * np.exp(-risk_free_rate * time_to_maturity) * norm.cdf(-d2)
            theta = term1 + term2
        
        # Convert to per-day theta (divide by 365)
        return theta / 365
    
    def vega(
        self,
        spot: float,
        strike: float,
        time_to_maturity: float,
        risk_free_rate: float,
        volatility: float
    ) -> float:
        """
        Calculate Vega: ∂V/∂σ
        Measures the rate of change of option value with respect to volatility.
        
        Formula: S * φ(d1) * √T
        
        Vega is the same for calls and puts.
        Always positive.
        Expressed as change per 1% change in volatility (divide by 100).
        """
        d1 = self._calculate_d1(
            spot, strike, time_to_maturity, risk_free_rate, volatility
        )
        
        # Vega per 1% change in volatility
        return spot * norm.pdf(d1) * np.sqrt(time_to_maturity) / 100
    
    def rho(
        self,
        spot: float,
        strike: float,
        time_to_maturity: float,
        risk_free_rate: float,
        volatility: float,
        option_type: str
    ) -> float:
        """
        Calculate Rho: ∂V/∂r
        Measures the rate of change of option value with respect to interest rate.
        
        Expressed as change per 1% change in interest rate (divide by 100).
        """
        d1 = self._calculate_d1(
            spot, strike, time_to_maturity, risk_free_rate, volatility
        )
        d2 = d1 - volatility * np.sqrt(time_to_maturity)
        
        if option_type.lower() == 'call':
            rho = (
                strike * time_to_maturity * 
                np.exp(-risk_free_rate * time_to_maturity) * 
                norm.cdf(d2)
            )
        else:  # put
            rho = (
                -strike * time_to_maturity * 
                np.exp(-risk_free_rate * time_to_maturity) * 
                norm.cdf(-d2)
            )
        
        # Rho per 1% change in interest rate
        return rho / 100
    
    def _calculate_d1(
        self,
        spot: float,
        strike: float,
        time_to_maturity: float,
        risk_free_rate: float,
        volatility: float
    ) -> float:
        """Calculate d1 parameter for Black-Scholes formula."""
        numerator = (
            np.log(spot / strike) + 
            (risk_free_rate + 0.5 * volatility ** 2) * time_to_maturity
        )
        denominator = volatility * np.sqrt(time_to_maturity)
        return numerator / denominator
