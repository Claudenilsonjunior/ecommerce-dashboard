"""
DataLens — E-Commerce Intelligence Dashboard
Demo dashboard para portfólio — Claudenilson Junior
Design: editorial premium, âmbar sobre preto
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date, timedelta
import os

st.set_page_config(
    page_title="DataLens · E-Commerce Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── DESIGN SYSTEM ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Lora:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg:        #07080c;
  --surface:   #0c0e14;
  --surface2:  #11131a;
  --border:    #1c1f2b;
  --amber:     #f5a623;
  --amber-dim: rgba(245,166,35,0.12);
  --amber-glow:rgba(245,166,35,0.06);
  --green:     #2dd4a0;
  --red:       #f05252;
  --blue:      #4da6ff;
  --text:      #dde2ec;
  --muted:     #4a5268;
  --muted2:    #2a2f40;
  --font-display: 'Bebas Neue', sans-serif;
  --font-serif:   'Lora', serif;
  --font-mono:    'JetBrains Mono', monospace;
}

/* ───────────────── BASE ───────────────── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: var(--bg) !important;
    color: var(--text) !important;
}

/* remove faixa preta do topo sem quebrar sidebar */
header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0rem !important;
}

/* esconde menu padrão */
#MainMenu, footer {
    visibility: hidden;
}

/* container principal */
.block-container {
    padding: 1.5rem 2.5rem 2rem 2.5rem !important;
    max-width: 1440px !important;
}

/* ───────────────── SIDEBAR ───────────────── */

/* sidebar principal */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

/* conteúdo interno */
[data-testid="stSidebarContent"] {
    background: var(--surface) !important;
    padding-top: 1rem !important;
}

/* botão recolher/abrir */
button[kind="header"],
[data-testid="collapsedControl"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--amber) !important;
    box-shadow: none !important;
    top: 0.75rem !important;
    left: 0.75rem !important;
    opacity: 0.9 !important;
}

button[kind="header"]:hover,
[data-testid="collapsedControl"]:hover {
    border-color: var(--amber) !important;
    opacity: 1 !important;
}

/* evita botão escondido atrás header */
[data-testid="collapsedControl"] {
    z-index: 99999 !important;
}

/* largura sidebar */
section[data-testid="stSidebar"] {
    min-width: 320px !important;
    max-width: 320px !important;
}

/* ───────────────── METRICS ───────────────── */
[data-testid="metric-container"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-top: 2px solid var(--amber) !important;
    border-radius: 4px 4px 8px 8px !important;
    padding: 1.2rem 1.4rem !important;
}

[data-testid="metric-container"]:hover {
    background: var(--amber-glow) !important;
}

[data-testid="stMetricLabel"] {
    font-family: var(--font-mono) !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}

[data-testid="stMetricValue"] {
    font-family: var(--font-display) !important;
    font-size: 32px !important;
    color: var(--text) !important;
}

/* ───────────────── INPUTS ───────────────── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stDateInput"] input,
.stTextInput input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
}

/* ───────────────── TABS ───────────────── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    border-bottom: 1px solid var(--border) !important;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}

[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--amber) !important;
    border-bottom: 2px solid var(--amber) !important;
}

/* scrollbar sidebar */
section[data-testid="stSidebar"] ::-webkit-scrollbar {
    width: 6px;
}
section[data-testid="stSidebar"] ::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────
@st.cache_data
def load_data():
    base  = os.path.dirname(os.path.abspath(__file__))
    sales = pd.read_csv(f"{base}/data/sales.csv", parse_dates=["date"])
    prods = pd.read_csv(f"{base}/data/products.csv")
    df    = sales.merge(
        prods[["product_id","product_name","rating","review_count","supplier"]],
        on="product_id", how="left"
    )
    return df, prods

df_all, df_products = load_data()

# ── SIDEBAR ───────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="logo-mark">◈ DATA<span style="color:var(--amber)">LENS</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="logo-sub" style="margin-bottom:24px">E-Commerce Intelligence</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-label">Date Range</div>', unsafe_allow_html=True)
    min_d = df_all["date"].min().date()
    max_d = df_all["date"].max().date()
    d_start = st.date_input("From", value=date(2024, 1, 1), min_value=min_d, max_value=max_d, label_visibility="collapsed")
    d_end   = st.date_input("To",   value=max_d,            min_value=min_d, max_value=max_d, label_visibility="collapsed")
    st.markdown(f'<div style="font-family:var(--font-mono);font-size:10px;color:var(--muted);margin-top:4px">{d_start} → {d_end}</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-label" style="margin-top:20px">Segment</div>', unsafe_allow_html=True)
    cats  = ["All Categories"] + sorted(df_all["category"].unique().tolist())
    chs   = ["All Channels"]   + sorted(df_all["channel"].unique().tolist())
    cos   = ["All Countries"]  + sorted(df_all["country"].unique().tolist())
    sel_cat = st.selectbox("Category", cats, label_visibility="collapsed")
    sel_ch  = st.selectbox("Channel",  chs,  label_visibility="collapsed")
    sel_co  = st.selectbox("Country",  cos,  label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f"""
    <div style="font-family:var(--font-mono);font-size:10px;color:var(--muted);line-height:1.8">
    BUILT BY<br>
    <span style="color:var(--amber);font-size:12px">Claudenilson Junior</span><br>
    Data Analyst<br>
    Python · SQL · Power BI<br><br>
    <span style="color:var(--muted2)">github.com/Claudenilsonjunior</span>
    </div>
    """, unsafe_allow_html=True)

# ── FILTER ────────────────────────────────────────────
mask = (df_all["date"].dt.date >= d_start) & (df_all["date"].dt.date <= d_end)
if sel_cat != "All Categories": mask &= df_all["category"] == sel_cat
if sel_ch  != "All Channels":   mask &= df_all["channel"]  == sel_ch
if sel_co  != "All Countries":  mask &= df_all["country"]  == sel_co
df = df_all[mask].copy()

# Período anterior
n_days    = max((d_end - d_start).days, 1)
prev_end  = d_start - timedelta(days=1)
prev_st   = prev_end - timedelta(days=n_days)
mask_p    = (df_all["date"].dt.date >= prev_st) & (df_all["date"].dt.date <= prev_end)
df_p      = df_all[mask_p]

def pct(a, b): return round((a - b) / b * 100, 1) if b else 0
def fmt_delta(v): return f"+{v}%" if v >= 0 else f"{v}%"

# KPIs
rev   = df["revenue"].sum();       rev_p  = df_p["revenue"].sum()
mgn   = df["gross_margin"].sum();  mgn_p  = df_p["gross_margin"].sum()
orders= len(df);                   ord_p  = len(df_p)
aov   = rev / orders if orders else 0
aov_p = rev_p / ord_p if ord_p else 0
mgn_r = mgn / rev * 100 if rev else 0
ret   = df["returned"].mean() * 100 if len(df) else 0

# ── THEME FOR PLOTLY ──────────────────────────────────
T = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="JetBrains Mono, monospace", color="#4a5268", size=10),
    margin=dict(l=0, r=0, t=28, b=0),
)
def ax(show_grid=True):
    return dict(gridcolor="#1c1f2b" if show_grid else "rgba(0,0,0,0)",
                linecolor="#1c1f2b", tickcolor="#1c1f2b", zeroline=False)

AMBER = "#f5a623"
GREEN = "#2dd4a0"
RED   = "#f05252"
BLUE  = "#4da6ff"
SEQ   = [AMBER, GREEN, BLUE, "#c084fc", RED, "#fb923c"]

# ── PAGE HEADER ───────────────────────────────────────
st.markdown(f"""
<div class="page-header">
  <div class="section-eyebrow">Sales Intelligence</div>
  <div class="section-title">PERFORMANCE OVERVIEW</div>
  <div style="font-family:var(--font-mono);font-size:11px;color:var(--muted);margin-top:4px">
    {d_start.strftime("%b %d, %Y")} — {d_end.strftime("%b %d, %Y")}
    &nbsp;·&nbsp; {orders:,} transactions
    &nbsp;·&nbsp; {df["product_id"].nunique()} products
    &nbsp;·&nbsp; {df["country"].nunique()} markets
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI ROW ───────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Revenue",      f"${rev/1e6:.2f}M",  fmt_delta(pct(rev, rev_p)))
k2.metric("Gross Margin", f"${mgn/1e6:.2f}M",  fmt_delta(pct(mgn, mgn_p)))
k3.metric("Margin Rate",  f"{mgn_r:.1f}%",      fmt_delta(round(mgn_r - (mgn_p/rev_p*100 if rev_p else 0), 1)))
k4.metric("Avg Order",    f"${aov:.0f}",        fmt_delta(pct(aov, aov_p)))
k5.metric("Return Rate",  f"{ret:.1f}%",         None)

st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "  REVENUE  ", "  PRODUCTS  ", "  CHANNELS & GEO  ", "  INSIGHTS  "
])

# ════════════════════════════════════════════════════
# TAB 1 — REVENUE
# ════════════════════════════════════════════════════
with tab1:
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    col_big, col_sm = st.columns([3, 1])

    with col_big:
        st.markdown('<div class="chart-label">Daily Revenue with 7-Day Moving Average</div>', unsafe_allow_html=True)
        daily = df.groupby("date").agg(revenue=("revenue","sum")).reset_index()
        daily["ma7"] = daily["revenue"].rolling(7).mean()
        daily["ma30"] = daily["revenue"].rolling(30).mean()

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=daily["date"], y=daily["revenue"], name="Daily",
            marker=dict(color=AMBER, opacity=0.18, line_width=0),
        ))
        fig.add_trace(go.Scatter(
            x=daily["date"], y=daily["ma7"], name="7D MA",
            line=dict(color=AMBER, width=2), mode="lines",
        ))
        fig.add_trace(go.Scatter(
            x=daily["date"], y=daily["ma30"], name="30D MA",
            line=dict(color=GREEN, width=1.5, dash="dot"), mode="lines",
        ))
        fig.update_layout(**T, height=280, showlegend=True,
            legend=dict(orientation="h", y=1.08, x=0, font=dict(size=10)),
            xaxis=ax(), yaxis=dict(**ax(), tickprefix="$", tickformat=",.0f"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_sm:
        st.markdown('<div class="chart-label">By Category</div>', unsafe_allow_html=True)
        cat_r = df.groupby("category")["revenue"].sum().sort_values()
        fig2 = go.Figure(go.Bar(
            x=cat_r.values, y=cat_r.index, orientation="h",
            marker=dict(
                color=list(range(len(cat_r))),
                colorscale=[[0,"#1c1f2b"],[0.6,"#7a4a00"],[1, AMBER]],
                showscale=False,
            ),
            text=[f"${v/1e6:.1f}M" for v in cat_r.values],
            textposition="outside",
            textfont=dict(size=9, color="#4a5268"),
        ))
        fig2.update_layout(**T, height=280)
        fig2.update_xaxes(visible=False, **ax(False))
        fig2.update_yaxes(**ax(False))
        st.plotly_chart(fig2, use_container_width=True)

    # Monthly revenue + margin
    st.markdown('<div class="chart-label" style="margin-top:8px">Monthly Revenue & Gross Margin %</div>', unsafe_allow_html=True)
    monthly = df.copy()
    monthly["month"] = monthly["date"].dt.to_period("M").astype(str)
    m_agg = monthly.groupby("month").agg(rev=("revenue","sum"), mgn=("gross_margin","sum")).reset_index()
    m_agg["mgn_pct"] = m_agg["mgn"] / m_agg["rev"] * 100

    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3.add_trace(go.Bar(x=m_agg["month"], y=m_agg["rev"], name="Revenue",
                          marker=dict(color=AMBER, opacity=0.3, line_width=0)), secondary_y=False)
    fig3.add_trace(go.Scatter(x=m_agg["month"], y=m_agg["mgn_pct"], name="Margin %",
                              line=dict(color=GREEN, width=2.5), mode="lines+markers",
                              marker=dict(size=4, color=GREEN)), secondary_y=True)
    fig3.update_layout(**T, height=220, showlegend=True,
                       legend=dict(orientation="h", y=1.12, font=dict(size=10)))
    fig3.update_xaxes(**ax())
    fig3.update_yaxes(tickprefix="$", tickformat=",.0f", gridcolor="#1c1f2b",
                      linecolor="#1c1f2b", zeroline=False, secondary_y=False)
    fig3.update_yaxes(ticksuffix="%", gridcolor="rgba(0,0,0,0)",
                      linecolor="rgba(0,0,0,0)", zeroline=False, secondary_y=True)
    st.plotly_chart(fig3, use_container_width=True)

# ════════════════════════════════════════════════════
# TAB 2 — PRODUCTS
# ════════════════════════════════════════════════════
with tab2:
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    col_p1, col_p2 = st.columns(2)

    prod_agg = df.groupby(["product_id","product_name","category"]).agg(
        revenue=("revenue","sum"),
        units=("units_sold","sum"),
        margin=("gross_margin","sum"),
        avg_price=("unit_price","mean"),
        avg_discount=("discount_pct","mean"),
    ).reset_index()
    prod_agg["margin_pct"] = (prod_agg["margin"] / prod_agg["revenue"] * 100).round(1)
    prod_agg = prod_agg[prod_agg["revenue"] > 0]

    with col_p1:
        st.markdown('<div class="chart-label">Top 15 Products — Revenue × Margin</div>', unsafe_allow_html=True)
        top15 = prod_agg.nlargest(15, "revenue")
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=top15["revenue"], y=top15["product_name"], orientation="h",
            marker=dict(color=top15["margin_pct"],
                        colorscale=[[0, RED],[0.5,"#7a4a00"],[1, AMBER]],
                        showscale=True,
                        colorbar=dict(title=dict(text="Margin%", font=dict(size=9, color="#4a5268")),
                                      tickfont=dict(size=8, color="#4a5268"),
                                      len=0.6, thickness=8)),
        ))
        fig4.update_layout(**T, height=380)
        fig4.update_xaxes(tickprefix="$", tickformat=",.0f", **ax())
        fig4.update_yaxes(**ax(False), tickfont=dict(size=9))
        st.plotly_chart(fig4, use_container_width=True)

    with col_p2:
        st.markdown('<div class="chart-label">Price vs Margin Rate — Size = Units Sold</div>', unsafe_allow_html=True)
        fig5 = px.scatter(
            prod_agg, x="avg_price", y="margin_pct",
            size="units", color="category", hover_name="product_name",
            size_max=35, opacity=0.75,
            color_discrete_sequence=SEQ,
        )
        fig5.update_layout(**T, height=380,
                           legend=dict(orientation="h", y=-0.18, font=dict(size=9)))
        fig5.update_xaxes(tickprefix="$", **ax())
        fig5.update_yaxes(ticksuffix="%", **ax())
        st.plotly_chart(fig5, use_container_width=True)

    # Discount impact
    st.markdown('<div class="chart-label" style="margin-top:8px">Discount Depth vs Margin Erosion</div>', unsafe_allow_html=True)
    df["disc_band"] = pd.cut(df["discount_pct"],
                              bins=[-1, 0, 5, 15, 25, 100],
                              labels=["No Discount","1–5%","6–15%","16–25%","25%+"])
    disc_agg = df.groupby("disc_band", observed=True).agg(
        revenue=("revenue","sum"), margin=("gross_margin","sum"), txns=("revenue","count")
    ).reset_index()
    disc_agg["margin_pct"] = (disc_agg["margin"] / disc_agg["revenue"] * 100).round(1)

    fig6 = make_subplots(specs=[[{"secondary_y": True}]])
    fig6.add_trace(go.Bar(
        x=disc_agg["disc_band"].astype(str), y=disc_agg["revenue"],
        name="Revenue", marker=dict(color=AMBER, opacity=0.35, line_width=0)
    ), secondary_y=False)
    fig6.add_trace(go.Scatter(
        x=disc_agg["disc_band"].astype(str), y=disc_agg["margin_pct"],
        name="Margin %", line=dict(color=RED, width=2.5),
        mode="lines+markers", marker=dict(size=6, color=RED)
    ), secondary_y=True)
    fig6.update_layout(**T, height=220, showlegend=True,
                       legend=dict(orientation="h", y=1.12, font=dict(size=10)))
    fig6.update_xaxes(**ax())
    fig6.update_yaxes(tickprefix="$", tickformat=",.0f",
                      gridcolor="#1c1f2b", linecolor="#1c1f2b", zeroline=False, secondary_y=False)
    fig6.update_yaxes(ticksuffix="%",
                      gridcolor="rgba(0,0,0,0)", linecolor="rgba(0,0,0,0)", zeroline=False, secondary_y=True)
    st.plotly_chart(fig6, use_container_width=True)

# ════════════════════════════════════════════════════
# TAB 3 — CHANNELS & GEO
# ════════════════════════════════════════════════════
with tab3:
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    col_c1, col_c2 = st.columns(2)

    ch_agg = df.groupby("channel").agg(
        revenue=("revenue","sum"),
        margin=("gross_margin","sum"),
        orders=("revenue","count"),
    ).reset_index()
    ch_agg["aov"]       = ch_agg["revenue"] / ch_agg["orders"]
    ch_agg["margin_pct"]= (ch_agg["margin"] / ch_agg["revenue"] * 100).round(1)

    with col_c1:
        st.markdown('<div class="chart-label">Revenue Share by Channel</div>', unsafe_allow_html=True)
        fig7 = go.Figure(go.Pie(
            labels=ch_agg["channel"], values=ch_agg["revenue"],
            hole=0.65, direction="clockwise",
            marker=dict(colors=SEQ, line=dict(color="#07080c", width=3)),
            textfont=dict(size=10, family="JetBrains Mono"),
            hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>",
        ))
        total_rev = ch_agg["revenue"].sum()
        fig7.add_annotation(
            text=f"${total_rev/1e6:.1f}M<br><span style='font-size:10px'>TOTAL</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(family="Bebas Neue", size=22, color="#dde2ec"),
        )
        fig7.update_layout(**T, height=300,
                           legend=dict(orientation="h", y=-0.12, font=dict(size=10)))
        st.plotly_chart(fig7, use_container_width=True)

    with col_c2:
        st.markdown('<div class="chart-label">Channel Performance — AOV vs Margin</div>', unsafe_allow_html=True)
        fig8 = go.Figure()
        for i, row in ch_agg.iterrows():
            fig8.add_trace(go.Bar(
                x=[row["channel"]], y=[row["margin_pct"]],
                name=row["channel"],
                marker_color=SEQ[i % len(SEQ)],
                text=[f"{row['margin_pct']:.1f}%"],
                textposition="outside",
                textfont=dict(size=9),
                showlegend=False,
            ))
        fig8.update_layout(**T, height=300, showlegend=False)
        fig8.update_xaxes(**ax(False))
        fig8.update_yaxes(ticksuffix="%", **ax())
        st.plotly_chart(fig8, use_container_width=True)

    # Channel trend over time
    st.markdown('<div class="chart-label" style="margin-top:8px">Channel Revenue Trend — Monthly</div>', unsafe_allow_html=True)
    ch_m = df.copy()
    ch_m["month"] = ch_m["date"].dt.to_period("M").astype(str)
    ch_trend = ch_m.groupby(["month","channel"])["revenue"].sum().reset_index()
    fig9 = px.line(ch_trend, x="month", y="revenue", color="channel",
                   color_discrete_sequence=SEQ, line_shape="spline")
    fig9.update_traces(line=dict(width=2))
    fig9.update_layout(**T, height=220,
                       legend=dict(orientation="h", y=1.12, font=dict(size=10)),
                       xaxis=ax(), yaxis=dict(**ax(), tickprefix="$", tickformat=",.0f"))
    st.plotly_chart(fig9, use_container_width=True)

    # Country map
    st.markdown('<div class="chart-label" style="margin-top:8px">Revenue by Market</div>', unsafe_allow_html=True)
    geo = df.groupby("country")["revenue"].sum().reset_index()
    fig10 = px.choropleth(
        geo, locations="country", locationmode="country names",
        color="revenue",
        color_continuous_scale=[[0,"#1c1f2b"],[0.5,"#7a4a00"],[1, AMBER]],
        hover_name="country",
        hover_data={"revenue": ":$,.0f"},
    )
    fig10.update_layout(
        **T, height=300,
        geo=dict(bgcolor="rgba(0,0,0,0)", showframe=False,
                 showcoastlines=True, coastlinecolor="#2a2f40",
                 landcolor="#11131a", showocean=True, oceancolor="#07080c",
                 showlakes=False),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig10, use_container_width=True)

# ════════════════════════════════════════════════════
# TAB 4 — INSIGHTS (análise automática, sem IA)
# ════════════════════════════════════════════════════
with tab4:
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Gerar insights automaticamente com Python puro
    insights = []

    if len(df) > 0 and rev > 0:

        # 1. Melhor categoria
        best_cat     = df.groupby("category")["revenue"].sum().idxmax()
        best_cat_rev = df.groupby("category")["revenue"].sum().max()
        best_cat_pct = best_cat_rev / rev * 100
        insights.append(("REVENUE CONCENTRATION", f"<strong>{best_cat}</strong> accounts for <strong>{best_cat_pct:.1f}%</strong> of total revenue (${best_cat_rev/1e6:.2f}M). This level of category dependency {'warrants diversification' if best_cat_pct > 40 else 'is within healthy range'} — consider whether this reflects market demand or underinvestment in other categories."))

        # 2. Canal mais eficiente por margem
        ch_mgn = df.groupby("channel").apply(lambda x: x["gross_margin"].sum() / x["revenue"].sum() * 100 if x["revenue"].sum() > 0 else 0)
        best_ch = ch_mgn.idxmax(); best_ch_pct = ch_mgn.max()
        worst_ch = ch_mgn.idxmin(); worst_ch_pct = ch_mgn.min()
        insights.append(("CHANNEL EFFICIENCY", f"<strong>{best_ch}</strong> delivers the highest margin rate at <strong>{best_ch_pct:.1f}%</strong>, while <strong>{worst_ch}</strong> lags at <strong>{worst_ch_pct:.1f}%</strong>. A shift of 15% budget from {worst_ch} to {best_ch} could improve blended margin by an estimated {((best_ch_pct - worst_ch_pct) * 0.15):.1f} percentage points."))

        # 3. Impacto do desconto
        no_disc_mgn = df[df["discount_pct"] == 0]["gross_margin"].sum() / df[df["discount_pct"] == 0]["revenue"].sum() * 100 if (df["discount_pct"] == 0).any() else 0
        disc_mgn    = df[df["discount_pct"] >  0]["gross_margin"].sum() / df[df["discount_pct"] >  0]["revenue"].sum() * 100 if (df["discount_pct"] >  0).any() else 0
        disc_pct_txn = (df["discount_pct"] > 0).mean() * 100
        insights.append(("DISCOUNT IMPACT", f"<strong>{disc_pct_txn:.1f}%</strong> of transactions include a discount. Discounted orders carry a <strong>{no_disc_mgn - disc_mgn:.1f}pp lower margin</strong> ({disc_mgn:.1f}% vs {no_disc_mgn:.1f}% for full-price). {'Discount strategy is eroding margin significantly — review threshold rules.' if no_disc_mgn - disc_mgn > 8 else 'Discount impact is controlled — current strategy is sustainable.'}"))

        # 4. Anomalia de receita (detecção automática)
        daily_r = df.groupby("date")["revenue"].sum()
        if len(daily_r) > 14:
            z = (daily_r - daily_r.rolling(7, center=True).mean()) / (daily_r.rolling(7, center=True).std() + 1)
            spikes = (z > 2.5).sum(); drops = (z < -2.5).sum()
            worst_drop_date = z[z < -2.5].idxmin() if drops > 0 else None
            if spikes + drops > 0:
                drop_str = f" Most significant drop: <strong>{worst_drop_date.strftime('%b %d, %Y') if worst_drop_date else 'N/A'}</strong>." if drops > 0 else ""
                insights.append(("ANOMALY DETECTION", f"Automated Z-score analysis identified <strong>{spikes} revenue spikes</strong> and <strong>{drops} significant drops</strong> in the selected period.{drop_str} Spikes typically correlate with promotions or viral moments — drops may indicate supply, ops or competitive issues worth investigating."))

        # 5. Produto com melhor ROI escondido
        hidden = prod_agg[(prod_agg["margin_pct"] > prod_agg["margin_pct"].quantile(0.75)) &
                          (prod_agg["revenue"]    < prod_agg["revenue"].quantile(0.4))].copy()
        if len(hidden) > 0:
            best_hidden = hidden.nlargest(1, "margin_pct").iloc[0]
            insights.append(("HIDDEN OPPORTUNITY", f"<strong>{best_hidden['product_name']}</strong> ({best_hidden['category']}) shows a <strong>{best_hidden['margin_pct']:.1f}% margin rate</strong> but ranks in the bottom 40% of revenue — a classic undermarketed high-margin SKU. Increasing visibility for this product through paid placement or email feature could yield disproportionate margin gains."))

        # 6. Tendência de crescimento
        if len(df) > 60:
            df_trend = df.copy()
            df_trend["week"] = df_trend["date"].dt.to_period("W").astype(str)
            weekly = df_trend.groupby("week")["revenue"].sum().reset_index()
            if len(weekly) >= 8:
                first4 = weekly["revenue"].head(4).mean()
                last4  = weekly["revenue"].tail(4).mean()
                trend_pct = pct(last4, first4)
                direction = "accelerating" if trend_pct > 10 else ("declining" if trend_pct < -5 else "stable")
                insights.append(("GROWTH TREND", f"Weekly revenue is <strong>{direction}</strong> in the selected period: last 4 weeks average <strong>${last4:,.0f}/week</strong> vs <strong>${first4:,.0f}/week</strong> in the first 4 weeks — a <strong>{fmt_delta(trend_pct)}</strong> change. {'Momentum is strong — consider scaling acquisition spend.' if trend_pct > 10 else 'Monitor closely for continued softness.' if trend_pct < -5 else 'Growth is steady — focus on margin improvement.'}"))

    # Renderizar insights
    if insights:
        col_i1, col_i2 = st.columns(2)
        for i, (itype, itext) in enumerate(insights):
            col = col_i1 if i % 2 == 0 else col_i2
            with col:
                st.markdown(f"""
                <div class="insight-card">
                    <div class="insight-type">{itype}</div>
                    <div class="insight-text">{itext}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No data available for the selected filters.")

    # Anomalia heatmap
    st.markdown('<div class="chart-label" style="margin-top:24px">Category Revenue — Month-over-Month Change (%)</div>', unsafe_allow_html=True)
    hm = df.copy()
    hm["month"] = hm["date"].dt.to_period("M").astype(str)
    hm_pivot = hm.groupby(["month","category"])["revenue"].sum().unstack(fill_value=0)
    hm_pct   = hm_pivot.pct_change().iloc[1:] * 100

    fig_hm = px.imshow(
        hm_pct.T,
        color_continuous_scale=[[0, RED],[0.5,"#1c1f2b"],[1, AMBER]],
        zmin=-50, zmax=50, aspect="auto",
        labels=dict(color="MoM %"),
        text_auto=".0f",
    )
    fig_hm.update_traces(textfont=dict(size=8, color="rgba(255,255,255,0.5)"))
    fig_hm.update_layout(**T, height=260, coloraxis_showscale=True,
                         xaxis=ax(), yaxis=ax(False))
    st.plotly_chart(fig_hm, use_container_width=True)
