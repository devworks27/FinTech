# 📈 FinIntel: Multi-Agent Autonomous Financial Intelligence System for Retail Investors

[![Hackverse 2026](https://img.shields.io/badge/Hackathon-Hackverse%202026-blue.svg)](https://vit.ac.in)
[![Track](https://img.shields.io/badge/Problem%20Statement-PS--01%20Financial%20Intelligence-emerald.svg)]()
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com)
[![Status](https://img.shields.io/badge/Tests-100%25%20Passing-brightgreen.svg)]()

> **IEEE Robotics & Automation Society · VIT Chennai Student Chapter**  
> **HACKVERSE: INTO THE WEB · 24-Hour Hackathon · Sprint 1 (Rapid Vibe Coding)**

---

## 📌 Problem Context & The Retail Gap

India added over **130 million new retail investors** in four years, with 80% under the age of 30. However, SEBI’s 2024 data reveals that **89% of retail F&O participants lose capital**. 

The fundamental failure is not a lack of public financial data — NSE price feeds, SEBI LODR corporate disclosures, FII/DII institutional flows, and options chain metrics are all public. The failure lies in the **decision intelligence gap**:
* **Hedge funds** deploy parallel analyst desks running simultaneous research across technicals, fundamentals, sentiment, and macro risk before committing capital.
* **Retail investors** get a raw candlestick chart and an unverified Telegram/social media tip.

**FinIntel** bridges this infrastructure gap by providing an orchestrated, multi-agent reasoning layer that pulls from multiple data feeds simultaneously, grounds advice in official SEBI regulatory filings, weights recommendations against the user's specific risk profile, and delivers explainable, citation-backed intelligence in **under 50 milliseconds**.

---

## 🏗️ System Architecture

```
                                      ┌────────────────────────────────────────┐
                                      │        Raw Market & Macro Feeds        │
                                      └───────────────────┬────────────────────┘
                                                          │
                    ┌─────────────────────────────────────┼─────────────────────────────────────┐
                    │                                     │                                     │
                    ▼                                     ▼                                     ▼
        ┌───────────────────────┐             ┌───────────────────────┐             ┌───────────────────────┐
        │   Agent 1: Technical   │             │   Agent 2: RAG &      │             │   Agent 3: Sentiment  │
        │   & Momentum Analyst  │             │   Fundamental Analyst │             │   & Microstructure    │
        └───────────┬───────────┘             └───────────┬───────────┘             └───────────┬───────────┘
                    │                                     │                                     │
            [RSI, MACD, EMAs,                     [SEBI Filings RAG,                    [FII/DII Net Flows,
             Volume Spikes]                        P/E Discount, Debt]                   Options PCR, News]
                    │                                     │                                     │
                    └─────────────────────────────────────┼─────────────────────────────────────┘
                                                          │
                                                          ▼
                                      ┌────────────────────────────────────────┐
                                      │   Behavioral Synthesis Orchestrator    │
                                      │   & Cross-Agent Conflict Resolver      │
                                      └───────────────────▲────────────────────┘
                                                          │
                                              ┌───────────┴───────────┐
                                              │ User Behavioral Profile│
                                              │ (Conservative/Aggressive)
                                              └───────────────────────┘
                                                          │
                    ┌─────────────────────────────────────┴─────────────────────────────────────┐
                    ▼                                                                           ▼
        ┌───────────────────────┐                                                   ┌───────────────────────┐
        │  Personalized Advice  │                                                   │  Risk & SLA Telemetry │
        │  & Reasoning Trace    │                                                   │  (VaR, HHI, Latency)  │
        └───────────────────────┘                                                   └───────────────────────┘
```

---

## ✨ Key Features & Capabilities

### 1. 🔍 Multi-Dimensional Signal Classification Module
Evaluates every listed equity across three independent quantitative dimensions:
* **Dimension 1 (Price Momentum & Trend)**: 14-period RSI, 20/50/200 EMA golden/death crosses, MACD histogram divergence.
* **Dimension 2 (Volume Anomaly & Microstructure)**: Real-time volume breakout multiplier vs 20-DMA, On-Balance Volume (OBV).
* **Dimension 3 (Derivatives & Institutional Positioning)**: Put-Call Ratio (PCR), Max Pain strike floor, net FII/DII daily cash flows.

### 2. 📑 Grounded RAG with SEBI Corporate Disclosures
* Semantic chunking and indexing of official SEBI Regulation 30 filings, quarterly earnings call transcripts, and Capex disclosures for major Indian equities (`RELIANCE`, `TATASTEEL`, `HDFCBANK`, `TCS`, `INFY`, `ZOMATO`).
* Every fundamental claim includes an exact attribution tag (e.g. `[RELIANCE SEBI Filing 2025-10-18 § 4. Oil-to-Chemicals & Capex]`).

### 3. 🤖 Parallel Specialized Agent Execution
* **Technical Analyst Desk**: Quant price action, overbought/oversold boundaries, and momentum indicators.
* **Fundamental & RAG Desk**: Valuation multiples (P/E vs sector), debt-to-equity ratios, and grounded filing citations.
* **Sentiment Desk**: FII/DII capital flows, Options PCR sentiment, and financial news polarity.
* **Synthesis Orchestrator**: Unifies agent contracts into a tailored investment action.

### 4. 👥 Dynamic User Profiling Engine (Hackathon Highlight)
Produces demonstrably different, justified recommendations for different personas on the **exact same market data**:
* **Conservative (Ramesh - Capital Preservation)**: Heavily weights fundamental health and dividend yield; enforces strict 5% risk guardrails.
* **Moderate (Priya - Balanced Growth)**: Balances technicals and fundamentals for 2–5 year horizon.
* **Aggressive (Arjun - Alpha Momentum)**: Chases volume breakouts, high-beta setups with tight 4% stop-losses.
* **F&O Trader (Vikram - Derivatives)**: Synthesizes PCR and Max Pain to recommend defined-risk option spreads.

### 5. ⚡ Degraded Mode & Signal Conflict Resolution
* **Feed Outage Fallback**: Gracefully degrades to baseline metrics with explicit confidence penalty tags when live feeds disconnect.
* **Conflict Resolution Protocol**: When technicals and fundamentals clash (e.g. Technical 90% Bullish vs Fundamental 80% Bearish), the orchestrator flags a **Divergence Alert** rather than producing a meaningless average.

### 6. 📊 Real-Time Risk & Telemetry Logging
* **Latency Tracker**: Captures per-agent and end-to-end pipeline execution times (<50ms SLA).
* **Portfolio Concentration**: Herfindahl-Hirschman Index (HHI) score.
* **Value-at-Risk (VaR)**: 1-Day Parametric 95% maximum drawdown estimate.

---

## 📁 Repository Structure

```
fin_intel_system/
│
├── frontend/                          # Presentation & Interactive UI Layer
│   └── app.py                         # Streamlit dark fintech UI dashboard
│
├── backend/                           # Engine & Service Layer
│   ├── api.py                         # FastAPI REST Endpoints (Synthesize, Signals, RAG)
│   ├── test_pipeline.py               # Automated verification test suite
│   │
│   ├── core/                          # Quantitative Core Modules
│   │   ├── market_feed.py             # 3D Signal Classifier & Candlestick Generator
│   │   ├── rag_engine.py              # Semantic chunking & SEBI citation grounding
│   │   ├── user_profile.py            # Personas & Behavioral bias detector
│   │   └── metrics_logger.py          # SLA Latency, HHI Concentration & VaR 95%
│   │
│   ├── agents/                        # Parallel Reasoning Agent Desks
│   │   ├── base_agent.py              # Strict typed output schemas
│   │   ├── technical_agent.py         # RSI, MACD, Volume Spikes, EMA Trend
│   │   ├── fundamental_agent.py       # P/E valuation & grounded SEBI disclosures
│   │   ├── sentiment_agent.py         # Options PCR, Max Pain & FII/DII Net Flows
│   │   └── synthesis_orchestrator.py   # Multi-agent weighted synthesis & conflict engine
│   │
│   └── data/                          # Ground Truth Document & Market Store
│       ├── market_universe.json       # Stock metadata, beta, options PCR, flows
│       └── sebi_filings/              # Real-world SEBI LODR corporate filings
│           ├── reliance_q3_disclosure.txt
│           ├── tatasteel_debt_update.txt
│           ├── hdfcbank_merger_filing.txt
│           ├── tcs_tcv_quarterly.txt
│           ├── infy_guidance_report.txt
│           └── zomato_profitability_filing.txt
│
├── run_app.bat                        # Windows one-click startup script
├── requirements.txt                   # Unified dependencies
├── judges_brief.md                    # Architecture documentation for judges
└── README.md                          # Project overview and guide
```

---

## 🚀 Quick Start & Installation

### Prerequisites
* Python 3.10+ (Python 3.12 recommended)
* `pip` package manager

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/your-team/fin_intel_system.git
cd fin_intel_system

pip install -r requirements.txt
```

### 2. Run Automated Verification Tests
Verify all 9 minimum problem statement requirements with zero external dependencies:
```bash
python backend/test_pipeline.py
```

### 3. Launch the Interactive Frontend Dashboard
```bash
streamlit run frontend/app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser.

*(On Windows, you can also simply double-click `run_app.bat`)*

### 4. (Optional) Run the Backend REST API Server
```bash
python -m uvicorn backend.api:app --reload --port 8000
```
API Documentation will be live at: **[http://localhost:8000/docs](http://localhost:8000/docs)**.

---

## 📡 REST API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | System status, indexed SEBI chunk count, supported equities |
| `GET` | `/api/stocks` | Full market universe with CMP, volume, and fundamentals |
| `GET` | `/api/signals/{symbol}` | Multi-dimensional 3D signal classification breakdown |
| `GET` | `/api/rag/search` | Grounded semantic search over SEBI corporate disclosures |
| `POST` | `/api/synthesize` | Multi-agent synthesized advice tailored to user persona |

#### Sample Synthesis Request (`POST /api/synthesize`):
```json
{
  "symbol": "RELIANCE",
  "persona": "CONSERVATIVE",
  "simulate_feed_failure": false,
  "simulate_missing_filing": false,
  "simulate_signal_conflict": false
}
```

---

## 🎯 3-Minute Hackathon Demo Script for Judges

1. **The Hook (0:00 - 0:30)**:
   - Introduce the retail dilemma in India: 130M+ retail investors, 89% F&O loss rate.
   - Explain the core differentiator: FinIntel is an orchestrated multi-agent reasoning layer that bridges raw data to defensible retail decisions.
2. **Live Multi-Agent Reasoning (0:30 - 1:15)**:
   - Select `RELIANCE` on the UI.
   - Show the sub-50ms latency, the **Reasoning Trace Waterfall**, and the target entry/stop-loss zones.
3. **Dynamic Persona Matrix (1:15 - 2:00)**:
   - Click on **Tab 5 (Persona Comparison Matrix)**.
   - Demonstrate how the *exact same market feed* generates **SIP Accumulation** for Conservative Ramesh, **Alpha Long** for Aggressive Arjun, and a **Bull Put Spread** for F&O Vikram.
4. **SEBI RAG Grounding (2:00 - 2:30)**:
   - Switch to **Tab 4 (SEBI Filing Corpus)**.
   - Show verified clause citations linking balance sheet safety directly to SEBI LODR filings.
5. **Fault Injection & Conflict Handling (2:30 - 3:00)**:
   - Toggle **"Simulate Feed Outage"** and **"Inject Cross-Agent Conflict"** in the sidebar.
   - Show that the system warns the user, penalizes uncertainty, and never hallucinates ungrounded advice.

---

## 📜 Compliance & SEBI Disclaimer
*This system is built as an academic and hackathon prototype for Hackverse 2026. All recommendations and metrics are for informational and educational demonstration purposes only and do not constitute registered investment advice under SEBI (Investment Advisers) Regulations, 2013.*
