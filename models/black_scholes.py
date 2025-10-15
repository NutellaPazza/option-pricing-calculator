"""
Black-Scholes option pricing model.
Implements the classic closed-form solution for European options.
"""

import numpy as np
from scipy.stats import norm
from typing import Dict, Any

from models.base_model import OptionPricingModel


class BlackScholesModel(OptionPricingModel):
    """
    Black-Scholes analytical pricing model for European options.
    
    Assumptions:
    - Constant volatility
    - Constant risk-free rate
    - No dividends
    - European exercise only
    - Log-normal distribution of returns
    """
    
    def calculate_price(
        self,
        spot: float,
        strike: float,
        time_to_maturity: float,
        risk_free_rate: float,
        volatility: float,
        option_type: str
    ) -> float:
        """
        Calculate option price using Black-Scholes formula.
        
        Formula:
        Call: S*N(d1) - K*exp(-r*T)*N(d2)
        Put: K*exp(-r*T)*N(-d2) - S*N(-d1)
        
        where:
        d1 = [ln(S/K) + (r + σ²/2)*T] / (σ*√T)
        d2 = d1 - σ*√T
        """
        # Validate inputs
        self.validate_inputs(
            spot, strike, time_to_maturity, 
            risk_free_rate, volatility, option_type
        )
        
        # Normalize option type
        option_type = self._get_option_type(option_type)
        
        # Calculate d1 and d2
        d1 = self._calculate_d1(
            spot, strike, time_to_maturity, risk_free_rate, volatility
        )
        d2 = self._calculate_d2(d1, volatility, time_to_maturity)
        
        # Calculate option price based on type
        if option_type == 'call':
            price = self._calculate_call_price(
                spot, strike, time_to_maturity, risk_free_rate, d1, d2
            )
        else:  # put
            price = self._calculate_put_price(
                spot, strike, time_to_maturity, risk_free_rate, d1, d2
            )
        
        return price
    
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
    
    def _calculate_d2(
        self,
        d1: float,
        volatility: float,
        time_to_maturity: float
    ) -> float:
        """Calculate d2 parameter for Black-Scholes formula."""
        return d1 - volatility * np.sqrt(time_to_maturity)
    
    def _calculate_call_price(
        self,
        spot: float,
        strike: float,
        time_to_maturity: float,
        risk_free_rate: float,
        d1: float,
        d2: float
    ) -> float:
        """Calculate call option price."""
        return (
            spot * norm.cdf(d1) - 
            strike * np.exp(-risk_free_rate * time_to_maturity) * norm.cdf(d2)
        )
    
    def _calculate_put_price(
        self,
        spot: float,
        strike: float,
        time_to_maturity: float,
        risk_free_rate: float,
        d1: float,
        d2: float
    ) -> float:
        """Calculate put option price."""
        return (
            strike * np.exp(-risk_free_rate * time_to_maturity) * norm.cdf(-d2) - 
            spot * norm.cdf(-d1)
        )
    
    def get_model_info(self) -> Dict[str, Any]:
        """Return information about the Black-Scholes model."""
        return {
            'name': 'Black-Scholes',
            'type': 'Analytical',
            'description': 'Closed-form solution for European options',
            'assumptions': [
                'Constant volatility',
                'Constant risk-free rate',
                'No dividends',
                'European exercise only',
                'Log-normal distribution of returns',
                'No transaction costs',
                'Continuous trading'
            ],
            'supports_american': False,
            'year_introduced': 1973,
            'authors': ['Fischer Black', 'Myron Scholes', 'Robert Merton']
        }
    
    def get_d1_d2(
        self,
        spot: float,
        strike: float,
        time_to_maturity: float,
        risk_free_rate: float,
        volatility: float
    ) -> tuple[float, float]:
        """
        Get d1 and d2 parameters (useful for Greeks calculation).
        
        Returns:
            tuple: (d1, d2)
        """
        d1 = self._calculate_d1(
            spot, strike, time_to_maturity, risk_free_rate, volatility
        )
        d2 = self._calculate_d2(d1, volatility, time_to_maturity)
        return d1, d2
