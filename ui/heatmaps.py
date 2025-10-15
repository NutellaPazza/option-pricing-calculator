"""
Interactive heatmaps for option pricing visualization
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Callable, Dict, Any


class OptionHeatmaps:
    """Class for generating interactive heatmaps for option pricing"""
    
    @staticmethod
    def price_heatmap_side_by_side(model, base_params: dict):
        """
        Side-by-side heatmap of Call and Put option prices with text annotations
        Similar to the reference project style
        """
        st.markdown("### Options Price - Interactive Heatmap")
        st.markdown("Explore how option prices fluctuate with varying 'Spot Prices and Volatility' levels using interactive heatmap parameters")
        
        # Heatmap parameters in sidebar or main area
        st.markdown("#### Heatmap Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            min_spot = st.slider(
                "Min Spot Price",
                min_value=base_params['spot'] * 0.5,
                max_value=base_params['spot'] * 0.9,
                value=base_params['spot'] * 0.7,
                step=0.01
            )
            
            min_vol = st.slider(
                "Min Volatility for Heatmap",
                min_value=0.01,
                max_value=base_params['volatility'],
                value=0.01,
                step=0.01
            )
        
        with col2:
            max_spot = st.slider(
                "Max Spot Price",
                min_value=base_params['spot'] * 1.1,
                max_value=base_params['spot'] * 2.0,
                value=base_params['spot'] * 1.5,
                step=0.01
            )
            
            max_vol = st.slider(
                "Max Volatility for Heatmap",
                min_value=base_params['volatility'],
                max_value=1.0,
                value=1.0,
                step=0.01
            )
        
        # Create ranges (fewer points for cleaner display)
        spot_range = np.linspace(min_spot, max_spot, 12)
        vol_range = np.linspace(min_vol, max_vol, 10)
        
        # Calculate prices for both Call and Put
        call_prices = np.zeros((len(vol_range), len(spot_range)))
        put_prices = np.zeros((len(vol_range), len(spot_range)))
        
        for i, vol in enumerate(vol_range):
            for j, spot in enumerate(spot_range):
                params_call = base_params.copy()
                params_call['spot'] = spot
                params_call['volatility'] = vol
                params_call['option_type'] = 'call'
                
                params_put = params_call.copy()
                params_put['option_type'] = 'put'
                
                call_prices[i, j] = model.calculate_price(
                    spot=params_call['spot'],
                    strike=params_call['strike'],
                    time_to_maturity=params_call['time_to_maturity'],
                    risk_free_rate=params_call['risk_free_rate'],
                    volatility=params_call['volatility'],
                    option_type=params_call['option_type']
                )
                put_prices[i, j] = model.calculate_price(
                    spot=params_put['spot'],
                    strike=params_put['strike'],
                    time_to_maturity=params_put['time_to_maturity'],
                    risk_free_rate=params_put['risk_free_rate'],
                    volatility=params_put['volatility'],
                    option_type=params_put['option_type']
                )
        
        # Create side-by-side subplots
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Call Price Heatmap", "Put Price Heatmap"),
            horizontal_spacing=0.15
        )
        
        # Call heatmap with text annotations
        call_text = [[f'{val:.2f}' for val in row] for row in call_prices]
        
        fig.add_trace(
            go.Heatmap(
                z=call_prices,
                x=[f'{x:.2f}' for x in spot_range],
                y=[f'{y:.2f}' for y in vol_range],
                text=call_text,
                texttemplate="%{text}",
                textfont={"size": 10},
                colorscale='RdYlGn',
                colorbar=dict(
                    title="Price",
                    x=0.45,
                    len=0.9
                ),
                hovertemplate='Spot: %{x}<br>Vol: %{y}<br>Call Price: %{z:.2f}<extra></extra>',
                name='CALL'
            ),
            row=1, col=1
        )
        
        # Put heatmap with text annotations
        put_text = [[f'{val:.2f}' for val in row] for row in put_prices]
        
        fig.add_trace(
            go.Heatmap(
                z=put_prices,
                x=[f'{x:.2f}' for x in spot_range],
                y=[f'{y:.2f}' for y in vol_range],
                text=put_text,
                texttemplate="%{text}",
                textfont={"size": 10},
                colorscale='RdYlGn',
                colorbar=dict(
                    title="Price",
                    x=1.02,
                    len=0.9
                ),
                hovertemplate='Spot: %{x}<br>Vol: %{y}<br>Put Price: %{z:.2f}<extra></extra>',
                name='PUT'
            ),
            row=1, col=2
        )
        
        # Update layout
        fig.update_xaxes(title_text="Spot Price", row=1, col=1)
        fig.update_xaxes(title_text="Spot Price", row=1, col=2)
        fig.update_yaxes(title_text="Volatility (σ)", row=1, col=1)
        fig.update_yaxes(title_text="Volatility (σ)", row=1, col=2)
        
        fig.update_layout(
            height=600,
            showlegend=False,
            font=dict(size=11)
        )
        
        return fig
    
    @staticmethod
    def greek_heatmap_side_by_side(greek_func: Callable, base_params: dict, greek_name: str):
        """
        Side-by-side heatmap for a specific Greek (Call and Put)
        """
        st.markdown(f"### {greek_name} - Interactive Heatmap")
        st.markdown(f"Visualize how {greek_name} changes with Spot Price and Time to Maturity")
        
        # Parameters
        col1, col2 = st.columns(2)
        
        with col1:
            min_spot = st.slider(
                f"Min Spot Price ({greek_name})",
                min_value=base_params['spot'] * 0.5,
                max_value=base_params['spot'] * 0.9,
                value=base_params['spot'] * 0.7,
                step=0.01,
                key=f"{greek_name}_min_spot"
            )
            
            min_time = st.slider(
                f"Min Time to Maturity ({greek_name})",
                min_value=0.1,
                max_value=base_params['time_to_maturity'] * 0.9,
                value=0.1,
                step=0.1,
                key=f"{greek_name}_min_time"
            )
        
        with col2:
            max_spot = st.slider(
                f"Max Spot Price ({greek_name})",
                min_value=base_params['spot'] * 1.1,
                max_value=base_params['spot'] * 2.0,
                value=base_params['spot'] * 1.3,
                step=0.01,
                key=f"{greek_name}_max_spot"
            )
            
            max_time = st.slider(
                f"Max Time to Maturity ({greek_name})",
                min_value=base_params['time_to_maturity'] * 1.1,
                max_value=3.0,
                value=base_params['time_to_maturity'] * 2.0,
                step=0.1,
                key=f"{greek_name}_max_time"
            )
        
        spot_range = np.linspace(min_spot, max_spot, 12)
        time_range = np.linspace(min_time, max_time, 10)
        
        call_greeks = np.zeros((len(time_range), len(spot_range)))
        put_greeks = np.zeros((len(time_range), len(spot_range)))
        
        for i, time in enumerate(time_range):
            for j, spot in enumerate(spot_range):
                params_call = base_params.copy()
                params_call['spot'] = spot
                params_call['time_to_maturity'] = time
                params_call['option_type'] = 'call'
                
                params_put = params_call.copy()
                params_put['option_type'] = 'put'
                
                call_greeks[i, j] = greek_func(
                    spot=params_call['spot'],
                    strike=params_call['strike'],
                    time_to_maturity=params_call['time_to_maturity'],
                    risk_free_rate=params_call['risk_free_rate'],
                    volatility=params_call['volatility'],
                    option_type=params_call['option_type']
                )
                put_greeks[i, j] = greek_func(
                    spot=params_put['spot'],
                    strike=params_put['strike'],
                    time_to_maturity=params_put['time_to_maturity'],
                    risk_free_rate=params_put['risk_free_rate'],
                    volatility=params_put['volatility'],
                    option_type=params_put['option_type']
                )
        
        # Create subplots
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=(f"Call {greek_name} Heatmap", f"Put {greek_name} Heatmap"),
            horizontal_spacing=0.15
        )
        
        # Call greek with text
        call_text = [[f'{val:.4f}' for val in row] for row in call_greeks]
        
        fig.add_trace(
            go.Heatmap(
                z=call_greeks,
                x=[f'{x:.2f}' for x in spot_range],
                y=[f'{y:.2f}' for y in time_range],
                text=call_text,
                texttemplate="%{text}",
                textfont={"size": 9},
                colorscale='Viridis',
                colorbar=dict(title=greek_name, x=0.45, len=0.9),
                hovertemplate=f'Spot: %{{x}}<br>Time: %{{y}}<br>{greek_name}: %{{z:.4f}}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Put greek with text
        put_text = [[f'{val:.4f}' for val in row] for row in put_greeks]
        
        fig.add_trace(
            go.Heatmap(
                z=put_greeks,
                x=[f'{x:.2f}' for x in spot_range],
                y=[f'{y:.2f}' for y in time_range],
                text=put_text,
                texttemplate="%{text}",
                textfont={"size": 9},
                colorscale='Viridis',
                colorbar=dict(title=greek_name, x=1.02, len=0.9),
                hovertemplate=f'Spot: %{{x}}<br>Time: %{{y}}<br>{greek_name}: %{{z:.4f}}<extra></extra>'
            ),
            row=1, col=2
        )
        
        fig.update_xaxes(title_text="Spot Price (S)", row=1, col=1)
        fig.update_xaxes(title_text="Spot Price (S)", row=1, col=2)
        fig.update_yaxes(title_text="Time to Maturity (Years)", row=1, col=1)
        fig.update_yaxes(title_text="Time to Maturity (Years)", row=1, col=2)
        
        fig.update_layout(
            height=600,
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def volatility_surface(base_params: dict, model):
        """
        3D Volatility Surface: Strike vs Time to Maturity
        """
        st.markdown("### Implied Volatility Surface (3D)")
        st.markdown("3D visualization of volatility smile across strikes and maturities")
        
        strike_range = np.linspace(base_params['spot'] * 0.7, base_params['spot'] * 1.3, 25)
        time_range = np.linspace(0.1, 2.0, 25)
        
        vol_surface = np.zeros((len(time_range), len(strike_range)))
        
        for i, time in enumerate(time_range):
            for j, strike in enumerate(strike_range):
                moneyness = strike / base_params['spot']
                vol_surface[i, j] = base_params['volatility'] * (1 + 0.3 * (moneyness - 1)**2 + 0.1 * time)
        
        fig = go.Figure(data=[go.Surface(
            z=vol_surface,
            x=strike_range,
            y=time_range,
            colorscale='Plasma',
            colorbar=dict(title="Volatility (σ)")
        )])
        
        fig.update_layout(
            scene=dict(
                xaxis_title='Strike Price (K)',
                yaxis_title='Time to Maturity (Years)',
                zaxis_title='Implied Volatility (σ)'
            ),
            width=900,
            height=700
        )
        
        return fig
    
    @staticmethod
    def profit_loss_heatmap(model, base_params: dict, entry_premium: float):
        """
        Profit & Loss Heatmap: Spot at Time vs Time to Expiry
        """
        st.markdown("### Profit & Loss Heatmap")
        st.markdown("Visualize P&L scenarios across different spot prices and time periods")
        
        col1, col2 = st.columns(2)
        
        with col1:
            entry_premium_call = st.number_input(
                "Entry Premium Paid - Call",
                value=entry_premium,
                step=0.1,
                key="pnl_premium_call"
            )
        
        with col2:
            entry_premium_put = st.number_input(
                "Entry Premium Paid - Put",
                value=entry_premium,
                step=0.1,
                key="pnl_premium_put"
            )
        
        spot_at_expiry = np.linspace(base_params['spot'] * 0.6, base_params['spot'] * 1.4, 12)
        time_range = np.linspace(base_params['time_to_maturity'], 0.01, 10)
        
        pnl_call = np.zeros((len(time_range), len(spot_at_expiry)))
        pnl_put = np.zeros((len(time_range), len(spot_at_expiry)))
        
        for i, time in enumerate(time_range):
            for j, spot in enumerate(spot_at_expiry):
                params_call = base_params.copy()
                params_call['spot'] = spot
                params_call['time_to_maturity'] = time
                params_call['option_type'] = 'call'
                
                params_put = params_call.copy()
                params_put['option_type'] = 'put'
                
                current_value_call = model.calculate_price(
                    spot=params_call['spot'],
                    strike=params_call['strike'],
                    time_to_maturity=params_call['time_to_maturity'],
                    risk_free_rate=params_call['risk_free_rate'],
                    volatility=params_call['volatility'],
                    option_type=params_call['option_type']
                )
                current_value_put = model.calculate_price(
                    spot=params_put['spot'],
                    strike=params_put['strike'],
                    time_to_maturity=params_put['time_to_maturity'],
                    risk_free_rate=params_put['risk_free_rate'],
                    volatility=params_put['volatility'],
                    option_type=params_put['option_type']
                )
                
                pnl_call[i, j] = current_value_call - entry_premium_call
                pnl_put[i, j] = current_value_put - entry_premium_put
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Call P&L Heatmap", "Put P&L Heatmap"),
            horizontal_spacing=0.15
        )
        
        # Call P&L with text
        call_text = [[f'{val:.2f}' for val in row] for row in pnl_call]
        
        fig.add_trace(
            go.Heatmap(
                z=pnl_call,
                x=[f'{x:.2f}' for x in spot_at_expiry],
                y=[f'{y:.2f}' for y in time_range],
                text=call_text,
                texttemplate="%{text}",
                textfont={"size": 9},
                colorscale='RdYlGn',
                zmid=0,
                colorbar=dict(title="P&L", x=0.45, len=0.9),
                hovertemplate='Spot: %{x}<br>Time: %{y}<br>P&L: %{z:.2f}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Put P&L with text
        put_text = [[f'{val:.2f}' for val in row] for row in pnl_put]
        
        fig.add_trace(
            go.Heatmap(
                z=pnl_put,
                x=[f'{x:.2f}' for x in spot_at_expiry],
                y=[f'{y:.2f}' for y in time_range],
                text=put_text,
                texttemplate="%{text}",
                textfont={"size": 9},
                colorscale='RdYlGn',
                zmid=0,
                colorbar=dict(title="P&L", x=1.02, len=0.9),
                hovertemplate='Spot: %{x}<br>Time: %{y}<br>P&L: %{z:.2f}<extra></extra>'
            ),
            row=1, col=2
        )
        
        fig.update_xaxes(title_text="Spot Price at Time", row=1, col=1)
        fig.update_xaxes(title_text="Spot Price at Time", row=1, col=2)
        fig.update_yaxes(title_text="Time to Maturity (Years)", row=1, col=1)
        fig.update_yaxes(title_text="Time to Maturity (Years)", row=1, col=2)
        
        fig.update_layout(
            height=600,
            showlegend=False
        )
        
        st.success("🟢 Green = Profit | 🔴 Red = Loss")
        
        return fig


    @staticmethod
    def greeks_correlation_heatmap(params: dict, model):
        """
        Correlation heatmap showing relationships between Greeks.
        """
        st.markdown("### Greeks Correlation Matrix")
        st.markdown("Understand how different Greeks correlate with each other")
        
        from calculations.greeks import GreeksCalculator
        greeks_calc = GreeksCalculator()
        
        # Create range of spot prices
        spot_range = np.linspace(params['spot'] * 0.7, params['spot'] * 1.3, 50)
        
        # Calculate all Greeks across spot range
        greeks_data = {
            'Delta': [],
            'Gamma': [],
            'Vega': [],
            'Theta': [],
            'Rho': []
        }
        
        for spot in spot_range:
            # Create params for Greeks calculation
            # Note: Gamma and Vega don't take option_type parameter
            base_params = {
                'spot': spot,
                'strike': params['strike'],
                'time_to_maturity': params['time_to_maturity'],
                'risk_free_rate': params['risk_free_rate'],
                'volatility': params['volatility']
            }
            
            params_with_type = base_params.copy()
            params_with_type['option_type'] = params['option_type']
            
            greeks_data['Delta'].append(greeks_calc.delta(**params_with_type))
            greeks_data['Gamma'].append(greeks_calc.gamma(**base_params))
            greeks_data['Vega'].append(greeks_calc.vega(**base_params))
            greeks_data['Theta'].append(greeks_calc.theta(**params_with_type))
            greeks_data['Rho'].append(greeks_calc.rho(**params_with_type))
        
        # Calculate correlation matrix
        import pandas as pd
        df = pd.DataFrame(greeks_data)
        corr_matrix = df.corr().values
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix,
            x=list(greeks_data.keys()),
            y=list(greeks_data.keys()),
            text=[[f'{val:.3f}' for val in row] for row in corr_matrix],
            texttemplate='%{text}',
            textfont={"size": 12},
            colorscale='RdBu',
            zmid=0,
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title="Greeks Correlation Matrix",
            xaxis_title="Greek",
            yaxis_title="Greek",
            height=500,
            width=600
        )
        
        return fig
    
    @staticmethod
    def risk_exposure_map(params: dict, model):
        """
        Risk exposure map showing portfolio exposure across multiple dimensions.
        """
        st.markdown("### Risk Exposure Heatmap")
        st.markdown("Visualize risk exposure across Spot Price and Volatility changes")
        
        # Risk parameters
        col1, col2 = st.columns(2)
        with col1:
            position_size = st.number_input(
                "Position Size (contracts)",
                value=10,
                min_value=1,
                max_value=100,
                key="risk_position_size"
            )
            position_type = st.selectbox(
                "Position Type",
                ["Long Call", "Long Put", "Short Call", "Short Put"],
                key="risk_position_type"
            )
        
        with col2:
            entry_price = st.number_input(
                "Entry Price (per contract)",
                value=5.0,
                min_value=0.1,
                max_value=50.0,
                step=0.5,
                key="risk_entry_price"
            )
        
        # Create ranges
        spot_pct_change = np.linspace(-0.3, 0.3, 15)  # -30% to +30%
        vol_pct_change = np.linspace(-0.5, 0.5, 12)   # -50% to +50%
        
        risk_matrix = np.zeros((len(vol_pct_change), len(spot_pct_change)))
        
        for i, vol_chg in enumerate(vol_pct_change):
            for j, spot_chg in enumerate(spot_pct_change):
                # Determine option type
                is_call = 'Call' in position_type
                option_type = 'call' if is_call else 'put'
                
                # Calculate current value with clean parameters
                current_value = model.calculate_price(
                    spot=params['spot'] * (1 + spot_chg),
                    strike=params['strike'],
                    time_to_maturity=params['time_to_maturity'],
                    risk_free_rate=params['risk_free_rate'],
                    volatility=params['volatility'] * (1 + vol_chg),
                    option_type=option_type
                )
                
                # Calculate P&L
                is_long = 'Long' in position_type
                if is_long:
                    pnl_per_contract = current_value - entry_price
                else:
                    pnl_per_contract = entry_price - current_value
                
                total_pnl = pnl_per_contract * position_size * 100  # x100 for contract multiplier
                risk_matrix[i, j] = total_pnl
        
        # Create heatmap
        spot_labels = [f'{chg:+.0%}' for chg in spot_pct_change]
        vol_labels = [f'{chg:+.0%}' for chg in vol_pct_change]
        
        text_matrix = [[f'${val:,.0f}' for val in row] for row in risk_matrix]
        
        fig = go.Figure(data=go.Heatmap(
            z=risk_matrix,
            x=spot_labels,
            y=vol_labels,
            text=text_matrix,
            texttemplate='%{text}',
            textfont={"size": 9},
            colorscale='RdYlGn',
            zmid=0,
            colorbar=dict(title="P&L ($)")
        ))
        
        fig.update_layout(
            title=f"Risk Exposure Map - {position_type} ({position_size} contracts)",
            xaxis_title="Spot Price Change",
            yaxis_title="Volatility Change",
            height=600
        )
        
        # Add risk metrics
        max_profit = np.max(risk_matrix)
        max_loss = np.min(risk_matrix)
        
        st.metric("Maximum Profit Scenario", f"${max_profit:,.2f}", delta="Best case")
        st.metric("Maximum Loss Scenario", f"${max_loss:,.2f}", delta="Worst case")
        
        return fig
    
    @staticmethod
    def strategy_comparison_grid(params: dict):
        """
        Strategy comparison grid showing key metrics for multiple strategies.
        """
        st.markdown("### Strategy Comparison Grid")
        st.markdown("Compare profitability and risk metrics across common strategies")
        
        from strategies.options import StrategyFactory
        
        # Initialize factory
        factory = StrategyFactory(
            spot=params['spot'],
            time_to_maturity=params['time_to_maturity'],
            risk_free_rate=params['risk_free_rate'],
            volatility=params['volatility']
        )
        
        # Create strategies
        strategies = {
            'Bull Call': factory.bull_call_spread(params['spot'] * 0.95, params['spot'] * 1.05),
            'Bear Put': factory.bear_put_spread(params['spot'] * 0.95, params['spot'] * 1.05),
            'Long Straddle': factory.long_straddle(params['spot']),
            'Long Strangle': factory.long_strangle(params['spot'] * 0.95, params['spot'] * 1.05),
            'Iron Condor': factory.iron_condor(
                params['spot'] * 0.85, params['spot'] * 0.95,
                params['spot'] * 1.05, params['spot'] * 1.15
            ),
            'Butterfly': factory.butterfly_spread(
                params['spot'] * 0.9, params['spot'], params['spot'] * 1.1
            )
        }
        
        # Calculate payoffs across spot range
        spot_range = np.linspace(params['spot'] * 0.7, params['spot'] * 1.3, 100)
        
        # Create matrix for heatmap
        strategy_names = list(strategies.keys())
        payoff_matrix = np.zeros((len(strategy_names), len(spot_range)))
        
        for i, (name, strategy) in enumerate(strategies.items()):
            payoff_matrix[i, :] = strategy.calculate_payoff(spot_range)
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=payoff_matrix,
            x=[f'${s:.1f}' for s in spot_range[::10]],  # Show every 10th label
            y=strategy_names,
            colorscale='RdYlGn',
            zmid=0,
            colorbar=dict(title="P&L ($)")
        ))
        
        fig.update_layout(
            title="Strategy Payoff Comparison Across Spot Prices",
            xaxis_title="Spot Price at Expiration",
            yaxis_title="Strategy",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Metrics table
        st.markdown("#### Strategy Metrics Summary")
        
        metrics_data = []
        for name, strategy in strategies.items():
            info = strategy.get_strategy_info()
            metrics_data.append({
                'Strategy': name,
                'Net Premium': f"${info['net_premium']:.2f}",
                'Max Profit': f"${info['max_profit']:.2f}",
                'Max Loss': f"${info['max_loss']:.2f}",
                'Risk/Reward': f"{info['risk_reward_ratio']:.2f}",
                'Break-Evens': len(info['break_even_points'])
            })
        
        import pandas as pd
        df = pd.DataFrame(metrics_data)
        st.dataframe(df, use_container_width=True)
        
        return fig


def render_heatmaps_tab(params: Dict[str, Any], model):
    """
    Main function to render the heatmaps tab with all visualizations
    """
    from calculations.greeks import GreeksCalculator
    
    st.header("🔥 Interactive Heatmaps")
    st.markdown("Advanced visualization of option pricing dynamics using interactive heatmaps")
    
    # Subtabs for different heatmap types
    subtab1, subtab2, subtab3, subtab4, subtab5, subtab6, subtab7 = st.tabs([
        "💰 Price Surface", 
        "📊 Greeks", 
        "🌊 Volatility (3D)", 
        "💹 P&L Analysis",
        "🔗 Greeks Correlation",
        "⚠️ Risk Exposure",
        "🎯 Strategy Comparison"
    ])
    
    with subtab1:
        fig = OptionHeatmaps.price_heatmap_side_by_side(model, params)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("💡 **How to use:** Adjust the sliders to change the ranges of Spot Price and Volatility. The heatmap updates in real-time!")
    
    with subtab2:
        greek_choice = st.selectbox(
            "Select Greek for Heatmap",
            ["Delta", "Gamma", "Vega", "Theta", "Rho"],
            key="greek_heatmap_choice"
        )
        
        # Create GreeksCalculator instance
        greeks_calc = GreeksCalculator()
        
        # Map greek name to function
        greek_functions = {
            'Delta': greeks_calc.delta,
            'Gamma': greeks_calc.gamma,
            'Vega': greeks_calc.vega,
            'Theta': greeks_calc.theta,
            'Rho': greeks_calc.rho
        }
        
        fig = OptionHeatmaps.greek_heatmap_side_by_side(
            greek_functions[greek_choice],
            params,
            greek_choice
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.info(f"💡 **{greek_choice} Interpretation:** Shows sensitivity across different market conditions")
    
    with subtab3:
        fig = OptionHeatmaps.volatility_surface(params, model)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("💡 **Volatility Surface:** 3D representation of implied volatility across strikes and maturities. The smile effect is visible!")
    
    with subtab4:
        entry_premium = params.get('spot', 100) * 0.05  # Default 5% of spot
        fig = OptionHeatmaps.profit_loss_heatmap(model, params, entry_premium)
        st.plotly_chart(fig, use_container_width=True)
    
    with subtab5:
        fig = OptionHeatmaps.greeks_correlation_heatmap(params, model)
        st.plotly_chart(fig, use_container_width=True)
        st.info("💡 **Correlation Insights:** Positive correlation (blue) means Greeks move together. Negative correlation (red) means they move opposite.")
    
    with subtab6:
        fig = OptionHeatmaps.risk_exposure_map(params, model)
        st.plotly_chart(fig, use_container_width=True)
        st.info("💡 **Risk Management:** Green areas represent profit, red areas represent loss. Use this to understand your portfolio's sensitivity to market changes.")
    
    with subtab7:
        OptionHeatmaps.strategy_comparison_grid(params)
        st.info("💡 **Strategy Selection:** Compare strategies side-by-side to find the best fit for your market outlook and risk tolerance.")
