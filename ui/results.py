"""
Results display component for Option Pricing Calculator.
Displays calculated prices, Greeks, and key metrics.
"""

import streamlit as st
import pandas as pd
from typing import Dict


def display_option_price(price: float, option_type: str, model_name: str):
    """
    Display the calculated option price prominently.
    
    Args:
        price: Calculated option price
        option_type: 'call' or 'put'
        model_name: Name of the pricing model used
    """
    st.markdown("### 💵 Option Price")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.metric(
            label=f"{option_type.capitalize()} Option Value",
            value=f"${price:.4f}",
            help=f"Calculated using {model_name} model"
        )
    
    with col2:
        st.metric(
            label="Model",
            value=model_name,
            help="Pricing model used for calculation"
        )
    
    with col3:
        st.metric(
            label="Type",
            value=option_type.capitalize(),
            help="Option type"
        )


def display_greeks(greeks: Dict[str, float]):
    """
    Display the Greeks in a clean tabular format.
    
    Args:
        greeks: Dictionary containing all Greeks values
    """
    st.markdown("### 📊 The Greeks")
    st.markdown("*Sensitivity measures of the option price*")
    
    # Create columns for Greeks
    cols = st.columns(5)
    
    greek_info = {
        'Delta': {
            'icon': 'Δ',
            'description': 'Change in price per $1 change in spot',
            'interpretation': 'Hedge ratio'
        },
        'Gamma': {
            'icon': 'Γ',
            'description': 'Change in Delta per $1 change in spot',
            'interpretation': 'Delta curvature'
        },
        'Theta': {
            'icon': 'Θ',
            'description': 'Change in price per day',
            'interpretation': 'Time decay'
        },
        'Vega': {
            'icon': 'ν',
            'description': 'Change in price per 1% change in volatility',
            'interpretation': 'Volatility sensitivity'
        },
        'Rho': {
            'icon': 'ρ',
            'description': 'Change in price per 1% change in interest rate',
            'interpretation': 'Rate sensitivity'
        }
    }
    
    for idx, (greek_name, greek_value) in enumerate(greeks.items()):
        with cols[idx]:
            info = greek_info[greek_name]
            
            # Determine color based on value
            if greek_value > 0:
                delta_color = "normal"
            elif greek_value < 0:
                delta_color = "inverse"
            else:
                delta_color = "off"
            
            st.metric(
                label=f"{info['icon']} {greek_name}",
                value=f"{greek_value:.6f}",
                help=f"{info['description']}\n\n{info['interpretation']}"
            )
    
    # Greeks detailed table
    with st.expander("📋 Detailed Greeks Table"):
        greeks_df = pd.DataFrame([
            {
                'Greek': greek_name,
                'Symbol': greek_info[greek_name]['icon'],
                'Value': f"{value:.6f}",
                'Description': greek_info[greek_name]['description'],
                'Interpretation': greek_info[greek_name]['interpretation']
            }
            for greek_name, value in greeks.items()
        ])
        
        st.dataframe(
            greeks_df,
            use_container_width=True,
            hide_index=True
        )


def display_input_summary(params: Dict):
    """
    Display a summary of input parameters.
    
    Args:
        params: Dictionary of input parameters
    """
    with st.expander("📝 Input Parameters Summary"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Price Parameters:**")
            st.write(f"- Spot Price (S): ${params['spot']:.2f}")
            st.write(f"- Strike Price (K): ${params['strike']:.2f}")
            st.write(f"- Moneyness (S/K): {params['spot']/params['strike']:.4f}")
        
        with col2:
            st.markdown("**Market Parameters:**")
            st.write(f"- Time to Maturity: {params['time_to_maturity']:.4f} years ({int(params['time_to_maturity']*365)} days)")
            st.write(f"- Risk-Free Rate: {params['risk_free_rate']*100:.2f}%")
            st.write(f"- Volatility: {params['volatility']*100:.2f}%")


def display_model_comparison(prices: Dict[str, float], option_type: str):
    """
    Display comparison between different pricing models.
    
    Args:
        prices: Dictionary with model names as keys and prices as values
        option_type: 'call' or 'put'
    """
    st.markdown("### 🔬 Model Comparison")
    
    # Create comparison dataframe
    comparison_df = pd.DataFrame([
        {
            'Model': model,
            'Price': f"${price:.4f}",
            'Price (numeric)': price
        }
        for model, price in prices.items()
    ])
    
    # Display as metrics
    cols = st.columns(len(prices))
    for idx, (model, price) in enumerate(prices.items()):
        with cols[idx]:
            st.metric(
                label=model,
                value=f"${price:.4f}"
            )
    
    # Show differences
    if len(prices) > 1:
        with st.expander("📊 Price Differences"):
            st.dataframe(
                comparison_df[['Model', 'Price']],
                use_container_width=True,
                hide_index=True
            )
            
            # Calculate and show standard deviation
            prices_list = list(prices.values())
            import numpy as np
            std_dev = np.std(prices_list)
            mean_price = np.mean(prices_list)
            
            st.write(f"**Mean Price:** ${mean_price:.4f}")
            st.write(f"**Std Deviation:** ${std_dev:.6f}")
            st.write(f"**Coefficient of Variation:** {(std_dev/mean_price)*100:.4f}%")


def display_payoff_info(params: Dict):
    """
    Display payoff information and intrinsic value.
    
    Args:
        params: Dictionary of input parameters
    """
    st.markdown("### 💰 Payoff Analysis")
    
    spot = params['spot']
    strike = params['strike']
    option_type = params['option_type']
    
    # Calculate intrinsic value
    if option_type == 'call':
        intrinsic_value = max(spot - strike, 0)
    else:  # put
        intrinsic_value = max(strike - spot, 0)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Intrinsic Value",
            value=f"${intrinsic_value:.4f}",
            help="Immediate exercise value"
        )
    
    with col2:
        # This will be filled by the calling function with actual option price
        st.metric(
            label="Time Value",
            value="Calculate first",
            help="Extrinsic value = Option Price - Intrinsic Value"
        )
    
    with col3:
        if intrinsic_value > 0:
            status = "✅ In-The-Money"
            color = "green"
        else:
            status = "❌ Out-of-The-Money"
            color = "red"
        
        st.markdown(f"**Status:** <span style='color:{color}'>{status}</span>", 
                   unsafe_allow_html=True)


def display_time_value(option_price: float, intrinsic_value: float):
    """
    Display time value calculation.
    
    Args:
        option_price: Calculated option price
        intrinsic_value: Intrinsic value of the option
    """
    time_value = option_price - intrinsic_value
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Option Price",
            value=f"${option_price:.4f}"
        )
    
    with col2:
        st.metric(
            label="Time Value",
            value=f"${time_value:.4f}",
            delta=f"{(time_value/option_price)*100:.2f}% of total value"
        )
