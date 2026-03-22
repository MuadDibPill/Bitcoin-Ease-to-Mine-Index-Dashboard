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
# COUNTRY SUMMARIES
# ============================================
COUNTRY_SUMMARIES = {
    "Oman": "Oman leads the EMI ranking (0.75) with a highly favorable environment. State supports mining through direct ownership of facilities in the Salalah Free Zone and Oman Vision 2040. Free zones offer 0% corporate tax and no import tariffs. Grid connection in 6-12 months with electricity at $38.5-$45.0/MWh.",
    "UAE": "UAE ranks second (0.71) with strong government support through VARA regulation. Free zones provide 0% corporate tax, 5% VAT only. Grid connection in 6-12 months with electricity at $42.5-$47.5/MWh. Construction permits secured in under 3 months.",
    "Iceland": "Iceland scores 0.60 with favorable conditions. Climate highly favorable with abundant hydro and geothermal. Electricity below $35.0/MWh. Political opposition growing with zoning laws incoming. Grid connection 18-24 months.",
    "Argentina": "Argentina scores 0.57 with moderately favorable conditions. Off-grid flare gas below $35.0/MWh in Vaca Muerta. Grid connection in 9-15 months. 27% VAT (refundable), 11% tariff.",
    "Paraguay": "Paraguay scores 0.57, powered by Itaipu Dam hydropower. Electricity at $42.5-$55.0/MWh via 5-year PPAs. Grid connection in 5-10 months. Tariff increases expected in 2026.",
    "Texas (US)": "Texas scores 0.56 with favorable legal and fiscal frameworks. ERCOT market with electricity at $35.0-$47.5/MWh. Grid connection now takes 16-22 months due to AI competition.",
    "Quebec (CA)": "Quebec scores 0.55 with Hydro-Quebec oversight. Electricity at $42.5-$47.5/MWh. Grid connection in 9-15 months. Fixed rate of $130/MWh for new crypto operations.",
    "Brazil": "Brazil scores 0.54 with improving conditions. Electricity at $47.5-55.0/MWh. Grid connection in 12 months. REDATA incentive for low-emission data centers.",
    "Alberta (CA)": "Alberta scores 0.53 with deregulated market. Electricity at $42.5-$47.5/MWh. Grid connection exceeds 24 months. Carbon tax applies.",
    "Russia": "Russia scores 0.51 transitioning from favorable. Mining restricted to Russian entities since 2024. Electricity at $55.0-$65.0/MWh. Regional bans increasing.",
    "Norway": "Norway scores 0.51 with deteriorating conditions. Electricity below $35.0/MWh but electricity tax at $14.7/MWh. Grid connection 18-24 months. Political opposition growing.",
    "Ethiopia": "Ethiopia scores 0.51, shifting from favorable. New permits suspended since February 2024. Electricity rising from $22.0/MWh to $65.0/MWh by 2028.",
    "Kazakhstan": "Kazakhstan scores 0.47 with improving framework post-crackdown. Electricity at $55.0-$65.0/MWh. Grid connection exceeds 24 months. Electricity tax at $4.0/MWh.",
    "Finland": "Finland scores 0.47 with restrictive framework. Electricity tax increased to €22.4/MWh (heat reuse exempt). VAT reclaim issues for miners.",
    "Kenya": "Kenya scores 0.47 with limited infrastructure. Off-grid below $35.0/MWh but scale limited. 16% VAT, 14% tariff.",
    "DRC": "DRC scores 0.46 with significant challenges. Off-grid power below $35.0/MWh but infrastructure unreliable. Political instability a key concern.",
    "Chile": "Chile scores 0.44 with critical barriers. Grid connection exceeds 24 months. Electricity at $55.0-$65.0/MWh. EIA highly burdensome.",
    "Sweden": "Sweden scores 0.45, hostile to mining. Electricity tax at $39.9/MWh. Mining excluded from VAT reclaim.",
    "Australia": "Australia scores 0.28, lowest in index. Stringent environmental regulations. Electricity at $55.0-$65.0/MWh. 30% corporate tax."
}

# ============================================
# TLDR DATA
# ============================================
COUNTRY_TLDR = {
    "Oman": {
        "Legal": "Highly favorable • Future: stable",
        "Fiscal": "0% corporate tax in free zones • No electricity tax • Low constraint to mitigate taxes",
        "Permits": "License required (>12 months) • Construction 6-9 months • Low EIA burden",
        "Energy": "Grid connection 6-12 months • Power cost $38.5-$45.0/MWh • Moderate entry barriers",
        "Tariffs": "5% VAT • No tariff • Highly favorable import process",
        "Climate": "Summer >35°C • Low diurnal spread (15.6°C) • Dust exposure"
    },
    "UAE": {
        "Legal": "Highly favorable • Future: stable • State ownership of mining facilities",
        "Fiscal": "0% corporate in free zones • 5% VAT only • No electricity tax",
        "Permits": "License <3 months • Construction <3 months • Low EIA burden",
        "Energy": "Grid connection 6-12 months • Power cost $42.5-$47.5/MWh",
        "Tariffs": "5% VAT • No tariff • Favorable import process",
        "Climate": "Summer >40°C • Significant dust"
    },
    "Australia": {
        "Legal": "Highly unfavorable • Future: unfavorable • Stringent environmental regulations",
        "Fiscal": "30% CIT • Cannot shift profit center • No incentives",
        "Permits": "License required • Construction 9-12 months • EIA strict • Zoning: highly restrictive",
        "Energy": "Grid connection 12-18 months • Power cost $55.0-$65.0/MWh • High barriers",
        "Tariffs": "10% GST • Import process unfavorable",
        "Climate": "High temps • PUE <1.4 mandated"
    }
}

# Complete TLDR for other countries (abbreviated for space)
for c in ["Iceland", "Argentina", "Paraguay", "Texas (US)", "Quebec (CA)", "Brazil", "Alberta (CA)", 
          "Russia", "Norway", "Ethiopia", "Kazakhstan", "Finland", "Kenya", "DRC", "Chile", "Sweden"]:
    if c not in COUNTRY_TLDR:
        COUNTRY_TLDR[c] = {"Legal": "See detailed analysis", "Fiscal": "See detailed analysis", 
                          "Permits": "See detailed analysis", "Energy": "See detailed analysis",
                          "Tariffs": "See detailed analysis", "Climate": "See detailed analysis"}

# ============================================
# HELPER FUNCTIONS
# ============================================
def get_score_color(score, min_score=0, max_score=1):
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
    page = st.radio("", ["Overview", "Jurisdiction", "Legal", "Methodology"], label_visibility="collapsed")
    
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
            colorbar=dict(title=dict(text="Score", side="right", font=dict(family="Barlow", size=10)), 
                         tickfont=dict(family="Barlow", size=9), len=0.5, thickness=10, x=1.02),
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
                    <div><span style="font-weight: 700; color: #1E293B; font-size: 0.9rem;">#{rank} {row['Country']}</span></div>
                    <div style="font-weight: 700; font-size: 1rem; color: {color};">{score:.2f}</div>
                </div>
                <div style="font-size: 0.7rem; color: #64748B; margin-top: 2px;">Hashrate Q1-26: {row['Hashrate_Q1_26']:.1f} EH/s</div>
            </div>""", unsafe_allow_html=True)
        
        st.markdown('<p class="section-title-small" style="margin-top: 1rem;">Bottom 3 Jurisdictions</p>', unsafe_allow_html=True)
        
        for idx, (i, row) in enumerate(df_sorted.tail(3).iterrows()):
            rank, score = 17 + idx, row[selected_col]
            color = get_score_color(score, min_s, max_s)
            st.markdown(f"""<div style="background: linear-gradient(90deg, {color}22 0%, transparent 100%); border-left: 4px solid {color}; padding: 10px 12px; margin-bottom: 8px; border-radius: 0 8px 8px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div><span style="font-weight: 700; color: #1E293B; font-size: 0.9rem;">#{rank} {row['Country']}</span></div>
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
            <p>The <strong>Ease to Mine Index (EMI)</strong> assesses jurisdiction attractiveness for Bitcoin mining across 6 dimensions:</p>
            <ul style="margin: 0.5rem 0; padding-left: 1.2rem;"><li>Legal framework</li><li>Fiscal environment</li><li>Permits & Licensing</li><li>Energy & Grid access</li><li>Tariffs & Import</li><li>Climate conditions</li></ul>
            <p style="margin-top: 0.75rem;"><strong>Coverage:</strong> 19 jurisdictions</p>
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
        colorbar=dict(title=dict(text="Score", side="right", font=dict(family="Barlow")), tickfont=dict(family="Barlow"), len=0.5, thickness=10)))
    annotations = [dict(x=heatmap_labels[j], y=heatmap_data.index[i], text=f"{heatmap_data.iloc[i, j]:.2f}", showarrow=False,
        font=dict(color=get_text_color_for_score(heatmap_data.iloc[i, j]), size=12, family="Barlow"))
        for i in range(len(heatmap_data.index)) for j in range(len(heatmap_labels))]
    fig_heat.update_layout(annotations=annotations, height=550, margin=dict(l=0, r=0, t=10, b=40),
        xaxis=dict(title="", tickangle=0, side="bottom", tickfont=dict(family="Barlow", size=13)),
        yaxis=dict(title="", autorange="reversed", tickfont=dict(family="Barlow", size=13)),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(family="Barlow"))
    st.plotly_chart(fig_heat, use_container_width=True)

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
    
    # TLDR Comparison
    tldr1 = COUNTRY_TLDR.get(country1, {})
    tldr2 = COUNTRY_TLDR.get(country2, {})
    
    col_tldr1, col_tldr2 = st.columns(2)
    
    with col_tldr1:
        st.markdown(f"""<div class="tldr-box">
            <div style="font-weight: 700; color: #1E293B; font-size: 1rem; margin-bottom: 0.75rem; border-bottom: 2px solid #6287F0; padding-bottom: 0.5rem;">{country1}</div>
            {"".join([f'<div class="tldr-section"><span class="tldr-section-title">{k}:</span> <span class="tldr-item">{v}</span></div>' for k, v in tldr1.items()])}
        </div>""", unsafe_allow_html=True)
    
    with col_tldr2:
        st.markdown(f"""<div class="tldr-box">
            <div style="font-weight: 700; color: #1E293B; font-size: 1rem; margin-bottom: 0.75rem; border-bottom: 2px solid #1D0DED; padding-bottom: 0.5rem;">{country2}</div>
            {"".join([f'<div class="tldr-section"><span class="tldr-section-title">{k}:</span> <span class="tldr-item">{v}</span></div>' for k, v in tldr2.items()])}
        </div>""", unsafe_allow_html=True)

# ============================================
# LEGAL PAGE - NEW DETAILED SECTION
# ============================================
elif page == "Legal":
    st.markdown("# Legal Framework Analysis")
    st.markdown('<p class="subtitle-text">Survey Questions 18 & 19 — Current regulatory environment and future expectations</p>', unsafe_allow_html=True)
    
    # Create DataFrame from LEGAL_SCORES
    legal_df = pd.DataFrame([
        {"Country": c, "Q18_Current": v["Q18"], "Q19_Future": v["Q19"], "Evolution": v["Q19"] - v["Q18"]}
        for c, v in LEGAL_SCORES.items()
    ])
    legal_df["ISO"] = legal_df["Country"].map(ISO_CODES)
    
    # Filter selector
    col_filter, _ = st.columns([1, 3])
    with col_filter:
        question_filter = st.selectbox(
            "Select question", 
            ["Q18: Current regulatory environment", "Q19: Future regulatory outlook"],
            key="legal_filter"
        )
    
    selected_q = "Q18_Current" if "Q18" in question_filter else "Q19_Future"
    q_title = "Current Regulatory Environment" if "Q18" in question_filter else "Expected Regulatory Evolution"
    q_full = "18. How would you characterize the overall regulatory environment for mining in your country?" if "Q18" in question_filter else "19. How do you expect the regulatory framework to evolve in the coming years?"
    
    st.markdown("---")
    
    # MAP
    st.markdown(f'<p class="section-title">{q_title}</p>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #64748B; font-size: 0.85rem; margin-bottom: 1rem;">{q_full}</p>', unsafe_allow_html=True)
    
    # Aggregate for countries with same ISO (Canada)
    map_df = legal_df.copy()
    map_agg = map_df.groupby("ISO").agg({selected_q: "mean", "Country": lambda x: ", ".join(x)}).reset_index()
    map_agg.columns = ["ISO", "Score", "Countries"]
    
    col_map, col_legend = st.columns([3, 1])
    
    with col_map:
        fig_map = go.Figure(go.Choropleth(
            locations=map_agg["ISO"],
            z=map_agg["Score"],
            text=map_agg["Countries"],
            colorscale=COLOR_SCALE,
            autocolorscale=False,
            marker_line_color='#4B5563',
            marker_line_width=1,
            zmin=0, zmax=1,
            colorbar=dict(
                title=dict(text="Score", side="right", font=dict(family="Barlow", size=10)),
                tickfont=dict(family="Barlow", size=9),
                len=0.5, thickness=10, x=1.02,
                tickvals=[0, 0.25, 0.5, 0.75, 1],
                ticktext=["0.00", "0.25", "0.50", "0.75", "1.00"]
            ),
            hovertemplate="<b>%{text}</b><br>Score: %{z:.2f}<extra></extra>"
        ))
        fig_map.update_layout(
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
        st.plotly_chart(fig_map, use_container_width=True)
    
    with col_legend:
        st.markdown("**Score Interpretation**")
        interpretations = [
            (1.0, "Highly Favorable", "#1E8449"),
            (0.75, "Favorable", "#28B463"),
            (0.5, "Neutral", "#F4D03F"),
            (0.25, "Unfavorable", "#E67E22"),
            (0.0, "Highly Unfavorable", "#922B21")
        ]
        for score, label, color in interpretations:
            st.markdown(f"""<div style="display: flex; align-items: center; margin-bottom: 8px;">
                <div style="width: 20px; height: 20px; background: {color}; border-radius: 4px; margin-right: 10px;"></div>
                <div><span style="font-weight: 600;">{score:.2f}</span> — {label}</div>
            </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # EVOLUTION CHART
    st.markdown('<p class="section-title">Regulatory Evolution: Current vs Future Expectations</p>', unsafe_allow_html=True)
    st.markdown('<p style="color: #64748B; font-size: 0.85rem; margin-bottom: 1rem;">Change between Q18 (current) and Q19 (future outlook) — Positive = Improving, Negative = Worsening</p>', unsafe_allow_html=True)
    
    # Sort by evolution
    evol_df = legal_df.sort_values("Evolution", ascending=True)
    
    # Create grouped bar chart with evolution
    fig_evol = go.Figure()
    
    # Add Q18 bars
    fig_evol.add_trace(go.Bar(
        name='Q18: Current',
        y=evol_df["Country"],
        x=evol_df["Q18_Current"],
        orientation='h',
        marker_color='#6287F0',
        text=evol_df["Q18_Current"].round(2),
        textposition='inside',
        textfont=dict(color='white', size=10)
    ))
    
    # Add Q19 bars
    fig_evol.add_trace(go.Bar(
        name='Q19: Future',
        y=evol_df["Country"],
        x=evol_df["Q19_Future"],
        orientation='h',
        marker_color='#1D0DED',
        text=evol_df["Q19_Future"].round(2),
        textposition='inside',
        textfont=dict(color='white', size=10)
    ))
    
    fig_evol.update_layout(
        barmode='group',
        height=600,
        margin=dict(l=0, r=150, t=30, b=40),
        xaxis=dict(range=[0, 1.1], title="Score", gridcolor='#E2E8F0'),
        yaxis=dict(title="", tickfont=dict(family="Barlow", size=12)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Barlow")
    )
    
    # Add evolution annotations on the right
    for i, row in evol_df.iterrows():
        evol = row["Evolution"]
        color = "#1E8449" if evol > 0 else "#922B21" if evol < 0 else "#64748B"
        arrow = "↑" if evol > 0 else "↓" if evol < 0 else "→"
        fig_evol.add_annotation(
            x=1.05,
            y=row["Country"],
            text=f"{arrow} {evol:+.2f}",
            showarrow=False,
            font=dict(color=color, size=11, family="Barlow"),
            xanchor="left"
        )
    
    st.plotly_chart(fig_evol, use_container_width=True)
    
    st.markdown("---")
    
    # Summary insights
    col_insight1, col_insight2, col_insight3 = st.columns(3)
    
    improving = evol_df[evol_df["Evolution"] > 0.05].sort_values("Evolution", ascending=False)
    worsening = evol_df[evol_df["Evolution"] < -0.05].sort_values("Evolution", ascending=True)
    stable = evol_df[(evol_df["Evolution"] >= -0.05) & (evol_df["Evolution"] <= 0.05)]
    
    with col_insight1:
        st.markdown("""<div class="info-box" style="border-left: 4px solid #1E8449;">
            <div class="info-box-title" style="color: #1E8449;">📈 Improving Outlook</div>""", unsafe_allow_html=True)
        for _, row in improving.iterrows():
            st.markdown(f"• **{row['Country']}**: +{row['Evolution']:.2f}")
        if len(improving) == 0:
            st.markdown("*No significant improvement expected*")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_insight2:
        st.markdown("""<div class="info-box" style="border-left: 4px solid #922B21;">
            <div class="info-box-title" style="color: #922B21;">📉 Worsening Outlook</div>""", unsafe_allow_html=True)
        for _, row in worsening.iterrows():
            st.markdown(f"• **{row['Country']}**: {row['Evolution']:.2f}")
        if len(worsening) == 0:
            st.markdown("*No significant deterioration expected*")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_insight3:
        st.markdown("""<div class="info-box" style="border-left: 4px solid #F4D03F;">
            <div class="info-box-title" style="color: #B7950B;">→ Stable Outlook</div>""", unsafe_allow_html=True)
        stable_list = stable["Country"].tolist()
        st.markdown(", ".join(stable_list[:8]) + ("..." if len(stable_list) > 8 else ""))
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Data table
    st.markdown('<p class="section-title">Full Data Table</p>', unsafe_allow_html=True)
    display_df = legal_df[["Country", "Q18_Current", "Q19_Future", "Evolution"]].copy()
    display_df.columns = ["Country", "Q18: Current Environment", "Q19: Future Outlook", "Evolution"]
    display_df = display_df.sort_values("Q18: Current Environment", ascending=False)
    st.dataframe(display_df, use_container_width=True, hide_index=True,
        column_config={
            "Q18: Current Environment": st.column_config.ProgressColumn("Q18: Current", format="%.2f", min_value=0, max_value=1),
            "Q19: Future Outlook": st.column_config.ProgressColumn("Q19: Future", format="%.2f", min_value=0, max_value=1),
            "Evolution": st.column_config.NumberColumn("Evolution", format="%+.2f")
        })

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
            <div class="timeline-desc">Semi-structured interviews conducted to validate findings</div></div>
        <div class="timeline-item"><div class="timeline-date">March 2026</div><div class="timeline-title">Report Publication</div>
            <div class="timeline-desc">Ease to Mine Index released</div></div>
        """, unsafe_allow_html=True)
    
    with col_pie:
        st.markdown('<p class="section-title">Index Weighting</p>', unsafe_allow_html=True)
        weights = {'Section': ['Energy & Grid', 'Fiscal', 'Legal', 'Permits & Licensing', 'Customs & Tariffs', 'Operating Conditions'], 'Weight': [25, 20, 17.5, 17.5, 15, 5]}
        weight_colors = ['#A7BCF7', '#6287F0', '#0D6FFF', '#1D0DED', '#002060', '#12E09B']
        
        fig_pie = go.Figure(go.Pie(labels=weights['Section'], values=weights['Weight'], hole=0.45, marker=dict(colors=weight_colors),
            textinfo='percent', textposition='outside', textfont=dict(size=11, family="Barlow"), texttemplate='%{percent:.1%}'))
        fig_pie.add_annotation(text="<b>Weight</b>", x=0.5, y=0.5, font=dict(size=14, color="#1E293B", family="Barlow"), showarrow=False)
        fig_pie.update_layout(height=280, margin=dict(l=20, r=120, t=20, b=20), showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02, font=dict(size=10, family="Barlow")),
            paper_bgcolor='rgba(0,0,0,0)', font=dict(family="Barlow"))
        st.plotly_chart(fig_pie, use_container_width=True)

# ============================================
# FOOTER
# ============================================
st.markdown("""<div class="footer">
    <p><strong>Ease to Mine Index (EMI)</strong> - March 2026</p>
    <p>Report Author: <strong>Valentin Rousseau</strong> - <a href="https://x.com/MuadDib_Pill" target="_blank">@MuadDib_Pill</a></p>
    <p>Research by <a href="https://www.e2cpartners.com/insights/global-bitcoin-mining-report-the-ease-to-mine-index" target="_blank">E2C Partners</a></p>
</div>""", unsafe_allow_html=True)
