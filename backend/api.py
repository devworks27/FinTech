"""
FinIntel REST API Server (FastAPI)
Provides programmatic REST endpoints for multi-agent synthesis, market data feeds, and RAG retrieval.
"""

import sys
import os
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

# Ensure backend path is accessible
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from core.market_feed import MarketFeed
from core.rag_engine import RAGEngine
from core.user_profile import get_preset_profiles, UserProfile
from core.metrics_logger import MetricsLogger
from agents.technical_agent import TechnicalAnalystAgent
from agents.fundamental_agent import FundamentalRAGAgent
from agents.sentiment_agent import SentimentMicrostructureAgent
from agents.synthesis_orchestrator import MultiAgentSynthesisOrchestrator

app = FastAPI(
    title="FinIntel Multi-Agent Financial Intelligence API",
    version="1.0.0",
    description="REST backend for PS-01 Multi-Agent Financial Intelligence System"
)

# Enable CORS for external frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
market_feed = MarketFeed()
rag_engine = RAGEngine()
tech_agent = TechnicalAnalystAgent(market_feed)
fund_agent = FundamentalRAGAgent(rag_engine, market_feed)
sent_agent = SentimentMicrostructureAgent(market_feed)
metrics_logger = MetricsLogger()
orchestrator = MultiAgentSynthesisOrchestrator(tech_agent, fund_agent, sent_agent, metrics_logger)
preset_profiles = get_preset_profiles()

class SynthesizeRequest(BaseModel):
    symbol: str = Field(..., example="RELIANCE")
    persona: str = Field("MODERATE", example="CONSERVATIVE")  # CONSERVATIVE, MODERATE, AGGRESSIVE, FO_TRADER
    simulate_feed_failure: bool = False
    simulate_missing_filing: bool = False
    simulate_signal_conflict: bool = False

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "supported_tickers": market_feed.get_supported_tickers(),
        "indexed_sebi_chunks": len(rag_engine.chunks)
    }

@app.get("/api/stocks")
def get_stocks():
    """Returns list of supported stocks and their latest metrics."""
    stocks = {}
    for ticker in market_feed.get_supported_tickers():
        stocks[ticker] = market_feed.get_stock_data(ticker)
    return {"stocks": stocks}

@app.get("/api/signals/{symbol}")
def get_stock_signal(symbol: str):
    """Evaluates multi-dimensional quantitative market signals."""
    sym = symbol.upper()
    try:
        sig = market_feed.evaluate_multi_dimensional_signals(sym)
        return {
            "symbol": sig.symbol,
            "cmp": sig.cmp,
            "change_pct": sig.change_pct,
            "rsi_14": sig.rsi_14,
            "macd_stance": sig.macd_stance,
            "volume_spike_ratio": sig.volume_spike_ratio,
            "options_pcr": sig.options_pcr,
            "overall_signal": sig.overall_signal,
            "confidence_score": sig.confidence_score,
            "rationale": sig.rationale_points
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/rag/search")
def search_rag_corpus(symbol: str, query: str = Query(..., min_length=2)):
    """Queries grounded SEBI corporate filings and returns top matching chunks with citations."""
    results = rag_engine.query(symbol=symbol.upper(), query_text=query, top_k=4)
    return {
        "symbol": symbol.upper(),
        "query": query,
        "results": [
            {
                "citation": r.citation_text,
                "relevance_score": r.relevance_score,
                "section": r.chunk.section_title,
                "snippet": r.chunk.content
            }
            for r in results
        ]
    }

@app.post("/api/synthesize")
def synthesize_intelligence(req: SynthesizeRequest):
    """Runs parallel multi-agent reasoning and produces personalized advice with audit trail."""
    sym = req.symbol.upper()
    if sym not in market_feed.get_supported_tickers():
        raise HTTPException(status_code=404, detail=f"Symbol {sym} not found in market universe.")

    profile = preset_profiles.get(req.persona.upper(), preset_profiles["MODERATE"])
    context = {
        "simulate_feed_failure": req.simulate_feed_failure,
        "simulate_missing_filing": req.simulate_missing_filing,
        "simulate_signal_conflict": req.simulate_signal_conflict
    }

    intelligence = orchestrator.synthesize(symbol=sym, user_profile=profile, context=context)

    return {
        "symbol": intelligence.symbol,
        "user_profile": intelligence.user_profile_name,
        "risk_category": intelligence.risk_category,
        "action": intelligence.action,
        "confidence_pct": intelligence.composite_confidence_pct,
        "risk_score": intelligence.risk_score,
        "executive_summary": intelligence.executive_summary,
        "personalized_rationale": intelligence.personalized_rationale,
        "target_entry_range": intelligence.target_entry_range,
        "suggested_stop_loss": intelligence.suggested_stop_loss,
        "guardrails": intelligence.guardrails,
        "behavioral_alerts": intelligence.behavioral_alerts,
        "conflict_detected": intelligence.conflict_detected,
        "conflict_explanation": intelligence.conflict_explanation,
        "degraded_mode_active": intelligence.degraded_mode_active,
        "degraded_mode_details": intelligence.degraded_mode_details,
        "reasoning_trace_waterfall": intelligence.reasoning_trace_waterfall,
        "pipeline_latency_ms": intelligence.session_metrics.total_pipeline_latency_ms
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
