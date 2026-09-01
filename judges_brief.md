# PS-01: Multi-Agent Autonomous Financial Intelligence System
**Hackverse: Into the Web · 24-Hour Hackathon · VIT Chennai (2026)**
**Team Architecture Dossier & Judge Evaluation Brief**

---

## 1. Project Organization (Clean Frontend / Backend Separation)

```
fin_intel_system/
│
├── frontend/                          # Presentation & Interactive UI Layer
│   └── app.py                         # Streamlit dark fintech UI dashboard
│
├── backend/                           # Core Analytical Engine & REST Services
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
├── run_app.bat                        # One-click Windows startup script
├── requirements.txt                   # Project dependencies
└── judges_brief.md                    # Technical documentation
```

---

## 2. Multi-Agent System Architecture

```
[Raw NSE Feeds & Candlesticks] ───► [Agent 1: Technical & Momentum Analyst] ──┐
                                                                              │
[SEBI Filings & Concall Corpus] ──► [Agent 2: Fundamental & RAG Analyst] ────┼──► [Synthesis & Risk Orchestrator]
                                                                              │              ▲
[Options PCR & FII/DII Flows] ───► [Agent 3: Sentiment & Microstructure] ────┘              │
                                                                                 [User Behavioral Profile]
                                                                                (Conservative / Moderate / Aggressive)
                                                                                             │
                                                                                             ▼
                                                                           [Personalized Guidance & Reasoning Trace]
```

### Specialized Agent Contracts:
1. **Technical & Momentum Analyst**: Evaluates price action across 3 quantitative sub-dimensions:
   - Trend alignment (CMP vs 20/50/200 EMA)
   - RSI-14 momentum & MACD histogram expansion
   - Institutional volume spike ratio vs 20-DMA
2. **Fundamental & Regulatory RAG Analyst**:
   - Queries indexed SEBI Regulation 30 corporate filings, debt covenants, and EBITDA margins.
   - Attaches verifiable source tags (e.g., `[RELIANCE SEBI Filing 2025-Q3 § Operational Performance]`).
   - Analyzes P/E discount relative to sector averages.
3. **Sentiment & Market Microstructure Analyst**:
   - Computes derivatives Put-Call Ratio (PCR) and Max Pain price floor.
   - Monitors FII & DII institutional net capital flows (in INR Crores).
   - Ingests verified financial news sentiment polarity.
4. **Behavioral Synthesis & Risk Orchestrator**:
   - Applies dynamic risk-weighting vectors based on individual user profiles.
   - Executes **Conflict Resolution Protocols** when signals diverge.
   - Injects behavioral guardrails (FOMO alerts, over-concentration warnings).

---

## 3. Demonstration of Core Hackathon Requirements

| Requirement | Implementation in FinIntel | Verified Status |
| :--- | :--- | :--- |
| **3-Dimensional Signal Classification** | Classifies price momentum (RSI/MACD), volume anomalies (Spike/OBV), and institutional flow (PCR/FII). | ✅ Implemented & Tested |
| **Grounded RAG with Visible Attribution** | Semantic indexing of SEBI LODR filings with snippet citation tags visible directly in UI. | ✅ Implemented & Tested |
| **Parallel Multi-Agent Architecture** | 3 specialized analytical agents + 1 behavioral synthesis orchestrator with typed data contracts. | ✅ Implemented & Tested |
| **User Profile Differentiation** | Produces demonstrably different actions (SIP vs Momentum vs Options Collar) on identical stock data. | ✅ Implemented & Tested |
| **Live Interactive Interface** | Streamlit fintech dashboard with candlestick charts, agent cards, and reasoning waterfall. | ✅ Implemented & Tested |
| **Performance & Risk SLA Log** | Real-time session tracker: sub-50ms latency, Herfindahl concentration index (HHI), 1-day VaR (95%). | ✅ Implemented & Tested |
| **Degraded Mode & Fault Ingestion** | Handles feed outages, missing filings, and conflicting signals without crashing. | ✅ Implemented & Tested |

---

## 4. Quick Start Commands

```bash
# 1. Run backend verification test suite:
python backend/test_pipeline.py

# 2. Launch the interactive frontend dashboard:
streamlit run frontend/app.py

# 3. (Optional) Run the FastAPI REST backend:
python -m uvicorn backend.api:app --reload --port 8000
```
