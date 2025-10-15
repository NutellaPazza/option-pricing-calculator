"""
Interactive tutorial system for Option Pricing Calculator.
Educational content and guided learning paths.
"""

import streamlit as st
from typing import Dict, List, Any


class TutorialSystem:
    """Interactive tutorial and educational content manager."""
    
    def __init__(self):
        """Initialize tutorial system with content."""
        self.tutorials = {
            'basics': {
                'title': '📚 Options Basics',
                'steps': 5,
                'duration': '10 min',
                'description': 'Learn fundamental concepts of options trading',
                'difficulty': 'Beginner'
            },
            'greeks': {
                'title': '📊 Understanding Greeks',
                'steps': 6,
                'duration': '15 min',
                'description': 'Master option sensitivity measures',
                'difficulty': 'Intermediate'
            },
            'strategies': {
                'title': '🎯 Option Strategies',
                'steps': 8,
                'duration': '20 min',
                'description': 'Learn common multi-leg strategies',
                'difficulty': 'Advanced'
            },
            'pricing_models': {
                'title': '🔬 Pricing Models',
                'steps': 7,
                'duration': '15 min',
                'description': 'Understand Black-Scholes, Monte Carlo, and Binomial Tree',
                'difficulty': 'Advanced'
            }
        }
        
        self.glossary = self._create_glossary()
        self.formulas = self._create_formulas()
    
    def _create_glossary(self) -> Dict[str, Dict[str, str]]:
        """Create comprehensive glossary of terms."""
        return {
            'Call Option': {
                'definition': 'A financial contract giving the buyer the right, but not obligation, to buy an underlying asset at a specified price within a specific time period.',
                'example': 'Buying a call option on stock XYZ at $100 strike allows you to buy the stock at $100, even if market price is higher.',
                'category': 'Basics'
            },
            'Put Option': {
                'definition': 'A financial contract giving the buyer the right, but not obligation, to sell an underlying asset at a specified price within a specific time period.',
                'example': 'Buying a put option on stock XYZ at $100 strike allows you to sell the stock at $100, even if market price is lower.',
                'category': 'Basics'
            },
            'Strike Price': {
                'definition': 'The predetermined price at which the option can be exercised.',
                'example': 'A call option with strike $50 allows buying the asset at $50.',
                'category': 'Basics'
            },
            'Delta': {
                'definition': 'Measures the rate of change of option value with respect to changes in underlying price. Range: 0 to 1 for calls, -1 to 0 for puts.',
                'example': 'Delta of 0.6 means option price changes by $0.60 for every $1 change in stock price.',
                'category': 'Greeks'
            },
            'Gamma': {
                'definition': 'Measures the rate of change in Delta with respect to changes in underlying price.',
                'example': 'High gamma means Delta changes rapidly as stock price moves.',
                'category': 'Greeks'
            },
            'Theta': {
                'definition': 'Measures the rate of decline in option value over time (time decay).',
                'example': 'Theta of -0.05 means option loses $0.05 per day, all else equal.',
                'category': 'Greeks'
            },
            'Vega': {
                'definition': 'Measures sensitivity to changes in implied volatility.',
                'example': 'Vega of 0.20 means option gains $0.20 for 1% increase in volatility.',
                'category': 'Greeks'
            },
            'Rho': {
                'definition': 'Measures sensitivity to changes in interest rates.',
                'example': 'Rho of 0.10 means option gains $0.10 for 1% increase in interest rate.',
                'category': 'Greeks'
            },
            'Implied Volatility': {
                'definition': "Market's forecast of likely movement in asset price, derived from option prices.",
                'example': 'IV of 20% suggests market expects ±20% annual price movement.',
                'category': 'Advanced'
            },
            'American Option': {
                'definition': 'Option that can be exercised at any time before expiration.',
                'example': 'Most stock options are American-style.',
                'category': 'Types'
            },
            'European Option': {
                'definition': 'Option that can only be exercised at expiration.',
                'example': 'Index options are typically European-style.',
                'category': 'Types'
            },
            'Moneyness': {
                'definition': 'Relationship between spot price and strike price.',
                'example': 'ATM (at-the-money): strike ≈ spot. ITM (in-the-money): call strike < spot.',
                'category': 'Basics'
            },
            'Premium': {
                'definition': 'The price paid to purchase an option contract.',
                'example': 'If a call option costs $5, you pay $5 premium per share ($500 per contract).',
                'category': 'Basics'
            },
            'Intrinsic Value': {
                'definition': 'The actual value of an option if exercised immediately.',
                'example': 'Call at $95 strike with stock at $100 has $5 intrinsic value.',
                'category': 'Valuation'
            },
            'Time Value': {
                'definition': 'The portion of option premium exceeding intrinsic value.',
                'example': 'Option worth $8 with $5 intrinsic value has $3 time value.',
                'category': 'Valuation'
            },
            'In-The-Money (ITM)': {
                'definition': 'Option with positive intrinsic value.',
                'example': 'Call with strike $95 when stock is $100 (intrinsic value = $5).',
                'category': 'Moneyness'
            },
            'At-The-Money (ATM)': {
                'definition': 'Option where strike price equals (or is very close to) spot price.',
                'example': 'Call with strike $100 when stock is $100.',
                'category': 'Moneyness'
            },
            'Out-The-Money (OTM)': {
                'definition': 'Option with no intrinsic value.',
                'example': 'Call with strike $105 when stock is $100 (would lose money if exercised).',
                'category': 'Moneyness'
            },
            'Volatility': {
                'definition': 'A measure of price fluctuation of the underlying asset.',
                'example': 'Volatility of 30% means the asset typically moves ±30% annually.',
                'category': 'Risk'
            }
        }
    
    def _create_formulas(self) -> Dict[str, Dict[str, Any]]:
        """Create formula explanations with LaTeX."""
        return {
            'black_scholes_call': {
                'name': 'Black-Scholes Call Option',
                'latex': r'C = S_0 N(d_1) - K e^{-rT} N(d_2)',
                'variables': {
                    'C': 'Call option price',
                    'S₀': 'Current stock price',
                    'K': 'Strike price',
                    'r': 'Risk-free rate',
                    'T': 'Time to maturity',
                    'N(·)': 'Cumulative normal distribution',
                    'd₁': '(ln(S/K) + (r + σ²/2)T) / (σ√T)',
                    'd₂': 'd₁ - σ√T',
                    'σ': 'Volatility'
                },
                'explanation': 'The Black-Scholes formula calculates the theoretical price of European call options based on the assumption of log-normal price distribution and constant volatility.'
            },
            'black_scholes_put': {
                'name': 'Black-Scholes Put Option',
                'latex': r'P = K e^{-rT} N(-d_2) - S_0 N(-d_1)',
                'variables': {
                    'P': 'Put option price',
                    'S₀': 'Current stock price',
                    'K': 'Strike price',
                    'r': 'Risk-free rate',
                    'T': 'Time to maturity',
                    'N(·)': 'Cumulative normal distribution'
                },
                'explanation': 'The Black-Scholes put formula, derived from put-call parity, calculates theoretical put option prices.'
            },
            'delta': {
                'name': 'Delta',
                'latex': r'\Delta = \frac{\partial V}{\partial S} = N(d_1) \text{ (call)}, \quad N(d_1) - 1 \text{ (put)}',
                'variables': {
                    'Δ': 'Delta',
                    'V': 'Option value',
                    'S': 'Stock price',
                    'N(d₁)': 'Cumulative normal of d₁'
                },
                'explanation': 'Delta measures how much the option price changes for a $1 change in stock price. Also represents approximate probability of finishing in-the-money.'
            },
            'gamma': {
                'name': 'Gamma',
                'latex': r'\Gamma = \frac{\partial^2 V}{\partial S^2} = \frac{N\'(d_1)}{S\sigma\sqrt{T}}',
                'variables': {
                    'Γ': 'Gamma',
                    "N'(d₁)": 'Normal probability density at d₁',
                    'σ': 'Volatility'
                },
                'explanation': 'Gamma measures the rate of change of Delta. Higher gamma means Delta is more sensitive to price changes.'
            },
            'theta': {
                'name': 'Theta',
                'latex': r'\Theta = -\frac{\partial V}{\partial T}',
                'variables': {
                    'Θ': 'Theta',
                    'T': 'Time',
                    'V': 'Option value'
                },
                'explanation': 'Theta measures time decay - how much value the option loses per day as time passes, all else equal.'
            },
            'vega': {
                'name': 'Vega',
                'latex': r'\mathcal{V} = \frac{\partial V}{\partial \sigma} = S\sqrt{T}N\'(d_1)',
                'variables': {
                    'ν': 'Vega',
                    'σ': 'Volatility',
                    'V': 'Option value'
                },
                'explanation': 'Vega measures sensitivity to changes in implied volatility. Options gain value when volatility increases.'
            },
            'rho': {
                'name': 'Rho',
                'latex': r'\rho = \frac{\partial V}{\partial r}',
                'variables': {
                    'ρ': 'Rho',
                    'r': 'Risk-free rate',
                    'V': 'Option value'
                },
                'explanation': 'Rho measures sensitivity to changes in interest rates. Generally less significant than other Greeks.'
            }
        }
    
    def render_tutorial_launcher(self):
        """Render tutorial selection and launcher."""
        st.markdown("## 🎓 Interactive Tutorials")
        st.markdown("Start learning with our step-by-step guided tutorials!")
        
        st.markdown("---")
        
        # Tutorial cards in 2 columns
        cols = st.columns(2)
        
        for idx, (key, tutorial) in enumerate(self.tutorials.items()):
            with cols[idx % 2]:
                with st.container():
                    st.markdown(f"### {tutorial['title']}")
                    
                    # Difficulty badge
                    diff_colors = {
                        'Beginner': '🟢',
                        'Intermediate': '🟡',
                        'Advanced': '🔴'
                    }
                    st.markdown(
                        f"{diff_colors[tutorial['difficulty']]} **{tutorial['difficulty']}** | "
                        f"⏱️ {tutorial['duration']} | "
                        f"📝 {tutorial['steps']} steps"
                    )
                    
                    st.markdown(tutorial['description'])
                    
                    if st.button(f"Start Tutorial", key=f"start_{key}", use_container_width=True):
                        st.session_state['current_tutorial'] = key
                        st.session_state['tutorial_step'] = 0
                        st.rerun()
                
                st.markdown("---")
    
    def render_active_tutorial(self, tutorial_key: str, step: int):
        """Render active tutorial content with navigation."""
        tutorial_content = self._get_tutorial_content(tutorial_key)
        
        if step >= len(tutorial_content):
            # Tutorial completed
            st.success("🎉 **Tutorial Completed!**")
            st.balloons()
            st.markdown("### Congratulations!")
            st.markdown("You've completed this tutorial. You can now:")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📚 Back to Tutorials", use_container_width=True):
                    del st.session_state['current_tutorial']
                    del st.session_state['tutorial_step']
                    st.rerun()
            
            with col2:
                if st.button("🏠 Back to App", use_container_width=True):
                    del st.session_state['current_tutorial']
                    del st.session_state['tutorial_step']
                    st.session_state['active_tab'] = 0
                    st.rerun()
            return
        
        current_step = tutorial_content[step]
        
        # Progress bar
        progress = (step + 1) / len(tutorial_content)
        st.progress(progress, text=f"Step {step + 1} of {len(tutorial_content)}")
        
        # Step content
        st.markdown(f"## {current_step['title']}")
        st.markdown(current_step['content'])
        
        # Interactive elements
        if 'interactive' in current_step:
            st.markdown("---")
            current_step['interactive']()
        
        # Navigation buttons
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if step > 0:
                if st.button("⬅️ Previous", use_container_width=True):
                    st.session_state['tutorial_step'] -= 1
                    st.rerun()
        
        with col2:
            if st.button("🏠 Exit Tutorial", use_container_width=True):
                del st.session_state['current_tutorial']
                del st.session_state['tutorial_step']
                st.rerun()
        
        with col3:
            if st.button("Next ➡️", use_container_width=True):
                st.session_state['tutorial_step'] += 1
                st.rerun()
    
    def _get_tutorial_content(self, tutorial_key: str) -> List[Dict]:
        """Get tutorial content based on key."""
        if tutorial_key == 'basics':
            return self._basics_tutorial()
        elif tutorial_key == 'greeks':
            return self._greeks_tutorial()
        elif tutorial_key == 'strategies':
            return self._strategies_tutorial()
        elif tutorial_key == 'pricing_models':
            return self._pricing_models_tutorial()
        
        return []
    
    def _basics_tutorial(self) -> List[Dict]:
        """Option basics tutorial content."""
        return [
            {
                'title': '📚 Welcome to Options Trading',
                'content': '''
### What are Options?

Options are **financial derivatives** that give you the **right, but not the obligation**, 
to buy or sell an asset at a predetermined price within a specific time period.

#### Key Points:
- Options are contracts between buyers and sellers
- They derive value from an underlying asset (stocks, indexes, commodities, etc.)
- Two main types: **Calls** and **Puts**
- Limited risk for buyers, defined profit/loss profiles
- Used for speculation, hedging, and income generation

#### Why Trade Options?
- **Leverage:** Control large positions with less capital
- **Flexibility:** Profit in bull, bear, or neutral markets
- **Risk Management:** Hedge existing positions
- **Income Generation:** Collect premiums through selling

Let's explore the fundamentals step by step!
                '''
            },
            {
                'title': '📞 Call Options Explained',
                'content': '''
### Call Options: The Right to Buy

A **Call Option** gives you the right to **buy** an asset at a specified price (strike price).

#### Real-World Example:
You think stock XYZ will rise from its current price of $100.

**Your trade:**
- Buy 1 Call Option
- Strike Price: $105
- Premium Paid: $3.00
- Expiration: 30 days

#### Possible Outcomes:

**Scenario 1: Stock rises to $110**
- Exercise the option: Buy at $105, immediately worth $110
- Profit = ($110 - $105) - $3 = **$2 per share**
- Return on Investment: 67%!

**Scenario 2: Stock stays at $100**
- Don't exercise (would lose money)
- Loss = Premium paid = **$3 per share**
- This is your maximum loss

**Scenario 3: Stock rises to $107**
- Exercise: Profit = ($107 - $105) - $3 = **-$1 per share**
- Break-even point is at $108 ($105 strike + $3 premium)

#### When to Use Calls:
✅ Bullish on the underlying asset  
✅ Want leverage on price increases  
✅ Limited risk (premium only)  
                ''',
                'interactive': lambda: self._call_option_demo()
            },
            {
                'title': '📉 Put Options Explained',
                'content': '''
### Put Options: The Right to Sell

A **Put Option** gives you the right to **sell** an asset at a specified price.

#### Real-World Example:
You think stock XYZ will fall from $100.

**Your trade:**
- Buy 1 Put Option
- Strike Price: $95
- Premium Paid: $2.50
- Expiration: 30 days

#### Possible Outcomes:

**Scenario 1: Stock falls to $85**
- Exercise: Sell at $95 (even though market is $85)
- Profit = ($95 - $85) - $2.50 = **$7.50 per share**
- Return: 300%!

**Scenario 2: Stock stays at $100**
- Don't exercise (strike is lower than market)
- Loss = Premium = **$2.50 per share**

**Scenario 3: Stock falls to $93**
- Exercise: Profit = ($95 - $93) - $2.50 = **-$0.50**
- Break-even at $92.50 ($95 - $2.50)

#### When to Use Puts:
✅ Bearish on the underlying  
✅ Portfolio protection (hedging)  
✅ Profit from declining prices  
                ''',
                'interactive': lambda: self._put_option_demo()
            },
            {
                'title': '🎯 Essential Option Terminology',
                'content': '''
### Key Terms You Must Know

#### **Strike Price (K)**
The predetermined price at which you can buy (call) or sell (put) the underlying.
- *Example:* A call with $100 strike lets you buy at $100

#### **Premium**
The price you pay to buy the option contract.
- *Example:* Premium of $5 means you pay $500 per contract (100 shares)

#### **Expiration Date**
The last day you can exercise the option. After this, the option becomes worthless.
- *Common:* Weekly, monthly, quarterly expirations

#### **Intrinsic Value**
The real, tangible value if exercised now:
- **Call:** max(Spot - Strike, 0)
- **Put:** max(Strike - Spot, 0)

#### **Time Value**
Premium minus intrinsic value. Represents the "hope" value:
- Time Value = Premium - Intrinsic Value
- Decays to zero at expiration

#### **Moneyness** - Where is the option?

**In-The-Money (ITM):**
- Call: Spot > Strike (has intrinsic value)
- Put: Spot < Strike

**At-The-Money (ATM):**
- Spot ≈ Strike (most actively traded)

**Out-The-Money (OTM):**
- Call: Spot < Strike (only time value)
- Put: Spot > Strike
                '''
            },
            {
                'title': '💡 Test Your Knowledge',
                'content': '''
### Quick Quiz: Options Basics

Answer these questions to check your understanding!
                ''',
                'interactive': lambda: self._basics_quiz()
            }
        ]
    
    def _call_option_demo(self):
        """Interactive call option payoff calculator."""
        st.markdown("#### 🧪 Interactive Call Option Calculator")
        st.markdown("Adjust the parameters to see how call options work:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Input Parameters:**")
            spot = st.slider("Stock Price at Expiration ($)", 80, 120, 100, key="call_spot")
            strike = st.number_input("Strike Price ($)", value=100, min_value=50, max_value=150, key="call_strike")
            premium = st.number_input("Premium Paid ($)", value=5.0, min_value=0.1, max_value=20.0, step=0.5, key="call_premium")
        
        with col2:
            st.markdown("**Results:**")
            intrinsic = max(spot - strike, 0)
            profit = intrinsic - premium
            roi = (profit / premium * 100) if premium > 0 else 0
            
            st.metric("Intrinsic Value", f"${intrinsic:.2f}")
            st.metric("Profit/Loss", f"${profit:.2f}", 
                     delta=f"{roi:+.1f}%")
            
            if profit > 0:
                st.success(f"✅ **Exercise!** Buy at ${strike:.2f}, sell at ${spot:.2f}")
            elif profit == -premium:
                st.error(f"❌ **Don't Exercise** - Loss limited to premium: ${premium:.2f}")
            else:
                st.warning(f"⚠️ **Exercise** but still net loss of ${-profit:.2f}")
            
            # Break-even
            be = strike + premium
            st.info(f"🎯 **Break-Even:** ${be:.2f}")
    
    def _put_option_demo(self):
        """Interactive put option payoff calculator."""
        st.markdown("#### 🧪 Interactive Put Option Calculator")
        st.markdown("Adjust the parameters to see how put options work:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Input Parameters:**")
            spot = st.slider("Stock Price at Expiration ($)", 80, 120, 100, key="put_spot")
            strike = st.number_input("Strike Price ($)", value=100, min_value=50, max_value=150, key="put_strike")
            premium = st.number_input("Premium Paid ($)", value=5.0, min_value=0.1, max_value=20.0, step=0.5, key="put_premium")
        
        with col2:
            st.markdown("**Results:**")
            intrinsic = max(strike - spot, 0)
            profit = intrinsic - premium
            roi = (profit / premium * 100) if premium > 0 else 0
            
            st.metric("Intrinsic Value", f"${intrinsic:.2f}")
            st.metric("Profit/Loss", f"${profit:.2f}",
                     delta=f"{roi:+.1f}%")
            
            if profit > 0:
                st.success(f"✅ **Exercise!** Sell at ${strike:.2f}, buy at ${spot:.2f}")
            elif profit == -premium:
                st.error(f"❌ **Don't Exercise** - Loss limited to premium: ${premium:.2f}")
            else:
                st.warning(f"⚠️ **Exercise** but still net loss of ${-profit:.2f}")
            
            # Break-even
            be = strike - premium
            st.info(f"🎯 **Break-Even:** ${be:.2f}")
    
    def _basics_quiz(self):
        """Interactive quiz for basics tutorial."""
        st.markdown("Answer all questions to complete the tutorial:")
        
        questions = [
            {
                'question': "What does a CALL option give you the right to do?",
                'options': ['Buy the underlying asset', 'Sell the underlying asset', 'Hold the asset indefinitely', 'Short sell the asset'],
                'correct': 0,
                'explanation': "A call option gives you the RIGHT to BUY the underlying at the strike price."
            },
            {
                'question': "If you buy a PUT option and the stock price RISES significantly, what happens?",
                'options': [
                    'You exercise and make large profit',
                    'You don\'t exercise and lose only the premium paid',
                    'You must buy the stock',
                    'You get a refund of premium'
                ],
                'correct': 1,
                'explanation': "When you buy a put and price rises, the put becomes worthless. You don't exercise and lose only the premium you paid."
            },
            {
                'question': "What is the MAXIMUM LOSS for an option BUYER?",
                'options': ['Unlimited', 'Strike price', 'Premium paid', 'Spot price - Strike price'],
                'correct': 2,
                'explanation': "Option buyers have limited risk: maximum loss is the premium paid for the option."
            },
            {
                'question': "A call option has Strike=$100, Spot=$110, Premium=$8. What is the intrinsic value?",
                'options': ['$2', '$8', '$10', '$18'],
                'correct': 2,
                'explanation': "Intrinsic value = max(Spot - Strike, 0) = max(110-100, 0) = $10"
            }
        ]
        
        if 'quiz_answers' not in st.session_state:
            st.session_state['quiz_answers'] = {}
        
        score = 0
        for i, q in enumerate(questions):
            st.markdown(f"**Q{i+1}: {q['question']}**")
            answer = st.radio(
                "Select your answer:",
                q['options'],
                key=f"quiz_basics_q{i}",
                index=st.session_state['quiz_answers'].get(f"q{i}", 0)
            )
            
            # Store answer
            st.session_state['quiz_answers'][f"q{i}"] = q['options'].index(answer)
            
            # Check button
            if st.button(f"Check Answer", key=f"check_basics_{i}"):
                if q['options'].index(answer) == q['correct']:
                    st.success(f"✅ Correct! {q['explanation']}")
                    score += 1
                else:
                    st.error(f"❌ Incorrect. {q['explanation']}")
                    st.info(f"Correct answer: **{q['options'][q['correct']]}**")
            
            st.markdown("---")
        
        # Show final score if all answered
        if len(st.session_state.get('quiz_answers', {})) == len(questions):
            st.markdown(f"### Your Progress: {len(st.session_state['quiz_answers'])}/{len(questions)} answered")
    
    def _greeks_tutorial(self) -> List[Dict]:
        """Greeks tutorial content."""
        return [
            {
                'title': '📊 Introduction to The Greeks',
                'content': '''
### What are "The Greeks"?

The Greeks are **risk measures** that describe how option prices change with market conditions.

#### Why Are They Important?
- **Risk Management:** Understand your exposure
- **Hedging:** Create balanced portfolios
- **Trading:** Identify opportunities
- **Professional Analysis:** Industry standard metrics

#### The Five Main Greeks:

**Delta (Δ):** Sensitivity to price changes  
**Gamma (Γ):** Rate of change of Delta  
**Theta (Θ):** Time decay  
**Vega (ν):** Sensitivity to volatility changes  
**Rho (ρ):** Sensitivity to interest rate changes  

Each Greek measures a different dimension of risk. Master them to trade like a pro!
                '''
            },
            {
                'title': '📈 Delta: The Speed of Change',
                'content': '''
### Delta (Δ): Price Sensitivity

Delta measures how much the option price changes when the underlying moves by $1.

#### Key Properties:

**Call Options:** Delta from 0 to +1
- Deep OTM: ~0 (barely moves)
- ATM: ~0.5 (moves half as fast as stock)
- Deep ITM: ~1 (moves dollar-for-dollar)

**Put Options:** Delta from -1 to 0
- Deep OTM: ~0
- ATM: ~-0.5
- Deep ITM: ~-1

#### Interpretation as Probability:
Delta also approximates the probability of finishing in-the-money!
- Delta 0.70 ≈ 70% chance of expiring ITM

#### Practical Use:
- **Position Sizing:** 100 shares ≈ 1 Call with Δ=1.0
- **Hedging:** Delta-neutral portfolios
- **Direction:** Positive delta = bullish, negative = bearish
                '''
            },
            {
                'title': '🎢 Gamma: Acceleration',
                'content': '''
### Gamma (Γ): Delta's Rate of Change

Gamma measures how fast Delta changes as the stock price moves.

#### Think of It Like Driving:
- **Delta** = Speed (mph)
- **Gamma** = Acceleration (how fast speed changes)

#### Key Characteristics:

**Highest at ATM:** Maximum uncertainty = maximum gamma  
**Lower for ITM/OTM:** More certainty = lower gamma  
**Decreases Near Expiration:** Time amplifies gamma effects  

#### Practical Implications:

**High Gamma (ATM options near expiration):**
- Delta changes rapidly
- Position can swing dramatically
- Requires active management

**Low Gamma (deep ITM/OTM, long-dated):**
- Delta stays stable
- More predictable behavior

#### Use Cases:
- **Gamma Scalping:** Profit from volatility
- **Risk Management:** Monitor position stability
- **Strategy Selection:** High vs low gamma strategies
                '''
            },
            {
                'title': '⏰ Theta: The Enemy of Time',
                'content': '''
### Theta (Θ): Time Decay

Theta measures how much option value decreases each day as time passes.

#### Universal Truth:
**All options lose value as time passes** (with other factors constant)

#### Key Characteristics:

**Always Negative for Long Options:**
- You're fighting time decay
- Option loses value every day

**Accelerates Near Expiration:**
- Exponential decay curve
- Last 30 days = rapid decay

**Highest for ATM Options:**
- Most time value to lose

#### Practical Example:
Option with Θ = -0.05
- Loses $0.05 per day
- Over weekend: ~$0.15 loss
- 30 days: ~$1.50 loss

#### Strategy Implications:

**Long Options (negative theta):**
- Need strong directional move
- Time is your enemy
- Best for high-conviction trades

**Short Options (positive theta):**
- Collect decay daily
- Time is your friend
- Income generation strategies
                '''
            },
            {
                'title': '💨 Vega: Volatility Sensitivity',
                'content': '''
### Vega (ν): The Volatility Greek

Vega measures how much option value changes for a 1% change in implied volatility.

#### Volatility 101:
**Implied Volatility (IV):** Market's expectation of future price swings
- High IV = Expensive options (uncertainty premium)
- Low IV = Cheap options

#### Key Properties:

**Always Positive:**
- Higher volatility = Higher option value
- True for both calls and puts

**Highest for ATM:**
- Maximum sensitivity to IV changes

**Highest for Long-Dated:**
- More time = more uncertainty value

#### Real-World Example:
Option with Vega = 0.20, IV = 25%

**IV increases to 30% (+5%):**
- Option gains: 0.20 × 5 = **+$1.00**

**IV drops to 20% (-5%):**
- Option loses: 0.20 × 5 = **-$1.00**

#### Trading Applications:

**Long Vega (buy options):**
- Profit from volatility expansion
- Earnings, news events
- "Volatility plays"

**Short Vega (sell options):**
- Profit from volatility contraction
- After big moves
- "Volatility mean reversion"
                '''
            },
            {
                'title': '💡 Greeks Quiz',
                'content': '''
### Test Your Greeks Knowledge
                ''',
                'interactive': lambda: self._greeks_quiz()
            }
        ]
    
    def _greeks_quiz(self):
        """Quiz for Greeks tutorial."""
        questions = [
            {
                'question': "What does a Delta of 0.60 on a call option mean?",
                'options': [
                    'Option moves $0.60 for every $1 move in stock',
                    'Option has 60% probability of expiring ITM',
                    'Both A and B (approximately)',
                    'Option will gain $0.60 per day'
                ],
                'correct': 2,
                'explanation': "Delta measures price sensitivity AND approximates probability of expiring in-the-money!"
            },
            {
                'question': "When is Gamma highest?",
                'options': [
                    'Deep in-the-money',
                    'Deep out-of-the-money',
                    'At-the-money, especially near expiration',
                    'Gamma is always constant'
                ],
                'correct': 2,
                'explanation': "Gamma peaks at-the-money where there's maximum uncertainty, and increases as expiration approaches."
            },
            {
                'question': "If you BUY an option, is Theta your friend or enemy?",
                'options': [
                    'Friend - you collect time decay',
                    'Enemy - you lose value each day',
                    'Neither - Theta only affects sellers',
                    'Depends on the stock price'
                ],
                'correct': 1,
                'explanation': "When long options, Theta is negative - you lose value daily due to time decay. You need the underlying to move in your favor to overcome this."
            },
            {
                'question': "Your option has Vega=0.25. If implied volatility increases by 4%, what happens?",
                'options': [
                    'Option loses $0.25',
                    'Option gains $1.00',
                    'Option gains $0.25',
                    'No change'
                ],
                'correct': 1,
                'explanation': "Vega measures sensitivity to IV. Gain = Vega × IV change = 0.25 × 4 = $1.00"
            }
        ]
        
        if 'greeks_quiz_answers' not in st.session_state:
            st.session_state['greeks_quiz_answers'] = {}
        
        for i, q in enumerate(questions):
            st.markdown(f"**Q{i+1}: {q['question']}**")
            answer = st.radio(
                "Select your answer:",
                q['options'],
                key=f"quiz_greeks_q{i}",
                index=st.session_state['greeks_quiz_answers'].get(f"gq{i}", 0)
            )
            
            st.session_state['greeks_quiz_answers'][f"gq{i}"] = q['options'].index(answer)
            
            if st.button(f"Check Answer", key=f"check_greeks_{i}"):
                if q['options'].index(answer) == q['correct']:
                    st.success(f"✅ Correct! {q['explanation']}")
                else:
                    st.error(f"❌ Incorrect. {q['explanation']}")
                    st.info(f"Correct answer: **{q['options'][q['correct']]}**")
            
            st.markdown("---")
    
    def _strategies_tutorial(self) -> List[Dict]:
        """Strategies tutorial placeholder."""
        return [
            {
                'title': '🎯 Option Strategies Overview',
                'content': '''
### Multi-Leg Option Strategies

Single options are powerful, but combining multiple options creates strategies with unique risk/reward profiles.

#### Why Use Strategies?

**Directional Plays:**
- Reduce cost vs single options
- Define risk precisely

**Income Generation:**
- Collect premiums
- Enhance returns

**Volatility Plays:**
- Profit from big moves (any direction)
- Or profit from no movement

**Risk Management:**
- Cap losses
- Protect existing positions

We'll explore spreads, straddles, strangles, and more!
                '''
            }
            # Additional strategy steps would go here
        ]
    
    def _pricing_models_tutorial(self) -> List[Dict]:
        """Pricing models tutorial placeholder."""
        return [
            {
                'title': '🔬 Option Pricing Models',
                'content': '''
### How Are Options Priced?

Understanding pricing models helps you:
- Evaluate if options are cheap or expensive
- Understand assumptions and limitations
- Choose the right model for your needs

#### The Three Models:

**Black-Scholes:**
- Closed-form solution
- Fast and accurate
- Industry standard

**Monte Carlo:**
- Simulation-based
- Flexible for complex payoffs
- Statistical approach

**Binomial Tree:**
- Discrete time steps
- Visual and intuitive
- Handles American options

Let's explore each model!
                '''
            }
            # Additional pricing model steps would go here
        ]
    
    def render_glossary(self):
        """Render searchable glossary."""
        st.markdown("## 📖 Options Glossary")
        st.markdown("Search and explore options terminology:")
        
        # Search functionality
        col1, col2 = st.columns([2, 1])
        
        with col1:
            search = st.text_input(
                "🔍 Search terms",
                placeholder="e.g., Delta, Call Option, Volatility...",
                key="glossary_search"
            )
        
        with col2:
            # Category filter
            categories = sorted(list(set(term['category'] for term in self.glossary.values())))
            category_filter = st.multiselect(
                "Filter by category",
                categories,
                default=categories,
                key="glossary_filter"
            )
        
        st.markdown("---")
        
        # Filter terms
        filtered_terms = {
            term: info for term, info in self.glossary.items()
            if (search.lower() in term.lower() or search.lower() in info['definition'].lower())
            and info['category'] in category_filter
        }
        
        if filtered_terms:
            # Display count
            st.caption(f"Showing {len(filtered_terms)} of {len(self.glossary)} terms")
            
            # Display terms
            for term, info in sorted(filtered_terms.items()):
                with st.expander(f"**{term}** 📂 {info['category']}"):
                    st.markdown(f"**Definition:**")
                    st.markdown(info['definition'])
                    st.markdown(f"**Example:**")
                    st.info(info['example'])
        else:
            st.warning("No terms found matching your search criteria.")
            st.info("💡 Try different keywords or adjust category filters.")
    
    def render_formulas(self):
        """Render formula reference with explanations."""
        st.markdown("## 🧮 Formula Reference")
        st.markdown("Mathematical formulas used in option pricing:")
        
        st.markdown("---")
        
        for key, formula in self.formulas.items():
            with st.expander(f"**{formula['name']}**", expanded=False):
                # Display formula
                st.markdown("### Formula:")
                st.latex(formula['latex'])
                
                # Variables
                st.markdown("### Variables:")
                for var, desc in formula['variables'].items():
                    st.markdown(f"- **{var}**: {desc}")
                
                # Explanation
                st.markdown("### Explanation:")
                st.info(formula['explanation'])


def render_education_tab():
    """Main education tab renderer."""
    
    # Initialize tutorial system
    if 'tutorial_system' not in st.session_state:
        st.session_state['tutorial_system'] = TutorialSystem()
    
    tutorial_sys = st.session_state['tutorial_system']
    
    # Check if tutorial is active
    if 'current_tutorial' in st.session_state:
        # Show active tutorial
        tutorial_sys.render_active_tutorial(
            st.session_state['current_tutorial'],
            st.session_state.get('tutorial_step', 0)
        )
    else:
        # Show education hub
        st.header("🎓 Education Center")
        st.markdown("""
        Welcome to the **Option Pricing Calculator Education Center**! 
        Learn options trading through interactive tutorials, reference materials, and formulas.
        """)
        
        # Create tabs for different educational content
        tab1, tab2, tab3 = st.tabs(["📚 Interactive Tutorials", "📖 Glossary", "🧮 Formula Reference"])
        
        with tab1:
            tutorial_sys.render_tutorial_launcher()
        
        with tab2:
            tutorial_sys.render_glossary()
        
        with tab3:
            tutorial_sys.render_formulas()
