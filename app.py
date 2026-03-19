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
# COLOR PALETTE - DARKER TONES
# ============================================
COLORS = {
    'primary': '#1E3A8A',      # Dark Blue
    'secondary': '#B45309',    # Dark Orange
    'success': '#166534',      # Dark Green
    'danger': '#991B1B',       # Dark Red
    'purple': '#5B21B6',       # Dark Purple
    'cyan': '#0E7490',         # Dark Cyan
    'text': '#1E293B',
    'text_muted': '#64748B',
    'border': '#E2E8F0'
}

# ============================================
# CUSTOM CSS - REDUCED SIDEBAR WIDTH
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #FFFFFF;
    }
    
    /* Reduce sidebar width by 15% */
    [data-testid="stSidebar"] {
        width: 255px !important;
        min-width: 255px !important;
        background-color: #FAFAFA;
        border-right: 1px solid #E2E8F0;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        width: 255px !important;
    }
    
    /* Reduce top padding */
    .block-container {
        padding-top: 1rem !important;
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
        color: #1E3A8A;
        text-decoration: none;
    }
    
    .footer a:hover {
        text-decoration: underline;
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
def get_score_color_dark(score, min_score, max_score):
    """Get darker color based on score"""
    if max_score == min_score:
        ratio = 0.5
    else:
        ratio = (score - min_score) / (max_score - min_score)
    
    ratio = max(0.0, min(1.0, ratio))
    
    # Darker gradient: Dark Red -> Dark Orange -> Dark Yellow -> Dark Green -> Dark Blue
    if ratio < 0.5:
        t = ratio * 2
        r = int(153 + (180 - 153) * t)
        g = int(27 + (130 - 27) * t)
        b = int(27 + (20 - 27) * t)
    else:
        t = (ratio - 0.5) * 2
        r = int(180 + (30 - 180) * t)
        g = int(130 + (58 - 130) * t)
        b = int(20 + (138 - 20) * t)
    
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))
    
    return f'#{r:02x}{g:02x}{b:02x}'

def generate_gradient_colors_simple(n, start_hex="#1E3A8A", end_hex="#B45309"):
    """Generate n colors as gradient"""
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

# ============================================
# SIDEBAR NAVIGATION - UPDATED
# ============================================
with st.sidebar:
    st.markdown("### Navigation")
    page = st.radio("", ["Overview", "Methodology"], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("**Ease to Mine Index (EMI)**")
    st.markdown("March 2026")
    st.markdown("")
    st.markdown("[E2C Partners](https://www.e2cpartners.com/insights/global-bitcoin-mining-report-the-ease-to-mine-index)")

# ============================================
# OVERVIEW PAGE
# ============================================
if page == "Overview":
    st.markdown("# Ease to Mine Index Dashboard")
    st.markdown("Comprehensive analysis of Bitcoin mining regulatory and operating conditions across 19 jurisdictions")
    
    # ========================================
    # FILTER FOR MAP (no separator line)
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
    # WORLD MAP - NO TITLE, NO BACKGROUND
    # ========================================
    df_map = df.copy()
    df_map["ISO"] = df_map["Country"].map(ISO_CODES)
    
    df_map_agg = df_map.groupby("ISO").agg({
        selected_col: "mean",
        "Country": lambda x: ", ".join(x) if len(x) > 1 else x.iloc[0]
    }).reset_index()
    df_map_agg.columns = ["ISO", "Score", "Country"]
    
    # Darker color scale
    fig_map = go.Figure(go.Choropleth(
        locations=df_map_agg["ISO"],
        z=df_map_agg["Score"],
        text=df_map_agg["Country"],
        colorscale=[
            [0, '#7F1D1D'],      # Dark Red
            [0.25, '#92400E'],   # Dark Orange
            [0.5, '#A16207'],    # Dark Yellow/Amber
            [0.75, '#166534'],   # Dark Green
            [1, '#1E3A8A']       # Dark Blue
        ],
        autocolorscale=False,
        marker_line_color='#4B5563',  # Dark gray borders
        marker_line_width=1,
        colorbar=dict(
            title=dict(text=score_type, side="right", font=dict(family="Inter", size=12)),
            tickfont=dict(family="Inter"),
            len=0.6,
            thickness=15
        ),
        hovertemplate="<b>%{text}</b><br>" + score_type + ": %{z:.2f}<extra></extra>"
    ))
    
    fig_map.update_layout(
        height=420,
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
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter")
    )
    
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================
    # COMBINED EMI RANKING + HASHRATE CHART
    # ========================================
    st.markdown('<p class="section-title">EMI Ranking & Hashrate Distribution</p>', unsafe_allow_html=True)
    
    col_chart_filter, col_spacer2 = st.columns([1, 3])
    with col_chart_filter:
        chart_view = st.selectbox("View", ["EMI Score", "Hashrate Q1 2026", "Both"], key="chart_view")
    
    df_rank = df.sort_values("Index_Score", ascending=True).copy()
    
    # Prepare hashrate data
    hash_lookup = {}
    for _, row in df.iterrows():
        country = row["Country"]
        hash_lookup[country] = row["Hashrate_Q1_26"]
    
    min_score = df_rank["Index_Score"].min()
    max_score = df_rank["Index_Score"].max()
    colors = [get_score_color_dark(score, min_score, max_score) for score in df_rank["Index_Score"]]
    
    if chart_view == "EMI Score":
        fig_combined = go.Figure(go.Bar(
            x=df_rank["Index_Score"],
            y=df_rank["Country"],
            orientation='h',
            marker_color=colors,
            text=df_rank["Index_Score"].round(2),
            textposition='outside',
            textfont=dict(size=11, family="Inter"),
            name="EMI Score"
        ))
        
        fig_combined.update_layout(
            xaxis=dict(
                range=[0, 1], 
                title=dict(text="EMI Score", font=dict(family="Inter", size=12)),
                gridcolor='#E2E8F0', 
                zeroline=False
            ),
        )
        
    elif chart_view == "Hashrate Q1 2026":
        df_hash_sorted = df.sort_values("Hashrate_Q1_26", ascending=True)
        
        fig_combined = go.Figure(go.Bar(
            x=df_hash_sorted["Hashrate_Q1_26"],
            y=df_hash_sorted["Country"],
            orientation='h',
            marker_color='#1E3A8A',
            text=df_hash_sorted["Hashrate_Q1_26"].round(1),
            textposition='outside',
            textfont=dict(size=11, family="Inter"),
            name="Hashrate"
        ))
        
        fig_combined.update_layout(
            xaxis=dict(
                title=dict(text="Hashrate (EH/s)", font=dict(family="Inter", size=12)),
                gridcolor='#E2E8F0', 
                zeroline=False
            ),
        )
        
    else:  # Both
        fig_combined = go.Figure()
        
        # EMI Score bars
        fig_combined.add_trace(go.Bar(
            x=df_rank["Index_Score"],
            y=df_rank["Country"],
            orientation='h',
            marker_color='#1E3A8A',
            text=df_rank["Index_Score"].round(2),
            textposition='outside',
            textfont=dict(size=10, family="Inter"),
            name="EMI Score",
            xaxis='x'
        ))
        
        # Hashrate bars (secondary axis)
        hashrate_values = [hash_lookup.get(c, 0) for c in df_rank["Country"]]
        fig_combined.add_trace(go.Bar(
            x=hashrate_values,
            y=df_rank["Country"],
            orientation='h',
            marker_color='#B45309',
            text=[f"{v:.0f}" for v in hashrate_values],
            textposition='outside',
            textfont=dict(size=10, family="Inter"),
            name="Hashrate (EH/s)",
            xaxis='x2'
        ))
        
        fig_combined.update_layout(
            xaxis=dict(
                range=[0, 1],
                title=dict(text="EMI Score", font=dict(family="Inter", size=12)),
                gridcolor='#E2E8F0',
                zeroline=False,
                side='bottom'
            ),
            xaxis2=dict(
                range=[0, max(hashrate_values) * 1.2],
                title=dict(text="Hashrate (EH/s)", font=dict(family="Inter", size=12)),
                overlaying='x',
                side='top',
                gridcolor='rgba(0,0,0,0)'
            ),
            barmode='group',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.08,
                xanchor="center",
                x=0.5,
                font=dict(family="Inter")
            )
        )
    
    fig_combined.update_layout(
        height=620,
        margin=dict(l=0, r=60, t=40, b=40),
        yaxis=dict(title="", tickfont=dict(family="Inter", size=11)),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter")
    )
    
    st.plotly_chart(fig_combined, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================
    # HEATMAP - MOVED HERE, DARKER COLORS
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
        colorscale=[
            [0, '#7F1D1D'],      # Dark Red
            [0.25, '#92400E'],   # Dark Orange
            [0.5, '#A16207'],    # Dark Amber
            [0.75, '#166534'],   # Dark Green
            [1, '#1E3A8A']       # Dark Blue
        ],
        text=np.round(heatmap_data.values, 2),
        texttemplate="%{text}",
        textfont=dict(size=10, color="white", family="Inter"),
        hovertemplate="Country: %{y}<br>Section: %{x}<br>Score: %{z:.2f}<extra></extra>",
        showscale=True,
        colorbar=dict(
            title=dict(text="Score", side="right", font=dict(family="Inter")),
            tickfont=dict(family="Inter")
        )
    ))
    
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
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Respondents", "48")
    with col2:
        st.metric("Jurisdictions Covered", "19")
    with col3:
        st.metric("Survey Period", "Dec 2025 - Feb 2026")
    
    st.markdown("---")
    
    # ========================================
    # RESPONDENTS PIE CHART - FIRST NOW
    # ========================================
    st.markdown('<p class="section-title">Survey Respondents by Jurisdiction</p>', unsafe_allow_html=True)
    
    df_resp = df.copy()
    canada_resp = df_resp[df_resp["Country"].isin(["Alberta (CA)", "Quebec (CA)"])]["Respondents"].sum()
    df_resp = df_resp[~df_resp["Country"].isin(["Alberta (CA)", "Quebec (CA)"])]
    df_resp = pd.concat([df_resp, pd.DataFrame([{"Country": "Canada", "Respondents": canada_resp}])], ignore_index=True)
    
    df_resp = df_resp[df_resp["Respondents"] > 0].sort_values("Respondents", ascending=False)
    total_respondents = df_resp["Respondents"].sum()
    
    pie_colors = generate_gradient_colors_simple(len(df_resp), "#1E3A8A", "#B45309")
    
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
        text=f"<b>{int(total_respondents)}</b><br><span style='font-size:14px'>Total</span>",
        x=0.5, y=0.5,
        font=dict(size=40, color="#1E293B", family="Inter"),
        showarrow=False
    )
    
    fig_pie.update_layout(
        height=450,
        margin=dict(l=40, r=40, t=20, b=20),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter")
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================
    # WEIGHTING STACKED BAR CHART - SECOND NOW
    # ========================================
    st.markdown('<p class="section-title">Index Weighting by Dimension</p>', unsafe_allow_html=True)
    
    fig_weights = go.Figure()
    
    # Using darker colors with appropriate text colors
    weights = [
        ("Energy & Grid", 25, "#1E3A8A", "white"),           # Dark Blue - white text
        ("Fiscal", 20, "#3B82F6", "white"),                   # Medium Blue - white text
        ("Legal", 17.5, "#B45309", "white"),                  # Dark Orange - white text
        ("Permits & Licensing", 17.5, "#F59E0B", "black"),    # Amber - black text
        ("Customs & Tariffs", 15, "#166534", "white"),        # Dark Green - white text
        ("Operating Conditions", 5, "#5B21B6", "white")       # Dark Purple - white text
    ]
    
    for name, weight, color, text_color in weights:
        fig_weights.add_trace(go.Bar(
            name=name,
            x=[weight],
            y=["EMI Index"],
            orientation='h',
            marker_color=color,
            text=[f"{name}: {weight}%"],
            textposition='inside',
            textfont=dict(size=11, family="Inter", color=text_color),
            hovertemplate=f"<b>{name}</b><br>Weight: {weight}%<extra></extra>"
        ))
    
    fig_weights.update_layout(
        barmode='stack',
        height=100,
        margin=dict(l=0, r=0, t=10, b=10),
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
# FOOTER
# ============================================
st.markdown("""
<div class="footer">
    <p><strong>Ease to Mine Index (EMI)</strong> - March 2026</p>
    <p>Research by <a href="https://www.e2cpartners.com/insights/global-bitcoin-mining-report-the-ease-to-mine-index" target="_blank">E2C Partners</a> | 
    Survey of 48 industry practitioners across 19 jurisdictions</p>
</div>
""", unsafe_allow_html=True)
