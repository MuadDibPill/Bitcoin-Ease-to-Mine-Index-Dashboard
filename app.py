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
    
    .section-title-small {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 0.6rem;
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
        font-size: 0.85rem !important;
    }
    
    [data-testid="stSelectbox"] > div > div:hover {
        border-color: #1E8449 !important;
    }
    
    [data-testid="stSelectbox"] > div > div > div {
        font-size: 0.85rem !important;
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
    
    .subtitle-text {
        color: #64748B;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .methodology-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .methodology-card-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.25rem;
    }
    
    .methodology-card-title {
        font-weight: 600;
        color: #1E293B;
        font-size: 0.95rem;
        margin-bottom: 0.25rem;
    }
    
    .methodology-card-desc {
        font-size: 0.8rem;
        color: #64748B;
    }
    
    .timeline-item {
        border-left: 3px solid #002060;
        padding-left: 1rem;
        margin-bottom: 1rem;
    }
    
    .timeline-date {
        font-size: 0.8rem;
        color: #002060;
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
        ratio = i / (n - 1) if n > 1 else 0
        r = max(0, min(255, int(start_r + (end_r - start_r) * ratio)))
        g = max(0, min(255, int(start_g + (end_g - start_g) * ratio)))
        b = max(0, min(255, int(start_b + (end_b - start_b) * ratio)))
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
    page = st.radio("", ["Overview", "Methodology"], label_visibility="collapsed")
    
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
# OVERVIEW PAGE (CREATIVE - NOW MAIN)
# ============================================
if page == "Overview":
    st.markdown("# Ease to Mine Index Dashboard")
    st.markdown('<p class="subtitle-text">Comprehensive analysis of Bitcoin mining regulatory and operating conditions across 19 jurisdictions</p>', unsafe_allow_html=True)
    
    # Map filter - applies to both map and top/bottom 3
    col_filter_main, col_spacer_main = st.columns([1, 3])
    with col_filter_main:
        score_type_main = st.selectbox(
            "Select category",
            ["Overall Index", "Fiscal", "Permits & Licensing", "Legal", "Energy & Grid", "Customs & Tariffs", "Operating Conditions"],
            key="score_filter_main"
        )
    
    selected_col_main = score_map[score_type_main]
    
    # Sort by selected dimension for Top/Bottom 3
    df_sorted = df.sort_values(selected_col_main, ascending=False)
    
    # Map and Top/Bottom 3
    col_map, col_top = st.columns([3, 1])
    
    with col_map:
        st.markdown('<p class="section-title">Ease to Mine Index Map</p>', unsafe_allow_html=True)
        
        df_map = df.copy()
        df_map["ISO"] = df_map["Country"].map(ISO_CODES)
        
        df_map_agg = df_map.groupby("ISO").agg({
            selected_col_main: "mean",
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
            height=540,
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
                bgcolor='rgba(0,0,0,0)',
                lonaxis=dict(range=[-180, 180]),
                lataxis=dict(range=[-55, 85])
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter")
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
    
    with col_top:
        st.markdown('<p class="section-title-small">Top 3 Jurisdictions</p>', unsafe_allow_html=True)
        
        # Get min/max for the selected dimension
        min_score_dim = df[selected_col_main].min()
        max_score_dim = df[selected_col_main].max()
        
        for idx, (i, row) in enumerate(df_sorted.head(3).iterrows()):
            rank = idx + 1
            score_val = row[selected_col_main]
            color = get_score_color(score_val, min_score_dim, max_score_dim)
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, {color}22 0%, transparent 100%); 
                        border-left: 4px solid {color}; 
                        padding: 10px 12px; 
                        margin-bottom: 8px; 
                        border-radius: 0 8px 8px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-weight: 700; color: #1E293B; font-size: 0.9rem;">#{rank} {row['Country']}</span>
                        <span style="color: #64748B; font-size: 0.9rem; margin-left: 6px;">{row['Region']}</span>
                    </div>
                    <div style="font-weight: 700; font-size: 1rem; color: {color};">{score_val:.2f}</div>
                </div>
                <div style="font-size: 0.7rem; color: #64748B; margin-top: 2px;">
                    Hashrate: {row['Hashrate_Q1_26']:.1f} EH/s
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("")
        st.markdown('<p class="section-title-small" style="margin-top: 0.5rem;">Bottom 3 Jurisdictions</p>', unsafe_allow_html=True)
        
        # Bottom 3 in order 17, 18, 19 (from best to worst among bottom)
        bottom_3 = df_sorted.tail(3)
        for idx, (i, row) in enumerate(bottom_3.iterrows()):
            rank = 17 + idx
            score_val = row[selected_col_main]
            color = get_score_color(score_val, min_score_dim, max_score_dim)
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, {color}22 0%, transparent 100%); 
                        border-left: 4px solid {color}; 
                        padding: 10px 12px; 
                        margin-bottom: 8px; 
                        border-radius: 0 8px 8px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-weight: 700; color: #1E293B; font-size: 0.9rem;">#{rank} {row['Country']}</span>
                        <span style="color: #64748B; font-size: 0.9rem; margin-left: 6px;">{row['Region']}</span>
                    </div>
                    <div style="font-weight: 700; font-size: 1rem; color: {color};">{score_val:.2f}</div>
                </div>
                <div style="font-size: 0.7rem; color: #64748B; margin-top: 2px;">
                    Hashrate: {row['Hashrate_Q1_26']:.1f} EH/s
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # EMI Ranking with text box
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
    
    min_score_r = df_rank[rank_col].min()
    max_score_r = df_rank[rank_col].max()
    colors_r = [get_score_color(score, min_score_r, max_score_r) for score in df_rank[rank_col]]
    
    col_chart, col_text = st.columns([2, 1])
    
    with col_chart:
        fig_rank = go.Figure(go.Bar(
            x=df_rank[rank_col],
            y=df_rank["Country"],
            orientation='h',
            marker_color=colors_r,
            text=df_rank[rank_col].round(2),
            textposition='outside',
            textfont=dict(size=13, family="Inter"),
            name=rank_dimension
        ))
        
        fig_rank.update_layout(
            height=560,
            margin=dict(l=0, r=60, t=10, b=40),
            xaxis=dict(range=[0, 1], title=dict(text=rank_dimension + " Score", font=dict(family="Inter", size=12)), gridcolor='#E2E8F0', zeroline=False),
            yaxis=dict(title="", tickfont=dict(family="Inter", size=13)),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter")
        )
        
        st.plotly_chart(fig_rank, use_container_width=True)
    
    with col_text:
        st.markdown("""
        <div class="info-box">
            <div class="info-box-title" style="font-size: 1.1rem; margin-bottom: 0.75rem;">EMI Description</div>
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
                font=dict(color=get_text_color_for_score(val), size=12, family="Inter")
            ))
    
    fig_heat.update_layout(annotations=annotations)
    fig_heat.update_layout(
        height=550,
        margin=dict(l=0, r=0, t=10, b=40),
        xaxis=dict(title="", tickangle=0, side="bottom", tickfont=dict(family="Inter", size=13)),
        yaxis=dict(title="", autorange="reversed", tickfont=dict(family="Inter", size=13)),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter")
    )
    
    st.plotly_chart(fig_heat, use_container_width=True)
    
    st.markdown("---")
    
    # Full Data Table
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
# METHODOLOGY PAGE (CREATIVE - NOW MAIN)
# ============================================
elif page == "Methodology":
    st.markdown("# Methodology")
    st.markdown("How we built the Ease to Mine Index")
    
    st.markdown("")
    
    # Key Stats Cards - No icons, black numbers
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="methodology-card">
            <div class="methodology-card-value">48</div>
            <div class="methodology-card-title">Respondents</div>
            <div class="methodology-card-desc">Industrial Miners, Association, Journalist & Experts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="methodology-card">
            <div class="methodology-card-value">55</div>
            <div class="methodology-card-title">Responses</div>
            <div class="methodology-card-desc">Total survey submissions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="methodology-card">
            <div class="methodology-card-value">19</div>
            <div class="methodology-card-title">Jurisdictions</div>
            <div class="methodology-card-desc">Including Québec & Alberta for Canada</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="methodology-card">
            <div class="methodology-card-value">33</div>
            <div class="methodology-card-title">Questions</div>
            <div class="methodology-card-desc">Across 5 survey sections</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Timeline + Weighting Pie Chart
    col_timeline, col_pie_weight = st.columns([1, 1])
    
    with col_timeline:
        st.markdown('<p class="section-title">Survey Timeline</p>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="timeline-item">
            <div class="timeline-date">December 2025</div>
            <div class="timeline-title">Survey Launch</div>
            <div class="timeline-desc">Online survey deployed targeting Bitcoin mining ecosystem stakeholders</div>
        </div>
        
        <div class="timeline-item">
            <div class="timeline-date">January - February 2026</div>
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
            <div class="timeline-desc">Ease to Mine Index released with comprehensive analysis across 19 jurisdictions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_pie_weight:
        st.markdown('<p class="section-title">Index Weighting</p>', unsafe_allow_html=True)
        
        weights_data = {
            'Section': ['Energy & Grid', 'Fiscal', 'Legal', 'Permits & Licensing', 'Customs & Tariffs', 'Operating Conditions'],
            'Weight': [25, 20, 17.5, 17.5, 15, 5]
        }
        
        # Blue color scheme for Methodology
        weight_colors = ['#A7BCF7', '#6287F0', '#0D6FFF', '#1D0DED', '#002060', '#12E09B']
        
        fig_pie_weight = go.Figure(go.Pie(
            labels=weights_data['Section'],
            values=weights_data['Weight'],
            hole=0.45,
            marker=dict(colors=weight_colors),
            textinfo='percent',
            textposition='outside',
            textfont=dict(size=12, family="Inter"),
            texttemplate='%{percent:.1%}',
            hovertemplate="<b>%{label}</b><br>Weight: %{value}%<extra></extra>"
        ))
        
        fig_pie_weight.add_annotation(
            text="<b>Weight</b><br><span style='font-size:13px'>(%)</span>",
            x=0.5, y=0.5,
            font=dict(size=16, color="#1E293B", family="Inter"),
            showarrow=False
        )
        
        fig_pie_weight.update_layout(
            height=340,
            margin=dict(l=20, r=140, t=20, b=20),
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.02,
                font=dict(size=11, family="Inter")
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter")
        )
        
        st.plotly_chart(fig_pie_weight, use_container_width=True)
    
    st.markdown("---")
    
    # Data Quality & Validation
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
    
    st.markdown("---")
    
    # Geographic Distribution + Survey Methodology Box
    st.markdown('<p class="section-title">Geographic Distribution of Respondents</p>', unsafe_allow_html=True)
    
    df_resp = df.copy()
    canada_resp = df_resp[df_resp["Country"].isin(["Alberta (CA)", "Quebec (CA)"])]["Respondents"].sum()
    df_resp = df_resp[~df_resp["Country"].isin(["Alberta (CA)", "Quebec (CA)"])]
    df_resp = pd.concat([df_resp, pd.DataFrame([{"Country": "Canada", "Respondents": canada_resp, "Region": "North America"}])], ignore_index=True)
    df_resp = df_resp[df_resp["Respondents"] > 0].sort_values("Respondents", ascending=False)
    total_respondents = df_resp["Respondents"].sum()
    
    # Adjusted column ratio: 60% chart, 40% text (reduced by 15%)
    col_bar, col_method_box = st.columns([1.2, 0.8])
    
    with col_bar:
        fig_resp_bar = go.Figure(go.Bar(
            x=df_resp["Respondents"],
            y=df_resp["Country"],
            orientation='h',
            marker_color='#1E293B',
            text=df_resp["Respondents"],
            textposition='outside',
            textfont=dict(size=12, family="Inter"),
            hovertemplate="<b>%{y}</b><br>Respondents: %{x}<extra></extra>"
        ))
        
        fig_resp_bar.update_layout(
            height=450,
            margin=dict(l=0, r=60, t=20, b=40),
            xaxis=dict(title="Number of Respondents", gridcolor='#E2E8F0'),
            yaxis=dict(title="", autorange="reversed", tickfont=dict(family="Inter", size=12)),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter")
        )
        
        st.plotly_chart(fig_resp_bar, use_container_width=True)
    
    with col_method_box:
        st.markdown("""
        <div class="info-box" style="height: 100%;">
            <div class="method-box-title">Survey Methodology</div>
            <p>Between December 2025 and February 2026, Hashlabs conducted an online survey targeting stakeholders within the Bitcoin mining ecosystem, including industrial miners, mining associations, industry journalists, and other experts.</p>
            <p style="margin-top: 0.75rem;"><strong>Survey scope:</strong> 5 sections covering legal, fiscal, energy & electricity grids, permitting & licensing, and tariffs & customs procedures. A total of 33 questions combined quantitative metrics with qualitative assessments.</p>
            <p style="margin-top: 0.75rem;"><strong>Data validation:</strong> Responses were reviewed for internal consistency and potential reporting bias. Follow-up semi-structured interviews were conducted with selected respondents to validate findings and clarify country-specific conditions.</p>
            <p style="margin-top: 0.75rem; padding: 0.5rem; background-color: #FEF3C7; border-radius: 4px; font-size: 0.85rem;"><strong>Note:</strong> The Climate Operating Conditions (C.O.C.) section is beyond survey scope and based on internal analysis.</p>
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
