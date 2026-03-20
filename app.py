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
    
    /* Hide radio button circles */
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
# OVERVIEW PAGE
# ============================================
if page == "Overview":
    st.markdown("# Ease to Mine Index Dashboard")
    st.markdown("Comprehensive analysis of Bitcoin mining regulatory and operating conditions across 19 jurisdictions")
    
    # ========================================
    # FILTER FOR MAP
    # ========================================
    col_filter, col_spacer = st.columns([1, 3])
    with col_filter:
        score_type = st.selectbox(
            "Select dimension",
            ["Overall Index", "Fiscal", "Permits & Licensing", "Legal", "Energy & Grid", "Customs & Tariffs", "Operating Conditions"],
            key="score_filter"
        )
    
    score_map = {
        "Overall Index": "Index_Score",
        "Fiscal": "Fiscal",
        "Permits & Licensing": "Permit_Licensing",
        "Legal": "Legal",
        "Energy & Grid": "Energy_Grid",
        "Customs & Tariffs": "Tariff_Import",
        "Operating Conditions": "Operating_Conditions"
    }
    selected_col = score_map[score_type]
    
    # ========================================
    # WORLD MAP - REDUCED TO 520px
    # ========================================
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
    
    # ========================================
    # HEATMAP
    # ========================================
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
    
    # ========================================
    # EMI RANKING WITH TEXT SECTION
    # ========================================
    st.markdown('<p class="section-title">EMI Ranking</p>', unsafe_allow_html=True)
    
    col_rank_filter, col_rank_spacer = st.columns([1, 3])
    with col_rank_filter:
        rank_dimension = st.selectbox(
            "Select dimension",
            ["Overall Index", "Fiscal", "Permits & Licensing", "Legal", "Energy & Grid", "Customs & Tariffs", "Operating Conditions"],
            key="rank_filter"
        )
    
    rank_col = score_map[rank_dimension]
    df_rank = df.sort_values(rank_col, ascending=True).copy()
    
    min_score = df_rank[rank_col].min()
    max_score = df_rank[rank_col].max()
    colors = [get_score_color(score, min_score, max_score) for score in df_rank[rank_col]]
    
    # Two columns: chart + text
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
            <p>The index evaluates a broad set of dimensions:</p>
            <ul style="margin: 0.5rem 0; padding-left: 1.2rem;">
                <li>Legal and fiscal frameworks</li>
                <li>Permitting and licensing conditions</li>
                <li>Energy market structure and grid access</li>
                <li>Climate characteristics</li>
                <li>Tariff and import environments</li>
            </ul>
            <p>While mining analysis traditionally emphasizes operational metrics (power costs, hashprice), regulatory conditions are often underweighted. By integrating both perspectives, the EMI provides a more holistic assessment of mining sustainability.</p>
            <p style="margin-top: 0.75rem;"><strong>Coverage:</strong> 18 countries spanning established mining regions (excluding China) and emerging markets such as DRC, Kenya, and Chile.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================
    # FULL DATA TABLE
    # ========================================
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
# METHODOLOGY PAGE
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
    
    # ========================================
    # RESPONDENTS PIE CHART WITH TEXT
    # ========================================
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
            text="<b>55</b><br><span style='font-size:12px'>Total<br>responses</span>",
            x=0.5, y=0.5,
            font=dict(size=32, color="#1E293B", family="Inter"),
            showarrow=False
        )
        
        fig_pie.update_layout(
            height=420,
            margin=dict(l=40, r=40, t=20, b=20),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter")
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_method:
        st.markdown("""
        <div class="info-box">
            <div class="info-box-title">Survey Methodology</div>
            <p>Between December 2025 and February 2026, Hashlabs conducted an online survey targeting stakeholders within the Bitcoin mining ecosystem, including industrial miners, mining associations, industry journalists, and other experts.</p>
            <p style="margin-top: 0.75rem;"><strong>Survey scope:</strong> 5 sections covering legal, fiscal, energy & electricity grids, permitting & licensing, and tariffs & customs procedures. A total of 33 questions combined quantitative metrics with qualitative assessments.</p>
            <p style="margin-top: 0.75rem;"><strong>Data validation:</strong> Responses were reviewed for internal consistency and potential reporting bias. Follow-up semi-structured interviews were conducted with selected respondents to validate findings and clarify country-specific conditions.</p>
            <p style="margin-top: 0.75rem; padding: 0.5rem; background-color: #FEF3C7; border-radius: 4px; font-size: 0.85rem;"><strong>Note:</strong> The Climate Operating Conditions section is beyond survey scope and based on internal analysis.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================
    # WEIGHTING STACKED BAR CHART - LARGER
    # ========================================
    st.markdown('<p class="section-title">Index Weighting by Dimension</p>', unsafe_allow_html=True)
    
    fig_weights = go.Figure()
    
    weights_main = [
        ("Energy & Grid", 25, "#1E8449", "white"),
        ("Fiscal", 20, "#28B463", "white"),
        ("Legal", 17.5, "#7DCEA0", "black"),
        ("Permits & Licensing", 17.5, "#F4D03F", "black"),
        ("Customs & Tariffs", 15, "#E67E22", "white"),
        ("Operating Cond.", 5, "#922B21", "white")
    ]
    
    for name, weight, color, text_color in weights_main:
        if weight <= 5:
            text_inside = ""
        else:
            text_inside = f"{name}<br>{weight}%"
        
        fig_weights.add_trace(go.Bar(
            name=name,
            x=[weight],
            y=["EMI Index"],
            orientation='h',
            marker_color=color,
            text=[text_inside],
            textposition='inside',
            insidetextanchor='middle',
            textfont=dict(size=13, family="Inter", color=text_color),
            hovertemplate=f"<b>{name}</b><br>Weight: {weight}%<extra></extra>"
        ))
    
    fig_weights.add_annotation(
        x=97.5,
        y="EMI Index",
        yshift=70,
        text="<b>Operating Conditions: 5%</b>",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#922B21",
        ax=0,
        ay=-55,
        font=dict(size=13, family="Inter", color="#1E293B"),
        bgcolor="#FFFFFF",
        bordercolor="#922B21",
        borderwidth=2,
        borderpad=8
    )
    
    fig_weights.update_layout(
        barmode='stack',
        height=180,
        margin=dict(l=0, r=0, t=90, b=20),
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
    
    # ========================================
    # RESPONDENTS TABLE
    # ========================================
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
# FOOTER - BOTH PAGES
# ============================================
st.markdown("""
<div class="footer">
    <p><strong>Ease to Mine Index (EMI)</strong> - March 2026</p>
    <p>Report Author: <strong>Valentin Rousseau</strong> - <a href="https://x.com/MuadDib_Pill" target="_blank">@MuadDib_Pill</a></p>
    <p>Research by <a href="https://www.e2cpartners.com/insights/global-bitcoin-mining-report-the-ease-to-mine-index" target="_blank">E2C Partners</a> | 
    Survey of 48 industry practitioners across 19 jurisdictions</p>
</div>
""", unsafe_allow_html=True)
