"""
UI Helper functions for enhanced user experience.
Includes loading indicators, tooltips, error handling.
"""

import streamlit as st
from typing import Callable, Any, Optional
import time
from functools import wraps


def with_loading_spinner(message: str = "Calculating..."):
    """
    Decorator to add a loading spinner to any function.
    
    Args:
        message: Message to display while loading
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            with st.spinner(message):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def show_info_tooltip(text: str, icon: str = "ℹ️"):
    """
    Display an informational tooltip.
    
    Args:
        text: Tooltip text
        icon: Icon to display
    """
    st.markdown(f"{icon} *{text}*")


def show_calculation_time(func: Callable, *args, **kwargs) -> tuple[Any, float]:
    """
    Execute function and return result with execution time.
    
    Args:
        func: Function to execute
        *args, **kwargs: Function arguments
        
    Returns:
        Tuple of (result, execution_time_ms)
    """
    start_time = time.time()
    result = func(*args, **kwargs)
    elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
    return result, elapsed_time


def display_metric_with_tooltip(
    label: str,
    value: str,
    delta: Optional[str] = None,
    tooltip: Optional[str] = None,
    help_text: Optional[str] = None
):
    """
    Display a metric with optional tooltip and help text.
    
    Args:
        label: Metric label
        value: Metric value
        delta: Optional delta value
        tooltip: Optional tooltip text
        help_text: Optional help text (shows as expandable)
    """
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.metric(label=label, value=value, delta=delta)
    
    if tooltip or help_text:
        with col2:
            if tooltip:
                st.markdown(f"*{tooltip}*")
            if help_text:
                with st.expander("?"):
                    st.markdown(help_text)


def safe_calculation(
    func: Callable,
    error_message: str = "Calculation failed",
    default_value: Any = None,
    show_error: bool = True
) -> Any:
    """
    Safely execute a calculation with error handling.
    
    Args:
        func: Function to execute
        error_message: Message to display on error
        default_value: Default value to return on error
        show_error: Whether to show error message to user
        
    Returns:
        Function result or default_value on error
    """
    try:
        return func()
    except Exception as e:
        if show_error:
            st.error(f"{error_message}: {str(e)}")
        return default_value


def show_progress_bar(total: int, current: int, message: str = "Progress"):
    """
    Display a progress bar.
    
    Args:
        total: Total number of steps
        current: Current step
        message: Progress message
    """
    progress = current / total
    st.progress(progress, text=f"{message}: {current}/{total} ({progress*100:.1f}%)")


def create_model_selector_with_help():
    """
    Create an enhanced model selector with help text for each model.
    """
    model_info = {
        "Black-Scholes": {
            "description": "Analytical solution for European options",
            "pros": "Fast, accurate for vanilla options",
            "cons": "European options only",
            "best_for": "Quick calculations, standard options"
        },
        "Monte Carlo": {
            "description": "Stochastic simulation (100K paths)",
            "pros": "Handles complex payoffs, American options",
            "cons": "Slower, has variance",
            "best_for": "Exotic options, path-dependent features"
        },
        "Binomial Tree": {
            "description": "Discrete lattice model (CRR)",
            "pros": "American options, intuitive, flexible",
            "cons": "Slower than analytical methods",
            "best_for": "American options, educational purposes"
        }
    }
    
    # Create columns for better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_model = st.selectbox(
            "Select Pricing Model",
            options=list(model_info.keys()),
            help="Choose the mathematical model for option pricing"
        )
    
    with col2:
        st.markdown("### Model Info")
        info = model_info[selected_model]
        st.markdown(f"""
        **{info['description']}**
        
        ✅ Pros: {info['pros']}  
        ⚠️ Cons: {info['cons']}  
        🎯 Best for: {info['best_for']}
        """)
    
    return selected_model


def show_convergence_indicator(diff_pct: float, threshold: float = 1.0):
    """
    Show a visual indicator of convergence quality.
    
    Args:
        diff_pct: Difference percentage from reference
        threshold: Threshold for "good" convergence
    """
    if diff_pct < threshold * 0.1:
        st.success(f"✅ Excellent convergence: {diff_pct:.3f}% difference")
    elif diff_pct < threshold * 0.5:
        st.info(f"✓ Good convergence: {diff_pct:.3f}% difference")
    elif diff_pct < threshold:
        st.warning(f"⚠ Acceptable convergence: {diff_pct:.3f}% difference")
    else:
        st.error(f"❌ Poor convergence: {diff_pct:.3f}% difference")


def create_download_button(
    data: Any,
    filename: str,
    button_text: str = "Download",
    mime_type: str = "text/csv"
):
    """
    Create a styled download button.
    
    Args:
        data: Data to download
        filename: Filename for download
        button_text: Button text
        mime_type: MIME type for download
    """
    st.download_button(
        label=f"📥 {button_text}",
        data=data,
        file_name=filename,
        mime=mime_type,
        help=f"Download {filename}"
    )


def show_feature_badge(text: str, badge_type: str = "info"):
    """
    Display a feature badge.
    
    Args:
        text: Badge text
        badge_type: Type of badge (info, success, warning, error)
    """
    colors = {
        "info": "#3498db",
        "success": "#2ecc71",
        "warning": "#f39c12",
        "error": "#e74c3c"
    }
    
    color = colors.get(badge_type, colors["info"])
    
    st.markdown(
        f"""
        <span style="
            background-color: {color};
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
            display: inline-block;
        ">{text}</span>
        """,
        unsafe_allow_html=True
    )


def create_greek_explanation_card(greek_name: str):
    """
    Create an expandable card with Greek explanation.
    
    Args:
        greek_name: Name of the Greek (Delta, Gamma, etc.)
    """
    explanations = {
        "Delta": {
            "symbol": "Δ",
            "definition": "Rate of change of option value with respect to underlying price",
            "range": "Call: 0 to 1, Put: -1 to 0",
            "interpretation": "Hedge ratio - number of shares to hedge one option",
            "example": "Delta of 0.6 means option gains $0.60 for every $1 increase in stock"
        },
        "Gamma": {
            "symbol": "Γ",
            "definition": "Rate of change of Delta with respect to underlying price",
            "range": "Always positive for long positions",
            "interpretation": "Measures Delta stability - higher gamma = less stable delta",
            "example": "Gamma of 0.05 means Delta increases by 0.05 for every $1 stock increase"
        },
        "Theta": {
            "symbol": "Θ",
            "definition": "Rate of change of option value with respect to time",
            "range": "Usually negative (time decay)",
            "interpretation": "Time decay per day - how much value lost daily",
            "example": "Theta of -0.05 means option loses $0.05 in value per day"
        },
        "Vega": {
            "symbol": "ν",
            "definition": "Rate of change of option value with respect to volatility",
            "range": "Always positive for long positions",
            "interpretation": "Sensitivity to volatility changes",
            "example": "Vega of 0.20 means option gains $0.20 for 1% vol increase"
        },
        "Rho": {
            "symbol": "ρ",
            "definition": "Rate of change of option value with respect to interest rate",
            "range": "Positive for calls, negative for puts",
            "interpretation": "Sensitivity to interest rate changes",
            "example": "Rho of 0.10 means option gains $0.10 for 1% rate increase"
        }
    }
    
    if greek_name in explanations:
        info = explanations[greek_name]
        with st.expander(f"📚 Learn about {greek_name} ({info['symbol']})"):
            st.markdown(f"""
            **Definition**: {info['definition']}
            
            **Typical Range**: {info['range']}
            
            **Interpretation**: {info['interpretation']}
            
            **Example**: {info['example']}
            """)


def show_calculation_settings(model_name: str):
    """
    Display model-specific calculation settings.
    
    Args:
        model_name: Name of the model
    """
    with st.expander("⚙️ Calculation Settings"):
        if model_name == "Monte Carlo":
            st.markdown("""
            **Current Settings:**
            - Simulations: 100,000 paths
            - Time steps: 252 (daily)
            - Variance reduction: Antithetic variates ✓
            - Random seed: 42 (reproducible)
            - Confidence interval: 95%
            """)
        elif model_name == "Binomial Tree":
            steps = st.session_state.get('bt_steps', 100)
            is_american = st.session_state.get('bt_is_american', False)
            st.markdown(f"""
            **Current Settings:**
            - Time steps: {steps}
            - Option type: {'American' if is_american else 'European'}
            - Method: Cox-Ross-Rubinstein (CRR)
            - Early exercise: {'Enabled' if is_american else 'Disabled'}
            """)
        elif model_name == "Black-Scholes":
            st.markdown("""
            **Current Settings:**
            - Method: Analytical closed-form solution
            - Greeks: Analytical derivatives
            - Assumptions: Constant volatility, log-normal returns
            - European options only
            """)


def show_performance_metrics(calc_time_ms: float, model_name: str):
    """
    Display performance metrics for a calculation.
    
    Args:
        calc_time_ms: Calculation time in milliseconds
        model_name: Name of the model used
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("⚡ Calculation Time", f"{calc_time_ms:.2f} ms")
    
    with col2:
        if calc_time_ms < 10:
            speed = "Very Fast"
            icon = "🚀"
        elif calc_time_ms < 50:
            speed = "Fast"
            icon = "✓"
        elif calc_time_ms < 200:
            speed = "Moderate"
            icon = "⏱"
        else:
            speed = "Slow"
            icon = "⏳"
        st.metric("Speed", f"{icon} {speed}")
    
    with col3:
        st.metric("Model", model_name)
