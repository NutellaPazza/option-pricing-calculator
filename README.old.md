# 📊 Option Pricing Calculator

Advanced financial derivatives pricing models implemented in Python with Streamlit.

Developed by **Giovanni Destasio** - Financial Engineer & Quantitative Developer

## 🚀 Features

- **Multiple Pricing Models**
  - Black-Scholes analytical solution
  - Monte Carlo simulation
  - Binomial tree model

- **Greeks Analysis**
  - Delta, Gamma, Theta, Vega, Rho
  - Real-time sensitivity analysis

- **Interactive Visualizations**
  - Heatmaps for price surfaces
  - Greeks sensitivity charts
  - Volatility surfaces (3D)
  - Profit/Loss diagrams

- **Professional UI**
  - Clean, intuitive interface
  - Real-time calculations
  - Responsive design

## 🛠️ Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Setup

```bash
# Clone the repository
git clone https://github.com/giovannidestasio/option-pricer.git
cd option-pricer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## ▶️ Running the Application

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Run Streamlit app
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📁 Project Structure

```
option-pricer/
├── app.py                    # Main Streamlit application
├── config/
│   └── settings.py          # Global configurations
├── models/
│   ├── base_model.py        # Abstract base class
│   ├── black_scholes.py     # Black-Scholes model
│   ├── monte_carlo.py       # Monte Carlo simulation
│   └── binomial.py          # Binomial tree model
├── calculations/
│   ├── greeks.py           # Greeks calculations
│   └── payoffs.py          # Payoff functions
├── ui/
│   ├── sidebar.py          # Sidebar components
│   ├── results.py          # Results display
│   ├── charts.py           # Standard charts
│   ├── heatmaps.py         # Interactive heatmaps
│   └── about_tab.py        # About page
├── utils/
│   ├── validators.py       # Input validation
│   └── helpers.py          # Helper functions
└── tests/
    └── test_*.py           # Unit tests
```

## 🎯 Usage

1. **Select Model**: Choose between Black-Scholes, Monte Carlo, or Binomial Tree
2. **Input Parameters**: 
   - Spot Price (S)
   - Strike Price (K)
   - Time to Maturity (T)
   - Risk-Free Rate (r)
   - Volatility (σ)
3. **View Results**: See option price, Greeks, and visualizations
4. **Analyze**: Explore heatmaps and sensitivity analysis

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.
```

## 📚 Mathematical Models

### Black-Scholes Model
Classic closed-form solution for European options pricing under constant volatility assumption.

### Monte Carlo Simulation
Stochastic simulation method for pricing complex derivatives and path-dependent options.

### Binomial Tree Model
Discrete-time model suitable for American options with early exercise features.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Giovanni Destasio**
- Email: giovanni.destasio@example.com
- LinkedIn: [giovanni-destasio](https://linkedin.com/in/giovanni-destasio)
- GitHub: [giovannidestasio](https://github.com/giovannidestasio)

## 🙏 Acknowledgments

- Inspired by modern quantitative finance tools
- Built with Streamlit, NumPy, SciPy, and Plotly
- Financial mathematics references from standard texts

---

*Built with ❤️ for the quantitative finance community*
