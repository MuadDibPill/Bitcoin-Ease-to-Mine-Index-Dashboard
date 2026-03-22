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
    
    [data-testid="stSidebar"] { width: 270px !important; min-width: 270px !important; background-color: #FAFAFA; border-right: 1px solid #E2E8F0; }
    [data-testid="stSidebar"] > div:first-child { width: 270px !important; }
    [data-testid="stSidebar"] .stRadio > div { gap: 0 !important; }
    [data-testid="stSidebar"] .stRadio > div > label { background: transparent !important; border: none !important; padding: 8px 0 !important; cursor: pointer; }
    [data-testid="stSidebar"] .stRadio > div > label:hover { color: #1E8449 !important; }
    [data-testid="stSidebar"] .stRadio > div > label > div:first-child { display: none !important; }
    
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
    page = st.radio("", ["Overview", "Jurisdiction", "Methodology"], label_visibility="collapsed")
    
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
    
    col_map, col_top = st.columns([3, 1])
    
    with col_map:
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
    
    with col_top:
        st.markdown('<p class="section-title-small">Top 3 Jurisdictions</p>', unsafe_allow_html=True)
        min_s, max_s = df[selected_col].min(), df[selected_col].max()
        
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
        
        st.markdown("")
        st.markdown('<p class="section-title-small" style="margin-top: 0.5rem;">Bottom 3 Jurisdictions</p>', unsafe_allow_html=True)
        
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
