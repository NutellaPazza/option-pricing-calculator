"""
Test script for Monte Carlo model.
Verifies implementation and compares with Black-Scholes.
"""

import sys
sys.path.insert(0, '/Users/giovannidestasio/Option-pricer')

from models.monte_carlo import MonteCarloModel
from models.black_scholes import BlackScholesModel
import time

print("=" * 70)
print("MONTE CARLO MODEL - TEST & VERIFICATION")
print("=" * 70)

# Test parameters
spot = 100.0
strike = 100.0
time_to_maturity = 1.0
risk_free_rate = 0.05
volatility = 0.20
option_type = 'call'

print("\n📊 Test Parameters:")
print(f"   Spot Price: ${spot}")
print(f"   Strike Price: ${strike}")
print(f"   Time to Maturity: {time_to_maturity} years")
print(f"   Risk-Free Rate: {risk_free_rate*100}%")
print(f"   Volatility: {volatility*100}%")
print(f"   Option Type: {option_type.upper()}")

# Initialize models
print("\n🎲 Initializing Monte Carlo Model...")
mc_model = MonteCarloModel(
    num_simulations=100000,
    num_steps=252,
    seed=42,
    antithetic=True
)

print("📐 Initializing Black-Scholes Model (for comparison)...")
bs_model = BlackScholesModel()

# Test 1: Basic pricing
print("\n" + "=" * 70)
print("TEST 1: Basic Option Pricing")
print("=" * 70)

print("\n⏱️  Timing Monte Carlo...")
start_time = time.time()
mc_price = mc_model.calculate_price(
    spot, strike, time_to_maturity,
    risk_free_rate, volatility, option_type
)
mc_time = time.time() - start_time

print("⏱️  Timing Black-Scholes...")
start_time = time.time()
bs_price = bs_model.calculate_price(
    spot, strike, time_to_maturity,
    risk_free_rate, volatility, option_type
)
bs_time = time.time() - start_time

print(f"\n💰 Monte Carlo Price: ${mc_price:.6f} (computed in {mc_time:.3f}s)")
print(f"💰 Black-Scholes Price: ${bs_price:.6f} (computed in {bs_time:.3f}s)")
print(f"📊 Difference: ${abs(mc_price - bs_price):.6f} ({abs(mc_price - bs_price)/bs_price*100:.2f}%)")

if abs(mc_price - bs_price) / bs_price < 0.02:  # Within 2%
    print("✅ PASS: Monte Carlo converged close to analytical solution!")
else:
    print("⚠️  WARNING: Larger difference than expected")

# Test 2: Put option
print("\n" + "=" * 70)
print("TEST 2: Put Option Pricing")
print("=" * 70)

mc_put = mc_model.calculate_price(
    spot, strike, time_to_maturity,
    risk_free_rate, volatility, 'put'
)
bs_put = bs_model.calculate_price(
    spot, strike, time_to_maturity,
    risk_free_rate, volatility, 'put'
)

print(f"\n💰 Monte Carlo Put: ${mc_put:.6f}")
print(f"💰 Black-Scholes Put: ${bs_put:.6f}")
print(f"📊 Difference: ${abs(mc_put - bs_put):.6f} ({abs(mc_put - bs_put)/bs_put*100:.2f}%)")

if abs(mc_put - bs_put) / bs_put < 0.02:
    print("✅ PASS: Put option pricing accurate!")
else:
    print("⚠️  WARNING: Larger difference than expected")

# Test 3: Put-Call Parity
print("\n" + "=" * 70)
print("TEST 3: Put-Call Parity Verification")
print("=" * 70)

import numpy as np

# Put-Call Parity: C - P = S - K*e^(-rT)
parity_mc = mc_price - mc_put
parity_theoretical = spot - strike * np.exp(-risk_free_rate * time_to_maturity)

print(f"\n📊 Monte Carlo: C - P = ${parity_mc:.6f}")
print(f"📊 Theoretical: S - K*e^(-rT) = ${parity_theoretical:.6f}")
print(f"📊 Difference: ${abs(parity_mc - parity_theoretical):.6f}")

if abs(parity_mc - parity_theoretical) < 0.5:
    print("✅ PASS: Put-Call Parity holds!")
else:
    print("⚠️  WARNING: Put-Call Parity violation detected")

# Test 4: Confidence Interval
print("\n" + "=" * 70)
print("TEST 4: Confidence Interval Estimation")
print("=" * 70)

print("\n⏱️  Calculating 95% confidence interval...")
confidence_result = mc_model.calculate_price_with_confidence(
    spot, strike, time_to_maturity,
    risk_free_rate, volatility, option_type,
    confidence_level=0.95
)

print(f"\n💰 Estimated Price: ${confidence_result['price']:.6f}")
print(f"📊 Standard Error: ${confidence_result['std_error']:.6f}")
print(f"📊 95% CI: [${confidence_result['lower_bound']:.6f}, ${confidence_result['upper_bound']:.6f}]")
print(f"📐 Black-Scholes Price: ${bs_price:.6f}")

if confidence_result['lower_bound'] <= bs_price <= confidence_result['upper_bound']:
    print("✅ PASS: Black-Scholes price within confidence interval!")
else:
    print("⚠️  INFO: Black-Scholes outside CI (expected occasionally)")

# Test 5: ITM and OTM options
print("\n" + "=" * 70)
print("TEST 5: ITM and OTM Options")
print("=" * 70)

# ITM Call (spot > strike)
itm_strike = 90
mc_itm = mc_model.calculate_price(spot, itm_strike, time_to_maturity, risk_free_rate, volatility, 'call')
bs_itm = bs_model.calculate_price(spot, itm_strike, time_to_maturity, risk_free_rate, volatility, 'call')

print(f"\n📈 ITM Call (K=90):")
print(f"   Monte Carlo: ${mc_itm:.6f}")
print(f"   Black-Scholes: ${bs_itm:.6f}")
print(f"   Difference: {abs(mc_itm - bs_itm)/bs_itm*100:.2f}%")

# OTM Call (spot < strike)
otm_strike = 110
mc_otm = mc_model.calculate_price(spot, otm_strike, time_to_maturity, risk_free_rate, volatility, 'call')
bs_otm = bs_model.calculate_price(spot, otm_strike, time_to_maturity, risk_free_rate, volatility, 'call')

print(f"\n📉 OTM Call (K=110):")
print(f"   Monte Carlo: ${mc_otm:.6f}")
print(f"   Black-Scholes: ${bs_otm:.6f}")
print(f"   Difference: {abs(mc_otm - bs_otm)/bs_otm*100:.2f}%")

if mc_itm > mc_price > mc_otm:
    print("\n✅ PASS: Correct ordering: ITM > ATM > OTM")
else:
    print("\n❌ FAIL: Incorrect price ordering")

# Test 6: Model Info
print("\n" + "=" * 70)
print("TEST 6: Model Information")
print("=" * 70)

info = mc_model.get_model_info()
print(f"\n📝 Model Name: {info['name']}")
print(f"📝 Type: {info['type']}")
print(f"📝 Description: {info['description']}")
print(f"\n📝 Parameters:")
for key, value in info['parameters'].items():
    print(f"   - {key}: {value}")

print("\n📝 Advantages:")
for adv in info['advantages']:
    print(f"   ✓ {adv}")

print("\n📝 Disadvantages:")
for dis in info['disadvantages']:
    print(f"   ✗ {dis}")

# Summary
print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)

tests_passed = 0
total_tests = 5

# Check all tests
if abs(mc_price - bs_price) / bs_price < 0.02:
    tests_passed += 1
if abs(mc_put - bs_put) / bs_put < 0.02:
    tests_passed += 1
if abs(parity_mc - parity_theoretical) < 0.5:
    tests_passed += 1
if confidence_result['lower_bound'] <= bs_price <= confidence_result['upper_bound']:
    tests_passed += 1
if mc_itm > mc_price > mc_otm:
    tests_passed += 1

print(f"\n✅ Tests Passed: {tests_passed}/{total_tests}")
print(f"📊 Success Rate: {tests_passed/total_tests*100:.1f}%")

if tests_passed == total_tests:
    print("\n🎉 ALL TESTS PASSED! Monte Carlo model is working correctly!")
elif tests_passed >= 4:
    print("\n✅ GOOD! Most tests passed. Minor discrepancies acceptable for MC.")
else:
    print("\n⚠️  WARNING: Some tests failed. Review implementation.")

print("\n" + "=" * 70)
