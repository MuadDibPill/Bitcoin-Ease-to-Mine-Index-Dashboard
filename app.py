import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(page_title="EMI Dashboard", page_icon="⛏️", layout="wide", initial_sidebar_state="expanded")

# ============================================
# COLOR PALETTE
# ============================================
COLOR_SCALE = [
    [0.00, '#922B21'], [0.07, '#C0392B'], [0.14, '#CD6155'], [0.21, '#DC7633'], [0.28, '#E67E22'],
    [0.35, '#EB984E'], [0.42, '#F5B041'], [0.50, '#F4D03F'], [0.57, '#F7DC6F'], [0.64, '#A9DFBF'],
    [0.71, '#7DCEA0'], [0.78, '#52BE80'], [0.85, '#28B463'], [0.92, '#239B56'], [1.00, '#1E8449']
]

# ============================================
# DETAILED DATA BY SECTION
# ============================================
SECTION_DATA = {
    "Legal": {
        "current_environment": {
            "Oman": "Highly favorable", "UAE": "Highly favorable", "Iceland": "Favorable", "Argentina": "Neutral",
            "Paraguay": "Slightly favorable", "Texas (US)": "Favorable", "Quebec (CA)": "Neutral", "Brazil": "Slightly favorable",
            "Alberta (CA)": "Favorable", "Russia": "Favorable", "Norway": "Neutral", "Ethiopia": "Slightly unfavorable",
            "Kazakhstan": "Slightly favorable", "Finland": "Unfavorable", "Kenya": "Neutral", "DRC": "Neutral",
            "Chile": "Neutral", "Sweden": "Unfavorable", "Australia": "Highly unfavorable"
        },
        "future_outlook": {
            "Oman": "Stable", "UAE": "Stable", "Iceland": "Stable", "Argentina": "Improving",
            "Paraguay": "Neutral", "Texas (US)": "Stable", "Quebec (CA)": "Neutral", "Brazil": "Mixed",
            "Alberta (CA)": "Stable", "Russia": "Worsening", "Norway": "Worsening", "Ethiopia": "Worsening",
            "Kazakhstan": "Improving", "Finland": "Unfavorable", "Kenya": "Neutral", "DRC": "Neutral",
            "Chile": "Neutral", "Sweden": "Unfavorable", "Australia": "Unfavorable"
        }
    },
    "Fiscal": {
        "corporate_tax": {
            "Oman": "0% (free zones)", "UAE": "0% (free zones) / 9%", "Iceland": "20%", "Argentina": "35%",
            "Paraguay": "10%", "Texas (US)": "0% state / 21% federal", "Quebec (CA)": "26.5%", "Brazil": "34%",
            "Alberta (CA)": "23%", "Russia": "20%", "Norway": "22%", "Ethiopia": "30% (exemptions available)",
            "Kazakhstan": "20%", "Finland": "20%", "Kenya": "30%", "DRC": "30%",
            "Chile": "27%", "Sweden": "20.6%", "Australia": "30%"
        },
        "electricity_tax": {
            "Oman": "No", "UAE": "No", "Iceland": "No", "Argentina": "No",
            "Paraguay": "Expected 2026", "Texas (US)": "No", "Quebec (CA)": "Yes ($130/MWh fixed rate)", "Brazil": "No",
            "Alberta (CA)": "Carbon tax only", "Russia": "No", "Norway": "Yes ($14.7/MWh)", "Ethiopia": "No (rate hikes enacted)",
            "Kazakhstan": "Yes ($4/MWh)", "Finland": "Yes (€22.4/MWh)", "Kenya": "No", "DRC": "No",
            "Chile": "No", "Sweden": "Yes ($39.9/MWh)", "Australia": "No"
        },
        "profit_center_shift": {
            "Oman": "Yes", "UAE": "Yes", "Iceland": "Yes", "Argentina": "Yes",
            "Paraguay": "Yes", "Texas (US)": "Yes", "Quebec (CA)": "Yes", "Brazil": "Yes",
            "Alberta (CA)": "Yes", "Russia": "No", "Norway": "Yes", "Ethiopia": "No",
            "Kazakhstan": "Yes", "Finland": "Yes", "Kenya": "No", "DRC": "No",
            "Chile": "Yes", "Sweden": "No", "Australia": "No"
        },
        "subsidies_incentives": {
            "Oman": "Yes (free zones)", "UAE": "Yes (free zones)", "Iceland": "No", "Argentina": "Yes",
            "Paraguay": "Yes (60/90 program)", "Texas (US)": "Yes", "Quebec (CA)": "No", "Brazil": "Yes (REDATA)",
            "Alberta (CA)": "No", "Russia": "Yes (SEZs)", "Norway": "No", "Ethiopia": "Yes (tax breaks)",
            "Kazakhstan": "No", "Finland": "No", "Kenya": "Yes (SEZs)", "DRC": "No",
            "Chile": "No", "Sweden": "No", "Australia": "No"
        },
        "vat_rate": {
            "Oman": "5%", "UAE": "5%", "Iceland": "24%", "Argentina": "27% (refundable)",
            "Paraguay": "10% (exemptable)", "Texas (US)": "0%", "Quebec (CA)": "5% GST (refundable)", "Brazil": "30-35%",
            "Alberta (CA)": "5% GST (refundable)", "Russia": "22%", "Norway": "25%", "Ethiopia": "15% (not enforced)",
            "Kazakhstan": "16%", "Finland": "25.5%", "Kenya": "16%", "DRC": "16%",
            "Chile": "19%", "Sweden": "25%", "Australia": "10% GST"
        },
        "tax_constraint_level": {
            "Oman": "Low", "UAE": "Low", "Iceland": "Neutral", "Argentina": "Moderate",
            "Paraguay": "Neutral", "Texas (US)": "Low", "Quebec (CA)": "Neutral", "Brazil": "High",
            "Alberta (CA)": "Moderate", "Russia": "High", "Norway": "High", "Ethiopia": "Neutral",
            "Kazakhstan": "Moderate", "Finland": "High", "Kenya": "Neutral", "DRC": "High",
            "Chile": "Neutral", "Sweden": "High", "Australia": "High"
        }
    },
    "Permits": {
        "operating_license": {
            "Oman": "Required (>12 months)", "UAE": "Required (<3 months)", "Iceland": "Not required", "Argentina": "Not required (AFIP registration)",
            "Paraguay": "Not required (registration)", "Texas (US)": "Not required", "Quebec (CA)": "Not required (reporting)", "Brazil": "Not required (registration)",
            "Alberta (CA)": "Required (3-6 months)", "Russia": "Required (<3 months)", "Norway": "Not required", "Ethiopia": "Required (<3 months, frozen)",
            "Kazakhstan": "Required (3-5 weeks)", "Finland": "Not required", "Kenya": "Required", "DRC": "Not required",
            "Chile": "Required (6-9 months)", "Sweden": "Not required", "Australia": "Required"
        },
        "construction_permit": {
            "Oman": "6-9 months", "UAE": "<3 months", "Iceland": "6 months", "Argentina": "6 months",
            "Paraguay": "6-9 months", "Texas (US)": "Variable", "Quebec (CA)": "8 months", "Brazil": "3-6 months",
            "Alberta (CA)": "3-6 months", "Russia": "3-12 months", "Norway": "3-6 months", "Ethiopia": "8 months",
            "Kazakhstan": "2-6 months", "Finland": "3-6 months", "Kenya": "3-6 months", "DRC": "3-6 months",
            "Chile": "6-9 months", "Sweden": "3-6 months", "Australia": "9-12 months"
        },
        "eia_burden": {
            "Oman": "Low", "UAE": "Low", "Iceland": "Neutral", "Argentina": "Low",
            "Paraguay": "Neutral", "Texas (US)": "Moderate", "Quebec (CA)": "Moderate", "Brazil": "Burdensome",
            "Alberta (CA)": "Moderate", "Russia": "Neutral", "Norway": "Neutral", "Ethiopia": "Low",
            "Kazakhstan": "Low", "Finland": "Moderate", "Kenya": "Neutral", "DRC": "Low",
            "Chile": "Highly burdensome", "Sweden": "Neutral", "Australia": "Strict"
        },
        "water_permits": {
            "Oman": "Low", "UAE": "Low", "Iceland": "Restrictive", "Argentina": "Restrictive",
            "Paraguay": "Neutral", "Texas (US)": "Low", "Quebec (CA)": "Neutral", "Brazil": "Burdensome",
            "Alberta (CA)": "Moderate", "Russia": "Low", "Norway": "Restrictive", "Ethiopia": "Not required",
            "Kazakhstan": "Low", "Finland": "Neutral", "Kenya": "Neutral", "DRC": "Not required",
            "Chile": "Moderate", "Sweden": "Neutral", "Australia": "Strict"
        },
        "emissions_noise": {
            "Oman": "Low", "UAE": "Insignificant", "Iceland": "Variable", "Argentina": "Variable",
            "Paraguay": "Significant", "Texas (US)": "Heavy", "Quebec (CA)": "Significant", "Brazil": "Modest",
            "Alberta (CA)": "Significant", "Russia": "Moderate", "Norway": "Significant", "Ethiopia": "Insignificant",
            "Kazakhstan": "Neutral", "Finland": "Moderate", "Kenya": "Moderate", "DRC": "None",
            "Chile": "Moderate", "Sweden": "Moderate", "Australia": "Strict"
        },
        "zoning_impact": {
            "Oman": "Low", "UAE": "Neutral", "Iceland": "Moderate", "Argentina": "None",
            "Paraguay": "Neutral", "Texas (US)": "Moderate", "Quebec (CA)": "High", "Brazil": "Low",
            "Alberta (CA)": "High", "Russia": "Neutral", "Norway": "High", "Ethiopia": "Neutral",
            "Kazakhstan": "Neutral", "Finland": "Neutral", "Kenya": "None", "DRC": "None",
            "Chile": "Low", "Sweden": "Neutral", "Australia": "High"
        }
    },
    "Energy": {
        "grid_connection": {
            "Oman": "6-12 months", "UAE": "6-12 months", "Iceland": "18-24 months", "Argentina": "9-15 months",
            "Paraguay": "5-10 months", "Texas (US)": "16-22 months", "Quebec (CA)": "9-15 months", "Brazil": "12 months",
            "Alberta (CA)": ">24 months", "Russia": "12 months", "Norway": "18-24 months", "Ethiopia": "6-12 months (frozen)",
            "Kazakhstan": ">24 months", "Finland": "12-18 months", "Kenya": "N/A (off-grid)", "DRC": "N/A (off-grid)",
            "Chile": ">24 months", "Sweden": "12-18 months", "Australia": "12-18 months"
        },
        "electricity_cost": {
            "Oman": "$38.5-$45.0/MWh", "UAE": "$42.5-$47.5/MWh", "Iceland": "<$35.0/MWh", "Argentina": "$35-$55/MWh (mixed)",
            "Paraguay": "$42.5-$55.0/MWh", "Texas (US)": "$35.0-$47.5/MWh", "Quebec (CA)": "$42.5-$47.5/MWh", "Brazil": "$47.5-$55.0/MWh",
            "Alberta (CA)": "$42.5-$47.5/MWh", "Russia": "$55.0-$65.0/MWh", "Norway": "<$35.0/MWh", "Ethiopia": "$35.0-$42.5/MWh (rising)",
            "Kazakhstan": "$55.0-$65.0/MWh", "Finland": "Median", "Kenya": "<$35.0/MWh (off-grid)", "DRC": "<$35.0/MWh (off-grid)",
            "Chile": "$55.0-$65.0/MWh", "Sweden": "$35.0-$42.5/MWh", "Australia": "$55.0-$65.0/MWh"
        },
        "entry_barriers": {
            "Oman": "Moderate", "UAE": "Moderate", "Iceland": "Moderate", "Argentina": "High",
            "Paraguay": "Neutral", "Texas (US)": "High (ERCOT)", "Quebec (CA)": "High", "Brazil": "Neutral",
            "Alberta (CA)": "High", "Russia": "Moderate", "Norway": "Moderate", "Ethiopia": "High",
            "Kazakhstan": "High", "Finland": "Neutral", "Kenya": "Moderate", "DRC": "High",
            "Chile": "Moderate", "Sweden": "Neutral", "Australia": "High"
        },
        "miner_status": {
            "Oman": "Favorable", "UAE": "Favorable", "Iceland": "Neutral", "Argentina": "Neutral",
            "Paraguay": "Neutral", "Texas (US)": "Neutral", "Quebec (CA)": "Neutral", "Brazil": "Neutral",
            "Alberta (CA)": "Neutral", "Russia": "Unfavorable", "Norway": "Neutral", "Ethiopia": "Unfavorable",
            "Kazakhstan": "Favorable", "Finland": "Neutral", "Kenya": "Neutral", "DRC": "Neutral",
            "Chile": "Neutral", "Sweden": "Neutral", "Australia": "Neutral"
        },
        "demand_response": {
            "Oman": "No", "UAE": "No", "Iceland": "Yes", "Argentina": "No",
            "Paraguay": "No", "Texas (US)": "Yes", "Quebec (CA)": "Yes", "Brazil": "Yes",
            "Alberta (CA)": "Yes", "Russia": "Yes", "Norway": "Yes", "Ethiopia": "No",
            "Kazakhstan": "No", "Finland": "Yes", "Kenya": "No", "DRC": "No",
            "Chile": "High curtailment", "Sweden": "Yes", "Australia": "No"
        }
    },
    "Tariffs": {
        "asic_vat": {
            "Oman": "5%", "UAE": "5%", "Iceland": "24%", "Argentina": "27%",
            "Paraguay": "10%", "Texas (US)": "0%", "Quebec (CA)": "5%", "Brazil": "30-35%",
            "Alberta (CA)": "5%", "Russia": "22%", "Norway": "25%", "Ethiopia": "15%",
            "Kazakhstan": "16%", "Finland": "25.5%", "Kenya": "16%", "DRC": "16%",
            "Chile": "19%", "Sweden": "25%", "Australia": "10%"
        },
        "asic_tariff": {
            "Oman": "0%", "UAE": "0%", "Iceland": "0%", "Argentina": "11%",
            "Paraguay": "4-10%", "Texas (US)": "10-30%", "Quebec (CA)": "0%", "Brazil": "Suspended",
            "Alberta (CA)": "2%", "Russia": "0%", "Norway": "0%", "Ethiopia": "3-15%",
            "Kazakhstan": "0%", "Finland": "0%", "Kenya": "14%", "DRC": "15%+",
            "Chile": "10%", "Sweden": "0%", "Australia": "Variable"
        },
        "import_license": {
            "Oman": "No", "UAE": "Yes", "Iceland": "Yes", "Argentina": "Yes",
            "Paraguay": "No", "Texas (US)": "No", "Quebec (CA)": "No", "Brazil": "No",
            "Alberta (CA)": "No", "Russia": "Yes (FSB)", "Norway": "Yes", "Ethiopia": "Yes",
            "Kazakhstan": "Yes", "Finland": "No", "Kenya": "Yes", "DRC": "Yes",
            "Chile": "No", "Sweden": "No", "Australia": "No"
        },
        "import_process": {
            "Oman": "Highly favorable", "UAE": "Favorable", "Iceland": "Favorable", "Argentina": "Unfavorable",
            "Paraguay": "Marginally favorable", "Texas (US)": "Unfavorable", "Quebec (CA)": "Slightly favorable", "Brazil": "Neutral",
            "Alberta (CA)": "Neutral", "Russia": "Neutral", "Norway": "Favorable", "Ethiopia": "Unfavorable",
            "Kazakhstan": "Neutral", "Finland": "Neutral", "Kenya": "Unfavorable", "DRC": "Highly unfavorable",
            "Chile": "Favorable", "Sweden": "Neutral", "Australia": "Unfavorable"
        },
        "equipment_delay": {
            "Oman": "1-5 months", "UAE": "2-4 months", "Iceland": "2-4 months", "Argentina": "1-5 months",
            "Paraguay": "2-4 months", "Texas (US)": "4-6 months", "Quebec (CA)": "2-5 months", "Brazil": "2-4 months",
            "Alberta (CA)": "2-5 months", "Russia": "2-4 months", "Norway": "2-3 months", "Ethiopia": "3-6 months",
            "Kazakhstan": "2-4 months", "Finland": "2-3 months", "Kenya": "3-6 months", "DRC": "Weeks-months",
            "Chile": ">4 months", "Sweden": "2-3 months", "Australia": "3-6 months"
        },
        "mitigation_effective": {
            "Oman": "N/A", "UAE": "Yes", "Iceland": "Yes", "Argentina": "Yes",
            "Paraguay": "Yes", "Texas (US)": "Partial", "Quebec (CA)": "Yes", "Brazil": "Slightly",
            "Alberta (CA)": "Yes", "Russia": "Slightly", "Norway": "Yes", "Ethiopia": "Slightly",
            "Kazakhstan": "Neutral", "Finland": "Neutral", "Kenya": "Neutral", "DRC": "Yes",
            "Chile": "No", "Sweden": "Yes", "Australia": "No"
        }
    },
    "Climate": {
        "summer_temp": {
            "Oman": ">35°C", "UAE": ">40°C", "Iceland": "<20°C", "Argentina": ">30°C",
            "Paraguay": "≥35°C", "Texas (US)": ">35°C", "Quebec (CA)": "25-30°C", "Brazil": ">30°C",
            "Alberta (CA)": "25-30°C", "Russia": "20-30°C", "Norway": "15-24°C", "Ethiopia": "20-25°C",
            "Kazakhstan": ">34°C", "Finland": "15-25°C", "Kenya": "20-28°C", "DRC": "20-27°C",
            "Chile": "25-35°C", "Sweden": "15-25°C", "Australia": ">35°C"
        },
        "winter_temp": {
            "Oman": "20-25°C", "UAE": "12-30°C", "Iceland": "-8 to 8°C", "Argentina": "5-15°C",
            "Paraguay": "10-20°C", "Texas (US)": "5-15°C", "Quebec (CA)": "-28 to -5°C", "Brazil": "18-25°C",
            "Alberta (CA)": "-25 to -5°C", "Russia": "-20 to 0°C", "Norway": "-5 to 5°C", "Ethiopia": "10-20°C",
            "Kazakhstan": "-29 to 1°C", "Finland": "-16 to 5°C", "Kenya": "13-20°C", "DRC": "15-22°C",
            "Chile": "5-15°C", "Sweden": "-15 to 5°C", "Australia": "10-20°C"
        },
        "diurnal_spread": {
            "Oman": "15.6°C", "UAE": "19.1°C", "Iceland": "13°C", "Argentina": "Wide",
            "Paraguay": "22.1°C", "Texas (US)": "27°C", "Quebec (CA)": "28°C", "Brazil": "13°C",
            "Alberta (CA)": "28°C", "Russia": "Moderate", "Norway": "19°C", "Ethiopia": "17.3°C",
            "Kazakhstan": "Significant", "Finland": "20.6°C", "Kenya": "14.3°C", "DRC": "12°C",
            "Chile": "17.8°C", "Sweden": "21°C", "Australia": "Wide"
        },
        "humidity": {
            "Oman": "63%", "UAE": "40%", "Iceland": "85%", "Argentina": "Variable",
            "Paraguay": "38-84%", "Texas (US)": "58%", "Quebec (CA)": "83.5%", "Brazil": "76-87%",
            "Alberta (CA)": "83.5%", "Russia": "86%", "Norway": "86%", "Ethiopia": "63%",
            "Kazakhstan": "Variable", "Finland": "85-87%", "Kenya": "61%", "DRC": "84%",
            "Chile": "63%", "Sweden": "89%", "Australia": "Variable"
        },
        "altitude": {
            "Oman": "Low", "UAE": "Low", "Iceland": "Low", "Argentina": "Variable",
            "Paraguay": "Low", "Texas (US)": "Low-Moderate", "Quebec (CA)": "Low", "Brazil": "Low",
            "Alberta (CA)": "Moderate", "Russia": "Low", "Norway": "Low", "Ethiopia": "~2,400m",
            "Kazakhstan": "Variable", "Finland": "Low", "Kenya": "~1,900m", "DRC": "~1,200m",
            "Chile": "~2,500m", "Sweden": "Low", "Australia": "Low"
        },
        "dust_exposure": {
            "Oman": "Yes", "UAE": "Significant", "Iceland": "No", "Argentina": "Moderate",
            "Paraguay": "Low", "Texas (US)": "Moderate", "Quebec (CA)": "No", "Brazil": "Low",
            "Alberta (CA)": "Low", "Russia": "Low", "Norway": "No", "Ethiopia": "Low",
            "Kazakhstan": "Yes (coal/salt)", "Finland": "No", "Kenya": "Yes", "DRC": "Low",
            "Chile": "Yes (Atacama)", "Sweden": "No", "Australia": "Yes"
        }
    }
}

# ============================================
# CUSTOM CSS
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Barlow', 'Forma DJR', -apple-system, sans-serif !important; }
    .stApp { background-color: #FFFFFF; }
    [data-testid="stSidebar"] { width: 270px !important; min-width: 270px !important; background-color: #FAFAFA; border-right: 1px solid #E2E8F0; }
    [data-testid="stSidebar"] > div:first-child { width: 270px !important; }
    [data-testid="stSidebar"] .stRadio > div { gap: 0 !important; }
    [data-testid="stSidebar"] .stRadio > div > label { background: transparent !important; border: none !important; padding: 6px 0 !important; cursor: pointer; font-size: 0.9rem; }
    [data-testid="stSidebar"] .stRadio > div > label:hover { color: #1E8449 !important; }
    [data-testid="stSidebar"] .stRadio > div > label > div:first-child { display: none !important; }
    .block-container { padding-top: 2rem !important; }
    h1 { font-weight: 700 !important; font-size: 1.8rem !important; color: #1E293B !important; }
    .section-title { font-size: 1.1rem; font-weight: 600; color: #1E293B; margin-bottom: 1rem; }
    .section-title-small { font-size: 0.9rem; font-weight: 600; color: #1E293B; margin-bottom: 0.6rem; }
    [data-testid="stSelectbox"] > div > div { border: 2px solid #E2E8F0 !important; border-radius: 8px !important; background-color: #F8FAFC !important; }
    .footer { text-align: center; color: #64748B; padding: 2rem; font-size: 0.85rem; border-top: 1px solid #E2E8F0; margin-top: 2rem; }
    .footer a { color: #1E8449; text-decoration: none; }
    .sidebar-author { font-size: 0.8rem; color: #64748B; line-height: 1.5; }
    .sidebar-author a { color: #1E8449; text-decoration: none; }
    .info-box { background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 1rem; font-size: 0.9rem; line-height: 1.6; color: #475569; }
    .info-box-title { font-weight: 600; color: #1E293B; margin-bottom: 0.5rem; }
    .subtitle-text { color: #64748B; font-size: 1rem; margin-bottom: 1.5rem; }
    .methodology-card { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.5rem; text-align: center; min-height: 140px; display: flex; flex-direction: column; justify-content: center; }
    .methodology-card-value { font-size: 2rem; font-weight: 700; color: #1E293B; }
    .methodology-card-title { font-weight: 600; color: #1E293B; font-size: 0.95rem; }
    .methodology-card-desc { font-size: 0.8rem; color: #64748B; min-height: 2.4em; }
    .timeline-item { border-left: 3px solid #002060; padding-left: 1rem; margin-bottom: 1rem; }
    .timeline-date { font-size: 0.8rem; color: #002060; font-weight: 600; }
    .timeline-title { font-weight: 600; color: #1E293B; margin: 0.25rem 0; }
    .timeline-desc { font-size: 0.85rem; color: #64748B; }
    .comparison-vs { font-size: 1.5rem; font-weight: 700; color: #64748B; text-align: center; padding: 1rem; }
    .tldr-box { background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 1rem; font-size: 0.85rem; line-height: 1.5; color: #475569; }
    .tldr-section { margin-bottom: 0.5rem; }
    .tldr-section-title { font-weight: 700; color: #1E293B; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_data():
    return pd.read_csv("data/emi_data.csv")

df = load_data()

ISO_CODES = {
    "Oman": "OMN", "UAE": "ARE", "Iceland": "ISL", "Argentina": "ARG", "Paraguay": "PRY", "Texas (US)": "USA",
    "Quebec (CA)": "CAN", "Brazil": "BRA", "Alberta (CA)": "CAN", "Russia": "RUS", "Norway": "NOR", "Ethiopia": "ETH",
    "Kazakhstan": "KAZ", "Finland": "FIN", "Kenya": "KEN", "DRC": "COD", "Chile": "CHL", "Sweden": "SWE", "Australia": "AUS"
}

# ============================================
# HELPER FUNCTIONS
# ============================================
def get_score_color(score, min_score, max_score):
    if max_score == min_score: ratio = 0.5
    else: ratio = (score - min_score) / (max_score - min_score)
    ratio = max(0.0, min(1.0, ratio))
    color_stops = [(0.00, '#922B21'), (0.07, '#C0392B'), (0.14, '#CD6155'), (0.21, '#DC7633'), (0.28, '#E67E22'),
        (0.35, '#EB984E'), (0.42, '#F5B041'), (0.50, '#F4D03F'), (0.57, '#F7DC6F'), (0.64, '#A9DFBF'),
        (0.71, '#7DCEA0'), (0.78, '#52BE80'), (0.85, '#28B463'), (0.92, '#239B56'), (1.00, '#1E8449')]
    for i in range(len(color_stops) - 1):
        if color_stops[i][0] <= ratio <= color_stops[i + 1][0]:
            t = (ratio - color_stops[i][0]) / (color_stops[i + 1][0] - color_stops[i][0])
            c1, c2 = color_stops[i][1], color_stops[i + 1][1]
            r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
            r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
            return f'#{int(r1 + (r2-r1)*t):02x}{int(g1 + (g2-g1)*t):02x}{int(b1 + (b2-b1)*t):02x}'
    return '#F4D03F'

def get_text_color_for_score(score):
    return "black" if 0.37 <= score <= 0.64 else "white"

def get_categorical_color(value, positive_values, negative_values):
    v = str(value).lower()
    if any(p.lower() in v for p in positive_values): return '#1E8449'
    if any(n.lower() in v for n in negative_values): return '#922B21'
    return '#F4D03F'

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("### Navigation")
    page = st.radio("", ["Overview", "Jurisdiction", "Legal", "Fiscal", "Permits & Licensing", "Energy & Grid", "Tariffs & Import", "Climate", "Methodology"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**Ease to Mine Index (EMI)**")
    st.markdown("March 2026")
    st.markdown("""<p class="sidebar-author">A report by <strong>Valentin Rousseau</strong><br><a href="https://x.com/MuadDib_Pill" target="_blank">@MuadDib_Pill</a><br><br>Provided by <a href="https://www.e2cpartners.com/insights/global-bitcoin-mining-report-the-ease-to-mine-index" target="_blank">E2C Partners</a></p>""", unsafe_allow_html=True)

score_map = {"Overall Index": "Index_Score", "Fiscal": "Fiscal", "Permits & Licensing": "Permit_Licensing", "Legal": "Legal", "Energy & Grid": "Energy_Grid", "Customs & Tariffs": "Tariff_Import", "Operating Conditions": "Operating_Conditions"}

# ============================================
# OVERVIEW PAGE
# ============================================
if page == "Overview":
    st.markdown("# Ease to Mine Index Dashboard")
    st.markdown('<p class="subtitle-text">Comprehensive analysis of Bitcoin mining conditions across 19 jurisdictions</p>', unsafe_allow_html=True)
    
    col_filter, _ = st.columns([1, 3])
    with col_filter:
        score_type = st.selectbox("Select category", list(score_map.keys()), key="main_filter")
    selected_col = score_map[score_type]
    df_sorted = df.sort_values(selected_col, ascending=False)
    
    col_map, col_top = st.columns([3, 1])
    with col_map:
        st.markdown('<p class="section-title">Ease to Mine Index Map</p>', unsafe_allow_html=True)
        df_map = df.copy()
        df_map["ISO"] = df_map["Country"].map(ISO_CODES)
        df_agg = df_map.groupby("ISO").agg({selected_col: "mean", "Country": lambda x: ", ".join(x)}).reset_index()
        df_agg.columns = ["ISO", "Score", "Country"]
        fig_map = go.Figure(go.Choropleth(locations=df_agg["ISO"], z=df_agg["Score"], text=df_agg["Country"],
            colorscale=COLOR_SCALE, marker_line_color='#4B5563', marker_line_width=1,
            colorbar=dict(title=dict(text="Score", side="right", font=dict(size=10)), tickfont=dict(size=9), len=0.5, thickness=10, x=1.02),
            hovertemplate="<b>%{text}</b><br>Score: %{z:.2f}<extra></extra>"))
        fig_map.update_layout(height=520, margin=dict(l=0, r=0, t=5, b=0),
            geo=dict(showframe=False, showcoastlines=True, coastlinecolor="#94A3B8", showland=True, landcolor="#E2E8F0",
                showocean=True, oceancolor="#FFFFFF", showcountries=True, countrycolor="#94A3B8", projection_type='natural earth', bgcolor='rgba(0,0,0,0)'),
            paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_map, use_container_width=True)
    
    with col_top:
        st.markdown('<p class="section-title-small">Top 3 Jurisdictions</p>', unsafe_allow_html=True)
        min_s, max_s = df[selected_col].min(), df[selected_col].max()
        for idx, (_, row) in enumerate(df_sorted.head(3).iterrows()):
            score, color = row[selected_col], get_score_color(row[selected_col], min_s, max_s)
            st.markdown(f"""<div style="background: linear-gradient(90deg, {color}22 0%, transparent 100%); border-left: 4px solid {color}; padding: 10px 12px; margin-bottom: 8px; border-radius: 0 8px 8px 0;">
                <div style="display: flex; justify-content: space-between;"><span style="font-weight: 700; font-size: 0.9rem;">#{idx+1} {row['Country']}</span><span style="font-weight: 700; color: {color};">{score:.2f}</span></div>
                <div style="font-size: 0.7rem; color: #64748B;">Hashrate Q1-26: {row['Hashrate_Q1_26']:.1f} EH/s</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('<p class="section-title-small" style="margin-top: 1rem;">Bottom 3 Jurisdictions</p>', unsafe_allow_html=True)
        for idx, (_, row) in enumerate(df_sorted.tail(3).iterrows()):
            score, color = row[selected_col], get_score_color(row[selected_col], min_s, max_s)
            st.markdown(f"""<div style="background: linear-gradient(90deg, {color}22 0%, transparent 100%); border-left: 4px solid {color}; padding: 10px 12px; margin-bottom: 8px; border-radius: 0 8px 8px 0;">
                <div style="display: flex; justify-content: space-between;"><span style="font-weight: 700; font-size: 0.9rem;">#{17+idx} {row['Country']}</span><span style="font-weight: 700; color: {color};">{score:.2f}</span></div>
                <div style="font-size: 0.7rem; color: #64748B;">Hashrate Q1-26: {row['Hashrate_Q1_26']:.1f} EH/s</div>
            </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<p class="section-title">EMI Ranking</p>', unsafe_allow_html=True)
    col_rf, _ = st.columns([1, 3])
    with col_rf:
        rank_dim = st.selectbox("Select category", list(score_map.keys()), key="rank_filter")
    rank_col = score_map[rank_dim]
    df_rank = df.sort_values(rank_col, ascending=True)
    min_r, max_r = df_rank[rank_col].min(), df_rank[rank_col].max()
    colors_r = [get_score_color(s, min_r, max_r) for s in df_rank[rank_col]]
    
    col_chart, col_text = st.columns([2, 1])
    with col_chart:
        fig_rank = go.Figure(go.Bar(x=df_rank[rank_col], y=df_rank["Country"], orientation='h', marker_color=colors_r,
            text=df_rank[rank_col].round(2), textposition='outside', textfont=dict(size=12)))
        fig_rank.update_layout(height=560, margin=dict(l=0, r=60, t=10, b=40),
            xaxis=dict(range=[0, 1], title=rank_dim + " Score", gridcolor='#E2E8F0'),
            yaxis=dict(tickfont=dict(size=12)), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_rank, use_container_width=True)
    with col_text:
        st.markdown("""<div class="info-box"><div class="info-box-title" style="font-size: 1.1rem;">EMI Description</div>
            <p>The <strong>Ease to Mine Index (EMI)</strong> assesses jurisdiction attractiveness for Bitcoin mining across dimensions: Legal, Fiscal, Permits, Energy, Tariffs, and Climate.</p>
            <p style="margin-top: 0.5rem;"><strong>Coverage:</strong> 19 jurisdictions including Texas (US proxy), Alberta & Québec (Canada).</p></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<p class="section-title">Score Heatmap by Section</p>', unsafe_allow_html=True)
    heatmap_cols = ["Fiscal", "Permit_Licensing", "Legal", "Energy_Grid", "Tariff_Import", "Operating_Conditions"]
    heatmap_labels = ["Fiscal", "Permits", "Legal", "Energy", "Tariffs", "Climate"]
    df_heat = df.sort_values("Index_Score", ascending=False).set_index("Country")[heatmap_cols]
    df_heat.columns = heatmap_labels
    fig_heat = go.Figure(go.Heatmap(z=df_heat.values, x=heatmap_labels, y=df_heat.index, colorscale=COLOR_SCALE,
        hovertemplate="%{y}<br>%{x}: %{z:.2f}<extra></extra>",
        colorbar=dict(title=dict(text="Score", side="right"), len=0.8)))
    annotations = [dict(x=heatmap_labels[j], y=df_heat.index[i], text=f"{df_heat.iloc[i,j]:.2f}", showarrow=False,
        font=dict(color=get_text_color_for_score(df_heat.iloc[i,j]), size=11)) for i in range(len(df_heat)) for j in range(len(heatmap_labels))]
    fig_heat.update_layout(annotations=annotations, height=550, margin=dict(l=0, r=0, t=10, b=40),
        xaxis=dict(tickfont=dict(size=12)), yaxis=dict(autorange="reversed", tickfont=dict(size=12)), plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_heat, use_container_width=True)

# ============================================
# JURISDICTION PAGE (simplified for space)
# ============================================
elif page == "Jurisdiction":
    st.markdown("# Jurisdiction Analysis")
    col_c, _ = st.columns([1, 2])
    with col_c:
        selected = st.selectbox("Select jurisdiction", df["Country"].tolist())
    cdata = df[df["Country"] == selected].iloc[0]
    
    st.markdown("---")
    cols = st.columns(7)
    dims = [("Overall", "Index_Score"), ("Fiscal", "Fiscal"), ("Permits", "Permit_Licensing"), ("Legal", "Legal"), ("Energy", "Energy_Grid"), ("Tariffs", "Tariff_Import"), ("Climate", "Operating_Conditions")]
    for col, (label, cn) in zip(cols, dims):
        score = cdata[cn]
        color = get_score_color(score, df[cn].min(), df[cn].max())
        rank = df[cn].rank(ascending=False)[df["Country"] == selected].values[0]
        with col:
            st.markdown(f"""<div style="text-align: center; padding: 1rem; background: {color}15; border-radius: 8px; border-left: 4px solid {color};">
                <div style="font-size: 1.8rem; font-weight: 700; color: {color};">{score:.2f}</div>
                <div style="font-size: 0.8rem; font-weight: 600;">{label}</div>
                <div style="font-size: 0.7rem; color: #64748B;">#{int(rank)}/19</div></div>""", unsafe_allow_html=True)

# ============================================
# SECTION PAGES - LEGAL
# ============================================
elif page == "Legal":
    st.markdown("# Legal Framework Analysis")
    st.markdown('<p class="subtitle-text">Current legal environment and future outlook by jurisdiction</p>', unsafe_allow_html=True)
    
    legal_data = SECTION_DATA["Legal"]
    countries = list(legal_data["current_environment"].keys())
    
    # Current Environment Map
    st.markdown('<p class="section-title">Current Legal Environment</p>', unsafe_allow_html=True)
    env_map = {"Highly favorable": 1.0, "Favorable": 0.75, "Slightly favorable": 0.6, "Neutral": 0.5, "Slightly unfavorable": 0.4, "Unfavorable": 0.25, "Highly unfavorable": 0.1}
    df_legal = pd.DataFrame({"Country": countries, "Environment": [legal_data["current_environment"][c] for c in countries]})
    df_legal["Score"] = df_legal["Environment"].map(env_map)
    df_legal["ISO"] = df_legal["Country"].map(ISO_CODES)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        fig = go.Figure(go.Choropleth(locations=df_legal["ISO"], z=df_legal["Score"], text=df_legal["Country"] + ": " + df_legal["Environment"],
            colorscale=COLOR_SCALE, marker_line_color='#4B5563',
            colorbar=dict(title="Score", len=0.5, thickness=10), hovertemplate="<b>%{text}</b><extra></extra>"))
        fig.update_layout(height=400, margin=dict(l=0, r=0, t=10, b=0),
            geo=dict(showframe=False, showcoastlines=True, coastlinecolor="#94A3B8", showland=True, landcolor="#E2E8F0", projection_type='natural earth'))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("**Legend**")
        for env, score in env_map.items():
            color = get_score_color(score, 0, 1)
            st.markdown(f"<div style='display: flex; align-items: center; margin-bottom: 4px;'><div style='width: 12px; height: 12px; background: {color}; border-radius: 2px; margin-right: 8px;'></div><span style='font-size: 0.85rem;'>{env}</span></div>", unsafe_allow_html=True)
    
    # Bar chart comparison
    st.markdown("---")
    st.markdown('<p class="section-title">Future Regulatory Outlook</p>', unsafe_allow_html=True)
    outlook_map = {"Stable": 0, "Improving": 1, "Neutral": 0, "Mixed": 0, "Worsening": -1, "Unfavorable": -1}
    df_outlook = pd.DataFrame({"Country": countries, "Outlook": [legal_data["future_outlook"][c] for c in countries]})
    df_outlook["Value"] = df_outlook["Outlook"].map(outlook_map)
    df_outlook = df_outlook.sort_values("Value", ascending=False)
    colors = ['#1E8449' if v > 0 else '#922B21' if v < 0 else '#F4D03F' for v in df_outlook["Value"]]
    
    fig = go.Figure(go.Bar(x=df_outlook["Country"], y=df_outlook["Value"], marker_color=colors, text=df_outlook["Outlook"], textposition='outside'))
    fig.update_layout(height=400, margin=dict(l=0, r=0, t=40, b=100), yaxis=dict(range=[-1.5, 1.5], title="Trend"),
        xaxis=dict(tickangle=45), plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    st.markdown("---")
    st.dataframe(pd.DataFrame({"Country": countries, "Current Environment": [legal_data["current_environment"][c] for c in countries],
        "Future Outlook": [legal_data["future_outlook"][c] for c in countries]}), use_container_width=True, hide_index=True)

# ============================================
# SECTION PAGES - FISCAL
# ============================================
elif page == "Fiscal":
    st.markdown("# Fiscal Framework Analysis")
    st.markdown('<p class="subtitle-text">Tax regime, electricity tax, and incentives by jurisdiction</p>', unsafe_allow_html=True)
    
    fiscal = SECTION_DATA["Fiscal"]
    countries = list(fiscal["corporate_tax"].keys())
    
    # Filter selection
    col_f, _ = st.columns([1, 3])
    with col_f:
        metric = st.selectbox("Select metric", ["Corporate Tax", "Electricity Tax", "Profit Center Shift", "Subsidies/Incentives", "VAT Rate", "Tax Constraint Level"])
    
    metric_map = {"Corporate Tax": "corporate_tax", "Electricity Tax": "electricity_tax", "Profit Center Shift": "profit_center_shift",
        "Subsidies/Incentives": "subsidies_incentives", "VAT Rate": "vat_rate", "Tax Constraint Level": "tax_constraint_level"}
    key = metric_map[metric]
    
    df_fiscal = pd.DataFrame({"Country": countries, "Value": [fiscal[key][c] for c in countries]})
    df_fiscal["ISO"] = df_fiscal["Country"].map(ISO_CODES)
    
    if key == "profit_center_shift":
        # Yes/No map
        st.markdown('<p class="section-title">Ability to Shift Profit Center Abroad</p>', unsafe_allow_html=True)
        df_fiscal["Score"] = df_fiscal["Value"].apply(lambda x: 1 if x == "Yes" else 0)
        colors = ['#1E8449' if v == "Yes" else '#922B21' for v in df_fiscal["Value"]]
        fig = go.Figure(go.Choropleth(locations=df_fiscal["ISO"], z=df_fiscal["Score"], text=df_fiscal["Country"] + ": " + df_fiscal["Value"],
            colorscale=[[0, '#922B21'], [1, '#1E8449']], marker_line_color='#4B5563', showscale=False,
            hovertemplate="<b>%{text}</b><extra></extra>"))
        fig.update_layout(height=450, margin=dict(l=0, r=0, t=10, b=0),
            geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth', showland=True, landcolor="#E2E8F0"))
        st.plotly_chart(fig, use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**✓ Can shift profit center:**")
            for c in [c for c in countries if fiscal[key][c] == "Yes"]:
                st.markdown(f"• {c}")
        with col2:
            st.markdown("**✗ Cannot shift profit center:**")
            for c in [c for c in countries if fiscal[key][c] == "No"]:
                st.markdown(f"• {c}")
    
    elif key == "electricity_tax":
        st.markdown('<p class="section-title">Electricity Tax by Jurisdiction</p>', unsafe_allow_html=True)
        df_fiscal = df_fiscal.sort_values("Value", key=lambda x: x.apply(lambda v: 0 if v == "No" else 1))
        colors = ['#922B21' if "Yes" in v or "$" in v or "€" in v else '#1E8449' for v in df_fiscal["Value"]]
        fig = go.Figure(go.Bar(y=df_fiscal["Country"], x=[1]*len(df_fiscal), orientation='h', marker_color=colors,
            text=df_fiscal["Value"], textposition='inside', textfont=dict(color='white', size=11)))
        fig.update_layout(height=550, margin=dict(l=0, r=0, t=10, b=40), xaxis=dict(showticklabels=False, showgrid=False),
            yaxis=dict(tickfont=dict(size=11)), plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        # Generic bar chart
        st.markdown(f'<p class="section-title">{metric} by Jurisdiction</p>', unsafe_allow_html=True)
        fig = go.Figure(go.Bar(y=df_fiscal["Country"], x=[1]*len(df_fiscal), orientation='h', marker_color='#6287F0',
            text=df_fiscal["Value"], textposition='inside', textfont=dict(color='white', size=11)))
        fig.update_layout(height=550, margin=dict(l=0, r=0, t=10, b=40), xaxis=dict(showticklabels=False, showgrid=False),
            yaxis=dict(tickfont=dict(size=11)), plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.dataframe(pd.DataFrame({c: [fiscal[k][c] for k in fiscal.keys()] for c in countries},
        index=["Corporate Tax", "Electricity Tax", "Profit Center Shift", "Subsidies/Incentives", "VAT Rate", "Tax Constraint"]).T, use_container_width=True)

# ============================================
# SECTION PAGES - PERMITS
# ============================================
elif page == "Permits & Licensing":
    st.markdown("# Permits & Licensing Analysis")
    st.markdown('<p class="subtitle-text">Operating license, construction permits, and regulatory burden by jurisdiction</p>', unsafe_allow_html=True)
    
    permits = SECTION_DATA["Permits"]
    countries = list(permits["operating_license"].keys())
    
    col_f, _ = st.columns([1, 3])
    with col_f:
        metric = st.selectbox("Select metric", ["Operating License", "Construction Permit Timeline", "EIA Burden", "Water Permits", "Emissions/Noise Restrictions", "Zoning Impact"])
    
    metric_map = {"Operating License": "operating_license", "Construction Permit Timeline": "construction_permit", "EIA Burden": "eia_burden",
        "Water Permits": "water_permits", "Emissions/Noise Restrictions": "emissions_noise", "Zoning Impact": "zoning_impact"}
    key = metric_map[metric]
    
    df_permits = pd.DataFrame({"Country": countries, "Value": [permits[key][c] for c in countries]})
    df_permits["ISO"] = df_permits["Country"].map(ISO_CODES)
    
    if key == "operating_license":
        st.markdown('<p class="section-title">Operating License Requirements</p>', unsafe_allow_html=True)
        df_permits["Required"] = df_permits["Value"].apply(lambda x: "Required" if "Required" in x else "Not required")
        colors = ['#922B21' if "Required" in v else '#1E8449' for v in df_permits["Required"]]
        fig = go.Figure(go.Bar(y=df_permits["Country"], x=[1]*len(df_permits), orientation='h', marker_color=colors,
            text=df_permits["Value"], textposition='inside', textfont=dict(color='white', size=10)))
        fig.update_layout(height=550, margin=dict(l=0, r=0, t=10, b=40), xaxis=dict(showticklabels=False, showgrid=False),
            yaxis=dict(tickfont=dict(size=11)), plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    elif key == "construction_permit":
        st.markdown('<p class="section-title">Construction Permit Timeline</p>', unsafe_allow_html=True)
        # Extract months for sorting
        def extract_months(val):
            if ">" in val: return 24
            if "<" in val: return 2
            nums = [int(s) for s in val.replace("-", " ").split() if s.isdigit()]
            return max(nums) if nums else 6
        df_permits["Months"] = df_permits["Value"].apply(extract_months)
        df_permits = df_permits.sort_values("Months")
        colors = [get_score_color(1 - m/24, 0, 1) for m in df_permits["Months"]]
        fig = go.Figure(go.Bar(y=df_permits["Country"], x=df_permits["Months"], orientation='h', marker_color=colors,
            text=df_permits["Value"], textposition='outside'))
        fig.update_layout(height=550, margin=dict(l=0, r=80, t=10, b=40), xaxis=dict(title="Months", gridcolor='#E2E8F0'),
            yaxis=dict(tickfont=dict(size=11)), plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        burden_map = {"Low": 0.8, "Neutral": 0.5, "Moderate": 0.4, "Burdensome": 0.25, "Highly burdensome": 0.1, "Strict": 0.1,
            "None": 1.0, "Not required": 1.0, "Insignificant": 0.9, "Variable": 0.5, "Heavy": 0.15, "High": 0.2, "Restrictive": 0.3, "Significant": 0.3, "Modest": 0.6}
        df_permits["Score"] = df_permits["Value"].apply(lambda x: next((v for k, v in burden_map.items() if k.lower() in x.lower()), 0.5))
        df_permits = df_permits.sort_values("Score", ascending=False)
        colors = [get_score_color(s, 0, 1) for s in df_permits["Score"]]
        fig = go.Figure(go.Bar(y=df_permits["Country"], x=df_permits["Score"], orientation='h', marker_color=colors,
            text=df_permits["Value"], textposition='outside'))
        fig.update_layout(height=550, margin=dict(l=0, r=100, t=10, b=40), xaxis=dict(range=[0, 1.1], title="Favorability", gridcolor='#E2E8F0'),
            yaxis=dict(tickfont=dict(size=11)), plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.dataframe(pd.DataFrame({c: [permits[k][c] for k in permits.keys()] for c in countries},
        index=["Operating License", "Construction Permit", "EIA Burden", "Water Permits", "Emissions/Noise", "Zoning Impact"]).T, use_container_width=True)

# ============================================
# SECTION PAGES - ENERGY
# ============================================
elif page == "Energy & Grid":
    st.markdown("# Energy & Grid Analysis")
    st.markdown('<p class="subtitle-text">Grid connection, electricity costs, and market access by jurisdiction</p>', unsafe_allow_html=True)
    
    energy = SECTION_DATA["Energy"]
    countries = list(energy["grid_connection"].keys())
    
    col_f, _ = st.columns([1, 3])
    with col_f:
        metric = st.selectbox("Select metric", ["Grid Connection Timeline", "Electricity Cost", "Entry Barriers", "Miner Grid Status", "Demand Response Access"])
    
    metric_map = {"Grid Connection Timeline": "grid_connection", "Electricity Cost": "electricity_cost", "Entry Barriers": "entry_barriers",
        "Miner Grid Status": "miner_status", "Demand Response Access": "demand_response"}
    key = metric_map[metric]
    
    df_energy = pd.DataFrame({"Country": countries, "Value": [energy[key][c] for c in countries]})
    df_energy["ISO"] = df_energy["Country"].map(ISO_CODES)
    
    if key == "grid_connection":
        st.markdown('<p class="section-title">Grid Connection Lead Time</p>', unsafe_allow_html=True)
        def extract_months(val):
            if "N/A" in val: return 0
            if ">" in val: return 30
            nums = [int(s) for s in val.replace("-", " ").split() if s.isdigit()]
            return max(nums) if nums else 12
        df_energy["Months"] = df_energy["Value"].apply(extract_months)
        df_energy = df_energy.sort_values("Months")
        colors = [get_score_color(1 - m/30, 0, 1) for m in df_energy["Months"]]
        fig = go.Figure(go.Bar(y=df_energy["Country"], x=df_energy["Months"], orientation='h', marker_color=colors,
            text=df_energy["Value"], textposition='outside'))
        fig.update_layout(height=550, margin=dict(l=0, r=100, t=10, b=40), xaxis=dict(title="Months", gridcolor='#E2E8F0'),
            yaxis=dict(tickfont=dict(size=11)), plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    elif key == "electricity_cost":
        st.markdown('<p class="section-title">Electricity Cost Range</p>', unsafe_allow_html=True)
        def extract_cost(val):
            if "<$35" in val: return 30
            if ">$55" in val or "$55" in val: return 60
            nums = [float(s.replace("$", "")) for s in val.split() if "$" in s or s.replace(".", "").isdigit()]
            return sum(nums)/len(nums) if nums else 45
        df_energy["Cost"] = df_energy["Value"].apply(extract_cost)
        df_energy = df_energy.sort_values("Cost")
        colors = [get_score_color(1 - (c-25)/45, 0, 1) for c in df_energy["Cost"]]
        fig = go.Figure(go.Bar(y=df_energy["Country"], x=df_energy["Cost"], orientation='h', marker_color=colors,
            text=df_energy["Value"], textposition='outside'))
        fig.update_layout(height=550, margin=dict(l=0, r=120, t=10, b=40), xaxis=dict(title="$/MWh (approx)", gridcolor='#E2E8F0'),
            yaxis=dict(tickfont=dict(size=11)), plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        status_map = {"Favorable": 0.8, "Neutral": 0.5, "Unfavorable": 0.2, "High": 0.2, "Moderate": 0.5, "Yes": 0.8, "No": 0.2, "High (ERCOT)": 0.2, "High curtailment": 0.3}
        df_energy["Score"] = df_energy["Value"].apply(lambda x: status_map.get(x, 0.5))
        df_energy = df_energy.sort_values("Score", ascending=False)
        colors = [get_score_color(s, 0, 1) for s in df_energy["Score"]]
        fig = go.Figure(go.Bar(y=df_energy["Country"], x=df_energy["Score"], orientation='h', marker_color=colors,
            text=df_energy["Value"], textposition='outside'))
        fig.update_layout(height=550, margin=dict(l=0, r=80, t=10, b=40), xaxis=dict(range=[0, 1], title="Favorability", gridcolor='#E2E8F0'),
            yaxis=dict(tickfont=dict(size=11)), plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.dataframe(pd.DataFrame({c: [energy[k][c] for k in energy.keys()] for c in countries},
        index=["Grid Connection", "Electricity Cost", "Entry Barriers", "Miner Status", "Demand Response"]).T, use_container_width=True)

# ============================================
# SECTION PAGES - TARIFFS
# ============================================
elif page == "Tariffs & Import":
    st.markdown("# Tariffs & Import Analysis")
    st.markdown('<p class="subtitle-text">VAT, tariffs, and import process by jurisdiction</p>', unsafe_allow_html=True)
    
    tariffs = SECTION_DATA["Tariffs"]
    countries = list(tariffs["asic_vat"].keys())
    
    col_f, _ = st.columns([1, 3])
    with col_f:
        metric = st.selectbox("Select metric", ["ASIC VAT Rate", "ASIC Tariff", "Import License Required", "Import Process Quality", "Equipment Delay", "Mitigation Effectiveness"])
    
    metric_map = {"ASIC VAT Rate": "asic_vat", "ASIC Tariff": "asic_tariff", "Import License Required": "import_license",
        "Import Process Quality": "import_process", "Equipment Delay": "equipment_delay", "Mitigation Effectiveness": "mitigation_effective"}
    key = metric_map[metric]
    
    df_tariffs = pd.DataFrame({"Country": countries, "Value": [tariffs[key][c] for c in countries]})
    df_tariffs["ISO"] = df_tariffs["Country"].map(ISO_CODES)
    
    if key in ["asic_vat", "asic_tariff"]:
        st.markdown(f'<p class="section-title">{metric}</p>', unsafe_allow_html=True)
        def extract_pct(val):
            nums = [float(s.replace("%", "")) for s in val.split() if "%" in s]
            return max(nums) if nums else 0
        df_tariffs["Pct"] = df_tariffs["Value"].apply(extract_pct)
        df_tariffs = df_tariffs.sort_values("Pct")
        colors = [get_score_color(1 - p/35, 0, 1) for p in df_tariffs["Pct"]]
        fig = go.Figure(go.Bar(y=df_tariffs["Country"], x=df_tariffs["Pct"], orientation='h', marker_color=colors,
            text=df_tariffs["Value"], textposition='outside'))
        fig.update_layout(height=550, margin=dict(l=0, r=80, t=10, b=40), xaxis=dict(title="Rate (%)", gridcolor='#E2E8F0'),
            yaxis=dict(tickfont=dict(size=11)), plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    elif key == "import_license":
        st.markdown('<p class="section-title">Import License Requirement</p>', unsafe_allow_html=True)
        df_tariffs["Required"] = df_tariffs["Value"].apply(lambda x: 1 if x == "Yes" else 0)
        colors = ['#922B21' if v == "Yes" else '#1E8449' for v in df_tariffs["Value"]]
        fig = go.Figure(go.Choropleth(locations=df_tariffs["ISO"], z=df_tariffs["Required"], text=df_tariffs["Country"] + ": " + df_tariffs["Value"],
            colorscale=[[0, '#1E8449'], [1, '#922B21']], marker_line_color='#4B5563', showscale=False))
        fig.update_layout(height=450, margin=dict(l=0, r=0, t=10, b=0),
            geo=dict(showframe=False, projection_type='natural earth', showland=True, landcolor="#E2E8F0"))
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        process_map = {"Highly favorable": 1.0, "Favorable": 0.8, "Marginally favorable": 0.65, "Slightly favorable": 0.6, "Neutral": 0.5,
            "Unfavorable": 0.25, "Highly unfavorable": 0.1, "Yes": 0.8, "Partial": 0.5, "Slightly": 0.4, "No": 0.2, "N/A": 0.5}
        df_tariffs["Score"] = df_tariffs["Value"].apply(lambda x: next((v for k, v in process_map.items() if k.lower() in x.lower()), 0.5))
        df_tariffs = df_tariffs.sort_values("Score", ascending=False)
        colors = [get_score_color(s, 0, 1) for s in df_tariffs["Score"]]
        fig = go.Figure(go.Bar(y=df_tariffs["Country"], x=df_tariffs["Score"], orientation='h', marker_color=colors,
            text=df_tariffs["Value"], textposition='outside'))
        fig.update_layout(height=550, margin=dict(l=0, r=100, t=10, b=40), xaxis=dict(range=[0, 1.1], title="Favorability", gridcolor='#E2E8F0'),
            yaxis=dict(tickfont=dict(size=11)), plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.dataframe(pd.DataFrame({c: [tariffs[k][c] for k in tariffs.keys()] for c in countries},
        index=["ASIC VAT", "ASIC Tariff", "Import License", "Import Process", "Equipment Delay", "Mitigation"]).T, use_container_width=True)

# ============================================
# SECTION PAGES - CLIMATE
# ============================================
elif page == "Climate":
    st.markdown("# Climate Operating Conditions")
    st.markdown('<p class="subtitle-text">Temperature, humidity, altitude, and environmental factors by jurisdiction</p>', unsafe_allow_html=True)
    
    climate = SECTION_DATA["Climate"]
    countries = list(climate["summer_temp"].keys())
    
    col_f, _ = st.columns([1, 3])
    with col_f:
        metric = st.selectbox("Select metric", ["Summer Temperature", "Winter Temperature", "Diurnal Spread", "Humidity", "Altitude", "Dust Exposure"])
    
    metric_map = {"Summer Temperature": "summer_temp", "Winter Temperature": "winter_temp", "Diurnal Spread": "diurnal_spread",
        "Humidity": "humidity", "Altitude": "altitude", "Dust Exposure": "dust_exposure"}
    key = metric_map[metric]
    
    df_climate = pd.DataFrame({"Country": countries, "Value": [climate[key][c] for c in countries]})
    df_climate["ISO"] = df_climate["Country"].map(ISO_CODES)
    
    if key == "dust_exposure":
        st.markdown('<p class="section-title">Dust Exposure Risk</p>', unsafe_allow_html=True)
        df_climate["HasDust"] = df_climate["Value"].apply(lambda x: 1 if x in ["Yes", "Significant"] else 0.5 if x == "Moderate" else 0)
        colors = ['#922B21' if v in ["Yes", "Significant"] else '#F4D03F' if v == "Moderate" else '#1E8449' for v in df_climate["Value"]]
        fig = go.Figure(go.Choropleth(locations=df_climate["ISO"], z=df_climate["HasDust"], text=df_climate["Country"] + ": " + df_climate["Value"],
            colorscale=[[0, '#1E8449'], [0.5, '#F4D03F'], [1, '#922B21']], marker_line_color='#4B5563', showscale=False))
        fig.update_layout(height=450, margin=dict(l=0, r=0, t=10, b=0),
            geo=dict(showframe=False, projection_type='natural earth', showland=True, landcolor="#E2E8F0"))
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.markdown(f'<p class="section-title">{metric}</p>', unsafe_allow_html=True)
        fig = go.Figure(go.Bar(y=df_climate["Country"], x=[1]*len(df_climate), orientation='h', marker_color='#6287F0',
            text=df_climate["Value"], textposition='inside', textfont=dict(color='white', size=10)))
        fig.update_layout(height=550, margin=dict(l=0, r=0, t=10, b=40), xaxis=dict(showticklabels=False, showgrid=False),
            yaxis=dict(tickfont=dict(size=11)), plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.dataframe(pd.DataFrame({c: [climate[k][c] for k in climate.keys()] for c in countries},
        index=["Summer Temp", "Winter Temp", "Diurnal Spread", "Humidity", "Altitude", "Dust Exposure"]).T, use_container_width=True)

# ============================================
# METHODOLOGY PAGE
# ============================================
elif page == "Methodology":
    st.markdown("# Methodology")
    st.markdown("How we built the Ease to Mine Index")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class="methodology-card"><div class="methodology-card-value">48</div><div class="methodology-card-title">Respondents</div><div class="methodology-card-desc">Industrial Miners, Associations, Experts</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="methodology-card"><div class="methodology-card-value">55</div><div class="methodology-card-title">Responses</div><div class="methodology-card-desc">Total survey submissions</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="methodology-card"><div class="methodology-card-value">19</div><div class="methodology-card-title">Jurisdictions</div><div class="methodology-card-desc">Including Québec & Alberta</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="methodology-card"><div class="methodology-card-value">33</div><div class="methodology-card-title">Questions</div><div class="methodology-card-desc">Across 5 survey sections</div></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    weights = {'Section': ['Energy & Grid', 'Fiscal', 'Legal', 'Permits & Licensing', 'Customs & Tariffs', 'Operating Conditions'], 'Weight': [25, 20, 17.5, 17.5, 15, 5]}
    fig = go.Figure(go.Pie(labels=weights['Section'], values=weights['Weight'], hole=0.45,
        marker=dict(colors=['#A7BCF7', '#6287F0', '#0D6FFF', '#1D0DED', '#002060', '#12E09B']),
        texttemplate='%{percent:.1%}', textposition='outside'))
    fig.add_annotation(text="<b>Weight</b>", x=0.5, y=0.5, showarrow=False, font=dict(size=14))
    fig.update_layout(height=300, margin=dict(l=20, r=120, t=20, b=20), legend=dict(x=1.02, y=0.5))
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# FOOTER
# ============================================
st.markdown("""<div class="footer"><p><strong>Ease to Mine Index (EMI)</strong> - March 2026</p>
    <p>Report Author: <strong>Valentin Rousseau</strong> - <a href="https://x.com/MuadDib_Pill">@MuadDib_Pill</a></p>
    <p>Research by <a href="https://www.e2cpartners.com/insights/global-bitcoin-mining-report-the-ease-to-mine-index">E2C Partners</a></p></div>""", unsafe_allow_html=True)
