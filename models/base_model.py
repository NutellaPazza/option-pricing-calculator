"""
Base abstract class for all option pricing models.
Defines the common interface that all pricing models must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class OptionPricingModel(ABC):
    """
    Abstract base class for option pricing models.
    All concrete pricing models must inherit from this class and implement
    the abstract methods.
    """
    
    @abstractmethod
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
        Calculate the option price.
        
        Args:
            spot: Current spot price of the underlying asset
            strike: Strike price of the option
            time_to_maturity: Time to expiration in years
            risk_free_rate: Risk-free interest rate (annualized)
            volatility: Volatility of the underlying asset (annualized)
            option_type: Type of option ('call' or 'put')
        
        Returns:
            float: The calculated option price
        
        Raises:
            ValueError: If input parameters are invalid
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """
        Return information about the pricing model.
        
        Returns:
            Dict containing:
                - name: Model name
                - type: Model type (Analytical, Simulation, Discrete)
                - description: Brief description
                - assumptions: List of key assumptions
        """
        pass
    
    def validate_inputs(
        self,
        spot: float,
        strike: float,
        time_to_maturity: float,
        risk_free_rate: float,
        volatility: float,
        option_type: str
    ) -> bool:
        """
        Validate input parameters for option pricing.
        Common validation logic shared across all models.
        
        Args:
            spot: Current spot price
            strike: Strike price
            time_to_maturity: Time to maturity
            risk_free_rate: Risk-free rate
            volatility: Volatility
            option_type: 'call' or 'put'
        
        Returns:
            bool: True if all inputs are valid
        
        Raises:
            ValueError: If any input is invalid with descriptive message
        """
        if spot <= 0:
            raise ValueError(f"Spot price must be positive. Got: {spot}")
        
        if strike <= 0:
            raise ValueError(f"Strike price must be positive. Got: {strike}")
        
        if time_to_maturity <= 0:
            raise ValueError(
                f"Time to maturity must be positive. Got: {time_to_maturity}"
            )
        
        if volatility <= 0:
            raise ValueError(f"Volatility must be positive. Got: {volatility}")
        
        if risk_free_rate < -0.1 or risk_free_rate > 0.5:
            raise ValueError(
                f"Risk-free rate must be between -0.1 and 0.5. Got: {risk_free_rate}"
            )
        
        if option_type.lower() not in ['call', 'put']:
            raise ValueError(
                f"Option type must be 'call' or 'put'. Got: {option_type}"
            )
        
        return True
    
    def _get_option_type(self, option_type: str) -> str:
        """
        Normalize option type to lowercase.
        
        Args:
            option_type: Option type string
        
        Returns:
            str: Normalized option type ('call' or 'put')
        """
        return option_type.lower().strip()
