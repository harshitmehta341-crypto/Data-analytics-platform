
import requests
import pandas as pd
import plotly.express as px
import streamlit as st

API_URL = "https://data-analytics-platform-wfp4.onrender.com"

st.set_page_config(
    page_title="NEXUS | Data Analytics",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- BLACK & GOLD DESIGN ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --gold: #D6B46A;
    --gold-light: #F5DE9B;
    --bg: #090A0C;
    --panel: #121316;
    --text: #F4F0E6;
    --muted: #9A9BA2;
}

.stApp {
    background:
      radial-gradient(ellipse at 80% 0%, #29200e 0%, transparent 34%),
      linear-gradient(135deg, #090A0C, #101114 55%, #090A0C);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text) !important;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #141416, #090A0C);
    border-right: 1px solid #39301d;
}

[data-testid="stSidebar"] * {
    color: #E8D9B4;
}

.hero {
    background: linear-gradient(120deg, #1B1A16, #111214 65%, #29200E);
    border: 1px solid #756039;
    border-radius: 22px;
    padding: 30px 32px;
    margin-bottom: 25px;
    box-shadow: 0 12px 40px #00000066, inset 0 1px 0 #ffffff12;
    position: relative;
    overflow: hidden;
}

.hero:after {
    content: "◆";
    position: absolute;
    right: 35px;
    top: 5px;
    font-size: 100px;
    color: #D6B46A16;
}

.eyebrow {
    color: var(--gold);
    letter-spacing: 3px;
    font-size: 11px;
    font-weight: 700;
}

.hero h1 {
    font-size: clamp(30px, 4vw, 46px);
    margin: 12px 0 6px;
    background: linear-gradient(90deg, #FFF5D5, #D6B46A);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #B8B5AC;
    margin: 0;
    font-size: 14px;
}

.section-title {
    color: #E8D9B4;
    font-size: 19px;
    font-weight: 700;
    margin: 28px 0 14px;
}

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #1C1C1E, #111214);
    border: 1px solid #4A3C23;
    border-radius: 17px;
    padding: 20px 22px;
    box-shadow: 0 8px 20px #00000055, inset 0 1px 0 #ffffff0a;
    transition: all 0.2s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: #D6B46A;
    box-shadow: 0 12px 28px #D6B46A18;
}

div[data-testid="stMetricLabel"] {
    color: #B9B4A7 !important;
}

div[data-testid="stMetricValue"] {
    color: #F2D58C !important;
    font-family: 'Space Grotesk', sans-serif;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #453921;
    border-radius: 12px;
    overflow: hidden;
}

.stButton button, .stDownloadButton button {
    background: linear-gradient(135deg, #F0D58F, #B28B3D);
    color: #14110A !important;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    transition: all 0.2s ease;
}

.stButton button:hover, .stDownloadButton button:hover {
    background: #FFE8AC;
    box-shadow: 0 0 20px #D6B46A35;
    transform: translateY(-2px);
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

hr {
    border-color: #39301F;
}

footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ---------- API CONNECTION ----------
@st.cache_data(ttl=30)
def get_data(endpoint):
    response = requests.get(f"{API_URL}{endpoint}", timeout=60)
    response.raise_for_status()
    return response.json()


# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## ◆ NEXUS")
    st.caption("DATA INTELLIGENCE PLATFORM")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        ["Overview", "Sales Records", "Analytics"],
    )

    st.divider()
    st.markdown("**SYSTEM STATUS**")
    st.caption("FastAPI · REST · SQL Analytics")
    st.caption("Dashboard refresh interval: 30 sec")
    if st.button("↻ Refresh data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()


# ---------- HERO ----------
st.markdown("""
<div class="hero">
  <div class="eyebrow">BUSINESS INTELLIGENCE / LIVE DASHBOARD</div>
  <h1>Data, with a clearer perspective.</h1>
  <p>Explore sales performance, monitor revenue, and turn structured data into insights.</p>
</div>
""", unsafe_allow_html=True)

try:
    health = get_data("/api/v1/health")
    summary = get_data("/api/v1/analytics/summary")
    category_response = get_data("/api/v1/analytics/categories")
    products_response = get_data("/api/v1/analytics/top-products")
    records_response = get_data("/api/v1/records?limit=100&offset=0")

    categories = (
        category_response.get("categories", [])
        if isinstance(category_response, dict)
        else category_response
    )

    products = (
        products_response.get("top_products", [])
        if isinstance(products_response, dict)
        else products_response
    )

    records = records_response.get("data", [])

    st.success("Connected to the live analytics API")

    # ---------- KPI CARDS ----------
    st.markdown('<div class="section-title">✦ Business Overview</div>',
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "TOTAL RECORDS",
            f"{summary.get('total_records', 0):,}",
        )

    with col2:
        st.metric(
            "TOTAL REVENUE",
            f"₹{summary.get('total_revenue', 0):,.2f}",
        )

    with col3:
        st.metric(
            "AVERAGE RECORD VALUE",
            f"₹{summary.get('average_record_value', 0):,.2f}",
        )

    # ---------- PAGE: OVERVIEW ----------
    if page == "Overview":
        st.markdown('<div class="section-title">✦ Revenue Intelligence</div>',
                    unsafe_allow_html=True)

        if records:
            df = pd.DataFrame(records)

            if {"category", "total_value"}.issubset(df.columns):
                chart_df = (
                    df.groupby("category", as_index=False)["total_value"]
                    .sum()
                    .rename(columns={"total_value": "Revenue"})
                )

                fig = px.bar(
                    chart_df,
                    x="category",
                    y="Revenue",
                    color="Revenue",
                    color_continuous_scale=["#75551F", "#D6B46A", "#FFF0BD"],
                    template="plotly_dark",
                    title="Revenue by Category",
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#EDE5D1",
                    title_font_color="#F2D58C",
                    coloraxis_showscale=False,
                    margin=dict(l=10, r=10, t=55, b=10),
                )
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("#### Recent Sales Records")
            st.dataframe(df.head(10), use_container_width=True,
                         hide_index=True)
        else:
            st.info("No sales records available yet. Add a record through the API.")

    # ---------- PAGE: SALES RECORDS ----------
    elif page == "Sales Records":
        st.markdown('<div class="section-title">✦ Sales Database</div>',
                    unsafe_allow_html=True)

        if records:
            df = pd.DataFrame(records)

            search = st.text_input("Search records", placeholder="Search product or category...")
            if search:
                mask = df.astype(str).apply(
                    lambda col: col.str.contains(search, case=False, na=False)
                ).any(axis=1)
                df = df[mask]

            st.caption(f"{len(df)} records displayed")
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.download_button(
                "↓ Export CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="sales_records.csv",
                mime="text/csv",
            )
        else:
            st.info("No records found.")

    # ---------- PAGE: ANALYTICS ----------
    elif page == "Analytics":
        st.markdown('<div class="section-title">✦ Advanced Analytics</div>',
                    unsafe_allow_html=True)

        left, right = st.columns(2)

        with left:
            st.markdown("#### Category Performance")
            if categories:
                cat_df = pd.DataFrame(categories)
                st.dataframe(cat_df, use_container_width=True, hide_index=True)

                if {"category", "revenue"}.issubset(cat_df.columns):
                    fig = px.pie(
                        cat_df,
                        names="category",
                        values="revenue",
                        hole=0.65,
                        color_discrete_sequence=[
                            "#D6B46A", "#8D6B2D", "#F5DE9B",
                            "#6E6250", "#B7A16D",
                        ],
                        template="plotly_dark",
                    )
                    fig.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        font_color="#EDE5D1",
                        margin=dict(l=5, r=5, t=20, b=5),
                        legend_title_text="Category",
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No category data available.")

        with right:
            st.markdown("#### Top Products")
            if products:
                product_df = pd.DataFrame(products)
                st.dataframe(product_df, use_container_width=True,
                             hide_index=True)
            else:
                st.info("No top-product data available.")

    st.divider()
    st.caption("NEXUS DATA INTELLIGENCE  ·  Powered by FastAPI, SQLAlchemy & Streamlit")

except requests.RequestException as error:
    st.error("Could not connect to the API. The free server may be waking up.")
    st.caption(str(error))
except (ValueError, TypeError, KeyError) as error:
    st.error("The API returned data in an unexpected format.")
    st.caption(str(error))
