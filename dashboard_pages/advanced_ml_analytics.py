# dashboard_pages/advanced_ml_analytics.py
import streamlit as st
import pandas as pd
import plotly.express as px
import utils
import styles

def render(theme="light"):
    st.markdown(
        """
        <div class="header-container">
            <h1 class="header-title">Advanced ML Analytics</h1>
            <p class="header-subtitle">Model evaluation benchmarks and feature importance rankings</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Load metrics and features
    df_metrics = utils.load_csv_data("model_metrics.csv")
    df_feat = utils.load_csv_data("feature_importance.csv")
    
    if df_metrics.empty or df_feat.empty:
        st.warning("Model analytics datasets are not available. Please verify your data/ folder.")
        return

    # Highlight Card: Best Model Random Forest
    st.markdown(
        f"""
        <div class="glass-card" style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(168, 85, 247, 0.05) 100%) !important; border: 1px solid rgba(168, 85, 247, 0.15) !important;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
                <div>
                    <span class="badge badge-success" style="margin-bottom:8px; background-color:rgba(16, 185, 129, 0.15); color:#10b981; border:1px solid #10b981;">PRODUCTION MODEL ACTIVATED</span>
                    <h2 style="margin:4px 0 8px 0; font-size:2.2rem; font-weight:800; background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Best Model: Random Forest</h2>
                    <p style="margin:0; color:#64748b; font-size:1.05rem;">The Random Forest model outperformed other classifiers on the holdout validation set and is configured for live churn predictions.</p>
                </div>
                <div style="display:flex; gap:16px; margin-top:16px;">
                    <div style="text-align:center; padding:10px 16px; background:rgba(0,0,0,0.02); border-radius:10px; border:1px solid rgba(0,0,0,0.05);">
                        <div style="font-size:0.75rem; color:#64748b; text-transform:uppercase;">Validation Accuracy</div>
                        <div style="font-size:1.8rem; font-weight:800; color:#6366f1;">89.5%</div>
                    </div>
                    <div style="text-align:center; padding:10px 16px; background:rgba(0,0,0,0.02); border-radius:10px; border:1px solid rgba(0,0,0,0.05);">
                        <div style="font-size:0.75rem; color:#64748b; text-transform:uppercase;">F1 Score</div>
                        <div style="font-size:1.8rem; font-weight:800; color:#a855f7;">86.8%</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Row of charts: Model Comparison & Feature Importance
    row1_cols = st.columns([1, 1])
    
    with row1_cols[0]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;'>Model Performance Comparison</h3>", unsafe_allow_html=True)
        
        # Reshape metrics for grouped bar chart
        df_melt = df_metrics.melt(id_vars="Model", var_name="Metric", value_name="Score")
        
        fig_comp = px.bar(
            df_melt,
            x="Model",
            y="Score",
            color="Metric",
            barmode="group",
            color_discrete_sequence=utils.DISCRETE_PALETTE,
            title="Algorithm Benchmarks",
            range_y=[0.6, 0.95]
        )
        utils.style_plotly_fig(fig_comp, theme)
        st.plotly_chart(fig_comp, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with row1_cols[1]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;'>Random Forest Feature Importance</h3>", unsafe_allow_html=True)
        
        df_feat_sorted = df_feat.sort_values("Importance", ascending=True)
        
        fig_feat = px.bar(
            df_feat_sorted,
            y="Feature",
            x="Importance",
            orientation="h",
            color="Importance",
            color_continuous_scale=utils.CONTINUOUS_SCALE,
            title="Relative Feature Importance Weights"
        )
        fig_feat.update_layout(coloraxis_showscale=False)
        utils.style_plotly_fig(fig_feat, theme)
        st.plotly_chart(fig_feat, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
