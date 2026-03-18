import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="EMI Dashboard | Hashlabs",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# DARK FINANCIAL THEME - CUSTOM CSS
# ============================================
st.markdown("""
<style>
    /* Import Inter font - clean financial look */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global dark theme */
    .stApp {
        background-color: #0a0a0f;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #0f1118;
        border-right: 1px solid #1e2530;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #8bb8e8;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #5ba4e8 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em;
    }
    
    h1 {
        font-size: 2.2rem !important;
        border-bottom: 2px solid #1a3a5c;
        padding-bottom: 0.5rem;
    }
    
    h2 {
        font-size: 1.4rem !important;
        color: #7ab8f0 !important;
    }
    
    h3 {
        font-size: 1.1rem !important;
        color: #6aaae5 !important;
    }
    
    /* Body text */
    p, span, div {
        color: #a8c5e2;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #5ba4e8 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.8rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #6a8caa !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        font-size: 0.75rem !important;
        letter-spacing: 0.05em;
    }
    
    [data-testid="stMetricDelta"] {
        color: #4ecdc4 !important;
    }
    
    /* Metric cards background */
    [data-testid="metric-container"] {
        background-color: #111827;
        border: 1px solid #1e2530;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Radio buttons / Navigation */
    .stRadio > label {
        color: #8bb8e8 !important;
        font-weight: 500;
    }
    
    .stRadio > div {
        background-color: transparent;
    }
    
    .stRadio > div > label {
        background-color: #111827 !important;
        border: 1px solid #1e2530 !important;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        margin: 0.25rem 0;
        color: #8bb8e8 !important;
        transition: all 0.2s ease;
    }
    
    .stRadio > div > label:hover {
        background-color: #1a2744 !important;
        border-color: #2a4a6a !important;
    }
    
    .stRadio > div > label[data-checked="true"] {
        background-color: #1a3a5c !important;
        border-color: #5ba4e8 !important;
        color: #5ba4e8 !important;
    }
    
    /* Multiselect */
    .stMultiSelect > div > div {
        background-color: #111827;
        border-color: #1e2530;
        color: #8bb8e8;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #111827 !important;
        border: 1px solid #1e2530 !important;
        border-radius: 6px;
        color: #8bb8e8 !important;
        font-weight: 500;
    }
    
    .streamlit-expanderContent {
        background-color: #0d1117 !important;
        border: 1px solid #1e2530 !important;
        border-top: none !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #111827;
        border: 1px solid #1e2530;
        border-radius: 6px;
        color: #8bb8e8;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1a3a5c !important;
        border-color: #5ba4e8 !important;
        color: #5ba4e8 !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        background-color: #111827;
        border: 1px solid #1e2530;
        border-radius: 8px;
    }
    
    /* Divider */
    hr {
        border-color: #1e2530;
    }
    
    /* Links */
    a {
        color: #5ba4e8 !important;
    }
    
    /* Custom classes */
    .main-title {
        color: #5ba4e8;
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        margin-bottom: 0;
    }
    
    .subtitle {
        color: #6a8caa;
        font-size: 1rem;
        font-weight: 400;
        margin-top: 0.25rem;
    }
    
    .section-header {
        color: #5ba4e8;
        font-size: 1.1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #1e2530;
    }
    
    .metric-highlight {
        background: linear-gradient(135deg, #1a3a5c 0%, #0f2744 100%);
        border: 1px solid #2a5a8c;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .legend-item {
        display: inline-flex;
        align-items: center;
        margin-right: 1.5rem;
        color: #8bb8e8;
        font-size: 0.85rem;
    }
    
    .legend-dot {
        width: 12px;
        height: 12px;
        border-radius: 3px;
        margin-right: 6px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #4a6a8a;
        padding: 2rem;
        font-size: 0.85rem;
        border-top: 1px solid #1e2530;
        margin-top: 2rem;
    }
    
    .footer a {
        color: #5ba4e8 !important;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# PLOTLY THEME
# ============================================
PLOT_COLORS = {
    'excellent': '#10b981',  # Green
    'good': '#3b82f6',       # Blue  
    'neutral': '#f59e0b',    # Amber
    'poor': '#ef4444',       # Red
    'background': '#0a0a0f',
    'paper': '#111827',
    'grid': '#1e2530',
    'text': '#8bb8e8',
    'title': '#5ba4e8'
}

def get_score_color(score):
    if score >= 0.6:
        return PLOT_COLORS['excellent']
    elif score >= 0.5:
        return PLOT_COLORS['good']
    elif score >= 0.4:
        return PLOT_COLORS['neutral']
    else:
        return PLOT_COLORS['poor']

def style_plotly_chart(fig, height=500):
    fig.update_layout(
        height=height,
        plot_bgcolor=PLOT_COLORS['background'],
        paper_bgcolor=PLOT_COLORS['paper'],
        font=dict(family="Inter, sans-serif", color=PLOT_COLORS['text']),
        title_font=dict(color=PLOT_COLORS['title'], size=16),
        margin=dict(l=20, r=40, t=40, b=40),
        xaxis=dict(
            gridcolor=PLOT_COLORS['grid'],
            zerolinecolor=PLOT_COLORS['grid'],
            tickfont=dict(color=PLOT_COLORS['text'])
        ),
        yaxis=dict(
            gridcolor=PLOT_COLORS['grid'],
            zerolinecolor=PLOT_COLORS['grid'],
            tickfont=dict(color=PLOT_COLORS['text'])
        ),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            font=dict(color=PLOT_COLORS['text'])
        )
    )
    return fig

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_data():
    scores = pd.read_csv("data/emi_scores.csv")
    detailed = pd.read_csv("data/detailed_responses.csv")
    return scores, detailed

df_scores, df_detailed = load_data()

# ============================================
# SIDEBAR NAVIGATION
# ============================================
with st.sidebar:
    st.image("https://framerusercontent.com/images/H3JhLauLgPETCRKMoj3axnBKME.png", width=160)
    st.markdown("---")
    
    st.markdown('<p class="section-header">Navigation</p>', unsafe_allow_html=True)
    
    sections = [
        "🏠 Overview",
        "💰 Fiscal",
        "📋 Permitting & Licensing", 
        "⚖️ Legal",
        "⚡ Energy & Grid",
        "🚢 Customs & Tariffs"
    ]
    selected_section = st.radio("", sections, label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown('<p class="section-header">Filters</p>', unsafe_allow_html=True)
    
    selected_regions = st.multiselect(
        "Regions",
        df_scores["Region"].unique(),
        default=df_scores["Region"].unique()
    )

# Filter data
df_filtered = df_scores[df_scores["Region"].isin(selected_regions)]
df_detailed_filtered = df_detailed[df_detailed["Region"].isin(selected_regions)]

# ============================================
# HELPER FUNCTIONS
# ============================================
def show_regional_header(section_col, section_name):
    """Display regional averages as header metrics"""
    st.markdown(f'<p class="section-header">Regional Performance — {section_name}</p>', unsafe_allow_html=True)
    
    regional_avg = df_filtered.groupby("Region")[section_col].mean().sort_values(ascending=False)
    
    cols = st.columns(len(regional_avg) + 1)
    
    # Global average first
    with cols[0]:
        global_avg = df_filtered[section_col].mean()
        st.metric("🌍 Global", f"{global_avg:.2f}")
    
    # Regional averages
    for i, (region, avg) in enumerate(regional_avg.items()):
        with cols[i + 1]:
            emoji = "🏆" if i == 0 else ""
            st.metric(f"{emoji} {region}", f"{avg:.2f}")

def show_country_ranking(section_col, title):
    """Display country ranking with dark theme"""
    df_sorted = df_filtered.sort_values(section_col, ascending=True)
    
    colors = [get_score_color(x) for x in df_sorted[section_col]]
    
    fig = go.Figure(go.Bar(
        x=df_sorted[section_col],
        y=df_sorted["Country"],
        orientation='h',
        marker_color=colors,
        text=df_sorted[section_col].round(2),
        textposition='outside',
        textfont=dict(color=PLOT_COLORS['text'], size=11)
    ))
    
    fig.update_layout(
        xaxis=dict(range=[0, 1], title="Score", title_font=dict(color=PLOT_COLORS['text'])),
        yaxis=dict(title=""),
    )
    
    fig = style_plotly_chart(fig, height=580)
    st.plotly_chart(fig, use_container_width=True)
    
    # Legend
    st.markdown("""
    <div style="display: flex; flex-wrap: wrap; gap: 1.5rem; margin-top: 1rem;">
        <span class="legend-item"><span class="legend-dot" style="background: #10b981;"></span>Excellent (≥0.60)</span>
        <span class="legend-item"><span class="legend-dot" style="background: #3b82f6;"></span>Good (0.50-0.59)</span>
        <span class="legend-item"><span class="legend-dot" style="background: #f59e0b;"></span>Neutral (0.40-0.49)</span>
        <span class="legend-item"><span class="legend-dot" style="background: #ef4444;"></span>Poor (<0.40)</span>
    </div>
    """, unsafe_allow_html=True)

def show_question_breakdown(section_name, questions_list):
    """Display breakdown by question with response distribution"""
    st.markdown('<p class="section-header">Detailed Question Analysis</p>', unsafe_allow_html=True)
    
    section_data = df_detailed_filtered[df_detailed_filtered["Section"] == section_name]
    
    for question in questions_list:
        q_data = section_data[section_data["Question"] == question]
        
        if len(q_data) > 0:
            with st.expander(f"📊 {question} — {len(q_data)} responses"):
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    response_counts = q_data["Response"].value_counts()
                    
                    fig = go.Figure(go.Pie(
                        labels=response_counts.index,
                        values=response_counts.values,
                        hole=0.5,
                        marker=dict(colors=px.colors.sequential.Blues_r),
                        textinfo='percent',
                        textfont=dict(color='white', size=11)
                    ))
                    fig.update_layout(
                        showlegend=True,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=-0.3,
                            font=dict(size=10)
                        )
                    )
                    fig = style_plotly_chart(fig, height=300)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    country_responses = q_data.groupby("Country")["Response"].apply(
                        lambda x: ", ".join(x.unique())
                    ).reset_index()
                    country_responses.columns = ["Country", "Response(s)"]
                    st.dataframe(
                        country_responses,
                        use_container_width=True,
                        hide_index=True,
                        height=280
                    )

def show_duration_chart(section_name, question_name, title):
    """Chart for duration-type questions"""
    section_data = df_detailed_filtered[
        (df_detailed_filtered["Section"] == section_name) & 
        (df_detailed_filtered["Question"] == question_name)
    ]
    
    duration_map = {
        'less than 3 months': 1.5, '3 – 6 months': 4.5, '3 - 6 months': 4.5,
        '6 – 9 months': 7.5, '6 - 9 months': 7.5, '9 – 12 months': 10.5,
        '9 - 12 months': 10.5, '12 – 18 months': 15, '12 - 18 months': 15,
        '18 – 24 months': 21, '18 - 24 months': 21, '> 24 months': 30,
        'more than 12 months': 15,
    }
    
    country_durations = []
    for country in section_data["Country"].unique():
        country_data = section_data[section_data["Country"] == country]
        durations = []
        for resp in country_data["Response"]:
            for key, val in duration_map.items():
                if key.lower() in resp.lower():
                    durations.append(val)
                    break
        if durations:
            country_durations.append({
                "Country": country,
                "Duration": sum(durations) / len(durations),
                "Region": country_data["Region"].iloc[0]
            })
    
    if country_durations:
        df_duration = pd.DataFrame(country_durations).sort_values("Duration")
        
        def get_duration_color(d):
            if d < 6: return PLOT_COLORS['excellent']
            elif d < 12: return PLOT_COLORS['good']
            elif d < 18: return PLOT_COLORS['neutral']
            else: return PLOT_COLORS['poor']
        
        colors = [get_duration_color(d) for d in df_duration["Duration"]]
        
        fig = go.Figure(go.Bar(
            x=df_duration["Duration"],
            y=df_duration["Country"],
            orientation='h',
            marker_color=colors,
            text=[f"{d:.1f} mo" for d in df_duration["Duration"]],
            textposition='outside',
            textfont=dict(color=PLOT_COLORS['text'], size=11)
        ))
        
        fig.update_layout(
            xaxis=dict(title="Duration (months)", title_font=dict(color=PLOT_COLORS['text'])),
            yaxis=dict(title=""),
        )
        
        fig = style_plotly_chart(fig, height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div style="display: flex; flex-wrap: wrap; gap: 1.5rem; margin-top: 1rem;">
            <span class="legend-item"><span class="legend-dot" style="background: #10b981;"></span>Fast (<6 mo)</span>
            <span class="legend-item"><span class="legend-dot" style="background: #3b82f6;"></span>Moderate (6-12 mo)</span>
            <span class="legend-item"><span class="legend-dot" style="background: #f59e0b;"></span>Slow (12-18 mo)</span>
            <span class="legend-item"><span class="legend-dot" style="background: #ef4444;"></span>Very slow (>18 mo)</span>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# MAIN CONTENT
# ============================================

# --- OVERVIEW ---
if selected_section == "🏠 Overview":
    st.markdown('<h1 class="main-title">⛏️ Ease to Mine Index</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Comprehensive analysis of Bitcoin mining conditions across 19 jurisdictions</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        best = df_filtered.loc[df_filtered["Index_Score"].idxmax()]
        st.metric("🏆 TOP JURISDICTION", best["Country"], f"Score: {best['Index_Score']:.2f}")
    
    with col2:
        st.metric("📊 GLOBAL AVERAGE", f"{df_filtered['Index_Score'].mean():.2f}", f"{len(df_filtered)} countries")
    
    with col3:
        best_energy = df_filtered.loc[df_filtered["Energy_Grid"].idxmax()]
        st.metric("⚡ BEST ENERGY", best_energy["Country"], f"{best_energy['Energy_Grid']:.2f}")
    
    with col4:
        fastest = df_filtered.loc[df_filtered["Permit_Months"].idxmin()]
        st.metric("⏱️ FASTEST PERMITS", fastest["Country"], f"{fastest['Permit_Months']:.1f} months")
    
    st.markdown("---")
    
    # Two columns: Ranking + Regional heatmap
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("### 🏆 Overall EMI Ranking")
        show_country_ranking("Index_Score", "Overall EMI Score")
    
    with col2:
        st.markdown("### 🌍 Regional Comparison")
        
        # Heatmap by region and dimension
        dims = ["Fiscal", "Permit_Licensing", "Legal", "Energy_Grid", "Tariff_Import"]
        dim_labels = ["Fiscal", "Permits", "Legal", "Energy", "Tariffs"]
        
        regional_data = df_filtered.groupby("Region")[dims].mean()
        
        fig = go.Figure(go.Heatmap(
            z=regional_data.values,
            x=dim_labels,
            y=regional_data.index,
            colorscale=[[0, '#1e3a5c'], [0.5, '#3b82f6'], [1, '#10b981']],
            text=regional_data.values.round(2),
            texttemplate="%{text}",
            textfont=dict(color="white", size=11),
            hovertemplate="Region: %{y}<br>Dimension: %{x}<br>Score: %{z:.2f}<extra></extra>"
        ))
        
        fig = style_plotly_chart(fig, height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Scatter: EMI vs Permit Time
        st.markdown("### ⏱️ Score vs. Permit Speed")
        
        fig = go.Figure()
        
        for region in df_filtered["Region"].unique():
            region_data = df_filtered[df_filtered["Region"] == region]
            fig.add_trace(go.Scatter(
                x=region_data["Permit_Months"],
                y=region_data["Index_Score"],
                mode='markers+text',
                name=region,
                text=region_data["Country"],
                textposition="top center",
                textfont=dict(size=9, color=PLOT_COLORS['text']),
                marker=dict(size=12, opacity=0.8)
            ))
        
        fig.update_layout(
            xaxis=dict(title="Permit Timeline (months)"),
            yaxis=dict(title="EMI Score", range=[0.2, 0.85]),
        )
        
        fig = style_plotly_chart(fig, height=400)
        st.plotly_chart(fig, use_container_width=True)


# --- FISCAL ---
elif selected_section == "💰 Fiscal":
    st.markdown('<h1 class="main-title">💰 Fiscal Environment</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Tax policies, subsidies, and fiscal incentives</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    show_regional_header("Fiscal", "Fiscal")
    st.markdown("---")
    
    st.markdown("### 🏆 Country Ranking — Fiscal Score")
    show_country_ranking("Fiscal", "Fiscal Score")
    st.markdown("---")
    
    fiscal_questions = [
        "Taxation environment", "Shift profit center possible", "Electricity tax exposure",
        "Tax abatements available", "Constraint to access benefits", "Corporate Income Tax (CIT)"
    ]
    show_question_breakdown("Fiscal", fiscal_questions)


# --- PERMITTING ---
elif selected_section == "📋 Permitting & Licensing":
    st.markdown('<h1 class="main-title">📋 Permitting & Licensing</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Construction permits, licenses, and regulatory approvals</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    show_regional_header("Permit_Licensing", "Permitting")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 Country Ranking")
        show_country_ranking("Permit_Licensing", "Permitting Score")
    
    with col2:
        st.markdown("### ⏱️ Construction Permit Timeline")
        show_duration_chart("Permitting", "Construction permit timeline", "Construction Permits")
    
    st.markdown("---")
    
    permit_questions = [
        "Operational license timeline", "ASIC import license required", "Construction permit timeline",
        "EIA complexity", "Water permits restrictiveness", "Heat/noise/emissions regulations", "Zoning restrictions impact"
    ]
    show_question_breakdown("Permitting", permit_questions)


# --- LEGAL ---
elif selected_section == "⚖️ Legal":
    st.markdown('<h1 class="main-title">⚖️ Legal Framework</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Regulatory environment and legislative outlook</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    show_regional_header("Legal", "Legal")
    st.markdown("---")
    
    st.markdown("### 🏆 Country Ranking — Legal Score")
    show_country_ranking("Legal", "Legal Score")
    st.markdown("---")
    
    legal_questions = ["Regulatory environment", "Framework evolution outlook", "Legislative risk"]
    show_question_breakdown("Legal", legal_questions)


# --- ENERGY ---
elif selected_section == "⚡ Energy & Grid":
    st.markdown('<h1 class="main-title">⚡ Energy & Grid Access</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Grid connectivity, energy prices, and access barriers</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    show_regional_header("Energy_Grid", "Energy & Grid")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 Country Ranking")
        show_country_ranking("Energy_Grid", "Energy Score")
    
    with col2:
        st.markdown("### ⏱️ Grid Connection Lead Time")
        show_duration_chart("Energy", "Grid connection lead time", "Grid Connection")
    
    st.markdown("---")
    
    energy_questions = ["Grid access barriers", "Grid connection lead time", "Electricity price", "Regulatory status for miners"]
    show_question_breakdown("Energy", energy_questions)


# --- CUSTOMS ---
elif selected_section == "🚢 Customs & Tariffs":
    st.markdown('<h1 class="main-title">🚢 Customs & Tariffs</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Import procedures, VAT, and trade barriers</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    show_regional_header("Tariff_Import", "Customs & Tariffs")
    st.markdown("---")
    
    st.markdown("### 🏆 Country Ranking — Customs Score")
    show_country_ranking("Tariff_Import", "Customs Score")
    st.markdown("---")
    
    customs_questions = [
        "VAT rate", "VAT filing burden", "ASIC import process", "Electrical infra import",
        "Tariff on China imports", "Procurement lead times", "Mitigation effectiveness"
    ]
    show_question_breakdown("Customs", customs_questions)


# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="footer">
    <p><strong>Ease to Mine Index (EMI)</strong> — First Edition 2026</p>
    <p>Research by <a href="https://hashlabs.io" target="_blank">Hashlabs</a> | 
    Survey of 48 industry practitioners across 19 jurisdictions</p>
</div>
""", unsafe_allow_html=True)
