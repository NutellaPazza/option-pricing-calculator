"""
Option Pricing Calculator - Phase 3
Includes Monte Carlo and Binomial Tree models
"""

import streamlit as st
from models.black_scholes import BlackScholesModel
from models.monte_carlo import MonteCarloModel
from models.binomial_tree import BinomialTreeModel
from calculations.greeks import GreeksCalculator
from ui.sidebar import render_sidebar, render_sidebar_footer
from ui.results import display_option_price, display_greeks
from config.settings import APP_INFO

st.set_page_config(
    page_title=APP_INFO['title'],
    page_icon=APP_INFO['icon'],
    layout="wide"
)

def main():
    st.title(f"{APP_INFO['icon']} {APP_INFO['title']}")
    st.markdown(f"*{APP_INFO['description']}*")
    st.markdown("---")
    
    params = render_sidebar()
    render_sidebar_footer()
    
    # Initialize all models
    bs_model = BlackScholesModel()
    mc_model = MonteCarloModel(num_simulations=10000, random_seed=42)
    bin_model = BinomialTreeModel(num_steps=200)
    greeks_calc = GreeksCalculator()
    
    # Select active model
    if params['model'] == 'Monte Carlo':
        pricing_model = mc_model
    elif params['model'] == 'Binomial Tree':
        pricing_model = bin_model
    else:
        pricing_model = bs_model
    
    st.success(f"✅ Using {params['model']} model")
    
    # Calculate price
    price = pricing_model.calculate_price(
        spot=params['spot'],
        strike=params['strike'],
        time_to_maturity=params['time_to_maturity'],
        risk_free_rate=params['risk_free_rate'],
        volatility=params['volatility'],
        option_type=params['option_type']
    )
    
    display_option_price(price, params['option_type'], params['model'])
    
    # Show confidence interval for Monte Carlo
    if params['model'] == 'Monte Carlo':
        _, lower, upper = mc_model.calculate_with_confidence(
            spot=params['spot'],
            strike=params['strike'],
            time_to_maturity=params['time_to_maturity'],
            risk_free_rate=params['risk_free_rate'],
            volatility=params['volatility'],
            option_type=params['option_type']
        )
        st.info(f"📊 95% CI: [${lower:.4f}, ${upper:.4f}]")
    
    # Show Greeks for Black-Scholes
    if params['model'] == 'Black-Scholes':
        greeks = greeks_calc.calculate_all_greeks(
            spot=params['spot'],
            strike=params['strike'],
            time_to_maturity=params['time_to_maturity'],
            risk_free_rate=params['risk_free_rate'],
            volatility=params['volatility'],
            option_type=params['option_type']
        )
        st.markdown("---")
        display_greeks(greeks)

if __name__ == "__main__":
    main()
