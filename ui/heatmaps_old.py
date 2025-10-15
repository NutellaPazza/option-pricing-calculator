"""
Interactive heatmaps for Option Pricing Calculator.
Creates 2D and 3D visualizations for sensitivity analysis.
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from typing import Dict, Callable


class OptionHeatmaps:
    """Generator for interactive heatmaps showing option pricing sensitivities."""
    
    @staticmethod
    def price_heatmap(
        pricing_model,
        base_params: Dict,
        option_type: str = 'call'
    ):
        """
        Create heatmap of option price: Spot Price vs Strike Price.
        
        Args:
            pricing_model: Pricing model instance
            base_params: Base parameters dictionary
            option_type: 'call' or 'put'
        
        Returns:
            Plotly figure object
        """
        # Create ranges
        spot_range = np.linspace(
            base_params['spot'] * 0.7, 
            base_params['spot'] * 1.3, 
            30
        )
        strike_range = np.linspace(
            base_params['strike'] * 0.7, 
            base_params['strike'] * 1.3, 
            30
        )
        
        # Calculate prices matrix
        prices = np.zeros((len(strike_range), len(spot_range)))
        
        for i, strike in enumerate(strike_range):
            for j, spot in enumerate(spot_range):
                prices[i, j] = pricing_model.calculate_price(
                    spot=spot,
                    strike=strike,
                    time_to_maturity=base_params['time_to_maturity'],
                    risk_free_rate=base_params['risk_free_rate'],
                    volatility=base_params['volatility'],
                    option_type=option_type
                )
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=prices,
            x=spot_range,
            y=strike_range,
            colorscale='RdYlGn',
            colorbar=dict(title="Option Price ($)"),
            hoverongaps=False,
            hovertemplate='Spot: $%{x:.2f}<br>Strike: $%{y:.2f}<br>Price: $%{z:.2f}<extra></extra>'
        ))
        
        # Add ATM line (where Spot = Strike)
        fig.add_shape(
            type="line",
            x0=min(spot_range), 
            y0=min(strike_range),
            x1=max(spot_range), 
            y1=max(strike_range),
            line=dict(color="white", width=2, dash="dash"),
        )
        
        # Add current spot/strike marker
        fig.add_trace(go.Scatter(
            x=[base_params['spot']],
            y=[base_params['strike']],
            mode='markers',
            marker=dict(size=15, color='blue', symbol='star', line=dict(color='white', width=2)),
            name='Current',
            hovertemplate='Current Position<br>Spot: $%{x:.2f}<br>Strike: $%{y:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f'{option_type.capitalize()} Option Price Heatmap',
            xaxis_title='Spot Price (S) - $',
            yaxis_title='Strike Price (K) - $',
            width=800,
            height=600,
            font=dict(size=12),
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def greek_heatmap(
        greek_calculator,
        base_params: Dict,
        greek_name: str,
        option_type: str = 'call'
    ):
        """
        Create heatmap of a Greek: Spot Price vs Time to Maturity.
        
        Args:
            greek_calculator: GreeksCalculator instance
            base_params: Base parameters dictionary
            greek_name: Name of Greek ('Delta', 'Gamma', etc.)
            option_type: 'call' or 'put'
        
        Returns:
            Plotly figure object
        """
        # Create ranges
        spot_range = np.linspace(
            base_params['spot'] * 0.7,
            base_params['spot'] * 1.3,
            30
        )
        time_range = np.linspace(
            0.1,
            base_params['time_to_maturity'] * 2,
            30
        )
        
        # Map Greek name to calculator method
        greek_methods = {
            'Delta': greek_calculator.delta,
            'Gamma': greek_calculator.gamma,
            'Theta': greek_calculator.theta,
            'Vega': greek_calculator.vega,
            'Rho': greek_calculator.rho
        }
        
        greek_func = greek_methods[greek_name]
        
        # Calculate Greek values matrix
        greek_values = np.zeros((len(time_range), len(spot_range)))
        
        for i, time in enumerate(time_range):
            for j, spot in enumerate(spot_range):
                greek_values[i, j] = greek_func(
                    spot=spot,
                    strike=base_params['strike'],
                    time_to_maturity=time,
                    risk_free_rate=base_params['risk_free_rate'],
                    volatility=base_params['volatility'],
                    option_type=option_type
                )
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=greek_values,
            x=spot_range,
            y=time_range,
            colorscale='Viridis',
            colorbar=dict(title=greek_name),
            hoverongaps=False,
            hovertemplate='Spot: $%{x:.2f}<br>Time: %{y:.2f} years<br>' + greek_name + ': %{z:.4f}<extra></extra>'
        ))
        
        # Add current position marker
        current_value = greek_func(
            spot=base_params['spot'],
            strike=base_params['strike'],
            time_to_maturity=base_params['time_to_maturity'],
            risk_free_rate=base_params['risk_free_rate'],
            volatility=base_params['volatility'],
            option_type=option_type
        )
        
        fig.add_trace(go.Scatter(
            x=[base_params['spot']],
            y=[base_params['time_to_maturity']],
            mode='markers',
            marker=dict(size=15, color='red', symbol='star', line=dict(color='white', width=2)),
            name='Current',
            hovertemplate=f'Current {greek_name}<br>Spot: $%{{x:.2f}}<br>Time: %{{y:.2f}} years<br>{greek_name}: {current_value:.4f}<extra></extra>'
        ))
        
        # Add strike line
        fig.add_vline(
            x=base_params['strike'],
            line_dash="dash",
            line_color="white",
            annotation_text=f"Strike: ${base_params['strike']:.2f}",
            annotation_position="top"
        )
        
        fig.update_layout(
            title=f'{greek_name} Heatmap - {option_type.capitalize()} Option',
            xaxis_title='Spot Price (S) - $',
            yaxis_title='Time to Maturity (Years)',
            width=800,
            height=600,
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def volatility_surface(base_params: Dict, pricing_model):
        """
        Create 3D volatility surface: Strike vs Time to Maturity.
        Simulates implied volatility smile/skew.
        
        Args:
            base_params: Base parameters dictionary
            pricing_model: Pricing model instance
        
        Returns:
            Plotly figure object
        """
        # Create ranges
        strike_range = np.linspace(
            base_params['spot'] * 0.7,
            base_params['spot'] * 1.3,
            25
        )
        time_range = np.linspace(0.1, 2.0, 25)
        
        # Simulate volatility surface (simplified smile/skew)
        vol_surface = np.zeros((len(time_range), len(strike_range)))
        
        for i, time in enumerate(time_range):
            for j, strike in enumerate(strike_range):
                # Simplified volatility smile model
                moneyness = strike / base_params['spot']
                
                # Volatility smile: higher vol for OTM/ITM, lower for ATM
                smile_effect = 0.3 * (moneyness - 1)**2
                
                # Term structure: slight increase with time
                term_effect = 0.05 * np.sqrt(time)
                
                vol_surface[i, j] = base_params['volatility'] * (
                    1 + smile_effect + term_effect
                )
        
        # Create 3D surface
        fig = go.Figure(data=[go.Surface(
            z=vol_surface * 100,  # Convert to percentage
            x=strike_range,
            y=time_range,
            colorscale='Plasma',
            colorbar=dict(title="Volatility (%)")
        )])
        
        # Add current point
        fig.add_trace(go.Scatter3d(
            x=[base_params['strike']],
            y=[base_params['time_to_maturity']],
            z=[base_params['volatility'] * 100],
            mode='markers',
            marker=dict(size=10, color='red', symbol='diamond'),
            name='Current'
        ))
        
        fig.update_layout(
            title='Volatility Surface (Implied Vol)',
            scene=dict(
                xaxis_title='Strike Price (K) - $',
                yaxis_title='Time to Maturity (Years)',
                zaxis_title='Implied Volatility (%)',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.3)
                )
            ),
            width=900,
            height=700,
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def profit_loss_heatmap(
        pricing_model,
        base_params: Dict,
        entry_premium: float,
        option_type: str = 'call'
    ):
        """
        Create P&L heatmap: Spot at Different Times vs Entry Spot.
        
        Args:
            pricing_model: Pricing model instance
            base_params: Base parameters dictionary
            entry_premium: Premium paid for the option
            option_type: 'call' or 'put'
        
        Returns:
            Plotly figure object
        """
        # Create ranges
        spot_at_future = np.linspace(
            base_params['spot'] * 0.5,
            base_params['spot'] * 1.5,
            40
        )
        time_range = np.linspace(
            base_params['time_to_maturity'],
            0.01,
            30
        )
        
        # Calculate P&L matrix
        pnl = np.zeros((len(time_range), len(spot_at_future)))
        
        for i, time in enumerate(time_range):
            for j, spot in enumerate(spot_at_future):
                current_value = pricing_model.calculate_price(
                    spot=spot,
                    strike=base_params['strike'],
                    time_to_maturity=time,
                    risk_free_rate=base_params['risk_free_rate'],
                    volatility=base_params['volatility'],
                    option_type=option_type
                )
                pnl[i, j] = current_value - entry_premium
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=pnl,
            x=spot_at_future,
            y=time_range * 365,  # Convert to days
            colorscale='RdYlGn',
            zmid=0,  # Center colorscale at zero
            colorbar=dict(title="P&L ($)"),
            hovertemplate='Spot: $%{x:.2f}<br>Days Left: %{y:.0f}<br>P&L: $%{z:.2f}<extra></extra>'
        ))
        
        # Add strike line
        fig.add_vline(
            x=base_params['strike'],
            line_dash="dash",
            line_color="black",
            annotation_text=f"Strike: ${base_params['strike']:.2f}",
            annotation_position="top"
        )
        
        # Add current position
        fig.add_trace(go.Scatter(
            x=[base_params['spot']],
            y=[base_params['time_to_maturity'] * 365],
            mode='markers',
            marker=dict(size=15, color='blue', symbol='star', line=dict(color='white', width=2)),
            name='Current Position',
            hovertemplate='Current<br>Spot: $%{x:.2f}<br>Days: %{y:.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f'Profit/Loss Heatmap - {option_type.capitalize()} Option',
            xaxis_title='Spot Price at Time - $',
            yaxis_title='Days to Expiration',
            width=800,
            height=600,
            showlegend=True
        )
        
        return fig
    
    @staticmethod
    def comparison_heatmap(
        models_dict: Dict,
        base_params: Dict,
        option_type: str = 'call'
    ):
        """
        Compare prices from different models in heatmaps.
        
        Args:
            models_dict: Dictionary of {model_name: model_instance}
            base_params: Base parameters dictionary
            option_type: 'call' or 'put'
        
        Returns:
            Plotly figure object
        """
        # Create ranges
        spot_range = np.linspace(
            base_params['spot'] * 0.8,
            base_params['spot'] * 1.2,
            20
        )
        vol_range = np.linspace(
            base_params['volatility'] * 0.5,
            base_params['volatility'] * 1.5,
            20
        )
        
        model_names = list(models_dict.keys())
        
        # Create figure with dropdown
        fig = go.Figure()
        
        for idx, (name, model) in enumerate(models_dict.items()):
            prices = np.zeros((len(vol_range), len(spot_range)))
            
            for i, vol in enumerate(vol_range):
                for j, spot in enumerate(spot_range):
                    prices[i, j] = model.calculate_price(
                        spot=spot,
                        strike=base_params['strike'],
                        time_to_maturity=base_params['time_to_maturity'],
                        risk_free_rate=base_params['risk_free_rate'],
                        volatility=vol,
                        option_type=option_type
                    )
            
            fig.add_trace(go.Heatmap(
                z=prices,
                x=spot_range,
                y=vol_range * 100,
                name=name,
                colorscale='Viridis',
                colorbar=dict(title="Price ($)"),
                visible=(idx == 0),
                hovertemplate='Spot: $%{x:.2f}<br>Vol: %{y:.2f}%<br>Price: $%{z:.2f}<extra></extra>'
            ))
        
        # Create buttons for model selection
        buttons = []
        for i, name in enumerate(model_names):
            visibility = [j == i for j in range(len(model_names))]
            buttons.append(
                dict(
                    label=name,
                    method="update",
                    args=[
                        {"visible": visibility},
                        {"title": f"Option Prices - {name} Model"}
                    ]
                )
            )
        
        fig.update_layout(
            updatemenus=[dict(
                buttons=buttons,
                direction="down",
                showactive=True,
                x=0.17,
                y=1.15
            )],
            title=f"Option Prices - {model_names[0]} Model",
            xaxis_title='Spot Price (S) - $',
            yaxis_title='Volatility (σ) - %',
            width=800,
            height=600
        )
        
        return fig
