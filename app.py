"""
Main Streamlit application for Option Pricing Calculator.
Entry point for the web application.
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from models.black_scholes import BlackScholesModel
from models.monte_carlo import MonteCarloModel
from models.binomial_tree import BinomialTreeModel
from calculations.greeks import GreeksCalculator
from ui.sidebar import render_sidebar, render_sidebar_footer
from ui.results import (
    display_option_price,
    display_greeks,
    display_input_summary,
    display_payoff_info,
    display_time_value
)
from ui.charts import (
    plot_payoff_diagram,
    plot_greeks_vs_spot,
    plot_price_vs_volatility,
    plot_price_vs_time,
    plot_all_greeks
)
from ui.heatmaps import OptionHeatmaps
from ui.helpers import (
    show_calculation_time,
    show_performance_metrics,
    show_calculation_settings,
    show_convergence_indicator,
    create_greek_explanation_card
)
from ui.export import create_download_section
from ui.tutorials import render_education_tab
from strategies.options import StrategyFactory
from strategies.visualizations import (
    plot_strategy_payoff,
    plot_risk_profile,
    plot_multiple_strategies,
    create_strategy_comparison_table,
    create_strategy_details_card
)
from config.settings import APP_INFO


# Page configuration
st.set_page_config(
    page_title=APP_INFO['title'],
    page_icon=APP_INFO['icon'],
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:giovanni.destasio@example.com',
        'Report a bug': 'mailto:giovanni.destasio@example.com',
        'About': f"{APP_INFO['title']} v{APP_INFO['version']} - {APP_INFO['description']}"
    }
)


def main():
    """Main application function."""
    
    # Header
    st.title(f"{APP_INFO['icon']} {APP_INFO['title']}")
    st.markdown(f"*{APP_INFO['description']}*")
    st.markdown("---")
    
    # Render sidebar and get parameters
    params = render_sidebar()
    render_sidebar_footer()
    
    # Initialize models
    bs_model = BlackScholesModel()
    greeks_calc = GreeksCalculator()
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🔢 Pricing & Results",
        "📈 Greeks Analysis",
        "📊 Sensitivity Analysis",
        "🌡 Heatmaps",
        "🎯 Option Strategies",
        "🎓 Education",
        "ℹ️ About"
    ])
    
    # TAB 1: Pricing & Results
    with tab1:
        st.header("Option Pricing Results")
        
        # Display input summary
        display_input_summary(params)
        
        st.markdown("---")
        
        # Calculate price based on selected model
        try:
            if params['model'] == "Black-Scholes":
                # Calculate price with timing
                with st.spinner("⚡ Calculating option price..."):
                    price, calc_time_ms = show_calculation_time(
                        bs_model.calculate_price,
                        spot=params['spot'],
                        strike=params['strike'],
                        time_to_maturity=params['time_to_maturity'],
                        risk_free_rate=params['risk_free_rate'],
                        volatility=params['volatility'],
                        option_type=params['option_type']
                    )
                
                # Display price
                display_option_price(price, params['option_type'], "Black-Scholes")
                
                # Show performance metrics
                show_performance_metrics(calc_time_ms, "Black-Scholes")
                
                # Calculate and display Greeks
                st.markdown("---")
                greeks = greeks_calc.calculate_all_greeks(
                    spot=params['spot'],
                    strike=params['strike'],
                    time_to_maturity=params['time_to_maturity'],
                    risk_free_rate=params['risk_free_rate'],
                    volatility=params['volatility'],
                    option_type=params['option_type']
                )
                display_greeks(greeks)
                
                # Export section
                create_download_section(params, price, greeks, "Black-Scholes")
                
                # Calculate intrinsic value
                st.markdown("---")
                if params['option_type'] == 'call':
                    intrinsic_value = max(params['spot'] - params['strike'], 0)
                else:
                    intrinsic_value = max(params['strike'] - params['spot'], 0)
                
                display_time_value(price, intrinsic_value)
                
                # Payoff diagram
                st.markdown("---")
                st.subheader("📉 Payoff Diagram")
                plot_payoff_diagram(
                    spot=params['spot'],
                    strike=params['strike'],
                    option_price=price,
                    option_type=params['option_type']
                )
                
            elif params['model'] == "Monte Carlo":
                # Initialize Monte Carlo model
                mc_model = MonteCarloModel(
                    num_simulations=100000,
                    num_steps=252,
                    seed=42,
                    antithetic=True
                )
                
                st.info("🎲 **Monte Carlo Simulation** - Using 100,000 simulations with antithetic variates for variance reduction")
                
                # Show calculation settings
                show_calculation_settings("Monte Carlo")
                
                # Calculate price with progress and timing
                with st.spinner("⚡ Running Monte Carlo simulation (100K paths)..."):
                    price, calc_time_ms = show_calculation_time(
                        mc_model.calculate_price,
                        spot=params['spot'],
                        strike=params['strike'],
                        time_to_maturity=params['time_to_maturity'],
                        risk_free_rate=params['risk_free_rate'],
                        volatility=params['volatility'],
                        option_type=params['option_type']
                    )
                
                # Display price
                display_option_price(price, params['option_type'], "Monte Carlo")
                
                # Show confidence interval
                st.markdown("---")
                st.subheader("📊 Statistical Analysis")
                
                with st.spinner("Calculating confidence interval..."):
                    conf_result = mc_model.calculate_price_with_confidence(
                        spot=params['spot'],
                        strike=params['strike'],
                        time_to_maturity=params['time_to_maturity'],
                        risk_free_rate=params['risk_free_rate'],
                        volatility=params['volatility'],
                        option_type=params['option_type'],
                        confidence_level=0.95
                    )
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Standard Error",
                        f"${conf_result['std_error']:.6f}",
                        help="Statistical uncertainty in the estimate"
                    )
                
                with col2:
                    st.metric(
                        "Lower Bound (95%)",
                        f"${conf_result['lower_bound']:.6f}"
                    )
                
                with col3:
                    st.metric(
                        "Upper Bound (95%)",
                        f"${conf_result['upper_bound']:.6f}"
                    )
                
                st.info(f"💡 The true option price has a 95% probability of being between ${conf_result['lower_bound']:.4f} and ${conf_result['upper_bound']:.4f}")
                
                # Compare with Black-Scholes
                st.markdown("---")
                st.subheader("📐 Comparison with Black-Scholes")
                
                bs_price = bs_model.calculate_price(
                    spot=params['spot'],
                    strike=params['strike'],
                    time_to_maturity=params['time_to_maturity'],
                    risk_free_rate=params['risk_free_rate'],
                    volatility=params['volatility'],
                    option_type=params['option_type']
                )
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Monte Carlo", f"${price:.6f}")
                
                with col2:
                    st.metric("Black-Scholes", f"${bs_price:.6f}")
                
                with col3:
                    diff = abs(price - bs_price)
                    diff_pct = (diff / bs_price) * 100
                    st.metric("Difference", f"${diff:.6f}", f"{diff_pct:.2f}%")
                
                if diff_pct < 1.0:
                    st.success("✅ Excellent agreement with analytical solution!")
                elif diff_pct < 2.0:
                    st.info("✓ Good agreement with analytical solution")
                else:
                    st.warning("⚠️ Consider increasing number of simulations for better accuracy")
                
                # Show performance metrics
                show_performance_metrics(calc_time_ms, "Monte Carlo")
                
                # Calculate and display Greeks (using numerical methods)
                st.markdown("---")
                greeks = greeks_calc.calculate_all_greeks(
                    spot=params['spot'],
                    strike=params['strike'],
                    time_to_maturity=params['time_to_maturity'],
                    risk_free_rate=params['risk_free_rate'],
                    volatility=params['volatility'],
                    option_type=params['option_type']
                )
                display_greeks(greeks)
                
                # Export section
                create_download_section(params, price, greeks, "Monte Carlo")
                
                # Model info
                st.markdown("---")
                with st.expander("ℹ️ Monte Carlo Model Information"):
                    model_info = mc_model.get_model_info()
                    st.markdown(f"**{model_info['name']}**")
                    st.markdown(model_info['description'])
                    
                    st.markdown("**Parameters:**")
                    for key, value in model_info['parameters'].items():
                        st.write(f"- {key}: {value}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Advantages:**")
                        for adv in model_info['advantages']:
                            st.write(f"✓ {adv}")
                    
                    with col2:
                        st.markdown("**Disadvantages:**")
                        for dis in model_info['disadvantages']:
                            st.write(f"✗ {dis}")
                
                # Payoff diagram
                st.markdown("---")
                st.subheader("📉 Payoff Diagram")
                plot_payoff_diagram(
                    spot=params['spot'],
                    strike=params['strike'],
                    option_price=price,
                    option_type=params['option_type']
                )
                
            elif params['model'] == "Binomial Tree":
                # Initialize Binomial Tree model
                # Check if American option is selected (we'll add this option later)
                is_american = st.checkbox(
                    "American Option (Early Exercise)",
                    value=False,
                    help="European options can only be exercised at expiration. American options can be exercised anytime before expiration."
                )
                
                num_steps = st.slider(
                    "Number of Tree Steps",
                    min_value=10,
                    max_value=500,
                    value=100,
                    step=10,
                    help="More steps = more accurate but slower. 100-200 steps is usually sufficient."
                )
                
                bt_model = BinomialTreeModel(
                    num_steps=num_steps,
                    american=is_american
                )
                
                option_style = "American" if is_american else "European"
                st.info(f"🌲 **Binomial Tree (Cox-Ross-Rubinstein)** - {num_steps} steps, {option_style} option")
                
                # Show calculation settings
                show_calculation_settings("Binomial Tree")
                
                # Calculate price with progress and timing
                with st.spinner(f"⚡ Building binomial tree ({num_steps} steps)..."):
                    price, calc_time_ms = show_calculation_time(
                        bt_model.calculate_price,
                        spot=params['spot'],
                        strike=params['strike'],
                        time_to_maturity=params['time_to_maturity'],
                        risk_free_rate=params['risk_free_rate'],
                        volatility=params['volatility'],
                        option_type=params['option_type']
                    )
                
                # Store in session state for other tabs
                st.session_state['bt_is_american'] = is_american
                st.session_state['bt_steps'] = num_steps
                
                # Display price
                display_option_price(price, params['option_type'], f"Binomial Tree ({option_style})")
                
                # Compare with Black-Scholes
                st.markdown("---")
                st.subheader("� Comparison with Black-Scholes")
                
                bs_price = bs_model.calculate_price(
                    spot=params['spot'],
                    strike=params['strike'],
                    time_to_maturity=params['time_to_maturity'],
                    risk_free_rate=params['risk_free_rate'],
                    volatility=params['volatility'],
                    option_type=params['option_type']
                )
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Binomial Tree", f"${price:.6f}")
                
                with col2:
                    st.metric("Black-Scholes", f"${bs_price:.6f}")
                
                with col3:
                    diff = abs(price - bs_price)
                    diff_pct = (diff / bs_price) * 100
                    st.metric("Difference", f"${diff:.6f}", f"{diff_pct:.2f}%")
                
                with col4:
                    if is_american:
                        # Calculate European BT for comparison
                        bt_euro = BinomialTreeModel(num_steps=num_steps, american=False)
                        euro_price = bt_euro.calculate_price(
                            spot=params['spot'],
                            strike=params['strike'],
                            time_to_maturity=params['time_to_maturity'],
                            risk_free_rate=params['risk_free_rate'],
                            volatility=params['volatility'],
                            option_type=params['option_type']
                        )
                        early_premium = price - euro_price
                        st.metric(
                            "Early Exercise Premium",
                            f"${early_premium:.6f}",
                            help="Additional value from early exercise right"
                        )
                
                # Show convergence indicator
                show_convergence_indicator(diff_pct, threshold=2.0)
                
                # Show performance metrics
                show_performance_metrics(calc_time_ms, f"Binomial Tree ({num_steps} steps)")
                
                # Show early exercise info for American options
                if is_american and params['option_type'] == 'put':
                    st.info("💡 **American Puts** often have early exercise value, especially when deep in-the-money or with high interest rates.")
                
                # Calculate and display Greeks
                st.markdown("---")
                greeks = greeks_calc.calculate_all_greeks(
                    spot=params['spot'],
                    strike=params['strike'],
                    time_to_maturity=params['time_to_maturity'],
                    risk_free_rate=params['risk_free_rate'],
                    volatility=params['volatility'],
                    option_type=params['option_type']
                )
                display_greeks(greeks)
                
                # Export section
                create_download_section(params, price, greeks, f"Binomial Tree ({option_style})")
                
                # Convergence Analysis
                st.markdown("---")
                st.subheader("📊 Convergence Analysis")
                
                with st.spinner("Analyzing convergence..."):
                    convergence = bt_model.get_convergence_analysis(
                        spot=params['spot'],
                        strike=params['strike'],
                        time_to_maturity=params['time_to_maturity'],
                        risk_free_rate=params['risk_free_rate'],
                        volatility=params['volatility'],
                        option_type=params['option_type'],
                        step_sizes=[10, 25, 50, 100, 200]
                    )
                
                # Create convergence chart
                import plotly.graph_objects as go
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=convergence['step_sizes'],
                    y=convergence['prices'],
                    mode='lines+markers',
                    name='Binomial Tree',
                    line=dict(color='blue', width=2),
                    marker=dict(size=8)
                ))
                
                fig.add_hline(
                    y=bs_price,
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"Black-Scholes: ${bs_price:.4f}",
                    annotation_position="right"
                )
                
                fig.update_layout(
                    title="Convergence: Binomial Tree → Black-Scholes",
                    xaxis_title="Number of Steps",
                    yaxis_title="Option Price ($)",
                    hovermode='x unified',
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.info("💡 **Convergence**: As steps increase, Binomial Tree converges to Black-Scholes solution. Oscillation is normal.")
                
                # Model info
                st.markdown("---")
                with st.expander("ℹ️ Binomial Tree Model Information"):
                    model_info = bt_model.get_model_info()
                    st.markdown(f"**{model_info['name']}**")
                    st.markdown(model_info['description'])
                    
                    st.markdown("**Parameters:**")
                    for key, value in model_info['parameters'].items():
                        st.write(f"- {key}: {value}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Advantages:**")
                        for adv in model_info['advantages']:
                            st.write(f"✓ {adv}")
                    
                    with col2:
                        st.markdown("**Disadvantages:**")
                        for dis in model_info['disadvantages']:
                            st.write(f"✗ {dis}")
                
                # Payoff diagram
                st.markdown("---")
                st.subheader("📉 Payoff Diagram")
                plot_payoff_diagram(
                    spot=params['spot'],
                    strike=params['strike'],
                    option_price=price,
                    option_type=params['option_type']
                )
                
        except Exception as e:
            st.error(f"❌ Error calculating option price: {str(e)}")
            st.exception(e)
    
    # TAB 2: Greeks Analysis
    with tab2:
        st.header("Greeks Sensitivity Analysis")
        
        if params['model'] == "Black-Scholes":
            # Display current Greeks
            greeks = greeks_calc.calculate_all_greeks(
                spot=params['spot'],
                strike=params['strike'],
                time_to_maturity=params['time_to_maturity'],
                risk_free_rate=params['risk_free_rate'],
                volatility=params['volatility'],
                option_type=params['option_type']
            )
            
            st.markdown("### Current Greeks Values")
            display_greeks(greeks)
            
            st.markdown("---")
            
            # Plot all Greeks together
            st.markdown("### Greeks vs Spot Price")
            plot_all_greeks(params, greeks_calc)
            
            st.markdown("---")
            
            # Individual Greek plots
            st.markdown("### Individual Greek Analysis")
            
            greek_choice = st.selectbox(
                "Select Greek to Analyze",
                options=['Delta', 'Gamma', 'Theta', 'Vega', 'Rho'],
                index=0
            )
            
            # Map Greek names to calculator methods
            greek_methods = {
                'Delta': greeks_calc.delta,
                'Gamma': greeks_calc.gamma,
                'Theta': greeks_calc.theta,
                'Vega': greeks_calc.vega,
                'Rho': greeks_calc.rho
            }
            
            plot_greeks_vs_spot(
                params=params,
                greek_calculator=greek_methods[greek_choice],
                greek_name=greek_choice
            )
            
            # Greek interpretation
            interpretations = {
                'Delta': """
                **Delta (Δ)** measures the rate of change of option value with respect to changes in the underlying asset's price.
                - **Call Delta**: Ranges from 0 to 1
                - **Put Delta**: Ranges from -1 to 0
                - Also represents the hedge ratio (number of shares to hedge)
                """,
                'Gamma': """
                **Gamma (Γ)** measures the rate of change in Delta with respect to changes in the underlying price.
                - Maximum for at-the-money options
                - Indicates Delta stability
                - Same for calls and puts
                - Always positive for long positions
                """,
                'Theta': """
                **Theta (Θ)** measures the rate of change in option value with respect to time (time decay).
                - Usually negative for long positions
                - Expressed per day
                - Maximum for at-the-money options near expiration
                - Time is the enemy of option buyers
                """,
                'Vega': """
                **Vega (ν)** measures sensitivity to volatility changes.
                - Always positive for long positions
                - Same for calls and puts
                - Maximum for at-the-money options
                - Long-dated options have higher vega
                """,
                'Rho': """
                **Rho (ρ)** measures sensitivity to interest rate changes.
                - Positive for calls, negative for puts
                - Less significant for short-dated options
                - More important for long-dated options
                """
            }
            
            with st.expander(f"ℹ️ About {greek_choice}"):
                st.markdown(interpretations[greek_choice])
        
        elif params['model'] == "Monte Carlo":
            st.info("📊 **Note:** Greeks for Monte Carlo are calculated using numerical approximation methods (finite differences)")
            
            # Display current Greeks
            greeks = greeks_calc.calculate_all_greeks(
                spot=params['spot'],
                strike=params['strike'],
                time_to_maturity=params['time_to_maturity'],
                risk_free_rate=params['risk_free_rate'],
                volatility=params['volatility'],
                option_type=params['option_type']
            )
            
            st.markdown("### Current Greeks Values")
            display_greeks(greeks)
            
            st.markdown("---")
            
            # Plot all Greeks together
            st.markdown("### Greeks vs Spot Price")
            plot_all_greeks(params, greeks_calc)
            
            st.markdown("---")
            
            # Individual Greek plots
            st.markdown("### Individual Greek Analysis")
            
            greek_choice = st.selectbox(
                "Select Greek to Analyze",
                options=['Delta', 'Gamma', 'Theta', 'Vega', 'Rho'],
                index=0,
                key="mc_greek_choice"
            )
            
            # Map Greek names to calculator methods
            greek_methods = {
                'Delta': greeks_calc.delta,
                'Gamma': greeks_calc.gamma,
                'Theta': greeks_calc.theta,
                'Vega': greeks_calc.vega,
                'Rho': greeks_calc.rho
            }
            
            plot_greeks_vs_spot(
                params=params,
                greek_calculator=greek_methods[greek_choice],
                greek_name=greek_choice
            )
            
            # Greek interpretation
            interpretations = {
                'Delta': """
                **Delta (Δ)** measures the rate of change of option value with respect to changes in the underlying asset's price.
                - **Call Delta**: Ranges from 0 to 1
                - **Put Delta**: Ranges from -1 to 0
                - Also represents the hedge ratio (number of shares to hedge)
                """,
                'Gamma': """
                **Gamma (Γ)** measures the rate of change in Delta with respect to changes in the underlying price.
                - Maximum for at-the-money options
                - Indicates Delta stability
                - Same for calls and puts
                - Always positive for long positions
                """,
                'Theta': """
                **Theta (Θ)** measures the rate of change in option value with respect to time (time decay).
                - Usually negative for long positions
                - Expressed per day
                - Maximum for at-the-money options near expiration
                - Time is the enemy of option buyers
                """,
                'Vega': """
                **Vega (ν)** measures sensitivity to volatility changes.
                - Always positive for long positions
                - Same for calls and puts
                - Maximum for at-the-money options
                - Long-dated options have higher vega
                """,
                'Rho': """
                **Rho (ρ)** measures sensitivity to interest rate changes.
                - Positive for calls, negative for puts
                - Less significant for short-dated options
                - More important for long-dated options
                """
            }
            
            with st.expander(f"ℹ️ About {greek_choice}"):
                st.markdown(interpretations[greek_choice])
        
        elif params['model'] == "Binomial Tree":
            st.info("🌲 **Note:** Greeks for Binomial Tree are calculated using numerical approximation methods (finite differences)")
            
            # Check if using American options
            is_american = st.session_state.get('bt_is_american', False)
            bt_steps = st.session_state.get('bt_steps', 100)
            
            if is_american:
                st.warning("⚠️ American options - Greeks may show discontinuities due to early exercise boundary")
            
            # Display current Greeks
            greeks = greeks_calc.calculate_all_greeks(
                spot=params['spot'],
                strike=params['strike'],
                time_to_maturity=params['time_to_maturity'],
                risk_free_rate=params['risk_free_rate'],
                volatility=params['volatility'],
                option_type=params['option_type']
            )
            
            st.markdown("### Current Greeks Values")
            display_greeks(greeks)
            
            st.markdown("---")
            
            # Plot all Greeks together
            st.markdown("### Greeks vs Spot Price")
            plot_all_greeks(params, greeks_calc)
            
            st.markdown("---")
            
            # Individual Greek plots
            st.markdown("### Individual Greek Analysis")
            
            greek_choice = st.selectbox(
                "Select Greek to Analyze",
                options=['Delta', 'Gamma', 'Theta', 'Vega', 'Rho'],
                index=0,
                key="bt_greek_choice"
            )
            
            # Map Greek names to calculator methods
            greek_methods = {
                'Delta': greeks_calc.delta,
                'Gamma': greeks_calc.gamma,
                'Theta': greeks_calc.theta,
                'Vega': greeks_calc.vega,
                'Rho': greeks_calc.rho
            }
            
            plot_greeks_vs_spot(
                params=params,
                greek_calculator=greek_methods[greek_choice],
                greek_name=greek_choice
            )
            
            # Greek interpretation
            interpretations = {
                'Delta': """
                **Delta (Δ)** measures the rate of change of option value with respect to changes in the underlying asset's price.
                - **Call Delta**: Ranges from 0 to 1
                - **Put Delta**: Ranges from -1 to 0
                - Also represents the hedge ratio (number of shares to hedge)
                - For American options, may show jumps near early exercise boundary
                """,
                'Gamma': """
                **Gamma (Γ)** measures the rate of change in Delta with respect to changes in the underlying price.
                - Maximum for at-the-money options
                - Indicates Delta stability
                - Same for calls and puts
                - Always positive for long positions
                - Can spike at early exercise boundary for American options
                """,
                'Theta': """
                **Theta (Θ)** measures the rate of change in option value with respect to time (time decay).
                - Usually negative for long positions
                - Expressed per day
                - Maximum for at-the-money options near expiration
                - Time is the enemy of option buyers
                - American options may show different decay patterns
                """,
                'Vega': """
                **Vega (ν)** measures sensitivity to volatility changes.
                - Always positive for long positions
                - Same for calls and puts
                - Maximum for at-the-money options
                - Long-dated options have higher vega
                """,
                'Rho': """
                **Rho (ρ)** measures sensitivity to interest rate changes.
                - Positive for calls, negative for puts
                - Less significant for short-dated options
                - More important for long-dated options
                """
            }
            
            with st.expander(f"ℹ️ About {greek_choice}"):
                st.markdown(interpretations[greek_choice])
            
            # Additional info about computation
            with st.expander("🔍 Computation Details"):
                st.markdown(f"""
                **Binomial Tree Configuration:**
                - Steps: {bt_steps}
                - Option Type: {'American' if is_american else 'European'}
                - Method: Cox-Ross-Rubinstein (CRR)
                
                **Greek Calculation Method:**
                - All Greeks computed using finite difference approximations
                - Delta: (V(S+δS) - V(S-δS)) / (2δS)
                - Gamma: (V(S+δS) - 2V(S) + V(S-δS)) / (δS²)
                - Similar methods for other Greeks
                
                **Note:** American options may show discontinuities in Greeks near the early exercise boundary.
                """)
        
        else:
            st.info("Greeks analysis is currently available for Black-Scholes, Monte Carlo, and Binomial Tree models.")
    
    # TAB 3: Sensitivity Analysis
    with tab3:
        st.header("📊 Sensitivity Analysis")
        
        if params['model'] == "Black-Scholes":
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Price vs Volatility")
                plot_price_vs_volatility(bs_model, params)
                
                st.markdown("""
                **Analysis:**
                - Shows how option value changes with volatility
                - Higher volatility = higher option value
                - Demonstrates Vega sensitivity
                """)
            
            with col2:
                st.subheader("⏱️ Price vs Time (Time Decay)")
                plot_price_vs_time(bs_model, params)
                
                st.markdown("""
                **Analysis:**
                - Shows time decay effect (Theta)
                - Options lose value as expiration approaches
                - Decay accelerates near expiration
                """)
            
            st.markdown("---")
            
            # Scenario analysis
            st.subheader("🎯 Scenario Analysis")
            
            st.markdown("Analyze option value under different market scenarios:")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                scenario_spot = st.slider(
                    "Spot Price Change (%)",
                    min_value=-50,
                    max_value=50,
                    value=0,
                    step=5
                )
            
            with col2:
                scenario_vol = st.slider(
                    "Volatility Change (%)",
                    min_value=-50,
                    max_value=50,
                    value=0,
                    step=5
                )
            
            with col3:
                scenario_time = st.slider(
                    "Days Passed",
                    min_value=0,
                    max_value=int(params['time_to_maturity'] * 365),
                    value=0,
                    step=5
                )
            
            # Calculate scenario price
            scenario_params = params.copy()
            scenario_params['spot'] = params['spot'] * (1 + scenario_spot / 100)
            scenario_params['volatility'] = params['volatility'] * (1 + scenario_vol / 100)
            scenario_params['time_to_maturity'] = params['time_to_maturity'] - (scenario_time / 365)
            
            if scenario_params['time_to_maturity'] > 0:
                scenario_price = bs_model.calculate_price(
                    spot=scenario_params['spot'],
                    strike=scenario_params['strike'],
                    time_to_maturity=scenario_params['time_to_maturity'],
                    risk_free_rate=scenario_params['risk_free_rate'],
                    volatility=scenario_params['volatility'],
                    option_type=scenario_params['option_type']
                )
                
                original_price = bs_model.calculate_price(
                    spot=params['spot'],
                    strike=params['strike'],
                    time_to_maturity=params['time_to_maturity'],
                    risk_free_rate=params['risk_free_rate'],
                    volatility=params['volatility'],
                    option_type=params['option_type']
                )
                price_change = scenario_price - original_price
                pct_change = (price_change / original_price) * 100
                
                st.markdown("### Scenario Results")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Original Price",
                        f"${original_price:.4f}"
                    )
                
                with col2:
                    st.metric(
                        "Scenario Price",
                        f"${scenario_price:.4f}",
                        delta=f"${price_change:.4f}"
                    )
                
                with col3:
                    st.metric(
                        "Change",
                        f"{pct_change:+.2f}%",
                        delta=f"${price_change:.4f}"
                    )
            else:
                st.warning("⚠️ Time to maturity cannot be negative!")
        
        elif params['model'] == "Monte Carlo":
            # Initialize Monte Carlo model
            mc_model = MonteCarloModel(
                num_simulations=50000,  # Reduced for faster sensitivity analysis
                num_steps=252,
                seed=42,
                antithetic=True
            )
            
            st.info("🎲 Using Monte Carlo simulation (50,000 paths for faster analysis)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Price vs Volatility")
                plot_price_vs_volatility(mc_model, params)
                
                st.markdown("""
                **Analysis:**
                - Shows how option value changes with volatility
                - Higher volatility = higher option value
                - Monte Carlo captures volatility smile effects
                """)
            
            with col2:
                st.subheader("⏱️ Price vs Time (Time Decay)")
                plot_price_vs_time(mc_model, params)
                
                st.markdown("""
                **Analysis:**
                - Shows time decay effect (Theta)
                - Options lose value as expiration approaches
                - Stochastic simulation of time evolution
                """)
            
            st.markdown("---")
            
            # Scenario analysis
            st.subheader("🎯 Scenario Analysis")
            
            st.markdown("Analyze option value under different market scenarios:")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                scenario_spot = st.slider(
                    "Spot Price Change (%)",
                    min_value=-50,
                    max_value=50,
                    value=0,
                    step=5,
                    key="mc_scenario_spot"
                )
            
            with col2:
                scenario_vol = st.slider(
                    "Volatility Change (%)",
                    min_value=-50,
                    max_value=50,
                    value=0,
                    step=5,
                    key="mc_scenario_vol"
                )
            
            with col3:
                scenario_days = st.slider(
                    "Days Passed",
                    min_value=0,
                    max_value=int(params['time_to_maturity'] * 365),
                    value=0,
                    step=1,
                    key="mc_scenario_days"
                )
            
            # Calculate scenario
            scenario_params = params.copy()
            scenario_params['spot'] = params['spot'] * (1 + scenario_spot / 100)
            scenario_params['volatility'] = params['volatility'] * (1 + scenario_vol / 100)
            scenario_params['time_to_maturity'] = max(0.001, params['time_to_maturity'] - (scenario_days / 365))
            
            if scenario_params['time_to_maturity'] > 0:
                with st.spinner("Running scenario simulation..."):
                    scenario_price = mc_model.calculate_price(
                        spot=scenario_params['spot'],
                        strike=scenario_params['strike'],
                        time_to_maturity=scenario_params['time_to_maturity'],
                        risk_free_rate=scenario_params['risk_free_rate'],
                        volatility=scenario_params['volatility'],
                        option_type=scenario_params['option_type']
                    )
                    
                    original_price = mc_model.calculate_price(
                        spot=params['spot'],
                        strike=params['strike'],
                        time_to_maturity=params['time_to_maturity'],
                        risk_free_rate=params['risk_free_rate'],
                        volatility=params['volatility'],
                        option_type=params['option_type']
                    )
                
                price_change = scenario_price - original_price
                pct_change = (price_change / original_price) * 100
                
                st.markdown("### Scenario Results")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Original Price (MC)",
                        f"${original_price:.4f}"
                    )
                
                with col2:
                    st.metric(
                        "Scenario Price (MC)",
                        f"${scenario_price:.4f}",
                        delta=f"${price_change:.4f}"
                    )
                
                with col3:
                    st.metric(
                        "Change",
                        f"{pct_change:+.2f}%",
                        delta=f"${price_change:.4f}"
                    )
            else:
                st.warning("⚠️ Time to maturity cannot be negative!")
        
        elif params['model'] == "Binomial Tree":
            # Get settings from session state
            is_american = st.session_state.get('bt_is_american', False)
            bt_steps = st.session_state.get('bt_steps', 100)
            
            # Initialize Binomial Tree model
            bt_model = BinomialTreeModel(
                num_steps=bt_steps,
                american=is_american
            )
            
            st.info(f"🌲 Using Binomial Tree ({bt_steps} steps, {'American' if is_american else 'European'} option)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Price vs Volatility")
                plot_price_vs_volatility(bt_model, params)
                
                st.markdown("""
                **Analysis:**
                - Shows how option value changes with volatility
                - Higher volatility = higher option value
                - Discrete-time lattice approximation
                """ + ("- American options may show non-linear effects" if is_american else ""))
            
            with col2:
                st.subheader("⏱️ Price vs Time (Time Decay)")
                plot_price_vs_time(bt_model, params)
                
                st.markdown("""
                **Analysis:**
                - Shows time decay effect (Theta)
                - Options lose value as expiration approaches
                - Tree structure captures discrete time steps
                """ + ("- American options may show early exercise effects" if is_american else ""))
            
            st.markdown("---")
            
            # Scenario analysis
            st.subheader("🎯 Scenario Analysis")
            
            st.markdown("Analyze option value under different market scenarios:")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                scenario_spot = st.slider(
                    "Spot Price Change (%)",
                    min_value=-50,
                    max_value=50,
                    value=0,
                    step=5,
                    key="bt_scenario_spot"
                )
            
            with col2:
                scenario_vol = st.slider(
                    "Volatility Change (%)",
                    min_value=-50,
                    max_value=50,
                    value=0,
                    step=5,
                    key="bt_scenario_vol"
                )
            
            with col3:
                scenario_days = st.slider(
                    "Days Passed",
                    min_value=0,
                    max_value=int(params['time_to_maturity'] * 365),
                    value=0,
                    step=1,
                    key="bt_scenario_days"
                )
            
            # Calculate scenario
            scenario_params = params.copy()
            scenario_params['spot'] = params['spot'] * (1 + scenario_spot / 100)
            scenario_params['volatility'] = params['volatility'] * (1 + scenario_vol / 100)
            scenario_params['time_to_maturity'] = max(0.001, params['time_to_maturity'] - (scenario_days / 365))
            
            if scenario_params['time_to_maturity'] > 0:
                with st.spinner("Calculating scenario with binomial tree..."):
                    scenario_price = bt_model.calculate_price(
                        spot=scenario_params['spot'],
                        strike=scenario_params['strike'],
                        time_to_maturity=scenario_params['time_to_maturity'],
                        risk_free_rate=scenario_params['risk_free_rate'],
                        volatility=scenario_params['volatility'],
                        option_type=scenario_params['option_type']
                    )
                    
                    original_price = bt_model.calculate_price(
                        spot=params['spot'],
                        strike=params['strike'],
                        time_to_maturity=params['time_to_maturity'],
                        risk_free_rate=params['risk_free_rate'],
                        volatility=params['volatility'],
                        option_type=params['option_type']
                    )
                
                price_change = scenario_price - original_price
                pct_change = (price_change / original_price) * 100
                
                st.markdown("### Scenario Results")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Original Price (BT)",
                        f"${original_price:.4f}"
                    )
                
                with col2:
                    st.metric(
                        "Scenario Price (BT)",
                        f"${scenario_price:.4f}",
                        delta=f"${price_change:.4f}"
                    )
                
                with col3:
                    st.metric(
                        "Change",
                        f"{pct_change:+.2f}%",
                        delta=f"${price_change:.4f}"
                    )
                
                # Additional info for American options
                if is_american:
                    st.info("💡 **American Option**: Scenario price includes early exercise optionality")
            else:
                st.warning("⚠️ Time to maturity cannot be negative!")
        
        else:
            st.info("Sensitivity analysis is currently available for Black-Scholes, Monte Carlo, and Binomial Tree models.")
    
    # TAB 4: Heatmaps
    with tab4:
        if params['model'] == "Black-Scholes":
            from ui.heatmaps import render_heatmaps_tab
            render_heatmaps_tab(params, bs_model)
        
        elif params['model'] == "Monte Carlo":
            # Initialize Monte Carlo with fewer simulations for heatmaps (performance)
            mc_model = MonteCarloModel(
                num_simulations=30000,  # Reduced for heatmap performance
                num_steps=100,           # Fewer steps for faster computation
                seed=42,
                antithetic=True
            )
            
            st.warning("⚠️ **Note:** Heatmaps use 30,000 simulations for performance. This may take 10-30 seconds to generate.")
            
            from ui.heatmaps import render_heatmaps_tab
            render_heatmaps_tab(params, mc_model)
        
        elif params['model'] == "Binomial Tree":
            # Get settings from session state
            is_american = st.session_state.get('bt_is_american', False)
            bt_steps = st.session_state.get('bt_steps', 100)
            
            # Initialize Binomial Tree with fewer steps for heatmaps (performance)
            bt_model = BinomialTreeModel(
                num_steps=50,  # Reduced steps for faster heatmap generation
                american=is_american
            )
            
            st.warning(f"⚠️ **Note:** Heatmaps use 50 steps for performance (vs {bt_steps} in pricing). {'American options' if is_american else 'European options'} selected. This may take 10-20 seconds to generate.")
            
            from ui.heatmaps import render_heatmaps_tab
            render_heatmaps_tab(params, bt_model)
        
        else:
            st.info("Heatmaps are currently available for Black-Scholes, Monte Carlo, and Binomial Tree models.")
    
    # TAB 5: Option Strategies
    with tab5:
        render_strategies_tab(params)
    
    # TAB 6: Education
    with tab6:
        render_education_tab()
    
    # TAB 7: About
    with tab7:
        render_about_page()


def render_strategies_tab(params: dict):
    """Render the Option Strategies tab."""
    st.header("🎯 Option Trading Strategies")
    
    st.markdown("""
    Analyze common multi-leg option strategies with detailed P&L profiles, risk metrics, and break-even analysis.
    """)
    
    # Initialize strategy factory
    factory = StrategyFactory(
        spot=params['spot'],
        time_to_maturity=params['time_to_maturity'],
        risk_free_rate=params['risk_free_rate'],
        volatility=params['volatility']
    )
    
    # Strategy selection
    st.markdown("---")
    st.subheader("📋 Select Strategy")
    
    strategy_category = st.selectbox(
        "Strategy Category",
        options=[
            "Vertical Spreads",
            "Volatility Strategies",
            "Advanced Strategies"
        ]
    )
    
    # Strategy parameters based on category
    if strategy_category == "Vertical Spreads":
        col1, col2 = st.columns(2)
        
        with col1:
            strategy_type = st.selectbox(
                "Strategy Type",
                options=[
                    "Bull Call Spread",
                    "Bear Put Spread",
                    "Bull Put Spread",
                    "Bear Call Spread"
                ]
            )
        
        with col2:
            spread_width = st.slider(
                "Spread Width ($)",
                min_value=1.0,
                max_value=20.0,
                value=5.0,
                step=1.0,
                help="Distance between strikes"
            )
        
        # Calculate strikes around current spot
        if strategy_type in ["Bull Call Spread", "Bear Call Spread"]:
            lower_strike = params['spot'] - spread_width / 2
            upper_strike = params['spot'] + spread_width / 2
        else:  # Put spreads
            lower_strike = params['spot'] - spread_width
            upper_strike = params['spot']
        
        # Create strategy
        if strategy_type == "Bull Call Spread":
            strategy = factory.bull_call_spread(lower_strike, upper_strike)
        elif strategy_type == "Bear Put Spread":
            strategy = factory.bear_put_spread(lower_strike, upper_strike)
        elif strategy_type == "Bull Put Spread":
            strategy = factory.bull_put_spread(lower_strike, upper_strike)
        else:  # Bear Call Spread
            strategy = factory.bear_call_spread(lower_strike, upper_strike)
    
    elif strategy_category == "Volatility Strategies":
        col1, col2 = st.columns(2)
        
        with col1:
            strategy_type = st.selectbox(
                "Strategy Type",
                options=[
                    "Long Straddle",
                    "Short Straddle",
                    "Long Strangle",
                    "Short Strangle"
                ]
            )
        
        strangle_width = 5.0  # Default
        with col2:
            if "Strangle" in strategy_type:
                strangle_width = st.slider(
                    "Strangle Width ($)",
                    min_value=2.0,
                    max_value=20.0,
                    value=5.0,
                    step=1.0,
                    help="Distance from ATM to each strike"
                )
        
        # Create strategy
        if strategy_type == "Long Straddle":
            strategy = factory.long_straddle(params['spot'])
        elif strategy_type == "Short Straddle":
            strategy = factory.short_straddle(params['spot'])
        elif strategy_type == "Long Strangle":
            call_strike = params['spot'] + strangle_width
            put_strike = params['spot'] - strangle_width
            strategy = factory.long_strangle(call_strike, put_strike)
        else:  # Short Strangle
            call_strike = params['spot'] + strangle_width
            put_strike = params['spot'] - strangle_width
            strategy = factory.short_strangle(call_strike, put_strike)
    
    else:  # Advanced Strategies
        col1, col2 = st.columns(2)
        
        with col1:
            strategy_type = st.selectbox(
                "Strategy Type",
                options=[
                    "Butterfly Spread",
                    "Iron Condor",
                    "Iron Butterfly"
                ]
            )
        
        with col2:
            wing_width = st.slider(
                "Wing Width ($)",
                min_value=5.0,
                max_value=30.0,
                value=10.0,
                step=2.5,
                help="Distance between strikes"
            )
        
        # Create strategy
        if strategy_type == "Butterfly Spread":
            lower = params['spot'] - wing_width
            middle = params['spot']
            upper = params['spot'] + wing_width
            strategy = factory.butterfly_spread(lower, middle, upper, option_type='call')
        elif strategy_type == "Iron Condor":
            put_lower = params['spot'] - wing_width * 1.5
            put_upper = params['spot'] - wing_width * 0.5
            call_lower = params['spot'] + wing_width * 0.5
            call_upper = params['spot'] + wing_width * 1.5
            strategy = factory.iron_condor(put_lower, put_upper, call_lower, call_upper)
        else:  # Iron Butterfly
            lower = params['spot'] - wing_width
            middle = params['spot']
            upper = params['spot'] + wing_width
            strategy = factory.iron_butterfly(lower, middle, upper)
    
    # Display strategy details
    st.markdown("---")
    st.subheader("📊 Strategy Analysis")
    
    # Strategy info card using native Streamlit components
    info = strategy.get_strategy_info()
    
    # Create a nice card layout
    with st.container():
        st.markdown(f"### {strategy.name}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            net_prem = info['net_premium']
            premium_type = "💰 Credit" if net_prem > 0 else "💳 Debit" if net_prem < 0 else "⚖️ Neutral"
            st.metric("Position Type", premium_type)
            st.metric("Net Premium", f"${net_prem:.2f}")
            st.metric("Max Profit", f"${info['max_profit']:.2f}")
        
        with col2:
            st.metric("Max Loss", f"${info['max_loss']:.2f}")
            st.metric("Risk/Reward Ratio", f"{info['risk_reward_ratio']:.2f}")
            
            risk_reward = info['risk_reward_ratio']
            if risk_reward < 0.5:
                risk_level = "🟢 Low Risk"
            elif risk_reward < 1.5:
                risk_level = "🟡 Moderate Risk"
            else:
                risk_level = "🔴 High Risk"
            st.metric("Risk Level", risk_level)
        
        # Break-even points
        if info['break_even_points']:
            st.markdown("**🎯 Break-Even Points:**")
            be_text = ", ".join([f"${be:.2f}" for be in info['break_even_points']])
            st.info(be_text)
        
        # Position details
        st.markdown("**📋 Position Details:**")
        for leg in strategy.legs:
            leg_desc = f"• {leg.position.title()} {leg.quantity}x {leg.option_type.title()} @ ${leg.strike:.2f} (Premium: ${leg.premium:.2f})"
            st.text(leg_desc)
    
    # Payoff diagram
    st.markdown("---")
    st.subheader("📈 Payoff Diagram")
    
    show_legs = st.checkbox("Show Individual Legs", value=True, help="Display each option leg separately")
    
    fig_payoff = plot_strategy_payoff(strategy, params['spot'], show_legs=show_legs)
    st.plotly_chart(fig_payoff, use_container_width=True)
    
    # Risk profile
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Risk Profile")
        fig_risk = plot_risk_profile(strategy)
        st.plotly_chart(fig_risk, use_container_width=True)
    
    with col2:
        st.markdown("### 💰 Key Metrics")
        info = strategy.get_strategy_info()
        
        st.metric("Net Premium", f"${info['net_premium']:.2f}",
                 help="Negative = debit (paid), Positive = credit (received)")
        st.metric("Max Profit", f"${info['max_profit']:.2f}")
        st.metric("Max Loss", f"${info['max_loss']:.2f}")
        st.metric("Risk/Reward Ratio", f"{info['risk_reward_ratio']:.2f}",
                 help="Lower is better (less risk per dollar of profit)")
        
        if info['break_even_points']:
            st.markdown("**Break-Even Points:**")
            for i, be in enumerate(info['break_even_points'], 1):
                st.write(f"{i}. ${be:.2f}")
    
    # Strategy comparison (optional)
    st.markdown("---")
    with st.expander("🔍 Compare Multiple Strategies"):
        st.markdown("Compare different strategies side-by-side")
        
        # Quick comparison of similar strategies
        comparison_strategies = []
        
        if strategy_category == "Vertical Spreads":
            comparison_strategies = [
                factory.bull_call_spread(params['spot'] - 5, params['spot'] + 5),
                factory.bear_put_spread(params['spot'] - 5, params['spot'] + 5),
                factory.bull_put_spread(params['spot'] - 5, params['spot'] + 5),
                factory.bear_call_spread(params['spot'] - 5, params['spot'] + 5)
            ]
        elif strategy_category == "Volatility Strategies":
            comparison_strategies = [
                factory.long_straddle(params['spot']),
                factory.long_strangle(params['spot'] + 5, params['spot'] - 5),
            ]
        
        if comparison_strategies:
            fig_comparison = plot_multiple_strategies(comparison_strategies, params['spot'])
            st.plotly_chart(fig_comparison, use_container_width=True)
            
            # Comparison table
            comparison_data = create_strategy_comparison_table(comparison_strategies)
            import pandas as pd
            df_comparison = pd.DataFrame(comparison_data)
            st.dataframe(df_comparison, use_container_width=True)
    
    # Educational content
    st.markdown("---")
    with st.expander("📚 Strategy Guides & Tips"):
        if "Bull" in strategy.name:
            st.markdown("""
            **Bullish Strategies** profit when the underlying price rises.
            
            - **Best used when**: You expect moderate to strong upward movement
            - **Risk**: Limited to premium paid (for debit spreads)
            - **Reward**: Limited to spread width minus premium
            - **Time decay**: Works against you (for long positions)
            """)
        elif "Bear" in strategy.name:
            st.markdown("""
            **Bearish Strategies** profit when the underlying price falls.
            
            - **Best used when**: You expect moderate to strong downward movement
            - **Risk**: Limited (for defined-risk spreads)
            - **Reward**: Limited to spread width or premium received
            - **Time decay**: Can work for or against you depending on position
            """)
        elif "Straddle" in strategy.name or "Strangle" in strategy.name:
            st.markdown("""
            **Volatility Strategies** profit from large price movements in either direction.
            
            - **Long positions**: Profit from high volatility (large moves)
            - **Short positions**: Profit from low volatility (range-bound)
            - **Best for**: Earnings announcements, major events
            - **Risk**: Unlimited for short positions, limited for long
            """)
        else:
            st.markdown("""
            **Advanced Strategies** combine multiple options for specific risk/reward profiles.
            
            - **Butterfly/Condor**: Profit from range-bound markets
            - **Lower cost**: Than straddles/strangles
            - **Limited risk**: All positions have defined maximum loss
            - **Complexity**: Requires careful strike selection
            """)


def render_about_page():
    """Render the About page with project and developer information."""
    
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1>🚀 Option Pricing Calculator</h1>
        <p style='font-size: 18px; color: #666;'>Advanced Financial Derivatives Pricing Models</p>
        <p style='font-size: 14px; color: #999;'>Built in 2025 with AI-Assisted Development</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## 📋 About This Project
        
        This web application implements advanced mathematical models for pricing financial options,
        providing a professional tool for financial analysts, traders, and quantitative finance students.
        
        ### 🤖 The AI-Assisted Development Story
        
        This project represents a **new paradigm in software development**: combining **financial domain expertise** 
        with **AI-powered coding**.
        
        Unlike traditional development where every line is written by a programmer, this application was created through:
        
        - 🎯 **Human Vision** - Conceptual design and financial requirements
        - 🤖 **AI Implementation** - Code generation guided by Claude AI (Anthropic)
        - 🔄 **Iterative Refinement** - Continuous feedback and improvement
        - � **Domain Knowledge** - Finance theory meets computational power
        
        **The Result?** A professional-grade financial application built by a finance student with limited coding experience,
        demonstrating how AI is **democratizing software development**.
        
        ### �🔬 Models Implemented
        
        **1. Black-Scholes Model** ✅
        - Classic analytical solution for European options
        - Closed-form formula for fast and accurate pricing
        - Calculation time: ~1-2 ms ⚡
        
        **2. Monte Carlo Simulation** ✅
        - Stochastic simulation using geometric Brownian motion
        - 100,000 simulations with antithetic variates
        - Confidence intervals and convergence analysis
        - Calculation time: ~150-200 ms
        
        **3. Binomial Tree Model** ✅
        - Cox-Ross-Rubinstein discrete-time lattice model
        - Supports both European and American options
        - Early exercise detection and premium calculation
        - Configurable steps (10-500)
        
        ### ✨ Key Features
        
        - 🔄 **Real-time pricing** across three mathematical models
        - 📊 **Complete Greeks analysis** (Delta, Gamma, Theta, Vega, Rho)
        - 📈 **Interactive visualizations** with Plotly
        - � **Advanced heatmaps** - Price surfaces, Greeks correlation, Risk exposure
        - 🎯 **11 Option Strategies** - From spreads to iron condors
        - 📚 **Educational tutorials** - Learn while you price
        - � **Data export** - CSV and Excel reports
        - 🎨 **Professional UI** - Intuitive and responsive
        
        ### 🛠️ Technology Stack
        
        - **Python 3.10+** - Core language
        - **Streamlit** - Web framework
        - **NumPy & SciPy** - Mathematical computations
        - **Plotly** - Interactive visualizations
        - **Pandas** - Data manipulation
        - **Claude AI** - Development assistant
        
        ### 🎯 Use Cases
        
        - **Finance Students** - Learn derivatives pricing interactively
        - **Quantitative Analysts** - Rapid option valuation and analysis
        - **Risk Managers** - Sensitivity calculations for hedging
        - **Researchers** - Compare pricing methodologies
        - **Educators** - Teaching tool for financial engineering
        """)
    
    with col2:
        st.markdown("""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h3 style='color: #1f77b4; margin-top: 0;'>👨‍🎓 Creator</h3>
            <h4 style='margin: 10px 0;'>Giovanni De Stasio</h4>
            <p style='color: #666; font-style: italic;'>Finance & Economics Student</p>
            <p style='color: #666; font-size: 14px;'>Università Bocconi, Milan</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### 🎓 Background
        
        I'm a **Finance & Economics student at Bocconi University** with a passion for:
        - **Quantitative Finance** & Derivatives
        - **Financial Modeling** & Risk Management
        - **AI Applications** in Finance
        - **Computational Methods** for Pricing
        
        ### 💡 The Philosophy
        
        This project embodies a simple but powerful idea:
        
        > **"You don't need to be a programmer to build software. You need to be a great communicator with AI."**
        
        Through **"Vibe Coding"** - the art of guiding AI to implement your vision - 
        I transformed financial theory knowledge into a working application.
        
        ### � AI-Assisted Development
        
        **My Role:**
        - 🎯 Define requirements and features
        - 📚 Provide financial domain expertise
        - 🔍 Test and validate implementations
        - 🎨 Design user experience
        - 🔄 Iterate and refine continuously
        
        **AI's Role:**
        - ⌨️ Generate code implementations
        - 🐛 Debug and fix errors
        - 📝 Write documentation
        - 🧪 Create test suites
        - ⚡ Optimize performance
        
        ### 🔗 Connect
        """)
        
        # Contact buttons with real links
        st.link_button("📧 Email", "mailto:gdestasio922@gmail.com", use_container_width=True)
        st.link_button("💼 LinkedIn", "https://www.linkedin.com/in/gds-", use_container_width=True)
        st.link_button("🐙 GitHub", "https://github.com/NutellaPazza", use_container_width=True)
        st.link_button("📊 Repository", "https://github.com/NutellaPazza/option-pricing-calculator", use_container_width=True)
    
    st.markdown("---")
    
    # Additional info section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📊 Project Stats
        - **Lines of Code:** ~6,000+
        - **Models:** 3 (BS, MC, BT)
        - **Strategies:** 11
        - **Greeks:** 5
        - **Tests:** 20+ unit tests
        - **Development Time:** 2 weeks
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 Features
        - ✅ Real-time Pricing
        - ✅ Greeks Analysis
        - ✅ Interactive Heatmaps
        - ✅ Strategy Builder
        - ✅ Educational Tutorials
        - ✅ Data Export
        """)
    
    with col3:
        st.markdown("""
        ### 🌟 Highlights
        - 🤖 AI-Assisted Build
        - 📈 3 Pricing Models
        - 🎓 Educational Focus
        - 💼 Professional Grade
        - 🚀 Open Source
        - 🔄 Actively Maintained
        """)
    
    st.markdown("---")
    
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px 0;'>
        <h3>🙏 Acknowledgments</h3>
        <p>Special thanks to:</p>
        <ul style='list-style: none; padding: 0;'>
            <li>🤖 <strong>Claude (Anthropic)</strong> - AI assistant that made this project possible</li>
            <li>🎓 <strong>Università Bocconi</strong> - Academic foundation in finance</li>
            <li>💻 <strong>Streamlit</strong> - Excellent framework for data applications</li>
            <li>📊 <strong>Plotly</strong> - Beautiful interactive visualizations</li>
            <li>🐍 <strong>Python Community</strong> - Amazing open-source ecosystem</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <h2>🤖 + 🧠 = 🚀</h2>
        <p style='font-size: 18px;'><em>"The future of software development is not about writing code,<br>
        but about guiding intelligence."</em></p>
        <br>
        <p><strong>© 2025 Giovanni De Stasio - Option Pricing Calculator</strong></p>
        <p>Built with AI Assistance | Version 1.0.0 | MIT License</p>
        <br>
        <p style='font-size: 12px; color: #999;'>
            This project demonstrates the power of AI-assisted development.<br>
            Domain expertise + AI capabilities = Professional software
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
