"""
Monte Carlo simulation model for option pricing.
Uses geometric Brownian motion to simulate price paths.
"""

import numpy as np
from typing import Dict, Any, Optional
from .base_model import OptionPricingModel


class MonteCarloModel(OptionPricingModel):
    """
    Monte Carlo simulation model for European option pricing.
    
    This model simulates multiple price paths for the underlying asset
    using geometric Brownian motion and calculates the option payoff
    at expiration for each path.
    
    Advantages:
        - Works for complex payoff structures
        - Easy to extend for path-dependent options
        - Can handle multiple stochastic factors
    
    Disadvantages:
        - Computationally intensive
        - Results have statistical uncertainty
        - Not suitable for American options (without modifications)
    """
    
    def __init__(
        self,
        num_simulations: int = 100000,
        num_steps: int = 252,
        seed: Optional[int] = None,
        antithetic: bool = True
    ):
        """
        Initialize Monte Carlo pricing model.
        
        Args:
            num_simulations: Number of price paths to simulate
            num_steps: Number of time steps per simulation (252 = daily for 1 year)
            seed: Random seed for reproducibility (None for random)
            antithetic: Use antithetic variates for variance reduction
        """
        self.num_simulations = num_simulations
        self.num_steps = num_steps
        self.seed = seed
        self.antithetic = antithetic
        
        # Set random seed if provided
        if seed is not None:
            np.random.seed(seed)
    
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
        Calculate option price using Monte Carlo simulation.
        
        The model simulates stock price paths using geometric Brownian motion:
        dS = μ*S*dt + σ*S*dW
        
        Where:
        - S is the stock price
        - μ is the drift (risk-free rate)
        - σ is the volatility
        - dW is a Wiener process (random walk)
        
        Args:
            spot: Current spot price of underlying asset
            strike: Strike price of the option
            time_to_maturity: Time to expiration in years
            risk_free_rate: Risk-free interest rate (annualized)
            volatility: Volatility of underlying asset (annualized)
            option_type: Type of option ('call' or 'put')
        
        Returns:
            float: Estimated option price
        
        Raises:
            ValueError: If input parameters are invalid
        """
        # Validate inputs
        self.validate_inputs(
            spot, strike, time_to_maturity,
            risk_free_rate, volatility, option_type
        )
        
        option_type = self._get_option_type(option_type)
        
        # Calculate time step
        dt = time_to_maturity / self.num_steps
        
        # Determine number of simulations (double if using antithetic variates)
        num_sims = self.num_simulations // 2 if self.antithetic else self.num_simulations
        
        # Generate random numbers for Wiener process
        # Shape: (num_steps, num_simulations)
        random_numbers = np.random.standard_normal((self.num_steps, num_sims))
        
        if self.antithetic:
            # Create antithetic paths (negative of original random numbers)
            # This reduces variance by ensuring symmetric paths
            random_numbers = np.concatenate([random_numbers, -random_numbers], axis=1)
        
        # Initialize price paths
        # Start all paths at the current spot price
        price_paths = np.zeros((self.num_steps + 1, random_numbers.shape[1]))
        price_paths[0] = spot
        
        # Simulate price paths using geometric Brownian motion
        # S(t+dt) = S(t) * exp((r - 0.5*σ²)*dt + σ*sqrt(dt)*Z)
        # where Z ~ N(0,1)
        
        drift = (risk_free_rate - 0.5 * volatility**2) * dt
        diffusion = volatility * np.sqrt(dt)
        
        for t in range(1, self.num_steps + 1):
            price_paths[t] = price_paths[t-1] * np.exp(
                drift + diffusion * random_numbers[t-1]
            )
        
        # Get final prices at expiration
        final_prices = price_paths[-1]
        
        # Calculate payoffs at expiration
        if option_type == 'call':
            payoffs = np.maximum(final_prices - strike, 0)
        else:  # put
            payoffs = np.maximum(strike - final_prices, 0)
        
        # Calculate option price as discounted expected payoff
        option_price = np.exp(-risk_free_rate * time_to_maturity) * np.mean(payoffs)
        
        return float(option_price)
    
    def calculate_price_with_confidence(
        self,
        spot: float,
        strike: float,
        time_to_maturity: float,
        risk_free_rate: float,
        volatility: float,
        option_type: str,
        confidence_level: float = 0.95
    ) -> Dict[str, float]:
        """
        Calculate option price with confidence interval.
        
        Args:
            spot: Current spot price
            strike: Strike price
            time_to_maturity: Time to maturity in years
            risk_free_rate: Risk-free rate
            volatility: Volatility
            option_type: 'call' or 'put'
            confidence_level: Confidence level (e.g., 0.95 for 95%)
        
        Returns:
            Dict with:
                - price: Estimated option price
                - std_error: Standard error of the estimate
                - lower_bound: Lower confidence bound
                - upper_bound: Upper confidence bound
        """
        # Run multiple batches to estimate standard error
        num_batches = 10
        batch_size = self.num_simulations // num_batches
        
        batch_prices = []
        
        for _ in range(num_batches):
            # Temporarily set num_simulations for batch
            original_sims = self.num_simulations
            self.num_simulations = batch_size
            
            price = self.calculate_price(
                spot, strike, time_to_maturity,
                risk_free_rate, volatility, option_type
            )
            batch_prices.append(price)
            
            # Restore original
            self.num_simulations = original_sims
        
        batch_prices = np.array(batch_prices)
        mean_price = np.mean(batch_prices)
        std_error = np.std(batch_prices) / np.sqrt(num_batches)
        
        # Calculate confidence interval
        from scipy import stats
        z_score = stats.norm.ppf((1 + confidence_level) / 2)
        margin = z_score * std_error
        
        return {
            'price': float(mean_price),
            'std_error': float(std_error),
            'lower_bound': float(mean_price - margin),
            'upper_bound': float(mean_price + margin),
            'confidence_level': confidence_level
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Return information about the Monte Carlo model.
        
        Returns:
            Dict containing model information
        """
        return {
            'name': 'Monte Carlo Simulation',
            'type': 'Simulation',
            'description': (
                'Simulates multiple price paths using geometric Brownian motion '
                'to estimate option prices through statistical averaging.'
            ),
            'assumptions': [
                'Asset prices follow geometric Brownian motion',
                'Constant volatility and risk-free rate',
                'No transaction costs or taxes',
                'European exercise only (at expiration)',
                'Log-normal distribution of asset prices'
            ],
            'parameters': {
                'num_simulations': self.num_simulations,
                'num_steps': self.num_steps,
                'antithetic_variates': self.antithetic,
                'seed': self.seed
            },
            'advantages': [
                'Flexible for complex payoff structures',
                'Easy to extend for path-dependent options',
                'Can handle multiple risk factors',
                'Intuitive interpretation'
            ],
            'disadvantages': [
                'Computationally intensive',
                'Statistical uncertainty in results',
                'Slower than analytical methods',
                'Requires many simulations for accuracy'
            ]
        }
    
    def get_convergence_analysis(
        self,
        spot: float,
        strike: float,
        time_to_maturity: float,
        risk_free_rate: float,
        volatility: float,
        option_type: str,
        simulation_sizes: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Analyze how the price estimate converges as simulations increase.
        Useful for determining optimal number of simulations.
        
        Args:
            spot: Current spot price
            strike: Strike price
            time_to_maturity: Time to maturity
            risk_free_rate: Risk-free rate
            volatility: Volatility
            option_type: 'call' or 'put'
            simulation_sizes: List of simulation sizes to test
        
        Returns:
            Dict with simulation sizes and corresponding prices
        """
        if simulation_sizes is None:
            simulation_sizes = [1000, 5000, 10000, 50000, 100000]
        
        prices = []
        original_sims = self.num_simulations
        
        for size in simulation_sizes:
            self.num_simulations = size
            price = self.calculate_price(
                spot, strike, time_to_maturity,
                risk_free_rate, volatility, option_type
            )
            prices.append(price)
        
        # Restore original
        self.num_simulations = original_sims
        
        return {
            'simulation_sizes': simulation_sizes,
            'prices': prices,
            'final_price': prices[-1],
            'convergence': True
        }
