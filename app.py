import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
st.sidebar.image("https://framerusercontent.com/images/H3JhLauLgPETCRKMoj3axnBKME.png", width=180)
st.sidebar.markdown("---")

# Section navigation
sections = ["🏠 Overview", "💰 Fiscal", "📋 Permitting & Licensing", "⚖️ Legal", "⚡ Energy & Grid", "🚢 Customs & Tariffs"]
selected_section = st.sidebar.radio("Navigate to", sections)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Filters")
selected_regions = st.sidebar.multiselect(
    "Filter by Region",
    df_scores["Region"].unique(),
    default=df_scores["Region"].unique()
)

# Filter data
df_filtered = df_scores[df_scores["Region"].isin(selected_regions)]
df_detailed_filtered = df_detailed[df_detailed["Region"].isin(selected_regions)]

# ============================================
# HELPER FUNCTIONS
# ============================================
def show_regional_averages(section_col):
    """Display regional averages for a given section"""
    st.subheader("📊 Regional Averages")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        regional_avg = df_filtered.groupby("Region")[section_col].mean().sort_values(ascending=True)
        
        fig = go.Figure(go.Bar(
            x=regional_avg.values,
            y=regional_avg.index,
            orientation='h',
            marker_color=['#1D9E75' if v >= 0.6 else '#378ADD' if v >= 0.5 else '#EF9F27' if v >= 0.4 else '#E24B4A' for v in regional_avg.values],
            text=[f"{v:.2f}" for v in regional_avg.values],
            textposition='outside'
        ))
        fig.update_layout(
            height=300,
            xaxis=dict(range=[0, 1], title="Average Score"),
            yaxis_title="",
            margin=dict(l=0, r=50, t=20, b=40),
            plot_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.metric("🌍 Global Average", f"{df_filtered[section_col].mean():.2f}")
        best_region = regional_avg.idxmax()
        worst_region = regional_avg.idxmin()
        st.metric("🏆 Best Region", best_region, f"{regional_avg[best_region]:.2f}")
        st.metric("⚠️ Lowest Region", worst_region, f"{regional_avg[worst_region]:.2f}")

def show_country_ranking(section_col, title):
    """Display country ranking for a section"""
    st.subheader(f"🏆 Country Ranking - {title}")
    
    df_sorted = df_filtered.sort_values(section_col, ascending=True)
    
    colors = df_sorted[section_col].apply(
        lambda x: "#1D9E75" if x >= 0.6 else ("#378ADD" if x >= 0.5 else ("#EF9F27" if x >= 0.4 else "#E24B4A"))
    )
    
    fig = go.Figure(go.Bar(
        x=df_sorted[section_col],
        y=df_sorted["Country"],
        orientation='h',
        marker_color=colors,
        text=df_sorted[section_col].round(2),
        textposition='outside'
    ))
    
    fig.update_layout(
        height=550,
        xaxis=dict(range=[0, 1], title="Score"),
        yaxis_title="",
        margin=dict(l=0, r=50, t=20, b=40),
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_question_breakdown(section_name, questions_list):
    """Display breakdown by question with response distribution"""
    st.subheader("📋 Detailed Question Analysis")
    
    section_data = df_detailed_filtered[df_detailed_filtered["Section"] == section_name]
    
    for question in questions_list:
        q_data = section_data[section_data["Question"] == question]
        
        if len(q_data) > 0:
            with st.expander(f"**{question}** ({len(q_data)} responses)", expanded=False):
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    # Response distribution
                    response_counts = q_data["Response"].value_counts()
                    
                    fig = px.pie(
                        values=response_counts.values,
                        names=response_counts.index,
                        hole=0.4
                    )
                    fig.update_layout(
                        height=300,
                        margin=dict(l=20, r=20, t=30, b=20),
                        showlegend=True,
                        legend=dict(orientation="h", yanchor="bottom", y=-0.3)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Country breakdown table
                    country_responses = q_data.groupby("Country")["Response"].apply(lambda x: ", ".join(x.unique())).reset_index()
                    country_responses.columns = ["Country", "Response(s)"]
                    st.dataframe(country_responses, use_container_width=True, hide_index=True, height=280)

def show_duration_analysis(section_name, question_name):
    """Special analysis for duration-type questions"""
    st.subheader(f"⏱️ {question_name}")
    
    section_data = df_detailed_filtered[
        (df_detailed_filtered["Section"] == section_name) & 
        (df_detailed_filtered["Question"] == question_name)
    ]
    
    # Duration mapping
    duration_map = {
        'Less than 3 months': 1.5,
        'less than 3 months': 1.5,
        '3 – 6 months': 4.5,
        '3 - 6 months': 4.5,
        '6 – 9 months': 7.5,
        '6 - 9 months': 7.5,
        '9 – 12 months': 10.5,
        '9 - 12 months': 10.5,
        '12 – 18 months': 15,
        '12 - 18 months': 15,
        '18 – 24 months': 21,
        '18 - 24 months': 21,
        '> 24 months': 30,
        'More than 12 months': 15,
    }
    
    # Calculate average duration per country
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
                "Avg_Duration": sum(durations) / len(durations),
                "Region": country_data["Region"].iloc[0]
            })
    
    if country_durations:
        df_duration = pd.DataFrame(country_durations).sort_values("Avg_Duration")
        
        colors = df_duration["Avg_Duration"].apply(
            lambda x: "#1D9E75" if x < 6 else ("#378ADD" if x < 12 else ("#EF9F27" if x < 18 else "#E24B4A"))
        )
        
        fig = go.Figure(go.Bar(
            x=df_duration["Avg_Duration"],
            y=df_duration["Country"],
            orientation='h',
            marker_color=colors,
            text=[f"{v:.1f} mo" for v in df_duration["Avg_Duration"]],
            textposition='outside'
        ))
        
        fig.update_layout(
            height=500,
            xaxis_title="Average Duration (months)",
            yaxis_title="",
            margin=dict(l=0, r=60, t=20, b=40),
            plot_bgcolor='rgba(0,0,0,0)',
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Legend
        col1, col2, col3, col4 = st.columns(4)
        col1.markdown("🟢 **Fast** (<6 mo)")
        col2.markdown("🔵 **Moderate** (6-12 mo)")
        col3.markdown("🟠 **Slow** (12-18 mo)")
        col4.markdown("🔴 **Very slow** (>18 mo)")


# ============================================
# MAIN CONTENT
# ============================================

# --- OVERVIEW ---
if selected_section == "🏠 Overview":
    st.title("⛏️ Ease to Mine Index Dashboard")
    st.markdown("*Comparing Bitcoin mining conditions across 19 jurisdictions worldwide*")
    st.markdown("---")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        best = df_filtered.loc[df_filtered["Index_Score"].idxmax()]
        st.metric("🏆 Top Jurisdiction", best["Country"], f"{best['Index_Score']:.2f}")
    with col2:
        st.metric("📊 Average EMI", f"{df_filtered['Index_Score'].mean():.2f}", f"{len(df_filtered)} countries")
    with col3:
        best_energy = df_filtered.loc[df_filtered["Energy_Grid"].idxmax()]
        st.metric("⚡ Best Energy Access", best_energy["Country"], f"{best_energy['Energy_Grid']:.2f}")
    with col4:
        fastest = df_filtered.loc[df_filtered["Permit_Months"].idxmin()]
        st.metric("⏱️ Fastest Permits", fastest["Country"], f"{fastest['Permit_Months']:.1f} mo")
    
    st.markdown("---")
    
    # Overall ranking
    show_country_ranking("Index_Score", "Overall EMI Score")
    
    # Regional summary
    st.markdown("---")
    st.subheader("🌍 Regional Performance")
    
    regional_summary = df_filtered.groupby("Region").agg({
        "Index_Score": "mean",
        "Fiscal": "mean",
        "Permit_Licensing": "mean",
        "Legal": "mean",
        "Energy_Grid": "mean",
        "Tariff_Import": "mean"
    }).round(2)
    
    st.dataframe(regional_summary, use_container_width=True)


# --- FISCAL ---
elif selected_section == "💰 Fiscal":
    st.title("💰 Fiscal Environment")
    st.markdown("*Tax policies, subsidies, and fiscal incentives for Bitcoin mining*")
    st.markdown("---")
    
    show_regional_averages("Fiscal")
    st.markdown("---")
    show_country_ranking("Fiscal", "Fiscal Score")
    st.markdown("---")
    
    fiscal_questions = [
        "Taxation environment",
        "Shift profit center possible",
        "Electricity tax exposure",
        "Tax abatements available",
        "Constraint to access benefits",
        "Corporate Income Tax (CIT)"
    ]
    show_question_breakdown("Fiscal", fiscal_questions)


# --- PERMITTING ---
elif selected_section == "📋 Permitting & Licensing":
    st.title("📋 Permitting & Licensing")
    st.markdown("*Construction permits, licenses, and regulatory approvals*")
    st.markdown("---")
    
    show_regional_averages("Permit_Licensing")
    st.markdown("---")
    show_country_ranking("Permit_Licensing", "Permitting Score")
    st.markdown("---")
    
    # Special duration charts
    st.subheader("⏱️ Timeline Analysis")
    tab1, tab2 = st.tabs(["Construction Permits", "Grid Connection"])
    
    with tab1:
        show_duration_analysis("Permitting", "Construction permit timeline")
    
    with tab2:
        show_duration_analysis("Energy", "Grid connection lead time")
    
    st.markdown("---")
    
    permit_questions = [
        "Operational license timeline",
        "ASIC import license required",
        "Construction permit timeline",
        "EIA complexity",
        "Water permits restrictiveness",
        "Heat/noise/emissions regulations",
        "Zoning restrictions impact"
    ]
    show_question_breakdown("Permitting", permit_questions)


# --- LEGAL ---
elif selected_section == "⚖️ Legal":
    st.title("⚖️ Legal Framework")
    st.markdown("*Regulatory environment and legislative outlook*")
    st.markdown("---")
    
    show_regional_averages("Legal")
    st.markdown("---")
    show_country_ranking("Legal", "Legal Score")
    st.markdown("---")
    
    legal_questions = [
        "Regulatory environment",
        "Framework evolution outlook",
        "Legislative risk"
    ]
    show_question_breakdown("Legal", legal_questions)


# --- ENERGY ---
elif selected_section == "⚡ Energy & Grid":
    st.title("⚡ Energy & Grid Access")
    st.markdown("*Grid connectivity, energy prices, and access barriers*")
    st.markdown("---")
    
    show_regional_averages("Energy_Grid")
    st.markdown("---")
    show_country_ranking("Energy_Grid", "Energy & Grid Score")
    st.markdown("---")
    
    # Grid connection timeline
    show_duration_analysis("Energy", "Grid connection lead time")
    st.markdown("---")
    
    energy_questions = [
        "Grid access barriers",
        "Grid connection lead time",
        "Electricity price",
        "Regulatory status for miners"
    ]
    show_question_breakdown("Energy", energy_questions)


# --- CUSTOMS ---
elif selected_section == "🚢 Customs & Tariffs":
    st.title("🚢 Customs & Tariffs")
    st.markdown("*Import procedures, VAT, and trade barriers*")
    st.markdown("---")
    
    show_regional_averages("Tariff_Import")
    st.markdown("---")
    show_country_ranking("Tariff_Import", "Customs & Tariffs Score")
    st.markdown("---")
    
    customs_questions = [
        "VAT rate",
        "VAT filing burden",
        "ASIC import process",
        "Electrical infra import",
        "Tariff on China imports",
        "Procurement lead times",
        "Mitigation effectiveness"
    ]
    show_question_breakdown("Customs", customs_questions)


# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; padding: 1rem;'>
    <p>📊 <strong>Ease to Mine Index (EMI)</strong> — First Edition 2026</p>
    <p>Research by <a href='https://hashlabs.io' target='_blank'>Hashlabs</a> | 
    Survey of 48 industry practitioners across 19 jurisdictions</p>
</div>
""", unsafe_allow_html=True)
