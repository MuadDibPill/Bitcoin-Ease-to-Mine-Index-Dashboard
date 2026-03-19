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
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# GALAXY-STYLE CSS
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background-color: #ffffff;
    }
    
    /* Typography - Galaxy style */
    h1 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        color: #000000 !important;
        letter-spacing: -0.03em !important;
        line-height: 1.1 !important;
    }
    
    h2 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
        color: #000000 !important;
        letter-spacing: -0.02em !important;
    }
    
    h3 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        color: #1a1a1a !important;
        letter-spacing: -0.01em !important;
    }
    
    p, span, div, label {
        font-family: 'Inter', sans-serif;
        color: #374151;
    }
    
    /* Section titles */
    .section-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.25rem;
        font-weight: 600;
        color: #000000;
        letter-spacing: -0.02em;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #e5e7eb;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.75rem !important;
        color: #000000 !important;
        letter-spacing: -0.02em !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.75rem !important;
        color: #6b7280 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #fafafa;
        border-right: 1px solid #e5e7eb;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #000000 !important;
    }
    
    /* Radio buttons */
    .stRadio > label {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        color: #374151 !important;
    }
    
    /* Select box */
    .stSelectbox > label {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        color: #374151 !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Links */
    a {
        color: #2563eb !important;
        text-decoration: none !important;
    }
    
    a:hover {
        text-decoration: underline !important;
    }
    
    /* Footer */
    .footer {
        font-family: 'Inter', sans-serif;
        text-align: center;
        color: #6b7280;
        padding: 2rem;
        font-size: 0.875rem;
        border-top: 1px solid #e5e7eb;
        margin-top: 3rem;
    }
    
    .footer strong {
        color: #000000;
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
# HELPER FUNCTIONS (NO MATPLOTLIB)
# ============================================
def hex_to_rgb(hex_color):
    """Convert hex to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Convert RGB tuple to hex"""
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def generate_gradient_colors(n, start_color="#10b981", end_color="#3622E6"):
    """Generate n colors as gradient from start to end"""
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

def get_score_color(score, min_score, max_score):
    """Get color based on score position in range"""
    ratio = (score - min_score) / (max_score - min_score) if max_score > min_score else 0.5
    
    # Gradient from #3622E6 (low) to #10b981 (high)
    start_rgb = hex_to_rgb("#3622E6")
    end_rgb = hex_to_rgb("#10b981")
    
    r = start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio
    g = start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio
    b = start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio
    
    return rgb_to_hex((r, g, b))

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("### Navigation")
    page = st.radio("", ["Overview"], label_visibility="collapsed")
    
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
    
    score_type = st.selectbox(
        "Select dimension to view",
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
            xaxis=dict(range=[0, 1], title=dict(text="EMI Score", font=dict(family="Inter", size=12)), 
                      gridcolor='#f3f4f6', zeroline=False),
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
            colorscale=[[0, '#3622E6'], [0.5, '#22a8e6'], [1, '#10b981']],
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
    # PIE CHART & TREEMAP
    # ========================================
    col_pie, col_tree = st.columns(2)
    
    with col_pie:
        st.markdown('<p class="section-title">Survey Respondents by Jurisdiction</p>', unsafe_allow_html=True)
        
        df_resp = df.copy()
        canada_resp = df_resp[df_resp["Country"].isin(["Alberta (CA)", "Quebec (CA)"])]["Respondents"].sum()
        df_resp = df_resp[~df_resp["Country"].isin(["Alberta (CA)", "Quebec (CA)"])]
        df_resp = pd.concat([df_resp, pd.DataFrame([{"Country": "Canada", "Respondents": canada_resp}])], ignore_index=True)
        
        df_resp = df_resp[df_resp["Respondents"] > 0].sort_values("Respondents", ascending=False)
        total_respondents = df_resp["Respondents"].sum()
        
        pie_colors = generate_gradient_colors(len(df_resp), "#10b981", "#3622E6")
        
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
            text=f"<b>{int(total_respondents)}</b><br><span style='font-size:12px'>Respondents</span>",
            x=0.5, y=0.5,
            font=dict(size=28, color="#000000", family="Inter"),
            showarrow=False
        )
        
        fig_pie.update_layout(
            height=480,
            margin=dict(l=40, r=40, t=20, b=20),
            showlegend=False,
            paper_bgcolor='white',
            font=dict(family="Inter")
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_tree:
        st.markdown('<p class="section-title">Hashrate Distribution Q1 2025 vs Q1 2026</p>', unsafe_allow_html=True)
        
        treemap_data = []
        for _, row in df.iterrows():
            country = row["Country"].replace(" (CA)", "").replace(" (US)", "")
            if country in ["Alberta", "Quebec"]:
                continue
            treemap_data.append({
                "Country": country,
                "Q1_2025": row["Hashrate_Q1_25"],
                "Q1_2026": row["Hashrate_Q1_26"]
            })
        
        canada_25 = df[df["Country"].isin(["Alberta (CA)", "Quebec (CA)"])]["Hashrate_Q1_25"].sum()
        canada_26 = df[df["Country"].isin(["Alberta (CA)", "Quebec (CA)"])]["Hashrate_Q1_26"].sum()
        treemap_data.append({"Country": "Canada", "Q1_2025": canada_25, "Q1_2026": canada_26})
        
        df_tree = pd.DataFrame(treemap_data)
        df_tree = df_tree[df_tree["Q1_2026"] > 0]
        df_tree["Growth"] = ((df_tree["Q1_2026"] - df_tree["Q1_2025"]) / df_tree["Q1_2025"].replace(0, 1) * 100).round(1)
        
        fig_tree = px.treemap(
            df_tree,
            path=["Country"],
            values="Q1_2026",
            color="Growth",
            color_continuous_scale=[[0, '#E63622'], [0.35, '#e6a822'], [0.5, '#22a8e6'], [1, '#10b981']],
            color_continuous_midpoint=20,
            custom_data=["Q1_2025", "Q1_2026", "Growth"]
        )
        
        fig_tree.update_traces(
            texttemplate="<b>%{label}</b><br>%{value:.0f} EH/s<br>%{customdata[2]:+.0f}%",
            textfont=dict(size=11, color="white", family="Inter"),
            hovertemplate="<b>%{label}</b><br>Q1 2025: %{customdata[0]:.1f} EH/s<br>Q1 2026: %{customdata[1]:.1f} EH/s<br>Growth: %{customdata[2]:+.1f}%<extra></extra>"
        )
        
        fig_tree.update_layout(
            height=480,
            margin=dict(l=10, r=10, t=20, b=10),
            paper_bgcolor='white',
            font=dict(family="Inter"),
            coloraxis_colorbar=dict(
                title=dict(text="YoY %", side="right", font=dict(family="Inter")),
                tickfont=dict(family="Inter")
            )
        )
        
        st.plotly_chart(fig_tree, use_container_width=True)
    
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
    
    display_cols = ["Country", "Region", "EMI Score", "Fiscal", "Permits", "Legal", "Energy", "Tariffs", "Climate", "Respondents", "Hashrate Q1-25 (EH/s)", "Hashrate Q1-26 (EH/s)"]
    
    st.dataframe(
        df_display[display_cols],
        use_container_width=True,
        hide_index=True,
        height=550,
        column_config={
            "EMI Score": st.column_config.ProgressColumn(
                "EMI Score",
                format="%.2f",
                min_value=0,
                max_value=1,
            ),
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
    st.download_button(
        label="Download Data (CSV)",
        data=csv,
        file_name="emi_data_export.csv",
        mime="text/csv"
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
