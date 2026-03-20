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
    [0.00, '#922B21'],
    [0.07, '#C0392B'],
    [0.14, '#CD6155'],
    [0.21, '#DC7633'],
    [0.28, '#E67E22'],
    [0.35, '#EB984E'],
    [0.42, '#F5B041'],
    [0.50, '#F4D03F'],
    [0.57, '#F7DC6F'],
    [0.64, '#A9DFBF'],
    [0.71, '#7DCEA0'],
    [0.78, '#52BE80'],
    [0.85, '#28B463'],
    [0.92, '#239B56'],
    [1.00, '#1E8449']
]

# ============================================
# CUSTOM CSS
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #FFFFFF;
    }
    
    [data-testid="stSidebar"] {
        width: 270px !important;
        min-width: 270px !important;
        background-color: #FAFAFA;
        border-right: 1px solid #E2E8F0;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        width: 270px !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        gap: 0 !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label {
        background: transparent !important;
        border: none !important;
        padding: 8px 0 !important;
        cursor: pointer;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        color: #1E8449 !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label > div:first-child {
        display: none !important;
    }
    
    .block-container {
        padding-top: 2.5rem !important;
    }
    
    h1 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        color: #1E293B !important;
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    h2, h3 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        color: #1E293B !important;
    }
    
    .section-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 1rem;
    }
    
    .map-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 0.5rem;
    }
    
    [data-testid="stSelectbox"] > div > div {
        border: 2px solid #E2E8F0 !important;
        border-radius: 8px !important;
        background-color: #F8FAFC !important;
    }
    
    [data-testid="stSelectbox"] > div > div:hover {
        border-color: #1E8449 !important;
    }
    
    [data-testid="stMetricValue"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.6rem !important;
        color: #1E293B !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.75rem !important;
        color: #64748B !important;
        text-transform: uppercase !important;
    }
    
    .footer {
        font-family: 'Inter', sans-serif;
        text-align: center;
        color: #64748B;
        padding: 2rem;
        font-size: 0.85rem;
        border-top: 1px solid #E2E8F0;
        margin-top: 2rem;
    }
    
    .footer a {
        color: #1E8449;
        text-decoration: none;
    }
    
    .footer a:hover {
        text-decoration: underline;
    }
    
    .sidebar-author {
        font-size: 0.8rem;
        color: #64748B;
        line-height: 1.5;
    }
    
    .sidebar-author a {
        color: #1E8449;
        text-decoration: none;
    }
    
    .sidebar-author a:hover {
        text-decoration: underline;
    }
    
    .info-box {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        font-size: 0.9rem;
        line-height: 1.6;
        color: #475569;
    }
    
    .info-box-title {
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 0.5rem;
    }
    
    .method-box-title {
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 0.5rem;
        font-size: 1rem;
    }
    
    .kpi-simple {
        text-align: center;
        padding: 1rem;
    }
    
    .kpi-simple-value {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    
    .kpi-simple-label {
        font-size: 0.85rem;
        color: #1E293B;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .methodology-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        height: 100%;
    }
    
    .methodology-card-icon {
        font-size: 2rem;
        margin-bottom: 0.75rem;
    }
    
    .methodology-card-title {
        font-weight: 600;
        color: #1E293B;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .methodology-card-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E8449;
        margin-bottom: 0.25rem;
    }
    
    .methodology-card-desc {
        font-size: 0.85rem;
        color: #64748B;
    }
    
    .timeline-item {
        border-left: 3px solid #1E8449;
        padding-left: 1rem;
        margin-bottom: 1rem;
    }
    
    .timeline-date {
        font-size: 0.8rem;
        color: #1E8449;
        font-weight: 600;
    }
    
    .timeline-title {
        font-weight: 600;
        color: #1E293B;
        margin: 0.25rem 0;
    }
    
    .timeline-desc {
        font-size: 0.85rem;
        color: #64748B;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_data():
    df = pd.read_csv("data/emi_data.csv")
    return df

df = load_data()

# ============================================
# ISO CODES FOR MAP
# ============================================
ISO_CODES = {
    "Oman": "OMN",
    "UAE": "ARE",
    "Iceland": "ISL",
    "Argentina": "ARG",
    "Paraguay": "PRY",
    "Texas (US)": "USA",
    "Quebec (CA)": "CAN",
    "Brazil": "BRA",
    "Alberta (CA)": "CAN",
    "Russia": "RUS",
    "Norway": "NOR",
    "Ethiopia": "ETH",
    "Kazakhstan": "KAZ",
    "Finland": "FIN",
    "Kenya": "KEN",
    "DRC": "COD",
    "Chile": "CHL",
    "Sweden": "SWE",
    "Australia": "AUS"
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
        (0.00, '#922B21'),
        (0.07, '#C0392B'),
        (0.14, '#CD6155'),
        (0.21, '#DC7633'),
        (0.28, '#E67E22'),
        (0.35, '#EB984E'),
        (0.42, '#F5B041'),
        (0.50, '#F4D03F'),
        (0.57, '#F7DC6F'),
        (0.64, '#A9DFBF'),
        (0.71, '#7DCEA0'),
        (0.78, '#52BE80'),
        (0.85, '#28B463'),
        (0.92, '#239B56'),
        (1.00, '#1E8449')
    ]
    
    for i in range(len(color_stops) - 1):
        if color_stops[i][0] <= ratio <= color_stops[i + 1][0]:
            t = (ratio - color_stops[i][0]) / (color_stops[i + 1][0] - color_stops[i][0])
            
            c1 = color_stops[i][1]
            c2 = color_stops[i + 1][1]
            
            r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
            r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
            
            r = int(r1 + (r2 - r1) * t)
            g = int(g1 + (g2 - g1) * t)
            b = int(b1 + (b2 - b1) * t)
            
            return f'#{r:02x}{g:02x}{b:02x}'
    
    return '#F4D03F'

def generate_gradient_colors_simple(n, start_hex="#1E8449", end_hex="#E67E22"):
    start_r = int(start_hex[1:3], 16)
    start_g = int(start_hex[3:5], 16)
    start_b = int(start_hex[5:7], 16)
    
    end_r = int(end_hex[1:3], 16)
    end_g = int(end_hex[3:5], 16)
    end_b = int(end_hex[5:7], 16)
    
    colors = []
    for i in range(n):
        if n > 1:
            ratio = i / (n - 1)
        else:
            ratio = 0
        
        r = int(start_r + (end_r - start_r) * ratio)
        g = int(start_g + (end_g - start_g) * ratio)
        b = int(start_b + (end_b - start_b) * ratio)
        
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        
        colors.append(f'#{r:02x}{g:02x}{b:02x}')
    
    return colors

def get_text_color_for_score(score):
    if 0.37 <= score <= 0.64:
        return "black"
    return "white"

# ============================================
# SIDEBAR NAVIGATION
# ============================================
with st.sidebar:
    st.markdown("### Navigation")
    page = st.radio("", ["Overview", "Overview (Creative)", "Methodology", "Methodology (Creative)"], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("**Ease to Mine Index (EMI)**")
    st.markdown("March 2026")
    st.markdown("")
    st.markdown("""
    <p class="sidebar-author">
    A report by <strong>Valentin Rousseau</strong><br>
    <a href="https://x.com/MuadDib_Pill" target="_blank">@MuadDib_Pill</a><br><br>
    Provided by <a href="https://www.e2cpartners.com/insights/global-bitcoin-mining-report-the-ease-to-mine-index" target="_blank">E2C Partners</a>
    </p>
    """, unsafe_allow_html=True)

# ============================================
# SCORE MAP FOR FILTERS
# ============================================
score_map = {
    "Overall Index": "Index_Score",
    "Fiscal": "Fiscal",
    "Permits & Licensing": "Permit_Licensing",
    "Legal": "Legal",
    "Energy & Grid": "Energy_Grid",
    "Customs & Tariffs": "Tariff_Import",
    "Operating Conditions": "Operating_Conditions"
}

# ============================================
# OVERVIEW PAGE (ORIGINAL)
# ============================================
if page == "Overview":
    st.markdown("# Ease to Mine Index Dashboard")
    st.markdown("Comprehensive analysis of Bitcoin mining regulatory and operating conditions across 19 jurisdictions")
    
    st.markdown('<p class="map-title">Ease to Mine Index Map</p>', unsafe_allow_html=True)
    
    col_filter, col_spacer = st.columns([1, 3])
    with col_filter:
        score_type = st.selectbox(
            "Select category",
            ["Overall Index", "Fiscal", "Permits & Licensing", "Legal", "Energy & Grid", "Customs & Tariffs", "Operating Conditions"],
            key="score_filter"
        )
    
    selected_col = score_map[score_type]
    
    df_map = df.copy()
    df_map["ISO"] = df_map["Country"].map(ISO_CODES)
    
    df_map_agg = df_map.groupby("ISO").agg({
        selected_col: "mean",
        "Country": lambda x: ", ".join(x) if len(x) > 1 else x.iloc[0]
    }).reset_index()
    df_map_agg.columns = ["ISO", "Score", "Country"]
    
    fig_map = go.Figure(go.Choropleth(
        locations=df_map_agg["ISO"],
        z=df_map_agg["Score"],
        text=df_map_agg["Country"],
        colorscale=COLOR_SCALE,
        autocolorscale=False,
        marker_line_color='#4B5563',
        marker_line_width=1,
        colorbar=dict(
            title=dict(text=score_type, side="right", font=dict(family="Inter", size=12)),
            tickfont=dict(family="Inter"),
            len=0.7,
            thickness=15
        ),
        hovertemplate="<b>%{text}</b><br>" + score_type + ": %{z:.2f}<extra></extra>"
    ))
    
    fig_map.update_layout(
        height=520,
        margin=dict(l=0, r=0, t=10, b=0),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="#94A3B8",
            showland=True,
            landcolor="#E2E8F0",
            showocean=True,
            oceancolor="#FFFFFF",
            showlakes=True,
            lakecolor="#FFFFFF",
            showcountries=True,
            countrycolor="#94A3B8",
            projection_type='equirectangular',
            bgcolor='rgba(0,0,0,0)',
            lonaxis=dict(range=[-180, 180]),
            lataxis=dict(range=[-65, 90])
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter")
    )
    
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown('<p class="section-title">Score Heatmap by Section</p>', unsafe_allow_html=True)
    
    heatmap_cols = ["Fiscal", "Permit_Licensing", "Legal", "Energy_Grid", "Tariff_Import", "Operating_Conditions"]
    heatmap_labels = ["Fiscal", "Permits", "Legal", "Energy", "Tariffs", "Climate"]
    
    df_heat = df.sort_values("Index_Score", ascending=False)
    heatmap_data = df_heat.set_index("Country")[heatmap_cols]
    heatmap_data.columns = heatmap_labels
    
    fig_heat = go.Figure(go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_labels,
        y=heatmap_data.index,
        colorscale=COLOR_SCALE,
        hovertemplate="Country: %{y}<br>Section: %{x}<br>Score: %{z:.2f}<extra></extra>",
        showscale=True,
        colorbar=dict(
            title=dict(text="Score", side="right", font=dict(family="Inter")),
            tickfont=dict(family="Inter")
        )
    ))
    
    annotations = []
    for i, country in enumerate(heatmap_data.index):
        for j, section in enumerate(heatmap_labels):
            val = heatmap_data.iloc[i, j]
            annotations.append(dict(
                x=section,
                y=country,
                text=f"{val:.2f}",
                showarrow=False,
                font=dict(
                    color=get_text_color_for_score(val),
                    size=10,
                    family="Inter"
                )
            ))
    
    fig_heat.update_layout(annotations=annotations)
    
    fig_heat.update_layout(
        height=580,
        margin=dict(l=0, r=0, t=10, b=40),
        xaxis=dict(title="", tickangle=0, side="bottom", tickfont=dict(family="Inter", size=11)),
        yaxis=dict(title="", autorange="reversed", tickfont=dict(family="Inter", size=11)),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter")
    )
    
    st.plotly_chart(fig_heat, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown('<p class="section-title">EMI Ranking</p>', unsafe_allow_html=True)
    
    col_rank_filter, col_rank_spacer = st.columns([1, 3])
    with col_rank_filter:
        rank_dimension = st.selectbox(
            "Select category",
            ["Overall Index", "Fiscal", "Permits & Licensing", "Legal", "Energy & Grid", "Customs & Tariffs", "Operating Conditions"],
            key="rank_filter"
        )
    
    rank_col = score_map[rank_dimension]
    df_rank = df.sort_values(rank_col, ascending=True).copy()
    
    min_score = df_rank[rank_col].min()
    max_score = df_rank[rank_col].max()
    colors = [get_score_color(score, min_score, max_score) for score in df_rank[rank_col]]
    
    col_chart, col_text = st.columns([2, 1])
    
    with col_chart:
        fig_rank = go.Figure(go.Bar(
            x=df_rank[rank_col],
            y=df_rank["Country"],
            orientation='h',
            marker_color=colors,
            text=df_rank[rank_col].round(2),
            textposition='outside',
            textfont=dict(size=11, family="Inter"),
            name=rank_dimension
        ))
        
        fig_rank.update_layout(
            height=620,
            margin=dict(l=0, r=60, t=10, b=40),
            xaxis=dict(
                range=[0, 1], 
                title=dict(text=rank_dimension + " Score", font=dict(family="Inter", size=12)),
                gridcolor='#E2E8F0', 
                zeroline=False
            ),
            yaxis=dict(title="", tickfont=dict(family="Inter", size=11)),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter")
        )
        
        st.plotly_chart(fig_rank, use_container_width=True)
    
    with col_text:
        st.markdown("""
        <div class="info-box">
            <div class="info-box-title">About the Ease to Mine Index</div>
            <p>The first edition of the <strong>Ease to Mine Index (EMI)</strong> is a composite framework designed to assess the overall attractiveness of jurisdictions for Bitcoin mining.</p>
            <p style="margin-top: 0.75rem;">The index evaluates a broad set of dimensions:</p>
            <ul style="margin: 0.5rem 0; padding-left: 1.2rem;">
                <li>Legal and fiscal frameworks</li>
                <li>Permitting and licensing conditions</li>
                <li>Energy market structure and grid access</li>
                <li>Climate characteristics</li>
                <li>Tariff and import environments</li>
            </ul>
            <p style="margin-top: 0.75rem;">While mining analysis traditionally emphasizes operational metrics (power costs, hashprice), regulatory conditions are often underweighted. By integrating both perspectives, the EMI provides a more holistic assessment of mining sustainability.</p>
            <p style="margin-top: 0.75rem;"><strong>Coverage:</strong> 18 countries spanning established and emerging mining regions — 19 jurisdictions (where Texas serves as a proxy of U.S., and Alberta and Québec for Canada).</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<p class="section-title">Full Data Table</p>', unsafe_allow_html=True)
    
    df_display = df.copy()
    df_display = df_display.rename(columns={
        "Index_Score": "EMI Score",
        "Permit_Licensing": "Permits",
        "Energy_Grid": "Energy",
        "Tariff_Import": "Tariffs",
        "Operating_Conditions": "Climate",
        "Hashrate_Q1_25": "Hashrate Q1-25 (EH/s)",
        "Hashrate_Q1_26": "Hashrate Q1-26 (EH/s)"
    })
    
    numeric_cols = ["EMI Score", "Fiscal", "Permits", "Legal", "Energy", "Tariffs", "Climate"]
    for col in numeric_cols:
        df_display[col] = df_display[col].round(2)
    
    df_display = df_display.sort_values("EMI Score", ascending=False)
    display_cols = ["Country", "Region", "EMI Score", "Fiscal", "Permits", "Legal", "Energy", "Tariffs", "Climate", "Hashrate Q1-25 (EH/s)", "Hashrate Q1-26 (EH/s)"]
    
    st.dataframe(
        df_display[display_cols],
        use_container_width=True,
        hide_index=True,
        height=550,
        column_config={
            "EMI Score": st.column_config.ProgressColumn("EMI Score", format="%.2f", min_value=0, max_value=1),
            "Fiscal": st.column_config.NumberColumn(format="%.2f"),
            "Permits": st.column_config.NumberColumn(format="%.2f"),
            "Legal": st.column_config.NumberColumn(format="%.2f"),
            "Energy": st.column_config.NumberColumn(format="%.2f"),
            "Tariffs": st.column_config.NumberColumn(format="%.2f"),
            "Climate": st.column_config.NumberColumn(format="%.2f"),
            "Hashrate Q1-25 (EH/s)": st.column_config.NumberColumn(format="%.1f"),
            "Hashrate Q1-26 (EH/s)": st.column_config.NumberColumn(format="%.1f"),
        }
    )
    
    csv = df_display[display_cols].to_csv(index=False)
    st.download_button(label="Download Data (CSV)", data=csv, file_name="emi_data_export.csv", mime="text/csv")

# ============================================
# OVERVIEW PAGE (CREATIVE)
# ============================================
elif page == "Overview (Creative)":
    st.markdown("# Ease to Mine Index Dashboard")
    
    df_sorted = df.sort_values("Index_Score", ascending=False)
    top_country = df_sorted.iloc[0]
    bottom_country = df_sorted.iloc[-1]
    avg_score = df["Index_Score"].mean()
    total_hashrate = df["Hashrate_Q1_26"].sum()
    
    # KPI Cards - Simple style with colored text
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-simple">
            <div class="kpi-simple-value" style="color: #1E8449;">19</div>
            <div class="kpi-simple-label">Jurisdictions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-simple">
            <div class="kpi-simple-value" style="color: #1E8449;">{avg_score:.2f}</div>
            <div class="kpi-simple-label">Average EMI Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-simple">
            <div class="kpi-simple-value" style="color: #475569;">{total_hashrate:.0f}</div>
            <div class="kpi-simple-label">Total Hashrate (EH/s)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-simple">
            <div class="kpi-simple-value" style="color: #1E8449;">{top_country['Index_Score']:.2f}</div>
            <div class="kpi-simple-label">🏆 {top_country['Country']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="kpi-simple">
            <div class="kpi-simple-value" style="color: #DC7633;">{bottom_country['Index_Score']:.2f}</div>
            <div class="kpi-simple-label">⚠️ {bottom_country['Country']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Map and Top/Bottom 3 - Adjusted column ratio (3:1 instead of 2:1)
    col_map, col_top = st.columns([3, 1])
    
    with col_map:
        st.markdown('<p class="section-title">Ease to Mine Index Map</p>', unsafe_allow_html=True)
        
        score_type_creative = st.selectbox(
            "Select category",
            ["Overall Index", "Fiscal", "Permits & Licensing", "Legal", "Energy & Grid", "Customs & Tariffs", "Operating Conditions"],
            key="score_filter_creative"
        )
        
        selected_col_creative = score_map[score_type_creative]
        
        df_map = df.copy()
        df_map["ISO"] = df_map["Country"].map(ISO_CODES)
        
        df_map_agg = df_map.groupby("ISO").agg({
            selected_col_creative: "mean",
            "Country": lambda x: ", ".join(x) if len(x) > 1 else x.iloc[0]
        }).reset_index()
        df_map_agg.columns = ["ISO", "Score", "Country"]
        
        fig_map = go.Figure(go.Choropleth(
            locations=df_map_agg["ISO"],
            z=df_map_agg["Score"],
            text=df_map_agg["Country"],
            colorscale=COLOR_SCALE,
            autocolorscale=False,
            marker_line_color='#4B5563',
            marker_line_width=1,
            colorbar=dict(
                title=dict(text="Score", side="right", font=dict(family="Inter", size=11)),
                tickfont=dict(family="Inter", size=10),
                len=0.8,
                thickness=12
            ),
            hovertemplate="<b>%{text}</b><br>Score: %{z:.2f}<extra></extra>"
        ))
        
        fig_map.update_layout(
            height=420,
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
                projection_type='equirectangular',
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter")
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
    
    with col_top:
        st.markdown('<p class="section-title">Top 3 Jurisdictions</p>', unsafe_allow_html=True)
        
        for idx, (i, row) in enumerate(df_sorted.head(3).iterrows()):
            rank = idx + 1
            color = get_score_color(row["Index_Score"], df["Index_Score"].min(), df["Index_Score"].max())
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, {color}22 0%, transparent 100%); 
                        border-left: 4px solid {color}; 
                        padding: 10px 12px; 
                        margin-bottom: 8px; 
                        border-radius: 0 8px 8px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-weight: 700; color: #1E293B; font-size: 0.9rem;">#{rank} {row['Country']}</span>
                        <span style="color: #64748B; font-size: 0.75rem; margin-left: 6px;">{row['Region']}</span>
                    </div>
                    <div style="font-weight: 700; font-size: 1.1rem; color: {color};">{row['Index_Score']:.2f}</div>
                </div>
                <div style="font-size: 0.75rem; color: #64748B; margin-top: 2px;">
                    Hashrate: {row['Hashrate_Q1_26']:.1f} EH/s
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("")
        st.markdown('<p class="section-title" style="margin-top: 0.75rem;">Bottom 3 Jurisdictions</p>', unsafe_allow_html=True)
        
        bottom_3 = df_sorted.tail(3).iloc[::-1]
        for idx, (i, row) in enumerate(bottom_3.iterrows()):
            rank = 19 - idx
            color = get_score_color(row["Index_Score"], df["Index_Score"].min(), df["Index_Score"].max())
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, {color}22 0%, transparent 100%); 
                        border-left: 4px solid {color}; 
                        padding: 10px 12px; 
                        margin-bottom: 8px; 
                        border-radius: 0 8px 8px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-weight: 700; color: #1E293B; font-size: 0.9rem;">#{rank} {row['Country']}</span>
                        <span style="color: #64748B; font-size: 0.75rem; margin-left: 6px;">{row['Region']}</span>
                    </div>
                    <div style="font-weight: 700; font-size: 1.1rem; color: {color};">{row['Index_Score']:.2f}</div>
                </div>
                <div style="font-size: 0.75rem; color: #64748B; margin-top: 2px;">
                    Hashrate: {row['Hashrate_Q1_26']:.1f} EH/s
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Radar + Regional
    col_radar, col_regional = st.columns([1, 1])
    
    with col_radar:
        st.markdown('<p class="section-title">Dimension Comparison: Top 3 vs Bottom 3</p>', unsafe_allow_html=True)
        
        categories = ['Fiscal', 'Permits', 'Legal', 'Energy', 'Tariffs', 'Climate']
        
        top3_avg = df_sorted.head(3)[["Fiscal", "Permit_Licensing", "Legal", "Energy_Grid", "Tariff_Import", "Operating_Conditions"]].mean().values.tolist()
        bottom3_avg = df_sorted.tail(3)[["Fiscal", "Permit_Licensing", "Legal", "Energy_Grid", "Tariff_Import", "Operating_Conditions"]].mean().values.tolist()
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=top3_avg + [top3_avg[0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor='rgba(30, 132, 73, 0.2)',
            line=dict(color='#1E8449', width=2),
            name='Top 3 Average'
        ))
        
        fig_radar.add_trace(go.Scatterpolar(
            r=bottom3_avg + [bottom3_avg[0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor='rgba(146, 43, 33, 0.2)',
            line=dict(color='#922B21', width=2),
            name='Bottom 3 Average'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    tickfont=dict(size=10),
                    gridcolor='#E2E8F0'
                ),
                angularaxis=dict(tickfont=dict(size=11, family="Inter"))
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.15,
                xanchor="center",
                x=0.5,
                font=dict(size=11)
            ),
            height=380,
            margin=dict(l=60, r=60, t=30, b=60),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter")
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col_regional:
        st.markdown('<p class="section-title">Average EMI Score by Region</p>', unsafe_allow_html=True)
        
        df_regional = df.groupby("Region").agg({
            "Index_Score": "mean",
            "Country": "count",
            "Hashrate_Q1_26": "sum"
        }).reset_index()
        df_regional.columns = ["Region", "Avg_Score", "Count", "Total_Hashrate"]
        df_regional = df_regional.sort_values("Avg_Score", ascending=True)
        
        colors_regional = [get_score_color(s, df_regional["Avg_Score"].min(), df_regional["Avg_Score"].max()) for s in df_regional["Avg_Score"]]
        
        fig_regional = go.Figure(go.Bar(
            x=df_regional["Avg_Score"],
            y=df_regional["Region"],
            orientation='h',
            marker_color=colors_regional,
            text=[f"{s:.2f}" for s in df_regional["Avg_Score"]],
            textposition='outside',
            textfont=dict(size=12, family="Inter"),
            hovertemplate="<b>%{y}</b><br>Avg Score: %{x:.2f}<extra></extra>"
        ))
        
        fig_regional.update_layout(
            height=380,
            margin=dict(l=0, r=50, t=30, b=40),
            xaxis=dict(
                range=[0, 0.85],
                title="",
                gridcolor='#E2E8F0',
                zeroline=False,
                showticklabels=False
            ),
            yaxis=dict(title="", tickfont=dict(family="Inter", size=12)),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter")
        )
        
        st.plotly_chart(fig_regional, use_container_width=True)
    
    st.markdown("---")
    
    # Bubble Chart
    st.markdown('<p class="section-title">Hashrate vs EMI Score by Jurisdiction</p>', unsafe_allow_html=True)
    
    df_bubble = df.copy()
    df_bubble["color"] = [get_score_color(s, df["Index_Score"].min(), df["Index_Score"].max()) for s in df["Index_Score"]]
    
    fig_bubble = go.Figure()
    
    for _, row in df_bubble.iterrows():
        fig_bubble.add_trace(go.Scatter(
            x=[row["Index_Score"]],
            y=[row["Hashrate_Q1_26"]],
            mode='markers+text',
            marker=dict(
                size=max(15, min(60, row["Hashrate_Q1_26"] / 5)),
                color=row["color"],
                opacity=0.7,
                line=dict(width=1, color='white')
            ),
            text=[row["Country"]],
            textposition="top center",
            textfont=dict(size=9, family="Inter"),
            hovertemplate=f"<b>{row['Country']}</b><br>EMI Score: {row['Index_Score']:.2f}<br>Hashrate: {row['Hashrate_Q1_26']:.1f} EH/s<extra></extra>",
            showlegend=False
        ))
    
    fig_bubble.update_layout(
        height=450,
        margin=dict(l=60, r=40, t=20, b=60),
        xaxis=dict(
            title=dict(text="EMI Score", font=dict(family="Inter", size=12)),
            range=[0.2, 0.85],
            gridcolor='#E2E8F0',
            zeroline=False
        ),
        yaxis=dict(
            title=dict(text="Hashrate Q1-26 (EH/s)", font=dict(family="Inter", size=12)),
            gridcolor='#E2E8F0',
            zeroline=False
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter")
    )
    
    st.plotly_chart(fig_bubble, use_container_width=True)
    
    st.markdown("---")
    
    # Heatmap
    st.markdown('<p class="section-title">Score Heatmap by Section</p>', unsafe_allow_html=True)
    
    heatmap_cols = ["Fiscal", "Permit_Licensing", "Legal", "Energy_Grid", "Tariff_Import", "Operating_Conditions"]
    heatmap_labels = ["Fiscal", "Permits", "Legal", "Energy", "Tariffs", "Climate"]
    
    df_heat = df.sort_values("Index_Score", ascending=False)
    heatmap_data = df_heat.set_index("Country")[heatmap_cols]
    heatmap_data.columns = heatmap_labels
    
    fig_heat = go.Figure(go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_labels,
        y=heatmap_data.index,
        colorscale=COLOR_SCALE,
        hovertemplate="Country: %{y}<br>Section: %{x}<br>Score: %{z:.2f}<extra></extra>",
        showscale=True,
        colorbar=dict(
            title=dict(text="Score", side="right", font=dict(family="Inter")),
            tickfont=dict(family="Inter")
        )
    ))
    
    annotations = []
    for i, country in enumerate(heatmap_data.index):
        for j, section in enumerate(heatmap_labels):
            val = heatmap_data.iloc[i, j]
            annotations.append(dict(
                x=section,
                y=country,
                text=f"{val:.2f}",
                showarrow=False,
                font=dict(color=get_text_color_for_score(val), size=10, family="Inter")
            ))
    
    fig_heat.update_layout(annotations=annotations)
    
    fig_heat.update_layout(
        height=550,
        margin=dict(l=0, r=0, t=10, b=40),
        xaxis=dict(title="", tickangle=0, side="bottom", tickfont=dict(family="Inter", size=11)),
        yaxis=dict(title="", autorange="reversed", tickfont=dict(family="Inter", size=11)),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter")
    )
    
    st.plotly_chart(fig_heat, use_container_width=True)

# ============================================
# METHODOLOGY PAGE (ORIGINAL)
# ============================================
elif page == "Methodology":
    st.markdown("# Methodology")
    st.markdown("Survey design, data collection, and respondent distribution")
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Respondents", "48")
    with col2:
        st.metric("Total Responses", "55")
    with col3:
        st.metric("Jurisdictions Covered", "19")
    with col4:
        st.metric("Survey Period", "Dec 2025 - Feb 2026")
    
    st.markdown("---")
    
    st.markdown('<p class="section-title">Survey Respondents by Jurisdiction</p>', unsafe_allow_html=True)
    
    col_pie, col_method = st.columns([1, 1])
    
    with col_pie:
        df_resp = df.copy()
        canada_resp = df_resp[df_resp["Country"].isin(["Alberta (CA)", "Quebec (CA)"])]["Respondents"].sum()
        df_resp = df_resp[~df_resp["Country"].isin(["Alberta (CA)", "Quebec (CA)"])]
        df_resp = pd.concat([df_resp, pd.DataFrame([{"Country": "Canada", "Respondents": canada_resp}])], ignore_index=True)
        
        df_resp = df_resp[df_resp["Respondents"] > 0].sort_values("Respondents", ascending=False)
        total_respondents = df_resp["Respondents"].sum()
        
        pie_colors = generate_gradient_colors_simple(len(df_resp), "#1E8449", "#E67E22")
        
        fig_pie = go.Figure(go.Pie(
            labels=df_resp["Country"],
            values=df_resp["Respondents"],
            hole=0.55,
            marker=dict(colors=pie_colors),
            textinfo='label+value',
            textposition='outside',
            textfont=dict(size=10, family="Inter"),
            hovertemplate="<b>%{label}</b><br>Respondents: %{value}<br>Share: %{percent}<extra></extra>",
            pull=[0.02] * len(df_resp)
        ))
        
        fig_pie.add_annotation(
            text="<b>55</b><br><span style='font-size:11px'>Total responses</span>",
            x=0.5, y=0.5,
            font=dict(size=28, color="#1E293B", family="Inter"),
            showarrow=False
        )
        
        fig_pie.update_layout(
            height=480,
            margin=dict(l=60, r=60, t=20, b=40),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter")
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_method:
        st.markdown("""
        <div class="info-box">
            <div class="method-box-title">Survey Methodology</div>
            <p>Between December 2025 and February 2026, Hashlabs conducted an online survey targeting stakeholders within the Bitcoin mining ecosystem, including industrial miners, mining associations, industry journalists, and other experts.</p>
            <p style="margin-top: 0.75rem;"><strong>Survey scope:</strong> 5 sections covering legal, fiscal, energy & electricity grids, permitting & licensing, and tariffs & customs procedures. A total of 33 questions combined quantitative metrics with qualitative assessments.</p>
            <p style="margin-top: 0.75rem;"><strong>Data validation:</strong> Responses were reviewed for internal consistency and potential reporting bias. Follow-up semi-structured interviews were conducted with selected respondents to validate findings and clarify country-specific conditions.</p>
            <p style="margin-top: 0.75rem; padding: 0.5rem; background-color: #FEF3C7; border-radius: 4px; font-size: 0.85rem;"><strong>Note:</strong> The Climate Operating Conditions (C.O.C.) section is beyond survey scope and based on internal analysis.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<p class="section-title">Index Weighting by Dimension</p>', unsafe_allow_html=True)
    
    fig_weights = go.Figure()
    
    weights_main = [
        ("Energy & Grid", 25, "#1E8449", "white", "Energy & Grid<br>25.0%"),
        ("Fiscal", 20, "#28B463", "white", "Fiscal<br>20.0%"),
        ("Legal", 17.5, "#7DCEA0", "black", "Legal<br>17.5%"),
        ("Permits & Licensing", 17.5, "#F4D03F", "black", "Permits<br>17.5%"),
        ("Customs & Tariffs", 15, "#E67E22", "white", "Tariffs<br>15.0%"),
        ("C.O.C.", 5, "#922B21", "white", "C.O.C.<br>5.0%")
    ]
    
    for name, weight, color, text_color, display_text in weights_main:
        fig_weights.add_trace(go.Bar(
            name=name,
            x=[weight],
            y=["EMI Index"],
            orientation='h',
            marker_color=color,
            text=[display_text],
            textposition='inside',
            insidetextanchor='middle',
            textfont=dict(size=12, family="Inter", color=text_color),
            hovertemplate=f"<b>{name}</b><br>Weight: {weight}%<extra></extra>"
        ))
    
    fig_weights.update_layout(
        barmode='stack',
        height=120,
        margin=dict(l=0, r=0, t=20, b=20),
        xaxis=dict(
            title="",
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            range=[0, 100]
        ),
        yaxis=dict(
            title="",
            showticklabels=False
        ),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter")
    )
    
    st.plotly_chart(fig_weights, use_container_width=True)
    
    st.markdown("---")
    
    st.markdown('<p class="section-title">Respondents by Jurisdiction</p>', unsafe_allow_html=True)
    
    df_resp_table = df_resp[["Country", "Respondents"]].copy()
    df_resp_table["Share"] = (df_resp_table["Respondents"] / total_respondents * 100).round(1)
    df_resp_table = df_resp_table.sort_values("Respondents", ascending=False)
    
    st.dataframe(
        df_resp_table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Country": "Jurisdiction",
            "Respondents": st.column_config.NumberColumn("Respondents", format="%d"),
            "Share": st.column_config.NumberColumn("Share (%)", format="%.1f%%")
        }
    )

# ============================================
# METHODOLOGY PAGE (CREATIVE)
# ============================================
elif page == "Methodology (Creative)":
    st.markdown("# Methodology")
    st.markdown("How we built the Ease to Mine Index")
    
    st.markdown("")
    
    # Key Stats Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="methodology-card">
            <div class="methodology-card-icon">👥</div>
            <div class="methodology-card-value">48</div>
            <div class="methodology-card-title">Respondents</div>
            <div class="methodology-card-desc">Industry practitioners surveyed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="methodology-card">
            <div class="methodology-card-icon">📝</div>
            <div class="methodology-card-value">55</div>
            <div class="methodology-card-title">Responses</div>
            <div class="methodology-card-desc">Total survey submissions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="methodology-card">
            <div class="methodology-card-icon">🌍</div>
            <div class="methodology-card-value">19</div>
            <div class="methodology-card-title">Jurisdictions</div>
            <div class="methodology-card-desc">Countries & regions covered</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="methodology-card">
            <div class="methodology-card-icon">❓</div>
            <div class="methodology-card-value">33</div>
            <div class="methodology-card-title">Questions</div>
            <div class="methodology-card-desc">Across 5 survey sections</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Two columns: Timeline + Respondent Profile
    col_timeline, col_profile = st.columns([1, 1])
    
    with col_timeline:
        st.markdown('<p class="section-title">Survey Timeline</p>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="timeline-item">
            <div class="timeline-date">December 2025</div>
            <div class="timeline-title">Survey Launch</div>
            <div class="timeline-desc">Online survey deployed targeting Bitcoin mining ecosystem stakeholders</div>
        </div>
        
        <div class="timeline-item">
            <div class="timeline-date">January 2026</div>
            <div class="timeline-title">Data Collection</div>
            <div class="timeline-desc">Responses collected from industrial miners, associations, journalists and experts</div>
        </div>
        
        <div class="timeline-item">
            <div class="timeline-date">February 2026</div>
            <div class="timeline-title">Validation Phase</div>
            <div class="timeline-desc">Semi-structured interviews conducted to validate findings and clarify ambiguities</div>
        </div>
        
        <div class="timeline-item">
            <div class="timeline-date">March 2026</div>
            <div class="timeline-title">Report Publication</div>
            <div class="timeline-desc">EMI V2 released with comprehensive analysis across 19 jurisdictions</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        st.markdown("""
        <div style="background-color: #FEF3C7; border-radius: 8px; padding: 1rem; margin-top: 1rem;">
            <p style="font-size: 0.85rem; color: #92400E; margin: 0;"><strong>Note:</strong> The Climate Operating Conditions (C.O.C.) section is beyond survey scope and based on internal analysis.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_profile:
        st.markdown('<p class="section-title">Respondent Profile</p>', unsafe_allow_html=True)
        
        # Respondent types donut
        respondent_types = {
            "Industrial Miners": 60,
            "Mining Associations": 15,
            "Industry Journalists": 10,
            "Other Experts": 15
        }
        
        fig_types = go.Figure(go.Pie(
            labels=list(respondent_types.keys()),
            values=list(respondent_types.values()),
            hole=0.6,
            marker=dict(colors=['#1E8449', '#28B463', '#7DCEA0', '#A9DFBF']),
            textinfo='percent',
            textposition='outside',
            textfont=dict(size=11, family="Inter"),
            hovertemplate="<b>%{label}</b><br>Share: %{percent}<extra></extra>"
        ))
        
        fig_types.add_annotation(
            text="<b>Respondent</b><br><span style='font-size:11px'>Types</span>",
            x=0.5, y=0.5,
            font=dict(size=14, color="#1E293B", family="Inter"),
            showarrow=False
        )
        
        fig_types.update_layout(
            height=280,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(size=10)
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter")
        )
        
        st.plotly_chart(fig_types, use_container_width=True)
    
    st.markdown("---")
    
    # Survey Sections and Weighting
    st.markdown('<p class="section-title">Index Composition & Weighting</p>', unsafe_allow_html=True)
    
    col_sections, col_weight_chart = st.columns([1, 1])
    
    with col_sections:
        sections_data = [
            ("⚡", "Energy & Grid", "25.0%", "Grid access, power costs, curtailment exposure"),
            ("💰", "Fiscal", "20.0%", "Tax regime, incentives, profit center flexibility"),
            ("⚖️", "Legal", "17.5%", "Regulatory framework, policy stability"),
            ("📋", "Permits & Licensing", "17.5%", "Construction permits, zoning, compliance"),
            ("🚢", "Customs & Tariffs", "15.0%", "Import duties, VAT, procedures"),
            ("🌡️", "C.O.C.", "5.0%", "Temperature, humidity, altitude (internal analysis)")
        ]
        
        for icon, name, weight, desc in sections_data:
            st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 12px 0; border-bottom: 1px solid #E2E8F0;">
                <div style="font-size: 1.5rem; margin-right: 12px;">{icon}</div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #1E293B;">{name}</div>
                    <div style="font-size: 0.8rem; color: #64748B;">{desc}</div>
                </div>
                <div style="font-weight: 700; color: #1E8449; font-size: 1.1rem;">{weight}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_weight_chart:
        weights_df = pd.DataFrame({
            'Section': ['Energy & Grid', 'Fiscal', 'Legal', 'Permits', 'Tariffs', 'C.O.C.'],
            'Weight': [25, 20, 17.5, 17.5, 15, 5]
        })
        
        fig_weight = go.Figure(go.Bar(
            x=weights_df['Weight'],
            y=weights_df['Section'],
            orientation='h',
            marker_color=['#1E8449', '#28B463', '#52BE80', '#7DCEA0', '#A9DFBF', '#D5F5E3'],
            text=[f"{w}%" for w in weights_df['Weight']],
            textposition='inside',
            textfont=dict(size=12, family="Inter", color="white"),
            hovertemplate="<b>%{y}</b><br>Weight: %{x}%<extra></extra>"
        ))
        
        fig_weight.update_layout(
            height=320,
            margin=dict(l=0, r=40, t=20, b=20),
            xaxis=dict(
                title="Weight (%)",
                range=[0, 30],
                gridcolor='#E2E8F0'
            ),
            yaxis=dict(title="", autorange="reversed"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter")
        )
        
        st.plotly_chart(fig_weight, use_container_width=True)
    
    st.markdown("---")
    
    # Geographic Distribution
    st.markdown('<p class="section-title">Geographic Distribution of Respondents</p>', unsafe_allow_html=True)
    
    df_resp = df.copy()
    canada_resp = df_resp[df_resp["Country"].isin(["Alberta (CA)", "Quebec (CA)"])]["Respondents"].sum()
    df_resp = df_resp[~df_resp["Country"].isin(["Alberta (CA)", "Quebec (CA)"])]
    df_resp = pd.concat([df_resp, pd.DataFrame([{"Country": "Canada", "Respondents": canada_resp, "Region": "North America"}])], ignore_index=True)
    df_resp = df_resp[df_resp["Respondents"] > 0].sort_values("Respondents", ascending=False)
    
    # Bar chart of respondents
    fig_resp_bar = go.Figure(go.Bar(
        x=df_resp["Respondents"],
        y=df_resp["Country"],
        orientation='h',
        marker_color=generate_gradient_colors_simple(len(df_resp), "#1E8449", "#E67E22"),
        text=df_resp["Respondents"],
        textposition='outside',
        textfont=dict(size=11, family="Inter"),
        hovertemplate="<b>%{y}</b><br>Respondents: %{x}<extra></extra>"
    ))
    
    fig_resp_bar.update_layout(
        height=450,
        margin=dict(l=0, r=60, t=20, b=40),
        xaxis=dict(
            title="Number of Respondents",
            gridcolor='#E2E8F0'
        ),
        yaxis=dict(title="", autorange="reversed", tickfont=dict(family="Inter", size=11)),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter")
    )
    
    st.plotly_chart(fig_resp_bar, use_container_width=True)
    
    st.markdown("---")
    
    # Data Quality Box
    st.markdown('<p class="section-title">Data Quality & Validation</p>', unsafe_allow_html=True)
    
    col_qual1, col_qual2, col_qual3 = st.columns(3)
    
    with col_qual1:
        st.markdown("""
        <div class="info-box" style="height: 100%;">
            <div class="info-box-title">✓ Internal Consistency</div>
            <p>All responses reviewed for logical consistency and cross-validated against publicly available data sources.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_qual2:
        st.markdown("""
        <div class="info-box" style="height: 100%;">
            <div class="info-box-title">✓ Bias Detection</div>
            <p>Responses screened for potential reporting bias. Outliers flagged and verified through follow-up interviews.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_qual3:
        st.markdown("""
        <div class="info-box" style="height: 100%;">
            <div class="info-box-title">✓ Expert Validation</div>
            <p>Semi-structured interviews with selected respondents to validate findings and clarify country-specific nuances.</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# FOOTER - ALL PAGES
# ============================================
st.markdown("""
<div class="footer">
    <p><strong>Ease to Mine Index (EMI)</strong> - March 2026</p>
    <p>Report Author: <strong>Valentin Rousseau</strong> - <a href="https://x.com/MuadDib_Pill" target="_blank">@MuadDib_Pill</a></p>
    <p>Research by <a href="https://www.e2cpartners.com/insights/global-bitcoin-mining-report-the-ease-to-mine-index" target="_blank">E2C Partners</a> | 
    Survey of 48 industry practitioners across 19 jurisdictions</p>
</div>
""", unsafe_allow_html=True)
