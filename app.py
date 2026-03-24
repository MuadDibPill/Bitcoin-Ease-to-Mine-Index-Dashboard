import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="EMI Dashboard",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# COLOR PALETTE
# ============================================
COLOR_SCALE = [
    [0.00, '#922B21'], [0.07, '#C0392B'], [0.14, '#CD6155'],
    [0.21, '#DC7633'], [0.28, '#E67E22'], [0.35, '#EB984E'],
    [0.42, '#F5B041'], [0.50, '#F4D03F'], [0.57, '#F7DC6F'],
    [0.64, '#A9DFBF'], [0.71, '#7DCEA0'], [0.78, '#52BE80'],
    [0.85, '#28B463'], [0.92, '#239B56'], [1.00, '#1E8449']
]

# ============================================
# CUSTOM CSS
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;600;700;800&display=swap');
    
    * { font-family: 'Barlow', 'Forma DJR', -apple-system, BlinkMacSystemFont, sans-serif !important; }
    .stApp { font-family: 'Barlow', 'Forma DJR', sans-serif; background-color: #FFFFFF; }
    
    [data-testid="stSidebar"] { width: 256px !important; min-width: 256px !important; background-color: #FAFAFA; border-right: 1px solid #E2E8F0; }
    [data-testid="stSidebar"] > div:first-child { width: 256px !important; }
    [data-testid="stSidebar"] .stRadio > div { gap: 0 !important; }
    [data-testid="stSidebar"] .stRadio > div > label { background: transparent !important; border: none !important; padding: 8px 0 !important; cursor: pointer; font-size: 0.95rem !important; }
    [data-testid="stSidebar"] .stRadio > div > label:hover { color: #1E8449 !important; }
    [data-testid="stSidebar"] .stRadio > div > label > div:first-child { display: none !important; }
    
    /* Sidebar navigation buttons - no border, left aligned */
    [data-testid="stSidebar"] button[kind="secondary"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        text-align: left !important;
        padding: 0.5rem 0 !important;
        font-size: 0.95rem !important;
        color: #334155 !important;
        font-weight: 500 !important;
        justify-content: flex-start !important;
    }
    [data-testid="stSidebar"] button[kind="secondary"]:hover {
        color: #1E8449 !important;
        background: transparent !important;
        border: none !important;
    }
    [data-testid="stSidebar"] button[kind="secondary"]:focus {
        box-shadow: none !important;
        border: none !important;
    }
    [data-testid="stSidebar"] button[kind="secondary"]:active {
        background: transparent !important;
        border: none !important;
    }
    
    /* Expander styling - no border at all, same font size as other buttons */
    [data-testid="stSidebar"] .stExpander {
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
    }
    [data-testid="stSidebar"] .stExpander > details {
        border: none !important;
        background: transparent !important;
    }
    [data-testid="stSidebar"] .stExpander > details > summary {
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        color: #334155 !important;
        padding: 0.5rem 0 !important;
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
    }
    [data-testid="stSidebar"] .stExpander > details > summary:hover {
        color: #1E8449 !important;
    }
    [data-testid="stSidebar"] .stExpander > details[open] > summary {
        border: none !important;
        background: transparent !important;
    }
    [data-testid="stSidebar"] details {
        border: none !important;
    }
    [data-testid="stSidebar"] summary {
        border: none !important;
    }
    
    /* Buttons inside expander - indented */
    [data-testid="stSidebar"] .stExpander button[kind="secondary"] {
        padding-left: 1.5rem !important;
        font-size: 0.9rem !important;
        color: #64748B !important;
    }
    [data-testid="stSidebar"] .stExpander button[kind="secondary"]:hover {
        color: #1E8449 !important;
    }
    
    .block-container { padding-top: 2.5rem !important; }
    
    h1 { font-family: 'Barlow', sans-serif !important; font-weight: 700 !important; font-size: 2rem !important; color: #1E293B !important; margin-top: 0 !important; }
    h2, h3 { font-family: 'Barlow', sans-serif !important; font-weight: 600 !important; color: #1E293B !important; }
    
    .section-title { font-family: 'Barlow', sans-serif; font-size: 1.1rem; font-weight: 600; color: #1E293B; margin-bottom: 1rem; }
    .section-title-small { font-family: 'Barlow', sans-serif; font-size: 0.9rem; font-weight: 600; color: #1E293B; margin-bottom: 0.6rem; }
    
    [data-testid="stSelectbox"] > div > div { border: 2px solid #E2E8F0 !important; border-radius: 8px !important; background-color: #F8FAFC !important; font-size: 0.85rem !important; }
    [data-testid="stSelectbox"] > div > div:hover { border-color: #1E8449 !important; }
    
    .footer { font-family: 'Barlow', sans-serif; text-align: center; color: #64748B; padding: 2rem; font-size: 0.85rem; border-top: 1px solid #E2E8F0; margin-top: 2rem; }
    .footer a { color: #1E8449; text-decoration: none; }
    .footer a:hover { text-decoration: underline; }
    
    .sidebar-author { font-size: 0.8rem; color: #64748B; line-height: 1.5; }
    .sidebar-author a { color: #1E8449; text-decoration: none; }
    
    .info-box { background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 1rem; font-size: 0.9rem; line-height: 1.6; color: #475569; }
    .info-box-title { font-weight: 600; color: #1E293B; margin-bottom: 0.5rem; }
    .method-box-title { font-weight: 600; color: #1E293B; margin-bottom: 0.5rem; font-size: 1rem; }
    
    .subtitle-text { color: #64748B; font-size: 1rem; margin-bottom: 1.5rem; }
    
    .methodology-card { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.5rem; text-align: center; min-height: 140px; display: flex; flex-direction: column; justify-content: center; }
    .methodology-card-value { font-size: 2rem; font-weight: 700; color: #1E293B; margin-bottom: 0.25rem; }
    .methodology-card-title { font-weight: 600; color: #1E293B; font-size: 0.95rem; margin-bottom: 0.25rem; }
    .methodology-card-desc { font-size: 0.8rem; color: #64748B; min-height: 2.4em; }
    
    .timeline-item { border-left: 3px solid #002060; padding-left: 1rem; margin-bottom: 1rem; }
    .timeline-date { font-size: 0.8rem; color: #002060; font-weight: 600; }
    .timeline-title { font-weight: 600; color: #1E293B; margin: 0.25rem 0; }
    .timeline-desc { font-size: 0.85rem; color: #64748B; }
    
    .comparison-vs { font-size: 1.5rem; font-weight: 700; color: #64748B; text-align: center; padding: 1rem; }
    
    .tldr-box { background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 1rem; font-size: 0.85rem; line-height: 1.5; color: #475569; height: 100%; }
    .tldr-section { margin-bottom: 0.75rem; }
    .tldr-section-title { font-weight: 700; color: #1E293B; font-size: 0.85rem; }
    .tldr-item { margin-left: 0; color: #64748B; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_data():
    return pd.read_csv("data/emi_data.csv")

df = load_data()

# ============================================
# ISO CODES
# ============================================
ISO_CODES = {
    "Oman": "OMN", "UAE": "ARE", "Iceland": "ISL", "Argentina": "ARG",
    "Paraguay": "PRY", "Texas (US)": "USA", "Quebec (CA)": "CAN",
    "Brazil": "BRA", "Alberta (CA)": "CAN", "Russia": "RUS",
    "Norway": "NOR", "Ethiopia": "ETH", "Kazakhstan": "KAZ",
    "Finland": "FIN", "Kenya": "KEN", "DRC": "COD",
    "Chile": "CHL", "Sweden": "SWE", "Australia": "AUS"
}

# ============================================
# EXTENDED COUNTRY SUMMARIES
# ============================================
COUNTRY_SUMMARIES = {
    "Oman": """Oman leads the EMI ranking (0.75) with a highly favorable environment. The state actively supports mining through direct ownership of facilities in the Salalah Free Zone and Oman Vision 2040's diversification strategy. Free zones offer tax exemptions including 0% corporate tax and no import tariffs on ASICs. Grid connection timelines are favorable at 6-12 months with electricity costs of $38.5-$45.0/MWh. Permitting constraints are minimal with low environmental and zoning restrictions. Climate conditions are challenging with summer temperatures exceeding 35°C requiring adapted cooling infrastructure.""",
    
    "UAE": """UAE ranks second (0.71) with a highly favorable framework. Mining benefits from strong government support through VARA regulation and state-backed initiatives. Free zones (DMCC, ADGM) provide 0% corporate tax, 5% VAT only, and no tariffs on imports. Grid connection is achievable in 6-12 months with electricity at $42.5-$47.5/MWh. Construction permits secured in under 3 months with minimal zoning restrictions. Climate is challenging with summer temperatures exceeding 40°C and significant dust exposure requiring hydro or immersion cooling.""",
    
    "Iceland": """Iceland scores 0.60 with favorable conditions. Climate is highly favorable with temperatures of -8°C to 8°C and low diurnal variation (13°C). Electricity costs below $35.0/MWh from abundant hydro and geothermal. However, political opposition is growing with incoming zoning laws constraining new data centers. Grid connection lead times extend to 18-24 months. No electricity tax but 25% VAT on imports. No operating license required but competition from AI data centers intensifying given limited power expansion capacity.""",
    
    "Argentina": """Argentina scores 0.57 with moderately favorable conditions. No specific mining framework but operations are tolerated, particularly off-grid flare gas projects in Vaca Muerta. Off-grid electricity below $35.0/MWh, grid-connected at $47.5-55.0/MWh. Grid connection in 9-15 months. Neutral tax regime with ability to shift profit center abroad. 27% VAT on imports (refundable), 11% tariff. No operating license but mandatory AFIP registration. Construction permits in 6 months. Zoning restrictions vary by province.""",
    
    "Paraguay": """Paraguay scores 0.57, powered entirely by hydropower from Itaipu Dam. Electricity at $42.5-$55.0/MWh via 5-year PPAs with ANDE. Grid connection in 5-10 months. Slightly favorable legal framework but electricity tariff increases expected in 2026. 10% VAT (can be exempted), 4-10% tariffs. No license required but mandatory registration with authorities. Construction permits in 6-9 months. Emissions and noise restrictions significant. Climate neutral with summer temperatures reaching 35°C.""",
    
    "Texas (US)": """Texas scores 0.56 with favorable legal and fiscal frameworks. Deregulated ERCOT market with electricity at $35.0-$47.5/MWh. However, grid connection now takes 16-22 months due to AI competition. No electricity tax with available incentives. 10-30% tariffs on ASICs depending on origin and mitigation. No license required. Construction permits variable. Zoning moderately affects land availability; noise restrictions significant. Climate challenging with hot summers and wide diurnal spread (27°C).""",
    
    "Quebec (CA)": """Quebec scores 0.55 with neutral conditions. Hydro-Quebec provides electricity at $42.5-$47.5/MWh but historically halted crypto projects. Grid connection in 9-15 months. Electricity tax applies. 5% GST (refundable), 0% tariff. No license but mandatory reporting. Construction permits in 8 months. Zoning highly restricts land availability. Climate favorable despite cold winters (-28°C) and high humidity (83.5%). GST on electricity purchases can be claimed back.""",
    
    "Brazil": """Brazil scores 0.54 with improving conditions. Hashrate doubled YoY to 4.0 EH driven by wind and solar build-out. Electricity at $47.5-55.0/MWh on-grid, lower off-grid. Grid connection in 12 months. REDATA incentive exempts federal taxes for low-emission data centers. High VAT layers 30-35% (some exemptions). No license but mandatory registration. Construction permits in 3-6 months. EIA and water permits burdensome. Climate neutral with summer temperatures above 30°C.""",
    
    "Alberta (CA)": """Alberta scores 0.53 with neutral conditions. Deregulated market with direct producer contracts. Electricity at $42.5-$47.5/MWh. Grid connection exceeds 24 months. Carbon tax applies but no electricity tax. 5% GST (refundable), 2% tariff. Operating license required (3-6 months). Construction permits in 3-6 months. Zoning highly restricts land availability. Climate favorable but extreme cold in winter and high diurnal spread (28°C).""",
    
    "Russia": """Russia scores 0.51 with neutral environment transitioning from favorable. Electricity at $55.0-$65.0/MWh, up from median levels. Grid connection in 12 months. Since 2024, mining restricted to Russian entities with multiple regional bans. No electricity tax. 22% VAT, no tariff but FSB license required for ASIC imports. Operating license required (under 3 months). Construction permits 3-12 months. Climate favorable with 86% humidity.""",
    
    "Norway": """Norway scores 0.51 with neutral but deteriorating conditions. Leading Nordic hashrate at 16.0 EH. Electricity below $35.0/MWh but electricity tax at $14.7/MWh (up from $0.56 in 2022). Grid connection 18-24 months. Political opposition growing with incoming zoning restrictions. 25% VAT, no tariff, no license. Construction permits 3-6 months. Climate highly favorable with low temperatures and modest diurnal spread despite 86% humidity.""",
    
    "Ethiopia": """Ethiopia scores 0.51, shifting from favorable. Hashrate surged to 27.5 EH (+129% YoY) but new permits suspended since February 2024. Electricity historically at $22.0/MWh but tariff increases enacted through 2028 to $35.0-$42.5/MWh. Grid connection 6-12 months but new connections frozen. 15% VAT (not yet enforced), 3-15% tariff. License required (under 3 months when available). Climate favorable but altitude (~2,400m) affects ASIC performance.""",
    
    "Kazakhstan": """Kazakhstan scores 0.47 with neutral but improving framework. Post-crackdown regulatory stabilization. Electricity at $55.0-$65.0/MWh on-grid, reduced off-grid. Grid connection exceeds 24 months. Electricity tax at $4.0/MWh ($2.0 off-grid renewables). 16% VAT (increased from 12%), no tariff but license required. Operating license in 3-5 weeks. Construction permits 2-6 months. Climate slightly unfavorable with hot summers and pronounced diurnal variation.""",
    
    "Finland": """Finland scores 0.47 with restrictive framework. Electricity tax increased from €0.5 to €22.4/MWh in 2026 (miners with heat reuse exempted). Electricity at median rates. Grid connection 12-18 months. 25.5% VAT with VAT reclaim issues for miners. No license required. Construction permits 3-6 months. Climate highly favorable with low temperatures despite 85% humidity. Tax authorities reclaiming VAT on previous imports.""",
    
    "Kenya": """Kenya scores 0.47 with limited infrastructure. Off-grid installations offer below $35.0/MWh but scale limited. Grid connection 6-12 months. 16% VAT, 14% tariff. Operating license required. Climate favorable (13-28°C, 61% humidity) but altitude (~1,900m) requires careful ASIC management. Regulatory framework underdeveloped for large-scale operations.""",
    
    "DRC": """DRC scores 0.46 with significant challenges. Off-grid power below $35.0/MWh but infrastructure unreliable with only 51% electrification. Import process highly unfavorable with 15% tariff. Political instability a key concern. Climate favorable with stable temperatures (15-27°C) but humidity at 84% and altitude (~1,200m) require attention.""",
    
    "Chile": """Chile scores 0.44 with critical barriers. Grid connection exceeds 24 months. Electricity at $55.0-$65.0/MWh. Favorable tax regime with ability to shift profit abroad. No electricity tax. 19% VAT, 10% tariff. License required (6-9 months). Construction permits 6-9 months. EIA highly burdensome. Climate neutral in Atacama but dust and altitude present challenges.""",
    
    "Sweden": """Sweden scores 0.45, hostile to mining. Electricity tax at $39.9/MWh (up from $0.6/MWh in 2017). Electricity at $35.0-$42.5/MWh but tax erases advantage. Grid connection 12-18 months. 25% VAT with mining excluded from VAT reclaim. Ministry of Finance previously pushed for EU-wide ban. Climate highly favorable with low temperatures and modest diurnal spread (21°C).""",
    
    "Australia": """Australia scores 0.28, lowest in index. Stringent environmental regulations. Electricity at $55.0-$65.0/MWh. Grid connection 12-18 months. 30% corporate tax with no profit center shift allowed. 10% GST. Construction permits 9-12 months. Strict heat, noise, emissions thresholds. Zoning highly restrictive. PUE <1.4 and net-zero roadmap mandated for data centers."""
}

# ============================================
# TLDR DATA BY COUNTRY
# ============================================
COUNTRY_TLDR = {
    "Oman": {
        "Legal": "Highly favorable • Future: stable",
        "Fiscal": "0% corporate tax in free zones • No electricity tax • Low constraint to mitigate taxes",
        "Permits": "License required (>12 months) • Construction 6-9 months • Low EIA burden • Zoning: low impact",
        "Energy": "Grid connection 6-12 months • Power cost $38.5-$45.0/MWh • Moderate entry barriers",
        "Tariffs": "5% VAT • No tariff • No license required • Highly favorable import process",
        "Climate": "Summer >35°C • Low diurnal spread (15.6°C) • Dust exposure"
    },
    "UAE": {
        "Legal": "Highly favorable • Future: stable • State ownership of mining facilities",
        "Fiscal": "0% corporate in free zones • 5% VAT only • No electricity tax • Low tax constraints",
        "Permits": "License <3 months • Construction <3 months • Low EIA burden • Zoning: neutral",
        "Energy": "Grid connection 6-12 months • Power cost $42.5-$47.5/MWh • Moderate entry barriers",
        "Tariffs": "5% VAT • No tariff • License required • Favorable import process",
        "Climate": "Summer >40°C • Diurnal spread 19.1°C • 40% humidity • Significant dust"
    },
    "Iceland": {
        "Legal": "Neutral • Future: worsening • Political opposition growing • Zoning laws incoming",
        "Fiscal": "Neutral tax regime • Profit center shift allowed • No electricity tax • High constraints",
        "Permits": "No license required • Construction 3-6 months • Water permits restrictive • Zoning: high impact",
        "Energy": "Grid connection 18-24 months • Power cost <$35.0/MWh • Moderate entry barriers",
        "Tariffs": "25% VAT • No tariff • License required • Favorable import process",
        "Climate": "Highly favorable temps (-8°C to 8°C) • Low diurnal spread (13°C) • 85% humidity"
    },
    "Argentina": {
        "Legal": "Neutral • Future: improving • No specific framework but tolerated • Off-grid flare gas active",
        "Fiscal": "Neutral regime • Profit center shift allowed • No electricity tax • Moderate constraints",
        "Permits": "No license but AFIP registration • Construction 6 months • Low EIA • Zoning: variable",
        "Energy": "Grid connection 9-15 months • Off-grid <$35.0/MWh, Grid $47.5-55.0/MWh • High barriers",
        "Tariffs": "27% VAT (refundable) • 11% tariff • License required • Unfavorable process",
        "Climate": "Neutral • Summer >30°C • Wide diurnal spread • Hot summers in Vaca Muerta"
    },
    "Paraguay": {
        "Legal": "Slightly favorable • Future: neutral • Tariff increases expected • Registration mandatory",
        "Fiscal": "Favorable regime • Profit center shift allowed • Electricity tax expected to increase • Neutral constraints",
        "Permits": "No license but registration required • Construction 6-9 months • Neutral EIA • Emissions significant",
        "Energy": "Grid connection 5-10 months • Power cost $42.5-$55.0/MWh • Neutral barriers • 5-year PPAs",
        "Tariffs": "10% VAT (exemptable) • 4-10% tariff • No license • Marginally favorable process",
        "Climate": "Neutral • Summer ≥35°C • Diurnal spread 22.1°C • Humidity 38-84%"
    },
    "Texas (US)": {
        "Legal": "Favorable • Future: stable • Potential zoning pressure from AI data centers",
        "Fiscal": "Slightly favorable • Profit center shift allowed • No electricity tax • Incentives available",
        "Permits": "No license required • Construction variable • Moderate EIA • Zoning: moderate impact • Noise significant",
        "Energy": "Grid connection 16-22 months • Power cost $35.0-$47.5/MWh • High entry barriers (ERCOT)",
        "Tariffs": "No VAT • 10-30% tariff depending on origin • No license • Unfavorable process",
        "Climate": "Unfavorable • Hot summers • Wide diurnal spread (27°C) • 58% humidity"
    },
    "Quebec (CA)": {
        "Legal": "Neutral • Future: neutral • Hydro-Quebec strict oversight • Historical project halts",
        "Fiscal": "Unfavorable in Quebec • Profit center shift allowed • Electricity tax applies • GST reclaimable",
        "Permits": "No license but reporting mandatory • Construction 8 months • Moderate EIA • Zoning: high impact",
        "Energy": "Grid connection 9-15 months • Power cost $42.5-$47.5/MWh • High entry barriers",
        "Tariffs": "5% GST (refundable) • 0% tariff • No license • Slightly favorable process",
        "Climate": "Favorable • Cold winters (-28°C) • High diurnal spread (28°C) • 83.5% humidity"
    },
    "Brazil": {
        "Legal": "Slightly favorable • Future: mixed • REDATA incentive for low-emission data centers",
        "Fiscal": "Unfavorable regime • Profit center shift allowed • No electricity tax • High constraints",
        "Permits": "No license but registration • Construction 3-6 months • EIA burdensome • Zoning: low impact",
        "Energy": "Grid connection 12 months • Power cost $47.5-55.0/MWh • Neutral barriers • Behind-meter opportunity",
        "Tariffs": "30-35% VAT layers • Tariffs suspended • No license • Neutral process",
        "Climate": "Neutral • Summer >30°C • Low diurnal spread (18-31°C) • 76-87% humidity"
    },
    "Alberta (CA)": {
        "Legal": "Favorable • Future: stable • Deregulated market • Direct producer contracts available",
        "Fiscal": "Neutral • Profit center shift allowed • Carbon tax (no electricity tax) • Moderate constraints",
        "Permits": "License required (3-6 months) • Construction 3-6 months • Moderate EIA • Zoning: high impact",
        "Energy": "Grid connection >24 months • Power cost $42.5-$47.5/MWh • High entry barriers",
        "Tariffs": "5% GST (refundable) • 2% tariff • No license • Neutral process",
        "Climate": "Favorable • Extreme cold winters • High diurnal spread (28°C) • 83.5% humidity"
    },
    "Russia": {
        "Legal": "Favorable but worsening • Mining restricted to Russian entities since 2024 • Regional bans",
        "Fiscal": "Neutral regime • Cannot shift profit center • No electricity tax • High constraints",
        "Permits": "License <3 months • Construction 3-12 months • Neutral EIA • Zoning: neutral impact",
        "Energy": "Grid connection 12 months • Power cost $55.0-$65.0/MWh • Moderate barriers",
        "Tariffs": "22% VAT • No tariff • FSB license required for ASICs • Neutral process",
        "Climate": "Favorable • Modest temps • Diurnal spread moderate • 86% humidity"
    },
    "Norway": {
        "Legal": "Neutral • Future: worsening • Political opposition • Zoning restrictions incoming",
        "Fiscal": "Neutral regime • Profit center shift allowed • Electricity tax $14.7/MWh • High constraints",
        "Permits": "No license required • Construction 3-6 months • Water permits restrictive • Zoning: high impact",
        "Energy": "Grid connection 18-24 months • Power cost <$35.0/MWh • Moderate barriers",
        "Tariffs": "25% VAT • No tariff • License required • Favorable process",
        "Climate": "Highly favorable • Low temps (5-24°C) • Modest diurnal spread • 86% humidity"
    },
    "Ethiopia": {
        "Legal": "Slightly unfavorable • Future: worsening • New permits frozen since Feb 2024",
        "Fiscal": "Slightly unfavorable • Cannot shift profit center • Power rate hikes enacted through 2028",
        "Permits": "License <3 months (when available) • Construction 8 months • Low EIA • Zoning: neutral",
        "Energy": "Grid connection 6-12 months (frozen) • Power cost $35.0-$42.5/MWh (rising) • High barriers",
        "Tariffs": "15% VAT (not enforced) • 3-15% tariff • License required • Unfavorable process",
        "Climate": "Favorable temps • Low diurnal spread (17.3°C) • Altitude ~2,400m affects ASICs"
    },
    "Kazakhstan": {
        "Legal": "Slightly favorable • Future: improving • Post-crackdown stabilization",
        "Fiscal": "Favorable regime • Profit center shift allowed • Electricity tax $4.0/MWh • Moderate constraints",
        "Permits": "License 3-5 weeks • Construction 2-6 months • Low EIA • Zoning: neutral impact",
        "Energy": "Grid connection >24 months • Power cost $55.0-$65.0/MWh • High entry barriers",
        "Tariffs": "16% VAT • No tariff • License required • Neutral process",
        "Climate": "Slightly unfavorable • Hot summers • Pronounced diurnal variation"
    },
    "Finland": {
        "Legal": "Unfavorable • Future: unfavorable • Data center concerns driving policy",
        "Fiscal": "Unfavorable • Profit center shift allowed • Electricity tax €22.4/MWh (heat reuse exempt) • High constraints",
        "Permits": "No license required • Construction 3-6 months • Moderate EIA • Zoning: neutral impact",
        "Energy": "Grid connection 12-18 months • Power cost at median • Neutral barriers",
        "Tariffs": "25.5% VAT • No tariff • No license • Neutral process • VAT reclaim issues",
        "Climate": "Highly favorable • Low temps • Modest diurnal spread • 85% humidity"
    },
    "Kenya": {
        "Legal": "Neutral • Future: neutral • Framework underdeveloped for large-scale",
        "Fiscal": "Neutral regime • Profit center shift allowed • No electricity tax • Moderate constraints",
        "Permits": "License required • Construction 6-9 months • Moderate EIA • Zoning: neutral",
        "Energy": "Grid connection 6-12 months • Off-grid <$35.0/MWh • High barriers • Limited scale",
        "Tariffs": "16% VAT • 14% tariff • License required • Unfavorable process",
        "Climate": "Favorable (13-28°C) • Low diurnal spread (14.3°C) • 61% humidity • Altitude ~1,900m"
    },
    "DRC": {
        "Legal": "Neutral • Future: uncertain • Political instability • Only 51% electrification",
        "Fiscal": "Neutral regime • Profit center shift allowed • No electricity tax",
        "Permits": "License required • Construction 6+ months • Low EIA • Infrastructure unreliable",
        "Energy": "Grid connection uncertain • Off-grid <$35.0/MWh but limited scale • High barriers",
        "Tariffs": "15% tariff • Import process unfavorable • Customs delays weeks to months",
        "Climate": "Favorable temps (15-27°C) • Low diurnal spread • 84% humidity • Altitude ~1,200m"
    },
    "Chile": {
        "Legal": "Neutral • Future: neutral • No specific mining framework • Data center-friendly policies",
        "Fiscal": "Favorable regime • Profit center shift allowed • No electricity tax • Neutral constraints",
        "Permits": "License 6-9 months • Construction 6-9 months • EIA highly burdensome • Zoning: low impact",
        "Energy": "Grid connection >24 months • Power cost $55.0-$65.0/MWh • Moderate barriers • High curtailment",
        "Tariffs": "19% VAT • 10% tariff • No license • No mitigation impact",
        "Climate": "Neutral in Atacama • Mild temps but dust exposure • High altitude challenges"
    },
    "Sweden": {
        "Legal": "Unfavorable • Future: unfavorable • Ministry pushed for EU ban • Hostile environment",
        "Fiscal": "Highly unfavorable • Cannot shift profit center • Electricity tax $39.9/MWh • High constraints",
        "Permits": "No license required • Construction 3-6 months • Neutral EIA • Zoning: neutral impact",
        "Energy": "Grid connection 12-18 months • Power cost $35.0-$42.5/MWh • Neutral barriers",
        "Tariffs": "25% VAT • No tariff • No license • Mining excluded from VAT reclaim",
        "Climate": "Highly favorable • Low temps • Diurnal spread 21°C • 89% humidity"
    },
    "Australia": {
        "Legal": "Highly unfavorable • Future: unfavorable • Stringent environmental regulations",
        "Fiscal": "Unfavorable • 30% CIT • Cannot shift profit center • No incentives",
        "Permits": "License required • Construction 9-12 months • EIA strict • Zoning: highly restrictive",
        "Energy": "Grid connection 12-18 months • Power cost $55.0-$65.0/MWh • High barriers (NEM)",
        "Tariffs": "10% GST • Import process unfavorable",
        "Climate": "Unfavorable • High temps • PUE <1.4 mandated • Net-zero roadmap required"
    }
}

# ============================================
# LEGAL SECTION DATA FROM EXCEL (Q18 & Q19)
# ============================================
LEGAL_SCORES = {
    "UAE": {"Q18": 0.875, "Q19": 0.875},
    "Oman": {"Q18": 0.875, "Q19": 0.875},
    "Alberta (CA)": {"Q18": 0.75, "Q19": 0.85},
    "Texas (US)": {"Q18": 0.75, "Q19": 0.694},
    "Iceland": {"Q18": 0.75, "Q19": 0.75},
    "Russia": {"Q18": 0.667, "Q19": 0.333},
    "Argentina": {"Q18": 0.625, "Q19": 0.75},
    "Paraguay": {"Q18": 0.607, "Q19": 0.50},
    "Kazakhstan": {"Q18": 0.583, "Q19": 0.667},
    "Brazil": {"Q18": 0.583, "Q19": 0.50},
    "Quebec (CA)": {"Q18": 0.50, "Q19": 0.50},
    "DRC": {"Q18": 0.50, "Q19": 0.50},
    "Norway": {"Q18": 0.50, "Q19": 0.25},
    "Chile": {"Q18": 0.50, "Q19": 0.50},
    "Kenya": {"Q18": 0.50, "Q19": 0.50},
    "Ethiopia": {"Q18": 0.40, "Q19": 0.35},
    "Australia": {"Q18": 0.25, "Q19": 0.00},
    "Finland": {"Q18": 0.25, "Q19": 0.25},
    "Sweden": {"Q18": 0.25, "Q19": 0.25}
}

# ============================================
# FISCAL SECTION DATA FROM EXCEL
# ============================================
# Q1: Taxation environment (Row 8)
# Q2: Profit center shift abroad (Row 9)
# Q4: Electricity Tax (Row 11)
# Q5: Tax abatements, subsidies, incentives (Row 12)
# Q6: Constraint to avoid taxes or access subsidies (Row 13)
FISCAL_SCORES = {
    "Argentina": {"Q1_Taxation": 0.50, "Q2_Profit_Center": 0.75, "Q4_Electricity_Tax": 0.75, "Q5_Subsidies": 0.50, "Q6_Constraints": 0.33},
    "Quebec (CA)": {"Q1_Taxation": 0.38, "Q2_Profit_Center": 0.75, "Q4_Electricity_Tax": 0.75, "Q5_Subsidies": 0.50, "Q6_Constraints": 0.60},
    "Alberta (CA)": {"Q1_Taxation": 0.50, "Q2_Profit_Center": 0.75, "Q4_Electricity_Tax": 0.75, "Q5_Subsidies": 0.50, "Q6_Constraints": 0.30},
    "Brazil": {"Q1_Taxation": 0.33, "Q2_Profit_Center": 0.75, "Q4_Electricity_Tax": 0.75, "Q5_Subsidies": 0.75, "Q6_Constraints": 0.27},
    "Chile": {"Q1_Taxation": 0.75, "Q2_Profit_Center": 0.75, "Q4_Electricity_Tax": 0.75, "Q5_Subsidies": 0.50, "Q6_Constraints": 0.50},
    "Ethiopia": {"Q1_Taxation": 0.40, "Q2_Profit_Center": 0.43, "Q4_Electricity_Tax": 0.25, "Q5_Subsidies": 0.75, "Q6_Constraints": 0.47},
    "Finland": {"Q1_Taxation": 0.25, "Q2_Profit_Center": 0.75, "Q4_Electricity_Tax": 0.25, "Q5_Subsidies": 0.50, "Q6_Constraints": 0.15},
    "Iceland": {"Q1_Taxation": 0.58, "Q2_Profit_Center": 0.75, "Q4_Electricity_Tax": 0.75, "Q5_Subsidies": 0.50, "Q6_Constraints": 0.57},
    "Kazakhstan": {"Q1_Taxation": 0.67, "Q2_Profit_Center": 0.35, "Q4_Electricity_Tax": 0.30, "Q5_Subsidies": 0.50, "Q6_Constraints": 0.38},
    "Kenya": {"Q1_Taxation": 0.50, "Q2_Profit_Center": 0.35, "Q4_Electricity_Tax": 0.75, "Q5_Subsidies": 0.50, "Q6_Constraints": 0.50},
    "Norway": {"Q1_Taxation": 0.58, "Q2_Profit_Center": 0.75, "Q4_Electricity_Tax": 0.27, "Q5_Subsidies": 0.50, "Q6_Constraints": 0.27},
    "Oman": {"Q1_Taxation": 1.00, "Q2_Profit_Center": 0.75, "Q4_Electricity_Tax": 0.75, "Q5_Subsidies": 0.75, "Q6_Constraints": 0.70},
    "Paraguay": {"Q1_Taxation": 0.71, "Q2_Profit_Center": 0.75, "Q4_Electricity_Tax": 0.25, "Q5_Subsidies": 0.71, "Q6_Constraints": 0.43},
    "DRC": {"Q1_Taxation": 0.25, "Q2_Profit_Center": 0.75, "Q4_Electricity_Tax": 0.75, "Q5_Subsidies": 0.50, "Q6_Constraints": 0.15},
    "Russia": {"Q1_Taxation": 0.50, "Q2_Profit_Center": 0.35, "Q4_Electricity_Tax": 0.75, "Q5_Subsidies": 0.75, "Q6_Constraints": 0.15},
    "Sweden": {"Q1_Taxation": 0.00, "Q2_Profit_Center": 0.35, "Q4_Electricity_Tax": 0.15, "Q5_Subsidies": 0.50, "Q6_Constraints": 0.15},
    "UAE": {"Q1_Taxation": 1.00, "Q2_Profit_Center": 0.75, "Q4_Electricity_Tax": 0.75, "Q5_Subsidies": 0.75, "Q6_Constraints": 0.60},
    "Texas (US)": {"Q1_Taxation": 0.58, "Q2_Profit_Center": 0.75, "Q4_Electricity_Tax": 0.75, "Q5_Subsidies": 0.72, "Q6_Constraints": 0.36},
    "Australia": {"Q1_Taxation": 0.25, "Q2_Profit_Center": 0.75, "Q4_Electricity_Tax": 0.50, "Q5_Subsidies": 0.25, "Q6_Constraints": 0.25}
}

# ============================================
# PERMITS & LICENSES SECTION DATA FROM EXCEL
# ============================================
# Q10: Timeline to obtain operational license (Row 19)
# Q11: ASIC imports licensing requirements (Row 20)
# Q12: Timeline to secure construction permits (Row 21)
# Q13: EIA required before construction (Row 22)
# Q14: Water-use permits (Row 23)
# Q15: Regulations heat, noise, emissions (Row 24)
# Q16: Zoning restrictions land availability (Row 25)
PERMIT_SCORES = {
    "Argentina": {"Q10_Op_License": 0.70, "Q11_Import_License": 0.35, "Q12_Construction": 0.50, "Q13_EIA": 0.75, "Q14_Water": 0.15, "Q15_Emissions": 0.57, "Q16_Zoning": 0.90},
    "Quebec (CA)": {"Q10_Op_License": 0.70, "Q11_Import_License": 0.70, "Q12_Construction": 0.50, "Q13_EIA": 0.30, "Q14_Water": 0.50, "Q15_Emissions": 0.25, "Q16_Zoning": 0.22},
    "Alberta (CA)": {"Q10_Op_License": 0.35, "Q11_Import_License": 0.70, "Q12_Construction": 0.70, "Q13_EIA": 0.30, "Q14_Water": 0.30, "Q15_Emissions": 0.25, "Q16_Zoning": 0.15},
    "Brazil": {"Q10_Op_License": 0.70, "Q11_Import_License": 0.70, "Q12_Construction": 0.80, "Q13_EIA": 0.30, "Q14_Water": 0.30, "Q15_Emissions": 0.68, "Q16_Zoning": 0.70},
    "Chile": {"Q10_Op_License": 0.35, "Q11_Import_License": 0.70, "Q12_Construction": 0.30, "Q13_EIA": 0.15, "Q14_Water": 0.30, "Q15_Emissions": 0.55, "Q16_Zoning": 0.90},
    "Ethiopia": {"Q10_Op_License": 0.35, "Q11_Import_License": 0.35, "Q12_Construction": 0.24, "Q13_EIA": 0.95, "Q14_Water": 1.00, "Q15_Emissions": 0.78, "Q16_Zoning": 0.43},
    "Finland": {"Q10_Op_License": 0.70, "Q11_Import_License": 0.70, "Q12_Construction": 0.50, "Q13_EIA": 0.75, "Q14_Water": 0.40, "Q15_Emissions": 0.50, "Q16_Zoning": 0.50},
    "Iceland": {"Q10_Op_License": 0.70, "Q11_Import_License": 0.70, "Q12_Construction": 0.67, "Q13_EIA": 0.50, "Q14_Water": 0.67, "Q15_Emissions": 0.72, "Q16_Zoning": 0.40},
    "Kazakhstan": {"Q10_Op_License": 0.35, "Q11_Import_License": 0.35, "Q12_Construction": 0.90, "Q13_EIA": 0.75, "Q14_Water": 0.75, "Q15_Emissions": 0.57, "Q16_Zoning": 0.57},
    "Kenya": {"Q10_Op_License": 0.70, "Q11_Import_License": 0.70, "Q12_Construction": 0.70, "Q13_EIA": 0.30, "Q14_Water": 0.50, "Q15_Emissions": 0.55, "Q16_Zoning": 0.90},
    "Norway": {"Q10_Op_License": 0.70, "Q11_Import_License": 0.58, "Q12_Construction": 0.70, "Q13_EIA": 0.50, "Q14_Water": 0.55, "Q15_Emissions": 0.30, "Q16_Zoning": 0.20},
    "Oman": {"Q10_Op_License": 0.35, "Q11_Import_License": 0.70, "Q12_Construction": 0.85, "Q13_EIA": 0.95, "Q14_Water": 0.70, "Q15_Emissions": 0.90, "Q16_Zoning": 0.70},
    "Paraguay": {"Q10_Op_License": 0.70, "Q11_Import_License": 0.70, "Q12_Construction": 0.43, "Q13_EIA": 0.45, "Q14_Water": 0.50, "Q15_Emissions": 0.46, "Q16_Zoning": 0.61},
    "DRC": {"Q10_Op_License": 0.70, "Q11_Import_License": 0.35, "Q12_Construction": 0.70, "Q13_EIA": 1.00, "Q14_Water": 1.00, "Q15_Emissions": 1.00, "Q16_Zoning": 0.90},
    "Russia": {"Q10_Op_License": 0.35, "Q11_Import_License": 0.35, "Q12_Construction": 0.62, "Q13_EIA": 0.40, "Q14_Water": 0.53, "Q15_Emissions": 0.55, "Q16_Zoning": 0.50},
    "Sweden": {"Q10_Op_License": 0.70, "Q11_Import_License": 0.70, "Q12_Construction": 0.50, "Q13_EIA": 0.50, "Q14_Water": 0.55, "Q15_Emissions": 0.50, "Q16_Zoning": 0.50},
    "UAE": {"Q10_Op_License": 0.35, "Q11_Import_License": 0.61, "Q12_Construction": 0.67, "Q13_EIA": 0.71, "Q14_Water": 0.75, "Q15_Emissions": 0.81, "Q16_Zoning": 0.46},
    "Texas (US)": {"Q10_Op_License": 0.70, "Q11_Import_License": 0.70, "Q12_Construction": 0.64, "Q13_EIA": 0.42, "Q14_Water": 0.50, "Q15_Emissions": 0.36, "Q16_Zoning": 0.44},
    "Australia": {"Q10_Op_License": 0.35, "Q11_Import_License": 0.70, "Q12_Construction": 0.30, "Q13_EIA": 0.30, "Q14_Water": 0.30, "Q15_Emissions": 0.30, "Q16_Zoning": 0.30}
}

# ============================================
# ENERGY & GRID SECTION DATA FROM EXCEL
# ============================================
# Q22: Level of barriers to entry for accessing grid/energy (Row 33)
# Q23: Lead time grid connection (Row 34)
# Q24: Electricity Price (Row 35)
# Q25: Specific regulatory status for miners / Grid status (Row 36)
ENERGY_SCORES = {
    "Argentina": {"Q22_Barriers": 0.21, "Q23_Lead_Time": 0.62, "Q24_Elec_Price": 0.35, "Q25_Grid_Status": 0.50},
    "Quebec (CA)": {"Q22_Barriers": 0.21, "Q23_Lead_Time": 0.62, "Q24_Elec_Price": 0.55, "Q25_Grid_Status": 0.62},
    "Alberta (CA)": {"Q22_Barriers": 0.15, "Q23_Lead_Time": 0.00, "Q24_Elec_Price": 0.55, "Q25_Grid_Status": 0.50},
    "Brazil": {"Q22_Barriers": 0.67, "Q23_Lead_Time": 0.42, "Q24_Elec_Price": 0.50, "Q25_Grid_Status": 0.50},
    "Chile": {"Q22_Barriers": 0.00, "Q23_Lead_Time": 0.25, "Q24_Elec_Price": 0.50, "Q25_Grid_Status": 0.50},
    "Ethiopia": {"Q22_Barriers": 0.81, "Q23_Lead_Time": 0.71, "Q24_Elec_Price": 0.25, "Q25_Grid_Status": 0.50},
    "Finland": {"Q22_Barriers": 0.50, "Q23_Lead_Time": 0.35, "Q24_Elec_Price": 0.88, "Q25_Grid_Status": 0.50},
    "Iceland": {"Q22_Barriers": 0.58, "Q23_Lead_Time": 0.45, "Q24_Elec_Price": 0.50, "Q25_Grid_Status": 0.50},
    "Kazakhstan": {"Q22_Barriers": 0.19, "Q23_Lead_Time": 0.00, "Q24_Elec_Price": 0.28, "Q25_Grid_Status": 0.50},
    "Kenya": {"Q22_Barriers": 1.00, "Q23_Lead_Time": 1.00, "Q24_Elec_Price": 0.50, "Q25_Grid_Status": 0.50},
    "Norway": {"Q22_Barriers": 0.23, "Q23_Lead_Time": 0.25, "Q24_Elec_Price": 1.00, "Q25_Grid_Status": 0.50},
    "Oman": {"Q22_Barriers": 0.75, "Q23_Lead_Time": 0.65, "Q24_Elec_Price": 0.50, "Q25_Grid_Status": 0.50},
    "Paraguay": {"Q22_Barriers": 0.44, "Q23_Lead_Time": 0.82, "Q24_Elec_Price": 0.40, "Q25_Grid_Status": 0.50},
    "DRC": {"Q22_Barriers": 0.50, "Q23_Lead_Time": 1.00, "Q24_Elec_Price": 0.00, "Q25_Grid_Status": 0.50},
    "Russia": {"Q22_Barriers": 0.23, "Q23_Lead_Time": 0.62, "Q24_Elec_Price": 0.53, "Q25_Grid_Status": 0.25},
    "Sweden": {"Q22_Barriers": 0.50, "Q23_Lead_Time": 0.75, "Q24_Elec_Price": 0.50, "Q25_Grid_Status": 0.50},
    "UAE": {"Q22_Barriers": 0.83, "Q23_Lead_Time": 0.53, "Q24_Elec_Price": 0.62, "Q25_Grid_Status": 0.50},
    "Texas (US)": {"Q22_Barriers": 0.39, "Q23_Lead_Time": 0.69, "Q24_Elec_Price": 0.57, "Q25_Grid_Status": 0.50},
    "Australia": {"Q22_Barriers": 0.30, "Q23_Lead_Time": 0.30, "Q24_Elec_Price": 0.30, "Q25_Grid_Status": 0.30}
}

# ============================================
# HELPER FUNCTIONS
# ============================================
def get_score_color(score, min_score, max_score):
    if max_score == min_score:
        ratio = 0.5
    else:
        ratio = (score - min_score) / (max_score - min_score)
    ratio = max(0.0, min(1.0, ratio))
    
    color_stops = [
        (0.00, '#922B21'), (0.07, '#C0392B'), (0.14, '#CD6155'),
        (0.21, '#DC7633'), (0.28, '#E67E22'), (0.35, '#EB984E'),
        (0.42, '#F5B041'), (0.50, '#F4D03F'), (0.57, '#F7DC6F'),
        (0.64, '#A9DFBF'), (0.71, '#7DCEA0'), (0.78, '#52BE80'),
        (0.85, '#28B463'), (0.92, '#239B56'), (1.00, '#1E8449')
    ]
    
    for i in range(len(color_stops) - 1):
        if color_stops[i][0] <= ratio <= color_stops[i + 1][0]:
            t = (ratio - color_stops[i][0]) / (color_stops[i + 1][0] - color_stops[i][0])
            c1, c2 = color_stops[i][1], color_stops[i + 1][1]
            r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
            r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
            r, g, b = int(r1 + (r2 - r1) * t), int(g1 + (g2 - g1) * t), int(b1 + (b2 - b1) * t)
            return f'#{r:02x}{g:02x}{b:02x}'
    return '#F4D03F'

def get_text_color_for_score(score):
    return "black" if 0.37 <= score <= 0.64 else "white"

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("### Navigation")
    
    # Initialize session state for page
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Overview"
    
    current = st.session_state.current_page
    emi_categories = ["Legal", "Fiscal", "Permits & Licenses", "Energy & Grid", "Customs & Tariffs"]
    
    # Overview with home icon (extra space after icon)
    if st.button("⌂  Overview", key="btn_overview", use_container_width=True):
        st.session_state.current_page = "Overview"
        st.rerun()
    
    # Jurisdiction with globe icon (extra space after icon)
    if st.button("◎  Jurisdiction", key="btn_jurisdiction", use_container_width=True):
        st.session_state.current_page = "Jurisdiction"
        st.rerun()
    
    # Category expander (extra space after icon)
    with st.expander("◷  Category", expanded=True):
        for cat in emi_categories:
            if st.button(f"    {cat}", key=f"btn_{cat.lower().replace(' ', '_').replace('&', 'and')}", use_container_width=True):
                st.session_state.current_page = cat
                st.rerun()
    
    # Methodology with chart icon (extra space after icon)
    if st.button("▥  Methodology", key="btn_methodology", use_container_width=True):
        st.session_state.current_page = "Methodology"
        st.rerun()
    
    page = st.session_state.current_page
    
    st.markdown("---")
    st.markdown("**Ease to Mine Index (EMI)**")
    st.markdown("March 2026")
    st.markdown("")
    st.markdown("""<p class="sidebar-author">A report by <strong>Valentin Rousseau</strong><br>
    <a href="https://x.com/MuadDib_Pill" target="_blank">@MuadDib_Pill</a><br><br>
    Provided by <a href="https://www.e2cpartners.com/insights/global-bitcoin-mining-report-the-ease-to-mine-index" target="_blank">E2C Partners</a></p>""", unsafe_allow_html=True)

score_map = {
    "Overall Index": "Index_Score", "Fiscal": "Fiscal", "Permits & Licensing": "Permit_Licensing",
    "Legal": "Legal", "Energy & Grid": "Energy_Grid", "Customs & Tariffs": "Tariff_Import", "Operating Conditions": "Operating_Conditions"
}

# ============================================
# OVERVIEW PAGE
# ============================================
if page == "Overview":
    st.markdown("# Ease to Mine Index Dashboard")
    st.markdown('<p class="subtitle-text">Comprehensive analysis of Bitcoin mining regulatory and operating conditions across 19 jurisdictions</p>', unsafe_allow_html=True)
    
    col_filter, _ = st.columns([1, 3])
    with col_filter:
        score_type = st.selectbox("Select category", list(score_map.keys()), key="score_filter_main")
    
    selected_col = score_map[score_type]
    df_sorted = df.sort_values(selected_col, ascending=False)
    
    # Map (full width)
    st.markdown('<p class="section-title">Ease to Mine Index Map</p>', unsafe_allow_html=True)
    df_map = df.copy()
    df_map["ISO"] = df_map["Country"].map(ISO_CODES)
    df_map_agg = df_map.groupby("ISO").agg({selected_col: "mean", "Country": lambda x: ", ".join(x) if len(x) > 1 else x.iloc[0]}).reset_index()
    df_map_agg.columns = ["ISO", "Score", "Country"]
    
    fig_map = go.Figure(go.Choropleth(
        locations=df_map_agg["ISO"], z=df_map_agg["Score"], text=df_map_agg["Country"],
        colorscale=COLOR_SCALE, autocolorscale=False, marker_line_color='#4B5563', marker_line_width=1,
        colorbar=dict(title=dict(text="Score", side="right", font=dict(family="Barlow", size=11)), tickfont=dict(family="Barlow", size=10), len=0.8, thickness=12),
        hovertemplate="<b>%{text}</b><br>Score: %{z:.2f}<extra></extra>"))
    fig_map.update_layout(height=520, margin=dict(l=0, r=0, t=5, b=0),
        geo=dict(showframe=False, showcoastlines=True, coastlinecolor="#94A3B8", showland=True, landcolor="#E2E8F0",
            showocean=True, oceancolor="#FFFFFF", showcountries=True, countrycolor="#94A3B8", projection_type='natural earth', bgcolor='rgba(0,0,0,0)'),
        paper_bgcolor='rgba(0,0,0,0)', font=dict(family="Barlow"))
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Top 3 and Bottom 3 below the map
    min_s, max_s = df[selected_col].min(), df[selected_col].max()
    
    col_top3, col_bottom3 = st.columns(2)
    
    with col_top3:
        st.markdown('<p class="section-title-small">Top 3 Jurisdictions</p>', unsafe_allow_html=True)
        for idx, (i, row) in enumerate(df_sorted.head(3).iterrows()):
            rank, score = idx + 1, row[selected_col]
            color = get_score_color(score, min_s, max_s)
            st.markdown(f"""<div style="background: linear-gradient(90deg, {color}22 0%, transparent 100%); border-left: 4px solid {color}; padding: 10px 12px; margin-bottom: 8px; border-radius: 0 8px 8px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div><span style="font-weight: 700; color: #1E293B; font-size: 0.9rem;">#{rank} {row['Country']}</span><span style="color: #64748B; font-size: 0.9rem; margin-left: 6px;">{row['Region']}</span></div>
                    <div style="font-weight: 700; font-size: 1rem; color: {color};">{score:.2f}</div>
                </div>
                <div style="font-size: 0.7rem; color: #64748B; margin-top: 2px;">Hashrate Q1-26: {row['Hashrate_Q1_26']:.1f} EH/s</div>
            </div>""", unsafe_allow_html=True)
    
    with col_bottom3:
        st.markdown('<p class="section-title-small">Bottom 3 Jurisdictions</p>', unsafe_allow_html=True)
        for idx, (i, row) in enumerate(df_sorted.tail(3).iterrows()):
            rank, score = 17 + idx, row[selected_col]
            color = get_score_color(score, min_s, max_s)
            st.markdown(f"""<div style="background: linear-gradient(90deg, {color}22 0%, transparent 100%); border-left: 4px solid {color}; padding: 10px 12px; margin-bottom: 8px; border-radius: 0 8px 8px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div><span style="font-weight: 700; color: #1E293B; font-size: 0.9rem;">#{rank} {row['Country']}</span><span style="color: #64748B; font-size: 0.9rem; margin-left: 6px;">{row['Region']}</span></div>
                    <div style="font-weight: 700; font-size: 1rem; color: {color};">{score:.2f}</div>
                </div>
                <div style="font-size: 0.7rem; color: #64748B; margin-top: 2px;">Hashrate Q1-26: {row['Hashrate_Q1_26']:.1f} EH/s</div>
            </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # EMI Ranking
    st.markdown('<p class="section-title">EMI Ranking</p>', unsafe_allow_html=True)
    col_rf, _ = st.columns([1, 3])
    with col_rf:
        rank_dim = st.selectbox("Select category", list(score_map.keys()), key="rank_filter")
    
    rank_col = score_map[rank_dim]
    df_rank = df.sort_values(rank_col, ascending=True).copy()
    min_r, max_r = df_rank[rank_col].min(), df_rank[rank_col].max()
    colors_r = [get_score_color(s, min_r, max_r) for s in df_rank[rank_col]]
    
    col_chart, col_text = st.columns([2, 1])
    with col_chart:
        fig_rank = go.Figure(go.Bar(x=df_rank[rank_col], y=df_rank["Country"], orientation='h', marker_color=colors_r,
            text=df_rank[rank_col].round(2), textposition='outside', textfont=dict(size=13, family="Barlow")))
        fig_rank.update_layout(height=560, margin=dict(l=0, r=60, t=10, b=40),
            xaxis=dict(range=[0, 1], title=dict(text=rank_dim + " Score", font=dict(family="Barlow", size=12)), gridcolor='#E2E8F0', zeroline=False),
            yaxis=dict(title="", tickfont=dict(family="Barlow", size=13)), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(family="Barlow"))
        st.plotly_chart(fig_rank, use_container_width=True)
    
    with col_text:
        st.markdown("""<div class="info-box">
            <div class="info-box-title" style="font-size: 1.1rem; margin-bottom: 0.75rem;">EMI Description</div>
            <p>The first edition of the <strong>Ease to Mine Index (EMI)</strong> is a composite framework designed to assess the overall attractiveness of jurisdictions for Bitcoin mining.</p>
            <p style="margin-top: 0.75rem;">The index evaluates a broad set of dimensions:</p>
            <ul style="margin: 0.5rem 0; padding-left: 1.2rem;"><li>Legal and fiscal frameworks</li><li>Permitting and licensing conditions</li><li>Energy market structure and grid access</li><li>Climate characteristics</li><li>Tariff and import environments</li></ul>
            <p style="margin-top: 0.75rem;"><strong>Coverage:</strong> 18 countries spanning established and emerging mining regions — 19 jurisdictions (where Texas serves as a proxy of U.S., and Alberta and Québec for Canada).</p>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Heatmap
    st.markdown('<p class="section-title">Score Heatmap by Section</p>', unsafe_allow_html=True)
    heatmap_cols = ["Fiscal", "Permit_Licensing", "Legal", "Energy_Grid", "Tariff_Import", "Operating_Conditions"]
    heatmap_labels = ["Fiscal", "Permits", "Legal", "Energy", "Tariffs", "Climate"]
    df_heat = df.sort_values("Index_Score", ascending=False)
    heatmap_data = df_heat.set_index("Country")[heatmap_cols]
    heatmap_data.columns = heatmap_labels
    
    fig_heat = go.Figure(go.Heatmap(z=heatmap_data.values, x=heatmap_labels, y=heatmap_data.index, colorscale=COLOR_SCALE,
        hovertemplate="Country: %{y}<br>Section: %{x}<br>Score: %{z:.2f}<extra></extra>", showscale=True,
        colorbar=dict(title=dict(text="Score", side="right", font=dict(family="Barlow")), tickfont=dict(family="Barlow"))))
    annotations = [dict(x=heatmap_labels[j], y=heatmap_data.index[i], text=f"{heatmap_data.iloc[i, j]:.2f}", showarrow=False,
        font=dict(color=get_text_color_for_score(heatmap_data.iloc[i, j]), size=12, family="Barlow"))
        for i in range(len(heatmap_data.index)) for j in range(len(heatmap_labels))]
    fig_heat.update_layout(annotations=annotations, height=550, margin=dict(l=0, r=0, t=10, b=40),
        xaxis=dict(title="", tickangle=0, side="bottom", tickfont=dict(family="Barlow", size=13)),
        yaxis=dict(title="", autorange="reversed", tickfont=dict(family="Barlow", size=13)),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(family="Barlow"))
    st.plotly_chart(fig_heat, use_container_width=True)
    
    st.markdown("---")
    
    # Data Table
    st.markdown('<p class="section-title">Full Data Table</p>', unsafe_allow_html=True)
    df_display = df.copy()
    df_display = df_display.rename(columns={"Index_Score": "EMI Score", "Permit_Licensing": "Permits", "Energy_Grid": "Energy", "Tariff_Import": "Tariffs", "Operating_Conditions": "Climate", "Hashrate_Q1_25": "Hashrate Q1-25 (EH/s)", "Hashrate_Q1_26": "Hashrate Q1-26 (EH/s)"})
    for col in ["EMI Score", "Fiscal", "Permits", "Legal", "Energy", "Tariffs", "Climate"]:
        df_display[col] = df_display[col].round(2)
    df_display = df_display.sort_values("EMI Score", ascending=False)
    display_cols = ["Country", "Region", "EMI Score", "Fiscal", "Permits", "Legal", "Energy", "Tariffs", "Climate", "Hashrate Q1-25 (EH/s)", "Hashrate Q1-26 (EH/s)"]
    st.dataframe(df_display[display_cols], use_container_width=True, hide_index=True, height=550,
        column_config={"EMI Score": st.column_config.ProgressColumn("EMI Score", format="%.2f", min_value=0, max_value=1)})
    csv = df_display[display_cols].to_csv(index=False)
    st.download_button(label="Download Data (CSV)", data=csv, file_name="emi_data_export.csv", mime="text/csv")

# ============================================
# JURISDICTION PAGE
# ============================================
elif page == "Jurisdiction":
    st.markdown("# Jurisdiction Analysis")
    st.markdown('<p class="subtitle-text">Detailed breakdown by jurisdiction</p>', unsafe_allow_html=True)
    
    col_country, _ = st.columns([1, 2])
    with col_country:
        selected_country = st.selectbox("Select jurisdiction", df["Country"].tolist(), key="country_select")
    
    country_data = df[df["Country"] == selected_country].iloc[0]
    
    st.markdown("---")
    st.markdown('<p class="section-title">Score Overview</p>', unsafe_allow_html=True)
    
    cols = st.columns(7)
    dimensions = [("Overall", "Index_Score"), ("Fiscal", "Fiscal"), ("Permits", "Permit_Licensing"), 
                  ("Legal", "Legal"), ("Energy", "Energy_Grid"), ("Tariffs", "Tariff_Import"), ("Climate", "Operating_Conditions")]
    
    for col, (label, col_name) in zip(cols, dimensions):
        score = country_data[col_name]
        color = get_score_color(score, df[col_name].min(), df[col_name].max())
        rank = df[col_name].rank(ascending=False)[df["Country"] == selected_country].values[0]
        with col:
            st.markdown(f"""<div style="text-align: center; padding: 1rem; background: {color}15; border-radius: 8px; border-left: 4px solid {color};">
                <div style="font-size: 1.8rem; font-weight: 700; color: {color};">{score:.2f}</div>
                <div style="font-size: 0.8rem; font-weight: 600; color: #1E293B;">{label}</div>
                <div style="font-size: 0.7rem; color: #64748B;">Rank #{int(rank)}/19</div>
            </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col_radar, col_summary = st.columns([1, 1])
    
    with col_radar:
        st.markdown('<p class="section-title">Dimension Profile</p>', unsafe_allow_html=True)
        categories = ['Fiscal', 'Permits', 'Legal', 'Energy', 'Tariffs', 'Climate']
        values = [country_data["Fiscal"], country_data["Permit_Licensing"], country_data["Legal"], 
                  country_data["Energy_Grid"], country_data["Tariff_Import"], country_data["Operating_Conditions"]]
        
        fig_radar = go.Figure(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself',
            fillcolor='rgba(13, 111, 255, 0.2)', line=dict(color='#0D6FFF', width=2), name=selected_country))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1], tickfont=dict(size=10), gridcolor='#E2E8F0'),
            angularaxis=dict(tickfont=dict(size=12, family="Barlow"))), showlegend=False, height=350, margin=dict(l=60, r=60, t=30, b=30),
            paper_bgcolor='rgba(0,0,0,0)', font=dict(family="Barlow"))
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col_summary:
        st.markdown('<p class="section-title">Jurisdiction Summary</p>', unsafe_allow_html=True)
        summary = COUNTRY_SUMMARIES.get(selected_country, "Detailed analysis available in the full report.")
        st.markdown(f"""<div class="info-box" style="height: 350px; overflow-y: auto;"><p style="font-size: 0.85rem;">{summary}</p>
            <p style="margin-top: 1rem;"><strong>Hashrate Q1-26:</strong> {country_data['Hashrate_Q1_26']:.1f} EH/s</p>
            <p><strong>Region:</strong> {country_data['Region']}</p>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Comparison
    st.markdown('<p class="section-title">Jurisdiction Comparison</p>', unsafe_allow_html=True)
    
    col_c1, col_vs, col_c2 = st.columns([2, 1, 2])
    with col_c1:
        country1 = st.selectbox("Jurisdiction 1", df["Country"].tolist(), index=0, key="compare1")
    with col_vs:
        st.markdown('<div class="comparison-vs">VS</div>', unsafe_allow_html=True)
    with col_c2:
        country2 = st.selectbox("Jurisdiction 2", df["Country"].tolist(), index=1, key="compare2")
    
    c1_data, c2_data = df[df["Country"] == country1].iloc[0], df[df["Country"] == country2].iloc[0]
    
    compare_dims = ["Index_Score", "Fiscal", "Permit_Licensing", "Legal", "Energy_Grid", "Tariff_Import", "Operating_Conditions"]
    compare_labels = ["Overall", "Fiscal", "Permits", "Legal", "Energy", "Tariffs", "Climate"]
    
    fig_compare = go.Figure()
    fig_compare.add_trace(go.Bar(name=country1, x=compare_labels, y=[c1_data[d] for d in compare_dims], marker_color='#6287F0'))
    fig_compare.add_trace(go.Bar(name=country2, x=compare_labels, y=[c2_data[d] for d in compare_dims], marker_color='#1D0DED'))
    fig_compare.update_layout(barmode='group', height=350, margin=dict(l=0, r=0, t=30, b=40),
        yaxis=dict(range=[0, 1], title="Score", gridcolor='#E2E8F0'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(family="Barlow"))
    st.plotly_chart(fig_compare, use_container_width=True)
    
    # TLDR Comparison boxes
    st.markdown("")
    tldr1 = COUNTRY_TLDR.get(country1, {})
    tldr2 = COUNTRY_TLDR.get(country2, {})
    
    col_tldr1, col_tldr2 = st.columns(2)
    
    with col_tldr1:
        st.markdown(f"""<div class="tldr-box">
            <div style="font-weight: 700; color: #1E293B; font-size: 1rem; margin-bottom: 0.75rem; border-bottom: 2px solid #6287F0; padding-bottom: 0.5rem;">{country1}</div>
            <div class="tldr-section"><span class="tldr-section-title">Legal:</span> <span class="tldr-item">{tldr1.get('Legal', 'N/A')}</span></div>
            <div class="tldr-section"><span class="tldr-section-title">Fiscal:</span> <span class="tldr-item">{tldr1.get('Fiscal', 'N/A')}</span></div>
            <div class="tldr-section"><span class="tldr-section-title">Permits:</span> <span class="tldr-item">{tldr1.get('Permits', 'N/A')}</span></div>
            <div class="tldr-section"><span class="tldr-section-title">Energy:</span> <span class="tldr-item">{tldr1.get('Energy', 'N/A')}</span></div>
            <div class="tldr-section"><span class="tldr-section-title">Tariffs:</span> <span class="tldr-item">{tldr1.get('Tariffs', 'N/A')}</span></div>
            <div class="tldr-section"><span class="tldr-section-title">Climate:</span> <span class="tldr-item">{tldr1.get('Climate', 'N/A')}</span></div>
        </div>""", unsafe_allow_html=True)
    
    with col_tldr2:
        st.markdown(f"""<div class="tldr-box">
            <div style="font-weight: 700; color: #1E293B; font-size: 1rem; margin-bottom: 0.75rem; border-bottom: 2px solid #1D0DED; padding-bottom: 0.5rem;">{country2}</div>
            <div class="tldr-section"><span class="tldr-section-title">Legal:</span> <span class="tldr-item">{tldr2.get('Legal', 'N/A')}</span></div>
            <div class="tldr-section"><span class="tldr-section-title">Fiscal:</span> <span class="tldr-item">{tldr2.get('Fiscal', 'N/A')}</span></div>
            <div class="tldr-section"><span class="tldr-section-title">Permits:</span> <span class="tldr-item">{tldr2.get('Permits', 'N/A')}</span></div>
            <div class="tldr-section"><span class="tldr-section-title">Energy:</span> <span class="tldr-item">{tldr2.get('Energy', 'N/A')}</span></div>
            <div class="tldr-section"><span class="tldr-section-title">Tariffs:</span> <span class="tldr-item">{tldr2.get('Tariffs', 'N/A')}</span></div>
            <div class="tldr-section"><span class="tldr-section-title">Climate:</span> <span class="tldr-item">{tldr2.get('Climate', 'N/A')}</span></div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("")
    
    # Data table
    comp_df = pd.DataFrame({
        "Dimension": compare_labels,
        country1: [f"{c1_data[d]:.2f}" for d in compare_dims],
        country2: [f"{c2_data[d]:.2f}" for d in compare_dims],
        "Difference": [f"{c1_data[d] - c2_data[d]:+.2f}" for d in compare_dims]
    })
    st.dataframe(comp_df, use_container_width=True, hide_index=True)

# ============================================
# LEGAL PAGE
# ============================================
elif page == "Legal":
    st.markdown("# Legal Framework Analysis")
    st.markdown('<p class="subtitle-text">Regulatory environment assessment based on survey responses</p>', unsafe_allow_html=True)
    
    # Create Legal DataFrame
    legal_data = []
    for country, scores in LEGAL_SCORES.items():
        q18 = scores["Q18"]
        q19 = scores["Q19"]
        evolution = q19 - q18
        legal_data.append({
            "Country": country,
            "Q18_Current": q18,
            "Q19_Future": q19,
            "Evolution": evolution
        })
    df_legal = pd.DataFrame(legal_data)
    df_legal = df_legal.merge(df[["Country", "Region"]], on="Country", how="left")
    df_legal["ISO"] = df_legal["Country"].map(ISO_CODES)
    
    # Filter selection
    col_filter, _ = st.columns([1, 3])
    with col_filter:
        legal_view = st.selectbox(
            "Select metric",
            ["Current legal framework", "Expected regulatory outlook"],
            key="legal_filter"
        )
    
    selected_legal_col = "Q18_Current" if "Current" in legal_view else "Q19_Future"
    
    # Map
    st.markdown('<p class="section-title">Regulatory Environment Map</p>', unsafe_allow_html=True)
    
    df_legal_agg = df_legal.groupby("ISO").agg({
        selected_legal_col: "mean",
        "Country": lambda x: ", ".join(x) if len(x) > 1 else x.iloc[0]
    }).reset_index()
    df_legal_agg.columns = ["ISO", "Score", "Country"]
    
    fig_legal_map = go.Figure(go.Choropleth(
        locations=df_legal_agg["ISO"],
        z=df_legal_agg["Score"],
        text=df_legal_agg["Country"],
        colorscale=COLOR_SCALE,
        autocolorscale=False,
        marker_line_color='#4B5563',
        marker_line_width=1,
        colorbar=dict(
            title=dict(text="Score", side="right", font=dict(family="Barlow", size=11)),
            tickfont=dict(family="Barlow", size=10),
            len=0.8,
            thickness=12
        ),
        hovertemplate="<b>%{text}</b><br>Score: %{z:.2f}<extra></extra>"
    ))
    fig_legal_map.update_layout(
        height=450,
        margin=dict(l=0, r=0, t=5, b=0),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="#94A3B8",
            showland=True,
            landcolor="#E2E8F0",
            showocean=True,
            oceancolor="#FFFFFF",
            showcountries=True,
            countrycolor="#94A3B8",
            projection_type='natural earth',
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Barlow")
    )
    st.plotly_chart(fig_legal_map, use_container_width=True)
    
    # Score interpretation legend
    st.markdown("""
    <div style="display: flex; justify-content: center; gap: 2rem; margin: 1rem 0; font-size: 0.85rem;">
        <span><strong style="color: #1E8449;">●</strong> Highly Favorable (≥0.75)</span>
        <span><strong style="color: #28B463;">●</strong> Favorable (0.60-0.74)</span>
        <span><strong style="color: #F4D03F;">●</strong> Neutral (0.40-0.59)</span>
        <span><strong style="color: #E67E22;">●</strong> Unfavorable (0.25-0.39)</span>
        <span><strong style="color: #922B21;">●</strong> Highly Unfavorable (<0.25)</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Regulatory Evolution Chart with Filter
    st.markdown('<p class="section-title">Regulatory Evolution</p>', unsafe_allow_html=True)
    
    # Calculate categories
    improving = df_legal[df_legal["Evolution"] > 0.001].copy()
    worsening = df_legal[df_legal["Evolution"] < -0.001].copy()
    stable = df_legal[(df_legal["Evolution"] >= -0.001) & (df_legal["Evolution"] <= 0.001)].copy()
    
    col_evo_filter, _ = st.columns([1, 3])
    with col_evo_filter:
        evolution_filter = st.selectbox(
            "Select outlook",
            ["All", "Improving Outlook", "Stable Outlook", "Worsening Outlook"],
            key="evolution_filter"
        )
    
    # Filter data based on selection
    if evolution_filter == "Improving Outlook":
        df_evo_filtered = improving.sort_values("Evolution", ascending=False)
        bar_color = '#1E8449'
        chart_title = "Jurisdictions with Improving Regulatory Outlook"
    elif evolution_filter == "Worsening Outlook":
        df_evo_filtered = worsening.sort_values("Evolution", ascending=True)
        bar_color = '#922B21'
        chart_title = "Jurisdictions with Worsening Regulatory Outlook"
    elif evolution_filter == "Stable Outlook":
        df_evo_filtered = stable.sort_values("Q18_Current", ascending=False)
        bar_color = '#64748B'
        chart_title = "Jurisdictions with Stable Regulatory Outlook"
    else:
        df_evo_filtered = df_legal.sort_values("Evolution", ascending=False)
        bar_color = None
        chart_title = "All Jurisdictions - Regulatory Evolution"
    
    if len(df_evo_filtered) > 0:
        # Create bar chart showing only evolution values
        if evolution_filter == "All":
            # Color bars based on evolution direction
            colors = []
            for evo in df_evo_filtered["Evolution"]:
                if evo > 0.001:
                    colors.append('#1E8449')
                elif evo < -0.001:
                    colors.append('#922B21')
                else:
                    colors.append('#64748B')
        else:
            colors = bar_color
        
        fig_evo = go.Figure(go.Bar(
            x=df_evo_filtered["Country"],
            y=df_evo_filtered["Evolution"],
            marker_color=colors,
            text=df_evo_filtered["Evolution"].apply(lambda x: f"{x:+.3f}"),
            textposition='outside',
            textfont=dict(size=11, family="Barlow")
        ))
        
        # Calculate y-axis range
        if evolution_filter == "Stable Outlook":
            y_range = [-0.05, 0.05]
        else:
            max_abs = max(abs(df_evo_filtered["Evolution"].min()), abs(df_evo_filtered["Evolution"].max()), 0.1)
            y_range = [-max_abs - 0.05, max_abs + 0.08]
        
        fig_evo.update_layout(
            height=450,
            margin=dict(l=0, r=0, t=40, b=100),
            title=dict(
                text=chart_title,
                font=dict(family="Barlow", size=14, color="#1E293B"),
                x=0.5,
                xanchor="center"
            ),
            xaxis=dict(
                title="",
                tickangle=-45,
                tickfont=dict(family="Barlow", size=11)
            ),
            yaxis=dict(
                range=y_range,
                title="Evolution",
                gridcolor='#E2E8F0',
                tickfont=dict(family="Barlow", size=11),
                zeroline=True,
                zerolinecolor='#1E293B',
                zerolinewidth=2
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Barlow")
        )
        st.plotly_chart(fig_evo, use_container_width=True)
    else:
        st.info("No jurisdictions in this category.")
    
    st.markdown("---")
    
    # Data table
    st.markdown('<p class="section-title">Legal Framework Data</p>', unsafe_allow_html=True)
    
    df_legal_display = df_legal[["Country", "Region", "Q18_Current", "Q19_Future", "Evolution"]].copy()
    df_legal_display = df_legal_display.rename(columns={
        "Q18_Current": "Current Legal Framework",
        "Q19_Future": "Expected Regulatory Outlook"
    })
    df_legal_display = df_legal_display.sort_values("Current Legal Framework", ascending=False)
    
    st.dataframe(
        df_legal_display,
        use_container_width=True,
        hide_index=True,
        height=500,
        column_config={
            "Current Legal Framework": st.column_config.ProgressColumn(
                "Current Legal Framework",
                format="%.2f",
                min_value=0,
                max_value=1
            ),
            "Expected Regulatory Outlook": st.column_config.ProgressColumn(
                "Expected Regulatory Outlook",
                format="%.2f",
                min_value=0,
                max_value=1
            ),
            "Evolution": st.column_config.NumberColumn(
                "Evolution",
                format="%+.2f"
            )
        }
    )

# ============================================
# FISCAL PAGE
# ============================================
elif page == "Fiscal":
    st.markdown("# Fiscal Framework Analysis")
    st.markdown('<p class="subtitle-text">Taxation environment and fiscal incentives assessment</p>', unsafe_allow_html=True)
    
    # Create Fiscal DataFrame
    fiscal_data = []
    for country, scores in FISCAL_SCORES.items():
        fiscal_data.append({
            "Country": country,
            "Q1_Taxation": scores["Q1_Taxation"],
            "Q2_Profit_Center": scores["Q2_Profit_Center"],
            "Q4_Electricity_Tax": scores["Q4_Electricity_Tax"],
            "Q5_Subsidies": scores["Q5_Subsidies"],
            "Q6_Constraints": scores["Q6_Constraints"]
        })
    df_fiscal = pd.DataFrame(fiscal_data)
    df_fiscal = df_fiscal.merge(df[["Country", "Region"]], on="Country", how="left")
    df_fiscal["ISO"] = df_fiscal["Country"].map(ISO_CODES)
    
    # =====================
    # SECTION 1: Scatter plot - Taxation Environment vs Constraints
    # =====================
    st.markdown('<p class="section-title">Taxation Environment vs Constraints to Access Benefits or Avoid Taxes</p>', unsafe_allow_html=True)
    
    fig_scatter = go.Figure()
    
    # Add colored quadrant backgrounds (15% opacity = 0.15)
    # CORRECTED LOGIC:
    # Y-axis (Taxation): 0 = Unfavorable, 1 = Favorable
    # X-axis (Constraints): 0 = High Constraint, 1 = Low Constraint
    # Top-right: Favorable Tax / Low Constraint (GREEN - best)
    fig_scatter.add_shape(type="rect", x0=0.5, y0=0.5, x1=1, y1=1,
        fillcolor="rgba(30, 132, 73, 0.15)", line=dict(width=0), layer="below")
    # Top-left: Favorable Tax / High Constraint (ORANGE)
    fig_scatter.add_shape(type="rect", x0=0, y0=0.5, x1=0.5, y1=1,
        fillcolor="rgba(230, 126, 34, 0.15)", line=dict(width=0), layer="below")
    # Bottom-right: Unfavorable Tax / Low Constraint (ORANGE)
    fig_scatter.add_shape(type="rect", x0=0.5, y0=0, x1=1, y1=0.5,
        fillcolor="rgba(230, 126, 34, 0.15)", line=dict(width=0), layer="below")
    # Bottom-left: Unfavorable Tax / High Constraint (RED - worst)
    fig_scatter.add_shape(type="rect", x0=0, y0=0, x1=0.5, y1=0.5,
        fillcolor="rgba(146, 43, 33, 0.15)", line=dict(width=0), layer="below")
    
    # Add scatter points
    fig_scatter.add_trace(go.Scatter(
        x=df_fiscal["Q6_Constraints"],
        y=df_fiscal["Q1_Taxation"],
        mode='markers+text',
        marker=dict(
            size=12,
            color=[get_score_color((row["Q1_Taxation"] + row["Q6_Constraints"]) / 2, 0, 1) for _, row in df_fiscal.iterrows()],
            line=dict(width=1, color='#4B5563')
        ),
        text=df_fiscal["Country"],
        textposition='top center',
        textfont=dict(size=9, family="Barlow"),
        hovertemplate="<b>%{text}</b><br>Taxation: %{y:.2f}<br>Constraints: %{x:.2f}<extra></extra>"
    ))
    
    # Add quadrant lines
    fig_scatter.add_hline(y=0.5, line_dash="dash", line_color="#94A3B8", line_width=1)
    fig_scatter.add_vline(x=0.5, line_dash="dash", line_color="#94A3B8", line_width=1)
    
    # Add quadrant labels (bold) - CORRECTED
    fig_scatter.add_annotation(x=0.75, y=0.95, text="<b>Favorable Tax / Low Constraint</b>", showarrow=False,
        font=dict(size=10, color="#1E8449", family="Barlow"), xanchor="center")
    fig_scatter.add_annotation(x=0.25, y=0.95, text="<b>Favorable Tax / High Constraint</b>", showarrow=False,
        font=dict(size=10, color="#E67E22", family="Barlow"), xanchor="center")
    fig_scatter.add_annotation(x=0.75, y=0.05, text="<b>Unfavorable Tax / Low Constraint</b>", showarrow=False,
        font=dict(size=10, color="#E67E22", family="Barlow"), xanchor="center")
    fig_scatter.add_annotation(x=0.25, y=0.05, text="<b>Unfavorable Tax / High Constraint</b>", showarrow=False,
        font=dict(size=10, color="#922B21", family="Barlow"), xanchor="center")
    
    fig_scatter.update_layout(
        height=550,
        margin=dict(l=60, r=40, t=40, b=60),
        xaxis=dict(
            title="Constraints to Access Tax Benefits or Avoid Taxes",
            range=[-0.05, 1.05],
            gridcolor='#E2E8F0',
            tickfont=dict(family="Barlow", size=11),
            titlefont=dict(family="Barlow", size=12)
        ),
        yaxis=dict(
            title="Taxation Environment",
            range=[-0.05, 1.05],
            gridcolor='#E2E8F0',
            tickfont=dict(family="Barlow", size=11),
            titlefont=dict(family="Barlow", size=12)
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Barlow"),
        showlegend=False
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("---")
    
    # =====================
    # SECTION 2: Map with filter for Q2, Q4 and Q5 (Yes/No binary)
    # =====================
    st.markdown('<p class="section-title">Fiscal Incentives Map</p>', unsafe_allow_html=True)
    
    col_map_filter, _ = st.columns([1, 3])
    with col_map_filter:
        fiscal_map_question = st.selectbox(
            "Select question",
            ["Is there a power tax?", "Access to subsidies or abatements?", "Ability to shift profit center abroad?"],
            key="fiscal_map_filter"
        )
    
    if fiscal_map_question == "Is there a power tax?":
        map_col = "Q4_Electricity_Tax"
        map_title = "Power Tax Exposure"
        # For power tax: low score = Yes (there is a tax), high score = No (no tax)
        df_fiscal["Binary"] = df_fiscal[map_col].apply(lambda x: 0 if x < 0.5 else 1)
        # Power tax: Yes = #fc7a53 (orange-red), No = #12E09B (green)
        binary_colorscale = [[0, '#fc7a53'], [1, '#12E09B']]
        yes_color = "#fc7a53"
        no_color = "#12E09B"
    elif fiscal_map_question == "Access to subsidies or abatements?":
        map_col = "Q5_Subsidies"
        map_title = "Access to Subsidies or Abatements"
        # For subsidies: high score = Yes (access exists), low score = No
        df_fiscal["Binary"] = df_fiscal[map_col].apply(lambda x: 1 if x >= 0.5 else 0)
        # Subsidies: Yes = #12E09B (green), No = #fc7a53 (orange-red)
        binary_colorscale = [[0, '#fc7a53'], [1, '#12E09B']]
        yes_color = "#12E09B"
        no_color = "#fc7a53"
    else:  # Ability to shift profit center abroad?
        map_col = "Q2_Profit_Center"
        map_title = "Ability to Shift Profit Center Abroad"
        # For profit center: high score = Yes (possible), low score = No
        df_fiscal["Binary"] = df_fiscal[map_col].apply(lambda x: 1 if x >= 0.5 else 0)
        # Profit center: Yes = #12E09B (green), No = #fc7a53 (orange-red)
        binary_colorscale = [[0, '#fc7a53'], [1, '#12E09B']]
        yes_color = "#12E09B"
        no_color = "#fc7a53"
    
    df_fiscal_agg = df_fiscal.groupby("ISO").agg({
        "Binary": "mean",
        "Country": lambda x: ", ".join(x) if len(x) > 1 else x.iloc[0]
    }).reset_index()
    df_fiscal_agg.columns = ["ISO", "Score", "Country"]
    
    fig_fiscal_map = go.Figure(go.Choropleth(
        locations=df_fiscal_agg["ISO"],
        z=df_fiscal_agg["Score"],
        text=df_fiscal_agg["Country"],
        colorscale=binary_colorscale,
        autocolorscale=False,
        zmin=0,
        zmax=1,
        marker_line_color='#4B5563',
        marker_line_width=1,
        showscale=False,
        hovertemplate="<b>%{text}</b><extra></extra>"
    ))
    fig_fiscal_map.update_layout(
        height=450,
        margin=dict(l=0, r=0, t=30, b=0),
        title=dict(
            text=map_title,
            font=dict(family="Barlow", size=14, color="#1E293B"),
            x=0.5,
            xanchor="center"
        ),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="#94A3B8",
            showland=True,
            landcolor="#E2E8F0",
            showocean=True,
            oceancolor="#FFFFFF",
            showcountries=True,
            countrycolor="#94A3B8",
            projection_type='natural earth',
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Barlow")
    )
    st.plotly_chart(fig_fiscal_map, use_container_width=True)
    
    # Binary legend Yes/No with dynamic colors
    st.markdown(f"""
    <div style="display: flex; justify-content: center; gap: 3rem; margin: 1rem 0; font-size: 0.9rem;">
        <span><strong style="color: {yes_color}; font-size: 1.2rem;">●</strong> Yes</span>
        <span><strong style="color: {no_color}; font-size: 1.2rem;">●</strong> No</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # =====================
    # SECTION 3: Corporate Income Tax (CIT) Rates
    # =====================
    st.markdown('<p class="section-title">Corporate Income Tax (CIT) Rates by Jurisdiction</p>', unsafe_allow_html=True)
    
    # CIT rates data (standard corporate tax rates) - Without Texas (US)
    CIT_RATES = {
        "UAE": 9.0,
        "Paraguay": 10.0,
        "Oman": 15.0,
        "Russia": 20.0,
        "Iceland": 20.0,
        "Finland": 20.0,
        "Sweden": 20.6,
        "Kazakhstan": 20.0,
        "Quebec (CA)": 26.5,
        "Alberta (CA)": 23.0,
        "Norway": 22.0,
        "Chile": 27.0,
        "Kenya": 30.0,
        "Ethiopia": 30.0,  # Note: Currently not applied to miners
        "DRC": 30.0,
        "Brazil": 34.0,
        "Argentina": 35.0,
        "Australia": 30.0
    }
    
    # Color function based on CIT rate brackets
    def get_cit_color(rate):
        if rate < 11.0:
            return '#0EAA76'  # Dark green
        elif rate < 20.0:
            return '#12E09B'  # Light green
        elif rate <= 25.0:
            return '#F3B11D'  # Orange/yellow
        elif rate <= 30.0:
            return '#fc7a53'  # Red-orange
        else:
            return '#8A0000'  # Dark red
    
    # Create CIT dataframe
    cit_data = [{"Country": k, "CIT_Rate": v} for k, v in CIT_RATES.items()]
    df_cit = pd.DataFrame(cit_data)
    df_cit = df_cit.sort_values("CIT_Rate", ascending=True)
    
    # Add asterisk to Ethiopia
    df_cit["Display_Country"] = df_cit["Country"].apply(lambda x: x + "*" if x == "Ethiopia" else x)
    
    # Color based on brackets
    colors_cit = [get_cit_color(rate) for rate in df_cit["CIT_Rate"]]
    
    fig_cit = go.Figure(go.Bar(
        x=df_cit["CIT_Rate"],
        y=df_cit["Display_Country"],
        orientation='h',
        marker_color=colors_cit,
        text=df_cit["CIT_Rate"].apply(lambda x: f"{x:.1f}%"),
        textposition='outside',
        textfont=dict(size=11, family="Barlow")
    ))
    
    fig_cit.update_layout(
        height=520,
        margin=dict(l=0, r=60, t=10, b=60),
        xaxis=dict(
            title="Corporate Income Tax Rate (%)",
            range=[0, 42],
            gridcolor='#E2E8F0',
            tickfont=dict(family="Barlow", size=11),
            titlefont=dict(family="Barlow", size=12)
        ),
        yaxis=dict(
            title="",
            tickfont=dict(family="Barlow", size=11)
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Barlow")
    )
    st.plotly_chart(fig_cit, use_container_width=True)
    
    # Legend for CIT color brackets
    st.markdown("""
    <div style="display: flex; justify-content: center; gap: 1.5rem; margin: 0.5rem 0 1rem 0; font-size: 0.85rem; flex-wrap: wrap;">
        <span><strong style="color: #0EAA76; font-size: 1.1rem;">●</strong> &lt;11%</span>
        <span><strong style="color: #12E09B; font-size: 1.1rem;">●</strong> 11-19%</span>
        <span><strong style="color: #F3B11D; font-size: 1.1rem;">●</strong> 20-25%</span>
        <span><strong style="color: #fc7a53; font-size: 1.1rem;">●</strong> 26-30%</span>
        <span><strong style="color: #8A0000; font-size: 1.1rem;">●</strong> &gt;30%</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Note for Ethiopia
    st.markdown("""
    <p style="font-size: 0.8rem; color: #64748B; text-align: center; margin-top: -0.5rem;">
        * Ethiopia: 30% CIT rate currently not applied to Bitcoin miners
    </p>
    """, unsafe_allow_html=True)

# ============================================
# PERMITS & LICENSES PAGE
# ============================================
elif page == "Permits & Licenses":
    st.markdown("# Permits & Licenses Analysis")
    st.markdown('<p class="subtitle-text">Regulatory requirements and permitting conditions assessment</p>', unsafe_allow_html=True)
    
    # Create Permits DataFrame
    permit_data = []
    for country, scores in PERMIT_SCORES.items():
        permit_data.append({
            "Country": country,
            "Q10_Op_License": scores["Q10_Op_License"],
            "Q11_Import_License": scores["Q11_Import_License"],
            "Q12_Construction": scores["Q12_Construction"],
            "Q13_EIA": scores["Q13_EIA"],
            "Q14_Water": scores["Q14_Water"],
            "Q15_Emissions": scores["Q15_Emissions"],
            "Q16_Zoning": scores["Q16_Zoning"]
        })
    df_permit = pd.DataFrame(permit_data)
    df_permit = df_permit.merge(df[["Country", "Region"]], on="Country", how="left")
    df_permit["ISO"] = df_permit["Country"].map(ISO_CODES)
    
    # =====================
    # SECTION 1: Radar Chart Comparison (Coleoptere)
    # =====================
    st.markdown('<p class="section-title">Regulatory Constraints Comparison</p>', unsafe_allow_html=True)
    
    col_radar_f1, col_radar_f2 = st.columns(2)
    countries_list = df_permit["Country"].tolist()
    
    with col_radar_f1:
        country1_radar = st.selectbox("Select first jurisdiction", countries_list, index=0, key="permit_radar_country1")
    with col_radar_f2:
        country2_radar = st.selectbox("Select second jurisdiction", countries_list, index=1, key="permit_radar_country2")
    
    # Radar chart categories
    radar_categories = ["Water Permit", "EIA Process", "Zoning & Land", "Emissions & Noise"]
    radar_cols = ["Q14_Water", "Q13_EIA", "Q16_Zoning", "Q15_Emissions"]
    
    # Get data for both countries
    country1_data = df_permit[df_permit["Country"] == country1_radar].iloc[0]
    country2_data = df_permit[df_permit["Country"] == country2_radar].iloc[0]
    
    country1_values = [country1_data[col] for col in radar_cols]
    country2_values = [country2_data[col] for col in radar_cols]
    
    # Close the radar
    country1_values.append(country1_values[0])
    country2_values.append(country2_values[0])
    radar_categories_closed = radar_categories + [radar_categories[0]]
    
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=country1_values,
        theta=radar_categories_closed,
        fill='toself',
        fillcolor='rgba(18, 224, 155, 0.3)',
        line=dict(color='#12E09B', width=2),
        name=country1_radar
    ))
    
    fig_radar.add_trace(go.Scatterpolar(
        r=country2_values,
        theta=radar_categories_closed,
        fill='toself',
        fillcolor='rgba(243, 177, 29, 0.3)',
        line=dict(color='#F3B11D', width=2),
        name=country2_radar
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickfont=dict(size=10, family="Barlow"),
                gridcolor='#E2E8F0'
            ),
            angularaxis=dict(
                tickfont=dict(size=11, family="Barlow")
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.1,
            xanchor="center",
            x=0.5,
            font=dict(family="Barlow")
        ),
        height=400,
        margin=dict(l=60, r=60, t=60, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Barlow")
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # Descriptions for each radar dimension
    st.markdown("""
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0; font-size: 0.85rem; color: #475569;">
        <div><strong style="color: #F3B11D;">●</strong> <strong>EIA Process:</strong> Environmental Impact Assessment — measures how burdensome the process used to evaluate the potential environmental effects of a proposed project before it is approved or built.</div>
        <div><strong style="color: #fc7a53;">●</strong> <strong>Water Permit:</strong> An official authorization that allows a project to use, withdraw, discharge, or alter water resources under regulated conditions. It evaluates how difficult is to obtain this permit when developing a mining data center.</div>
        <div><strong style="color: #F3B11D;">●</strong> <strong>Zoning & Land:</strong> How zoning rules impact land availability for data center development</div>
        <div><strong style="color: #fc7a53;">●</strong> <strong>Emissions & Noise:</strong> Sizes how restrictive these rules are on data center operations</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # =====================
    # SECTION 2: Map with filter for Q10 and Q11 (Yes/No binary)
    # =====================
    st.markdown('<p class="section-title">Licensing Requirements Map</p>', unsafe_allow_html=True)
    
    col_map_filter, _ = st.columns([1, 3])
    with col_map_filter:
        permit_map_question = st.selectbox(
            "Select question",
            ["License required for operations?", "License required for imports?"],
            key="permit_map_filter"
        )
    
    if permit_map_question == "License required for operations?":
        map_col = "Q10_Op_License"
        map_title = "Operational License Requirement"
    else:
        map_col = "Q11_Import_License"
        map_title = "Import License Requirement"
    
    # For licenses: low score = Yes (license required), high score = No (no license)
    df_permit["Binary"] = df_permit[map_col].apply(lambda x: 0 if x < 0.5 else 1)
    # Yes (required) = #fc7a53, No (not required) = #12E09B
    binary_colorscale = [[0, '#fc7a53'], [1, '#12E09B']]
    yes_color = "#fc7a53"
    no_color = "#12E09B"
    
    df_permit_agg = df_permit.groupby("ISO").agg({
        "Binary": "mean",
        "Country": lambda x: ", ".join(x) if len(x) > 1 else x.iloc[0]
    }).reset_index()
    df_permit_agg.columns = ["ISO", "Score", "Country"]
    
    fig_permit_map = go.Figure(go.Choropleth(
        locations=df_permit_agg["ISO"],
        z=df_permit_agg["Score"],
        text=df_permit_agg["Country"],
        colorscale=binary_colorscale,
        autocolorscale=False,
        zmin=0,
        zmax=1,
        marker_line_color='#4B5563',
        marker_line_width=1,
        showscale=False,
        hovertemplate="<b>%{text}</b><extra></extra>"
    ))
    fig_permit_map.update_layout(
        height=450,
        margin=dict(l=0, r=0, t=30, b=0),
        title=dict(
            text=map_title,
            font=dict(family="Barlow", size=14, color="#1E293B"),
            x=0.5,
            xanchor="center"
        ),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="#94A3B8",
            showland=True,
            landcolor="#E2E8F0",
            showocean=True,
            oceancolor="#FFFFFF",
            showcountries=True,
            countrycolor="#94A3B8",
            projection_type='natural earth',
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Barlow")
    )
    st.plotly_chart(fig_permit_map, use_container_width=True)
    
    # Binary legend Yes/No
    st.markdown(f"""
    <div style="display: flex; justify-content: center; gap: 3rem; margin: 1rem 0; font-size: 0.9rem;">
        <span><strong style="color: {yes_color}; font-size: 1.2rem;">●</strong> License Required</span>
        <span><strong style="color: {no_color}; font-size: 1.2rem;">●</strong> No License Required</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Note for Alberta operating license
    if permit_map_question == "License required for operations?":
        st.markdown("""
        <p style="font-size: 0.8rem; color: #64748B; text-align: center; margin-top: 0;">
            * Note: In Canada, Alberta requires an operating license, not Quebec.
        </p>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # =====================
    # SECTION 3: Construction Permit Timeline Bar Chart
    # =====================
    st.markdown('<p class="section-title">How Long to Break Ground?</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">Construction permit timelines for Bitcoin mining facilities</p>', unsafe_allow_html=True)
    
    # Convert score to estimated months (inverse relationship: higher score = faster = fewer months)
    # Linear mapping: score 1.0 = 2 months, score 0.2 = 18 months
    df_construction = df_permit.copy()
    df_construction["Months"] = df_construction["Q12_Construction"].apply(lambda s: round(18 - (s * 16)))
    df_construction = df_construction.sort_values("Months", ascending=False)
    
    # Color based on month brackets
    def get_construction_color(months):
        if months <= 6:
            return '#0EAA76'  # Dark green
        elif months <= 8:
            return '#12E09B'  # Light green
        elif months <= 12:
            return '#F3B11D'  # Orange/yellow
        else:
            return '#fc7a53'  # Red-orange
    
    colors_construction = [get_construction_color(m) for m in df_construction["Months"]]
    
    fig_construction = go.Figure(go.Bar(
        x=df_construction["Months"],
        y=df_construction["Country"],
        orientation='h',
        marker_color=colors_construction,
        text=df_construction["Months"].apply(lambda x: f"{x} months"),
        textposition='outside',
        textfont=dict(size=11, family="Barlow")
    ))
    
    fig_construction.update_layout(
        height=550,
        margin=dict(l=0, r=80, t=10, b=60),
        xaxis=dict(
            title="Average Timeline (months)",
            range=[0, df_construction["Months"].max() + 3],
            gridcolor='#E2E8F0',
            tickfont=dict(family="Barlow", size=11),
            titlefont=dict(family="Barlow", size=12)
        ),
        yaxis=dict(
            title="",
            tickfont=dict(family="Barlow", size=11)
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Barlow")
    )
    st.plotly_chart(fig_construction, use_container_width=True)
    
    # Legend for timeline color brackets
    st.markdown("""
    <div style="display: flex; justify-content: center; gap: 1.5rem; margin: 0.5rem 0 1rem 0; font-size: 0.85rem; flex-wrap: wrap;">
        <span><strong style="color: #0EAA76; font-size: 1.1rem;">●</strong> &lt;6 months</span>
        <span><strong style="color: #12E09B; font-size: 1.1rem;">●</strong> 7-8 months</span>
        <span><strong style="color: #F3B11D; font-size: 1.1rem;">●</strong> 10-12 months</span>
        <span><strong style="color: #fc7a53; font-size: 1.1rem;">●</strong> &gt;12 months</span>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# ENERGY & GRID PAGE
# ============================================
elif page == "Energy & Grid":
    st.markdown("# Energy & Grid Access")
    st.markdown('<p class="subtitle-text">Power market accessibility and grid connection conditions</p>', unsafe_allow_html=True)
    
    # Real data from EMI report - Electricity Price ($/MWh) and Grid Connection Time (months)
    ENERGY_REAL_DATA = {
        "Argentina": {"price_mwh": 51.25, "grid_months": 12, "barriers": 0.21},
        "Quebec (CA)": {"price_mwh": 45.0, "grid_months": 15, "barriers": 0.21},
        "Alberta (CA)": {"price_mwh": 45.0, "grid_months": 24, "barriers": 0.15},
        "Brazil": {"price_mwh": 50.0, "grid_months": 12, "barriers": 0.67},
        "Chile": {"price_mwh": 60.0, "grid_months": 24, "barriers": 0.00},
        "Ethiopia": {"price_mwh": 42.5, "grid_months": 9, "barriers": 0.81},
        "Finland": {"price_mwh": 45.0, "grid_months": 15, "barriers": 0.50},
        "Iceland": {"price_mwh": 55.0, "grid_months": 12, "barriers": 0.58},
        "Kazakhstan": {"price_mwh": 60.0, "grid_months": 15, "barriers": 0.19},
        "Kenya": {"price_mwh": 35.0, "grid_months": 6, "barriers": 1.00},
        "Norway": {"price_mwh": 35.0, "grid_months": 21, "barriers": 0.23},
        "Oman": {"price_mwh": 41.75, "grid_months": 9, "barriers": 0.75},
        "Paraguay": {"price_mwh": 48.75, "grid_months": 7.5, "barriers": 0.44},
        "DRC": {"price_mwh": 22.0, "grid_months": 6, "barriers": 0.50},
        "Russia": {"price_mwh": 60.0, "grid_months": 12, "barriers": 0.23},
        "Sweden": {"price_mwh": 38.75, "grid_months": 15, "barriers": 0.50},
        "UAE": {"price_mwh": 45.0, "grid_months": 9, "barriers": 0.83},
        "Texas (US)": {"price_mwh": 45.0, "grid_months": 12, "barriers": 0.39},
        "Australia": {"price_mwh": 60.0, "grid_months": 15, "barriers": 0.30}
    }
    
    # Create Energy DataFrame with real data
    energy_real_list = []
    for country, data in ENERGY_REAL_DATA.items():
        energy_real_list.append({
            "Country": country,
            "Price_MWh": data["price_mwh"],
            "Grid_Months": data["grid_months"],
            "Barriers": data["barriers"]
        })
    df_energy_real = pd.DataFrame(energy_real_list)
    df_energy_real = df_energy_real.merge(df[["Country", "Region"]], on="Country", how="left")
    df_energy_real["ISO"] = df_energy_real["Country"].map(ISO_CODES)
    
    # =====================
    # SECTION 1: Scatter Plot - Grid Connection Time vs Electricity Price (Real Values)
    # =====================
    st.markdown('<p class="section-title">Grid Connection Time vs Electricity Price</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">Comparing time to connect to the grid (months) with power costs ($/MWh)</p>', unsafe_allow_html=True)
    
    fig_energy_scatter = go.Figure()
    
    # Define thresholds for quadrants - center at 15 months and 47.5 $/MWh
    price_center = 47.5
    time_center = 15
    
    # Add colored quadrant backgrounds (15% opacity)
    # Top-left: Fast Connection / Expensive Power (ORANGE)
    fig_energy_scatter.add_shape(type="rect", x0=3, y0=price_center, x1=time_center, y1=80,
        fillcolor="rgba(230, 126, 34, 0.15)", line=dict(width=0), layer="below")
    # Top-right: Slow Connection / Expensive Power (RED - worst)
    fig_energy_scatter.add_shape(type="rect", x0=time_center, y0=price_center, x1=30, y1=80,
        fillcolor="rgba(146, 43, 33, 0.15)", line=dict(width=0), layer="below")
    # Bottom-left: Fast Connection / Cheap Power (GREEN - best)
    fig_energy_scatter.add_shape(type="rect", x0=3, y0=15, x1=time_center, y1=price_center,
        fillcolor="rgba(30, 132, 73, 0.15)", line=dict(width=0), layer="below")
    # Bottom-right: Slow Connection / Cheap Power (ORANGE)
    fig_energy_scatter.add_shape(type="rect", x0=time_center, y0=15, x1=30, y1=price_center,
        fillcolor="rgba(230, 126, 34, 0.15)", line=dict(width=0), layer="below")
    
    # Calculate colors based on combined favorability (lower price + faster time = better)
    def get_energy_color(price, months):
        # Normalize: lower is better for both
        price_score = 1 - (price - 20) / (70 - 20)  # 20-70 range
        time_score = 1 - (months - 3) / (30 - 3)  # 3-30 range
        combined = (price_score + time_score) / 2
        return get_score_color(max(0, min(1, combined)), 0, 1)
    
    colors_energy = [get_energy_color(row["Price_MWh"], row["Grid_Months"]) for _, row in df_energy_real.iterrows()]
    
    fig_energy_scatter.add_trace(go.Scatter(
        x=df_energy_real["Grid_Months"],
        y=df_energy_real["Price_MWh"],
        mode='markers+text',
        marker=dict(
            size=14,
            color=colors_energy,
            line=dict(width=1.5, color='#4B5563')
        ),
        text=df_energy_real["Country"],
        textposition='top center',
        textfont=dict(size=10, family="Barlow"),
        hovertemplate="<b>%{text}</b><br>Grid Time: %{x} months<br>Price: $%{y}/MWh<extra></extra>"
    ))
    
    # Add quadrant lines at medians (dashed line at $47.5/MWh)
    fig_energy_scatter.add_hline(y=47.5, line_dash="dash", line_color="#94A3B8", line_width=1.5,
        annotation_text="$47.5/MWh", annotation_position="right")
    fig_energy_scatter.add_vline(x=time_center, line_dash="dash", line_color="#94A3B8", line_width=1.5,
        annotation_text="15 months", annotation_position="top")
    
    # Add quadrant labels
    fig_energy_scatter.add_annotation(x=9, y=71, text="<b>Fast / Expensive</b>", showarrow=False,
        font=dict(size=11, color="#E67E22", family="Barlow"), xanchor="center")
    fig_energy_scatter.add_annotation(x=22.5, y=71, text="<b>Slow / Expensive</b>", showarrow=False,
        font=dict(size=11, color="#922B21", family="Barlow"), xanchor="center")
    fig_energy_scatter.add_annotation(x=9, y=20, text="<b>Fast / Cheap</b>", showarrow=False,
        font=dict(size=11, color="#1E8449", family="Barlow"), xanchor="center")
    fig_energy_scatter.add_annotation(x=22.5, y=20, text="<b>Slow / Cheap</b>", showarrow=False,
        font=dict(size=11, color="#E67E22", family="Barlow"), xanchor="center")
    
    fig_energy_scatter.update_layout(
        height=550,
        margin=dict(l=60, r=60, t=30, b=60),
        xaxis=dict(
            title="<b>Grid Connection Lead Time (months)</b>",
            range=[3, 30],
            gridcolor='#E2E8F0',
            tickfont=dict(family="Barlow", size=11),
            titlefont=dict(family="Barlow", size=12),
            dtick=6
        ),
        yaxis=dict(
            title="<b>Electricity Price ($/MWh)</b>",
            range=[15, 75],
            gridcolor='#E2E8F0',
            tickfont=dict(family="Barlow", size=11),
            titlefont=dict(family="Barlow", size=12),
            tickprefix="$"
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Barlow"),
        showlegend=False
    )
    st.plotly_chart(fig_energy_scatter, use_container_width=True)
    
    st.markdown("---")
    
    # =====================
    # SECTION 2: Map - Barriers to Entry the Energy Market
    # =====================
    st.markdown('<p class="section-title">Barriers to Entry the Energy Market</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">Level of barriers to entry for accessing grid/energy</p>', unsafe_allow_html=True)
    
    df_barriers_agg = df_energy_real.groupby("ISO").agg({
        "Barriers": "mean",
        "Country": lambda x: ", ".join(x) if len(x) > 1 else x.iloc[0]
    }).reset_index()
    df_barriers_agg.columns = ["ISO", "Score", "Country"]
    
    fig_barriers_map = go.Figure(go.Choropleth(
        locations=df_barriers_agg["ISO"],
        z=df_barriers_agg["Score"],
        text=df_barriers_agg["Country"],
        colorscale=[
            [0, '#922B21'], [0.25, '#E67E22'], [0.5, '#F4D03F'], [0.75, '#52BE80'], [1, '#1E8449']
        ],
        autocolorscale=False,
        zmin=0,
        zmax=1,
        marker_line_color='#4B5563',
        marker_line_width=1,
        colorbar=dict(
            title=dict(text="Score", side="right", font=dict(family="Barlow", size=12)),
            tickfont=dict(family="Barlow", size=10),
            len=0.6,
            tickvals=[0, 0.25, 0.5, 0.75, 1],
            ticktext=["High Barriers", "", "Neutral", "", "Low Barriers"]
        ),
        hovertemplate="<b>%{text}</b><br>Score: %{z:.2f}<extra></extra>"
    ))
    
    fig_barriers_map.update_layout(
        height=450,
        margin=dict(l=0, r=0, t=10, b=0),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="#94A3B8",
            showland=True,
            landcolor="#E2E8F0",
            showocean=True,
            oceancolor="#FFFFFF",
            showcountries=True,
            countrycolor="#94A3B8",
            projection_type='natural earth',
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Barlow")
    )
    st.plotly_chart(fig_barriers_map, use_container_width=True)
    
    st.markdown("""
    <p style="font-size: 0.85rem; color: #64748B; text-align: center;">
        Higher score = Lower barriers to entry for energy market participation or grid interconnection
    </p>
    """, unsafe_allow_html=True)


# ============================================
# CUSTOMS & TARIFFS PAGE
# ============================================
elif page == "Customs & Tariffs":
    st.markdown("# Customs & Tariffs")
    st.markdown('<p class="subtitle-text">Import procedures, VAT regime, and trade barriers for mining equipment</p>', unsafe_allow_html=True)
    
    # Customs & Tariffs data from Excel
    CUSTOMS_TARIFFS_SCORES = {
        "Argentina": {"VAT_Rate": 1.0, "VAT_Filing": 0.35, "ASIC_Import": 0.25, "Elec_Import": 0.38, "Tariff_Duties": 0.55, "Procurement": 0.48, "Mitigation": 0.50},
        "Quebec (CA)": {"VAT_Rate": 1.0, "VAT_Filing": 0.75, "ASIC_Import": 0.62, "Elec_Import": 0.62, "Tariff_Duties": 0.85, "Procurement": 0.25, "Mitigation": 0.50},
        "Alberta (CA)": {"VAT_Rate": 0.9, "VAT_Filing": 0.75, "ASIC_Import": 0.5, "Elec_Import": 0.5, "Tariff_Duties": 0.85, "Procurement": 0.5, "Mitigation": 0.50},
        "Brazil": {"VAT_Rate": 0.15, "VAT_Filing": 0.5, "ASIC_Import": 0.5, "Elec_Import": 1.0, "Tariff_Duties": 0.38, "Procurement": 0.5, "Mitigation": 0.68},
        "Chile": {"VAT_Rate": 0.75, "VAT_Filing": 0.5, "ASIC_Import": 0.75, "Elec_Import": 0.55, "Tariff_Duties": 0.15, "Procurement": 0.5, "Mitigation": 0.20},
        "Ethiopia": {"VAT_Rate": 0.45, "VAT_Filing": 0.5, "ASIC_Import": 0.35, "Elec_Import": 0.85, "Tariff_Duties": 0.29, "Procurement": 0.5, "Mitigation": 0.65},
        "Finland": {"VAT_Rate": 0.62, "VAT_Filing": 0.5, "ASIC_Import": 0.75, "Elec_Import": 1.0, "Tariff_Duties": 0.5, "Procurement": 0.5, "Mitigation": 0.70},
        "Iceland": {"VAT_Rate": 0.67, "VAT_Filing": 0.5, "ASIC_Import": 0.75, "Elec_Import": 0.5, "Tariff_Duties": 0.48, "Procurement": 0.5, "Mitigation": 0.47},
        "Kazakhstan": {"VAT_Rate": 0.25, "VAT_Filing": 0.5, "ASIC_Import": 0.5, "Elec_Import": 0.75, "Tariff_Duties": 1.0, "Procurement": 0.7, "Mitigation": 0.50},
        "Kenya": {"VAT_Rate": 0.25, "VAT_Filing": 0.35, "ASIC_Import": 0.5, "Elec_Import": 0.5, "Tariff_Duties": 0.0, "Procurement": 0.5, "Mitigation": 0.50},
        "Norway": {"VAT_Rate": 0.1, "VAT_Filing": 0.62, "ASIC_Import": 0.83, "Elec_Import": 0.75, "Tariff_Duties": 1.0, "Procurement": 0.48, "Mitigation": 0.50},
        "Oman": {"VAT_Rate": 0.9, "VAT_Filing": 0.5, "ASIC_Import": 0.88, "Elec_Import": 1.0, "Tariff_Duties": 0.57, "Procurement": 0.5, "Mitigation": 0.75},
        "Paraguay": {"VAT_Rate": 1.0, "VAT_Filing": 0.62, "ASIC_Import": 0.64, "Elec_Import": 0.71, "Tariff_Duties": 0.85, "Procurement": 0.49, "Mitigation": 0.50},
        "DRC": {"VAT_Rate": 0.5, "VAT_Filing": 0.5, "ASIC_Import": 0.0, "Elec_Import": 0.0, "Tariff_Duties": 0.5, "Procurement": 0.5, "Mitigation": 0.75},
        "Russia": {"VAT_Rate": 0.25, "VAT_Filing": 0.55, "ASIC_Import": 0.5, "Elec_Import": 0.58, "Tariff_Duties": 1.0, "Procurement": 0.55, "Mitigation": 0.50},
        "Sweden": {"VAT_Rate": 0.75, "VAT_Filing": 0.5, "ASIC_Import": 0.5, "Elec_Import": 1.0, "Tariff_Duties": 0.5, "Procurement": 0.5, "Mitigation": 0.75},
        "UAE": {"VAT_Rate": 0.5, "VAT_Filing": 0.62, "ASIC_Import": 0.62, "Elec_Import": 0.44, "Tariff_Duties": 1.0, "Procurement": 0.15, "Mitigation": 0.50},
        "Texas (US)": {"VAT_Rate": 0.05, "VAT_Filing": 0.5, "ASIC_Import": 0.33, "Elec_Import": 0.26, "Tariff_Duties": 0.26, "Procurement": 0.5, "Mitigation": 0.66},
        "Australia": {"VAT_Rate": 0.5, "VAT_Filing": 0.5, "ASIC_Import": 0.5, "Elec_Import": 0.5, "Tariff_Duties": 0.5, "Procurement": 0.5, "Mitigation": 0.30}
    }
    
    # Tariffs and VAT data from the uploaded Excel file
    TARIFF_VAT_DATA = {
        "Argentina": {"tariff": 0.11, "vat": 0.27, "refundable": "Yes"},
        "Australia": {"tariff": 0.00, "vat": 0.10, "refundable": "No"},
        "Brazil": {"tariff": 0.00, "vat": 0.325, "refundable": "Partially"},
        "Alberta (CA)": {"tariff": 0.02, "vat": 0.05, "refundable": "Yes"},
        "Quebec (CA)": {"tariff": 0.00, "vat": 0.05, "refundable": "Yes"},
        "Chile": {"tariff": 0.10, "vat": 0.19, "refundable": "No"},
        "DRC": {"tariff": 1.80, "vat": 0.16, "refundable": "No"},
        "Ethiopia": {"tariff": 0.03, "vat": 0.15, "refundable": "Yes"},
        "Finland": {"tariff": 0.00, "vat": 0.255, "refundable": "No"},
        "Iceland": {"tariff": 0.00, "vat": 0.24, "refundable": "Yes"},
        "Kazakhstan": {"tariff": 0.00, "vat": 0.16, "refundable": "No"},
        "Kenya": {"tariff": 0.14, "vat": 0.16, "refundable": "Yes"},
        "Norway": {"tariff": 0.00, "vat": 0.25, "refundable": "No"},
        "Oman": {"tariff": 0.00, "vat": 0.05, "refundable": "Yes"},
        "Paraguay": {"tariff": 0.07, "vat": 0.10, "refundable": "Yes"},
        "Russia": {"tariff": 0.22, "vat": 0.00, "refundable": "No"},
        "Sweden": {"tariff": 0.00, "vat": 0.25, "refundable": "No"},
        "UAE": {"tariff": 0.00, "vat": 0.05, "refundable": "Yes"},
        "Texas (US)": {"tariff": 0.20, "vat": 0.00, "refundable": "No"}
    }
    
    # Customs summaries from the Word document
    CUSTOMS_SUMMARIES = {
        "Argentina": "27% VAT (refundable), 11% tariff on ASICs. Import license required. Unfavorable procedures for ASICs. Custom brokers effective to mitigate delays and avoid tariffs.",
        "Quebec (CA)": "5% GST (refundable), 0% tariff. No license required. Slightly favorable import procedures. Mitigation mechanisms effective to accelerate deliveries.",
        "Alberta (CA)": "5% GST (refundable), 2% tariff. No license required. Neutral import procedures. Mitigation mechanisms effective to cut tariffs.",
        "Brazil": "30-35% VAT (complex layers), tariffs temporarily suspended. No license required. Neutral procedures but qualified local expert strongly recommended.",
        "Chile": "19% VAT, 10% tariff. No license required. Highly favorable procedures for ASICs. Mitigation mechanisms ineffective to cut tariffs.",
        "Ethiopia": "15% VAT (not yet applied), 3-15% tariff depending on HS classification. License required. Slightly unfavorable procedures, experienced clearing agent essential.",
        "Finland": "25.5% VAT, no tariff. No license required. Neutral procedures for ASICs. Mitigation mechanisms effective to avoid VAT.",
        "Iceland": "24% VAT (refundable), no tariff. No license required. Favorable procedures. Mitigation slightly effective, VAT exclusion discussions ongoing.",
        "Kazakhstan": "16% VAT, no tariff. License required. Neutral procedures. Mitigation marginally effective.",
        "Kenya": "16% VAT (can be exempted), 14% tariff. No license required. Mitigation mechanisms effective to cut tariffs.",
        "Norway": "25% VAT, no tariff. License required. Favorable procedures. Mitigation effective to avoid VAT.",
        "Oman": "5% VAT (exempted in free zones), <5% tariff. No license required. Highly favorable procedures. Custom brokers effective.",
        "Paraguay": "10% VAT (can be exempted), 4-10% tariff. No license required. Marginally favorable procedures. Mitigation effective to reduce custom burden.",
        "DRC": "16% VAT, up to 180% total tariff possible. License required. Highly unfavorable procedures. Mitigation effective to circumvent taxes.",
        "Russia": "22% tariff, no VAT on imports. License required. Neutral procedures. Mitigation slightly effective.",
        "Sweden": "25% VAT, no tariff. No license required. Neutral procedures. Mitigation effective to avoid VAT.",
        "UAE": "5% VAT (exempted in free zones), no tariff. License required. Favorable procedures. Mitigation effective.",
        "Texas (US)": "No VAT, 10-30% tariff (variable). No license required. Unfavorable procedures. Mitigation slightly effective.",
        "Australia": "10% GST, no tariff. License required. Unfavorable procedures with stringent oversight. Mitigation largely ineffective."
    }
    
    # Create customs dataframe
    customs_list = []
    for country, scores in CUSTOMS_TARIFFS_SCORES.items():
        tariff_data = TARIFF_VAT_DATA.get(country, {"tariff": 0, "vat": 0, "refundable": "No"})
        customs_list.append({
            "Country": country,
            "VAT_Rate": scores["VAT_Rate"],
            "VAT_Percent": tariff_data["vat"] * 100,
            "Tariff_Percent": tariff_data["tariff"] * 100,
            "Refundable": tariff_data["refundable"],
            "VAT_Filing": scores["VAT_Filing"],
            "ASIC_Import": scores["ASIC_Import"],
            "Elec_Import": scores["Elec_Import"],
            "Tariff_Duties": scores["Tariff_Duties"],
            "Procurement": scores["Procurement"],
            "Mitigation": scores["Mitigation"]
        })
    df_customs = pd.DataFrame(customs_list)
    df_customs = df_customs.merge(df[["Country", "Region"]], on="Country", how="left")
    df_customs["ISO"] = df_customs["Country"].map(ISO_CODES)
    
    # =====================
    # SECTION 1: Scatter Plot - ASIC Import vs Electrical Infrastructure Import
    # =====================
    st.markdown('<p class="section-title">Equipment Import Complexity</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">ASIC miners import process vs. electrical infrastructure import process</p>', unsafe_allow_html=True)
    
    fig_import_scatter = go.Figure()
    
    # Add quadrant backgrounds
    fig_import_scatter.add_shape(type="rect", x0=0.5, y0=0.5, x1=1, y1=1,
        fillcolor="rgba(30, 132, 73, 0.15)", line=dict(width=0), layer="below")
    fig_import_scatter.add_shape(type="rect", x0=0, y0=0.5, x1=0.5, y1=1,
        fillcolor="rgba(230, 126, 34, 0.15)", line=dict(width=0), layer="below")
    fig_import_scatter.add_shape(type="rect", x0=0.5, y0=0, x1=1, y1=0.5,
        fillcolor="rgba(230, 126, 34, 0.15)", line=dict(width=0), layer="below")
    fig_import_scatter.add_shape(type="rect", x0=0, y0=0, x1=0.5, y1=0.5,
        fillcolor="rgba(146, 43, 33, 0.15)", line=dict(width=0), layer="below")
    
    colors_import = [get_score_color((row["ASIC_Import"] + row["Elec_Import"]) / 2, 0, 1) for _, row in df_customs.iterrows()]
    
    fig_import_scatter.add_trace(go.Scatter(
        x=df_customs["ASIC_Import"],
        y=df_customs["Elec_Import"],
        mode='markers+text',
        marker=dict(size=14, color=colors_import, line=dict(width=1.5, color='#4B5563')),
        text=df_customs["Country"],
        textposition='top center',
        textfont=dict(size=10, family="Barlow"),
        hovertemplate="<b>%{text}</b><br>ASIC Import: %{x:.2f}<br>Elec Import: %{y:.2f}<extra></extra>"
    ))
    
    fig_import_scatter.add_hline(y=0.5, line_dash="dash", line_color="#94A3B8", line_width=1.5)
    fig_import_scatter.add_vline(x=0.5, line_dash="dash", line_color="#94A3B8", line_width=1.5)
    
    fig_import_scatter.add_annotation(x=0.75, y=0.95, text="<b>Easy ASIC / Easy Elec</b>", showarrow=False,
        font=dict(size=11, color="#1E8449", family="Barlow"), xanchor="center")
    fig_import_scatter.add_annotation(x=0.25, y=0.95, text="<b>Hard ASIC / Easy Elec</b>", showarrow=False,
        font=dict(size=11, color="#E67E22", family="Barlow"), xanchor="center")
    fig_import_scatter.add_annotation(x=0.75, y=0.05, text="<b>Easy ASIC / Hard Elec</b>", showarrow=False,
        font=dict(size=11, color="#E67E22", family="Barlow"), xanchor="center")
    fig_import_scatter.add_annotation(x=0.25, y=0.05, text="<b>Hard ASIC / Hard Elec</b>", showarrow=False,
        font=dict(size=11, color="#922B21", family="Barlow"), xanchor="center")
    
    fig_import_scatter.update_layout(
        height=500,
        margin=dict(l=60, r=60, t=30, b=60),
        xaxis=dict(
            title="<b>ASIC Import Process</b><br>(Higher = Easier)",
            range=[-0.05, 1.05],
            gridcolor='#E2E8F0',
            tickfont=dict(family="Barlow", size=11),
            titlefont=dict(family="Barlow", size=12)
        ),
        yaxis=dict(
            title="<b>Electrical Infrastructure Import</b><br>(Higher = Easier)",
            range=[-0.05, 1.05],
            gridcolor='#E2E8F0',
            tickfont=dict(family="Barlow", size=11),
            titlefont=dict(family="Barlow", size=12)
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Barlow"),
        showlegend=False
    )
    st.plotly_chart(fig_import_scatter, use_container_width=True)
    
    st.markdown("---")
    
    # =====================
    # SECTION 2: Tariffs & VAT Combined Stacked Bar Chart
    # =====================
    st.markdown('<p class="section-title">Tariffs & VAT Exposure</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">Import tariffs and VAT rates applied to ASICs imports</p>', unsafe_allow_html=True)
    
    # Country filter - multiselect with Argentina as default
    all_countries = df_customs["Country"].tolist()
    # Ensure Argentina is first in the default selection
    default_countries = ["Argentina"]
    
    selected_countries_tariff = st.multiselect(
        "Select countries",
        options=all_countries,
        default=default_countries,
        key="tariff_vat_countries"
    )
    
    # If no country selected, show Argentina
    if not selected_countries_tariff:
        selected_countries_tariff = ["Argentina"]
    
    # Filter and sort by total burden (tariff + VAT)
    df_tariff_vat = df_customs[df_customs["Country"].isin(selected_countries_tariff)].copy()
    df_tariff_vat["Total_Burden"] = df_tariff_vat["Tariff_Percent"] + df_tariff_vat["VAT_Percent"]
    df_tariff_vat = df_tariff_vat.sort_values("Total_Burden", ascending=True)
    
    fig_tariff_vat = go.Figure()
    
    # Tariff bars - with 20% transparency
    fig_tariff_vat.add_trace(go.Bar(
        name='Tariff (%)',
        y=df_tariff_vat["Country"],
        x=df_tariff_vat["Tariff_Percent"],
        orientation='h',
        marker_color='rgba(167, 188, 247, 0.8)',
        text=df_tariff_vat["Tariff_Percent"].apply(lambda x: f"{x:.0f}%" if x >= 1 else f"{x:.1f}%" if x > 0 else ""),
        textposition='inside',
        textfont=dict(size=10, family="Barlow", color="#1E293B")
    ))
    
    # VAT bars (stacked) - Color based on refundable status (with 20% transparency)
    vat_colors = []
    for _, row in df_tariff_vat.iterrows():
        if row["Refundable"] == "Yes":
            vat_colors.append('rgba(13, 111, 255, 0.8)')  # Blue for refundable
        elif row["Refundable"] == "Partially":
            vat_colors.append('rgba(0, 32, 96, 0.8)')  # Dark blue for partially
        else:
            vat_colors.append('rgba(243, 177, 29, 0.8)')  # Yellow/orange for non-refundable
    
    fig_tariff_vat.add_trace(go.Bar(
        name='VAT (%)',
        y=df_tariff_vat["Country"],
        x=df_tariff_vat["VAT_Percent"],
        orientation='h',
        marker_color=vat_colors,
        text=df_tariff_vat.apply(lambda row: f"{row['VAT_Percent']:.1f}%{'*' if row['Refundable'] == 'Yes' else '**' if row['Refundable'] == 'Partially' else ''}", axis=1),
        textposition='inside',
        textfont=dict(size=10, family="Barlow", color="white")
    ))
    
    # Dynamic height based on number of countries
    chart_height = max(200, len(selected_countries_tariff) * 35 + 80)
    
    fig_tariff_vat.update_layout(
        height=chart_height,
        margin=dict(l=0, r=80, t=10, b=60),
        barmode='stack',
        xaxis=dict(
            title="Rate (%)",
            range=[0, max(df_tariff_vat["Total_Burden"].max() + 10, 50) if len(df_tariff_vat) > 0 else 50],
            gridcolor='#E2E8F0',
            tickfont=dict(family="Barlow", size=11),
            titlefont=dict(family="Barlow", size=12),
            ticksuffix="%"
        ),
        yaxis=dict(
            title="",
            tickfont=dict(family="Barlow", size=11)
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Barlow"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(family="Barlow", size=11)
        )
    )
    st.plotly_chart(fig_tariff_vat, use_container_width=True)
    
    # Legend for VAT refundable status - updated colors
    st.markdown("""
    <div style="display: flex; justify-content: center; gap: 2rem; margin: 0.5rem 0 1rem 0; font-size: 0.85rem; flex-wrap: wrap;">
        <span><strong style="color: #A7BCF7; font-size: 1.1rem;">■</strong> Tariff</span>
        <span><strong style="color: #0D6FFF; font-size: 1.1rem;">■</strong> VAT Refundable*</span>
        <span><strong style="color: #002060; font-size: 1.1rem;">■</strong> VAT Partially Refundable**</span>
        <span><strong style="color: #F3B11D; font-size: 1.1rem;">■</strong> VAT Non-Refundable</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # =====================
    # SECTION 3: Mitigation Mechanisms Map
    # =====================
    st.markdown('<p class="section-title">Import Constraint Mitigation Mechanisms</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">Effectiveness of administrative mitigation efforts to reduce import burdens</p>', unsafe_allow_html=True)
    
    df_mitigation_agg = df_customs.groupby("ISO").agg({
        "Mitigation": "mean",
        "Country": lambda x: ", ".join(x) if len(x) > 1 else x.iloc[0]
    }).reset_index()
    df_mitigation_agg.columns = ["ISO", "Score", "Country"]
    
    fig_mitigation_map = go.Figure(go.Choropleth(
        locations=df_mitigation_agg["ISO"],
        z=df_mitigation_agg["Score"],
        text=df_mitigation_agg["Country"],
        colorscale=[
            [0, '#922B21'], [0.25, '#E67E22'], [0.5, '#F4D03F'], [0.75, '#52BE80'], [1, '#1E8449']
        ],
        autocolorscale=False,
        zmin=0,
        zmax=1,
        marker_line_color='#4B5563',
        marker_line_width=1,
        colorbar=dict(
            title=dict(text="Score", side="right", font=dict(family="Barlow", size=12)),
            tickfont=dict(family="Barlow", size=10),
            len=0.6,
            tickvals=[0, 0.25, 0.5, 0.75, 1],
            ticktext=["Ineffective", "", "Moderate", "", "Highly Effective"]
        ),
        hovertemplate="<b>%{text}</b><br>Score: %{z:.2f}<extra></extra>"
    ))
    
    fig_mitigation_map.update_layout(
        height=450,
        margin=dict(l=0, r=0, t=10, b=0),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="#94A3B8",
            showland=True,
            landcolor="#E2E8F0",
            showocean=True,
            oceancolor="#FFFFFF",
            showcountries=True,
            countrycolor="#94A3B8",
            projection_type='natural earth',
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Barlow")
    )
    st.plotly_chart(fig_mitigation_map, use_container_width=True)
    
    st.markdown("---")
    
    # =====================
    # SECTION 4: Import Process Comparison Radar
    # =====================
    st.markdown('<p class="section-title">Import Process Comparison</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        customs_j1 = st.selectbox("Select first jurisdiction", df_customs["Country"].tolist(), index=0, key="customs_j1")
    with col2:
        customs_j2 = st.selectbox("Select second jurisdiction", df_customs["Country"].tolist(), index=1, key="customs_j2")
    
    # Get data for selected jurisdictions
    j1_data = df_customs[df_customs["Country"] == customs_j1].iloc[0]
    j2_data = df_customs[df_customs["Country"] == customs_j2].iloc[0]
    
    categories = ['ASIC Import', 'Elec. Import', 'Tariff Duties', 'Procurement', 'VAT Rate', 'Mitigation']
    
    fig_customs_radar = go.Figure()
    
    fig_customs_radar.add_trace(go.Scatterpolar(
        r=[j1_data["ASIC_Import"], j1_data["Elec_Import"], j1_data["Tariff_Duties"], 
           j1_data["Procurement"], j1_data["VAT_Rate"], j1_data["Mitigation"], j1_data["ASIC_Import"]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(18, 224, 155, 0.3)',
        line=dict(color='#12E09B', width=2),
        name=customs_j1
    ))
    
    fig_customs_radar.add_trace(go.Scatterpolar(
        r=[j2_data["ASIC_Import"], j2_data["Elec_Import"], j2_data["Tariff_Duties"], 
           j2_data["Procurement"], j2_data["VAT_Rate"], j2_data["Mitigation"], j2_data["ASIC_Import"]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(243, 177, 29, 0.3)',
        line=dict(color='#F3B11D', width=2),
        name=customs_j2
    ))
    
    fig_customs_radar.update_layout(
        height=450,
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickfont=dict(family="Barlow", size=10),
                gridcolor='#E2E8F0'
            ),
            angularaxis=dict(
                tickfont=dict(family="Barlow", size=11),
                gridcolor='#E2E8F0'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Barlow"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(family="Barlow", size=12)
        ),
        margin=dict(l=60, r=60, t=40, b=60)
    )
    st.plotly_chart(fig_customs_radar, use_container_width=True)
    
    # Descriptions
    st.markdown("""
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0; font-size: 0.85rem; color: #475569;">
        <div><strong>ASIC Import:</strong> Ease of importing mining hardware (ASICs)</div>
        <div><strong>Elec. Import:</strong> Ease of importing electrical infrastructure</div>
        <div><strong>Tariff Duties:</strong> Level of customs duties (higher = lower duties)</div>
        <div><strong>Procurement:</strong> Lead times impact on equipment delivery</div>
        <div><strong>VAT Rate:</strong> Favorability of VAT/sales tax regime</div>
        <div><strong>Mitigation:</strong> Effectiveness of mechanisms to reduce import burdens</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Side-by-side customs summaries (no separator, no title, new colors)
    col_sum1, col_sum2 = st.columns(2)
    with col_sum1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(18, 224, 155, 0.1) 0%, rgba(18, 224, 155, 0.05) 100%); border-radius: 12px; padding: 1.25rem; border-left: 4px solid #12E09B; height: 100%;">
            <p style="font-size: 1rem; font-weight: 600; color: #12E09B; margin-bottom: 0.75rem;">{customs_j1}</p>
            <p style="font-size: 0.85rem; color: #334155; line-height: 1.6;">{CUSTOMS_SUMMARIES.get(customs_j1, "No data available.")}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_sum2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(243, 177, 29, 0.1) 0%, rgba(243, 177, 29, 0.05) 100%); border-radius: 12px; padding: 1.25rem; border-left: 4px solid #F3B11D; height: 100%;">
            <p style="font-size: 1rem; font-weight: 600; color: #F3B11D; margin-bottom: 0.75rem;">{customs_j2}</p>
            <p style="font-size: 0.85rem; color: #334155; line-height: 1.6;">{CUSTOMS_SUMMARIES.get(customs_j2, "No data available.")}</p>
        </div>
        """, unsafe_allow_html=True)

# METHODOLOGY PAGE
# ============================================
elif page == "Methodology":
    st.markdown("# Methodology")
    st.markdown("How we built the Ease to Mine Index")
    st.markdown("")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class="methodology-card"><div class="methodology-card-value">48</div>
            <div class="methodology-card-title">Respondents</div>
            <div class="methodology-card-desc">Industrial Miners, Association,<br>Journalist & Experts</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="methodology-card"><div class="methodology-card-value">55</div>
            <div class="methodology-card-title">Responses</div>
            <div class="methodology-card-desc">Total survey submissions<br>&nbsp;</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="methodology-card"><div class="methodology-card-value">19</div>
            <div class="methodology-card-title">Jurisdictions</div>
            <div class="methodology-card-desc">Including Québec & Alberta<br>for Canada</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="methodology-card"><div class="methodology-card-value">33</div>
            <div class="methodology-card-title">Questions</div>
            <div class="methodology-card-desc">Across 5 survey sections<br>&nbsp;</div></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col_timeline, col_pie = st.columns([1, 1])
    
    with col_timeline:
        st.markdown('<p class="section-title">Survey Timeline</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="timeline-item"><div class="timeline-date">December 2025</div><div class="timeline-title">Survey Launch</div>
            <div class="timeline-desc">Online survey deployed targeting Bitcoin mining ecosystem stakeholders</div></div>
        <div class="timeline-item"><div class="timeline-date">January - February 2026</div><div class="timeline-title">Data Collection</div>
            <div class="timeline-desc">Responses collected from industrial miners, associations, journalists and experts</div></div>
        <div class="timeline-item"><div class="timeline-date">February 2026</div><div class="timeline-title">Validation Phase</div>
            <div class="timeline-desc">Semi-structured interviews conducted to validate findings and clarify ambiguities</div></div>
        <div class="timeline-item"><div class="timeline-date">March 2026</div><div class="timeline-title">Report Publication</div>
            <div class="timeline-desc">Ease to Mine Index released with comprehensive analysis across 19 jurisdictions</div></div>
        """, unsafe_allow_html=True)
    
    with col_pie:
        st.markdown('<p class="section-title">Index Weighting</p>', unsafe_allow_html=True)
        weights = {'Section': ['Energy & Grid', 'Fiscal', 'Legal', 'Permits & Licensing', 'Customs & Tariffs', 'Operating Conditions'], 'Weight': [25, 20, 17.5, 17.5, 15, 5]}
        weight_colors = ['#A7BCF7', '#6287F0', '#0D6FFF', '#1D0DED', '#002060', '#12E09B']
        
        fig_pie = go.Figure(go.Pie(labels=weights['Section'], values=weights['Weight'], hole=0.45, marker=dict(colors=weight_colors),
            textinfo='percent', textposition='outside', textfont=dict(size=11, family="Barlow"), texttemplate='%{percent:.1%}'))
        fig_pie.add_annotation(text="<b>Weight</b><br><span style='font-size:12px'>(%)</span>", x=0.5, y=0.5, font=dict(size=14, color="#1E293B", family="Barlow"), showarrow=False)
        fig_pie.update_layout(height=280, margin=dict(l=20, r=120, t=20, b=20), showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02, font=dict(size=10, family="Barlow")),
            paper_bgcolor='rgba(0,0,0,0)', font=dict(family="Barlow"))
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown('<p class="section-title">Data Quality & Validation</p>', unsafe_allow_html=True)
    col_q1, col_q2, col_q3 = st.columns(3)
    with col_q1:
        st.markdown("""<div class="info-box"><div class="info-box-title">✓ Internal Consistency</div>
            <p>All responses reviewed for logical consistency and cross-validated against publicly available data sources.</p></div>""", unsafe_allow_html=True)
    with col_q2:
        st.markdown("""<div class="info-box"><div class="info-box-title">✓ Bias Detection</div>
            <p>Responses screened for potential reporting bias. Outliers flagged and verified through follow-up interviews.</p></div>""", unsafe_allow_html=True)
    with col_q3:
        st.markdown("""<div class="info-box"><div class="info-box-title">✓ Expert Validation</div>
            <p>Semi-structured interviews with selected respondents to validate findings and clarify country-specific nuances.</p></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<p class="section-title">Geographic Distribution of Respondents</p>', unsafe_allow_html=True)
    
    df_resp = df.copy()
    canada_resp = df_resp[df_resp["Country"].isin(["Alberta (CA)", "Quebec (CA)"])]["Respondents"].sum()
    df_resp = df_resp[~df_resp["Country"].isin(["Alberta (CA)", "Quebec (CA)"])]
    df_resp = pd.concat([df_resp, pd.DataFrame([{"Country": "Canada", "Respondents": canada_resp}])], ignore_index=True)
    df_resp = df_resp[df_resp["Respondents"] > 0].sort_values("Respondents", ascending=False)
    
    col_bar, col_method = st.columns([1.2, 0.8])
    
    with col_bar:
        fig_bar = go.Figure(go.Bar(x=df_resp["Respondents"], y=df_resp["Country"], orientation='h', marker_color='#1E293B',
            text=df_resp["Respondents"], textposition='outside', textfont=dict(size=12, family="Barlow")))
        fig_bar.update_layout(height=480, margin=dict(l=0, r=60, t=20, b=40),
            xaxis=dict(title="Number of Respondents", gridcolor='#E2E8F0'),
            yaxis=dict(title="", autorange="reversed", tickfont=dict(family="Barlow", size=12)),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(family="Barlow"))
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col_method:
        st.markdown("""<div class="info-box" style="height: 100%;">
            <div class="method-box-title">Survey Methodology</div>
            <p>Between December 2025 and February 2026, Hashlabs conducted an online survey targeting stakeholders within the Bitcoin mining ecosystem, including industrial miners, mining associations, industry journalists, and other experts.</p>
            <p style="margin-top: 0.75rem;"><strong>Survey scope:</strong> 5 sections covering legal, fiscal, energy & electricity grids, permitting & licensing, and tariffs & customs procedures. A total of 33 questions combined quantitative metrics with qualitative assessments.</p>
            <p style="margin-top: 0.75rem;"><strong>Data validation:</strong> Responses were reviewed for internal consistency and potential reporting bias. Follow-up semi-structured interviews were conducted with selected respondents to validate findings and clarify country-specific conditions.</p>
            <p style="margin-top: 0.75rem; padding: 0.5rem; background-color: #FEF3C7; border-radius: 4px; font-size: 0.85rem;"><strong>Note:</strong> The Climate Operating Conditions (C.O.C.) section is beyond survey scope and based on internal analysis.</p>
        </div>""", unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown("""<div class="footer">
    <p><strong>Ease to Mine Index (EMI)</strong> - March 2026</p>
    <p>Report Author: <strong>Valentin Rousseau</strong> - <a href="https://x.com/MuadDib_Pill" target="_blank">@MuadDib_Pill</a></p>
    <p>Research by <a href="https://www.e2cpartners.com/insights/global-bitcoin-mining-report-the-ease-to-mine-index" target="_blank">E2C Partners</a> | Survey of 48 industry practitioners across 19 jurisdictions</p>
</div>""", unsafe_allow_html=True)
