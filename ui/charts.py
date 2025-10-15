"""
Charts and visualizations for Option Pricing Calculator.
Creates interactive plots using Plotly.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import Dict, Any


def plot_payoff_diagram(
    spot: float,
    strike: float,
    option_price: float,
    option_type: str
):
    """
    Create payoff diagram showing profit/loss at expiration.
    
    Args:
        spot: Current spot price
        strike: Strike price
        option_price: Option premium paid
        option_type: 'call' or 'put'
    """
    # Create range of spot prices at expiration
    spot_range = np.linspace(strike * 0.5, strike * 1.5, 100)
    
    if option_type == 'call':
        # Call payoff
        payoff = np.maximum(spot_range - strike, 0)
        profit = payoff - option_price
    else:  # put
        # Put payoff
        payoff = np.maximum(strike - spot_range, 0)
        profit = payoff - option_price
    
    # Create figure
    fig = go.Figure()
    
    # Add payoff line
    fig.add_trace(go.Scatter(
        x=spot_range,
        y=payoff,
        mode='lines',
        name='Payoff at Expiration',
        line=dict(color='blue', width=2),
        hovertemplate='Spot: $%{x:.2f}<br>Payoff: $%{y:.2f}<extra></extra>'
    ))
    
    # Add profit/loss line
    fig.add_trace(go.Scatter(
        x=spot_range,
        y=profit,
        mode='lines',
        name='Profit/Loss',
        line=dict(color='green', width=2, dash='dash'),
        hovertemplate='Spot: $%{x:.2f}<br>P&L: $%{y:.2f}<extra></extra>'
    ))
    
    # Add break-even line
    fig.add_hline(
        y=0,
        line_dash="dot",
        line_color="gray",
        annotation_text="Break-even",
        annotation_position="right"
    )
    
    # Add current spot price
    fig.add_vline(
        x=spot,
        line_dash="dot",
        line_color="red",
        annotation_text=f"Current Spot: ${spot:.2f}",
        annotation_position="top"
    )
    
    # Add strike price
    fig.add_vline(
        x=strike,
        line_dash="dash",
        line_color="orange",
        annotation_text=f"Strike: ${strike:.2f}",
        annotation_position="bottom"
    )
    
    # Calculate break-even point
    if option_type == 'call':
        breakeven = strike + option_price
    else:
        breakeven = strike - option_price
    
    fig.add_vline(
        x=breakeven,
        line_dash="dot",
        line_color="purple",
        annotation_text=f"Break-even: ${breakeven:.2f}",
        annotation_position="top"
    )
    
    # Update layout
    fig.update_layout(
        title=f"{option_type.capitalize()} Option Payoff Diagram",
        xaxis_title="Spot Price at Expiration ($)",
        yaxis_title="Profit/Loss ($)",
        hovermode='x unified',
        showlegend=True,
        height=500,
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def plot_greeks_vs_spot(
    params: Dict,
    greek_calculator: Any,
    greek_name: str
):
    """
    Plot a Greek's value vs spot price.
    
    Args:
        params: Base parameters dictionary
        greek_calculator: Function to calculate the Greek
        greek_name: Name of the Greek to plot
    """
    # Create range of spot prices
    base_spot = params['spot']
    spot_range = np.linspace(base_spot * 0.7, base_spot * 1.3, 50)
    
    # Calculate Greek for each spot price
    greek_values = []
    for spot in spot_range:
        value = greek_calculator(
            spot=spot,
            strike=params['strike'],
            time_to_maturity=params['time_to_maturity'],
            risk_free_rate=params['risk_free_rate'],
            volatility=params['volatility'],
            option_type=params['option_type']
        )
        greek_values.append(value)
    
    # Create figure
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=spot_range,
        y=greek_values,
        mode='lines',
        name=greek_name,
        line=dict(color='blue', width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 100, 255, 0.2)',
        hovertemplate='Spot: $%{x:.2f}<br>' + greek_name + ': %{y:.6f}<extra></extra>'
    ))
    
    # Add current spot marker
    current_greek = greek_calculator(
        spot=base_spot,
        strike=params['strike'],
        time_to_maturity=params['time_to_maturity'],
        risk_free_rate=params['risk_free_rate'],
        volatility=params['volatility'],
        option_type=params['option_type']
    )
    
    fig.add_trace(go.Scatter(
        x=[base_spot],
        y=[current_greek],
        mode='markers',
        name='Current',
        marker=dict(size=12, color='red', symbol='diamond'),
        hovertemplate='Current Spot: $%{x:.2f}<br>' + greek_name + ': %{y:.6f}<extra></extra>'
    ))
    
    # Add strike line
    fig.add_vline(
        x=params['strike'],
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Strike: ${params['strike']:.2f}",
        annotation_position="top"
    )
    
    # Update layout
    fig.update_layout(
        title=f"{greek_name} vs Spot Price",
        xaxis_title="Spot Price ($)",
        yaxis_title=greek_name,
        hovermode='x unified',
        showlegend=True,
        height=400,
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def plot_price_vs_volatility(pricing_model: Any, params: Dict):
    """
    Plot option price vs volatility.
    
    Args:
        pricing_model: Pricing model instance
        params: Dictionary with pricing parameters
    """
    # Create range of volatilities
    base_vol = params['volatility']
    vol_range = np.linspace(base_vol * 0.5, base_vol * 2, 50)
    
    # Calculate prices
    prices = []
    for vol in vol_range:
        price = pricing_model.calculate_price(
            spot=params['spot'],
            strike=params['strike'],
            time_to_maturity=params['time_to_maturity'],
            risk_free_rate=params['risk_free_rate'],
            volatility=vol,
            option_type=params['option_type']
        )
        prices.append(price)
    
    # Create figure
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=vol_range * 100,  # Convert to percentage
        y=prices,
        mode='lines',
        name='Option Price',
        line=dict(color='green', width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 255, 100, 0.2)',
        hovertemplate='Volatility: %{x:.2f}%<br>Price: $%{y:.2f}<extra></extra>'
    ))
    
    # Add current volatility marker
    current_price = pricing_model.calculate_price(
        spot=params['spot'],
        strike=params['strike'],
        time_to_maturity=params['time_to_maturity'],
        risk_free_rate=params['risk_free_rate'],
        volatility=params['volatility'],
        option_type=params['option_type']
    )
    
    fig.add_trace(go.Scatter(
        x=[params['volatility'] * 100],
        y=[current_price],
        mode='markers',
        name='Current',
        marker=dict(size=12, color='red', symbol='diamond'),
        hovertemplate='Current Vol: %{x:.2f}%<br>Price: $%{y:.2f}<extra></extra>'
    ))
    
    # Update layout
    fig.update_layout(
        title="Option Price vs Volatility",
        xaxis_title="Volatility (%)",
        yaxis_title="Option Price ($)",
        hovermode='x unified',
        showlegend=True,
        height=400,
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def plot_price_vs_time(pricing_model: Any, params: Dict):
    """
    Plot option price vs time to maturity (time decay).
    
    Args:
        pricing_model: Pricing model instance
        params: Dictionary with pricing parameters
    """
    # Create range of times (from current to expiration)
    max_time = params['time_to_maturity']
    time_range = np.linspace(0.01, max_time, 50)
    
    # Calculate prices
    prices = []
    for time in time_range:
        price = pricing_model.calculate_price(
            spot=params['spot'],
            strike=params['strike'],
            time_to_maturity=time,
            risk_free_rate=params['risk_free_rate'],
            volatility=params['volatility'],
            option_type=params['option_type']
        )
        prices.append(price)
    
    # Create figure
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=time_range * 365,  # Convert to days
        y=prices,
        mode='lines',
        name='Option Price',
        line=dict(color='purple', width=2),
        fill='tozeroy',
        fillcolor='rgba(128, 0, 128, 0.2)',
        hovertemplate='Days to Expiry: %{x:.0f}<br>Price: $%{y:.2f}<extra></extra>'
    ))
    
    # Add current time marker
    current_price = pricing_model.calculate_price(
        spot=params['spot'],
        strike=params['strike'],
        time_to_maturity=params['time_to_maturity'],
        risk_free_rate=params['risk_free_rate'],
        volatility=params['volatility'],
        option_type=params['option_type']
    )
    
    fig.add_trace(go.Scatter(
        x=[params['time_to_maturity'] * 365],
        y=[current_price],
        mode='markers',
        name='Current',
        marker=dict(size=12, color='red', symbol='diamond'),
        hovertemplate='Days to Expiry: %{x:.0f}<br>Price: $%{y:.2f}<extra></extra>'
    ))
    
    # Update layout
    fig.update_layout(
        title="Option Price vs Time to Maturity (Time Decay)",
        xaxis_title="Days to Expiration",
        yaxis_title="Option Price ($)",
        hovermode='x unified',
        showlegend=True,
        height=400,
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def plot_all_greeks(
    params: Dict,
    greeks_calculator
):
    """
    Plot all Greeks together in subplots.
    
    Args:
        params: Base parameters dictionary
        greeks_calculator: GreeksCalculator instance
    """
    from plotly.subplots import make_subplots
    
    # Create range of spot prices
    base_spot = params['spot']
    spot_range = np.linspace(base_spot * 0.7, base_spot * 1.3, 50)
    
    greeks_names = ['Delta', 'Gamma', 'Theta', 'Vega', 'Rho']
    greeks_data = {name: [] for name in greeks_names}
    
    # Calculate all Greeks for each spot
    for spot in spot_range:
        all_greeks = greeks_calculator.calculate_all_greeks(
            spot=spot,
            strike=params['strike'],
            time_to_maturity=params['time_to_maturity'],
            risk_free_rate=params['risk_free_rate'],
            volatility=params['volatility'],
            option_type=params['option_type']
        )
        for name in greeks_names:
            greeks_data[name].append(all_greeks[name])
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=greeks_names,
        specs=[[{}, {}, {}], [{}, {}, {}]]
    )
    
    colors = ['blue', 'green', 'red', 'purple', 'orange']
    positions = [(1,1), (1,2), (1,3), (2,1), (2,2)]
    
    for idx, (name, color, pos) in enumerate(zip(greeks_names, colors, positions)):
        fig.add_trace(
            go.Scatter(
                x=spot_range,
                y=greeks_data[name],
                mode='lines',
                name=name,
                line=dict(color=color, width=2),
                showlegend=False
            ),
            row=pos[0], col=pos[1]
        )
        
        # Add strike line with vertical shape
        fig.add_shape(
            type="line",
            x0=params['strike'],
            x1=params['strike'],
            y0=0,
            y1=1,
            yref="paper",
            line=dict(dash="dash", color="gray"),
            row=pos[0], col=pos[1]
        )
    
    # Update layout
    fig.update_layout(
        title_text="All Greeks vs Spot Price",
        showlegend=False,
        height=600,
        template='plotly_white'
    )
    
    fig.update_xaxes(title_text="Spot Price ($)")
    
    st.plotly_chart(fig, use_container_width=True)
