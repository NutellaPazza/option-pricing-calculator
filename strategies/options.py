"""
Option Trading Strategies Module.
Implements common multi-leg option strategies with P&L analysis.
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
from dataclasses import dataclass
from models.black_scholes import BlackScholesModel


@dataclass
class OptionLeg:
    """Represents a single option leg in a strategy."""
    option_type: str  # 'call' or 'put'
    strike: float
    position: str  # 'long' or 'short'
    quantity: int = 1
    premium: float = 0.0  # Price paid/received
    
    def payoff(self, spot: float) -> float:
        """
        Calculate payoff at expiration for this leg.
        
        Args:
            spot: Spot price at expiration
            
        Returns:
            Payoff value (positive = profit, negative = loss)
        """
        if self.option_type == 'call':
            intrinsic = max(spot - self.strike, 0)
        else:  # put
            intrinsic = max(self.strike - spot, 0)
        
        # Long position: pay premium, receive intrinsic
        # Short position: receive premium, pay intrinsic
        if self.position == 'long':
            return (intrinsic - self.premium) * self.quantity
        else:  # short
            return (self.premium - intrinsic) * self.quantity


class OptionStrategy:
    """Base class for option trading strategies."""
    
    def __init__(self, name: str, legs: List[OptionLeg]):
        """
        Initialize strategy.
        
        Args:
            name: Strategy name
            legs: List of option legs
        """
        self.name = name
        self.legs = legs
        self.bs_model = BlackScholesModel()
    
    def calculate_payoff(self, spot_range: np.ndarray) -> np.ndarray:
        """
        Calculate strategy payoff across spot price range.
        
        Args:
            spot_range: Array of spot prices
            
        Returns:
            Array of payoffs
        """
        payoffs = np.zeros_like(spot_range)
        for spot_idx, spot in enumerate(spot_range):
            total_payoff = sum(leg.payoff(spot) for leg in self.legs)
            payoffs[spot_idx] = total_payoff
        return payoffs
    
    def net_premium(self) -> float:
        """
        Calculate net premium paid/received.
        
        Returns:
            Net premium (negative = paid, positive = received)
        """
        net = 0.0
        for leg in self.legs:
            if leg.position == 'long':
                net -= leg.premium * leg.quantity
            else:  # short
                net += leg.premium * leg.quantity
        return net
    
    def max_profit(self) -> float:
        """Calculate maximum profit."""
        spot_range = self._get_analysis_range()
        payoffs = self.calculate_payoff(spot_range)
        return float(np.max(payoffs))
    
    def max_loss(self) -> float:
        """Calculate maximum loss."""
        spot_range = self._get_analysis_range()
        payoffs = self.calculate_payoff(spot_range)
        return float(np.min(payoffs))
    
    def break_even_points(self) -> List[float]:
        """
        Find break-even points where payoff = 0.
        
        Returns:
            List of break-even spot prices
        """
        spot_range = self._get_analysis_range()
        payoffs = self.calculate_payoff(spot_range)
        
        break_evens = []
        for i in range(len(payoffs) - 1):
            # Check for sign change (zero crossing)
            if payoffs[i] * payoffs[i + 1] < 0:
                # Linear interpolation to find exact break-even
                be = spot_range[i] - payoffs[i] * (spot_range[i + 1] - spot_range[i]) / (payoffs[i + 1] - payoffs[i])
                break_evens.append(float(be))
        
        return break_evens
    
    def risk_reward_ratio(self) -> float:
        """
        Calculate risk/reward ratio.
        
        Returns:
            Ratio of max loss to max profit
        """
        max_prof = self.max_profit()
        max_loss = abs(self.max_loss())
        
        if max_prof == 0:
            return float('inf')
        return max_loss / max_prof
    
    def _get_analysis_range(self) -> np.ndarray:
        """Get spot price range for analysis."""
        strikes = [leg.strike for leg in self.legs]
        min_strike = min(strikes)
        max_strike = max(strikes)
        
        # Extend range 50% beyond strikes
        range_width = max_strike - min_strike
        start = max(min_strike - 0.5 * range_width, 0.01)
        end = max_strike + 0.5 * range_width
        
        return np.linspace(start, end, 1000)
    
    def get_strategy_info(self) -> Dict:
        """Get comprehensive strategy information."""
        return {
            'name': self.name,
            'legs': len(self.legs),
            'net_premium': self.net_premium(),
            'max_profit': self.max_profit(),
            'max_loss': self.max_loss(),
            'break_even_points': self.break_even_points(),
            'risk_reward_ratio': self.risk_reward_ratio()
        }


class StrategyFactory:
    """Factory for creating common option strategies."""
    
    def __init__(
        self,
        spot: float,
        time_to_maturity: float,
        risk_free_rate: float,
        volatility: float
    ):
        """
        Initialize factory.
        
        Args:
            spot: Current spot price
            time_to_maturity: Time to expiration
            risk_free_rate: Risk-free rate
            volatility: Volatility
        """
        self.spot = spot
        self.time_to_maturity = time_to_maturity
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility
        self.bs_model = BlackScholesModel()
    
    def _calculate_premium(self, option_type: str, strike: float) -> float:
        """Calculate option premium using Black-Scholes."""
        return self.bs_model.calculate_price(
            spot=self.spot,
            strike=strike,
            time_to_maturity=self.time_to_maturity,
            risk_free_rate=self.risk_free_rate,
            volatility=self.volatility,
            option_type=option_type
        )
    
    # ==================== VERTICAL SPREADS ====================
    
    def bull_call_spread(self, lower_strike: float, upper_strike: float) -> OptionStrategy:
        """
        Bull Call Spread: Long lower strike call + Short higher strike call.
        
        Bullish strategy with limited profit and limited loss.
        """
        long_call = OptionLeg(
            option_type='call',
            strike=lower_strike,
            position='long',
            premium=self._calculate_premium('call', lower_strike)
        )
        
        short_call = OptionLeg(
            option_type='call',
            strike=upper_strike,
            position='short',
            premium=self._calculate_premium('call', upper_strike)
        )
        
        return OptionStrategy("Bull Call Spread", [long_call, short_call])
    
    def bear_put_spread(self, lower_strike: float, upper_strike: float) -> OptionStrategy:
        """
        Bear Put Spread: Long higher strike put + Short lower strike put.
        
        Bearish strategy with limited profit and limited loss.
        """
        long_put = OptionLeg(
            option_type='put',
            strike=upper_strike,
            position='long',
            premium=self._calculate_premium('put', upper_strike)
        )
        
        short_put = OptionLeg(
            option_type='put',
            strike=lower_strike,
            position='short',
            premium=self._calculate_premium('put', lower_strike)
        )
        
        return OptionStrategy("Bear Put Spread", [long_put, short_put])
    
    def bull_put_spread(self, lower_strike: float, upper_strike: float) -> OptionStrategy:
        """
        Bull Put Spread: Short higher strike put + Long lower strike put.
        
        Bullish credit spread with limited profit and limited loss.
        """
        short_put = OptionLeg(
            option_type='put',
            strike=upper_strike,
            position='short',
            premium=self._calculate_premium('put', upper_strike)
        )
        
        long_put = OptionLeg(
            option_type='put',
            strike=lower_strike,
            position='long',
            premium=self._calculate_premium('put', lower_strike)
        )
        
        return OptionStrategy("Bull Put Spread", [short_put, long_put])
    
    def bear_call_spread(self, lower_strike: float, upper_strike: float) -> OptionStrategy:
        """
        Bear Call Spread: Short lower strike call + Long higher strike call.
        
        Bearish credit spread with limited profit and limited loss.
        """
        short_call = OptionLeg(
            option_type='call',
            strike=lower_strike,
            position='short',
            premium=self._calculate_premium('call', lower_strike)
        )
        
        long_call = OptionLeg(
            option_type='call',
            strike=upper_strike,
            position='long',
            premium=self._calculate_premium('call', upper_strike)
        )
        
        return OptionStrategy("Bear Call Spread", [short_call, long_call])
    
    # ==================== VOLATILITY STRATEGIES ====================
    
    def long_straddle(self, strike: float) -> OptionStrategy:
        """
        Long Straddle: Long call + Long put at same strike.
        
        Profits from large moves in either direction. High volatility play.
        """
        long_call = OptionLeg(
            option_type='call',
            strike=strike,
            position='long',
            premium=self._calculate_premium('call', strike)
        )
        
        long_put = OptionLeg(
            option_type='put',
            strike=strike,
            position='long',
            premium=self._calculate_premium('put', strike)
        )
        
        return OptionStrategy("Long Straddle", [long_call, long_put])
    
    def short_straddle(self, strike: float) -> OptionStrategy:
        """
        Short Straddle: Short call + Short put at same strike.
        
        Profits from low volatility. Unlimited risk.
        """
        short_call = OptionLeg(
            option_type='call',
            strike=strike,
            position='short',
            premium=self._calculate_premium('call', strike)
        )
        
        short_put = OptionLeg(
            option_type='put',
            strike=strike,
            position='short',
            premium=self._calculate_premium('put', strike)
        )
        
        return OptionStrategy("Short Straddle", [short_call, short_put])
    
    def long_strangle(self, call_strike: float, put_strike: float) -> OptionStrategy:
        """
        Long Strangle: Long OTM call + Long OTM put.
        
        Similar to straddle but cheaper, requires bigger move.
        """
        long_call = OptionLeg(
            option_type='call',
            strike=call_strike,
            position='long',
            premium=self._calculate_premium('call', call_strike)
        )
        
        long_put = OptionLeg(
            option_type='put',
            strike=put_strike,
            position='long',
            premium=self._calculate_premium('put', put_strike)
        )
        
        return OptionStrategy("Long Strangle", [long_call, long_put])
    
    def short_strangle(self, call_strike: float, put_strike: float) -> OptionStrategy:
        """
        Short Strangle: Short OTM call + Short OTM put.
        
        Profits from low volatility with wider profit range than short straddle.
        """
        short_call = OptionLeg(
            option_type='call',
            strike=call_strike,
            position='short',
            premium=self._calculate_premium('call', call_strike)
        )
        
        short_put = OptionLeg(
            option_type='put',
            strike=put_strike,
            position='short',
            premium=self._calculate_premium('put', put_strike)
        )
        
        return OptionStrategy("Short Strangle", [short_call, short_put])
    
    def butterfly_spread(
        self, 
        lower_strike: float, 
        middle_strike: float, 
        upper_strike: float,
        option_type: str = 'call'
    ) -> OptionStrategy:
        """
        Butterfly Spread: 1 long lower + 2 short middle + 1 long upper.
        
        Profits from low volatility around middle strike.
        """
        if option_type == 'call':
            legs = [
                OptionLeg('call', lower_strike, 'long', 1, self._calculate_premium('call', lower_strike)),
                OptionLeg('call', middle_strike, 'short', 2, self._calculate_premium('call', middle_strike)),
                OptionLeg('call', upper_strike, 'long', 1, self._calculate_premium('call', upper_strike))
            ]
            name = "Call Butterfly Spread"
        else:
            legs = [
                OptionLeg('put', lower_strike, 'long', 1, self._calculate_premium('put', lower_strike)),
                OptionLeg('put', middle_strike, 'short', 2, self._calculate_premium('put', middle_strike)),
                OptionLeg('put', upper_strike, 'long', 1, self._calculate_premium('put', upper_strike))
            ]
            name = "Put Butterfly Spread"
        
        return OptionStrategy(name, legs)
    
    def iron_condor(
        self,
        put_lower_strike: float,
        put_upper_strike: float,
        call_lower_strike: float,
        call_upper_strike: float
    ) -> OptionStrategy:
        """
        Iron Condor: Bull put spread + Bear call spread.
        
        Profits from low volatility with defined risk.
        """
        legs = [
            # Bull put spread
            OptionLeg('put', put_lower_strike, 'long', 1, self._calculate_premium('put', put_lower_strike)),
            OptionLeg('put', put_upper_strike, 'short', 1, self._calculate_premium('put', put_upper_strike)),
            # Bear call spread
            OptionLeg('call', call_lower_strike, 'short', 1, self._calculate_premium('call', call_lower_strike)),
            OptionLeg('call', call_upper_strike, 'long', 1, self._calculate_premium('call', call_upper_strike))
        ]
        
        return OptionStrategy("Iron Condor", legs)
    
    def iron_butterfly(
        self,
        lower_strike: float,
        middle_strike: float,
        upper_strike: float
    ) -> OptionStrategy:
        """
        Iron Butterfly: Short straddle + Long strangle.
        
        Profits from low volatility, similar to butterfly but uses all four legs.
        """
        legs = [
            OptionLeg('put', lower_strike, 'long', 1, self._calculate_premium('put', lower_strike)),
            OptionLeg('put', middle_strike, 'short', 1, self._calculate_premium('put', middle_strike)),
            OptionLeg('call', middle_strike, 'short', 1, self._calculate_premium('call', middle_strike)),
            OptionLeg('call', upper_strike, 'long', 1, self._calculate_premium('call', upper_strike))
        ]
        
        return OptionStrategy("Iron Butterfly", legs)
