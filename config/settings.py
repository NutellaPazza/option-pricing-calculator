"""
Global configurations for Option Pricing Calculator application
"""

# Default parameters for options
DEFAULT_PARAMS = {
    'spot_price': 100.0,
    'strike_price': 100.0,
    'time_to_maturity': 1.0,
    'risk_free_rate': 0.05,
    'volatility': 0.20,
    'option_type': 'call'
}

# Validation ranges
VALIDATION_RANGES = {
    'spot_price': (0.01, 10000.0),
    'strike_price': (0.01, 10000.0),
    'time_to_maturity': (0.01, 10.0),
    'risk_free_rate': (-0.1, 0.5),
    'volatility': (0.001, 2.0)
}

# Models configuration
MODELS = {
    'black_scholes': {
        'name': 'Black-Scholes',
        'type': 'Analytical',
        'supports_american': False,
        'description': 'Closed-form solution for European options'
    },
    'monte_carlo': {
        'name': 'Monte Carlo',
        'type': 'Simulation',
        'supports_american': True,
        'default_simulations': 100000,
        'description': 'Stochastic simulation for complex payoffs'
    },
    'binomial': {
        'name': 'Binomial Tree',
        'type': 'Discrete',
        'supports_american': True,
        'default_steps': 100,
        'description': 'Discrete time model for American/European options'
    }
}

# Greeks configuration
GREEKS = ['Delta', 'Gamma', 'Theta', 'Vega', 'Rho']

# Chart configuration
CHART_CONFIG = {
    'default_width': 800,
    'default_height': 600,
    'color_scheme': 'plotly',
    'heatmap_colorscale': 'RdYlGn',
    'profit_colorscale': 'RdYlGn'
}

# Developer information
DEVELOPER_INFO = {
    'name': 'Giovanni De Stasio',
    'title': 'Financial Student',
    'email': 'giovanni.destasio@example.com',
    'linkedin': 'www.linkedin.com/in/gds-',
    'github': 'https://github.com/giovannidestasio',
    'github_repo': 'https://github.com/giovannidestasio/option-pricer'
}

# App metadata
APP_INFO = {
    'title': 'Option Pricing Calculator',
    'version': '1.0.0',
    'description': 'Advanced Financial Derivatives Pricing Models',
    'icon': '📊'
}
