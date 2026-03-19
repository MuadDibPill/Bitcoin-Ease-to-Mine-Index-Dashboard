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
# RGB COMPLEMENTARY PALETTE
# ============================================
COLORS = {
    'primary': '#2E5BFF',      # Blue
    'secondary': '#FF9F2E',    # Orange (complementary)
    'success': '#2EFF5B',      # Green
    'danger': '#FF2E5B',       # Red
    'purple': '#8B2EFF',       # Purple
    'cyan': '#2EFFFF',         # Cyan
    'text': '#1E293B',
    'text_muted': '#64748B',
    'border': '#E2E8F0'
}

# ============================================
# CUSTOM CSS
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #F8FAFC;
    }
    
    h1 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 2.2rem !important;
        color: #1E293B !important;
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
    
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
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
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def get_score_color(score, min_score, max_score):
    ratio = (score - min_score) / (max_score - min_score) if max_score > min_score else 0.5
    if ratio < 0.5:
        r = 255
        g = int(46 + (217) * (ratio * 2))
        b = int(91 + (30 - 91) * (ratio * 2))
    else:
        adjusted = (ratio - 0.5) * 2
        r = int(255 - (255 - 46) * adjusted)
        g = int(217 - (217 - 91) * adjusted)
        b = int(61 + (255 - 61) * adjusted)
    return rgb_to_hex((r, g, b))

def generate_gradient_colors(n, start_color="#2E5BFF", end_color="#FF9F2E"):
    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)
    colors = []
    for i in range(n):
        ratio = i / (n - 1) if n > 1 else 0
        r = start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio
        g = start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio
        b = start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio
        colors.append(rgb_to_hex((r, g, b)))
    return colors

# ============================================
# SIDEBAR NAVIGATION
# ============================================
with st.sidebar:
    st.markdown("### Navigation")
    page = st.radio("", ["Overview", "Report Methodology"], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("**Ease to Mine Index (EMI)**")
    st.markdown("First Edition 2026")
    st.markdown("")
    st.markdown("Survey of 48 practitioners across 19 jurisdictions.")
    st.markdown("")
    st.markdown("[Hashlabs](https://hashlabs.io)")

# ============================================
# OVERVIEW PAGE
# ============================================
if page == "Overview":
    st.markdown("# Ease to Mine Index Dashboard")
    st.markdown("Comprehensive analysis of Bitcoin mining conditions across 19 jurisdictions")
    st.markdown("---")
    
    # ========================================
    # SCORE CARD WITH FILTER
    # ========================================
    st.markdown('<p class="section-title">Global Scores</p>', unsafe_allow_html=True)
    
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
    df_sorted = df.sort_values(selected_col, ascending=False)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Top Jurisdiction", df_sorted.iloc[0]["Country"], f"{df_sorted.iloc[0][selected_col]:.2f}")
    with col2:
        st.metric("2nd Place", df_sorted.iloc[1]["Country"], f"{df_sorted.iloc[1][selected_col]:.2f}")
    with col3:
        st.metric("3rd Place", df_sorted.iloc[2]["Country"], f"{df_sorted.iloc[2][selected_col]:.2f}")
    with col4:
        st.metric("Global Average", f"{df[selected_col].mean():.2f}", f"{len(df)} jurisdictions")
    with col5:
        st.metric("Lowest Score", df_sorted.iloc[-1]["Country"], f"{df_sorted.iloc[-1][selected_col]:.2f}")
    
    st.markdown("---")
    
    # ========================================
    # WORLD MAP
    # ========================================
    st.markdown('<p class="section-title">EMI Score World Map</p>', unsafe_allow_html=True)
    
    # Prepare map data - aggregate Canada and US
    df_map = df.copy()
    df_map["ISO"] = df_map["Country"].map(ISO_CODES)
    
    # For countries with multiple regions (Canada, US), take the average
    df_map_agg = df_map.groupby("ISO").agg({
        "Index_Score": "mean",
        "Fiscal": "mean",
        "Permit_Licensing": "mean",
        "Legal": "mean",
        "Energy_Grid": "mean",
        "Tariff_Import": "mean",
        "Operating_Conditions": "mean",
        "Country": lambda x: ", ".join(x) if len(x) > 1 else x.iloc[0]
    }).reset_index()
    
    fig_map = go.Figure(go.Choropleth(
        locations=df_map_agg["ISO"],
        z=df_map_agg["Index_Score"],
        text=df_map_agg["Country"],
        colorscale=[
            [0, '#FF2E5B'],      # Red (low)
            [0.25, '#FF9F2E'],   # Orange
            [0.5, '#FFD93D'],    # Yellow
            [0.75, '#2EFF5B'],   # Green
            [1, '#2E5BFF']       # Blue (high)
        ],
        autocolorscale=False,
        marker_line_color='white',
        marker_line_width=0.5,
        colorbar=dict(
            title=dict(text="EMI Score", side="right", font=dict(family="Inter", size=12)),
            tickfont=dict(family="Inter"),
            len=0.6,
            thickness=15
        ),
        hovertemplate="<b>%{text}</b><br>EMI Score: %{z:.2f}<extra></extra>"
    ))
    
    fig_map.update_layout(
        height=500,
        margin=dict(l=0, r=0, t=10, b=0),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="#E2E8F0",
            showland=True,
            landcolor="#F1F5F9",
            showocean=True,
            oceancolor="#E0F2FE",
            showlakes=True,
            lakecolor="#E0F2FE",
            showcountries=True,
            countrycolor="#CBD5E1",
            projection_type='natural earth'
        ),
        paper_bgcolor='white',
        font=dict(family="Inter")
    )
    
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================
    # EMI RANKING & HEATMAP
    # ========================================
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown('<p class="section-title">EMI Ranking</p>', unsafe_allow_html=True)
        
        df_rank = df.sort_values("Index_Score", ascending=True)
        min_score = df_rank["Index_Score"].min()
        max_score = df_rank["Index_Score"].max()
        colors = [get_score_color(score, min_score, max_score) for score in df_rank["Index_Score"]]
        
        fig_rank = go.Figure(go.Bar(
            x=df_rank["Index_Score"],
            y=df_rank["Country"],
            orientation='h',
            marker_color=colors,
            text=df_rank["Index_Score"].round(2),
            textposition='outside',
            textfont=dict(size=11, family="Inter")
        ))
        
        fig_rank.update_layout(
            height=620,
            margin=dict(l=0, r=50, t=10, b=40),
            xaxis=dict(
                range=[0, 1], 
                title=dict(text="EMI Score", font=dict(family="Inter", size=12)),
                gridcolor='#E2E8F0', 
                zeroline=False
            ),
            yaxis=dict(title="", tickfont=dict(family="Inter", size=11)),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Inter")
        )
        
        st.plotly_chart(fig_rank, use_container_width=True)
    
    with col_right:
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
                [0, '#FF2E5B'],
                [0.25, '#FF9F2E'],
                [0.5, '#FFD93D'],
                [0.75, '#2EFF5B'],
                [1, '#2E5BFF']
            ],
            text=np.round(heatmap_data.values, 2),
            texttemplate="%{text}",
            textfont=dict(size=9, color="white", family="Inter"),
            hovertemplate="Country: %{y}<br>Section: %{x}<br>Score: %{z:.2f}<extra></extra>",
            showscale=True,
            colorbar=dict(
                title=dict(text="Score", side="right", font=dict(family="Inter")),
                tickfont=dict(family="Inter")
            )
        ))
        
        fig_heat.update_layout(
            height=620,
            margin=dict(l=0, r=0, t=10, b=40),
            xaxis=dict(title="", tickangle=0, side="bottom", tickfont=dict(family="Inter", size=11)),
            yaxis=dict(title="", autorange="reversed", tickfont=dict(family="Inter", size=11)),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Inter")
        )
        
        st.plotly_chart(fig_heat, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================
    # HASHRATE BAR CHART WITH FILTER
    # ========================================
    st.markdown('<p class="section-title">Hashrate Distribution Q1 2025 vs Q1 2026</p>', unsafe_allow_html=True)
    
    col_filter_hash, col_spacer2 = st.columns([1, 3])
    with col_filter_hash:
        view_mode = st.selectbox("View by", ["Country", "Region"], key="hashrate_view")
    
    if view_mode == "Country":
        hash_data = []
        for _, row in df.iterrows():
            country = row["Country"].replace(" (CA)", "").replace(" (US)", "")
            if country in ["Alberta", "Quebec"]:
                continue
            hash_data.append({
                "Name": country,
                "Q1_2025": row["Hashrate_Q1_25"],
                "Q1_2026": row["Hashrate_Q1_26"]
            })
        
        canada_25 = df[df["Country"].isin(["Alberta (CA)", "Quebec (CA)"])]["Hashrate_Q1_25"].sum()
        canada_26 = df[df["Country"].isin(["Alberta (CA)", "Quebec (CA)"])]["Hashrate_Q1_26"].sum()
        hash_data.append({"Name": "Canada", "Q1_2025": canada_25, "Q1_2026": canada_26})
        df_hash = pd.DataFrame(hash_data)
    else:
        df_region = df.copy()
        df_region["Region"] = df_region["Region"].replace({
            "North America": "Americas",
            "Latin America": "Americas"
        })
        df_hash = df_region.groupby("Region").agg({
            "Hashrate_Q1_25": "sum",
            "Hashrate_Q1_26": "sum"
        }).reset_index()
        df_hash.columns = ["Name", "Q1_2025", "Q1_2026"]
    
    df_hash = df_hash.sort_values("Q1_2026", ascending=True)
    
    fig_hash = go.Figure()
    
    fig_hash.add_trace(go.Bar(
        name='Q1 2025',
        y=df_hash["Name"],
        x=df_hash["Q1_2025"],
        orientation='h',
        marker_color=COLORS['secondary'],
        text=df_hash["Q1_2025"].round(1),
        textposition='outside',
        textfont=dict(size=10, family="Inter")
    ))
    
    fig_hash.add_trace(go.Bar(
        name='Q1 2026',
        y=df_hash["Name"],
        x=df_hash["Q1_2026"],
        orientation='h',
        marker_color=COLORS['primary'],
        text=df_hash["Q1_2026"].round(1),
        textposition='outside',
        textfont=dict(size=10, family="Inter")
    ))
    
    fig_hash.update_layout(
        barmode='group',
        height=500 if view_mode == "Country" else 300,
        margin=dict(l=0, r=80, t=10, b=40),
        xaxis=dict(
            title=dict(text="Hashrate (EH/s)", font=dict(family="Inter", size=12)),
            gridcolor='#E2E8F0'
        ),
        yaxis=dict(title="", tickfont=dict(family="Inter", size=11)),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Inter"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(family="Inter")
        )
    )
    
    st.plotly_chart(fig_hash, use_container_width=True)
    
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
# REPORT METHODOLOGY PAGE
# ============================================
elif page == "Report Methodology":
    st.markdown("# Report Methodology")
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
    # RESPONDENTS PIE CHART
    # ========================================
    st.markdown('<p class="section-title">Survey Respondents by Jurisdiction</p>', unsafe_allow_html=True)
    
    col_pie, col_info = st.columns([2, 1])
    
    with col_pie:
        df_resp = df.copy()
        canada_resp = df_resp[df_resp["Country"].isin(["Alberta (CA)", "Quebec (CA)"])]["Respondents"].sum()
        df_resp = df_resp[~df_resp["Country"].isin(["Alberta (CA)", "Quebec (CA)"])]
        df_resp = pd.concat([df_resp, pd.DataFrame([{"Country": "Canada", "Respondents": canada_resp}])], ignore_index=True)
        
        df_resp = df_resp[df_resp["Respondents"] > 0].sort_values("Respondents", ascending=False)
        total_respondents = df_resp["Respondents"].sum()
        
        pie_colors = generate_gradient_colors(len(df_resp), COLORS['primary'], COLORS['secondary'])
        
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
            text=f"<b>{int(total_respondents)}</b><br><span style='font-size:12px'>Total</span>",
            x=0.5, y=0.5,
            font=dict(size=32, color="#1E293B", family="Inter"),
            showarrow=False
        )
        
        fig_pie.update_layout(
            height=500,
            margin=dict(l=40, r=40, t=20, b=20),
            showlegend=False,
            paper_bgcolor='white',
            font=dict(family="Inter")
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_info:
        st.markdown("### Survey Details")
        st.markdown("""
        **Respondent Profile**
        
        Industry practitioners including:
        - Mining operators
        - Asset managers
        - Energy consultants
        - Legal advisors
        - Financial analysts
        
        **Data Collection**
        
        Online survey conducted between December 2025 and February 2026.
        
        **Weighting**
        
        Responses weighted by:
        - Energy & Grid: 25%
        - Fiscal: 20%
        - Legal: 17.5%
        - Permits: 17.5%
        - Tariffs: 15%
        - Climate: 5%
        """)
    
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
# FOOTER
# ============================================
st.markdown("""
<div class="footer">
    <p><strong>Ease to Mine Index (EMI)</strong> - First Edition 2026</p>
    <p>Research by <a href="https://hashlabs.io" target="_blank">Hashlabs</a> | 
    Survey of 48 industry practitioners across 19 jurisdictions</p>
</div>
""", unsafe_allow_html=True)
