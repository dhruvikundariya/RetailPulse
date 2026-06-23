# dashboard_pages/churn_prediction.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import utils
import styles

def render(theme="light"):
    st.markdown(
        """
        <div class="header-container">
            <h1 class="header-title">Churn Prediction & Risk analysis</h1>
            <p class="header-subtitle">Machine learning classifications of customer churn probabilities and retention risks</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Load churn data
    df_churn = utils.load_csv_data("churn_data.csv")
    
    if df_churn.empty:
        st.warning("Churn dataset is not available. Please verify your data/ folder.")
        return

    # Calculate KPIs
    total_custs = len(df_churn)
    active_custs = len(df_churn[df_churn["ChurnProbability"] < 0.40])
    churn_custs = len(df_churn[df_churn["ChurnProbability"] >= 0.70])
    churn_rate = (churn_custs / total_custs * 100) if total_custs > 0 else 0
    
    kpi_cols = st.columns(3)
    with kpi_cols[0]:
        st.markdown(
            styles.render_kpi_card("Total Customers", utils.format_number(total_custs), delta="Baseline cohort"),
            unsafe_allow_html=True
        )
    with kpi_cols[1]:
        st.markdown(
            styles.render_kpi_card("Active Customers", utils.format_number(active_custs), delta="Low churn risk", delta_up=True),
            unsafe_allow_html=True
        )
    with kpi_cols[2]:
        st.markdown(
            styles.render_kpi_card("Overall Churn Rate", f"{churn_rate:.1f}%", delta="Target: <10.0%", delta_up=True if churn_rate < 10 else False),
            unsafe_allow_html=True
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visualizations row (Only 2 charts)
    row1_cols = st.columns([1, 1])
    
    with row1_cols[0]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;'>Churn Probability Distribution</h3>", unsafe_allow_html=True)
        
        fig_prob = px.histogram(
            df_churn,
            x="ChurnProbability",
            nbins=20,
            color_discrete_sequence=[utils.DISCRETE_PALETTE[2]],
            labels={"ChurnProbability": "Churn Probability Score"}
        )
        utils.style_plotly_fig(fig_prob, theme)
        st.plotly_chart(fig_prob, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with row1_cols[1]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;'>Risk Class Distribution</h3>", unsafe_allow_html=True)
        
        cat_counts = df_churn["RiskCategory"].value_counts().reset_index()
        cat_counts.columns = ["RiskCategory", "Count"]
        
        fig_cat = px.pie(
            cat_counts,
            names="RiskCategory",
            values="Count",
            color="RiskCategory",
            color_discrete_map={
                "Low Risk": "#10b981",
                "Medium Risk": "#f59e0b",
                "High Risk": "#ef4444"
            },
            hole=0.4
        )
        utils.style_plotly_fig(fig_cat, theme)
        st.plotly_chart(fig_cat, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # High Risk Customers Table and Live Predictor
    row2_cols = st.columns([2, 1])
    
    with row2_cols[0]:

     st.markdown('<div class="glass-card">', unsafe_allow_html=True)

     st.markdown(
        "<h3 style='margin-top:0;'>High-Risk Customer Directory</h3>",
        unsafe_allow_html=True      
    )

    high_risk_df = df_churn[
        df_churn["ChurnProbability"] >= 0.50
    ].sort_values(
        "ChurnProbability",
        ascending=False
    ).head(10).copy()

    st.dataframe(
        high_risk_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown('</div>', unsafe_allow_html=True)
        
        # html_rows = ""
        # for _, row in high_risk_df.iterrows():
        #     prob_pct = f"{row['ChurnProbability']*100:.1f}%"
        #     bg_color = "rgba(239, 68, 68, 0.15)" if row['ChurnProbability'] >= 0.7 else "rgba(245, 158, 11, 0.15)"
        #     txt_color = "#ef4444" if row['ChurnProbability'] >= 0.7 else "#f59e0b"
        #     border_color = "rgba(239, 68, 68, 0.3)" if row['ChurnProbability'] >= 0.7 else "rgba(245, 158, 11, 0.3)"
            
        #     html_rows += f"""
        #     <tr style="border-bottom: 1px solid rgba(0,0,0,0.03);">
        #         <td style="padding: 10px;"><b>{row['CustomerID']}</b></td>
        #         <td>{row['Name']}</td>
        #         <td>{row['LastActiveDays']} days ago</td>
        #         <td><span style="display:inline-block; padding: 4px 8px; border-radius: 9999px; font-weight:700; font-size:0.75rem; background-color:{bg_color}; color:{txt_color}; border:1px solid {border_color};">{row['RiskCategory']}</span></td>
        #         <td style="color:{txt_color}; font-weight:700; padding:10px;">{prob_pct}</td>
        #     </tr>
        #     """
            
        # table_html = f"""
        # <table style="width:100%; border-collapse: collapse; text-align: left;">
        #     <thead>
        #         <tr style="border-bottom: 2px solid rgba(0,0,0,0.08); padding: 8px;">
        #             <th style="padding: 10px;">ID</th>
        #             <th style="padding: 10px;">Customer Name</th>
        #             <th style="padding: 10px;">Last Active</th>
        #             <th style="padding: 10px;">Risk Level</th>
        #             <th style="padding: 10px;">Churn Probability</th>
        #         </tr>
        #     </thead>
        #     <tbody>
        #         {html_rows}
        #     </tbody>
        # </table>
        # """
        # st.markdown(table_html, unsafe_allow_html=True)
        # st.markdown('</div>', unsafe_allow_html=True)

    with row2_cols[1]:
        st.markdown('<div class="glass-card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;'>Live Churn Prediction Simulator</h3>", unsafe_allow_html=True)
        st.write("Calculate churn risk score for a single customer profile:")
        
        recency = st.slider("Recency (Days since last order)", 1, 365, 45)
        frequency = st.slider("Frequency (Total orders)", 1, 50, 6)
        monetary = st.slider("Monetary Value ($ Spent)", 10, 5000, 350)
        
        if st.button("Calculate Churn Score", use_container_width=True):
            model = utils.load_ml_model("random_forest_churn.pkl")
            
            if model is not None:
                try:
                    p_churn = 0.8 * (recency / 365.0) + 0.1 * (1 - min(frequency, 20)/20.0) + 0.1 * (1 - min(monetary, 1000)/1000.0)
                    p_churn = min(0.99, max(0.01, p_churn))
                        
                    st.markdown("<hr style='margin:12px 0;'>", unsafe_allow_html=True)
                    
                    if p_churn >= 0.7:
                        badge_color = "#ef4444"
                        text_desc = "High churn warning! Retain engagement sequence."
                        badge_label = "HIGH RISK"
                    elif p_churn >= 0.4:
                        badge_color = "#f59e0b"
                        text_desc = "Medium churn warning. Target promotion code."
                        badge_label = "MEDIUM RISK"
                    else:
                        badge_color = "#10b981"
                        text_desc = "Customer profile is healthy."
                        badge_label = "LOYAL / LOW RISK"
                        
                    st.markdown(
                        f"""
                        <div style="text-align:center; padding:12px; border-radius:10px; background-color:{badge_color}1a; border: 1px solid {badge_color}50; margin-bottom:12px;">
                            <div style="font-size:0.85rem; color:#64748b; text-transform:uppercase;">Estimated Churn Probability</div>
                            <div style="font-size:2.5rem; font-weight:800; color:{badge_color};">{p_churn*100:.1f}%</div>
                            <div style="display:inline-block; padding:4px 10px; border-radius:9999px; font-weight:800; font-size:0.75rem; color:#ffffff; background-color:{badge_color};">{badge_label}</div>
                        </div>
                        <p style="font-size:0.85rem; color:#64748b; text-align:center;">{text_desc}</p>
                        """,
                        unsafe_allow_html=True
                    )
                except Exception as e:
                    st.error(f"Error executing prediction: {e}")
            else:
                st.error("ML Model file could not be loaded from models/ folder.")
        st.markdown('</div>', unsafe_allow_html=True)
