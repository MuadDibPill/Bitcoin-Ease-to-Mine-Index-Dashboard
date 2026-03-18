# ⛏️ Ease to Mine Index (EMI) Dashboard

An interactive dashboard visualizing Bitcoin mining conditions across 18 jurisdictions worldwide.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 🎯 Overview

The **Ease to Mine Index (EMI)** is a composite framework designed to assess the overall attractiveness of jurisdictions for Bitcoin mining. This dashboard provides interactive visualizations of the index data.

### Dimensions Analyzed
- 💰 **Fiscal** (20%) — Taxation environment, incentives
- 📋 **Permit & Licensing** (17.5%) — Construction permits, operational licenses
- ⚖️ **Legal** (17.5%) — Regulatory framework, legal clarity
- ⚡ **Energy & Grid** (25%) — Energy access, grid connection
- 🚢 **Tariff & Import** (15%) — Customs, import duties
- 🌡️ **Operating Conditions** (5%) — Climate suitability

## 🚀 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/emi-dashboard.git
cd emi-dashboard

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Deploy to Streamlit Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repository and `app.py`
5. Click "Deploy"

## 📁 Project Structure

```
emi-dashboard/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── data/
│   └── emi_scores.csv    # EMI data
└── README.md
```

## 📊 Features

- **Overall Ranking** — Horizontal bar chart of EMI scores
- **Dimension Analysis** — Radar charts and heatmaps for multi-dimensional comparison
- **Permit Timeline** — Construction permit duration by country
- **Regional View** — Geographic analysis and scatter plots
- **Interactive Filters** — Filter by region, score range
- **Data Export** — Download filtered data as CSV

## 📈 Data Source

Data collected through a survey of 48 industry practitioners between December 2025 and February 2026, covering:
- Industrial miners
- Mining associations
- Industry journalists
- Subject matter experts

## 🔗 Links

- [Hashlabs Website](https://hashlabs.io)
- [Full EMI Report](#) *(add link)*

## 📝 License

MIT License — See [LICENSE](LICENSE) for details.

---

*Built with ❤️ by Hashlabs Research Team*
