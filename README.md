# 📊 Option Pricing Calculator# 📊 Option Pricing Calculator



> **An AI-Assisted Financial Engineering Project**  Advanced financial derivatives pricing models implemented in Python with Streamlit.

> Built in 2025 using advanced AI-guided development techniques

Developed by **Giovanni Destasio** - Financial Engineer & Quantitative Developer

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

[![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)](https://streamlit.io/)## 🚀 Features

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[![GitHub](https://img.shields.io/badge/GitHub-NutellaPazza-black.svg)](https://github.com/NutellaPazza)- **Multiple Pricing Models**

  - Black-Scholes analytical solution

---  - Monte Carlo simulation

  - Binomial tree model

## 🎯 About This Project

- **Greeks Analysis**

This **Option Pricing Calculator** is a comprehensive web application that implements three advanced mathematical models for pricing financial derivatives:  - Delta, Gamma, Theta, Vega, Rho

  - Real-time sensitivity analysis

- **Black-Scholes Model** - Analytical solution for European options

- **Monte Carlo Simulation** - Stochastic simulation with 100K paths- **Interactive Visualizations**

- **Binomial Tree** - Discrete-time lattice for American & European options  - Heatmaps for price surfaces

  - Greeks sensitivity charts

### 🌟 What Makes This Project Unique  - Volatility surfaces (3D)

  - Profit/Loss diagrams

This project represents a **new paradigm in software development**: **AI-Assisted Coding** (or "Vibe Coding").

- **Professional UI**

Unlike traditional development where code is written line-by-line by a human programmer, this entire application was built through:  - Clean, intuitive interface

  - Real-time calculations

1. **Human Vision & Direction** - Conceptual design and requirements  - Responsive design

2. **AI Implementation** - Code generation guided by Claude AI

3. **Iterative Refinement** - Continuous feedback and improvement loop## 🛠️ Installation

4. **Domain Expertise** - Financial theory combined with AI capabilities

### Prerequisites

**The result?** A professional-grade financial application built by a finance student with limited coding experience, demonstrating the transformative power of AI in democratizing software development.- Python 3.10 or higher

- pip package manager

---

### Setup

## ✨ Features

```bash

### 📈 Three Pricing Models# Clone the repository

git clone https://github.com/giovannidestasio/option-pricer.git

| Model | Type | American Options | Speed | Accuracy |cd option-pricer

|-------|------|-----------------|-------|----------|

| **Black-Scholes** | Analytical | ❌ | ⚡⚡⚡ | ✅✅✅ |# Create virtual environment

| **Monte Carlo** | Stochastic | ✅ | ⚡ | ✅✅✅ |python3 -m venv venv

| **Binomial Tree** | Discrete | ✅ | ⚡⚡ | ✅✅✅ |source venv/bin/activate  # On Windows: venv\Scripts\activate



### 🎯 Key Capabilities# Install dependencies

pip install -r requirements.txt

- ✅ **Real-time Option Pricing** - Instant calculations across all models```

- ✅ **Complete Greeks Analysis** - Delta, Gamma, Theta, Vega, Rho

- ✅ **Interactive Visualizations** - Plotly-based charts and heatmaps## ▶️ Running the Application

- ✅ **Sensitivity Analysis** - Scenario testing and what-if analysis

- ✅ **Strategy Builder** - 11 pre-built option strategies```bash

- ✅ **Educational Tools** - Interactive tutorials and glossary# Activate virtual environment (if not already active)

- ✅ **Export Functionality** - CSV and Excel reportssource venv/bin/activate



### 📊 Advanced Analytics# Run Streamlit app

streamlit run app.py

- 🔥 **Interactive Heatmaps** - Price surfaces, Greeks correlation, Risk exposure```

- 📈 **Strategy Comparison** - Side-by-side analysis of multi-leg strategies

- 🎓 **Educational Content** - Built-in tutorials and formula referenceThe application will open in your default browser at `http://localhost:8501`

- 💾 **Data Export** - Professional reports in multiple formats

## 📁 Project Structure

---

```

## 🚀 Quick Startoption-pricer/

├── app.py                    # Main Streamlit application

### Installation├── config/

│   └── settings.py          # Global configurations

```bash├── models/

# Clone the repository│   ├── base_model.py        # Abstract base class

git clone https://github.com/NutellaPazza/option-pricing-calculator.git│   ├── black_scholes.py     # Black-Scholes model

cd option-pricing-calculator│   ├── monte_carlo.py       # Monte Carlo simulation

│   └── binomial.py          # Binomial tree model

# Create virtual environment├── calculations/

python3 -m venv venv│   ├── greeks.py           # Greeks calculations

source venv/bin/activate  # On Windows: venv\Scripts\activate│   └── payoffs.py          # Payoff functions

├── ui/

# Install dependencies│   ├── sidebar.py          # Sidebar components

pip install -r requirements.txt│   ├── results.py          # Results display

```│   ├── charts.py           # Standard charts

│   ├── heatmaps.py         # Interactive heatmaps

### Run the Application│   └── about_tab.py        # About page

├── utils/

```bash│   ├── validators.py       # Input validation

streamlit run app.py│   └── helpers.py          # Helper functions

```└── tests/

    └── test_*.py           # Unit tests

The app will open in your browser at `http://localhost:8501````



---## 🎯 Usage



## 📚 Documentation1. **Select Model**: Choose between Black-Scholes, Monte Carlo, or Binomial Tree

2. **Input Parameters**: 

### Project Structure   - Spot Price (S)

   - Strike Price (K)

```   - Time to Maturity (T)

option-pricing-calculator/   - Risk-Free Rate (r)

├── app.py                      # Main Streamlit application   - Volatility (σ)

├── models/                     # Pricing models3. **View Results**: See option price, Greeks, and visualizations

│   ├── black_scholes.py       # Black-Scholes implementation4. **Analyze**: Explore heatmaps and sensitivity analysis

│   ├── monte_carlo.py         # Monte Carlo simulation

│   └── binomial_tree.py       # Binomial tree model## 🧪 Testing

├── calculations/               # Greeks and payoff calculations

│   ├── greeks.py              # Greek calculations```bash

│   └── payoffs.py             # Payoff functions# Run all tests

├── strategies/                 # Option strategiespytest

│   ├── options.py             # Strategy implementations

│   └── visualizations.py      # Strategy charts# Run with coverage

├── ui/                         # User interface componentspytest --cov=.

│   ├── sidebar.py             # Input parameters```

│   ├── results.py             # Results display

│   ├── charts.py              # Visualization components## 📚 Mathematical Models

│   ├── heatmaps.py            # Heatmap generators

│   ├── tutorials.py           # Educational content### Black-Scholes Model

│   └── export.py              # Export functionalityClassic closed-form solution for European options pricing under constant volatility assumption.

├── config/                     # Configuration files

│   └── settings.py            # Global settings### Monte Carlo Simulation

└── tests/                      # Test suiteStochastic simulation method for pricing complex derivatives and path-dependent options.

    └── test_*.py              # Unit tests

```### Binomial Tree Model

Discrete-time model suitable for American options with early exercise features.

### Models Explained

## 🤝 Contributing

#### 1. Black-Scholes Model

```pythonContributions are welcome! Please feel free to submit a Pull Request.

# Analytical formula for European options

C = S₀N(d₁) - Ke^(-rT)N(d₂)## 📄 License

```

This project is licensed under the MIT License - see the LICENSE file for details.

- **Pros**: Instant calculation, exact solution

- **Cons**: European options only, assumes constant volatility## 👨‍💻 Author



#### 2. Monte Carlo Simulation**Giovanni Destasio**

```python- Email: giovanni.destasio@example.com

# Simulate 100,000 price paths- LinkedIn: [giovanni-destasio](https://linkedin.com/in/giovanni-destasio)

S_T = S₀ * exp((r - σ²/2)T + σ√T * Z)- GitHub: [giovannidestasio](https://github.com/giovannidestasio)

```

## 🙏 Acknowledgments

- **Pros**: Handles complex payoffs, path-dependent options

- **Cons**: Slower, requires many simulations for accuracy- Inspired by modern quantitative finance tools

- Built with Streamlit, NumPy, SciPy, and Plotly

#### 3. Binomial Tree- Financial mathematics references from standard texts

```python

# Build lattice with Cox-Ross-Rubinstein---

u = e^(σ√Δt), d = 1/u, p = (e^(rΔt) - d)/(u - d)

```*Built with ❤️ for the quantitative finance community*


- **Pros**: American options, early exercise, intuitive
- **Cons**: Slower for many steps, oscillates near convergence

---

## 🎓 Educational Background

### About the Creator

This project was created by **Giovanni De Stasio**, a **Finance & Economics student at Bocconi University**, as an exploration of the intersection between:

- **Financial Theory** - Options pricing, risk management, derivatives
- **AI Technology** - Large language models for code generation
- **Quantitative Methods** - Stochastic calculus, numerical methods

### The AI-Assisted Development Approach

**Traditional Development:**
```
Concept → Learn Programming → Write Code → Debug → Deploy
(Months/Years of learning required)
```

**AI-Assisted Development:**
```
Concept → Direct AI → Guide Implementation → Refine → Deploy
(Days/Weeks with domain expertise)
```

This project demonstrates that **domain knowledge + AI capabilities** can replace traditional programming skills for many applications.

---

## 🛠️ Technology Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Language** | Python 3.10+ | Core programming |
| **Framework** | Streamlit | Web interface |
| **Computation** | NumPy, SciPy | Mathematical operations |
| **Visualization** | Plotly | Interactive charts |
| **Data** | Pandas | Data manipulation |
| **Export** | OpenPyXL | Excel generation |
| **AI Assistant** | Claude (Anthropic) | Code generation & guidance |

---

## 🎯 Use Cases

### For Students
- Learn option pricing theory through interactive models
- Understand Greeks and their implications
- Practice with educational tutorials

### For Analysts
- Quick option valuation for research
- Sensitivity analysis for reports
- Export-ready charts and tables

### For Traders
- Real-time pricing across models
- Strategy comparison and analysis
- Risk metrics calculation

### For Educators
- Teaching tool for derivatives courses
- Visual demonstrations of concepts
- Interactive examples

---

## 🚧 Roadmap

### Future Enhancements

- [ ] **Implied Volatility Calculator** - Reverse pricing
- [ ] **Historical Data Integration** - Yahoo Finance API
- [ ] **Portfolio Greeks** - Multi-position analysis
- [ ] **Advanced Models** - Heston, SABR, Jump Diffusion
- [ ] **Real-time Market Data** - Live option prices
- [ ] **Mobile App** - React Native version
- [ ] **API Endpoints** - RESTful API for integrations

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

While this project was built with AI assistance, contributions are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📬 Contact

**Giovanni De Stasio**  
Finance & Economics Student @ Bocconi University

- 📧 Email: [gdestasio922@gmail.com](mailto:gdestasio922@gmail.com)
- 💼 LinkedIn: [linkedin.com/in/gds-](https://www.linkedin.com/in/gds-)
- 🐙 GitHub: [@NutellaPazza](https://github.com/NutellaPazza)

---

## 🙏 Acknowledgments

- **Claude (Anthropic)** - AI assistant that made this project possible
- **Bocconi University** - Academic foundation in finance
- **Streamlit** - Excellent framework for data apps
- **Plotly** - Beautiful interactive visualizations
- **Open Source Community** - For the amazing Python ecosystem

---

## ⭐ Star History

If you find this project useful, please consider giving it a ⭐!

---

<div align="center">

**Built with 🤖 AI Assistance + 🧠 Human Expertise**

*"The future of software development is not about writing code, but about guiding intelligence."*

**© 2025 Giovanni De Stasio**

</div>
