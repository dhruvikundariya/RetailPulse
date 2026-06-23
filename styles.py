# styles.py

def get_css():
    """
    Returns custom CSS for the clean Light Theme dashboard design.
    """
    bg_color = "#f8fafc"
    card_bg = "rgba(255, 255, 255, 0.75)"
    card_border = "1px solid rgba(0, 0, 0, 0.06)"
    text_primary = "#1e293b"
    text_secondary = "#64748b"
    shadow = "0 8px 32px 0 rgba(31, 38, 135, 0.07)"
    sidebar_bg = "#ffffff"
    metric_val_color = "#6366f1" # Indigo

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    /* Global settings */
    html, body, [class*="css"], .stApp {{
        font-family: 'Outfit', sans-serif;
        background-color: {bg_color} !important;
        color: {text_primary} !important;
    }}

    /* Remove Streamlit default header/footer */
    #MainMenu, footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stDeployButton {{display:none;}}

    /* Custom main container spacing */
    .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }}

    /* Glassmorphism Card styling */
    .glass-card {{
        background: {card_bg} !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border-radius: 16px !important;
        border: {card_border} !important;
        box-shadow: {shadow} !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
        transition: all 0.3s ease-in-out !important;
    }}
    .glass-card:hover {{
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 40px 0 rgba(99, 102, 241, 0.15) !important;
        border-color: rgba(99, 102, 241, 0.3) !important;
    }}

    /* Header styling with gradient underline */
    .header-container {{
        margin-bottom: 30px;
    }}
    .header-title {{
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        padding-bottom: 8px;
    }}
    .header-subtitle {{
        font-size: 1rem;
        color: {text_secondary};
        margin: 0;
    }}

    /* KPI styling inside glass card */
    .kpi-title {{
        font-size: 0.9rem;
        font-weight: 600;
        color: {text_secondary};
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }}
    .kpi-value {{
        font-size: 2rem;
        font-weight: 700;
        color: {text_primary};
        margin-bottom: 4px;
        background: linear-gradient(135deg, {metric_val_color} 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .kpi-delta {{
        font-size: 0.85rem;
        font-weight: 600;
        display: flex;
        align-items: center;
    }}
    .delta-up {{
        color: #10b981 !important; /* Emerald green */
    }}
    .delta-down {{
        color: #ef4444 !important; /* Rose red */
    }}

    /* Segment card styling */
    .segment-card {{
        border-radius: 12px !important;
        padding: 16px !important;
        color: #ffffff !important;
        font-weight: 600;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
        margin-bottom: 12px;
        transition: transform 0.2s;
    }}
    .segment-card:hover {{
        transform: scale(1.02);
    }}
    .segment-champions {{
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    }}
    .segment-loyal {{
        background: linear-gradient(135deg, #10b981, #3b82f6) !important;
    }}
    .segment-atrisk {{
        background: linear-gradient(135deg, #f59e0b, #ef4444) !important;
    }}
    .segment-lost {{
        background: linear-gradient(135deg, #64748b, #475569) !important;
    }}
    .segment-new {{
        background: linear-gradient(135deg, #ec4899, #f43f5e) !important;
    }}

    /* Badges */
    .badge {{
        display: inline-block;
        padding: 4px 8px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
    }}
    .badge-danger {{
        background-color: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }}
    .badge-warning {{
        background-color: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }}
    .badge-success {{
        background-color: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }}

    /* Sidebar customize */
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {card_border.split(' ')[2]} !important;
    }}
    
    /* Modify sidebar text colors */
    section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span {{
        color: {text_primary} !important;
    }}

    /* Sidebar Logo */
    .sidebar-logo {{
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 24px;
        text-align: center;
        letter-spacing: -0.02em;
    }}

    /* Tabs override */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: transparent !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 40px;
        white-space: pre-wrap;
        background-color: {card_bg} !important;
        border: {card_border} !important;
        border-radius: 8px !important;
        color: {text_secondary} !important;
        font-weight: 600 !important;
        padding: 10px 16px !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: #6366f1 !important;
        border-color: #6366f1 !important;
        background-color: rgba(99, 102, 241, 0.08) !important;
    }}

    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    ::-webkit-scrollbar-track {{
        background: transparent;
    }}
    ::-webkit-scrollbar-thumb {{
        background: {text_secondary}40;
        border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: {text_secondary}80;
    }}

    /* Table styling */
    .dataframe {{
        background-color: {card_bg} !important;
        border: {card_border} !important;
        border-radius: 8px !important;
        color: {text_primary} !important;
    }}
    .dataframe th {{
        background-color: {bg_color} !important;
        color: {text_secondary} !important;
        font-weight: 600 !important;
    }}

    /* Alert / Success overrides */
    .stAlert {{
        border-radius: 12px !important;
        background: {card_bg} !important;
        border: {card_border} !important;
    }}
    </style>
    """
    return css

def render_kpi_card(title, value, delta=None, delta_up=True, suffix=""):
    """
    Generates a HTML string for a beautiful glassmorphic KPI card.
    """
    delta_html = ""
    if delta is not None:
        delta_class = "delta-up" if delta_up else "delta-down"
        delta_sign = "+" if delta_up else ""
        delta_html = f'<div class="kpi-delta {delta_class}">{delta_sign}{delta}</div>'
    
    html = f"""
    <div class="glass-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}{suffix}</div>
        {delta_html}
    </div>
    """
    return html

def render_segment_card(title, count, percentage, css_class):
    """
    Generates a segment card HTML.
    """
    html = f"""
    <div class="segment-card {css_class}">
        <div style="font-size: 0.85rem; opacity: 0.8; text-transform: uppercase;">{title}</div>
        <div style="font-size: 1.8rem; font-weight: 800; margin: 4px 0;">{count:,}</div>
        <div style="font-size: 0.85rem; opacity: 0.9;">{percentage}% of customers</div>
    </div>
    """
    return html
