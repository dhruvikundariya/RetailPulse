# dashboard_pages/customer_segmentation.py
import streamlit as st
import pandas as pd
import plotly.express as px
import utils
import styles

def render(theme="light"):
    st.markdown(
        """
        <div class="header-container">
            <h1 class="header-title">Customer RFM Segmentation</h1>
            <p class="header-subtitle">Analyze customer behavior clusters using Recency, Frequency, and Monetary (RFM) modeling</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Load RFM data
    df_rfm = utils.load_csv_data("rfm_data.csv")
    
    if df_rfm.empty:
        st.warning("RFM segmentation data is not available. Please verify your data/ folder.")
        return

    # Count and percentages
    total_custs = len(df_rfm)
    
    segments = {
        "Champions": {"class": "segment-champions", "label": "Champions"},
        "Loyal Customers": {"class": "segment-loyal", "label": "Loyal Customers"},
        "New Customers": {"class": "segment-new", "label": "New Customers"},
        "At Risk Customers": {"class": "segment-atrisk", "label": "At Risk"},
        "Lost Customers": {"class": "segment-lost", "label": "Lost Customers"}
    }
    
    # Render segment cards
    cols = st.columns(5)
    
    for idx, (seg_name, config) in enumerate(segments.items()):
        seg_df = df_rfm[df_rfm["Segment"] == seg_name]
        count = len(seg_df)
        pct = (count / total_custs * 100) if total_custs > 0 else 0
        
        with cols[idx]:
            st.markdown(
                styles.render_segment_card(config["label"], count, round(pct, 1), config["class"]),
                unsafe_allow_html=True
            )
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visualizations row: Donut & 2D Cluster projection
    row1_cols = st.columns([1, 1])
    
    with row1_cols[0]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;'>Segment Distribution</h3>", unsafe_allow_html=True)
        
        seg_summary = df_rfm["Segment"].value_counts().reset_index()
        seg_summary.columns = ["Segment", "Count"]
        
        fig_pie = px.pie(
            seg_summary,
            names="Segment",
            values="Count",
            hole=0.4,
            color="Segment",
            color_discrete_sequence=utils.DISCRETE_PALETTE
        )
        utils.style_plotly_fig(fig_pie, theme)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with row1_cols[1]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;'>K-Means Cluster Space</h3>", unsafe_allow_html=True)
        
        # 2D projection of Recency vs Monetary with Cluster mapping
        df_rfm["Cluster_Name"] = df_rfm["Cluster"].apply(lambda c: f"Cluster {c}")
        
        fig_cluster = px.scatter(
            df_rfm,
            x="Recency",
            y="Monetary",
            color="Cluster_Name",
            size="Frequency",
            color_discrete_sequence=utils.DISCRETE_PALETTE[::-1],
            labels={"Recency": "Recency (Days since last purchase)", "Monetary": "Monetary Value ($)", "Cluster_Name": "Cluster"}
        )
        utils.style_plotly_fig(fig_cluster, theme)
        st.plotly_chart(fig_cluster, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
