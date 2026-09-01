@echo off
echo =======================================================
echo Starting FinIntel Multi-Agent Financial Intelligence System
echo =======================================================
cd /d "%~dp0"
python -m streamlit run frontend\app.py
pause
