"""
Sidebar component for Option Pricing Calculator.
Handles user input for option parameters.
"""

import streamlit as st
from config.settings import DEFAULT_PARAMS, VALIDATION_RANGES


def render_sidebar():
    """
    Render the sidebar with input parameters for option pricing.
    
    Returns:
        dict: Dictionary containing all user-selected parameters
    """
    st.sidebar.header("📊 Option Parameters")
    
    # Option Type Selection
    option_type = st.sidebar.selectbox(
        "Option Type",
        options=["Call", "Put"],
        index=0,
        help="Select Call or Put option"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("💰 Price Parameters")
    
    # Spot Price
    spot_price = st.sidebar.number_input(
        "Spot Price (S)",
        min_value=VALIDATION_RANGES['spot_price'][0],
        max_value=VALIDATION_RANGES['spot_price'][1],
        value=DEFAULT_PARAMS['spot_price'],
        step=1.0,
        help="Current price of the underlying asset"
    )
    
    # Strike Price
    strike_price = st.sidebar.number_input(
        "Strike Price (K)",
        min_value=VALIDATION_RANGES['strike_price'][0],
        max_value=VALIDATION_RANGES['strike_price'][1],
        value=DEFAULT_PARAMS['strike_price'],
        step=1.0,
        help="Exercise price of the option"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("⏱️ Time & Rate Parameters")
    
    # Time to Maturity
    time_to_maturity = st.sidebar.number_input(
        "Time to Maturity (T) - Years",
        min_value=VALIDATION_RANGES['time_to_maturity'][0],
        max_value=VALIDATION_RANGES['time_to_maturity'][1],
        value=DEFAULT_PARAMS['time_to_maturity'],
        step=0.1,
        format="%.2f",
        help="Time until option expiration in years"
    )
    
    # Alternative: Days input
    with st.sidebar.expander("📅 Or enter in days"):
        days = st.number_input(
            "Days to Maturity",
            min_value=1,
            max_value=3650,
            value=int(DEFAULT_PARAMS['time_to_maturity'] * 365),
            step=1,
            help="Time to maturity in calendar days"
        )
        time_to_maturity = days / 365.0
    
    # Risk-Free Rate
    risk_free_rate = st.sidebar.number_input(
        "Risk-Free Rate (r)",
        min_value=VALIDATION_RANGES['risk_free_rate'][0],
        max_value=VALIDATION_RANGES['risk_free_rate'][1],
        value=DEFAULT_PARAMS['risk_free_rate'],
        step=0.01,
        format="%.4f",
        help="Annual risk-free interest rate (e.g., 0.05 = 5%)"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📈 Volatility Parameter")
    
    # Volatility
    volatility = st.sidebar.number_input(
        "Volatility (σ)",
        min_value=VALIDATION_RANGES['volatility'][0],
        max_value=VALIDATION_RANGES['volatility'][1],
        value=DEFAULT_PARAMS['volatility'],
        step=0.01,
        format="%.4f",
        help="Annual volatility of the underlying asset (e.g., 0.20 = 20%)"
    )
    
    # Display as percentage
    st.sidebar.caption(f"Volatility: {volatility * 100:.2f}%")
    
    # Moneyness indicator
    st.sidebar.markdown("---")
    st.sidebar.subheader("📍 Moneyness")
    
    moneyness = spot_price / strike_price
    if moneyness > 1.05:
        moneyness_label = "🟢 In-The-Money (ITM)"
        color = "green"
    elif moneyness < 0.95:
        moneyness_label = "🔴 Out-of-The-Money (OTM)"
        color = "red"
    else:
        moneyness_label = "🟡 At-The-Money (ATM)"
        color = "orange"
    
    st.sidebar.markdown(
        f"<p style='color: {color}; font-weight: bold;'>{moneyness_label}</p>",
        unsafe_allow_html=True
    )
    st.sidebar.caption(f"S/K Ratio: {moneyness:.4f}")
    
    # Model Selection
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔬 Pricing Model")
    
    model_choice = st.sidebar.selectbox(
        "Select Model",
        options=["Black-Scholes", "Monte Carlo", "Binomial Tree"],
        index=0,
        help="Choose the pricing model to use"
    )
    
    # Model-specific parameters
    additional_params = {}
    
    if model_choice == "Monte Carlo":
        with st.sidebar.expander("⚙️ Monte Carlo Settings"):
            additional_params['simulations'] = st.number_input(
                "Number of Simulations",
                min_value=10000,
                max_value=1000000,
                value=100000,
                step=10000,
                help="More simulations = more accurate but slower"
            )
            additional_params['seed'] = st.number_input(
                "Random Seed",
                min_value=0,
                max_value=9999,
                value=42,
                help="For reproducible results"
            )
    
    elif model_choice == "Binomial Tree":
        with st.sidebar.expander("⚙️ Binomial Tree Settings"):
            additional_params['steps'] = st.number_input(
                "Number of Steps",
                min_value=10,
                max_value=500,
                value=100,
                step=10,
                help="More steps = more accurate but slower"
            )
            additional_params['american'] = st.checkbox(
                "American Option",
                value=False,
                help="Allow early exercise"
            )
    
    # Reset to defaults button
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Reset to Defaults"):
        st.rerun()
    
    # Return all parameters
    return {
        'spot': spot_price,
        'strike': strike_price,
        'time_to_maturity': time_to_maturity,
        'risk_free_rate': risk_free_rate,
        'volatility': volatility,
        'option_type': option_type.lower(),
        'model': model_choice,
        'additional_params': additional_params
    }


def render_sidebar_footer():
    """Render footer in sidebar with developer info."""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👨‍💻 About")
    
    with st.sidebar.expander("Developer Info"):
        st.markdown("""
        **Giovanni Destasio**
        
        🎓 *Financial Engineer & Developer*
        
        📧 giovanni.destasio@example.com
        
        💼 [LinkedIn](https://linkedin.com/in/giovanni-destasio)
        
        🐙 [GitHub](https://github.com/giovannidestasio)
        
        ---
        
        *This project implements various option pricing models using Python and Streamlit.*
        """)
