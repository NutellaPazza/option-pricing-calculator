"""
Binomial Tree model for option pricing.
Implements Cox-Ross-Rubinstein (CRR) model for European and American options.
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple
from .base_model import OptionPricingModel


class BinomialTreeModel(OptionPricingModel):
    """
    Binomial Tree model for option pricing (Cox-Ross-Rubinstein).
    
    This model builds a discrete-time tree of possible asset prices
    and works backward to determine option value. Supports both
    European and American options.
    
    Advantages:
        - Handles American options (early exercise)
        - Intuitive visualization
        - Flexible for different option types
        - Converges to Black-Scholes as steps increase
    
    Disadvantages:
        - Slower than analytical methods
        - Requires many steps for accuracy
        - Memory intensive for large trees
    """
    
    def __init__(
        self,
        num_steps: int = 100,
        american: bool = False
    ):
        """
        Initialize Binomial Tree model.
        
        Args:
            num_steps: Number of time steps in the tree
            american: True for American options, False for European
        """
        self.num_steps = num_steps
        self.american = american
        
        # Store last tree for visualization
        self._last_price_tree = None
        self._last_option_tree = None
        self._last_exercise_tree = None
    
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
        Calculate option price using Binomial Tree (CRR method).
        
        The CRR model uses the following parameters:
        - u (up factor): exp(σ * √(Δt))
        - d (down factor): 1/u = exp(-σ * √(Δt))
        - p (risk-neutral probability): (exp(r*Δt) - d) / (u - d)
        
        The tree is built forward (for asset prices) and then
        backward (for option values).
        
        Args:
            spot: Current spot price
            strike: Strike price
            time_to_maturity: Time to expiration in years
            risk_free_rate: Risk-free interest rate
            volatility: Volatility
            option_type: 'call' or 'put'
        
        Returns:
            float: Calculated option price
        
        Raises:
            ValueError: If input parameters are invalid
        """
        # Validate inputs
        self.validate_inputs(
            spot, strike, time_to_maturity,
            risk_free_rate, volatility, option_type
        )
        
        option_type = self._get_option_type(option_type)
        
        # Calculate tree parameters
        dt = time_to_maturity / self.num_steps  # Time step
        u = np.exp(volatility * np.sqrt(dt))     # Up factor
        d = 1 / u                                 # Down factor
        p = (np.exp(risk_free_rate * dt) - d) / (u - d)  # Risk-neutral probability
        discount = np.exp(-risk_free_rate * dt)  # Discount factor
        
        # Initialize price tree
        # Tree shape: price_tree[i][j] where i=step, j=node at that step
        price_tree = np.zeros((self.num_steps + 1, self.num_steps + 1))
        
        # Build asset price tree (forward)
        # At step i, node j: S * u^j * d^(i-j)
        for i in range(self.num_steps + 1):
            for j in range(i + 1):
                price_tree[i][j] = spot * (u ** j) * (d ** (i - j))
        
        # Initialize option value tree
        option_tree = np.zeros((self.num_steps + 1, self.num_steps + 1))
        
        # Initialize early exercise tree (for American options)
        exercise_tree = np.zeros((self.num_steps + 1, self.num_steps + 1), dtype=bool)
        
        # Calculate option values at expiration (terminal nodes)
        for j in range(self.num_steps + 1):
            if option_type == 'call':
                option_tree[self.num_steps][j] = max(0, price_tree[self.num_steps][j] - strike)
            else:  # put
                option_tree[self.num_steps][j] = max(0, strike - price_tree[self.num_steps][j])
        
        # Backward induction: calculate option values at earlier nodes
        for i in range(self.num_steps - 1, -1, -1):
            for j in range(i + 1):
                # Calculate continuation value (expected value if held)
                continuation_value = discount * (
                    p * option_tree[i + 1][j + 1] +  # Up move
                    (1 - p) * option_tree[i + 1][j]   # Down move
                )
                
                if self.american:
                    # For American options, check early exercise
                    if option_type == 'call':
                        exercise_value = max(0, price_tree[i][j] - strike)
                    else:  # put
                        exercise_value = max(0, strike - price_tree[i][j])
                    
                    # Take maximum of continuation and exercise
                    if exercise_value > continuation_value:
                        option_tree[i][j] = exercise_value
                        exercise_tree[i][j] = True  # Mark as early exercise
                    else:
                        option_tree[i][j] = continuation_value
                else:
                    # European option: only continuation value
                    option_tree[i][j] = continuation_value
        
        # Store trees for visualization
        self._last_price_tree = price_tree
        self._last_option_tree = option_tree
        self._last_exercise_tree = exercise_tree
        
        # Return option value at root node
        return float(option_tree[0][0])
    
    def get_tree_data(self) -> Optional[Dict[str, Any]]:
        """
        Get the last calculated tree data for visualization.
        
        Returns:
            Dict with:
                - price_tree: Asset prices at each node
                - option_tree: Option values at each node
                - exercise_tree: Early exercise indicators (American only)
            
            Returns None if no calculation has been performed yet.
        """
        if self._last_price_tree is None:
            return None
        
        return {
            'price_tree': self._last_price_tree,
            'option_tree': self._last_option_tree,
            'exercise_tree': self._last_exercise_tree,
            'num_steps': self.num_steps,
            'american': self.american
        }
    
    def calculate_greeks_numerical(
        self,
        spot: float,
        strike: float,
        time_to_maturity: float,
        risk_free_rate: float,
        volatility: float,
        option_type: str
    ) -> Dict[str, float]:
        """
        Calculate Greeks using numerical differentiation.
        
        Uses finite differences to approximate partial derivatives.
        
        Args:
            spot: Current spot price
            strike: Strike price
            time_to_maturity: Time to maturity
            risk_free_rate: Risk-free rate
            volatility: Volatility
            option_type: 'call' or 'put'
        
        Returns:
            Dict with Delta, Gamma, Theta, Vega, Rho
        """
        # Small perturbations for numerical derivatives
        h_spot = spot * 0.01    # 1% of spot
        h_vol = volatility * 0.01  # 1% of vol
        h_rate = 0.0001         # 1 basis point
        h_time = 1.0 / 365.0    # 1 day
        
        # Base price
        price = self.calculate_price(
            spot, strike, time_to_maturity,
            risk_free_rate, volatility, option_type
        )
        
        # Delta: ∂V/∂S
        price_up = self.calculate_price(
            spot + h_spot, strike, time_to_maturity,
            risk_free_rate, volatility, option_type
        )
        price_down = self.calculate_price(
            spot - h_spot, strike, time_to_maturity,
            risk_free_rate, volatility, option_type
        )
        delta = (price_up - price_down) / (2 * h_spot)
        
        # Gamma: ∂²V/∂S²
        gamma = (price_up - 2 * price + price_down) / (h_spot ** 2)
        
        # Theta: -∂V/∂t (negative because time decay)
        if time_to_maturity > h_time:
            price_time = self.calculate_price(
                spot, strike, time_to_maturity - h_time,
                risk_free_rate, volatility, option_type
            )
            theta = -(price_time - price) / h_time
        else:
            theta = 0.0
        
        # Vega: ∂V/∂σ
        price_vol_up = self.calculate_price(
            spot, strike, time_to_maturity,
            risk_free_rate, volatility + h_vol, option_type
        )
        vega = (price_vol_up - price) / h_vol
        
        # Rho: ∂V/∂r
        price_rate_up = self.calculate_price(
            spot, strike, time_to_maturity,
            risk_free_rate + h_rate, volatility, option_type
        )
        rho = (price_rate_up - price) / h_rate
        
        return {
            'Delta': float(delta),
            'Gamma': float(gamma),
            'Theta': float(theta / 365.0),  # Convert to per-day
            'Vega': float(vega / 100.0),     # Convert to per-percentage-point
            'Rho': float(rho / 100.0)        # Convert to per-percentage-point
        }
    
    def get_convergence_analysis(
        self,
        spot: float,
        strike: float,
        time_to_maturity: float,
        risk_free_rate: float,
        volatility: float,
        option_type: str,
        step_sizes: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Analyze convergence as number of steps increases.
        
        Args:
            spot: Current spot price
            strike: Strike price
            time_to_maturity: Time to maturity
            risk_free_rate: Risk-free rate
            volatility: Volatility
            option_type: 'call' or 'put'
            step_sizes: List of step sizes to test
        
        Returns:
            Dict with step sizes and corresponding prices
        """
        if step_sizes is None:
            step_sizes = [10, 25, 50, 100, 200, 500]
        
        prices = []
        original_steps = self.num_steps
        
        for steps in step_sizes:
            self.num_steps = steps
            price = self.calculate_price(
                spot, strike, time_to_maturity,
                risk_free_rate, volatility, option_type
            )
            prices.append(price)
        
        # Restore original
        self.num_steps = original_steps
        
        return {
            'step_sizes': step_sizes,
            'prices': prices,
            'final_price': prices[-1],
            'convergence': True
        }
    
    def get_early_exercise_boundary(
        self,
        spot_range: Tuple[float, float],
        strike: float,
        time_to_maturity: float,
        risk_free_rate: float,
        volatility: float,
        option_type: str,
        num_points: int = 50
    ) -> Optional[Dict[str, Any]]:
        """
        Calculate early exercise boundary for American options.
        
        Only applicable for American options.
        
        Args:
            spot_range: (min_spot, max_spot) tuple
            strike: Strike price
            time_to_maturity: Time to maturity
            risk_free_rate: Risk-free rate
            volatility: Volatility
            option_type: 'call' or 'put'
            num_points: Number of points to calculate
        
        Returns:
            Dict with spot prices, times, and exercise indicators
            Returns None if not American option
        """
        if not self.american:
            return None
        
        spot_prices = np.linspace(spot_range[0], spot_range[1], num_points)
        times = np.linspace(0, time_to_maturity, self.num_steps + 1)
        
        exercise_boundary = []
        
        for spot in spot_prices:
            self.calculate_price(
                spot, strike, time_to_maturity,
                risk_free_rate, volatility, option_type
            )
            
            # Find first time when early exercise is optimal
            tree_data = self.get_tree_data()
            if tree_data:
                exercise_tree = tree_data['exercise_tree']
                # Check diagonal (spot price path)
                for i in range(self.num_steps + 1):
                    if exercise_tree[i][i // 2] if i // 2 <= i else False:
                        exercise_boundary.append(times[i])
                        break
                else:
                    exercise_boundary.append(time_to_maturity)
        
        return {
            'spot_prices': spot_prices,
            'exercise_times': exercise_boundary,
            'times': times
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Return information about the Binomial Tree model.
        
        Returns:
            Dict containing model information
        """
        return {
            'name': 'Binomial Tree (Cox-Ross-Rubinstein)',
            'type': 'Discrete-Time',
            'description': (
                'Builds a discrete tree of possible asset price paths and works '
                'backward to determine option value. Supports both European and '
                'American options with early exercise.'
            ),
            'assumptions': [
                'Asset prices move up or down by fixed factors each period',
                'Risk-neutral pricing framework',
                'Constant volatility and risk-free rate',
                'No transaction costs or taxes',
                'Continuous trading possible'
            ],
            'parameters': {
                'num_steps': self.num_steps,
                'american': self.american,
                'method': 'Cox-Ross-Rubinstein (CRR)'
            },
            'advantages': [
                'Handles American options naturally',
                'Intuitive tree structure',
                'Flexible for various payoff structures',
                'Converges to Black-Scholes',
                'Supports path-dependent features'
            ],
            'disadvantages': [
                'Computationally slower than analytical methods',
                'Requires many steps for accuracy',
                'Memory intensive for large trees',
                'Convergence can oscillate'
            ]
        }

