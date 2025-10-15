"""
Visualization functions for option strategies.
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import List, Dict
from strategies.options import OptionStrategy


def plot_strategy_payoff(
    strategy: OptionStrategy,
    current_spot: float,
    show_legs: bool = True
) -> go.Figure:
    """
    Plot strategy payoff diagram.
    
    Args:
        strategy: OptionStrategy instance
        current_spot: Current spot price
        show_legs: Whether to show individual legs
        
    Returns:
        Plotly figure
    """
    # Get spot price range
    spot_range = strategy._get_analysis_range()
    
    # Calculate total payoff
    total_payoff = strategy.calculate_payoff(spot_range)
    
    # Create figure
    fig = go.Figure()
    
    # Add individual legs if requested
    if show_legs and len(strategy.legs) > 1:
        for i, leg in enumerate(strategy.legs):
            leg_payoffs = np.array([leg.payoff(s) for s in spot_range])
            
            leg_name = f"{leg.position.title()} {leg.option_type.title()} @ ${leg.strike:.2f}"
            if leg.quantity > 1:
                leg_name += f" x{leg.quantity}"
            
            fig.add_trace(go.Scatter(
                x=spot_range,
                y=leg_payoffs,
                mode='lines',
                name=leg_name,
                line=dict(dash='dash', width=1),
                opacity=0.5
            ))
    
    # Add total payoff
    fig.add_trace(go.Scatter(
        x=spot_range,
        y=total_payoff,
        mode='lines',
        name='Total P&L',
        line=dict(color='blue', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 100, 255, 0.1)'
    ))
    
    # Add zero line
    fig.add_hline(y=0, line_dash="solid", line_color="black", opacity=0.3)
    
    # Add current spot line
    fig.add_vline(
        x=current_spot,
        line_dash="dot",
        line_color="green",
        annotation_text=f"Current: ${current_spot:.2f}",
        annotation_position="top"
    )
    
    # Add break-even points
    break_evens = strategy.break_even_points()
    for be in break_evens:
        fig.add_vline(
            x=be,
            line_dash="dot",
            line_color="orange",
            annotation_text=f"B/E: ${be:.2f}",
            annotation_position="bottom"
        )
    
    # Update layout
    fig.update_layout(
        title=f"{strategy.name} - Payoff Diagram",
        xaxis_title="Spot Price at Expiration",
        yaxis_title="Profit / Loss ($)",
        hovermode='x unified',
        showlegend=True,
        height=500
    )
    
    return fig


def plot_risk_profile(strategy: OptionStrategy) -> go.Figure:
    """
    Plot risk profile bars for strategy.
    
    Args:
        strategy: OptionStrategy instance
        
    Returns:
        Plotly figure
    """
    info = strategy.get_strategy_info()
    
    fig = go.Figure()
    
    # Max profit bar
    fig.add_trace(go.Bar(
        x=['Max Profit'],
        y=[info['max_profit']],
        name='Max Profit',
        marker_color='green',
        text=[f"${info['max_profit']:.2f}"],
        textposition='outside'
    ))
    
    # Max loss bar
    fig.add_trace(go.Bar(
        x=['Max Loss'],
        y=[abs(info['max_loss'])],
        name='Max Loss',
        marker_color='red',
        text=[f"${info['max_loss']:.2f}"],
        textposition='outside'
    ))
    
    # Net premium bar
    net_prem = info['net_premium']
    color = 'green' if net_prem > 0 else 'orange'
    label = 'Credit' if net_prem > 0 else 'Debit'
    
    fig.add_trace(go.Bar(
        x=['Net Premium'],
        y=[abs(net_prem)],
        name=f'{label}',
        marker_color=color,
        text=[f"${net_prem:.2f}"],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=f"{strategy.name} - Risk Profile",
        yaxis_title="Amount ($)",
        showlegend=False,
        height=400
    )
    
    return fig


def create_strategy_comparison_table(strategies: List[OptionStrategy]) -> Dict:
    """
    Create comparison table data for multiple strategies.
    
    Args:
        strategies: List of OptionStrategy instances
        
    Returns:
        Dictionary with comparison data
    """
    comparison = {
        'Strategy': [],
        'Net Premium': [],
        'Max Profit': [],
        'Max Loss': [],
        'Risk/Reward': [],
        'Break-Even Points': []
    }
    
    for strategy in strategies:
        info = strategy.get_strategy_info()
        
        comparison['Strategy'].append(info['name'])
        comparison['Net Premium'].append(f"${info['net_premium']:.2f}")
        comparison['Max Profit'].append(f"${info['max_profit']:.2f}")
        comparison['Max Loss'].append(f"${info['max_loss']:.2f}")
        comparison['Risk/Reward'].append(f"{info['risk_reward_ratio']:.2f}")
        
        be_points = ", ".join([f"${be:.2f}" for be in info['break_even_points']])
        comparison['Break-Even Points'].append(be_points if be_points else "N/A")
    
    return comparison


def plot_multiple_strategies(
    strategies: List[OptionStrategy],
    current_spot: float
) -> go.Figure:
    """
    Plot multiple strategies on same chart for comparison.
    
    Args:
        strategies: List of OptionStrategy instances
        current_spot: Current spot price
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    # Colors for different strategies
    colors = px.colors.qualitative.Set2
    
    for idx, strategy in enumerate(strategies):
        spot_range = strategy._get_analysis_range()
        payoff = strategy.calculate_payoff(spot_range)
        
        fig.add_trace(go.Scatter(
            x=spot_range,
            y=payoff,
            mode='lines',
            name=strategy.name,
            line=dict(color=colors[idx % len(colors)], width=2)
        ))
    
    # Add zero line
    fig.add_hline(y=0, line_dash="solid", line_color="black", opacity=0.3)
    
    # Add current spot line
    fig.add_vline(
        x=current_spot,
        line_dash="dot",
        line_color="green",
        annotation_text=f"Current: ${current_spot:.2f}",
        annotation_position="top"
    )
    
    fig.update_layout(
        title="Strategy Comparison - Payoff Diagrams",
        xaxis_title="Spot Price at Expiration",
        yaxis_title="Profit / Loss ($)",
        hovermode='x unified',
        showlegend=True,
        height=500
    )
    
    return fig


def create_strategy_details_card(strategy: OptionStrategy) -> str:
    """
    Create detailed HTML card with strategy information.
    
    Args:
        strategy: OptionStrategy instance
        
    Returns:
        HTML string
    """
    info = strategy.get_strategy_info()
    
    # Determine strategy characteristics
    net_prem = info['net_premium']
    if net_prem > 0:
        premium_type = "Credit"
        premium_color = "green"
    elif net_prem < 0:
        premium_type = "Debit"
        premium_color = "orange"
    else:
        premium_type = "Neutral"
        premium_color = "gray"
    
    # Risk assessment
    risk_reward = info['risk_reward_ratio']
    if risk_reward < 0.5:
        risk_level = "Low Risk"
        risk_color = "green"
    elif risk_reward < 1.5:
        risk_level = "Moderate Risk"
        risk_color = "orange"
    else:
        risk_level = "High Risk"
        risk_color = "red"
    
    html = f"""
    <div style="
        border: 2px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: #f9f9f9;
    ">
        <h3 style="margin-top: 0; color: #333;">{strategy.name}</h3>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div>
                <p><strong>📊 Position Type:</strong> 
                    <span style="color: {premium_color}; font-weight: bold;">{premium_type}</span>
                </p>
                <p><strong>💰 Net Premium:</strong> ${net_prem:.2f}</p>
                <p><strong>📈 Max Profit:</strong> ${info['max_profit']:.2f}</p>
            </div>
            
            <div>
                <p><strong>⚠️ Max Loss:</strong> ${info['max_loss']:.2f}</p>
                <p><strong>🎯 Risk/Reward:</strong> {risk_reward:.2f}</p>
                <p><strong>📊 Risk Level:</strong> 
                    <span style="color: {risk_color}; font-weight: bold;">{risk_level}</span>
                </p>
            </div>
        </div>
        
        <p><strong>🎯 Break-Even Points:</strong></p>
        <ul>
            {''.join([f"<li>${be:.2f}</li>" for be in info['break_even_points']]) if info['break_even_points'] else '<li>None</li>'}
        </ul>
        
        <p><strong>📋 Position Details:</strong></p>
        <ul>
            {''.join([
                f"<li>{leg.position.title()} {leg.quantity}x {leg.option_type.title()} @ ${leg.strike:.2f} "
                f"(Premium: ${leg.premium:.2f})</li>" 
                for leg in strategy.legs
            ])}
        </ul>
    </div>
    """
    
    return html
