"""
FinIntel Multi-Agent Autonomous Financial Intelligence System
PS-01 Hackverse 2026 Interactive Financial Intelligence Dashboard (Frontend UI)
"""

import sys
import os
from pathlib import Path

# Ensure backend modules can be imported
backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import time

from core.market_feed import MarketFeed
from core.rag_engine import RAGEngine
from core.user_profile import get_preset_profiles, UserProfile, Holding
from core.metrics_logger import MetricsLogger
from agents.technical_agent import TechnicalAnalystAgent
from agents.fundamental_agent import FundamentalRAGAgent
from agents.sentiment_agent import SentimentMicrostructureAgent
from agents.synthesis_orchestrator import MultiAgentSynthesisOrchestrator

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="FinIntel | Autonomous Multi-Agent Financial Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- CUSTOM CSS FOR POLISHED FINTECH UI -----------------
st.markdown("""
<style>
    /* Dark Fintech theme styling */
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    .metric-card {
        background: linear-gradient(135deg, #131d31 0%, #1a2744 100%);
        border-radius: 12px;
        padding: 18px;
        border: 1px solid #2a3b61;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        margin-bottom: 12px;
    }
    .agent-card {
        background: #111827;
        border-radius: 10px;
        padding: 16px;
        border: 1px solid #1f2937;
        margin-bottom: 15px;
        border-left: 4px solid #3b82f6;
    }
    .action-badge-bull {
        background-color: #065f46;
        color: #34d399;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 1.1rem;
        display: inline-block;
    }
    .action-badge-bear {
        background-color: #7f1d1d;
        color: #f87171;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 1.1rem;
        display: inline-block;
    }
    .action-badge-neutral {
        background-color: #854d0e;
        color: #fde047;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 1.1rem;
        display: inline-block;
    }
    .citation-box {
        background-color: #1e293b;
        border-left: 3px solid #6366f1;
        padding: 10px 14px;
        border-radius: 6px;
        font-size: 0.88rem;
        margin: 6px 0;
        color: #cbd5e1;
    }
    .waterfall-step {
        background-color: #0f172a;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- CACHED SYSTEM INITIALIZATION -----------------
@st.cache_resource
def init_system():
    market_feed = MarketFeed()
    rag_engine = RAGEngine()
    tech_agent = TechnicalAnalystAgent(market_feed)
    fund_agent = FundamentalRAGAgent(rag_engine, market_feed)
    sent_agent = SentimentMicrostructureAgent(market_feed)
    logger = MetricsLogger()
    orchestrator = MultiAgentSynthesisOrchestrator(tech_agent, fund_agent, sent_agent, logger)
    profiles = get_preset_profiles()
    return market_feed, rag_engine, orchestrator, logger, profiles

market_feed, rag_engine, orchestrator, logger, preset_profiles = init_system()

# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.markdown("## 🛡️ FinIntel Control Center")
st.sidebar.caption("Autonomous Multi-Agent Retail Decision Engine")

# 1. Ticker Selector
tickers = market_feed.get_supported_tickers()
selected_ticker = st.sidebar.selectbox(
    "📊 Select Listed Equity (NSE)",
    options=tickers,
    index=0,
    help="Select an Indian equity to trigger multi-agent analysis."
)

# 2. User Persona Selector
st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 Retail Investor Profile")
persona_keys = list(preset_profiles.keys())
selected_persona_key = st.sidebar.selectbox(
    "Active User Persona",
    options=persona_keys,
    format_func=lambda x: preset_profiles[x].name,
    index=0
)
active_profile = preset_profiles[selected_persona_key]

with st.sidebar.expander("🔍 View Profile Risk Parameters"):
    st.write(f"**Risk Category:** `{active_profile.risk_category}`")
    st.write(f"**Investment Horizon:** {active_profile.investment_horizon}")
    st.write(f"**Max Drawdown Tolerance:** {active_profile.max_drawdown_tolerance_pct}%")
    st.write(f"**Cash Balance:** ₹{active_profile.cash_balance:,.2f}")
    st.write(f"**Agent Weights:** Tech: {active_profile.weight_technical:.2f} | Fund: {active_profile.weight_fundamental:.2f} | Sent: {active_profile.weight_sentiment:.2f}")

# 3. Degraded Mode & Edge-Case Simulator (Hackathon Requirement!)
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Degraded Mode & Fault Ingestion")
st.sidebar.caption("Simulate real-world data failures and signal conflicts")

sim_feed_fail = st.sidebar.checkbox("💥 Simulate Market Feed Outage", value=False, help="Simulates price feed drop to test technical fallback.")
sim_missing_rag = st.sidebar.checkbox("📑 Simulate Missing SEBI Filing", value=False, help="Simulates missing disclosure to test RAG grounding penalty.")
sim_conflict = st.sidebar.checkbox("⚡ Inject Cross-Agent Signal Conflict", value=False, help="Simulates conflicting sentiment/funda signals against technical trend.")

context_flags = {
    "simulate_feed_failure": sim_feed_fail,
    "simulate_missing_filing": sim_missing_rag,
    "simulate_signal_conflict": sim_conflict
}

# ----------------- RUN SYNTHESIS -----------------
with st.spinner("🤖 Dispatching parallel reasoning agents across market feeds & SEBI filings..."):
    intelligence = orchestrator.synthesize(
        symbol=selected_ticker,
        user_profile=active_profile,
        context=context_flags
    )

stock_data = market_feed.get_stock_data(selected_ticker) or {}

# ----------------- HEADER BAR -----------------
col_hdr1, col_hdr2, col_hdr3, col_hdr4 = st.columns([3, 1.2, 1.2, 1.2])

with col_hdr1:
    st.markdown(f"# {stock_data.get('name', selected_ticker)} (`NSE: {selected_ticker}`)")
    st.caption(f"Sector: **{stock_data.get('sector', 'N/A')}** | Active Profile: **{active_profile.name}**")

with col_hdr2:
    cmp = stock_data.get("cmp", 0.0)
    chg = stock_data.get("change_pct", 0.0)
    chg_color = "normal" if chg >= 0 else "inverse"
    st.metric("Current Market Price (CMP)", f"₹{cmp:,.2f}", f"{chg:+.2f}%")

with col_hdr3:
    st.metric("Pipeline Latency", f"{intelligence.session_metrics.total_pipeline_latency_ms:.1f} ms", "Sub-60s SLA ✅")

with col_hdr4:
    st.metric("Citation Grounding", f"{intelligence.session_metrics.rag_citation_grounding_score:.0f}%", "SEBI Attributed")

# ----------------- FAULT / CONFLICT ALERTS -----------------
if intelligence.degraded_mode_active:
    st.warning(f"⚠️ **Degraded State Active:** {intelligence.degraded_mode_details}. Output confidence adjusted accordingly.")

if intelligence.conflict_detected:
    st.error(f"⚡ **Cross-Agent Conflict Resolved:** {intelligence.conflict_explanation}")

# ----------------- MAIN TABS -----------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎯 Synthesized Guidance",
    "🤖 Parallel Agents Breakdown",
    "📊 Technical Chart & Signals",
    "📑 SEBI Filing RAG Corpus",
    "👥 Persona Comparison Matrix",
    "📈 Risk & Latency Analytics"
])

# ================= TAB 1: SYNTHESIZED GUIDANCE =================
with tab1:
    col_act1, col_act2 = st.columns([2.2, 1])

    with col_act1:
        st.markdown("### 🎯 Tailored Decision Intelligence")
        
        # Action badge styling
        action_name = intelligence.action
        if "BUY" in action_name or "ACCUMULATE" in action_name:
            badge_class = "action-badge-bull"
        elif "SELL" in action_name or "AVOID" in action_name or "SHORT" in action_name:
            badge_class = "action-badge-bear"
        else:
            badge_class = "action-badge-neutral"

        st.markdown(f"<div class='{badge_class}'>ACTION: {action_name.replace('_', ' ')}</div>", unsafe_allow_html=True)
        st.markdown("")
        
        st.markdown(f"**Executive Thesis:** {intelligence.executive_summary}")
        
        st.info(f"💡 **Personalized Reasoning for {active_profile.name}:**\n\n{intelligence.personalized_rationale}")

        # Behavioral and Safety Alerts
        if intelligence.behavioral_alerts:
            st.markdown("#### 🧠 Behavioral & Psychological Safeguards")
            for alert in intelligence.behavioral_alerts:
                st.warning(alert)

        # Mandatory Retail Guardrails
        st.markdown("#### 🛡️ Actionable Risk Guardrails & Execution Rules")
        for g in intelligence.guardrails:
            st.markdown(f"- {g}")

    with col_act2:
        st.markdown("### 🧭 Trade Execution Plan")
        st.markdown(f"""
        <div class='metric-card'>
            <p style='color: #94a3b8; font-size: 0.85rem; margin-bottom: 4px;'>RECOMMENDED ENTRY ZONE</p>
            <h3 style='color: #38bdf8; margin: 0;'>{intelligence.target_entry_range}</h3>
            <hr style='border-color: #334155; margin: 10px 0;'>
            <p style='color: #94a3b8; font-size: 0.85rem; margin-bottom: 4px;'>STOP-LOSS / INVALIDATION</p>
            <h3 style='color: #f87171; margin: 0;'>{intelligence.suggested_stop_loss}</h3>
            <hr style='border-color: #334155; margin: 10px 0;'>
            <p style='color: #94a3b8; font-size: 0.85rem; margin-bottom: 4px;'>CONFIDENCE SCORE</p>
            <h2 style='color: #34d399; margin: 0;'>{intelligence.composite_confidence_pct}%</h2>
            <p style='color: #94a3b8; font-size: 0.8rem;'>Risk Rating: {intelligence.risk_score}/10</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 💼 User Portfolio Context")
        user_alloc = active_profile.get_stock_allocation_pct(selected_ticker)
        st.progress(min(1.0, user_alloc / 100.0), text=f"Current {selected_ticker} Allocation: {user_alloc:.1f}%")
        st.write(f"Total Portfolio Net Worth: **₹{active_profile.portfolio_total_value:,.2f}**")
        st.write(f"Available Cash Buffer: **₹{active_profile.cash_balance:,.2f}**")

    # Reasoning Trace Waterfall
    st.markdown("---")
    st.markdown("### 🪜 Transparent Multi-Agent Reasoning Waterfall")
    st.caption("Verifiable audit trail from raw data ingestion to synthesized recommendation:")
    
    for step in intelligence.reasoning_trace_waterfall:
        st.markdown(f"""
        <div class='waterfall-step'>
            <b style='color: #818cf8;'>{step['stage']}</b><br>
            <span style='color: #cbd5e1;'>{step['detail']}</span>
        </div>
        """, unsafe_allow_html=True)

# ================= TAB 2: PARALLEL AGENTS BREAKDOWN =================
with tab2:
    st.markdown("### 🤖 Parallel Specialized Agent Reasoning Desks")
    st.caption("Each agent executes independently with strict typed output contracts and latency tracking.")

    col_ag1, col_ag2, col_ag3 = st.columns(3)

    # Technical Agent Column
    with col_ag1:
        t_out = intelligence.agent_outputs["technical"]
        st.markdown(f"""
        <div class='agent-card' style='border-left-color: #38bdf8;'>
            <h4 style='color: #38bdf8; margin-top: 0;'>📈 Technical & Momentum</h4>
            <p><b>Stance:</b> <code>{t_out.stance}</code> (Score: {t_out.score:+.2f})</p>
            <p><b>Confidence:</b> {t_out.confidence*100:.1f}% | <b>Latency:</b> {t_out.execution_time_ms:.1f}ms</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**Key Quant Findings:**")
        for f in t_out.key_findings:
            st.markdown(f"• {f}")

    # Fundamental Agent Column
    with col_ag2:
        f_out = intelligence.agent_outputs["fundamental"]
        st.markdown(f"""
        <div class='agent-card' style='border-left-color: #10b981;'>
            <h4 style='color: #10b981; margin-top: 0;'>📑 Fundamental & RAG</h4>
            <p><b>Stance:</b> <code>{f_out.stance}</code> (Score: {f_out.score:+.2f})</p>
            <p><b>Confidence:</b> {f_out.confidence*100:.1f}% | <b>Latency:</b> {f_out.execution_time_ms:.1f}ms</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**Valuation & SEBI Insights:**")
        for f in f_out.key_findings:
            st.markdown(f"• {f}")

        if f_out.citations:
            st.markdown("**Grounded RAG Citations:**")
            for c in f_out.citations:
                if "source_tag" in c:
                    st.markdown(f"<div class='citation-box'><b>{c['source_tag']}</b> (Relevance: {c.get('relevance_score', 0):.2f})<br><i>\"{c.get('snippet', '')}\"</i></div>", unsafe_allow_html=True)

    # Sentiment Agent Column
    with col_ag3:
        s_out = intelligence.agent_outputs["sentiment"]
        st.markdown(f"""
        <div class='agent-card' style='border-left-color: #f59e0b;'>
            <h4 style='color: #f59e0b; margin-top: 0;'>🌊 Sentiment & Microstructure</h4>
            <p><b>Stance:</b> <code>{s_out.stance}</code> (Score: {s_out.score:+.2f})</p>
            <p><b>Confidence:</b> {s_out.confidence*100:.1f}% | <b>Latency:</b> {s_out.execution_time_ms:.1f}ms</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**Flows & Derivatives Insights:**")
        for f in s_out.key_findings:
            st.markdown(f"• {f}")

# ================= TAB 3: TECHNICAL CHART & SIGNALS =================
with tab3:
    st.markdown("### 📊 Real-Time Candlestick Chart & Technical Indicators")
    
    df_candles = market_feed.generate_historical_candles(selected_ticker, periods=60)
    
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.06, row_heights=[0.7, 0.3])
    
    # Candlestick
    fig.add_trace(go.Candlestick(
        x=df_candles["Date"],
        open=df_candles["Open"],
        high=df_candles["High"],
        low=df_candles["Low"],
        close=df_candles["Close"],
        name="OHLC Price"
    ), row=1, col=1)
    
    # EMAs
    fig.add_trace(go.Scatter(x=df_candles["Date"], y=df_candles["EMA20"], line=dict(color='#38bdf8', width=1.5), name="20 EMA"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_candles["Date"], y=df_candles["EMA50"], line=dict(color='#f59e0b', width=1.5), name="50 EMA"), row=1, col=1)
    
    # Volume Bar
    colors = ['#10b981' if c >= o else '#ef4444' for c, o in zip(df_candles["Close"], df_candles["Open"])]
    fig.add_trace(go.Bar(x=df_candles["Date"], y=df_candles["Volume"], marker_color=colors, name="Volume"), row=2, col=1)
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b0f19",
        plot_bgcolor="#111827",
        height=520,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_rangeslider_visible=False
    )
    st.plotly_chart(fig, use_container_width=True)

    # Multi-Dimensional Signal Screener Table
    st.markdown("#### 🔍 Multi-Dimensional Market Signal Screener (Entire Universe)")
    screener_rows = []
    for t in tickers:
        sig = market_feed.evaluate_multi_dimensional_signals(t)
        screener_rows.append({
            "Symbol": sig.symbol,
            "CMP (₹)": f"₹{sig.cmp:,.2f}",
            "Change %": f"{sig.change_pct:+.2f}%",
            "RSI (14)": f"{sig.rsi_14:.1f}",
            "MACD Trend": sig.macd_stance.split()[0],
            "Volume Spike": f"{sig.volume_spike_ratio:.2f}x",
            "Options PCR": f"{sig.options_pcr:.2f}",
            "Composite Signal": sig.overall_signal,
            "Confidence": f"{sig.confidence_score*100:.0f}%"
        })
    st.dataframe(pd.DataFrame(screener_rows), use_container_width=True, hide_index=True)

# ================= TAB 4: SEBI FILING RAG CORPUS =================
with tab4:
    st.markdown("### 📑 Grounded Regulatory Corpus & SEBI LODR Filings")
    st.caption("Verifiable repository of corporate disclosures, earnings concall transcripts, and debt covenants.")

    rag_query = st.text_input("🔍 Search Regulatory Corpus (Semantic Query):", value=f"{selected_ticker} debt capex revenue margin")
    
    if rag_query:
        query_res = rag_engine.query(symbol=selected_ticker, query_text=rag_query, top_k=4)
        if query_res:
            for r in query_res:
                c = r.chunk
                with st.expander(f"📄 {c.source_tag} — Relevance Match: {r.relevance_score*100:.1f}%", expanded=True):
                    st.write(f"**Company:** {c.company_name} (`{c.company_symbol}`)")
                    st.write(f"**Filing Type:** {c.filing_type} | **Date:** {c.date}")
                    st.write(f"**Section:** `{c.section_title}`")
                    st.markdown(f"```\n{c.content}\n```")
        else:
            st.info("No matching document chunks found for the specified query.")

# ================= TAB 5: PERSONA COMPARISON MATRIX =================
with tab5:
    st.markdown("### 👥 Dynamic Persona Comparison Matrix (Judges' Demo)")
    st.caption(f"Demonstrating completely distinct, tailored guidance on **{selected_ticker}** across 4 different retail risk profiles:")

    persona_cols = st.columns(4)
    for idx, (p_key, p_obj) in enumerate(preset_profiles.items()):
        with persona_cols[idx]:
            p_intel = orchestrator.synthesize(selected_ticker, p_obj, context_flags)
            
            st.markdown(f"""
            <div class='metric-card'>
                <h4 style='color: #818cf8; margin-top: 0;'>{p_obj.name.split('(')[0].strip()}</h4>
                <p style='color: #94a3b8; font-size: 0.85rem;'>Profile: <b>{p_obj.risk_category}</b></p>
                <hr style='border-color: #334155; margin: 8px 0;'>
                <p style='color: #38bdf8; font-size: 0.95rem; font-weight: bold;'>{p_intel.action.replace('_', ' ')}</p>
                <p style='font-size: 0.85rem; color: #cbd5e1;'>Confidence: <b>{p_intel.composite_confidence_pct}%</b></p>
                <hr style='border-color: #334155; margin: 8px 0;'>
                <p style='font-size: 0.8rem; color: #94a3b8;'><i>\"{p_intel.executive_summary[:130]}...\"</i></p>
            </div>
            """, unsafe_allow_html=True)

# ================= TAB 6: RISK & LATENCY ANALYTICS =================
with tab6:
    st.markdown("### 📈 Session Performance, Latency & Risk Concentration")
    st.caption("Capturing measurable SLA metrics, portfolio Value-at-Risk (VaR), and backtest win-rates.")

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("Total Pipeline Latency", f"{intelligence.session_metrics.total_pipeline_latency_ms:.1f} ms", "Target: < 500ms")
    with col_m2:
        st.metric("Portfolio Concentration (HHI)", f"{intelligence.session_metrics.portfolio_concentration_score:.1f} / 100", "Risk Index")
    with col_m3:
        st.metric("1-Day Parametric VaR (95%)", f"{intelligence.session_metrics.portfolio_var_95_pct:.2f}%", "Max Daily Drawdown")
    with col_m4:
        st.metric("Simulated Win Rate", f"{intelligence.session_metrics.backtest_win_rate_pct:.1f}%", "30-Day Forward Est.")

    st.markdown("#### 📜 Session History Log")
    history_records = logger.get_recent_history(limit=8)
    if history_records:
        rec_data = []
        for r in history_records:
            rec_data.append({
                "Symbol": r.symbol,
                "User Persona": r.user_profile_name.split('(')[0],
                "Total Latency (ms)": f"{r.total_pipeline_latency_ms:.1f}",
                "Tech Latency (ms)": f"{r.agent_latencies_ms.get('technical', 0):.1f}",
                "Funda Latency (ms)": f"{r.agent_latencies_ms.get('fundamental', 0):.1f}",
                "Sent Latency (ms)": f"{r.agent_latencies_ms.get('sentiment', 0):.1f}",
                "Concentration HHI": f"{r.portfolio_concentration_score:.1f}",
                "1-Day VaR (95%)": f"{r.portfolio_var_95_pct:.2f}%",
                "RAG Grounding %": f"{r.rag_citation_grounding_score:.0f}%"
            })
        st.dataframe(pd.DataFrame(rec_data), use_container_width=True, hide_index=True)

# ----------------- FOOTER -----------------
st.markdown("---")
st.caption("IEEE Robotics & Automation Society · VIT Chennai | Hackverse 2026 PS-01 Multi-Agent Financial Intelligence System")
