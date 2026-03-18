import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Ease to Mine Index Dashboard",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS
# ============================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-top: 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
    }
    .stMetric > div {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_data():
    df = pd.read_csv("data/emi_scores.csv")
    return df

df = load_data()

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.image("https://hashlabs.io/wp-content/uploads/2024/01/hashlabs-logo.png", width=200)
    st.markdown("---")
    st.markdown("### 🎛️ Filters")
    
    # Region filter
    regions = ["All Regions"] + sorted(df["Region"].unique().tolist())
    selected_region = st.selectbox("Select Region", regions)
    
    # Score range filter
    min_score, max_score = st.slider(
        "EMI Score Range",
        min_value=0.0,
        max_value=1.0,
        value=(0.0, 1.0),
        step=0.05
    )
    
    # Dimension selection for comparison
    st.markdown("### 📊 Dimensions")
    dimensions = {
        "Fiscal": "Fiscal",
        "Permit & Licensing": "Permit_Licensing", 
        "Legal": "Legal",
        "Energy & Grid": "Energy_Grid",
        "Tariff & Import": "Tariff_Import",
        "Operating Conditions": "Operating_Conditions"
    }
    selected_dims = st.multiselect(
        "Compare dimensions",
        list(dimensions.keys()),
        default=["Fiscal", "Legal", "Energy & Grid"]
    )
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    The **Ease to Mine Index (EMI)** evaluates 
    Bitcoin mining attractiveness across 18 jurisdictions.
    
    *Source: Hashlabs Research (2026)*
    """)

# ============================================
# FILTER DATA
# ============================================
filtered_df = df.copy()

if selected_region != "All Regions":
    filtered_df = filtered_df[filtered_df["Region"] == selected_region]

filtered_df = filtered_df[
    (filtered_df["Index_Score"] >= min_score) & 
    (filtered_df["Index_Score"] <= max_score)
]

# ============================================
# HEADER
# ============================================
st.markdown('<p class="main-header">⛏️ Ease to Mine Index Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Comparing Bitcoin mining conditions across 18 jurisdictions worldwide</p>', unsafe_allow_html=True)
st.markdown("---")

# ============================================
# KPI METRICS
# ============================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🏆 Top Jurisdiction",
        value=filtered_df.loc[filtered_df["Index_Score"].idxmax(), "Country"],
        delta=f"Score: {filtered_df['Index_Score'].max():.2f}"
    )

with col2:
    st.metric(
        label="📊 Average EMI Score",
        value=f"{filtered_df['Index_Score'].mean():.2f}",
        delta=f"{len(filtered_df)} countries"
    )

with col3:
    st.metric(
        label="⚡ Best Energy Access",
        value=filtered_df.loc[filtered_df["Energy_Grid"].idxmax(), "Country"],
        delta=f"Score: {filtered_df['Energy_Grid'].max():.2f}"
    )

with col4:
    st.metric(
        label="⏱️ Fastest Permits",
        value=filtered_df.loc[filtered_df["Permit_Months"].idxmin(), "Country"],
        delta=f"{filtered_df['Permit_Months'].min():.1f} months"
    )

st.markdown("---")

# ============================================
# MAIN CHARTS
# ============================================
tab1, tab2, tab3, tab4 = st.tabs(["🏆 Overall Ranking", "📊 Dimension Analysis", "⏱️ Permit Timeline", "🗺️ Regional View"])

# TAB 1: Overall Ranking
with tab1:
    st.subheader("EMI Score Ranking by Country")
    
    df_sorted = filtered_df.sort_values("Index_Score", ascending=True)
    
    # Color scale based on score
    colors = df_sorted["Index_Score"].apply(
        lambda x: "#1D9E75" if x >= 0.6 else ("#378ADD" if x >= 0.5 else ("#EF9F27" if x >= 0.4 else "#E24B4A"))
    )
    
    fig = go.Figure(go.Bar(
        x=df_sorted["Index_Score"],
        y=df_sorted["Country"],
        orientation='h',
        marker_color=colors,
        text=df_sorted["Index_Score"].round(2),
        textposition='outside'
    ))
    
    fig.update_layout(
        height=600,
        xaxis_title="EMI Score (0 = Unfavorable → 1 = Highly Favorable)",
        yaxis_title="",
        xaxis=dict(range=[0, 1]),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Legend
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown("🟢 **Highly Favorable** (≥0.60)")
    col2.markdown("🔵 **Favorable** (0.50-0.59)")
    col3.markdown("🟠 **Neutral** (0.40-0.49)")
    col4.markdown("🔴 **Unfavorable** (<0.40)")

# TAB 2: Dimension Analysis
with tab2:
    st.subheader("Multi-Dimension Comparison")
    
    if selected_dims:
        # Radar chart for selected countries
        col1, col2 = st.columns([1, 2])
        
        with col1:
            selected_countries = st.multiselect(
                "Select countries to compare",
                filtered_df["Country"].tolist(),
                default=filtered_df.nlargest(3, "Index_Score")["Country"].tolist()
            )
        
        with col2:
            if selected_countries:
                fig = go.Figure()
                
                dim_cols = [dimensions[d] for d in selected_dims]
                
                for country in selected_countries:
                    country_data = filtered_df[filtered_df["Country"] == country]
                    values = country_data[dim_cols].values.flatten().tolist()
                    values.append(values[0])  # Close the radar
                    
                    categories = selected_dims + [selected_dims[0]]
                    
                    fig.add_trace(go.Scatterpolar(
                        r=values,
                        theta=categories,
                        fill='toself',
                        name=country,
                        opacity=0.6
                    ))
                
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                    showlegend=True,
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please select at least one dimension in the sidebar.")

    # Heatmap
    st.subheader("Score Heatmap by Dimension")
    
    heatmap_cols = ["Fiscal", "Permit_Licensing", "Legal", "Energy_Grid", "Tariff_Import", "Operating_Conditions"]
    heatmap_labels = ["Fiscal", "Permits", "Legal", "Energy", "Tariffs", "Climate"]
    
    heatmap_data = filtered_df.set_index("Country")[heatmap_cols]
    heatmap_data.columns = heatmap_labels
    
    fig = px.imshow(
        heatmap_data.sort_values("Fiscal", ascending=False),
        color_continuous_scale="RdYlGn",
        aspect="auto",
        text_auto=".2f"
    )
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

# TAB 3: Permit Timeline
with tab3:
    st.subheader("Construction Permit Timeline by Country")
    
    df_permit = filtered_df.sort_values("Permit_Months", ascending=True)
    
    colors = df_permit["Permit_Months"].apply(
        lambda x: "#1D9E75" if x < 4 else ("#378ADD" if x <= 6 else ("#EF9F27" if x <= 9 else "#E24B4A"))
    )
    
    fig = go.Figure(go.Bar(
        x=df_permit["Permit_Months"],
        y=df_permit["Country"],
        orientation='h',
        marker_color=colors,
        text=df_permit["Permit_Months"].apply(lambda x: f"{x:.1f} mo"),
        textposition='outside'
    ))
    
    fig.update_layout(
        height=600,
        xaxis_title="Average Time to Obtain Construction Permits (months)",
        yaxis_title="",
        xaxis=dict(range=[0, 14]),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Legend
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown("🟢 **Fast** (<4 months)")
    col2.markdown("🔵 **Moderate** (4-6 months)")
    col3.markdown("🟠 **Slow** (6-9 months)")
    col4.markdown("🔴 **Very Slow** (>9 months)")
    
    # Stats
    st.markdown("---")
    st.subheader("📈 Key Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Fastest", f"{df_permit['Permit_Months'].min():.1f} months", df_permit.iloc[0]['Country'])
    col2.metric("Average", f"{df_permit['Permit_Months'].mean():.1f} months")
    col3.metric("Slowest", f"{df_permit['Permit_Months'].max():.1f} months", df_permit.iloc[-1]['Country'])

# TAB 4: Regional View
with tab4:
    st.subheader("Regional Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Average score by region
        region_avg = df.groupby("Region")["Index_Score"].mean().sort_values(ascending=True)
        
        fig = px.bar(
            x=region_avg.values,
            y=region_avg.index,
            orientation='h',
            color=region_avg.values,
            color_continuous_scale="Viridis",
            labels={"x": "Average EMI Score", "y": "Region"}
        )
        fig.update_layout(
            title="Average EMI Score by Region",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Country count by region
        region_count = df.groupby("Region").size()
        
        fig = px.pie(
            values=region_count.values,
            names=region_count.index,
            title="Countries Surveyed by Region",
            hole=0.4
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Scatter plot: EMI Score vs Permit Time
    st.subheader("EMI Score vs. Permit Timeline")
    
    fig = px.scatter(
        filtered_df,
        x="Permit_Months",
        y="Index_Score",
        color="Region",
        size="Energy_Grid",
        hover_name="Country",
        labels={
            "Permit_Months": "Permit Timeline (months)",
            "Index_Score": "EMI Score",
            "Energy_Grid": "Energy Score"
        }
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# DATA TABLE
# ============================================
st.markdown("---")
st.subheader("📋 Full Data Table")

# Format the dataframe for display
display_df = filtered_df.copy()
display_df = display_df.round(3)
display_df = display_df.sort_values("Index_Score", ascending=False)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Index_Score": st.column_config.ProgressColumn(
            "EMI Score",
            format="%.2f",
            min_value=0,
            max_value=1,
        ),
        "Permit_Months": st.column_config.NumberColumn(
            "Permit (months)",
            format="%.1f"
        )
    }
)

# Download button
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="📥 Download Data as CSV",
    data=csv,
    file_name="emi_data_export.csv",
    mime="text/csv"
)

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; padding: 1rem;'>
    <p>📊 <strong>Ease to Mine Index (EMI)</strong> — First Edition 2026</p>
    <p>Research by <a href='https://hashlabs.io' target='_blank'>Hashlabs</a> | 
    Data from survey of 48 industry practitioners across 18 countries</p>
</div>
""", unsafe_allow_html=True)
