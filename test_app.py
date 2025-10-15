"""
Simple test script to verify app can run without Streamlit server
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from models.black_scholes import BlackScholesModel
from calculations.greeks import GreeksCalculator

print("=" * 50)
print("Testing Option Pricing Calculator Components")
print("=" * 50)

# Test 1: Black-Scholes Model
print("\n1. Testing Black-Scholes Model...")
model = BlackScholesModel()
price = model.calculate_price(
    spot=100.0,
    strike=100.0,
    time_to_maturity=1.0,
    risk_free_rate=0.05,
    volatility=0.20,
    option_type='call'
)
print(f"   ✅ Call Option Price: ${price:.4f}")

# Test 2: Greeks
print("\n2. Testing Greeks Calculator...")
calc = GreeksCalculator()
greeks = calc.calculate_all_greeks(
    spot=100.0,
    strike=100.0,
    time_to_maturity=1.0,
    risk_free_rate=0.05,
    volatility=0.20,
    option_type='call'
)
print(f"   ✅ Greeks calculated: {list(greeks.keys())}")

# Test 3: Config
print("\n3. Testing Configuration...")
from config.settings import DEFAULT_PARAMS, APP_INFO
print(f"   ✅ App Title: {APP_INFO['title']}")
print(f"   ✅ Default Spot: ${DEFAULT_PARAMS['spot_price']}")

print("\n" + "=" * 50)
print("✅ ALL COMPONENTS WORKING!")
print("=" * 50)
print("\nReady to run: streamlit run app.py")
