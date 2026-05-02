"""
E-Commerce Intelligence Dashboard
Demo dashboard com IA integrada — Claudenilson Junior
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date, timedelta
import requests, json, os

# ── PAGE CONFIG ───────────────────────────────────────
st.set_page_config(
    page_title="DataLens · E-Commerce Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── DESIGN SYSTEM ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500&display=swap');

:root {
  --bg:       #080c14;
  --surface:  #0e1420;
  --border:   #1a2235;
  --accent:   #00d4ff;
  --accent2:  #7c3aed;
  --green:    #00e5a0;
  --red:      #ff4757;
  --amber:    #ffb547;
  --text:     #e8edf5;
  --muted:    #5a6a85;
  --font-display: 'Syne', sans-serif;
  --font-mono:    'DM Mono', monospace;
  --font-body:    'Inter', sans-serif;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--font-body) !important;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding: 1.5rem 2rem !important; max-width: 1400px !important; }

/* Metric cards */
[data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1.2rem !important;
}
[data-testid="stMetricLabel"] { 
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}
[data-testid="stMetricValue"] {
    font-family: var(--font-display) !important;
    font-size: 26px !important;
    font-weight: 700 !important;
    color: var(--text) !important;
}
[data-testid="stMetricDelta"] { font-family: var(--font-mono) !important; font-size: 12px !important; }

/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 2px !important;
    border: 1px solid var(--border) !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
    letter-spacing: 0.5px !important;
    color: var(--muted) !important;
    border-radius: 7px !important;
    padding: 6px 16px !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: var(--accent) !important;
    color: var(--bg) !important;
    font-weight: 600 !important;
}

/* Inputs */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] select,
.stDateInput input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: var(--font-body) !important;
}

/* Chat container */
.chat-msg-user {
    background: linear-gradient(135deg, #1a2a4a, #162040);
    border: 1px solid #2a3a5a;
    border-radius: 12px 12px 4px 12px;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 14px;
    line-height: 1.6;
}
.chat-msg-ai {
    background: linear-gradient(135deg, #0a1a12, #081510);
    border: 1px solid #1a3025;
    border-left: 3px solid var(--green);
    border-radius: 4px 12px 12px 12px;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 14px;
    line-height: 1.7;
}
.anomaly-badge {
    display: inline-block;
    background: rgba(255,71,87,0.15);
    border: 1px solid rgba(255,71,87,0.4);
    color: #ff4757;
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 600;
    font-family: var(--font-mono);
    letter-spacing: 0.5px;
}
.section-label {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
}
.logo-text {
    font-family: var(--font-display);
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.5px;
}
.logo-accent { color: var(--accent); }
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(__file__)
    sales    = pd.read_csv(f"{base}/data/sales.csv", parse_dates=["date"])
    products = pd.read_csv(f"{base}/data/products.csv")
    merged   = sales.merge(products[["product_id","product_name","rating","review_count","supplier"]], on="product_id", how="left")
    return merged, products

df_all, df_products = load_data()

# ── SIDEBAR ───────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="logo-text">◈ Data<span class="logo-accent">Lens</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px;color:var(--muted);margin-bottom:20px;font-family:var(--font-mono)">E-COMMERCE INTELLIGENCE</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">Date Range</div>', unsafe_allow_html=True)
    min_date = df_all["date"].min().date()
    max_date = df_all["date"].max().date()
    d_start = st.date_input("From", value=date(2024, 1, 1), min_value=min_date, max_value=max_date)
    d_end   = st.date_input("To",   value=max_date,         min_value=min_date, max_value=max_date)

    st.markdown('<div class="section-label" style="margin-top:16px">Filters</div>', unsafe_allow_html=True)
    cats = ["All"] + sorted(df_all["category"].unique().tolist())
    sel_cat = st.selectbox("Category", cats)

    channels = ["All"] + sorted(df_all["channel"].unique().tolist())
    sel_ch  = st.selectbox("Channel", channels)

    countries = ["All"] + sorted(df_all["country"].unique().tolist())
    sel_co  = st.selectbox("Country", countries)

    st.markdown("---")
    st.markdown('<div style="font-size:11px;color:var(--muted);font-family:var(--font-mono)">AI ASSISTANT</div>', unsafe_allow_html=True)
    api_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")
    st.markdown('<div style="font-size:10px;color:var(--muted)">Optional — enables natural language analysis</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f'<div style="font-size:10px;color:var(--muted);font-family:var(--font-mono)">BUILT BY<br><span style="color:var(--accent)">Claudenilson Junior</span><br>Data Analyst</div>', unsafe_allow_html=True)

# ── FILTER DATA ───────────────────────────────────────
mask = (df_all["date"].dt.date >= d_start) & (df_all["date"].dt.date <= d_end)
if sel_cat != "All":  mask &= df_all["category"] == sel_cat
if sel_ch  != "All":  mask &= df_all["channel"]  == sel_ch
if sel_co  != "All":  mask &= df_all["country"]  == sel_co
df = df_all[mask].copy()

# Período anterior para comparação
days_range  = (d_end - d_start).days
prev_end    = d_start - timedelta(days=1)
prev_start  = prev_end - timedelta(days=days_range)
mask_prev   = (df_all["date"].dt.date >= prev_start) & (df_all["date"].dt.date <= prev_end)
df_prev     = df_all[mask_prev]

def delta_pct(curr, prev):
    if prev == 0: return 0
    return round((curr - prev) / prev * 100, 1)

# ── MAIN CONTENT ──────────────────────────────────────
st.markdown('<div style="font-family:var(--font-display);font-size:28px;font-weight:800;margin-bottom:4px">Sales Intelligence Dashboard</div>', unsafe_allow_html=True)
st.markdown(f'<div style="font-family:var(--font-mono);font-size:11px;color:var(--muted);margin-bottom:24px">{d_start.strftime("%b %d, %Y")} — {d_end.strftime("%b %d, %Y")} &nbsp;·&nbsp; {len(df):,} transactions</div>', unsafe_allow_html=True)

# ── KPI ROW ───────────────────────────────────────────
rev      = df["revenue"].sum()
rev_prev = df_prev["revenue"].sum()
mgn      = df["gross_margin"].sum()
mgn_prev = df_prev["gross_margin"].sum()
orders   = len(df)
ord_prev = len(df_prev)
aov      = rev / orders if orders else 0
aov_prev = (rev_prev / ord_prev) if ord_prev else 0
ret_rate = df["returned"].mean() * 100

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Revenue",       f"${rev/1e6:.2f}M",   f"{delta_pct(rev,rev_prev):+.1f}%")
c2.metric("Gross Margin",  f"${mgn/1e6:.2f}M",   f"{delta_pct(mgn,mgn_prev):+.1f}%")
c3.metric("Margin %",      f"{mgn/rev*100:.1f}%" if rev else "—", f"{delta_pct(mgn/rev if rev else 0, mgn_prev/rev_prev if rev_prev else 0)*100:.1f}pp")
c4.metric("Avg Order",     f"${aov:.2f}",         f"{delta_pct(aov,aov_prev):+.1f}%")
c5.metric("Return Rate",   f"{ret_rate:.1f}%",    None)

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈  Revenue Trends",
    "🏷  Products",
    "📡  Channels & Geo",
    "⚠️  Anomaly Detection",
    "🤖  AI Assistant",
])

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Mono, monospace", color="#5a6a85", size=11),
    xaxis=dict(gridcolor="#1a2235", linecolor="#1a2235", tickcolor="#1a2235"),
    yaxis=dict(gridcolor="#1a2235", linecolor="#1a2235"),
    margin=dict(l=0, r=0, t=30, b=0),
)

# ── TAB 1: REVENUE TRENDS ─────────────────────────────
with tab1:
    col_l, col_r = st.columns([2, 1])

    with col_l:
        st.markdown('<div class="section-label">Daily Revenue + 7-Day Moving Average</div>', unsafe_allow_html=True)
        daily = df.groupby("date").agg(revenue=("revenue","sum"), margin=("gross_margin","sum")).reset_index()
        daily["ma7"] = daily["revenue"].rolling(7).mean()

        fig = go.Figure()
        fig.add_trace(go.Bar(x=daily["date"], y=daily["revenue"], name="Daily Revenue",
                             marker_color="rgba(0,212,255,0.25)", marker_line_width=0))
        fig.add_trace(go.Scatter(x=daily["date"], y=daily["ma7"], name="7D MA",
                                 line=dict(color="#00d4ff", width=2.5), mode="lines"))
        fig.update_layout(**PLOTLY_THEME, height=280, showlegend=True,
                          legend=dict(orientation="h", y=1.1, x=0, font=dict(size=10)))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-label">Revenue by Category</div>', unsafe_allow_html=True)
        cat_rev = df.groupby("category")["revenue"].sum().sort_values(ascending=True)
        fig2 = go.Figure(go.Bar(
            x=cat_rev.values, y=cat_rev.index, orientation="h",
            marker=dict(color=cat_rev.values,
                        colorscale=[[0,"#1a2235"],[0.5,"#0066aa"],[1,"#00d4ff"]],
                        showscale=False),
            text=[f"${v/1e6:.1f}M" for v in cat_rev.values],
            textposition="outside", textfont=dict(size=10, color="#5a6a85"),
        ))
        fig2.update_layout(**PLOTLY_THEME, height=280)
        fig2.update_xaxes(visible=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-label">Monthly Margin Trend</div>', unsafe_allow_html=True)
    monthly = df.copy()
    monthly["month"] = monthly["date"].dt.to_period("M").astype(str)
    monthly_agg = monthly.groupby("month").agg(
        revenue=("revenue","sum"), margin=("gross_margin","sum")
    ).reset_index()
    monthly_agg["margin_pct"] = monthly_agg["margin"] / monthly_agg["revenue"] * 100

    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3.add_trace(go.Bar(x=monthly_agg["month"], y=monthly_agg["revenue"],
                          name="Revenue", marker_color="rgba(124,58,237,0.5)"), secondary_y=False)
    fig3.add_trace(go.Scatter(x=monthly_agg["month"], y=monthly_agg["margin_pct"],
                              name="Margin %", line=dict(color="#00e5a0", width=2.5),
                              mode="lines+markers", marker=dict(size=5)), secondary_y=True)
    fig3.update_layout(**PLOTLY_THEME, height=240, showlegend=True,
                       legend=dict(orientation="h", y=1.12, x=0, font=dict(size=10)))
    fig3.update_yaxes(gridcolor="#1a2235", tickformat="$,.0f", secondary_y=False)
    fig3.update_yaxes(gridcolor="rgba(0,0,0,0)", tickformat=".1f", ticksuffix="%", secondary_y=True)
    st.plotly_chart(fig3, use_container_width=True)

# ── TAB 2: PRODUCTS ───────────────────────────────────
with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-label">Top 15 Products by Revenue</div>', unsafe_allow_html=True)
        top_prods = df.groupby(["product_id","product_name","category"]).agg(
            revenue=("revenue","sum"),
            units=("units_sold","sum"),
            margin=("gross_margin","sum"),
        ).reset_index().sort_values("revenue", ascending=False).head(15)
        top_prods["margin_pct"] = (top_prods["margin"] / top_prods["revenue"] * 100).round(1)

        fig4 = px.bar(top_prods, x="revenue", y="product_name", orientation="h",
                      color="margin_pct", color_continuous_scale=["#1a2235","#00d4ff","#00e5a0"],
                      hover_data={"units": True, "margin_pct": ":.1f"},
                      labels={"revenue":"Revenue","product_name":"","margin_pct":"Margin %"})
        fig4.update_layout(**PLOTLY_THEME, height=380, coloraxis_showscale=False)
        fig4.update_traces(texttemplate="$%{x:,.0f}", textposition="outside",
                           textfont=dict(size=9, color="#5a6a85"))
        st.plotly_chart(fig4, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-label">Price vs Margin — Bubble = Units Sold</div>', unsafe_allow_html=True)
        prod_summary = df.groupby(["product_id","product_name","category"]).agg(
            avg_price=("unit_price","mean"),
            margin_pct=("gross_margin","sum"),
            revenue=("revenue","sum"),
            units=("units_sold","sum"),
        ).reset_index()
        prod_summary["margin_pct"] = prod_summary["margin_pct"] / prod_summary["revenue"] * 100
        prod_summary = prod_summary[prod_summary["revenue"] > 0]

        fig5 = px.scatter(prod_summary, x="avg_price", y="margin_pct",
                          size="units", color="category", hover_name="product_name",
                          size_max=40, opacity=0.8,
                          color_discrete_sequence=["#00d4ff","#7c3aed","#00e5a0","#ffb547",
                                                   "#ff4757","#ff6b9d","#a8ff78","#f8f8f8"])
        fig5.update_layout(**PLOTLY_THEME, height=380,
                           legend=dict(orientation="h", y=-0.15, font=dict(size=9)))
        fig5.update_xaxes(tickprefix="$")
        fig5.update_yaxes(ticksuffix="%")
        st.plotly_chart(fig5, use_container_width=True)

    st.markdown('<div class="section-label">Discount Impact on Margin</div>', unsafe_allow_html=True)
    df["discount_band"] = pd.cut(df["discount_pct"],
                                  bins=[-1,0,5,15,25,100],
                                  labels=["No discount","1–5%","6–15%","16–25%","25%+"])
    disc_agg = df.groupby("discount_band", observed=True).agg(
        revenue=("revenue","sum"),
        margin_pct=("gross_margin","sum"),
        rev_total=("revenue","sum"),
    ).reset_index()
    disc_agg["margin_pct2"] = df.groupby("discount_band", observed=True).apply(
        lambda x: x["gross_margin"].sum() / x["revenue"].sum() * 100 if x["revenue"].sum() > 0 else 0
    ).values

    fig6 = make_subplots(specs=[[{"secondary_y": True}]])
    fig6.add_trace(go.Bar(x=disc_agg["discount_band"].astype(str), y=disc_agg["revenue"],
                          name="Revenue", marker_color="rgba(0,212,255,0.4)"), secondary_y=False)
    fig6.add_trace(go.Scatter(x=disc_agg["discount_band"].astype(str), y=disc_agg["margin_pct2"],
                              name="Margin %", line=dict(color="#ff4757", width=2.5),
                              mode="lines+markers"), secondary_y=True)
    fig6.update_layout(**PLOTLY_THEME, height=220, showlegend=True,
                       legend=dict(orientation="h", y=1.15, font=dict(size=10)))
    fig6.update_yaxes(tickformat="$,.0f", secondary_y=False, gridcolor="#1a2235")
    fig6.update_yaxes(ticksuffix="%", secondary_y=True, gridcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig6, use_container_width=True)

# ── TAB 3: CHANNELS & GEO ────────────────────────────
with tab3:
    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown('<div class="section-label">Revenue by Channel</div>', unsafe_allow_html=True)
        ch_agg = df.groupby("channel").agg(
            revenue=("revenue","sum"), orders=("revenue","count")
        ).reset_index().sort_values("revenue", ascending=False)

        fig7 = go.Figure(go.Pie(
            labels=ch_agg["channel"], values=ch_agg["revenue"],
            hole=0.6, textfont=dict(size=11),
            marker=dict(colors=["#00d4ff","#7c3aed","#00e5a0","#ffb547","#ff4757","#ff6b9d"],
                        line=dict(color=["#080c14"]*6, width=2)),
        ))
        fig7.update_layout(**PLOTLY_THEME, height=280,
                           legend=dict(orientation="h", y=-0.1, font=dict(size=10)))
        st.plotly_chart(fig7, use_container_width=True)

    with col_d:
        st.markdown('<div class="section-label">Revenue by Country</div>', unsafe_allow_html=True)
        geo_agg = df.groupby("country")["revenue"].sum().reset_index().sort_values("revenue", ascending=False)
        fig8 = px.choropleth(geo_agg, locations="country", locationmode="country names",
                             color="revenue", color_continuous_scale=["#0e1420","#0066aa","#00d4ff"],
                             hover_name="country")
        fig8.update_layout(**PLOTLY_THEME, height=280, geo=dict(
            bgcolor="rgba(0,0,0,0)", showframe=False, showcoastlines=True,
            coastlinecolor="#1a2235", landcolor="#0e1420", oceancolor="#080c14",
            showocean=True,
        ), coloraxis_showscale=False)
        st.plotly_chart(fig8, use_container_width=True)

    st.markdown('<div class="section-label">Channel Performance Over Time</div>', unsafe_allow_html=True)
    ch_monthly = df.copy()
    ch_monthly["month"] = ch_monthly["date"].dt.to_period("M").astype(str)
    ch_time = ch_monthly.groupby(["month","channel"])["revenue"].sum().reset_index()
    fig9 = px.line(ch_time, x="month", y="revenue", color="channel",
                   color_discrete_sequence=["#00d4ff","#7c3aed","#00e5a0","#ffb547","#ff4757","#a78bfa"])
    fig9.update_layout(**PLOTLY_THEME, height=220,
                       legend=dict(orientation="h", y=1.15, font=dict(size=10)))
    fig9.update_yaxes(tickformat="$,.0f")
    st.plotly_chart(fig9, use_container_width=True)

# ── TAB 4: ANOMALY DETECTION ──────────────────────────
with tab4:
    st.markdown('<div class="section-label">Automated Anomaly Detection — Z-Score Method (|z| > 2.5)</div>', unsafe_allow_html=True)

    daily_rev = df.groupby("date")["revenue"].sum().reset_index()
    daily_rev["ma7"]   = daily_rev["revenue"].rolling(7, center=True).mean()
    daily_rev["std7"]  = daily_rev["revenue"].rolling(7, center=True).std()
    daily_rev["z"]     = (daily_rev["revenue"] - daily_rev["ma7"]) / (daily_rev["std7"] + 1)
    daily_rev["anomaly"] = daily_rev["z"].abs() > 2.5
    daily_rev["direction"] = np.where(daily_rev["z"] > 0, "spike", "drop")

    anomalies = daily_rev[daily_rev["anomaly"]].copy()

    col_e, col_f = st.columns([3,1])
    with col_e:
        fig10 = go.Figure()
        fig10.add_trace(go.Scatter(x=daily_rev["date"], y=daily_rev["revenue"],
                                   name="Revenue", line=dict(color="#1a3a5a", width=1.5), mode="lines"))
        fig10.add_trace(go.Scatter(x=daily_rev["date"], y=daily_rev["ma7"],
                                   name="7D MA", line=dict(color="#00d4ff", width=2), mode="lines"))
        spikes = anomalies[anomalies["direction"]=="spike"]
        drops  = anomalies[anomalies["direction"]=="drop"]
        fig10.add_trace(go.Scatter(x=spikes["date"], y=spikes["revenue"],
                                   mode="markers", name="Spike",
                                   marker=dict(color="#00e5a0", size=10, symbol="triangle-up")))
        fig10.add_trace(go.Scatter(x=drops["date"], y=drops["revenue"],
                                   mode="markers", name="Drop",
                                   marker=dict(color="#ff4757", size=10, symbol="triangle-down")))
        fig10.update_layout(**PLOTLY_THEME, height=300, showlegend=True,
                            legend=dict(orientation="h", y=1.1, font=dict(size=10)))
        st.plotly_chart(fig10, use_container_width=True)

    with col_f:
        st.metric("Anomalies Detected", len(anomalies))
        st.metric("Spikes", len(spikes))
        st.metric("Drops",  len(drops))
        if len(anomalies):
            worst = anomalies.loc[anomalies["z"].abs().idxmax()]
            st.markdown(f'<div class="anomaly-badge">WORST: {worst["date"].strftime("%b %d")}</div>', unsafe_allow_html=True)

    if len(anomalies) > 0:
        st.markdown('<div class="section-label" style="margin-top:16px">Anomaly Log</div>', unsafe_allow_html=True)
        anom_display = anomalies[["date","revenue","z","direction"]].copy()
        anom_display["date"]      = anom_display["date"].dt.strftime("%Y-%m-%d")
        anom_display["revenue"]   = anom_display["revenue"].apply(lambda x: f"${x:,.0f}")
        anom_display["z"]         = anom_display["z"].apply(lambda x: f"{x:+.2f}")
        anom_display["direction"] = anom_display["direction"].str.upper()
        anom_display.columns      = ["Date","Revenue","Z-Score","Type"]
        st.dataframe(anom_display.sort_values("Z-Score", key=lambda x: x.str.replace("+","").astype(float).abs(), ascending=False),
                     use_container_width=True, hide_index=True, height=220)

    # Anomalia por categoria
    st.markdown('<div class="section-label" style="margin-top:8px">Category Anomaly Heatmap</div>', unsafe_allow_html=True)
    cat_monthly2 = df.copy()
    cat_monthly2["month"] = cat_monthly2["date"].dt.to_period("M").astype(str)
    heatmap_data = cat_monthly2.groupby(["month","category"])["revenue"].sum().unstack(fill_value=0)
    heatmap_pct  = heatmap_data.pct_change() * 100

    fig11 = px.imshow(heatmap_pct.T, color_continuous_scale=["#ff4757","#0e1420","#00e5a0"],
                      zmin=-60, zmax=60, aspect="auto",
                      labels=dict(color="MoM %"))
    fig11.update_layout(**PLOTLY_THEME, height=250, coloraxis_showscale=True)
    st.plotly_chart(fig11, use_container_width=True)

# ── TAB 5: AI ASSISTANT ───────────────────────────────
with tab5:
    st.markdown('<div class="section-label">Natural Language Data Analysis — Powered by Claude</div>', unsafe_allow_html=True)

    # Preparar contexto de dados para a IA
    @st.cache_data
    def build_context(df_hash):
        rev   = df["revenue"].sum()
        mgn   = df["gross_margin"].sum()
        top5  = df.groupby("product_name")["revenue"].sum().nlargest(5).to_dict()
        cat   = df.groupby("category")["revenue"].sum().sort_values(ascending=False).to_dict()
        ch    = df.groupby("channel")["revenue"].sum().sort_values(ascending=False).to_dict()
        ret   = df["returned"].mean() * 100
        aov_v = df["revenue"].sum() / len(df)
        discount_impact = df.groupby(df["discount_pct"]>0)["gross_margin"].mean().to_dict()

        return f"""
You are a senior e-commerce data analyst. Analyze this store's data and answer questions clearly and concisely.

CURRENT PERIOD DATA ({d_start} to {d_end}):
- Total Revenue: ${rev:,.0f}
- Gross Margin: ${mgn:,.0f} ({mgn/rev*100:.1f}% margin rate)
- Total Transactions: {len(df):,}
- Avg Order Value: ${aov_v:.2f}
- Return Rate: {ret:.1f}%

TOP 5 PRODUCTS BY REVENUE:
{json.dumps({k: f'${v:,.0f}' for k,v in top5.items()}, indent=2)}

REVENUE BY CATEGORY:
{json.dumps({k: f'${v:,.0f}' for k,v in cat.items()}, indent=2)}

REVENUE BY CHANNEL:
{json.dumps({k: f'${v:,.0f}' for k,v in ch.items()}, indent=2)}

DISCOUNT ANALYSIS:
- Avg margin without discounts: ${discount_impact.get(False, 0):,.0f} per transaction
- Avg margin with discounts: ${discount_impact.get(True, 0):,.0f} per transaction

Always respond with specific numbers from the data. Be direct and actionable. 
Format key numbers in bold. Keep responses under 200 words unless asked for detail.
End with one concrete recommendation when relevant.
"""
    context = build_context(len(df))

    def ask_claude(question: str, context: str, key: str) -> str:
        if not key or not key.startswith("sk-ant-"):
            # Modo demo sem API key
            demos = {
                "default": f"""Based on the current data:

**Revenue** is ${df['revenue'].sum()/1e6:.2f}M with a **{df['gross_margin'].sum()/df['revenue'].sum()*100:.1f}% gross margin**.

Top performing category is **{df.groupby('category')['revenue'].sum().idxmax()}** at ${df.groupby('category')['revenue'].sum().max()/1e6:.1f}M.

**Biggest opportunity**: {df.groupby('channel')['revenue'].sum().idxmin()} channel is underperforming — only ${df.groupby('channel')['revenue'].sum().min()/1e3:.0f}K revenue vs ${df.groupby('channel')['revenue'].sum().max()/1e6:.1f}M from top channel.

→ **Recommendation**: Shift 10-15% of paid ad budget toward your top channel to improve blended ROAS by an estimated 18-25%.

*Add your Anthropic API key in the sidebar for full AI analysis.*"""
            }
            return demos["default"]

        try:
            resp = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={"x-api-key": key, "anthropic-version": "2023-06-01",
                         "content-type": "application/json"},
                json={"model": "claude-haiku-4-5-20251001", "max_tokens": 400,
                      "system": context,
                      "messages": [{"role": "user", "content": question}]},
                timeout=30
            )
            data = resp.json()
            if "content" in data and data["content"]:
                return data["content"][0]["text"]
            return f"API Error: {data.get('error', {}).get('message', str(data))}"
        except Exception as e:
            return f"Connection error: {e}"

    # Chat UI
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Suggested questions
    st.markdown("**Quick questions:**")
    q_cols = st.columns(3)
    suggestions = [
        "Which products have declining margins?",
        "What's driving the revenue anomalies?",
        "Which channel has the best ROI?",
        "Where are the biggest discount losses?",
        "Which category should I prioritize?",
        "What's the return rate by category?",
    ]
    for i, (col, q) in enumerate(zip(q_cols * 2, suggestions)):
        with q_cols[i % 3]:
            if st.button(q, key=f"sugg_{i}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": q})
                with st.spinner("Analyzing..."):
                    ans = ask_claude(q, context, api_key)
                st.session_state.messages.append({"role": "assistant", "content": ans})

    # Chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-msg-user">💬 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-msg-ai">◈ {msg["content"]}</div>', unsafe_allow_html=True)

    # Input
    with st.form("chat_form", clear_on_submit=True):
        col_inp, col_btn = st.columns([5,1])
        with col_inp:
            user_q = st.text_input("", placeholder="Ask anything about your store data...", label_visibility="collapsed")
        with col_btn:
            send = st.form_submit_button("Send", use_container_width=True)

        if send and user_q.strip():
            st.session_state.messages.append({"role": "user", "content": user_q})
            with st.spinner("Analyzing your data..."):
                answer = ask_claude(user_q, context, api_key)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()

    if st.session_state.messages:
        if st.button("Clear conversation", key="clear_chat"):
            st.session_state.messages = []
            st.rerun()
