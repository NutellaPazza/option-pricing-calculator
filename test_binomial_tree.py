"""
Test script for Binomial Tree model.
Verifies implementation and compares with Black-Scholes.
"""

import sys
sys.path.insert(0, '/Users/giovannidestasio/Option-pricer')

from models.binomial_tree import BinomialTreeModel
from models.black_scholes import BlackScholesModel
import time

print("=" * 70)
print("BINOMIAL TREE MODEL - TEST & VERIFICATION")
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
print("\n🌲 Initializing Binomial Tree Model (European)...")
bt_euro = BinomialTreeModel(num_steps=100, american=False)

print("🌲 Initializing Binomial Tree Model (American)...")
bt_amer = BinomialTreeModel(num_steps=100, american=True)

print("📐 Initializing Black-Scholes Model (for comparison)...")
bs_model = BlackScholesModel()

# Test 1: European Call Option
print("\n" + "=" * 70)
print("TEST 1: European Call Option Pricing")
print("=" * 70)

print("\n⏱️  Timing Binomial Tree (European)...")
start_time = time.time()
bt_euro_price = bt_euro.calculate_price(
    spot, strike, time_to_maturity,
    risk_free_rate, volatility, option_type
)
bt_euro_time = time.time() - start_time

print("⏱️  Timing Black-Scholes...")
start_time = time.time()
bs_price = bs_model.calculate_price(
    spot, strike, time_to_maturity,
    risk_free_rate, volatility, option_type
)
bs_time = time.time() - start_time

print(f"\n💰 Binomial Tree (European): ${bt_euro_price:.6f} (computed in {bt_euro_time:.3f}s)")
print(f"💰 Black-Scholes: ${bs_price:.6f} (computed in {bs_time:.3f}s)")
print(f"📊 Difference: ${abs(bt_euro_price - bs_price):.6f} ({abs(bt_euro_price - bs_price)/bs_price*100:.2f}%)")

if abs(bt_euro_price - bs_price) / bs_price < 0.02:  # Within 2%
    print("✅ PASS: Binomial Tree converged close to Black-Scholes!")
else:
    print("⚠️  WARNING: Larger difference than expected")

# Test 2: European Put Option
print("\n" + "=" * 70)
print("TEST 2: European Put Option Pricing")
print("=" * 70)

bt_euro_put = bt_euro.calculate_price(
    spot, strike, time_to_maturity,
    risk_free_rate, volatility, 'put'
)
bs_put = bs_model.calculate_price(
    spot, strike, time_to_maturity,
    risk_free_rate, volatility, 'put'
)

print(f"\n💰 Binomial Tree Put: ${bt_euro_put:.6f}")
print(f"💰 Black-Scholes Put: ${bs_put:.6f}")
print(f"📊 Difference: ${abs(bt_euro_put - bs_put):.6f} ({abs(bt_euro_put - bs_put)/bs_put*100:.2f}%)")

if abs(bt_euro_put - bs_put) / bs_put < 0.02:
    print("✅ PASS: Put option pricing accurate!")
else:
    print("⚠️  WARNING: Larger difference than expected")

# Test 3: Put-Call Parity
print("\n" + "=" * 70)
print("TEST 3: Put-Call Parity Verification")
print("=" * 70)

import numpy as np

# Put-Call Parity: C - P = S - K*e^(-rT)
parity_bt = bt_euro_price - bt_euro_put
parity_theoretical = spot - strike * np.exp(-risk_free_rate * time_to_maturity)

print(f"\n📊 Binomial Tree: C - P = ${parity_bt:.6f}")
print(f"📊 Theoretical: S - K*e^(-rT) = ${parity_theoretical:.6f}")
print(f"📊 Difference: ${abs(parity_bt - parity_theoretical):.6f}")

if abs(parity_bt - parity_theoretical) < 0.1:
    print("✅ PASS: Put-Call Parity holds!")
else:
    print("⚠️  WARNING: Put-Call Parity violation detected")

# Test 4: American vs European Options
print("\n" + "=" * 70)
print("TEST 4: American vs European Options")
print("=" * 70)

print("\n⏱️  Calculating American option price...")
bt_amer_price = bt_amer.calculate_price(
    spot, strike, time_to_maturity,
    risk_free_rate, volatility, option_type
)

print(f"\n💰 European Call: ${bt_euro_price:.6f}")
print(f"💰 American Call: ${bt_amer_price:.6f}")
print(f"📊 Difference: ${bt_amer_price - bt_euro_price:.6f}")

if bt_amer_price >= bt_euro_price - 0.01:  # American >= European (with tolerance)
    print("✅ PASS: American option value >= European (as expected)")
else:
    print("❌ FAIL: American option should be at least as valuable as European")

# Test American Put (more interesting for early exercise)
bt_amer_put = bt_amer.calculate_price(
    spot, strike, time_to_maturity,
    risk_free_rate, volatility, 'put'
)

print(f"\n💰 European Put: ${bt_euro_put:.6f}")
print(f"💰 American Put: ${bt_amer_put:.6f}")
print(f"📊 Early Exercise Premium: ${bt_amer_put - bt_euro_put:.6f}")

if bt_amer_put > bt_euro_put:
    print("✅ PASS: American put has early exercise value!")
else:
    print("✓ INFO: No significant early exercise premium for these parameters")

# Test 5: Convergence Analysis
print("\n" + "=" * 70)
print("TEST 5: Convergence Analysis")
print("=" * 70)

print("\n⏱️  Testing convergence with different step sizes...")
convergence = bt_euro.get_convergence_analysis(
    spot, strike, time_to_maturity,
    risk_free_rate, volatility, option_type,
    step_sizes=[10, 25, 50, 100, 200]
)

print("\n📊 Convergence Results:")
print(f"{'Steps':<10} {'Price':<12} {'Diff from BS':<15} {'% Diff'}")
print("-" * 55)
for steps, price in zip(convergence['step_sizes'], convergence['prices']):
    diff = price - bs_price
    pct_diff = (diff / bs_price) * 100
    print(f"{steps:<10} ${price:<11.6f} ${diff:+.6f}      {pct_diff:+.3f}%")

print(f"\n📊 Black-Scholes Target: ${bs_price:.6f}")
print(f"📊 Final BT Price (200 steps): ${convergence['prices'][-1]:.6f}")

if abs(convergence['prices'][-1] - bs_price) / bs_price < 0.01:
    print("✅ PASS: Convergence to Black-Scholes verified!")
else:
    print("⚠️  INFO: More steps may be needed for tighter convergence")

# Test 6: ITM and OTM Options
print("\n" + "=" * 70)
print("TEST 6: ITM and OTM Options")
print("=" * 70)

# ITM Call (spot > strike)
itm_strike = 90
bt_itm = bt_euro.calculate_price(spot, itm_strike, time_to_maturity, risk_free_rate, volatility, 'call')
bs_itm = bs_model.calculate_price(spot, itm_strike, time_to_maturity, risk_free_rate, volatility, 'call')

print(f"\n📈 ITM Call (K=90):")
print(f"   Binomial Tree: ${bt_itm:.6f}")
print(f"   Black-Scholes: ${bs_itm:.6f}")
print(f"   Difference: {abs(bt_itm - bs_itm)/bs_itm*100:.2f}%")

# OTM Call (spot < strike)
otm_strike = 110
bt_otm = bt_euro.calculate_price(spot, otm_strike, time_to_maturity, risk_free_rate, volatility, 'call')
bs_otm = bs_model.calculate_price(spot, otm_strike, time_to_maturity, risk_free_rate, volatility, 'call')

print(f"\n📉 OTM Call (K=110):")
print(f"   Binomial Tree: ${bt_otm:.6f}")
print(f"   Black-Scholes: ${bs_otm:.6f}")
print(f"   Difference: {abs(bt_otm - bs_otm)/bs_otm*100:.2f}%")

if bt_itm > bt_euro_price > bt_otm:
    print("\n✅ PASS: Correct ordering: ITM > ATM > OTM")
else:
    print("\n❌ FAIL: Incorrect price ordering")

# Test 7: Model Info
print("\n" + "=" * 70)
print("TEST 7: Model Information")
print("=" * 70)

info = bt_euro.get_model_info()
print(f"\n📝 Model Name: {info['name']}")
print(f"📝 Type: {info['type']}")
print(f"📝 Description: {info['description']}")
print(f"\n📝 Parameters:")
for key, value in info['parameters'].items():
    print(f"   - {key}: {value}")

print("\n📝 Advantages:")
for adv in info['advantages']:
    print(f"   ✓ {adv}")

# Test 8: Tree Data
print("\n" + "=" * 70)
print("TEST 8: Tree Data Access")
print("=" * 70)

tree_data = bt_euro.get_tree_data()
if tree_data:
    print(f"\n✅ Tree data retrieved successfully")
    print(f"📊 Price tree shape: {tree_data['price_tree'].shape}")
    print(f"📊 Option tree shape: {tree_data['option_tree'].shape}")
    print(f"📊 Number of steps: {tree_data['num_steps']}")
    print(f"📊 American option: {tree_data['american']}")
    
    # Show some sample values
    print(f"\n📊 Sample prices at expiration (last 5 nodes):")
    for i in range(max(0, bt_euro.num_steps - 4), bt_euro.num_steps + 1):
        print(f"   Node {i}: S=${tree_data['price_tree'][bt_euro.num_steps][i]:.2f}, V=${tree_data['option_tree'][bt_euro.num_steps][i]:.2f}")
else:
    print("❌ FAIL: Could not retrieve tree data")

# Summary
print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)

tests_passed = 0
total_tests = 7

# Check all tests
if abs(bt_euro_price - bs_price) / bs_price < 0.02:
    tests_passed += 1
if abs(bt_euro_put - bs_put) / bs_put < 0.02:
    tests_passed += 1
if abs(parity_bt - parity_theoretical) < 0.1:
    tests_passed += 1
if bt_amer_price >= bt_euro_price - 0.01:
    tests_passed += 1
if abs(convergence['prices'][-1] - bs_price) / bs_price < 0.01:
    tests_passed += 1
if bt_itm > bt_euro_price > bt_otm:
    tests_passed += 1
if tree_data is not None:
    tests_passed += 1

print(f"\n✅ Tests Passed: {tests_passed}/{total_tests}")
print(f"📊 Success Rate: {tests_passed/total_tests*100:.1f}%")

if tests_passed == total_tests:
    print("\n🎉 ALL TESTS PASSED! Binomial Tree model is working correctly!")
elif tests_passed >= 6:
    print("\n✅ EXCELLENT! Most tests passed. Model working well.")
else:
    print("\n⚠️  WARNING: Some tests failed. Review implementation.")

print("\n" + "=" * 70)
